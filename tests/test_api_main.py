"""Tests for Phase 2 FastAPI skeleton endpoints."""

from datetime import datetime, timezone

from fastapi.testclient import TestClient

import src.api.main as api_main
from src.cli.models.service import CloudService

client = TestClient(api_main.app)


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_services_endpoint(monkeypatch) -> None:
    service = CloudService(
        provider="aws",
        service_type="EC2",
        name="i-api-001",
        region="us-east-1",
        status="running",
        created_at=_now_iso(),
        metadata={"instance_type": "t3.micro"},
    )

    class ProviderMock:
        def list_services(self, region=None):
            return [service]

    monkeypatch.setattr(
        api_main, "_get_providers_safe", lambda provider: [ProviderMock()]
    )

    response = client.get("/services?provider=aws")
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 1
    assert payload["limit"] == 100
    assert payload["offset"] == 0
    assert payload["has_more"] is False
    assert len(payload["items"]) == 1
    assert payload["items"][0]["name"] == "i-api-001"


def test_get_service_endpoint(monkeypatch) -> None:
    service = CloudService(
        provider="gcp",
        service_type="Compute Engine",
        name="instance-api-777",
        region="us-central1-a",
        status="RUNNING",
        created_at=_now_iso(),
        metadata={"machine_type": "e2-medium"},
    )

    class ProviderMock:
        def get_service(self, service_id):
            assert service_id == "instance-api-777"
            return service

    monkeypatch.setattr(api_main, "_get_provider", lambda provider: ProviderMock())

    response = client.get("/services/gcp/instance-api-777")
    assert response.status_code == 200
    assert response.json()["name"] == "instance-api-777"


def test_get_service_not_found(monkeypatch) -> None:
    class ProviderMock:
        def get_service(self, service_id):
            return None

    monkeypatch.setattr(api_main, "_get_provider", lambda provider: ProviderMock())

    response = client.get("/services/aws/missing-id")
    assert response.status_code == 404


def test_list_services_with_status_filter(monkeypatch) -> None:
    """Test filtering services by status."""
    services = [
        CloudService(
            provider="aws",
            service_type="EC2",
            name="i-running",
            region="us-east-1",
            status="running",
            created_at=_now_iso(),
            metadata={},
        ),
        CloudService(
            provider="aws",
            service_type="EC2",
            name="i-stopped",
            region="us-east-1",
            status="stopped",
            created_at=_now_iso(),
            metadata={},
        ),
    ]

    class ProviderMock:
        def list_services(self, region=None):
            return services

    monkeypatch.setattr(
        api_main, "_get_providers_safe", lambda provider: [ProviderMock()]
    )

    response = client.get("/services?status=running")
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 1
    assert len(payload["items"]) == 1
    assert payload["items"][0]["name"] == "i-running"
    assert payload["items"][0]["status"] == "running"


def test_list_services_with_service_type_filter(monkeypatch) -> None:
    """Test filtering services by service type."""
    services = [
        CloudService(
            provider="aws",
            service_type="EC2",
            name="i-ec2-001",
            region="us-east-1",
            status="running",
            created_at=_now_iso(),
            metadata={},
        ),
        CloudService(
            provider="gcp",
            service_type="Compute Engine",
            name="gcp-001",
            region="us-central1-a",
            status="RUNNING",
            created_at=_now_iso(),
            metadata={},
        ),
    ]

    class ProviderMock:
        def list_services(self, region=None):
            return services

    monkeypatch.setattr(
        api_main, "_get_providers_safe", lambda provider: [ProviderMock()]
    )

    response = client.get("/services?service_type=EC2")
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 1
    assert len(payload["items"]) == 1
    assert payload["items"][0]["name"] == "i-ec2-001"
    assert payload["items"][0]["service_type"] == "EC2"


def test_list_services_with_sorting(monkeypatch) -> None:
    """Test sorting services by name."""
    services = [
        CloudService(
            provider="aws",
            service_type="EC2",
            name="z-instance",
            region="us-east-1",
            status="running",
            created_at=_now_iso(),
            metadata={},
        ),
        CloudService(
            provider="aws",
            service_type="EC2",
            name="a-instance",
            region="us-east-1",
            status="running",
            created_at=_now_iso(),
            metadata={},
        ),
        CloudService(
            provider="aws",
            service_type="EC2",
            name="m-instance",
            region="us-east-1",
            status="running",
            created_at=_now_iso(),
            metadata={},
        ),
    ]

    class ProviderMock:
        def list_services(self, region=None):
            return services

    monkeypatch.setattr(
        api_main, "_get_providers_safe", lambda provider: [ProviderMock()]
    )

    # Test ascending order (default)
    response = client.get("/services?sort_by=name&sort_order=asc")
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 3
    items = payload["items"]
    assert len(items) == 3
    assert items[0]["name"] == "a-instance"
    assert items[1]["name"] == "m-instance"
    assert items[2]["name"] == "z-instance"

    # Test descending order
    response = client.get("/services?sort_by=name&sort_order=desc")
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 3
    items = payload["items"]
    assert len(items) == 3
    assert items[0]["name"] == "z-instance"
    assert items[1]["name"] == "m-instance"
    assert items[2]["name"] == "a-instance"


