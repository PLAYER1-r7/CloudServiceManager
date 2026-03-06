"""GCP cloud provider implementation."""

import logging
from datetime import datetime
from typing import List, Optional

from google.api_core.exceptions import GoogleAPIError, NotFound, PermissionDenied
from google.cloud import compute_v1

from ..auth.gcp_auth import GCPAuth
from ..models.service import CloudProvider, CloudService

logger = logging.getLogger(__name__)


class GCPProvider:
    """Google Cloud Platform service provider for listing and managing Compute Engine instances.
    
    This provider integrates with GCPAuth for authentication and provides
    methods to list and retrieve Compute Engine instances, converting them to the
    unified CloudService model.
    
    Attributes:
        auth: GCPAuth instance for authentication
        project_id: GCP project ID
    """

    def __init__(self, auth: Optional[GCPAuth] = None, project_id: Optional[str] = None):
        """Initialize GCP provider with authentication.
        
        Args:
            auth: Optional GCPAuth instance. If not provided, creates a new instance.
            project_id: Optional GCP project ID. If not provided, uses auth's project_id.
            
        Raises:
            RuntimeError: If authentication fails
        """
        self.auth = auth or GCPAuth(project_id=project_id)
        self.project_id = project_id or self.auth._project_id
        
        if not self.auth.is_authenticated():
            raise RuntimeError(
                "GCP authentication failed. Please configure credentials via:\n"
                "  - Service account key file (GOOGLE_APPLICATION_CREDENTIALS)\n"
                "  - Application Default Credentials (gcloud auth login)\n"
                "  - Compute Engine default service account"
            )
        
        if not self.project_id:
            raise RuntimeError(
                "GCP project ID not found. Please set GOOGLE_CLOUD_PROJECT or "
                "use a service account with project_id in the credentials file."
            )
        
        # Initialize GCP clients
        self.instances_client = compute_v1.InstancesClient(credentials=self.auth._credentials)
        self.zones_client = compute_v1.ZonesClient(credentials=self.auth._credentials)

    def list_services(self, region: Optional[str] = None) -> List[CloudService]:
        """
        List GCP Compute Engine instances across one or all zones.
        
        In GCP terminology, 'zone' is equivalent to 'region' in other cloud providers.
        This method lists instances from a specific zone or all zones.
        
        Args:
            region: Optional GCP zone to filter by (e.g., "us-central1-a").
                   If None, fetches from all zones.
            
        Returns:
            List of CloudService objects representing Compute Engine instances
            
        Raises:
            GoogleAPIError: If GCP API call fails
            RuntimeError: If project ID is not configured
        """
        try:
            services = []
            
            # Get all zones if not specified
            if region:
                zones = [region]
            else:
                zones = self._get_all_zones()
                logger.info(f"Fetching Compute Engine instances from {len(zones)} zones")
            
            for zone in zones:
                logger.debug(f"Fetching Compute Engine instances from zone: {zone}")
                
                try:
                    request = compute_v1.ListInstancesRequest(
                        project=self.project_id,
                        zone=zone,
                    )
                    page_result = self.instances_client.list(request=request)
                    
                    for instance in page_result:
                        try:
                            service = self._convert_to_cloud_service(instance, zone)
                            services.append(service)
                        except Exception as e:
                            logger.warning(
                                f"Failed to convert instance {instance.name} "
                                f"in zone {zone}: {e}"
                            )
                            
                except PermissionDenied:
                    logger.warning(f"Unauthorized to access zone {zone}, skipping")
                except NotFound:
                    logger.warning(f"Zone {zone} not found, skipping")
                except GoogleAPIError as e:
                    logger.error(f"Error fetching instances from zone {zone}: {e}")
                        
            logger.info(f"Found {len(services)} Compute Engine instances")
            return services
            
        except GoogleAPIError as e:
            logger.error(f"GCP API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error listing GCP services: {e}")
            raise

    def get_service(self, service_id: str, region: Optional[str] = None) -> Optional[CloudService]:
        """
        Get a specific Compute Engine instance by name.
        
        Args:
            service_id: Compute Engine instance name
            region: Optional GCP zone. If not specified, searches all zones.
            
        Returns:
            CloudService object if found, None otherwise
            
        Raises:
            GoogleAPIError: If GCP API call fails
        """
        try:
            # If zone is specified, search only in that zone
            if region:
                zones = [region]
            else:
                zones = self._get_all_zones()
            
            for zone in zones:
                try:
                    request = compute_v1.GetInstanceRequest(
                        project=self.project_id,
                        zone=zone,
                        instance=service_id,
                    )
                    instance = self.instances_client.get(request=request)
                    logger.debug(f"Found instance {service_id} in zone {zone}")
                    return self._convert_to_cloud_service(instance, zone)
                        
                except NotFound:
                    # Instance not in this zone, continue searching
                    continue
                except GoogleAPIError as e:
                    logger.error(f"Error fetching instance {service_id} from zone {zone}: {e}")
                    raise
                    
            logger.debug(f"Instance {service_id} not found in any zone")
            return None
            
        except Exception as e:
            logger.error(f"Unexpected error getting GCP service: {e}")
            raise

    def _convert_to_cloud_service(self, instance: compute_v1.Instance, zone: str) -> CloudService:
        """
        Convert a GCP Compute Engine instance to CloudService model.
        
        Args:
            instance: GCP Instance object from compute_v1 API
            zone: GCP zone where the instance is located
            
        Returns:
            CloudService object with converted data
        """
        # Extract machine type name (full path: projects/PROJECT/zones/ZONE/machineTypes/MACHINE_TYPE)
        machine_type = None
        if instance.machine_type:
            machine_type = instance.machine_type.split("/")[-1]
        
        # Extract internal IP
        internal_ip = None
        if instance.network_interfaces and len(instance.network_interfaces) > 0:
            internal_ip = instance.network_interfaces[0].network_ip
        
        # Extract external IP
        external_ip = None
        if instance.network_interfaces and len(instance.network_interfaces) > 0:
            access_configs = instance.network_interfaces[0].access_configs
            if access_configs and len(access_configs) > 0:
                external_ip = access_configs[0].nat_ip
        
        # Ensure creation timestamp is in ISO 8601 format string
        created_at = instance.creation_timestamp
        if isinstance(created_at, datetime):
            # Convert datetime to ISO 8601 format string
            created_at = created_at.strftime("%Y-%m-%dT%H:%M:%SZ")
        elif created_at and not isinstance(created_at, str):
            # Convert other types to string
            created_at = str(created_at)
        elif not created_at:
            # Use current time as fallback
            created_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        return CloudService(
            provider=CloudProvider.GCP,
            service_type="Compute Engine",
            name=instance.name,
            region=zone,
            status=instance.status.name if instance.status else "unknown",
            created_at=created_at,
            metadata={
                "id": instance.id,
                "machine_type": machine_type,
                "internal_ip": internal_ip,
                "external_ip": external_ip,
                "can_ip_forward": instance.can_ip_forward,
                "cpu_platform": instance.cpu_platform,
                "tags": instance.tags.items if instance.tags else [],
                "labels": dict(instance.labels) if instance.labels else {},
                "zone": zone,
            },
        )

    def _get_all_zones(self) -> List[str]:
        """
        Get all available GCP zones in the project.
        
        Returns:
            List of zone names (e.g., ["us-central1-a", "us-central1-b", ...])
            
        Raises:
            GoogleAPIError: If GCP API call fails
        """
        try:
            zones = []
            request = compute_v1.ListZonesRequest(project=self.project_id)
            page_result = self.zones_client.list(request=request)
            
            for zone in page_result:
                zones.append(zone.name)
            
            logger.debug(f"Available zones: {zones}")
            return zones
        except GoogleAPIError as e:
            logger.error(f"Error getting GCP zones: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error listing zones: {e}")
            raise
