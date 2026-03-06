"""
Integration tests for AWS provider with CloudService model.

Tests the conversion of AWS EC2 resources to the unified CloudService model.
"""

from datetime import datetime
from typing import NotRequired, TypedDict
from unittest.mock import MagicMock, Mock

import pytest

from src.cli.auth.aws_auth import AWSAuth
from src.cli.models.service import CloudService
from src.cli.providers.aws import AWSProvider


class _StateDict(TypedDict):
    Name: str


class _PlacementDict(TypedDict):
    AvailabilityZone: str


class _EC2InstanceDict(TypedDict):
    InstanceId: str
    InstanceType: str
    State: _StateDict
    LaunchTime: datetime
    ImageId: str
    Placement: NotRequired[_PlacementDict]


class TestAWSCloudServiceIntegration:
    """Integration tests between AWS provider and CloudService model."""

    @pytest.fixture
    def mock_ec2_client(self) -> MagicMock:
        """Fixture providing a mock EC2 client."""
        return MagicMock()

    @pytest.fixture
    def aws_provider(self, mock_ec2_client: MagicMock) -> AWSProvider:
        """Fixture providing AWSProvider with mocked EC2 client."""
        mock_auth = Mock(spec=AWSAuth)
        mock_auth.is_authenticated.return_value = True
        mock_auth.region = "us-east-1"

        mock_session = Mock()
        mock_session.client.return_value = mock_ec2_client
        mock_auth.get_session.return_value = mock_session

        provider = AWSProvider(auth=mock_auth)
        return provider

    def test_ec2_response_to_cloud_service_conversion(self):
        """Test converting AWS EC2 response to CloudService model."""
        # Simulated AWS EC2 instance response
        ec2_instance: _EC2InstanceDict = {
            "InstanceId": "i-0123456789abcdef0",
            "InstanceType": "t2.micro",
            "State": {"Name": "running"},
            "LaunchTime": datetime(2024, 1, 15, 10, 30, 0),
            "ImageId": "ami-0123456789abcdef0",
            "Placement": {"AvailabilityZone": "us-east-1a"},
        }

        # Convert to CloudService
        service = CloudService(
            provider="aws",
            service_type="EC2",
            name=ec2_instance["InstanceId"],
            region="us-east-1",
            status=ec2_instance["State"]["Name"],
            created_at=ec2_instance["LaunchTime"].isoformat() + "Z",
            metadata={
                "instance_type": ec2_instance["InstanceType"],
                "image_id": ec2_instance["ImageId"],
                "availability_zone": ec2_instance["Placement"]["AvailabilityZone"],
            },
        )

        # Verify conversion
        assert service.provider == "aws"
        assert service.service_type == "EC2"
        assert service.name == "i-0123456789abcdef0"
        assert service.status == "running"
        assert service.metadata["instance_type"] == "t2.micro"

    def test_multiple_aws_instances_conversion(self):
        """Test converting multiple AWS EC2 instances to CloudService models."""
        ec2_instances: list[_EC2InstanceDict] = [
            {
                "InstanceId": "i-0123456789abcdef0",
                "InstanceType": "t2.micro",
                "State": {"Name": "running"},
                "LaunchTime": datetime(2024, 1, 15, 10, 30, 0),
                "ImageId": "ami-0123456789abcdef0",
            },
            {
                "InstanceId": "i-0123456789abcdef1",
                "InstanceType": "t2.small",
                "State": {"Name": "stopped"},
                "LaunchTime": datetime(2024, 1, 14, 8, 20, 0),
                "ImageId": "ami-0123456789abcdef1",
            },
        ]

        services: list[CloudService] = []
        for instance in ec2_instances:
            service = CloudService(
                provider="aws",
                service_type="EC2",
                name=instance["InstanceId"],
                region="us-east-1",
                status=instance["State"]["Name"],
                created_at=instance["LaunchTime"].isoformat() + "Z",
                metadata={
                    "instance_type": instance["InstanceType"],
                    "image_id": instance["ImageId"],
                },
            )
            services.append(service)

        # Verify conversion of multiple instances
        assert len(services) == 2
        assert services[0].name == "i-0123456789abcdef0"
        assert services[0].status == "running"
        assert services[1].name == "i-0123456789abcdef1"
        assert services[1].status == "stopped"

    def test_aws_service_serialization_for_cli_output(self):
        """Test that CloudService can be serialized for CLI output."""
        service = CloudService(
            provider="aws",
            service_type="EC2",
            name="i-0123456789abcdef0",
            region="us-east-1",
            status="running",
            created_at="2024-01-15T10:30:00Z",
            metadata={"instance_type": "t2.micro", "image_id": "ami-0123456789abcdef0"},
        )

        # Test JSON output (for --format json)
        json_output = service.to_json()
        assert "i-0123456789abcdef0" in json_output
        assert "t2.micro" in json_output

        # Test CSV output
        csv_dict = service.to_csv_dict()
        assert csv_dict["provider"] == "aws"
        assert csv_dict["name"] == "i-0123456789abcdef0"

    def test_aws_provider_list_services_mock(
        self, aws_provider: AWSProvider, mock_ec2_client: MagicMock
    ):
        """Test AWSProvider.list_services with mocked EC2 client."""
        # Mock EC2 describe_instances response
        mock_response: dict[str, list[dict[str, list[_EC2InstanceDict]]]] = {
            "Reservations": [
                {
                    "Instances": [
                        {
                            "InstanceId": "i-0123456789abcdef0",
                            "InstanceType": "t2.micro",
                            "State": {"Name": "running"},
                            "LaunchTime": datetime(2024, 1, 15, 10, 30, 0),
                            "ImageId": "ami-0123456789abcdef0",
                        }
                    ]
                }
            ]
        }

        mock_ec2_client.describe_instances.return_value = mock_response
        mock_ec2_client.describe_regions.return_value = {
            "Regions": [{"RegionName": "us-east-1"}]
        }

        # Call list_services
        services = aws_provider.list_services(region="us-east-1")

        # Verify results
        assert len(services) == 1
        assert services[0].provider == "aws"
        assert services[0].name == "i-0123456789abcdef0"
        assert services[0].status == "running"

    def test_aws_provider_get_service_mock(
        self, aws_provider: AWSProvider, mock_ec2_client: MagicMock
    ):
        """Test AWSProvider.get_service with mocked EC2 client."""
        # Mock EC2 describe_instances response for single instance
        mock_response: dict[str, list[dict[str, list[_EC2InstanceDict]]]] = {
            "Reservations": [
                {
                    "Instances": [
                        {
                            "InstanceId": "i-0123456789abcdef0",
                            "InstanceType": "t2.micro",
                            "State": {"Name": "running"},
                            "LaunchTime": datetime(2024, 1, 15, 10, 30, 0),
                            "ImageId": "ami-0123456789abcdef0",
                            "Placement": {"AvailabilityZone": "us-east-1a"},
                        }
                    ]
                }
            ]
        }

        mock_ec2_client.describe_instances.return_value = mock_response

        # Call get_service with explicit region to avoid scanning all regions
        service = aws_provider.get_service("i-0123456789abcdef0", region="us-east-1")

        # Verify results
        assert service is not None
        assert service.provider == "aws"
        assert service.name == "i-0123456789abcdef0"
        assert service.service_type == "EC2"

    def test_cloud_service_consistency_across_providers(self):
        """Test that CloudService can represent resources from different providers consistently."""
        # AWS EC2 Instance
        aws_service = CloudService(
            provider="aws",
            service_type="EC2",
            name="i-0123456789abcdef0",
            region="us-east-1",
            status="running",
            created_at="2024-01-15T10:30:00Z",
            metadata={"instance_type": "t2.micro"},
        )

        # GCP Compute Engine Instance
        gcp_service = CloudService(
            provider="gcp",
            service_type="Compute Engine",
            name="instance-1",
            region="us-central1-a",
            status="RUNNING",
            created_at="2024-01-14T08:20:00Z",
            metadata={"machine_type": "n1-standard-1"},
        )

        # Azure Virtual Machine
        azure_service = CloudService(
            provider="azure",
            service_type="Virtual Machine",
            name="vm-01",
            region="eastus",
            status="running",
            created_at="2024-01-16T14:45:00Z",
            metadata={"size": "Standard_B1s"},
        )

        # All should be serializable consistently
        services = [aws_service, gcp_service, azure_service]
        for service in services:
            # to_dict
            dict_data = service.to_dict()
            assert all(
                k in dict_data
                for k in [
                    "provider",
                    "service_type",
                    "name",
                    "region",
                    "status",
                    "created_at",
                ]
            )

            # to_json
            json_str = service.to_json()
            assert isinstance(json_str, str)

            # roundtrip
            restored = CloudService.from_json(json_str)
            assert restored.provider == service.provider
            assert restored.name == service.name
