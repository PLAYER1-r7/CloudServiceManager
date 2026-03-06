"""Azure cloud provider implementation."""

import logging
from datetime import datetime
from typing import List, Optional

from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceNotFoundError,
)
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient

from ..auth.azure_auth import AzureAuth
from ..models.service import CloudProvider, CloudService

logger = logging.getLogger(__name__)


class AzureProvider:
    """Azure cloud provider for listing and managing Virtual Machines.

    This provider integrates with AzureAuth for authentication and provides
    methods to list and retrieve Virtual Machines, converting them to the
    unified CloudService model.

    Attributes:
        auth: AzureAuth instance for authentication
        subscription_id: Azure subscription ID
        compute_client: Azure Compute Management client
        resource_client: Azure Resource Management client
    """

    def __init__(
        self, auth: Optional[AzureAuth] = None, subscription_id: Optional[str] = None
    ):
        """Initialize Azure provider with authentication.

        Args:
            auth: Optional AzureAuth instance. If not provided, creates a new instance.
            subscription_id: Optional Azure subscription ID.

        Raises:
            RuntimeError: If authentication fails
        """
        self.auth = auth or AzureAuth(subscription_id=subscription_id)
        self.subscription_id = subscription_id or self.auth.subscription_id

        if not self.auth.is_authenticated():
            raise RuntimeError(
                "Azure authentication failed. Please configure credentials via:\n"
                "  - Environment variables (AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET)\n"
                "  - Azure CLI (az login)\n"
                "  - Managed Identity (for Azure VMs)\n"
                "  - Visual Studio Code credentials"
            )

        if not self.subscription_id:
            raise RuntimeError(
                "Azure subscription ID not found. Please set AZURE_SUBSCRIPTION_ID "
                "environment variable."
            )

        # Initialize Azure management clients
        self.compute_client = ComputeManagementClient(
            credential=self.auth._credential, subscription_id=self.subscription_id
        )
        self.resource_client = ResourceManagementClient(
            credential=self.auth._credential, subscription_id=self.subscription_id
        )

    def list_services(self, region: Optional[str] = None) -> List[CloudService]:
        """
        List Azure Virtual Machines across one or all regions.

        Args:
            region: Optional Azure region to filter by (e.g., "eastus", "westus").
                   If None, fetches from all regions.

        Returns:
            List of CloudService objects representing Virtual Machines

        Raises:
            HttpResponseError: If Azure API call fails
            RuntimeError: If subscription ID is not configured
        """
        try:
            services = []

            # Get all resource groups
            logger.info("Fetching resource groups...")
            try:
                resource_groups_list = list(self.resource_client.resource_groups.list())
            except ClientAuthenticationError:
                logger.error("Azure authentication failed")
                raise RuntimeError("Azure authentication failed")
            except HttpResponseError as e:
                logger.error(f"Failed to list resource groups: {e}")
                raise

            if not resource_groups_list:
                logger.info("No resource groups found")
                return services

            logger.info(f"Processing {len(resource_groups_list)} resource groups")

            for rg in resource_groups_list:
                # Filter by region if specified
                if region and region.lower() != rg.location.lower():
                    continue

                logger.debug(f"Fetching VMs from resource group: {rg.name}")

                try:
                    vms_list = list(self.compute_client.virtual_machines.list(rg.name))

                    for vm in vms_list:
                        try:
                            # Get instance view to get power state
                            instance_view = (
                                self.compute_client.virtual_machines.instance_view(
                                    rg.name, vm.name
                                )
                            )
                            service = self._convert_to_cloud_service(
                                vm, instance_view, rg.name, rg.location
                            )
                            services.append(service)
                        except Exception as e:
                            logger.warning(
                                f"Failed to convert VM {vm.name} "
                                f"in resource group {rg.name}: {e}"
                            )

                except HttpResponseError as e:
                    logger.error(
                        f"Error fetching VMs from resource group {rg.name}: {e}"
                    )
                except Exception as e:
                    logger.error(f"Unexpected error in resource group {rg.name}: {e}")

            logger.info(f"Found {len(services)} Virtual Machines")
            return services

        except Exception as e:
            logger.error(f"Unexpected error listing Azure services: {e}")
            raise

    def get_service(
        self,
        service_id: str,
        resource_group: Optional[str] = None,
        region: Optional[str] = None,
    ) -> Optional[CloudService]:
        """
        Get a specific Virtual Machine by name.

        Args:
            service_id: Virtual Machine name
            resource_group: Optional Azure resource group name.
                           If not specified, searches all resource groups.
            region: Optional Azure region. Used to filter resource groups if specified.

        Returns:
            CloudService object if found, None otherwise

        Raises:
            HttpResponseError: If Azure API call fails
        """
        try:
            # If resource group is specified, search only in that group
            if resource_group:
                resource_groups = [resource_group]
            else:
                # Get all resource groups, optionally filtered by region
                try:
                    all_rgs = list(self.resource_client.resource_groups.list())
                    resource_groups = [
                        rg.name
                        for rg in all_rgs
                        if not region or region.lower() == rg.location.lower()
                    ]
                except HttpResponseError as e:
                    logger.error(f"Error listing resource groups: {e}")
                    raise

            for rg_name in resource_groups:
                try:
                    vm = self.compute_client.virtual_machines.get(rg_name, service_id)
                    instance_view = self.compute_client.virtual_machines.instance_view(
                        rg_name, service_id
                    )

                    # Get resource group details for location
                    rg = self.resource_client.resource_groups.get(rg_name)

                    logger.debug(f"Found VM {service_id} in resource group {rg_name}")
                    return self._convert_to_cloud_service(
                        vm, instance_view, rg_name, rg.location
                    )

                except ResourceNotFoundError:
                    # VM not in this resource group, continue searching
                    continue
                except HttpResponseError as e:
                    logger.error(
                        f"Error fetching VM {service_id} from resource group {rg_name}: {e}"
                    )
                    raise

            logger.debug(f"VM {service_id} not found in any resource group")
            return None

        except Exception as e:
            logger.error(f"Unexpected error getting Azure service: {e}")
            raise

    def _convert_to_cloud_service(
        self, vm, instance_view, resource_group: str, location: str
    ) -> CloudService:
        """
        Convert an Azure Virtual Machine to CloudService model.

        Args:
            vm: Azure Virtual Machine object
            instance_view: Azure InstanceView object with power state
            resource_group: Azure resource group name
            location: Azure region/location

        Returns:
            CloudService object with converted data
        """
        # Extract power state from instance view
        status = "Unknown"
        if instance_view.statuses:
            for status_item in instance_view.statuses:
                if "PowerState/" in status_item.code:
                    status = status_item.code.split("/")[-1]
                    break

        # Extract VM creation time (use provisioning time as fallback)
        created_at = None
        try:
            if hasattr(vm, "time_created") and vm.time_created:
                time_created = vm.time_created
                # Only use if it's a valid datetime object (skip Mock objects)
                if isinstance(time_created, datetime):
                    created_at = time_created
        except Exception:
            pass

        if not created_at:
            # Use current time as fallback
            created_at = datetime.utcnow()

        # Ensure created_at is in ISO 8601 format string
        if isinstance(created_at, datetime):
            created_at_str = created_at.strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            created_at_str = str(created_at)

        # Extract VM size
        vm_size = None
        if vm.hardware_profile:
            vm_size = vm.hardware_profile.vm_size

        # Extract image reference
        image_info = None
        if vm.storage_profile and vm.storage_profile.image_reference:
            img_ref = vm.storage_profile.image_reference
            image_info = {
                "publisher": img_ref.publisher,
                "offer": img_ref.offer,
                "sku": img_ref.sku,
                "version": img_ref.version,
            }

        # Extract OS type
        os_type = None
        if vm.storage_profile and vm.storage_profile.os_disk:
            if vm.storage_profile.os_disk.os_type:
                os_type = vm.storage_profile.os_disk.os_type.name

        # Extract tags
        tags = dict(vm.tags) if vm.tags else {}

        # Extract network interfaces
        nic_ids = []
        if vm.network_profile and vm.network_profile.network_interfaces:
            nic_ids = [nic.id for nic in vm.network_profile.network_interfaces]

        return CloudService(
            provider=CloudProvider.AZURE.value,
            service_type="Virtual Machine",
            name=vm.name,
            region=location,
            status=status,
            created_at=created_at_str,
            metadata={
                "id": vm.id,
                "vm_size": vm_size,
                "resource_group": resource_group,
                "location": location,
                "image": image_info,
                "os_type": os_type,
                "tags": tags,
                "nic_ids": nic_ids,
                "provisioning_state": vm.provisioning_state,
            },
        )
