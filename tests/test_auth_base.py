"""Tests for CloudAuthBase abstract class."""

import pytest
from typing import Any, Dict

from src.cli.auth.base import CloudAuthBase


class ConcreteAuth(CloudAuthBase):
    """Concrete implementation for testing the abstract base class."""

    provider = "test"

    def __init__(self, authenticated: bool = True):
        super().__init__()
        self._is_authenticated = authenticated
        self.validated = False
        self.refreshed = False

    def is_authenticated(self) -> bool:
        return self._is_authenticated

    def validate(self) -> bool:
        self.validated = True
        return self._is_authenticated

    def get_credentials(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "authenticated": self._is_authenticated,
            "test": True,
        }

    def refresh(self) -> bool:
        self.refreshed = True
        return self._is_authenticated


class TestCloudAuthBase:
    """Test suite for CloudAuthBase abstract class."""

    def test_cannot_instantiate_abstract_class(self):
        """Test that CloudAuthBase cannot be instantiated directly."""
        with pytest.raises(TypeError):
            CloudAuthBase()

    def test_concrete_implementation_works(self):
        """Test that concrete implementation can be instantiated."""
        auth = ConcreteAuth()
        assert auth is not None
        assert auth.provider == "test"

    def test_is_authenticated_returns_bool(self):
        """Test is_authenticated returns boolean."""
        auth = ConcreteAuth(authenticated=True)
        assert auth.is_authenticated() is True

        auth_false = ConcreteAuth(authenticated=False)
        assert auth_false.is_authenticated() is False

    def test_validate_returns_bool(self):
        """Test validate returns boolean."""
        auth = ConcreteAuth(authenticated=True)
        result = auth.validate()
        assert isinstance(result, bool)
        assert result is True
        assert auth.validated is True

    def test_get_credentials_returns_dict(self):
        """Test get_credentials returns dictionary."""
        auth = ConcreteAuth()
        creds = auth.get_credentials()
        assert isinstance(creds, dict)
        assert "provider" in creds
        assert creds["provider"] == "test"

    def test_refresh_returns_bool(self):
        """Test refresh returns boolean."""
        auth = ConcreteAuth(authenticated=True)
        result = auth.refresh()
        assert isinstance(result, bool)
        assert result is True
        assert auth.refreshed is True

    def test_provider_attribute_exists(self):
        """Test that provider attribute is accessible."""
        auth = ConcreteAuth()
        assert hasattr(auth, "provider")
        assert isinstance(auth.provider, str)


class TestCloudAuthBaseInterface:
    """Test the interface contract of CloudAuthBase."""

    def test_subclass_must_implement_all_methods(self):
        """Test that subclass must implement all abstract methods."""

        # Missing is_authenticated
        with pytest.raises(TypeError):

            class IncompleteAuth1(CloudAuthBase):
                provider = "incomplete"

                def validate(self):
                    return True

                def get_credentials(self):
                    return {}

                def refresh(self):
                    return True

            IncompleteAuth1()

        # Missing validate
        with pytest.raises(TypeError):

            class IncompleteAuth2(CloudAuthBase):
                provider = "incomplete"

                def is_authenticated(self):
                    return True

                def get_credentials(self):
                    return {}

                def refresh(self):
                    return True

            IncompleteAuth2()

    def test_provider_attribute_required(self):
        """Test that provider attribute should be defined in subclasses."""
        auth = ConcreteAuth()
        assert auth.provider is not None
        assert len(auth.provider) > 0
