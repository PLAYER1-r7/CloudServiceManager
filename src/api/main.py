"""FastAPI entry point for Cloud Service Manager web API."""

import logging
from typing import Optional

from fastapi import FastAPI, HTTPException, Query

from src.cli.main import ProviderOption, _get_provider
from src.cli.providers.aws import AWSProvider
from src.cli.providers.azure import AzureProvider
from src.cli.providers.gcp import GCPProvider

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Cloud Service Manager API",
    version="2.0.0-alpha",
    description="Phase 2 API skeleton built on top of existing provider implementations.",
)


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


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint for readiness/liveness probes."""
    return {"status": "ok"}


@app.get("/services")
def list_services(
    provider: ProviderOption = Query(ProviderOption.ALL, description="aws|gcp|azure|all"),
    region: Optional[str] = Query(None, description="Provider-specific region/zone filter"),
) -> list[dict]:
    """List services via the unified provider abstraction."""
    services = []

    for prov in _get_providers_safe(provider):
        try:
            services.extend(prov.list_services(region))
        except Exception as e:
            # Phase 2 skeleton keeps parity with CLI behavior (best effort per provider)
            logger.warning(f"Failed to list from {prov.__class__.__name__}: {e}")
            continue

    return [svc.to_dict() for svc in services]


@app.get("/services/{provider}/{service_id}")
def get_service(provider: str, service_id: str) -> dict:
    """Get single service details by provider and service identifier."""
    try:
        prov = _get_provider(provider)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    service = prov.get_service(service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    return service.to_dict()
