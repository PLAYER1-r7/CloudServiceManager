"""Cloud authentication manager for multi-cloud support."""

from typing import Dict, Optional, Type, Union

from .base import CloudAuthBase
from .aws_auth import AWSAuth
from .gcp_auth import GCPAuth
from .azure_auth import AzureAuth


class CloudAuthManager:
    """Centralized authentication manager for multiple cloud providers.
    
    This manager handles authentication for AWS, GCP, and Azure,
    providing a unified interface for credential management across
    multiple cloud providers.
    """
    
    # Map provider names to their authentication classes
    _PROVIDER_CLASSES: Dict[str, Type[CloudAuthBase]] = {
        "aws": AWSAuth,
        "gcp": GCPAuth,
        "azure": AzureAuth,
    }
    
    def __init__(self) -> None:
        """Initialize the authentication manager."""
        self._auth_instances: Dict[str, CloudAuthBase] = {}
    
    def get_auth(
        self,
        provider: str,
        auto_initialize: bool = True,
        **kwargs
    ) -> CloudAuthBase:
        """Get authentication instance for a specific provider.
        
        Args:
            provider: Cloud provider name ('aws', 'gcp', or 'azure')
            auto_initialize: If True, create instance if not exists
            **kwargs: Provider-specific initialization parameters
        
        Returns:
            CloudAuthBase: Authentication instance for the provider
        
        Raises:
            ValueError: If provider is not supported
            RuntimeError: If provider not initialized and auto_initialize is False
        """
        provider = provider.lower()
        
        if provider not in self._PROVIDER_CLASSES:
            supported = ", ".join(self._PROVIDER_CLASSES.keys())
            raise ValueError(f"Unsupported provider: {provider}. Supported: {supported}")
        
        # Return existing instance if available
        if provider in self._auth_instances:
            return self._auth_instances[provider]
        
        if not auto_initialize:
            raise RuntimeError(f"Provider '{provider}' not initialized")
        
        # Create new instance
        auth_class = self._PROVIDER_CLASSES[provider]
        auth_instance = auth_class(**kwargs)
        self._auth_instances[provider] = auth_instance
        
        return auth_instance
    
    def initialize_provider(
        self,
        provider: str,
        **kwargs
    ) -> CloudAuthBase:
        """Explicitly initialize authentication for a provider.
        
        Args:
            provider: Cloud provider name ('aws', 'gcp', or 'azure')
            **kwargs: Provider-specific initialization parameters
        
        Returns:
            CloudAuthBase: Initialized authentication instance
        """
        provider = provider.lower()
        
        if provider not in self._PROVIDER_CLASSES:
            supported = ", ".join(self._PROVIDER_CLASSES.keys())
            raise ValueError(f"Unsupported provider: {provider}. Supported: {supported}")
        
        auth_class = self._PROVIDER_CLASSES[provider]
        auth_instance = auth_class(**kwargs)
        self._auth_instances[provider] = auth_instance
        
        return auth_instance
    
    def is_authenticated(self, provider: str) -> bool:
        """Check if a provider is authenticated.
        
        Args:
            provider: Cloud provider name
        
        Returns:
            bool: True if authenticated, False otherwise
        """
        provider = provider.lower()
        
        if provider not in self._auth_instances:
            return False
        
        return self._auth_instances[provider].is_authenticated()
    
    def validate(self, provider: str) -> bool:
        """Validate credentials for a provider.
        
        Args:
            provider: Cloud provider name
        
        Returns:
            bool: True if credentials are valid, False otherwise
        """
        provider = provider.lower()
        
        if provider not in self._auth_instances:
            return False
        
        return self._auth_instances[provider].validate()
    
    def get_credentials(self, provider: str) -> Dict:
        """Get credential information for a provider.
        
        Args:
            provider: Cloud provider name
        
        Returns:
            Dict: Credential metadata
        
        Raises:
            RuntimeError: If provider not initialized
        """
        provider = provider.lower()
        
        if provider not in self._auth_instances:
            raise RuntimeError(f"Provider '{provider}' not initialized")
        
        return self._auth_instances[provider].get_credentials()
    
    def refresh(self, provider: str) -> bool:
        """Refresh credentials for a provider.
        
        Args:
            provider: Cloud provider name
        
        Returns:
            bool: True if refresh was successful, False otherwise
        """
        provider = provider.lower()
        
        if provider not in self._auth_instances:
            return False
        
        return self._auth_instances[provider].refresh()
    
    def get_all_authenticated(self) -> Dict[str, bool]:
        """Get authentication status for all initialized providers.
        
        Returns:
            Dict[str, bool]: Map of provider names to authentication status
        """
        return {
            provider: auth.is_authenticated()
            for provider, auth in self._auth_instances.items()
        }
    
    def validate_all(self) -> Dict[str, bool]:
        """Validate credentials for all initialized providers.
        
        Returns:
            Dict[str, bool]: Map of provider names to validation results
        """
        return {
            provider: auth.validate()
            for provider, auth in self._auth_instances.items()
        }
    
    def refresh_all(self) -> Dict[str, bool]:
        """Refresh credentials for all initialized providers.
        
        Returns:
            Dict[str, bool]: Map of provider names to refresh results
        """
        return {
            provider: auth.refresh()
            for provider, auth in self._auth_instances.items()
        }
    
    def get_supported_providers(self) -> list[str]:
        """Get list of supported cloud providers.
        
        Returns:
            list[str]: List of supported provider names
        """
        return list(self._PROVIDER_CLASSES.keys())
    
    def clear_provider(self, provider: str) -> None:
        """Clear authentication instance for a provider.
        
        Args:
            provider: Cloud provider name
        """
        provider = provider.lower()
        
        if provider in self._auth_instances:
            del self._auth_instances[provider]
    
    def clear_all(self) -> None:
        """Clear all authentication instances."""
        self._auth_instances.clear()
