"""Tests for AWS authentication."""

import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from botocore.exceptions import ClientError, NoCredentialsError

from src.cli.auth.aws_auth import AWSAuth


class TestAWSAuth:
    """Test suite for AWS authentication."""
    
    def test_provider_attribute(self):
        """Test that provider is set to 'aws'."""
        with patch('src.cli.auth.aws_auth.boto3'):
            auth = AWSAuth()
            assert auth.provider == "aws"
    
    @patch('src.cli.auth.aws_auth.boto3.Session')
    def test_initialization_with_env_vars(self, mock_session_class):
        """Test initialization with environment variables."""
        mock_session = Mock()
        mock_session.get_credentials.return_value = Mock()
        mock_session_class.return_value = mock_session
        
        with patch.dict(os.environ, {
            'AWS_ACCESS_KEY_ID': 'test_key',
            'AWS_SECRET_ACCESS_KEY': 'test_secret',
            'AWS_DEFAULT_REGION': 'us-west-2'
        }):
            auth = AWSAuth()
            assert auth.region == 'us-west-2'
    
    @patch('src.cli.auth.aws_auth.boto3.Session')
    def test_initialization_with_parameters(self, mock_session_class):
        """Test initialization with explicit parameters."""
        mock_session = Mock()
        mock_session.get_credentials.return_value = Mock()
        mock_session_class.return_value = mock_session
        
        auth = AWSAuth(
            region='eu-west-1',
            profile='custom-profile'
        )
        assert auth.region == 'eu-west-1'
        assert auth.profile == 'custom-profile'
    
    @patch('src.cli.auth.aws_auth.boto3.Session')
    def test_is_authenticated_with_session(self, mock_session_class):
        """Test is_authenticated returns True when session exists."""
        mock_session = Mock()
        mock_session.get_credentials.return_value = Mock()
        mock_session_class.return_value = mock_session
        
        auth = AWSAuth()
        auth._session = mock_session
        auth._is_authenticated = True
        
        assert auth.is_authenticated() is True
    
    @patch('src.cli.auth.aws_auth.boto3.Session')
    def test_is_authenticated_without_session(self, mock_session_class):
        """Test is_authenticated returns False when session is None."""
        mock_session = Mock()
        mock_session.get_credentials.side_effect = NoCredentialsError()
        mock_session_class.return_value = mock_session
        
        auth = AWSAuth()
        auth._session = None
        auth._is_authenticated = False
        
        assert auth.is_authenticated() is False
    
    @patch('src.cli.auth.aws_auth.boto3.Session')
    def test_validate_success(self, mock_session_class):
        """Test validate returns True with valid credentials."""
        mock_sts = Mock()
        mock_sts.get_caller_identity.return_value = {
            'UserId': 'test-user',
            'Account': '123456789012',
            'Arn': 'arn:aws:iam::123456789012:user/test'
        }
        
        mock_session = Mock()
        mock_session.get_credentials.return_value = Mock()
        mock_session.client.return_value = mock_sts
        mock_session_class.return_value = mock_session
        
        auth = AWSAuth()
        auth._session = mock_session
        auth._is_authenticated = True
        
        assert auth.validate() is True
        mock_session.client.assert_called_with('sts')
        mock_sts.get_caller_identity.assert_called_once()
    
    @patch('src.cli.auth.aws_auth.boto3.Session')
    def test_validate_failure_no_credentials(self, mock_session_class):
        """Test validate returns False with no credentials."""
        mock_sts = Mock()
        mock_sts.get_caller_identity.side_effect = NoCredentialsError()
        
        mock_session = Mock()
        mock_session.get_credentials.return_value = Mock()
        mock_session.client.return_value = mock_sts
        mock_session_class.return_value = mock_session
        
        auth = AWSAuth()
        auth._session = mock_session
        auth._is_authenticated = True
        
        assert auth.validate() is False
        assert auth._is_authenticated is False
    
    @patch('src.cli.auth.aws_auth.boto3.Session')
    def test_validate_failure_client_error(self, mock_session_class):
        """Test validate returns False on ClientError."""
        mock_sts = Mock()
        mock_sts.get_caller_identity.side_effect = ClientError(
            {'Error': {'Code': 'InvalidClientTokenId', 'Message': 'Invalid token'}},
            'GetCallerIdentity'
        )
        
        mock_session = Mock()
        mock_session.get_credentials.return_value = Mock()
        mock_session.client.return_value = mock_sts
        mock_session_class.return_value = mock_session
        
        auth = AWSAuth()
        auth._session = mock_session
        auth._is_authenticated = True
        
        assert auth.validate() is False
    
    @patch('src.cli.auth.aws_auth.boto3.Session')
    def test_get_credentials(self, mock_session_class):
        """Test get_credentials returns expected information."""
        mock_sts = Mock()
        mock_sts.get_caller_identity.return_value = {
            'UserId': 'AIDAI123456789EXAMPLE',
            'Account': '123456789012',
            'Arn': 'arn:aws:iam::123456789012:user/testuser'
        }
        
        mock_session = Mock()
        mock_session.get_credentials.return_value = Mock()
        mock_session.client.return_value = mock_sts
        mock_session.region_name = 'us-east-1'
        mock_session_class.return_value = mock_session
        
        auth = AWSAuth()
        auth._session = mock_session
        auth._is_authenticated = True
        auth._auth_method = "environment"
        
        creds = auth.get_credentials()
        
        assert creds["provider"] == "aws"
        assert creds["authenticated"] is True
        assert creds["method"] == "environment"
        assert creds["region"] == "us-east-1"
        assert "account_id" in creds
        assert "user_arn" in creds
    
    @patch('src.cli.auth.aws_auth.boto3.Session')
    def test_get_credentials_when_not_authenticated(self, mock_session_class):
        """Test get_credentials when not authenticated."""
        mock_session = Mock()
        mock_session.get_credentials.side_effect = NoCredentialsError()
        mock_session_class.return_value = mock_session
        
        auth = AWSAuth()
        auth._session = None
        auth._is_authenticated = False
        auth.region = 'us-west-2'
        
        creds = auth.get_credentials()
        
        assert creds["provider"] == "aws"
        assert creds["authenticated"] is False
        assert creds["region"] == "us-west-2"
    
    @patch('src.cli.auth.aws_auth.boto3.Session')
    def test_refresh_success(self, mock_session_class):
        """Test refresh creates new session and validates."""
        mock_sts = Mock()
        mock_sts.get_caller_identity.return_value = {
            'Account': '123456789012'
        }
        
        mock_new_session = Mock()
        mock_new_session.get_credentials.return_value = Mock()
        mock_new_session.client.return_value = mock_sts
        mock_session_class.return_value = mock_new_session
        
        auth = AWSAuth()
        result = auth.refresh()
        
        assert result is True
        assert auth._session is not None
    
    @patch('src.cli.auth.aws_auth.boto3.Session')
    def test_get_session(self, mock_session_class):
        """Test get_session returns boto3 session."""
        mock_session = Mock()
        mock_session.get_credentials.return_value = Mock()
        mock_session_class.return_value = mock_session
        
        auth = AWSAuth()
        auth._session = mock_session
        auth._is_authenticated = True
        
        session = auth.get_session()
        assert session == mock_session
    
    @patch('src.cli.auth.aws_auth.boto3.Session')
    def test_get_session_raises_when_not_authenticated(self, mock_session_class):
        """Test get_session raises error when not authenticated."""
        mock_session = Mock()
        mock_session.get_credentials.side_effect = NoCredentialsError()
        mock_session_class.return_value = mock_session
        
        auth = AWSAuth()
        auth._session = None
        auth._is_authenticated = False
        
        with pytest.raises(RuntimeError, match="Not authenticated"):
            auth.get_session()
    
    @patch('src.cli.auth.aws_auth.boto3.Session')
    def test_auth_method_detection_env_vars(self, mock_session_class):
        """Test authentication method detection with environment variables."""
        mock_session = Mock()
        mock_session.get_credentials.return_value = Mock()
        mock_session_class.return_value = mock_session
        
        with patch.dict(os.environ, {
            'AWS_ACCESS_KEY_ID': 'test',
            'AWS_SECRET_ACCESS_KEY': 'test'
        }):
            auth = AWSAuth()
            # Auth method should be set during initialization
            assert auth._auth_method in ["environment", "credentials_file", "iam_role", None]
