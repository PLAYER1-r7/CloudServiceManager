"""
Data models for cloud services.
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class CloudProvider(str, Enum):
    """Supported cloud providers."""
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"


@dataclass
class CloudService:
    """Representation of a cloud service resource."""
    provider: CloudProvider
    service_type: str
    name: str
    region: str
    status: str
    created_at: Optional[str] = None
    metadata: Optional[dict] = None

    def to_dict(self) -> dict:
        """Convert to dictionary format."""
        return {
            "provider": self.provider.value,
            "service_type": self.service_type,
            "name": self.name,
            "region": self.region,
            "status": self.status,
            "created_at": self.created_at,
            "metadata": self.metadata or {},
        }
