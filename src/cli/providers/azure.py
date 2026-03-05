"""Azure cloud provider implementation."""

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from typing import List, Optional
from ..models.service import CloudService, CloudProvider


class AzureProvider:
    """Azure cloud provider."""

    def __init__(self):
        """Initialize Azure provider."""
        try:
            self.credential = DefaultAzureCredential()
            self.subscription_id = self._get_subscription_id()
            if self.subscription_id:
                self.compute_client = ComputeManagementClient(
                    self.credential,
                    self.subscription_id
                )
        except Exception as e:
            print(f"Error initializing Azure provider: {e}")

    def list_services(self, region: Optional[str] = None) -> List[CloudService]:
        """
        List Azure Virtual Machines.
        
        Args:
            region: Optional Azure region filter
            
        Returns:
            List of CloudService objects
        """
        try:
            if not hasattr(self, 'compute_client') or not self.compute_client:
                return []
            
            services = []
            
            # Get all resource groups
            resource_management_client = self._get_resource_management_client()
            if not resource_management_client:
                return []
            
            resource_groups = resource_management_client.resource_groups.list()
            
            for rg in resource_groups:
                # Get VMs in each resource group
                vms = self.compute_client.virtual_machines.list(rg.name)
                
                for vm in vms:
                    # Skip if region filter is specified and doesn't match
                    if region and region.lower() not in vm.location.lower():
                        continue
                    
                    service = CloudService(
                        provider=CloudProvider.AZURE,
                        service_type="Virtual Machine",
                        name=vm.name,
                        region=vm.location,
                        status="Unknown",  # Would need instance view for actual state
                        created_at=None,
                        metadata={
                            "vm_size": vm.hardware_profile.vm_size if vm.hardware_profile else None,
                            "resource_group": rg.name,
                        },
                    )
                    services.append(service)
            
            return services
        except Exception as e:
            print(f"Error fetching Azure services: {e}")
            return []

    def get_service(self, service_id: str, resource_group: Optional[str] = None) -> Optional[CloudService]:
        """
        Get a specific Azure Virtual Machine.
        
        Args:
            service_id: Azure VM name
            resource_group: Resource group name
            
        Returns:
            CloudService object or None
        """
        try:
            if not hasattr(self, 'compute_client') or not self.compute_client or not resource_group:
                return None
            
            vm = self.compute_client.virtual_machines.get(resource_group, service_id)
            
            return CloudService(
                provider=CloudProvider.AZURE,
                service_type="Virtual Machine",
                name=vm.name,
                region=vm.location,
                status="Unknown",
                created_at=None,
                metadata={
                    "vm_size": vm.hardware_profile.vm_size if vm.hardware_profile else None,
                    "resource_group": resource_group,
                },
            )
        except Exception as e:
            print(f"Error fetching Azure service: {e}")
        
        return None

    def _get_subscription_id(self) -> Optional[str]:
        """Get Azure subscription ID."""
        import os
        return os.getenv("AZURE_SUBSCRIPTION_ID")

    def _get_resource_management_client(self):
        """Get Azure Resource Management Client."""
        try:
            from azure.mgmt.resource import ResourceManagementClient
            return ResourceManagementClient(self.credential, self.subscription_id)
        except Exception as e:
            print(f"Error getting Resource Management Client: {e}")
            return None
