"""
Tests for AWS provider implementation.

Comprehensive tests for AWSProvider class including:
- Authentication integration
- Instance listing
- Instance retrieval
- Region handling
- Error handling
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError

from src.cli.auth.aws_auth import AWSAuth
from src.cli.providers.aws import AWSProvider


class TestAWSProvider:
    """Test suite for AWS provider."""

    @pytest.fixture
    def mock_auth(self):
        """Fixture providing a mocked AWSAuth."""
        mock = Mock(spec=AWSAuth)
        mock.is_authenticated.return_value = True
        mock.region = "us-east-1"

        # Mock session
        mock_session = Mock()
        mock.get_session.return_value = mock_session

        return mock

    @pytest.fixture
    def mock_ec2_client(self):
        """Fixture providing a mocked EC2 client."""
        return MagicMock()

    @pytest.fixture
    def aws_provider(self, mock_auth):
        """Fixture providing AWSProvider with mocked auth."""
        return AWSProvider(auth=mock_auth)

    def test_initialization_with_auth(self, mock_auth):
        """Test AWSProvider initialization with provided auth."""
        provider = AWSProvider(auth=mock_auth)
        assert provider.auth == mock_auth
        assert provider.region == "us-east-1"

    def test_initialization_without_auth(self):
        """Test AWSProvider initialization without auth (creates new AWSAuth)."""
        with patch("src.cli.providers.aws.AWSAuth") as mock_auth_class:
            mock_auth_instance = Mock()
            mock_auth_instance.is_authenticated.return_value = True
            mock_auth_instance.region = "us-west-2"
            mock_auth_class.return_value = mock_auth_instance

            provider = AWSProvider(region="us-west-2")

            mock_auth_class.assert_called_once_with(region="us-west-2")
            assert provider.region == "us-west-2"

    def test_initialization_fails_without_credentials(self):
        """Test that initialization fails when not authenticated."""
        with patch("src.cli.providers.aws.AWSAuth") as mock_auth_class:
            mock_auth_instance = Mock()
            mock_auth_instance.is_authenticated.return_value = False
            mock_auth_class.return_value = mock_auth_instance

            with pytest.raises(RuntimeError, match="AWS authentication failed"):
                AWSProvider()

    def test_list_services_single_region(
        self, aws_provider, mock_auth, mock_ec2_client
    ):
        """Test listing services from a single region."""
        # Mock EC2 response
        mock_response = {
            "Reservations": [
                {
                    "Instances": [
                        {
                            "InstanceId": "i-0123456789abcdef0",
                            "InstanceType": "t2.micro",
                            "State": {"Name": "running"},
                            "LaunchTime": datetime(2024, 1, 15, 10, 30, 0),
                            "ImageId": "ami-abc123",
                            "VpcId": "vpc-123",
                            "SubnetId": "subnet-123",
                            "PrivateIpAddress": "10.0.1.5",
                            "PublicIpAddress": "54.123.45.67",
                            "Placement": {"AvailabilityZone": "us-east-1a"},
                        }
                    ]
                }
            ]
        }

        mock_ec2_client.describe_instances.return_value = mock_response
        mock_auth.get_session.return_value.client.return_value = mock_ec2_client

        # Call list_services
        services = aws_provider.list_services(region="us-east-1")

        # Verify results
        assert len(services) == 1
        service = services[0]
        assert service.provider == "aws"
        assert service.service_type == "EC2"
        assert service.name == "i-0123456789abcdef0"
        assert service.region == "us-east-1"
        assert service.status == "running"
        assert service.metadata["instance_type"] == "t2.micro"
        assert service.metadata["image_id"] == "ami-abc123"
        assert service.metadata["vpc_id"] == "vpc-123"
        assert service.metadata["public_ip"] == "54.123.45.67"

    def test_list_services_all_regions(self, aws_provider, mock_auth, mock_ec2_client):
        """Test listing services from all regions."""
        # Mock regions response
        mock_regions_response = {
            "Regions": [{"RegionName": "us-east-1"}, {"RegionName": "us-west-2"}]
        }

        # Mock instances response (different for each region)
        mock_instances_us_east = {
            "Reservations": [
                {
                    "Instances": [
                        {
                            "InstanceId": "i-east-1",
                            "InstanceType": "t2.micro",
                            "State": {"Name": "running"},
                            "LaunchTime": datetime(2024, 1, 15, 10, 30, 0),
                            "ImageId": "ami-abc123",
                            "Placement": {"AvailabilityZone": "us-east-1a"},
                        }
                    ]
                }
            ]
        }

        mock_instances_us_west = {
            "Reservations": [
                {
                    "Instances": [
                        {
                            "InstanceId": "i-west-1",
                            "InstanceType": "t2.small",
                            "State": {"Name": "stopped"},
                            "LaunchTime": datetime(2024, 1, 14, 8, 20, 0),
                            "ImageId": "ami-def456",
                            "Placement": {"AvailabilityZone": "us-west-2a"},
                        }
                    ]
                }
            ]
        }

        # Setup mock client to return different results based on region
        def create_client_side_effect(service, region_name=None):
            client = MagicMock()
            if service == "ec2":
                if not region_name or region_name == "us-east-1":
                    client.describe_regions.return_value = mock_regions_response
                    client.describe_instances.return_value = mock_instances_us_east
                elif region_name == "us-west-2":
                    client.describe_instances.return_value = mock_instances_us_west
            return client

        mock_auth.get_session.return_value.client.side_effect = (
            create_client_side_effect
        )

        # Call list_services without region (all regions)
        services = aws_provider.list_services()

        # Verify results
        assert len(services) == 2
        assert services[0].name == "i-east-1"
        assert services[0].region == "us-east-1"
        assert services[1].name == "i-west-1"
        assert services[1].region == "us-west-2"

    def test_list_services_empty_result(self, aws_provider, mock_auth, mock_ec2_client):
        """Test listing services when no instances exist."""
        mock_response = {"Reservations": []}

        mock_ec2_client.describe_instances.return_value = mock_response
        mock_auth.get_session.return_value.client.return_value = mock_ec2_client

        services = aws_provider.list_services(region="us-east-1")

        assert len(services) == 0
        assert isinstance(services, list)

    def test_list_services_handles_unauthorized_region(
        self, aws_provider, mock_auth, mock_ec2_client
    ):
        """Test that unauthorized regions are skipped gracefully."""
        # Mock regions response
        mock_regions_response = {
            "Regions": [
                {"RegionName": "us-east-1"},
                {"RegionName": "ap-southeast-1"},  # Unauthorized
            ]
        }

        # First region succeeds, second fails with UnauthorizedOperation
        mock_instances_response = {
            "Reservations": [
                {
                    "Instances": [
                        {
                            "InstanceId": "i-authorized",
                            "InstanceType": "t2.micro",
                            "State": {"Name": "running"},
                            "LaunchTime": datetime(2024, 1, 15, 10, 30, 0),
                            "ImageId": "ami-abc123",
                            "Placement": {"AvailabilityZone": "us-east-1a"},
                        }
                    ]
                }
            ]
        }

        def create_client_side_effect(service, region_name=None):
            client = MagicMock()
            if service == "ec2":
                if region_name == "us-east-1":
                    client.describe_regions.return_value = mock_regions_response
                    client.describe_instances.return_value = mock_instances_response
                elif region_name == "ap-southeast-1":
                    error_response = {"Error": {"Code": "UnauthorizedOperation"}}
                    client.describe_instances.side_effect = ClientError(
                        error_response, "describe_instances"
                    )
            return client

        mock_auth.get_session.return_value.client.side_effect = (
            create_client_side_effect
        )

        # Should skip unauthorized region and return results from authorized region
        services = aws_provider.list_services()

        assert len(services) == 1
        assert services[0].name == "i-authorized"

    def test_get_service_found(self, aws_provider, mock_auth, mock_ec2_client):
        """Test getting a specific service by ID."""
        mock_response = {
            "Reservations": [
                {
                    "Instances": [
                        {
                            "InstanceId": "i-0123456789abcdef0",
                            "InstanceType": "t2.micro",
                            "State": {"Name": "running"},
                            "LaunchTime": datetime(2024, 1, 15, 10, 30, 0),
                            "ImageId": "ami-abc123",
                            "Placement": {"AvailabilityZone": "us-east-1a"},
                        }
                    ]
                }
            ]
        }

        mock_ec2_client.describe_instances.return_value = mock_response
        mock_auth.get_session.return_value.client.return_value = mock_ec2_client

        service = aws_provider.get_service("i-0123456789abcdef0", region="us-east-1")

        assert service is not None
        assert service.name == "i-0123456789abcdef0"
        assert service.status == "running"

    def test_get_service_not_found(self, aws_provider, mock_auth, mock_ec2_client):
        """Test getting a service that doesn't exist."""
        error_response = {"Error": {"Code": "InvalidInstanceID.NotFound"}}
        mock_ec2_client.describe_instances.side_effect = ClientError(
            error_response, "describe_instances"
        )
        mock_auth.get_session.return_value.client.return_value = mock_ec2_client

        # Mock _get_all_regions to avoid additional calls
        with patch.object(aws_provider, "_get_all_regions", return_value=["us-east-1"]):
            service = aws_provider.get_service("i-nonexistent", region="us-east-1")

        assert service is None

    def test_get_service_searches_all_regions(self, aws_provider, mock_auth):
        """Test that get_service searches all regions when region not specified."""
        # Mock regions
        mock_regions = ["us-east-1", "us-west-2", "eu-west-1"]

        # Instance found in third region
        def create_client_side_effect(service, region_name=None):
            client = MagicMock()
            if service == "ec2":
                if region_name in ["us-east-1", "us-west-2"]:
                    # Not found in first two regions
                    error_response = {"Error": {"Code": "InvalidInstanceID.NotFound"}}
                    client.describe_instances.side_effect = ClientError(
                        error_response, "describe_instances"
                    )
                elif region_name == "eu-west-1":
                    # Found in third region
                    client.describe_instances.return_value = {
                        "Reservations": [
                            {
                                "Instances": [
                                    {
                                        "InstanceId": "i-found-in-eu",
                                        "InstanceType": "t2.micro",
                                        "State": {"Name": "running"},
                                        "LaunchTime": datetime(2024, 1, 15, 10, 30, 0),
                                        "ImageId": "ami-abc123",
                                        "Placement": {"AvailabilityZone": "eu-west-1a"},
                                    }
                                ]
                            }
                        ]
                    }
            return client

        mock_auth.get_session.return_value.client.side_effect = (
            create_client_side_effect
        )

        with patch.object(aws_provider, "_get_all_regions", return_value=mock_regions):
            service = aws_provider.get_service("i-found-in-eu")

        assert service is not None
        assert service.name == "i-found-in-eu"
        assert service.region == "eu-west-1"

    def test_convert_to_cloud_service_complete(self, aws_provider):
        """Test _convert_to_cloud_service with all fields."""
        instance = {
            "InstanceId": "i-0123456789abcdef0",
            "InstanceType": "t2.micro",
            "State": {"Name": "running"},
            "LaunchTime": datetime(2024, 1, 15, 10, 30, 0),
            "ImageId": "ami-abc123",
            "VpcId": "vpc-123",
            "SubnetId": "subnet-123",
            "PrivateIpAddress": "10.0.1.5",
            "PublicIpAddress": "54.123.45.67",
            "Placement": {"AvailabilityZone": "us-east-1a"},
        }

        service = aws_provider._convert_to_cloud_service(instance, "us-east-1")

        assert service.provider == "aws"
        assert service.service_type == "EC2"
        assert service.name == "i-0123456789abcdef0"
        assert service.region == "us-east-1"
        assert service.status == "running"
        assert service.created_at == "2024-01-15T10:30:00Z"
        assert service.metadata["instance_type"] == "t2.micro"
        assert service.metadata["image_id"] == "ami-abc123"
        assert service.metadata["vpc_id"] == "vpc-123"
        assert service.metadata["subnet_id"] == "subnet-123"
        assert service.metadata["private_ip"] == "10.0.1.5"
        assert service.metadata["public_ip"] == "54.123.45.67"
        assert service.metadata["availability_zone"] == "us-east-1a"

    def test_convert_to_cloud_service_minimal(self, aws_provider):
        """Test _convert_to_cloud_service with minimal fields."""
        instance = {"InstanceId": "i-minimal", "State": {"Name": "pending"}}

        service = aws_provider._convert_to_cloud_service(instance, "us-west-2")

        assert service.provider == "aws"
        assert service.name == "i-minimal"
        assert service.region == "us-west-2"
        assert service.status == "pending"
        assert service.metadata["instance_type"] == "unknown"
        assert service.metadata["image_id"] == "unknown"
        # Optional fields should not be present
        assert "vpc_id" not in service.metadata
        assert "public_ip" not in service.metadata

    def test_convert_to_cloud_service_missing_instance_id(self, aws_provider):
        """Test that conversion fails without instance ID."""
        instance = {"InstanceType": "t2.micro", "State": {"Name": "running"}}

        with pytest.raises(ValueError, match="Instance ID is required"):
            aws_provider._convert_to_cloud_service(instance, "us-east-1")

    def test_get_all_regions_success(self, aws_provider, mock_auth, mock_ec2_client):
        """Test _get_all_regions returns all regions."""
        mock_response = {
            "Regions": [
                {"RegionName": "us-east-1"},
                {"RegionName": "us-west-2"},
                {"RegionName": "eu-west-1"},
            ]
        }

        mock_ec2_client.describe_regions.return_value = mock_response
        mock_auth.get_session.return_value.client.return_value = mock_ec2_client

        regions = aws_provider._get_all_regions()

        assert len(regions) == 3
        assert "us-east-1" in regions
        assert "us-west-2" in regions
        assert "eu-west-1" in regions

    def test_get_all_regions_failure_fallback(
        self, aws_provider, mock_auth, mock_ec2_client
    ):
        """Test _get_all_regions falls back to default region on error."""
        mock_ec2_client.describe_regions.side_effect = Exception("API Error")
        mock_auth.get_session.return_value.client.return_value = mock_ec2_client

        regions = aws_provider._get_all_regions()

        # Should fall back to provider's default region
        assert len(regions) == 1
        assert regions[0] == aws_provider.region

    def test_list_services_raises_no_credentials_error(self, aws_provider, mock_auth):
        """Test that NoCredentialsError is raised when credentials are missing."""
        mock_auth.get_session.side_effect = NoCredentialsError()

        with pytest.raises(NoCredentialsError):
            aws_provider.list_services(region="us-east-1")

    def test_created_at_format(self, aws_provider):
        """Test that created_at is properly formatted in ISO 8601 with Z suffix."""
        instance = {
            "InstanceId": "i-datetime-test",
            "State": {"Name": "running"},
            "LaunchTime": datetime(2024, 1, 15, 10, 30, 45),
        }

        service = aws_provider._convert_to_cloud_service(instance, "us-east-1")

        # Verify ISO 8601 format with Z suffix
        assert service.created_at == "2024-01-15T10:30:45Z"

        # Verify it can be parsed back to datetime
        from datetime import datetime as dt

        parsed = dt.fromisoformat(service.created_at.replace("Z", "+00:00"))
        assert parsed.year == 2024
        assert parsed.month == 1
        assert parsed.day == 15
