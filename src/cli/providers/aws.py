"""AWS cloud provider implementation."""

import logging
from datetime import datetime
from typing import List, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError

from ..auth.aws_auth import AWSAuth
from ..models.service import CloudService, CloudProvider

logger = logging.getLogger(__name__)


class AWSProvider:
    """AWS service provider for listing and managing EC2 instances.
    
    This provider integrates with AWSAuth for authentication and provides
    methods to list and retrieve EC2 instances, converting them to the
    unified CloudService model.
    
    Attributes:
        auth: AWSAuth instance for authentication
        region: AWS region to use (can be overridden per method call)
    """

    def __init__(self, auth: Optional[AWSAuth] = None, region: Optional[str] = None):
        """Initialize AWS provider with authentication.
        
        Args:
            auth: Optional AWSAuth instance. If not provided, creates a new instance.
            region: Optional AWS region. If not provided, uses auth's region or default.
            
        Raises:
            RuntimeError: If authentication fails
        """
        self.auth = auth or AWSAuth(region=region)
        self.region = region or self.auth.region
        
        if not self.auth.is_authenticated():
            raise RuntimeError(
                "AWS authentication failed. Please configure credentials via:\n"
                "  - Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)\n"
                "  - AWS credentials file (~/.aws/credentials)\n"
                "  - IAM role (for EC2 instances)"
            )

    def list_services(self, region: Optional[str] = None) -> List[CloudService]:
        """
        List AWS EC2 instances across one or all regions.
        
        Args:
            region: Optional AWS region to filter by. If None, fetches from all regions.
            
        Returns:
            List of CloudService objects representing EC2 instances
            
        Raises:
            NoCredentialsError: If AWS credentials are not configured
            ClientError: If AWS API call fails
        """
        try:
            services = []
            
            # Get all regions if not specified
            if region:
                regions = [region]
            else:
                regions = self._get_all_regions()
                logger.info(f"Fetching EC2 instances from {len(regions)} regions")
            
            for reg in regions:
                logger.debug(f"Fetching EC2 instances from region: {reg}")
                ec2 = self.auth.get_session().client("ec2", region_name=reg)
                
                try:
                    response = ec2.describe_instances()
                    
                    for reservation in response.get("Reservations", []):
                        for instance in reservation.get("Instances", []):
                            try:
                                service = self._convert_to_cloud_service(instance, reg)
                                services.append(service)
                            except Exception as e:
                                logger.warning(
                                    f"Failed to convert instance {instance.get('InstanceId')} "
                                    f"in region {reg}: {e}"
                                )
                                
                except ClientError as e:
                    error_code = e.response.get("Error", {}).get("Code", "Unknown")
                    if error_code == "UnauthorizedOperation":
                        logger.warning(f"Unauthorized to access region {reg}, skipping")
                    else:
                        logger.error(f"Error fetching instances from region {reg}: {e}")
                        
            logger.info(f"Found {len(services)} EC2 instances")
            return services
            
        except NoCredentialsError:
            logger.error("AWS credentials not found")
            raise
        except BotoCoreError as e:
            logger.error(f"AWS SDK error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error listing AWS services: {e}")
            raise

    def get_service(self, service_id: str, region: Optional[str] = None) -> Optional[CloudService]:
        """
        Get a specific EC2 instance by ID.
        
        Args:
            service_id: EC2 instance ID (e.g., "i-0123456789abcdef0")
            region: Optional AWS region. If not specified, searches all regions.
            
        Returns:
            CloudService object if found, None otherwise
            
        Raises:
            ClientError: If AWS API call fails
        """
        try:
            # If region is specified, search only in that region
            if region:
                regions = [region]
            else:
                # Search in default region first, then others if not found
                regions = [self.region] + [r for r in self._get_all_regions() if r != self.region]
            
            for reg in regions:
                try:
                    ec2 = self.auth.get_session().client("ec2", region_name=reg)
                    response = ec2.describe_instances(InstanceIds=[service_id])
                    
                    if response.get("Reservations"):
                        instance = response["Reservations"][0]["Instances"][0]
                        logger.debug(f"Found instance {service_id} in region {reg}")
                        return self._convert_to_cloud_service(instance, reg)
                        
                except ClientError as e:
                    error_code = e.response.get("Error", {}).get("Code", "Unknown")
                    if error_code == "InvalidInstanceID.NotFound":
                        # Instance not in this region, continue searching
                        continue
                    else:
                        logger.error(f"Error fetching instance {service_id} from region {reg}: {e}")
                        raise
                        
            logger.warning(f"Instance {service_id} not found in any region")
            return None
            
        except NoCredentialsError:
            logger.error("AWS credentials not found")
            raise
        except Exception as e:
            logger.error(f"Unexpected error getting AWS service {service_id}: {e}")
            raise

    def _get_all_regions(self) -> List[str]:
        """Get all AWS regions.
        
        Returns:
            List of AWS region names
        """
        try:
            ec2 = self.auth.get_session().client("ec2", region_name=self.region)
            response = ec2.describe_regions()
            regions = [r["RegionName"] for r in response.get("Regions", [])]
            logger.debug(f"Retrieved {len(regions)} AWS regions")
            return regions
        except Exception as e:
            logger.warning(f"Failed to get AWS regions: {e}. Using default region.")
            return [self.region]
    
    def _convert_to_cloud_service(self, instance: dict, region: str) -> CloudService:
        """Convert AWS EC2 instance to CloudService model.
        
        Args:
            instance: AWS EC2 instance dictionary from boto3
            region: AWS region name
            
        Returns:
            CloudService object
            
        Raises:
            ValueError: If required fields are missing
        """
        instance_id = instance.get("InstanceId")
        if not instance_id:
            raise ValueError("Instance ID is required")
        
        # Extract and format launch time
        launch_time = instance.get("LaunchTime")
        if launch_time:
            if isinstance(launch_time, datetime):
                created_at = launch_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            else:
                created_at = str(launch_time)
        else:
            created_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Build metadata
        metadata = {
            "instance_type": instance.get("InstanceType", "unknown"),
            "image_id": instance.get("ImageId", "unknown"),
            "availability_zone": instance.get("Placement", {}).get("AvailabilityZone", region),
            "vpc_id": instance.get("VpcId"),
            "subnet_id": instance.get("SubnetId"),
            "private_ip": instance.get("PrivateIpAddress"),
            "public_ip": instance.get("PublicIpAddress"),
        }
        
        # Remove None values from metadata
        metadata = {k: v for k, v in metadata.items() if v is not None}
        
        return CloudService(
            provider=CloudProvider.AWS.value,
            service_type="EC2",
            name=instance_id,
            region=region,
            status=instance.get("State", {}).get("Name", "unknown"),
            created_at=created_at,
            metadata=metadata,
        )
