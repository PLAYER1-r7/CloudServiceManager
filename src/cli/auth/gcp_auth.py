"""GCP authentication handler."""

import os
from typing import Any, Dict, Optional

from google.auth import default
from google.auth.exceptions import DefaultCredentialsError
from google.cloud import compute_v1
from google.oauth2 import service_account

from .base import CloudAuthBase


class GCPAuth(CloudAuthBase):
    """GCP authentication handler.

    Supports multiple authentication methods:
    1. Service account key file (GOOGLE_APPLICATION_CREDENTIALS)
    2. Application Default Credentials (ADC)
    3. Compute Engine default service account
    4. gcloud CLI credentials

    The authentication follows Google's Application Default Credentials chain.
    """

    provider = "gcp"

    def __init__(
        self, project_id: Optional[str] = None, credentials_file: Optional[str] = None
    ) -> None:
        """Initialize GCP authentication.

        Args:
            project_id: GCP project ID (default: from credentials or env)
            credentials_file: Path to service account JSON file
        """
        super().__init__()
        self._project_id = (
            project_id
            or os.getenv("GCP_PROJECT")
            or os.getenv("GCLOUD_PROJECT")
            or os.getenv("GOOGLE_CLOUD_PROJECT")
        )
        self._credentials_file = credentials_file or os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )
        self._credentials = None
        self._auth_method: Optional[str] = None

        # Try to initialize credentials
        self._initialize_credentials()

    def _initialize_credentials(self) -> None:
        """Initialize Google Cloud credentials."""
        try:
            if self._credentials_file and os.path.exists(self._credentials_file):
                # Use service account key file
                self._credentials = (
                    service_account.Credentials.from_service_account_file(
                        self._credentials_file
                    )
                )
                self._auth_method = "service_account_file"

                # Extract project ID from service account file if not provided
                if not self._project_id:
                    import json

                    with open(self._credentials_file, "r") as f:
                        sa_info = json.load(f)
                        self._project_id = sa_info.get("project_id")
            else:
                # Use Application Default Credentials
                self._credentials, project = default()
                self._auth_method = "application_default"

                if not self._project_id:
                    self._project_id = project

            self._is_authenticated = True

        except DefaultCredentialsError:
            self._is_authenticated = False
            self._auth_method = None
        except Exception:
            self._is_authenticated = False
            self._auth_method = None

    def is_authenticated(self) -> bool:
        """Check if GCP authentication is currently valid.

        Returns:
            bool: True if authenticated, False otherwise
        """
        return self._is_authenticated and self._credentials is not None

    def validate(self) -> bool:
        """Validate GCP credentials by making a test API call.

        Returns:
            bool: True if credentials are valid, False otherwise
        """
        if not self.is_authenticated():
            return False

        if not self._project_id:
            # Can't validate without a project ID
            return False

        try:
            # Try to list zones as a simple validation
            client = compute_v1.ZonesClient(credentials=self._credentials)
            # Just check if we can create the request (don't actually list)
            # This validates the credentials without making unnecessary API calls
            request = compute_v1.ListZonesRequest(project=self._project_id)
            # Attempt to make the call with a limit of 1 to minimize cost
            list(client.list(request=request, max_results=1))
            return True
        except Exception:
            self._is_authenticated = False
            return False

    def get_credentials(self) -> Dict[str, Any]:
        """Get non-sensitive GCP credential information.

        Returns:
            Dict[str, Any]: Dictionary with credential metadata
        """
        creds_info: Dict[str, Any] = {
            "provider": self.provider,
            "authenticated": self.is_authenticated(),
            "method": self._auth_method,
            "project_id": self._project_id,
        }

        if self.is_authenticated() and self._credentials:
            # Add service account email if available
            if hasattr(self._credentials, "service_account_email"):
                creds_info["service_account_email"] = (
                    self._credentials.service_account_email
                )

            # Add quota project if available
            if hasattr(self._credentials, "quota_project_id"):
                creds_info["quota_project_id"] = self._credentials.quota_project_id

        return creds_info

    def refresh(self) -> bool:
        """Refresh GCP credentials.

        For OAuth2 tokens, this refreshes the access token.
        For service accounts, this validates they're still valid.

        Returns:
            bool: True if refresh was successful, False otherwise
        """
        if not self.is_authenticated():
            self._initialize_credentials()
            return self.is_authenticated()

        try:
            # Refresh the credentials if they support it
            if hasattr(self._credentials, "refresh"):
                import google.auth.transport.requests

                request = google.auth.transport.requests.Request()
                self._credentials.refresh(request)

            return self.validate()
        except Exception:
            self._is_authenticated = False
            return False

    def get_credentials_object(self):
        """Get the Google credentials object for making API calls.

        Returns:
            google.auth.credentials.Credentials: The authenticated credentials object

        Raises:
            RuntimeError: If not authenticated
        """
        if not self.is_authenticated():
            raise RuntimeError(
                "Not authenticated with GCP. Please configure credentials."
            )

        return self._credentials

    @property
    def project_id(self) -> Optional[str]:
        """Get the GCP project ID.

        Returns:
            Optional[str]: The project ID if available
        """
        return self._project_id

    def set_project(self, project_id: str) -> bool:
        """Switch the active GCP project.

        This method only updates the target project ID for future API calls.

        Args:
            project_id: New GCP project ID

        Returns:
            bool: True when a non-empty project ID was applied, False otherwise
        """
        normalized = (project_id or "").strip()
        if not normalized:
            return False

        self._project_id = normalized
        return True
