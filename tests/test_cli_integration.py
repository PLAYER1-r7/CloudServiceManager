"""Integration tests for CLI command behavior across providers."""

from datetime import datetime, timezone
from typing import Optional

import pytest
from typer.testing import CliRunner

import src.cli.main as main_module
from src.cli.main import app
from src.cli.models.service import CloudService

runner = CliRunner()


@pytest.mark.integration
def test_list_services_all_providers_aggregates_results(
    monkeypatch: pytest.MonkeyPatch,
):
    """list-services should aggregate results from all providers."""

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    aws_service = CloudService(
        provider="aws",
        service_type="EC2",
        name="i-aws-001",
        region="us-east-1",
        status="running",
        created_at=now,
        metadata={"instance_type": "t3.micro"},
    )
    gcp_service = CloudService(
        provider="gcp",
        service_type="Compute Engine",
        name="gcp-001",
        region="us-central1-a",
        status="RUNNING",
        created_at=now,
        metadata={"machine_type": "e2-medium"},
    )
    azure_service = CloudService(
        provider="azure",
        service_type="Virtual Machine",
        name="vm-001",
        region="eastus",
        status="running",
        created_at=now,
        metadata={"vm_size": "Standard_B2s"},
    )

    class AWSMockProvider:
        def list_services(self, region: Optional[str] = None):
            return [aws_service]

    class GCPMockProvider:
        def list_services(self, region: Optional[str] = None):
            return [gcp_service]

    class AzureMockProvider:
        def list_services(self, region: Optional[str] = None):
            return [azure_service]

    def mock_get_providers(provider: object) -> list[object]:
        return [AWSMockProvider(), GCPMockProvider(), AzureMockProvider()]

    monkeypatch.setattr(
        main_module,
        "_get_providers",
        mock_get_providers,
    )

    result = runner.invoke(
        app, ["list-services", "--provider", "all", "--format", "json"]
    )

    assert result.exit_code == 0
    assert "i-aws-001" in result.stdout
    assert "gcp-001" in result.stdout
    assert "vm-001" in result.stdout


@pytest.mark.integration
def test_list_services_forwards_region_filter(monkeypatch: pytest.MonkeyPatch):
    """list-services should pass --region value to provider implementation."""

    captured: dict[str, Optional[str]] = {"region": None}
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    class RegionAwareProvider:
        def list_services(self, region: Optional[str] = None):
            captured["region"] = region
            return [
                CloudService(
                    provider="aws",
                    service_type="EC2",
                    name="i-region-001",
                    region=region or "us-east-1",
                    status="running",
                    created_at=now,
                    metadata={},
                )
            ]

    def mock_get_providers(provider: object) -> list[object]:
        return [RegionAwareProvider()]

    monkeypatch.setattr(main_module, "_get_providers", mock_get_providers)

    result = runner.invoke(
        app,
        [
            "list-services",
            "--provider",
            "aws",
            "--region",
            "ap-northeast-1",
            "--format",
            "json",
        ],
    )

    assert result.exit_code == 0
    assert captured["region"] == "ap-northeast-1"
    assert "ap-northeast-1" in result.stdout


@pytest.mark.integration
def test_get_service_cli_with_provider_dispatch(monkeypatch: pytest.MonkeyPatch):
    """get-service should dispatch to the selected provider and render JSON output."""

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    class ProviderMock:
        def get_service(self, service_id: str):
            return CloudService(
                provider="gcp",
                service_type="Compute Engine",
                name=service_id,
                region="us-central1-a",
                status="RUNNING",
                created_at=now,
                metadata={"machine_type": "e2-small"},
            )

    def mock_get_provider(provider: object):
        return ProviderMock()

    monkeypatch.setattr(main_module, "_get_provider", mock_get_provider)

    result = runner.invoke(
        app,
        [
            "get-service",
            "--provider",
            "gcp",
            "--id",
            "instance-777",
            "--format",
            "json",
        ],
    )

    assert result.exit_code == 0
    assert "instance-777" in result.stdout
    assert '"provider": "gcp"' in result.stdout
