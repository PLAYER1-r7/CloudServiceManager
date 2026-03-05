"""
Unit tests for CLI main module.
"""

import pytest
from typer.testing import CliRunner
from src.cli.main import app

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
