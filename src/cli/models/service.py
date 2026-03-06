"""
Data models for cloud services.

This module provides the unified CloudService model that maps resources
from AWS, GCP, and Azure to a common interface.
"""

import json
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Literal

from pydantic import BaseModel, Field, field_validator


class CloudProvider(str, Enum):
    """Supported cloud providers.

    Attributes:
        AWS: Amazon Web Services
        GCP: Google Cloud Platform
        AZURE: Microsoft Azure
    """

    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"


class CloudService(BaseModel):
    """Unified representation of a cloud service resource.

    This model maps resources from all supported cloud providers (AWS, GCP, Azure)
    to a common schema, enabling consistent handling across providers.

    Attributes:
        provider: Cloud provider identifier ("aws" | "gcp" | "azure")
        service_type: Type of service (e.g., "EC2", "Compute Engine", "Virtual Machine")
        name: Resource name or ID
        region: Region or zone name
        status: Resource status (provider-dependent)
        created_at: Creation timestamp in ISO 8601 format (e.g., "2024-01-15T10:30:00Z")
        metadata: Provider-specific additional information (default: empty dict)

    Example:
        >>> service = CloudService(
        ...     provider="aws",
        ...     service_type="EC2",
        ...     name="i-0123456789abcdef0",
        ...     region="us-east-1",
        ...     status="running",
        ...     created_at="2024-01-15T10:30:00Z",
        ...     metadata={"instance_type": "t2.micro"}
        ... )
        >>> service.to_dict()
        {'provider': 'aws', 'service_type': 'EC2', ...}
    """

    provider: Literal["aws", "gcp", "azure"] = Field(
        ..., description="Cloud provider identifier"
    )
    service_type: str = Field(
        ..., description="Type of cloud service", min_length=1, max_length=100
    )
    name: str = Field(
        ..., description="Resource name or ID", min_length=1, max_length=255
    )
    region: str = Field(
        ...,
        description="Region or availability zone name",
        min_length=1,
        max_length=100,
    )
    status: str = Field(..., description="Resource status", min_length=1, max_length=50)
    created_at: str = Field(..., description="Creation timestamp in ISO 8601 format")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Provider-specific metadata"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "provider": "aws",
                    "service_type": "EC2",
                    "name": "i-0123456789abcdef0",
                    "region": "us-east-1",
                    "status": "running",
                    "created_at": "2024-01-15T10:30:00Z",
                    "metadata": {"instance_type": "t2.micro"},
                }
            ]
        }
    }

    @field_validator("created_at")
    @classmethod
    def validate_iso8601(cls, v: str) -> str:
        """Validate and normalize ISO 8601 timestamp format.

        Args:
            v: Timestamp string to validate

        Returns:
            Validated ISO 8601 formatted timestamp

        Raises:
            ValueError: If timestamp is not in valid ISO 8601 format
        """
        try:
            # Try to parse ISO 8601 format
            dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
            # Return in standard format with Z suffix
            return dt.isoformat().replace("+00:00", "Z")
        except (ValueError, AttributeError) as e:
            raise ValueError(
                f"Invalid ISO 8601 timestamp format: '{v}'. "
                f"Expected format: '2024-01-15T10:30:00Z' or '2024-01-15T10:30:00+00:00'"
            ) from e

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format.

        Returns:
            Dictionary representation of the CloudService
        """
        return self.model_dump()

    def to_json(self) -> str:
        """Convert to JSON string.

        Returns:
            JSON string representation of the CloudService
        """
        return self.model_dump_json()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CloudService":
        """Create CloudService instance from dictionary.

        Args:
            data: Dictionary containing CloudService fields

        Returns:
            CloudService instance

        Raises:
            ValidationError: If data does not match CloudService schema
        """
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> "CloudService":
        """Create CloudService instance from JSON string.

        Args:
            json_str: JSON string representation

        Returns:
            CloudService instance

        Raises:
            ValidationError: If JSON does not match CloudService schema
        """
        return cls.model_validate_json(json_str)

    def to_csv_dict(self) -> Dict[str, Any]:
        """Convert to CSV-compatible dictionary format.

        Converts metadata to JSON string for CSV serialization.

        Returns:
            Dictionary with metadata as JSON string for CSV export

        Example:
            >>> service.to_csv_dict()
            {'provider': 'aws', 'service_type': 'EC2',
             'metadata': '{"instance_type": "t2.micro"}'}
        """
        data = self.model_dump()
        if data.get("metadata"):
            data["metadata"] = json.dumps(data["metadata"])
        return data