def test_list_services_with_combined_filters_and_sort(monkeypatch) -> None:
    """Test combining filters and sorting."""
    services = [
        CloudService(
            provider="aws",
            service_type="EC2",
            name="z-running",
            region="us-east-1",
            status="running",
            created_at=_now_iso(),
            metadata={},
        ),
        CloudService(
            provider="aws",
            service_type="EC2",
            name="a-running",
            region="us-east-1",
            status="running",
            created_at=_now_iso(),
            metadata={},
        ),
        CloudService(
            provider="aws",
            service_type="EC2",
            name="m-stopped",
            region="us-east-1",
            status="stopped",
            created_at=_now_iso(),
            metadata={},
        ),
    ]

    class ProviderMock:
        def list_services(self, region=None):
            return services

    monkeypatch.setattr(
        api_main, "_get_providers_safe", lambda provider: [ProviderMock()]
    )

    # Filter by status=running and sort by name desc
    response = client.get("/services?status=running&sort_by=name&sort_order=desc")
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 2
    items = payload["items"]
    assert len(items) == 2
    assert items[0]["name"] == "z-running"
    assert items[1]["name"] == "a-running"
    assert all(s["status"] == "running" for s in items)


def test_pagination_limit(monkeypatch) -> None:
    """Test pagination with limit parameter."""
    services = [
        CloudService(
            provider="aws",
            service_type="EC2",
            name=f"instance-{i:03d}",
            region="us-east-1",
            status="running",
            created_at=_now_iso(),
            metadata={},
        )
        for i in range(150)
    ]

    class ProviderMock:
        def list_services(self, region=None):
            return services

    monkeypatch.setattr(
        api_main, "_get_providers_safe", lambda provider: [ProviderMock()]
    )

    # Test with limit=50
    response = client.get("/services?limit=50")
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 150
    assert payload["limit"] == 50
    assert payload["offset"] == 0
    assert payload["has_more"] is True
    assert len(payload["items"]) == 50


def test_pagination_offset(monkeypatch) -> None:
    """Test pagination with offset parameter."""
    services = [
        CloudService(
            provider="aws",
            service_type="EC2",
            name=f"instance-{i:03d}",
            region="us-east-1",
            status="running",
            created_at=_now_iso(),
            metadata={},
        )
        for i in range(150)
    ]

    class ProviderMock:
        def list_services(self, region=None):
            return services

    monkeypatch.setattr(
        api_main, "_get_providers_safe", lambda provider: [ProviderMock()]
    )

    # Test with offset=100
    response = client.get("/services?limit=50&offset=100")
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 150
    assert payload["limit"] == 50
    assert payload["offset"] == 100
    assert payload["has_more"] is False  # 100 + 50 = 150
    assert len(payload["items"]) == 50


def test_pagination_has_more_false(monkeypatch) -> None:
    """Test has_more flag when there are no more items."""
    services = [
        CloudService(
            provider="aws",
            service_type="EC2",
            name=f"instance-{i:03d}",
            region="us-east-1",
            status="running",
            created_at=_now_iso(),
            metadata={},
        )
        for i in range(25)
    ]

    class ProviderMock:
        def list_services(self, region=None):
            return services

    monkeypatch.setattr(
        api_main, "_get_providers_safe", lambda provider: [ProviderMock()]
    )

    # Default limit is 100, but we have only 25 items
    response = client.get("/services")
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 25
    assert payload["limit"] == 100
    assert payload["offset"] == 0
    assert payload["has_more"] is False
    assert len(payload["items"]) == 25


def test_auth_disabled_allows_request_without_api_key(monkeypatch) -> None:
    """When auth is disabled, requests should succeed without X-API-Key."""

    class ProviderMock:
        def list_services(self, region=None):
            return []

    monkeypatch.delenv("ENABLE_API_AUTH", raising=False)
    monkeypatch.delenv("API_KEY", raising=False)
    monkeypatch.setattr(
        api_main, "_get_providers_safe", lambda provider: [ProviderMock()]
    )

    response = client.get("/services")
    assert response.status_code == 200


def test_auth_enabled_without_configured_api_key_returns_500(monkeypatch) -> None:
    """When auth is enabled but API_KEY is missing, endpoint should return 500."""

    class ProviderMock:
        def list_services(self, region=None):
            return []

    monkeypatch.setenv("ENABLE_API_AUTH", "true")
    monkeypatch.delenv("API_KEY", raising=False)
    monkeypatch.setattr(
        api_main, "_get_providers_safe", lambda provider: [ProviderMock()]
    )

    response = client.get("/services")
    assert response.status_code == 500
    assert "API_KEY" in response.json()["detail"]


