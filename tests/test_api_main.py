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

    monkeypatch.setattr(api_main, "_get_providers_safe", lambda provider: [ProviderMock()])

    response = client.get("/services?provider=aws")
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["name"] == "i-api-001"


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
