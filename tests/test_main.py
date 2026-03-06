"""
Unit tests for CLI main module.
"""

from datetime import datetime

import pytest
from typer.testing import CliRunner

import src.cli.main as main_module
from src.cli.main import app
from src.cli.models.service import CloudService

runner = CliRunner()


@pytest.mark.unit
def test_list_services_help():
    """Test that list-services command shows help."""
    result = runner.invoke(app, ["list-services", "--help"])
    assert result.exit_code == 0
    assert "List cloud services" in result.stdout


@pytest.mark.unit
def test_init_config_command():
    """Test init-config command."""
    result = runner.invoke(app, ["init-config"])
    assert result.exit_code == 0
    assert "Configuration" in result.stdout or "setup" in result.stdout.lower()


@pytest.mark.unit
def test_invalid_provider():
    """Test that invalid provider returns error."""
    result = runner.invoke(
        app,
        ["list-services", "--provider", "invalid"]
    )
    assert result.exit_code != 0


@pytest.mark.unit
def test_list_services_with_json_output(monkeypatch):
    """Test list-services JSON output with mocked provider."""

    service = CloudService(
        provider="aws",
        service_type="EC2",
        name="i-123456",
        region="us-east-1",
        status="running",
        created_at=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        metadata={"instance_type": "t3.micro"},
    )

    class MockProvider:
        def list_services(self, region=None):
            return [service]

    monkeypatch.setattr(main_module, "_get_providers", lambda provider: [MockProvider()])

    result = runner.invoke(app, ["list-services", "--provider", "aws", "--format", "json"])

    assert result.exit_code == 0
    assert "i-123456" in result.stdout
    assert '"provider": "aws"' in result.stdout


@pytest.mark.unit
def test_list_services_csv_output(monkeypatch):
    """Test list-services CSV output includes metadata as JSON string."""

    service = CloudService(
        provider="gcp",
        service_type="Compute Engine",
        name="instance-1",
        region="us-central1-a",
        status="RUNNING",
        created_at=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        metadata={"machine_type": "n1-standard-1"},
    )

    class MockProvider:
        def list_services(self, region=None):
            return [service]

    monkeypatch.setattr(main_module, "_get_providers", lambda provider: [MockProvider()])

    result = runner.invoke(app, ["list-services", "--provider", "gcp", "--format", "csv"])

    assert result.exit_code == 0
    assert "provider,service_type,name,region,status,created_at,metadata" in result.stdout
    assert "instance-1" in result.stdout
    assert "machine_type" in result.stdout
    assert "n1-standard-1" in result.stdout


@pytest.mark.unit
def test_list_services_partial_provider_failure(monkeypatch):
    """Test list-services continues when one provider fails."""

    service = CloudService(
        provider="azure",
        service_type="Virtual Machine",
        name="vm-01",
        region="eastus",
        status="running",
        created_at=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        metadata={},
    )

    class FailingProvider:
        def list_services(self, region=None):
            raise RuntimeError("auth failed")

    class WorkingProvider:
        def list_services(self, region=None):
            return [service]

    monkeypatch.setattr(
        main_module,
        "_get_providers",
        lambda provider: [FailingProvider(), WorkingProvider()],
    )

    result = runner.invoke(app, ["list-services", "--provider", "all", "--format", "table"])

    assert result.exit_code == 0
    assert "Warning" in result.stdout
    assert "vm-01" in result.stdout


@pytest.mark.unit
def test_list_services_all_providers_fail(monkeypatch):
    """Test list-services exits with error if all providers fail."""

    class FailingProvider:
        def list_services(self, region=None):
            raise RuntimeError("auth failed")

    monkeypatch.setattr(main_module, "_get_providers", lambda provider: [FailingProvider()])

    result = runner.invoke(app, ["list-services", "--provider", "all"])

    assert result.exit_code == 1
    assert "All requested providers failed" in result.stdout