def test_auth_enabled_with_invalid_api_key_returns_401(monkeypatch) -> None:
    """When auth is enabled, invalid key should be rejected."""

    class ProviderMock:
        def list_services(self, region=None):
            return []

    monkeypatch.setenv("ENABLE_API_AUTH", "true")
    monkeypatch.setenv("API_KEY", "expected-secret")
    monkeypatch.setattr(
        api_main, "_get_providers_safe", lambda provider: [ProviderMock()]
    )

    response = client.get("/services", headers={"X-API-Key": "wrong-secret"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing API key"


def test_auth_enabled_with_valid_api_key_returns_200(monkeypatch) -> None:
    """When auth is enabled, valid key should allow access."""

    class ProviderMock:
        def list_services(self, region=None):
            return []

    monkeypatch.setenv("ENABLE_API_AUTH", "true")
    monkeypatch.setenv("API_KEY", "expected-secret")
    monkeypatch.setattr(
        api_main, "_get_providers_safe", lambda provider: [ProviderMock()]
    )

    response = client.get("/services", headers={"X-API-Key": "expected-secret"})
    assert response.status_code == 200


def test_cache_key_uses_all_components() -> None:
    """Cache key should normalize optional fields and include sort settings."""
    key = api_main._cache_key("aws", "", "", "", "name", "asc")
    assert key == "aws:all:all:all:name:asc"


def test_get_providers_safe_all_skips_runtime_errors(monkeypatch) -> None:
    """Provider init failures should be skipped in ALL mode."""

    class AwsMock:
        pass

    class GcpMock:
        def __init__(self):
            raise RuntimeError("auth failed")

    class AzureMock:
        pass

    monkeypatch.setattr(api_main, "AWSProvider", AwsMock)
    monkeypatch.setattr(api_main, "GCPProvider", GcpMock)
    monkeypatch.setattr(api_main, "AzureProvider", AzureMock)

    providers = api_main._get_providers_safe(api_main.ProviderOption.ALL)
    assert len(providers) == 2
    assert isinstance(providers[0], AwsMock)
    assert isinstance(providers[1], AzureMock)


def test_get_providers_safe_single_provider_uses_get_provider(monkeypatch) -> None:
    """Single-provider path should delegate to _get_provider."""
    sentinel = object()
    monkeypatch.setattr(api_main, "_get_provider", lambda provider: sentinel)

    providers = api_main._get_providers_safe(api_main.ProviderOption.AWS)
    assert providers == [sentinel]


def test_list_services_continues_when_one_provider_fails(monkeypatch) -> None:
    """Best-effort behavior should continue after provider list failure."""
    service = CloudService(
        provider="aws",
        service_type="EC2",
        name="i-ok",
        region="us-east-1",
        status="running",
        created_at=_now_iso(),
        metadata={},
    )

    class FailingProvider:
        def list_services(self, region=None):
            raise Exception("provider failed")

    class HealthyProvider:
        def list_services(self, region=None):
            return [service]

    monkeypatch.setattr(
        api_main,
        "_get_providers_safe",
        lambda provider: [FailingProvider(), HealthyProvider()],
    )

    response = client.get("/services")
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 1
    assert payload["items"][0]["name"] == "i-ok"


def test_list_services_sort_by_all_additional_fields(monkeypatch) -> None:
    """Cover provider/status/created_at/region/service_type sort branches."""
    services = [
        CloudService(
            provider="gcp",
            service_type="Compute Engine",
            name="svc-a",
            region="us-central1-a",
            status="RUNNING",
            created_at="2026-03-06T10:00:00Z",
            metadata={},
        ),
        CloudService(
            provider="aws",
            service_type="EC2",
            name="svc-b",
            region="us-east-1",
            status="stopped",
            created_at="2026-03-06T09:00:00Z",
            metadata={},
        ),
    ]

    class ProviderMock:
        def list_services(self, region=None):
            return services

    monkeypatch.setattr(
        api_main, "_get_providers_safe", lambda provider: [ProviderMock()]
    )

    cases = [
        ("provider", "aws"),
        ("status", "RUNNING"),
        ("created_at", "2026-03-06T09:00:00Z"),
        ("region", "us-central1-a"),
        ("service_type", "Compute Engine"),
    ]

    for sort_by, expected_first in cases:
        response = client.get(f"/services?sort_by={sort_by}&sort_order=asc")
        assert response.status_code == 200
        items = response.json()["items"]
        first = items[0]
        if sort_by == "provider":
            assert first["provider"] == expected_first
        elif sort_by == "status":
            assert first["status"] == expected_first
        elif sort_by == "created_at":
            assert first["created_at"] == expected_first
        elif sort_by == "region":
            assert first["region"] == expected_first
        elif sort_by == "service_type":
            assert first["service_type"] == expected_first


def test_get_service_invalid_provider_returns_400(monkeypatch) -> None:
    """Invalid provider errors should map to HTTP 400."""

    def _raise_value_error(provider):
        raise ValueError("Unsupported provider")

    monkeypatch.setattr(api_main, "_get_provider", _raise_value_error)
    response = client.get("/services/invalid/svc-1")
    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported provider"
