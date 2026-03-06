"""Azure authentication handler."""

import os
from typing import Any, Dict, Optional

from azure.identity import DefaultAzureCredential, EnvironmentCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.core.exceptions import ClientAuthenticationError

from .base import CloudAuthBase


class AzureAuth(CloudAuthBase):
    """Azure authentication handler.

    Supports multiple authentication methods:
    1. Environment variables (AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET)
    2. Managed Identity (for Azure VMs)
    3. Azure CLI credentials (az login)
    4. Visual Studio Code credentials
    5. Azure PowerShell credentials

    The authentication follows Azure's DefaultAzureCredential chain.
    """

    provider = "azure"

    def __init__(
        self, subscription_id: Optional[str] = None, tenant_id: Optional[str] = None
    ) -> None:
        """Initialize Azure authentication.

        Args:
            subscription_id: Azure subscription ID (default: from env)
            tenant_id: Azure tenant ID (default: from env)
        """
        super().__init__()
        self.subscription_id = subscription_id or os.getenv("AZURE_SUBSCRIPTION_ID")
        self.tenant_id = tenant_id or os.getenv("AZURE_TENANT_ID")
        self._credential = None
        self._auth_method: Optional[str] = None

        # Try to initialize credentials
        self._initialize_credentials()

    def _initialize_credentials(self) -> None:
        """Initialize Azure credentials."""
        try:
            # Check if environment variables are set
            if all(
                [
                    os.getenv("AZURE_TENANT_ID"),
                    os.getenv("AZURE_CLIENT_ID"),
                    os.getenv("AZURE_CLIENT_SECRET"),
                ]
            ):
                self._credential = EnvironmentCredential()
                self._auth_method = "environment"
            else:
                # Use DefaultAzureCredential which tries multiple methods
                self._credential = DefaultAzureCredential()
                self._auth_method = "default_credential_chain"

            # Test the credential by getting a token
            # Use ARM endpoint as a standard test
            self._credential.get_token("https://management.azure.com/.default")
            self._is_authenticated = True

        except Exception:
            self._is_authenticated = False
            self._auth_method = None

    def is_authenticated(self) -> bool:
        """Check if Azure authentication is currently valid.

        Returns:
            bool: True if authenticated, False otherwise
        """
        return self._is_authenticated and self._credential is not None

    def validate(self) -> bool:
        """Validate Azure credentials by making a test API call.

        Returns:
            bool: True if credentials are valid, False otherwise
        """
        if not self.is_authenticated():
            return False

        try:
            # Validate by getting a token
            # This confirms credentials are valid without making API calls
            self._credential.get_token("https://management.azure.com/.default")

            # If we have a subscription_id, we can do a more thorough validation
            if self.subscription_id:
                try:
                    client = ResourceManagementClient(
                        credential=self._credential,
                        subscription_id=self.subscription_id,
                    )
                    # Try to list resource groups as a validation
                    list(client.resource_groups.list())
                except Exception:
                    # If this fails but we got a token, still consider it valid
                    pass

            return True
        except ClientAuthenticationError:
            self._is_authenticated = False
            return False
        except Exception:
            return False

    def get_credentials(self) -> Dict[str, Any]:
        """Get non-sensitive Azure credential information.

        Returns:
            Dict[str, Any]: Dictionary with credential metadata
        """
        creds_info: Dict[str, Any] = {
            "provider": self.provider,
            "authenticated": self.is_authenticated(),
            "method": self._auth_method,
            "subscription_id": self.subscription_id,
            "tenant_id": self.tenant_id,
        }

        if self.is_authenticated() and self._credential and self.subscription_id:
            try:
                # Try to get resource group count as additional info
                client = ResourceManagementClient(
                    credential=self._credential, subscription_id=self.subscription_id
                )
                rg_list = list(client.resource_groups.list())
                creds_info["resource_group_count"] = len(rg_list)
            except Exception:
                pass

        return creds_info

    def refresh(self) -> bool:
        """Refresh Azure credentials.

        Re-initializes the credential object to get fresh tokens.

        Returns:
            bool: True if refresh was successful, False otherwise
        """
        self._initialize_credentials()
        return self.validate()

    def get_credential(self):
        """Get the Azure credential object for making API calls.

        Returns:
            Azure credential object (DefaultAzureCredential or similar)

        Raises:
            RuntimeError: If not authenticated
        """
        if not self.is_authenticated():
            raise RuntimeError(
                "Not authenticated with Azure. Please configure credentials."
            )

        return self._credential
