"""Tests for CloudAuthManager."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from src.cli.auth.manager import CloudAuthManager
from src.cli.auth.base import CloudAuthBase
from src.cli.auth.aws_auth import AWSAuth
from src.cli.auth.gcp_auth import GCPAuth
from src.cli.auth.azure_auth import AzureAuth


class TestCloudAuthManager:
    """Test suite for CloudAuthManager."""
    
    def test_initialization(self):
        """Test manager initializes with empty instances."""
        manager = CloudAuthManager()
        assert manager._auth_instances == {}
    
    def test_supported_providers(self):
        """Test get_supported_providers returns correct list."""
        manager = CloudAuthManager()
        providers = manager.get_supported_providers()
        
        assert isinstance(providers, list)
        assert "aws" in providers
        assert "gcp" in providers
        assert "azure" in providers
        assert len(providers) == 3
    
    @patch('boto3.Session')
    def test_get_auth_auto_initialize(self, mock_boto_session):
        """Test get_auth auto-initializes provider."""
        mock_session = Mock()
        mock_boto_session.return_value = mock_session
        
        manager = CloudAuthManager()
        auth = manager.get_auth('aws', auto_initialize=True)
        
        assert auth is not None
        assert manager._auth_instances.get('aws') is not None
    
    @patch('google.auth.default')
    def test_get_auth_with_kwargs(self, mock_auth_default):
        """Test get_auth passes kwargs to provider constructor."""
        mock_credentials = Mock()
        mock_auth_default.return_value = (mock_credentials, 'test-project')
        
        manager = CloudAuthManager()
        auth = manager.get_auth('gcp', auto_initialize=True, project_id='test-project')
        
        assert auth is not None
        assert auth.project_id == 'test-project'
    
    def test_get_auth_returns_cached_instance(self):
        """Test get_auth returns cached instance on second call."""
        manager = CloudAuthManager()
        mock_auth = Mock(spec=CloudAuthBase)
        manager._auth_instances['aws'] = mock_auth
        
        auth = manager.get_auth('aws')
        assert auth == mock_auth
    
    def test_get_auth_no_auto_initialize_raises(self):
        """Test get_auth raises error when provider not initialized."""
        manager = CloudAuthManager()
        
        with pytest.raises(RuntimeError, match="not initialized"):
            manager.get_auth('aws', auto_initialize=False)
    
    def test_get_auth_invalid_provider_raises(self):
        """Test get_auth raises ValueError for unsupported provider."""
        manager = CloudAuthManager()
        
        with pytest.raises(ValueError, match="Unsupported provider"):
            manager.get_auth('invalid-cloud')
    
    def test_get_auth_case_insensitive(self):
        """Test get_auth handles provider names case-insensitively."""
        manager = CloudAuthManager()
        mock_auth = Mock(spec=CloudAuthBase)
        manager._auth_instances['aws'] = mock_auth
        
        auth_upper = manager.get_auth('AWS')
        auth_mixed = manager.get_auth('AwS')
        
        assert auth_upper == mock_auth
        assert auth_mixed == mock_auth
    
    @patch('azure.identity.DefaultAzureCredential')
    def test_initialize_provider(self, mock_credential_class):
        """Test initialize_provider creates new instance."""
        mock_credential = Mock()
        mock_credential.get_token.return_value = Mock(token="test_token")
        mock_credential_class.return_value = mock_credential
        
        manager = CloudAuthManager()
        auth = manager.initialize_provider('azure', subscription_id='sub-123')
        
        assert auth is not None
        assert auth.subscription_id == 'sub-123'
        assert 'azure' in manager._auth_instances
    
    def test_initialize_provider_invalid_raises(self):
        """Test initialize_provider raises ValueError for invalid provider."""
        manager = CloudAuthManager()
        
        with pytest.raises(ValueError, match="Unsupported provider"):
            manager.initialize_provider('invalid')
    
    def test_is_authenticated(self):
        """Test is_authenticated checks provider status."""
        manager = CloudAuthManager()
        mock_auth = Mock(spec=CloudAuthBase)
        mock_auth.is_authenticated.return_value = True
        manager._auth_instances['aws'] = mock_auth
        
        result = manager.is_authenticated('aws')
        
        assert result is True
        mock_auth.is_authenticated.assert_called_once()
    
    def test_is_authenticated_not_initialized(self):
        """Test is_authenticated returns False for uninitialized provider."""
        manager = CloudAuthManager()
        
        result = manager.is_authenticated('gcp')
        assert result is False
    
    def test_validate(self):
        """Test validate calls provider's validate method."""
        manager = CloudAuthManager()
        mock_auth = Mock(spec=CloudAuthBase)
        mock_auth.validate.return_value = True
        manager._auth_instances['gcp'] = mock_auth
        
        result = manager.validate('gcp')
        
        assert result is True
        mock_auth.validate.assert_called_once()
    
    def test_validate_not_initialized(self):
        """Test validate returns False for uninitialized provider."""
        manager = CloudAuthManager()
        
        result = manager.validate('azure')
        assert result is False
    
    def test_get_credentials(self):
        """Test get_credentials returns provider's credentials."""
        manager = CloudAuthManager()
        mock_auth = Mock(spec=CloudAuthBase)
        expected_creds = {"provider": "aws", "authenticated": True}
        mock_auth.get_credentials.return_value = expected_creds
        manager._auth_instances['aws'] = mock_auth
        
        creds = manager.get_credentials('aws')
        
        assert creds == expected_creds
        mock_auth.get_credentials.assert_called_once()
    
    def test_get_credentials_not_initialized_raises(self):
        """Test get_credentials raises error for uninitialized provider."""
        manager = CloudAuthManager()
        
        with pytest.raises(RuntimeError, match="not initialized"):
            manager.get_credentials('aws')
    
    def test_refresh(self):
        """Test refresh calls provider's refresh method."""
        manager = CloudAuthManager()
        mock_auth = Mock(spec=CloudAuthBase)
        mock_auth.refresh.return_value = True
        manager._auth_instances['azure'] = mock_auth
        
        result = manager.refresh('azure')
        
        assert result is True
        mock_auth.refresh.assert_called_once()
    
    def test_refresh_not_initialized(self):
        """Test refresh returns False for uninitialized provider."""
        manager = CloudAuthManager()
        
        result = manager.refresh('gcp')
        assert result is False
    
    def test_get_all_authenticated(self):
        """Test get_all_authenticated returns status for all providers."""
        manager = CloudAuthManager()
        
        mock_aws = Mock(spec=CloudAuthBase)
        mock_aws.is_authenticated.return_value = True
        
        mock_gcp = Mock(spec=CloudAuthBase)
        mock_gcp.is_authenticated.return_value = False
        
        manager._auth_instances['aws'] = mock_aws
        manager._auth_instances['gcp'] = mock_gcp
        
        result = manager.get_all_authenticated()
        
        assert result == {'aws': True, 'gcp': False}
    
    def test_validate_all(self):
        """Test validate_all validates all initialized providers."""
        manager = CloudAuthManager()
        
        mock_aws = Mock(spec=CloudAuthBase)
        mock_aws.validate.return_value = True
        
        mock_azure = Mock(spec=CloudAuthBase)
        mock_azure.validate.return_value = False
        
        manager._auth_instances['aws'] = mock_aws
        manager._auth_instances['azure'] = mock_azure
        
        result = manager.validate_all()
        
        assert result == {'aws': True, 'azure': False}
        mock_aws.validate.assert_called_once()
        mock_azure.validate.assert_called_once()
    
    def test_refresh_all(self):
        """Test refresh_all refreshes all initialized providers."""
        manager = CloudAuthManager()
        
        mock_aws = Mock(spec=CloudAuthBase)
        mock_aws.refresh.return_value = True
        
        mock_gcp = Mock(spec=CloudAuthBase)
        mock_gcp.refresh.return_value = True
        
        manager._auth_instances['aws'] = mock_aws
        manager._auth_instances['gcp'] = mock_gcp
        
        result = manager.refresh_all()
        
        assert result == {'aws': True, 'gcp': True}
        mock_aws.refresh.assert_called_once()
        mock_gcp.refresh.assert_called_once()
    
    def test_clear_provider(self):
        """Test clear_provider removes provider instance."""
        manager = CloudAuthManager()
        mock_auth = Mock(spec=CloudAuthBase)
        manager._auth_instances['aws'] = mock_auth
        
        manager.clear_provider('aws')
        
        assert 'aws' not in manager._auth_instances
    
    def test_clear_provider_not_initialized(self):
        """Test clear_provider handles uninitialized provider gracefully."""
        manager = CloudAuthManager()
        
        # Should not raise error
        manager.clear_provider('gcp')
        assert 'gcp' not in manager._auth_instances
    
    def test_clear_all(self):
        """Test clear_all removes all provider instances."""
        manager = CloudAuthManager()
        manager._auth_instances['aws'] = Mock()
        manager._auth_instances['gcp'] = Mock()
        manager._auth_instances['azure'] = Mock()
        
        manager.clear_all()
        
        assert manager._auth_instances == {}
    
    @patch('boto3.Session')
    @patch('google.auth.default')
    def test_multi_provider_workflow(self, mock_gcp_auth, mock_aws_session):
        """Test complete workflow with multiple providers."""
        # Setup AWS mock
        mock_session = Mock()
        mock_session.client.return_value.get_caller_identity.return_value = {
            'Account': '123456789012'
        }
        mock_aws_session.return_value = mock_session
        
        # Setup GCP mock  
        mock_credentials = Mock()
        mock_gcp_auth.return_value = (mock_credentials, 'test-project')
        
        manager = CloudAuthManager()
        
        # Initialize providers
        aws_auth = manager.get_auth('aws', region='us-west-2')
        gcp_auth = manager.get_auth('gcp', project_id='my-project')
        
        # Get authentication status (may be False initially, that's OK)
        auth_status = manager.get_all_authenticated()
        assert 'aws' in auth_status
        assert 'gcp' in auth_status
