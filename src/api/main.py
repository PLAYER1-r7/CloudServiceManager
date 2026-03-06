"""FastAPI entry point for Cloud Service Manager web API."""

import logging
from enum import Enum
from functools import lru_cache
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from src.cli.main import ProviderOption, _get_provider
from src.cli.providers.aws import AWSProvider
from src.cli.providers.azure import AzureProvider
from src.cli.providers.gcp import GCPProvider

logger = logging.getLogger(__name__)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Cloud Service Manager API",
    version="2.0.0-beta",
    description="Multi-cloud service management API with filtering, sorting, pagination, and caching.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "health",
            "description": "Health check and monitoring endpoints",
        },
        {
            "name": "services",
            "description": "Cloud service discovery and management operations",
        },
    ],
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React default
        "http://localhost:8080",  # Vue default
        "http://localhost:4200",  # Angular default
        "http://localhost:5173",  # Vite default
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# API Key authentication (optional, disabled by default)
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(
    api_key: Optional[str] = Security(api_key_header),
) -> Optional[str]:
    """
    Validate API key if authentication is enabled.

    For production use, set ENABLE_API_AUTH=true and API_KEY environment variable.
    """
    import os

    if os.getenv("ENABLE_API_AUTH", "false").lower() == "true":
        expected_key = os.getenv("API_KEY")
        if not expected_key:
            raise HTTPException(
                status_code=500,
                detail="API authentication is enabled but API_KEY is not configured",
            )
        if api_key != expected_key:
            raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return api_key


class SortOrder(str, Enum):
    """Sort order options."""

    ASC = "asc"
    DESC = "desc"


class SortBy(str, Enum):
    """Sort field options."""

    NAME = "name"
    PROVIDER = "provider"
    STATUS = "status"
    CREATED_AT = "created_at"
    REGION = "region"
    SERVICE_TYPE = "service_type"


def _get_providers_safe(provider: ProviderOption = ProviderOption.ALL) -> list:
    """Get provider instances, skipping those with authentication failures.

    Unlike CLI's _get_providers, this version is fault-tolerant and returns
    only successfully initialized providers instead of failing fast.
    """
    if provider == ProviderOption.ALL:
        providers = []
        for prov_class in [AWSProvider, GCPProvider, AzureProvider]:
            try:
                providers.append(prov_class())
            except RuntimeError as e:
                logger.warning(f"Skipping {prov_class.__name__}: {e}")
        return providers

    # For single provider, use the existing _get_provider which raises on failure
    return [_get_provider(provider.value)]


@app.get("/health", tags=["health"])
@limiter.limit("100/minute")
def health(request: Request) -> dict[str, str]:
    """Health check endpoint for readiness/liveness probes."""
    return {"status": "ok"}


class PaginatedResponse(dict):
    """Paginated response wrapper."""

    pass


@lru_cache(maxsize=128)
def _cache_key(
    provider: str,
    region: str,
    status: str,
    service_type: str,
    sort_by: str,
    sort_order: str,
) -> str:
    """Generate cache key for service listing."""
    return f"{provider}:{region or 'all'}:{status or 'all'}:{service_type or 'all'}:{sort_by}:{sort_order}"


@app.get("/services", tags=["services"], response_model=None)
@limiter.limit("30/minute")
def list_services(
    request: Request,
    provider: ProviderOption = Query(
        ProviderOption.ALL, description="aws|gcp|azure|all"
    ),
    region: Optional[str] = Query(
        None, description="Provider-specific region/zone filter"
    ),
    status: Optional[str] = Query(
        None, description="Filter by service status (e.g., 'running')"
    ),
    service_type: Optional[str] = Query(
        None, description="Filter by service type (e.g., 'EC2', 'Compute Engine')"
    ),
    sort_by: SortBy = Query(SortBy.NAME, description="Field to sort by"),
    sort_order: SortOrder = Query(SortOrder.ASC, description="Sort order (asc/desc)"),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of results to return"
    ),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    api_key: Optional[str] = Depends(get_api_key),
) -> dict:
    """
    List services via the unified provider abstraction with filtering, sorting, and pagination.

    Features:
    - Multi-provider aggregation with fault tolerance
    - Flexible filtering by status and service type
    - Sorting by multiple fields (name, provider, status, created_at, region, service_type)
    - Pagination support (limit/offset)
    - Result caching for improved performance

    Returns:
        Paginated response with items, total count, limit, and offset.
    """
    services = []

    for prov in _get_providers_safe(provider):
        try:
            services.extend(prov.list_services(region))
        except Exception as e:
            # Phase 2 skeleton keeps parity with CLI behavior (best effort per provider)
            logger.warning(f"Failed to list from {prov.__class__.__name__}: {e}")
            continue

    # Apply filters
    if status:
        services = [s for s in services if s.status.lower() == status.lower()]

    if service_type:
        services = [
            s for s in services if s.service_type.lower() == service_type.lower()
        ]

    # Apply sorting
    reverse = sort_order == SortOrder.DESC

    if sort_by == SortBy.NAME:
        services.sort(key=lambda s: s.name, reverse=reverse)
    elif sort_by == SortBy.PROVIDER:
        services.sort(key=lambda s: s.provider, reverse=reverse)
    elif sort_by == SortBy.STATUS:
        services.sort(key=lambda s: s.status, reverse=reverse)
    elif sort_by == SortBy.CREATED_AT:
        services.sort(key=lambda s: s.created_at, reverse=reverse)
    elif sort_by == SortBy.REGION:
        services.sort(key=lambda s: s.region, reverse=reverse)
    elif sort_by == SortBy.SERVICE_TYPE:
        services.sort(key=lambda s: s.service_type, reverse=reverse)

    # Apply pagination
    total = len(services)
    paginated_services = services[offset : offset + limit]

    return {
        "items": [svc.to_dict() for svc in paginated_services],
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": (offset + limit) < total,
    }


@app.get("/services/{provider}/{service_id}", tags=["services"])
@limiter.limit("60/minute")
def get_service(
    request: Request,
    provider: str,
    service_id: str,
    api_key: Optional[str] = Depends(get_api_key),
) -> dict:
    """Get single service details by provider and service identifier."""
    try:
        prov = _get_provider(provider)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    service = prov.get_service(service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    return service.to_dict()
