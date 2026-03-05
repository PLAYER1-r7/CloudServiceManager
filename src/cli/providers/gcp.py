"""GCP cloud provider implementation."""

from google.cloud import compute_v1
from typing import List, Optional
from ..models.service import CloudService, CloudProvider


class GCPProvider:
    """Google Cloud Platform service provider."""

    def __init__(self):
        """Initialize GCP provider."""
        self.instances_client = compute_v1.InstancesClient()
        self.projects_client = compute_v1.ProjectsClient()

    def list_services(self, region: Optional[str] = None) -> List[CloudService]:
        """
        List GCP Compute Engine instances.
        
        Args:
            region: Optional GCP zone filter
            
        Returns:
            List of CloudService objects
        """
        try:
            services = []
            project = self._get_project_id()
            
            if not project:
                return []
            
            # Get all zones if region not specified
            zones = self._get_zones(region) if region else self._get_all_zones()
            
            for zone in zones:
                request = compute_v1.ListInstancesRequest(
                    project=project,
                    zone=zone,
                )
                page_result = self.instances_client.list(request=request)
                
                for instance in page_result:
                    service = CloudService(
                        provider=CloudProvider.GCP,
                        service_type="Compute Engine",
                        name=instance.name,
                        region=zone,
                        status=instance.status.name if instance.status else "unknown",
                        created_at=instance.creation_timestamp,
                        metadata={
                            "machine_type": instance.machine_type.split("/")[-1] if instance.machine_type else None,
                            "internal_ip": instance.network_interfaces[0].network_ip if instance.network_interfaces else None,
                        },
                    )
                    services.append(service)
            
            return services
        except Exception as e:
            print(f"Error fetching GCP services: {e}")
            return []

    def get_service(self, service_id: str, region: Optional[str] = None) -> Optional[CloudService]:
        """
        Get a specific Compute Engine instance.
        
        Args:
            service_id: GCP instance name
            region: GCP zone
            
        Returns:
            CloudService object or None
        """
        try:
            project = self._get_project_id()
            if not project or not region:
                return None
            
            request = compute_v1.GetInstanceRequest(
                project=project,
                zone=region,
                resource=service_id,
            )
            
            instance = self.instances_client.get(request=request)
            
            return CloudService(
                provider=CloudProvider.GCP,
                service_type="Compute Engine",
                name=instance.name,
                region=region,
                status=instance.status.name if instance.status else "unknown",
                created_at=instance.creation_timestamp,
                metadata={
                    "machine_type": instance.machine_type.split("/")[-1] if instance.machine_type else None,
                    "internal_ip": instance.network_interfaces[0].network_ip if instance.network_interfaces else None,
                },
            )
        except Exception as e:
            print(f"Error fetching GCP service: {e}")
        
        return None

    def _get_project_id(self) -> Optional[str]:
        """Get GCP project ID."""
        try:
            # This assumes GOOGLE_APPLICATION_CREDENTIALS is set
            from google.auth import default
            _, project = default()
            return project
        except Exception as e:
            print(f"Error getting GCP project ID: {e}")
            return None

    def _get_all_zones(self) -> List[str]:
        """Get all GCP zones."""
        try:
            zones = []
            project = self._get_project_id()
            if not project:
                return zones
            
            zones_client = compute_v1.ZonesClient()
            request = compute_v1.ListZonesRequest(project=project)
            page_result = zones_client.list(request=request)
            
            return [zone.name for zone in page_result]
        except Exception as e:
            print(f"Error getting GCP zones: {e}")
            return []

    def _get_zones(self, pattern: str) -> List[str]:
        """Filter zones by pattern."""
        all_zones = self._get_all_zones()
        return [z for z in all_zones if pattern.lower() in z.lower()]
