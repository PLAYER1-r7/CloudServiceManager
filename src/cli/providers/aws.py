"""AWS cloud provider implementation."""

import boto3
from typing import List, Optional
from ..models.service import CloudService, CloudProvider


class AWSProvider:
    """AWS service provider."""

    def __init__(self):
        """Initialize AWS provider."""
        self.ec2_client = boto3.client("ec2")

    def list_services(self, region: Optional[str] = None) -> List[CloudService]:
        """
        List AWS EC2 instances.
        
        Args:
            region: Optional AWS region
            
        Returns:
            List of CloudService objects
        """
        try:
            services = []
            
            # Get all regions if not specified
            regions = [region] if region else self._get_all_regions()
            
            for reg in regions:
                ec2 = boto3.client("ec2", region_name=reg)
                response = ec2.describe_instances()
                
                for reservation in response.get("Reservations", []):
                    for instance in reservation.get("Instances", []):
                        service = CloudService(
                            provider=CloudProvider.AWS,
                            service_type="EC2",
                            name=instance.get("InstanceId"),
                            region=reg,
                            status=instance.get("State", {}).get("Name", "unknown"),
                            created_at=instance.get("LaunchTime", "").isoformat() if instance.get("LaunchTime") else None,
                            metadata={
                                "instance_type": instance.get("InstanceType"),
                                "image_id": instance.get("ImageId"),
                            },
                        )
                        services.append(service)
            
            return services
        except Exception as e:
            print(f"Error fetching AWS services: {e}")
            return []

    def get_service(self, service_id: str, region: Optional[str] = None) -> Optional[CloudService]:
        """
        Get a specific EC2 instance.
        
        Args:
            service_id: EC2 instance ID
            region: AWS region (optional)
            
        Returns:
            CloudService object or None
        """
        try:
            if region:
                ec2 = boto3.client("ec2", region_name=region)
            else:
                ec2 = self.ec2_client
            
            response = ec2.describe_instances(InstanceIds=[service_id])
            
            if response.get("Reservations"):
                instance = response["Reservations"][0]["Instances"][0]
                return CloudService(
                    provider=CloudProvider.AWS,
                    service_type="EC2",
                    name=instance.get("InstanceId"),
                    region=instance.get("Placement", {}).get("AvailabilityZone", "unknown"),
                    status=instance.get("State", {}).get("Name", "unknown"),
                    created_at=instance.get("LaunchTime", "").isoformat() if instance.get("LaunchTime") else None,
                    metadata={
                        "instance_type": instance.get("InstanceType"),
                        "image_id": instance.get("ImageId"),
                    },
                )
        except Exception as e:
            print(f"Error fetching AWS service: {e}")
        
        return None

    def _get_all_regions(self) -> List[str]:
        """Get all AWS regions."""
        try:
            response = self.ec2_client.describe_regions()
            return [r["RegionName"] for r in response.get("Regions", [])]
        except Exception as e:
            print(f"Error getting AWS regions: {e}")
            return ["us-east-1"]  # Fallback to default region
