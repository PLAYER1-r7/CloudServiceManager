"""Base provider interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..models.service import CloudService


class BaseProvider(ABC):
    """Abstract base class for cloud providers."""

    @abstractmethod
    def list_services(self, region: Optional[str] = None) -> List[CloudService]:
        """
        List all services from this provider.
        
        Args:
            region: Optional region filter
            
        Returns:
            List of CloudService objects
        """
        pass

    @abstractmethod
    def get_service(self, service_id: str) -> Optional[CloudService]:
        """
        Get a specific service by ID.
        
        Args:
            service_id: Service identifier
            
        Returns:
            CloudService object or None if not found
        """
        pass
