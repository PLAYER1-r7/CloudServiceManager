"""Tests for Azure authentication."""

import os
import pytest
from unittest.mock import Mock, patch
from azure.core.exceptions import ClientAuthenticationError

from src.cli.auth.azure_auth import AzureAuth


class TestAzureAuth:
    """Test suite for Azure authentication."""

    @patch("src.cli.auth.azure_auth.DefaultAzureCredential")
    def test_provider_attribute(self, mock_credential_class):
        """Test that provider is set to 'azure'."""
        mock_credential = Mock()
        mock_credential.get_token.return_value = Mock(token="test_token")
        mock_credential_class.return_value = mock_credential

        auth = AzureAuth()
        assert auth.provider == "azure"

    @patch("src.cli.auth.azure_auth.DefaultAzureCredential")
    def test_initialization_with_env_subscription(self, mock_credential_class):
        """Test initialization with AZURE_SUBSCRIPTION_ID environment variable."""
        mock_credential = Mock()
        mock_credential.get_token.return_value = Mock(token="test_token")
        mock_credential_class.return_value = mock_credential

        with patch.dict(os.environ, {"AZURE_SUBSCRIPTION_ID": "sub-12345"}):
            auth = AzureAuth()
            assert auth.subscription_id == "sub-12345"

    @patch("src.cli.auth.azure_auth.DefaultAzureCredential")
    def test_initialization_with_parameters(self, mock_credential_class):
        """Test initialization with explicit parameters."""
        mock_credential = Mock()
        mock_credential.get_token.return_value = Mock(token="test_token")
        mock_credential_class.return_value = mock_credential

        auth = AzureAuth(subscription_id="explicit-sub", tenant_id="explicit-tenant")
        assert auth.subscription_id == "explicit-sub"
        assert auth.tenant_id == "explicit-tenant"

    @patch("src.cli.auth.azure_auth.EnvironmentCredential")
    def test_initialization_with_env_credentials(self, mock_env_cred_class):
        """Test initialization with environment credentials."""
        mock_credential = Mock()
        mock_credential.get_token.return_value = Mock(token="test_token")
        mock_env_cred_class.return_value = mock_credential

        with patch.dict(
            os.environ,
            {
                "AZURE_TENANT_ID": "tenant-123",
                "AZURE_CLIENT_ID": "client-456",
                "AZURE_CLIENT_SECRET": "secret-789",
            },
        ):
            auth = AzureAuth()
            assert auth._auth_method == "environment"

    @patch("src.cli.auth.azure_auth.DefaultAzureCredential")
    def test_is_authenticated_with_credentials(self, mock_credential_class):
        """Test is_authenticated returns True when credentials exist."""
        mock_credential = Mock()
        mock_credential.get_token.return_value = Mock(token="test_token")
        mock_credential_class.return_value = mock_credential

        auth = AzureAuth()
        auth._credential = mock_credential
        auth._is_authenticated = True

        assert auth.is_authenticated() is True

    @patch("src.cli.auth.azure_auth.DefaultAzureCredential")
    def test_is_authenticated_without_credentials(self, mock_credential_class):
        """Test is_authenticated returns False when credentials are None."""
        mock_credential_class.side_effect = Exception("No credentials")

        auth = AzureAuth()
        auth._credential = None
        auth._is_authenticated = False

        assert auth.is_authenticated() is False

    @patch("src.cli.auth.azure_auth.DefaultAzureCredential")
    @patch("src.cli.auth.azure_auth.ResourceManagementClient")
    def test_validate_success(self, mock_client_class, mock_credential_class):
        """Test validate returns True with valid credentials."""
        mock_credential = Mock()
        mock_credential.get_token.return_value = Mock(token="test_token")
        mock_credential_class.return_value = mock_credential

        mock_client = Mock()
        mock_client.resource_groups.list.return_value = [Mock()]
        mock_client_class.return_value = mock_client

        auth = AzureAuth()
        auth._credential = mock_credential
        auth._is_authenticated = True
        auth.subscription_id = "test-sub-id"

        assert auth.validate() is True
        mock_credential.get_token.assert_called_with(
            "https://management.azure.com/.default"
        )

    @patch("src.cli.auth.azure_auth.DefaultAzureCredential")
    def test_validate_failure_auth_error(self, mock_credential_class):
        """Test validate returns False on ClientAuthenticationError."""
        mock_credential = Mock()
        mock_credential.get_token.side_effect = ClientAuthenticationError("Auth failed")
        mock_credential_class.return_value = mock_credential

        auth = AzureAuth()
        auth._credential = mock_credential
        auth._is_authenticated = True

        assert auth.validate() is False
        assert auth._is_authenticated is False

    @patch("src.cli.auth.azure_auth.DefaultAzureCredential")
    @patch("src.cli.auth.azure_auth.ResourceManagementClient")
    def test_get_credentials(self, mock_client_class, mock_credential_class):
        """Test get_credentials returns expected information."""
        mock_credential = Mock()
        mock_credential.get_token.return_value = Mock(token="test_token")
        mock_credential_class.return_value = mock_credential

        mock_rg1 = Mock()
        mock_rg2 = Mock()

        mock_client = Mock()
        mock_client.resource_groups.list.return_value = [mock_rg1, mock_rg2]
        mock_client_class.return_value = mock_client

        auth = AzureAuth()
        auth._credential = mock_credential
        auth._is_authenticated = True
        auth._auth_method = "default_credential_chain"
        auth.subscription_id = "test-sub-id"
        auth.tenant_id = "test-tenant-id"

        creds = auth.get_credentials()

        assert creds["provider"] == "azure"
        assert creds["authenticated"] is True
        assert creds["method"] == "default_credential_chain"
        assert creds["subscription_id"] == "test-sub-id"
        assert creds["tenant_id"] == "test-tenant-id"

    @patch("src.cli.auth.azure_auth.DefaultAzureCredential")
    def test_get_credentials_when_not_authenticated(self, mock_credential_class):
        """Test get_credentials when not authenticated."""
        mock_credential_class.side_effect = Exception("No credentials")

        auth = AzureAuth()
        auth._credential = None
        auth._is_authenticated = False
        auth.subscription_id = "test-sub"

        creds = auth.get_credentials()

        assert creds["provider"] == "azure"
        assert creds["authenticated"] is False
        assert creds["subscription_id"] == "test-sub"

    @patch("src.cli.auth.azure_auth.DefaultAzureCredential")
    def test_refresh_success(self, mock_credential_class):
        """Test refresh re-initializes credentials and validates."""
        mock_credential = Mock()
        mock_credential.get_token.return_value = Mock(token="test_token")
        mock_credential_class.return_value = mock_credential

        auth = AzureAuth()
        result = auth.refresh()

        assert result is True
        assert auth._credential is not None

    @patch("src.cli.auth.azure_auth.DefaultAzureCredential")
    def test_get_credential(self, mock_credential_class):
        """Test get_credential returns Azure credential object."""
        mock_credential = Mock()
        mock_credential.get_token.return_value = Mock(token="test_token")
        mock_credential_class.return_value = mock_credential

        auth = AzureAuth()
        auth._credential = mock_credential
        auth._is_authenticated = True

        credential = auth.get_credential()
        assert credential == mock_credential

    @patch("src.cli.auth.azure_auth.DefaultAzureCredential")
    def test_get_credential_raises_when_not_authenticated(self, mock_credential_class):
        """Test get_credential raises error when not authenticated."""
        mock_credential_class.side_effect = Exception("No credentials")

        auth = AzureAuth()
        auth._credential = None
        auth._is_authenticated = False

        with pytest.raises(RuntimeError, match="Not authenticated"):
            auth.get_credential()

    @patch("src.cli.auth.azure_auth.EnvironmentCredential")
    def test_auth_method_environment(self, mock_env_cred_class):
        """Test authentication method is 'environment' with env vars."""
        mock_credential = Mock()
        mock_credential.get_token.return_value = Mock(token="test_token")
        mock_env_cred_class.return_value = mock_credential

        with patch.dict(
            os.environ,
            {
                "AZURE_TENANT_ID": "tenant",
                "AZURE_CLIENT_ID": "client",
                "AZURE_CLIENT_SECRET": "secret",
            },
        ):
            auth = AzureAuth()
            assert auth._auth_method == "environment"

    @patch("src.cli.auth.azure_auth.DefaultAzureCredential")
    def test_auth_method_default_credential_chain(self, mock_credential_class):
        """Test authentication method is 'default_credential_chain' without env vars."""
        mock_credential = Mock()
        mock_credential.get_token.return_value = Mock(token="test_token")
        mock_credential_class.return_value = mock_credential

        with patch.dict(os.environ, {}, clear=True):
            auth = AzureAuth()
            assert auth._auth_method == "default_credential_chain"
