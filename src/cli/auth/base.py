"""Base authentication interface for cloud providers."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class CloudAuthBase(ABC):
    """Abstract base class for cloud provider authentication.

    This class defines the interface that all cloud provider authentication
    implementations must follow. It provides methods for checking authentication
    status, validating credentials, and refreshing tokens.
    """

    provider: str  # "aws", "gcp", or "azure"

    def __init__(self) -> None:
        """Initialize the authentication handler."""
        self._is_authenticated = False

    @abstractmethod
    def is_authenticated(self) -> bool:
        """Check if authentication is currently valid.

        Returns:
            bool: True if authenticated, False otherwise
        """
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Validate the authentication credentials.

        This method should check if the credentials are valid and can be used
        to make API calls to the cloud provider.

        Returns:
            bool: True if credentials are valid, False otherwise

        Raises:
            Exception: If validation fails due to an error
        """
        pass

    @abstractmethod
    def get_credentials(self) -> Dict[str, Any]:
        """Get non-sensitive credential information.

        Returns a dictionary containing metadata about the credentials,
        but excludes sensitive information like access keys or secrets.

        Returns:
            Dict[str, Any]: Dictionary with credential metadata:
                - provider: Cloud provider name
                - authenticated: Whether authentication is active
                - method: Authentication method used (e.g., "env", "file", "role")
                - region: Default region (if applicable)
                - account_id: Account/Project ID (if available)
        """
        pass

    @abstractmethod
    def refresh(self) -> bool:
        """Refresh authentication credentials.

        For providers that use tokens or temporary credentials, this method
        should refresh them. For static credentials, this may be a no-op.

        Returns:
            bool: True if refresh was successful, False otherwise
        """
        pass

    def __repr__(self) -> str:
        """Return string representation of the authentication object."""
        return f"<{self.__class__.__name__} provider={self.provider} authenticated={self._is_authenticated}>"
