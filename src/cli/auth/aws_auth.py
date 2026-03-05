"""AWS authentication handler."""

import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError

from .base import CloudAuthBase


class AWSAuth(CloudAuthBase):
    """AWS authentication handler.
    
    Supports multiple authentication methods:
    1. Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    2. AWS credentials file (~/.aws/credentials)
   3. IAM roles (for EC2 instances)
    4. AWS config file (~/.aws/config)
    
    The authentication follows boto3's default credential chain.
    """
    
    provider = "aws"
    
    def __init__(self, region: Optional[str] = None, profile: Optional[str] = None) -> None:
        """Initialize AWS authentication.
        
        Args:
            region: AWS region to use (default: from env or config)
            profile: AWS profile name to use (default: uses default profile)
        """
        super().__init__()
        self.region = region or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
        self.profile = profile
        self._session: Optional[boto3.Session] = None
        self._auth_method: Optional[str] = None
        
        # Try to initialize session
        self._initialize_session()
    
    def _initialize_session(self) -> None:
        """Initialize boto3 session with available credentials."""
        try:
            if self.profile:
                self._session = boto3.Session(profile_name=self.profile, region_name=self.region)
                self._auth_method = f"profile:{self.profile}"
            else:
                self._session = boto3.Session(region_name=self.region)
                
                # Detect authentication method
                if os.getenv("AWS_ACCESS_KEY_ID"):
                    self._auth_method = "environment"
                elif os.path.exists(os.path.expanduser("~/.aws/credentials")):
                    self._auth_method = "credentials_file"
                else:
                    self._auth_method = "iam_role"
            
            # Test if credentials are available
            self._session.get_credentials()
            self._is_authenticated = True
            
        except (NoCredentialsError, PartialCredentialsError):
            self._is_authenticated = False
            self._auth_method = None
    
    def is_authenticated(self) -> bool:
        """Check if AWS authentication is currently valid.
        
        Returns:
            bool: True if authenticated, False otherwise
        """
        return self._is_authenticated and self._session is not None
    
    def validate(self) -> bool:
        """Validate AWS credentials by making a test API call.
        
        Returns:
            bool: True if credentials are valid, False otherwise
        """
        if not self.is_authenticated():
            return False
        
        try:
            # Use STS to validate credentials
            sts = self._session.client("sts")
            sts.get_caller_identity()
            return True
        except ClientError:
            self._is_authenticated = False
            return False
        except Exception:
            return False
    
    def get_credentials(self) -> Dict[str, Any]:
        """Get non-sensitive AWS credential information.
        
        Returns:
            Dict[str, Any]: Dictionary with credential metadata
        """
        creds_info: Dict[str, Any] = {
            "provider": self.provider,
            "authenticated": self.is_authenticated(),
            "method": self._auth_method,
            "region": self.region,
        }
        
        if self.is_authenticated() and self._session:
            try:
                sts = self._session.client("sts")
                identity = sts.get_caller_identity()
                creds_info["account_id"] = identity.get("Account")
                creds_info["user_arn"] = identity.get("Arn")
                creds_info["user_id"] = identity.get("UserId")
            except Exception:
                pass
        
        return creds_info
    
    def refresh(self) -> bool:
        """Refresh AWS credentials.
        
        For IAM roles and temporary credentials, this attempts to refresh them.
        For static credentials, this validates they're still valid.
        
        Returns:
            bool: True if refresh was successful, False otherwise
        """
        self._initialize_session()
        return self.validate()
    
    def get_session(self) -> boto3.Session:
        """Get the boto3 session for making AWS API calls.
        
        Returns:
            boto3.Session: The authenticated boto3 session
        
        Raises:
            RuntimeError: If not authenticated
        """
        if not self.is_authenticated():
            raise RuntimeError("Not authenticated with AWS. Please configure credentials.")
        
        return self._session
