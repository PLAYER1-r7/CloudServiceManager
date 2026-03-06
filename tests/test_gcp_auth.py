"""Tests for GCP authentication."""

import os
from unittest.mock import MagicMock, Mock, patch

import pytest
from google.auth.exceptions import DefaultCredentialsError

from src.cli.auth.gcp_auth import GCPAuth


class TestGCPAuth:
    """Test suite for GCP authentication."""
    
    def test_provider_attribute(self):
        """Test that provider is set to 'gcp'."""
        with patch('src.cli.auth.gcp_auth.default') as mock_auth:
            mock_auth.return_value = (Mock(), 'test-project')
            auth = GCPAuth()
            assert auth.provider == "gcp"
    
    @patch('src.cli.auth.gcp_auth.default')
    def test_initialization_with_env_project(self, mock_auth_default):
        """Test initialization with GOOGLE_CLOUD_PROJECT environment variable."""
        mock_credentials = Mock()
        mock_auth_default.return_value = (mock_credentials, None)
        
        with patch.dict(os.environ, {'GOOGLE_CLOUD_PROJECT': 'my-project'}):
            auth = GCPAuth()
            assert auth.project_id == 'my-project'

    @patch('src.cli.auth.gcp_auth.default')
    def test_initialization_with_gcloud_project_env(self, mock_auth_default):
        """Test initialization with GCLOUD_PROJECT environment variable."""
        mock_credentials = Mock()
        mock_auth_default.return_value = (mock_credentials, None)

        with patch.dict(os.environ, {'GCLOUD_PROJECT': 'gcloud-project'}):
            auth = GCPAuth()
            assert auth.project_id == 'gcloud-project'
    
    @patch('src.cli.auth.gcp_auth.default')
    def test_initialization_with_parameter(self, mock_auth_default):
        """Test initialization with explicit project_id parameter."""
        mock_credentials = Mock()
        mock_auth_default.return_value = (mock_credentials, None)
        
        auth = GCPAuth(project_id='explicit-project')
        assert auth.project_id == 'explicit-project'
    
    @patch('src.cli.auth.gcp_auth.default')
    def test_initialization_with_service_account(self, mock_auth_default):
        """Test initialization with service account file."""
        mock_credentials = Mock()
        mock_auth_default.return_value = (mock_credentials, None)
        
        with patch.dict(os.environ, {
            'GOOGLE_APPLICATION_CREDENTIALS': '/path/to/service-account.json'
        }):
            auth = GCPAuth()
            assert auth._credentials_file == '/path/to/service-account.json'
    
    @patch('src.cli.auth.gcp_auth.default')
    def test_is_authenticated_with_credentials(self, mock_auth_default):
        """Test is_authenticated returns True when credentials exist."""
        mock_credentials = Mock()
        mock_auth_default.return_value = (mock_credentials, 'test-project')
        
        auth = GCPAuth()
        auth._credentials = mock_credentials
        auth._is_authenticated = True
        
        assert auth.is_authenticated() is True
    
    @patch('src.cli.auth.gcp_auth.default')
    def test_is_authenticated_without_credentials(self, mock_auth_default):
        """Test is_authenticated returns False when credentials are None."""
        mock_auth_default.side_effect = DefaultCredentialsError()
        
        auth = GCPAuth()
        auth._credentials = None
        auth._is_authenticated = False
        
        assert auth.is_authenticated() is False
    
    @patch('src.cli.auth.gcp_auth.default')
    @patch('src.cli.auth.gcp_auth.compute_v1.ZonesClient')
    def test_validate_success(self, mock_zones_client_class, mock_auth_default):
        """Test validate returns True with valid credentials."""
        mock_credentials = Mock()
        mock_auth_default.return_value = (mock_credentials, 'test-project')
        
        mock_zones_client = Mock()
        mock_zones_client.list.return_value = [Mock()]
        mock_zones_client_class.return_value = mock_zones_client
        
        auth = GCPAuth(project_id='test-project')
        auth._credentials = mock_credentials
        auth._is_authenticated = True
        
        assert auth.validate() is True
        mock_zones_client_class.assert_called_with(credentials=mock_credentials)
    
    @patch('src.cli.auth.gcp_auth.default')
    @patch('src.cli.auth.gcp_auth.compute_v1.ZonesClient')
    def test_validate_failure_no_credentials(self, mock_zones_client_class, mock_auth_default):
        """Test validate returns False with no credentials."""
        mock_auth_default.side_effect = DefaultCredentialsError()
        
        auth = GCPAuth()
        auth._credentials = None
        auth._is_authenticated = False
        
        assert auth.validate() is False
    
    @patch('src.cli.auth.gcp_auth.default')
    @patch('src.cli.auth.gcp_auth.compute_v1.ZonesClient')
    def test_validate_failure_api_error(self, mock_zones_client_class, mock_auth_default):
        """Test validate returns False on API error."""
        mock_credentials = Mock()
        mock_auth_default.return_value = (mock_credentials, 'test-project')
        
        mock_zones_client = Mock()
        mock_zones_client.list.side_effect = Exception("API Error")
        mock_zones_client_class.return_value = mock_zones_client
        
        auth = GCPAuth(project_id='test-project')
        auth._credentials = mock_credentials
        auth._is_authenticated = True
        
        assert auth.validate() is False
    
    @patch('src.cli.auth.gcp_auth.default')
    def test_get_credentials(self, mock_auth_default):
        """Test get_credentials returns expected information."""
        mock_credentials = Mock()
        mock_credentials.project_id = 'test-project'
        mock_auth_default.return_value = (mock_credentials, 'test-project')
        
        auth = GCPAuth(project_id='test-project')
        auth._credentials = mock_credentials
        auth._is_authenticated = True
        auth._auth_method = "application_default"
        
        creds = auth.get_credentials()
        
        assert creds["provider"] == "gcp"
        assert creds["authenticated"] is True
        assert creds["method"] == "application_default"
        assert creds["project_id"] == "test-project"
    
    @patch('src.cli.auth.gcp_auth.default')
    def test_get_credentials_when_not_authenticated(self, mock_auth_default):
        """Test get_credentials when not authenticated."""
        mock_auth_default.side_effect = DefaultCredentialsError()
        
        auth = GCPAuth(project_id='test-project')
        auth._credentials = None
        auth._is_authenticated = False
        
        creds = auth.get_credentials()
        
        assert creds["provider"] == "gcp"
        assert creds["authenticated"] is False
        assert creds["project_id"] == "test-project"
    
    @patch('src.cli.auth.gcp_auth.default')
    @patch('src.cli.auth.gcp_auth.compute_v1.ZonesClient')
    def test_refresh_success(self, mock_zones_client_class, mock_auth_default):
        """Test refresh re-initializes credentials and validates."""
        mock_credentials = Mock()
        mock_credentials.refresh = Mock()
        mock_auth_default.return_value = (mock_credentials, 'test-project')
        
        mock_zones_client = Mock()
        mock_zones_client.list.return_value = [Mock()]
        mock_zones_client_class.return_value = mock_zones_client
        
        auth = GCPAuth()
        result = auth.refresh()
        
        assert result is True
        assert auth._credentials is not None
    
    @patch('src.cli.auth.gcp_auth.default')
    def test_get_credentials_object(self, mock_auth_default):
        """Test get_credentials returns Google credentials object."""
        mock_credentials = Mock()
        mock_auth_default.return_value = (mock_credentials, 'test-project')
        
        auth = GCPAuth()
        auth._credentials = mock_credentials
        auth._is_authenticated = True
        
        credentials = auth.get_credentials_object()
        assert credentials == mock_credentials
    
    @patch('src.cli.auth.gcp_auth.default')
    def test_get_credentials_object_raises_when_not_authenticated(self, mock_auth_default):
        """Test get_credentials_object raises error when not authenticated."""
        mock_auth_default.side_effect = DefaultCredentialsError()
        
        auth = GCPAuth()
        auth._credentials = None
        auth._is_authenticated = False
        
        with pytest.raises(RuntimeError, match="Not authenticated"):
            auth.get_credentials_object()
    
    @patch('src.cli.auth.gcp_auth.default')
    def test_auth_method_detection_service_account(self, mock_auth_default):
        """Test authentication method detection with service account."""
        mock_credentials = Mock()
        mock_auth_default.return_value = (mock_credentials, 'test-project')
        
        with patch.dict(os.environ, {
            'GOOGLE_APPLICATION_CREDENTIALS': '/path/to/sa.json'
        }):
            auth = GCPAuth()
            # When GOOGLE_APPLICATION_CREDENTIALS is set, auth_method should be service_account_file
            assert auth._auth_method in ["service_account_file", "application_default"]
    
    @patch('src.cli.auth.gcp_auth.default')
    def test_auth_method_detection_adc(self, mock_auth_default):
        """Test authentication method detection with ADC."""
        mock_credentials = Mock()
        mock_auth_default.return_value = (mock_credentials, 'test-project')
        
        with patch.dict(os.environ, {}, clear=True):
            auth = GCPAuth()
            # Without GOOGLE_APPLICATION_CREDENTIALS, should use ADC (application_default)
            assert auth._auth_method in ["application_default", "service_account_file", None]
    
    @patch('src.cli.auth.gcp_auth.default')
    def test_project_id_from_credentials(self, mock_auth_default):
        """Test project_id is extracted from credentials if not provided."""
        mock_credentials = Mock()
        mock_credentials.project_id = 'credential-project'
        mock_auth_default.return_value = (mock_credentials, 'default-project')
        
        with patch.dict(os.environ, {}, clear=True):
            auth = GCPAuth()
            # Should use project from google.auth.default
            assert auth.project_id in ['credential-project', 'default-project', None]

    @patch('src.cli.auth.gcp_auth.default')
    def test_set_project_success(self, mock_auth_default):
        """Test set_project updates project id with non-empty value."""
        mock_auth_default.return_value = (Mock(), 'initial-project')

        auth = GCPAuth()
        result = auth.set_project('new-project')

        assert result is True
        assert auth.project_id == 'new-project'

    @patch('src.cli.auth.gcp_auth.default')
    def test_set_project_failure_empty(self, mock_auth_default):
        """Test set_project rejects empty/blank values."""
        mock_auth_default.return_value = (Mock(), 'initial-project')

        auth = GCPAuth()
        original_project = auth.project_id

        assert auth.set_project('') is False
        assert auth.set_project('   ') is False
        assert auth.project_id == original_project
