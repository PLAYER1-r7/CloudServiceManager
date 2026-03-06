"""
Tests for Azure provider implementation.

Comprehensive tests for AzureProvider class including:
- Authentication integration
- Virtual Machine listing
- Virtual Machine retrieval
- Region and resource group handling
- Error handling
"""

# pyright: reportUnknownParameterType=false, reportUnknownArgumentType=false, reportUnknownVariableType=false, reportUnknownMemberType=false, reportMissingParameterType=false

from unittest.mock import Mock, patch

import pytest
from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceNotFoundError,
)

from src.cli.auth.azure_auth import AzureAuth
from src.cli.models.service import CloudProvider
from src.cli.providers.azure import AzureProvider


class TestAzureProvider:
    """Test suite for Azure provider."""
    
    @pytest.fixture
    def mock_auth(self):
        """Fixture providing a mocked AzureAuth."""
        mock = Mock(spec=AzureAuth)
        mock.is_authenticated.return_value = True
        mock.subscription_id = "test-subscription-123"
        mock._credential = Mock()
        
        return mock
    
    @pytest.fixture
    def mock_vm(self):
        """Fixture providing a mocked Azure Virtual Machine."""
        vm = Mock()
        vm.id = "/subscriptions/test-subscription-123/resourceGroups/test-rg/providers/Microsoft.Compute/virtualMachines/test-vm-1"
        vm.name = "test-vm-1"
        vm.location = "eastus"
        vm.provisioning_state = "Succeeded"
        vm.tags = {"env": "test", "team": "engineering"}
        
        # Don't set time_created - let hasattr return False
        vm.configure_mock(**{'time_created': None})
        
        # Hardware profile
        hw_profile = Mock()
        hw_profile.vm_size = "Standard_B2s"
        vm.hardware_profile = hw_profile
        
        # Storage profile
        storage_profile = Mock()
        os_disk = Mock()
        os_disk.os_type = Mock()
        os_disk.os_type.name = "Linux"
        storage_profile.os_disk = os_disk
        
        image_ref = Mock()
        image_ref.publisher = "Canonical"
        image_ref.offer = "UbuntuServer"
        image_ref.sku = "18.04-LTS"
        image_ref.version = "18.04.202401010"
        storage_profile.image_reference = image_ref
        storage_profile.data_disks = []
        vm.storage_profile = storage_profile
        
        # Network profile
        network_profile = Mock()
        nic = Mock()
        nic.id = "/subscriptions/test-subscription-123/resourceGroups/test-rg/providers/Microsoft.Network/networkInterfaces/test-nic"
        network_profile.network_interfaces = [nic]
        vm.network_profile = network_profile
        
        return vm
    
    @pytest.fixture
    def mock_instance_view(self):
        """Fixture providing a mocked Azure InstanceView."""
        instance_view = Mock()
        
        # Power state status
        status1 = Mock()
        status1.code = "ProvisioningState/succeeded"
        status2 = Mock()
        status2.code = "PowerState/running"
        instance_view.statuses = [status1, status2]
        
        return instance_view
    
    @pytest.fixture
    def mock_resource_group(self):
        """Fixture providing a mocked Azure ResourceGroup."""
        rg = Mock()
        rg.id = "/subscriptions/test-subscription-123/resourceGroups/test-rg"
        rg.name = "test-rg"
        rg.location = "eastus"
        
        return rg
    
    @pytest.fixture
    def azure_provider(self, mock_auth):
        """Fixture providing AzureProvider with mocked auth."""
        with patch('src.cli.providers.azure.ComputeManagementClient'):
            with patch('src.cli.providers.azure.ResourceManagementClient'):
                return AzureProvider(auth=mock_auth)
    
    def test_initialization_with_auth(self, mock_auth):
        """Test AzureProvider initialization with provided auth."""
        with patch('src.cli.providers.azure.ComputeManagementClient'):
            with patch('src.cli.providers.azure.ResourceManagementClient'):
                provider = AzureProvider(auth=mock_auth)
                assert provider.auth == mock_auth
                assert provider.subscription_id == "test-subscription-123"
    
    def test_initialization_without_auth(self):
        """Test AzureProvider initialization without auth (creates new AzureAuth)."""
        with patch('src.cli.providers.azure.AzureAuth') as mock_auth_class:
            mock_auth_instance = Mock()
            mock_auth_instance.is_authenticated.return_value = True
            mock_auth_instance.subscription_id = "test-subscription-456"
            mock_auth_instance._credential = Mock()
            mock_auth_class.return_value = mock_auth_instance
            
            with patch('src.cli.providers.azure.ComputeManagementClient'):
                with patch('src.cli.providers.azure.ResourceManagementClient'):
                    provider = AzureProvider(subscription_id="test-subscription-456")
                    
                    mock_auth_class.assert_called_once_with(subscription_id="test-subscription-456")
                    assert provider.subscription_id == "test-subscription-456"
    
    def test_initialization_fails_without_credentials(self):
        """Test that initialization fails when not authenticated."""
        with patch('src.cli.providers.azure.AzureAuth') as mock_auth_class:
            mock_auth_instance = Mock()
            mock_auth_instance.is_authenticated.return_value = False
            mock_auth_class.return_value = mock_auth_instance
            
            with pytest.raises(RuntimeError, match="Azure authentication failed"):
                AzureProvider()
    
    def test_initialization_fails_without_subscription_id(self):
        """Test that initialization fails when subscription_id is not found."""
        with patch('src.cli.providers.azure.AzureAuth') as mock_auth_class:
            mock_auth_instance = Mock()
            mock_auth_instance.is_authenticated.return_value = True
            mock_auth_instance.subscription_id = None
            mock_auth_instance._credential = Mock()
            mock_auth_class.return_value = mock_auth_instance
            
            with pytest.raises(RuntimeError, match="Azure subscription ID not found"):
                AzureProvider()
    
    def test_list_services_single_region(
        self, azure_provider, mock_auth, mock_resource_group, mock_vm, mock_instance_view
    ):
        """Test listing VMs from a single region."""
        # Mock resource groups
        azure_provider.resource_client = Mock()
        azure_provider.resource_client.resource_groups.list.return_value = [mock_resource_group]
        
        # Mock VMs
        azure_provider.compute_client = Mock()
        azure_provider.compute_client.virtual_machines.list.return_value = [mock_vm]
        azure_provider.compute_client.virtual_machines.instance_view.return_value = mock_instance_view
        
        # Call list_services with specific region
        services = azure_provider.list_services(region="eastus")
        
        assert len(services) == 1
        assert services[0].name == "test-vm-1"
        assert services[0].provider == CloudProvider.AZURE
        assert services[0].service_type == "Virtual Machine"
        assert services[0].region == "eastus"
        assert services[0].status == "running"
        assert isinstance(services[0].created_at, str)
    
    def test_list_services_all_regions(
        self, azure_provider, mock_auth, mock_resource_group, mock_vm, mock_instance_view
    ):
        """Test listing VMs from all regions."""
        # Mock resource groups
        azure_provider.resource_client = Mock()
        azure_provider.resource_client.resource_groups.list.return_value = [mock_resource_group]
        
        # Mock VMs
        azure_provider.compute_client = Mock()
        azure_provider.compute_client.virtual_machines.list.return_value = [mock_vm]
        azure_provider.compute_client.virtual_machines.instance_view.return_value = mock_instance_view
        
        # Call list_services without region filter
        services = azure_provider.list_services()
        
        assert len(services) == 1
        assert services[0].name == "test-vm-1"
    
    def test_list_services_multiple_resource_groups(
        self, azure_provider, mock_auth, mock_vm, mock_instance_view
    ):
        """Test listing VMs from multiple resource groups."""
        # Create second resource group and VM
        rg2 = Mock()
        rg2.id = "/subscriptions/test-subscription-123/resourceGroups/test-rg2"
        rg2.name = "test-rg2"
        rg2.location = "westus"
        
        vm2 = Mock()
        vm2.id = "/subscriptions/test-subscription-123/resourceGroups/test-rg2/providers/Microsoft.Compute/virtualMachines/test-vm-2"
        vm2.name = "test-vm-2"
        vm2.location = "westus"
        vm2.provisioning_state = "Succeeded"
        vm2.tags = {}
        
        hw_profile2 = Mock()
        hw_profile2.vm_size = "Standard_B1s"
        vm2.hardware_profile = hw_profile2
        
        vm2.storage_profile = Mock()
        vm2.storage_profile.os_disk = Mock()
        vm2.storage_profile.os_disk.os_type = None
        vm2.storage_profile.image_reference = None
        vm2.network_profile = Mock()
        vm2.network_profile.network_interfaces = []
        
        # Mock resource groups
        rg1 = Mock()
        rg1.name = "test-rg"
        rg1.location = "eastus"
        azure_provider.resource_client = Mock()
        azure_provider.resource_client.resource_groups.list.return_value = [rg1, rg2]
        
        # Mock VMs
        azure_provider.compute_client = Mock()
        azure_provider.compute_client.virtual_machines.list.side_effect = [[mock_vm], [vm2]]
        azure_provider.compute_client.virtual_machines.instance_view.return_value = mock_instance_view
        
        # Call list_services
        services = azure_provider.list_services()
        
        assert len(services) == 2
        assert services[0].name == "test-vm-1"
        assert services[0].region == "eastus"
        assert services[1].name == "test-vm-2"
        assert services[1].region == "westus"
    
    def test_list_services_empty_resource_groups(self, azure_provider):
        """Test listing VMs when no resource groups exist."""
        # Mock empty resource groups
        azure_provider.resource_client = Mock()
        azure_provider.resource_client.resource_groups.list.return_value = []
        
        # Call list_services
        services = azure_provider.list_services()
        
        assert len(services) == 0
    
    def test_list_services_auth_error(self, azure_provider):
        """Test handling authentication error when listing resource groups."""
        # Mock authentication error
        azure_provider.resource_client = Mock()
        azure_provider.resource_client.resource_groups.list.side_effect = ClientAuthenticationError("Auth failed")
        
        # Call list_services
        with pytest.raises(RuntimeError, match="Azure authentication failed"):
            azure_provider.list_services()
    
    def test_list_services_http_error(self, azure_provider):
        """Test handling HTTP error when listing resource groups."""
        # Mock HTTP error
        azure_provider.resource_client = Mock()
        azure_provider.resource_client.resource_groups.list.side_effect = HttpResponseError("HTTP Error")
        
        # Call list_services
        with pytest.raises(HttpResponseError):
            azure_provider.list_services()
    
    def test_get_service_in_specific_resource_group(
        self, azure_provider, mock_vm, mock_instance_view
    ):
        """Test retrieving a specific VM in a specific resource group."""
        # Mock resource group
        rg = Mock()
        rg.location = "eastus"
        azure_provider.resource_client = Mock()
        azure_provider.resource_client.resource_groups.get.return_value = rg
        
        # Mock compute client
        azure_provider.compute_client = Mock()
        azure_provider.compute_client.virtual_machines.get.return_value = mock_vm
        azure_provider.compute_client.virtual_machines.instance_view.return_value = mock_instance_view
        
        # Call get_service with resource group
        service = azure_provider.get_service("test-vm-1", resource_group="test-rg")
        
        assert service is not None
        assert service.name == "test-vm-1"
        assert service.region == "eastus"
    
    def test_get_service_in_all_resource_groups(
        self, azure_provider, mock_vm, mock_instance_view
    ):
        """Test retrieving a specific VM by searching all resource groups."""
        # Create mocked resource groups
        rg1 = Mock()
        rg1.name = "test-rg"
        rg1.location = "eastus"
        rg2 = Mock()
        rg2.name = "test-rg2"
        rg2.location = "eastus"
        
        # Mock resource groups list
        azure_provider.resource_client = Mock()
        azure_provider.resource_client.resource_groups.list.return_value = [rg1, rg2]
        azure_provider.resource_client.resource_groups.get.return_value = rg1
        
        # Mock compute client to raise NotFound for first RG, return for second
        azure_provider.compute_client = Mock()
        azure_provider.compute_client.virtual_machines.get.side_effect = [
            ResourceNotFoundError("Not found"),
            mock_vm
        ]
        azure_provider.compute_client.virtual_machines.instance_view.return_value = mock_instance_view
        
        # Call get_service without resource group
        service = azure_provider.get_service("test-vm-1")
        
        assert service is not None
        assert service.name == "test-vm-1"
    
    def test_get_service_not_found(self, azure_provider):
        """Test retrieving a non-existent VM."""
        # Mock resource groups
        rg = Mock()
        rg.name = "test-rg"
        rg.location = "eastus"
        azure_provider.resource_client = Mock()
        azure_provider.resource_client.resource_groups.list.return_value = [rg]
        
        # Mock compute client to raise NotFound
        azure_provider.compute_client = Mock()
        azure_provider.compute_client.virtual_machines.get.side_effect = ResourceNotFoundError("Not found")
        
        # Call get_service
        service = azure_provider.get_service("nonexistent")
        
        assert service is None
    
    def test_convert_to_cloud_service(
        self, azure_provider, mock_vm, mock_instance_view
    ):
        """Test conversion from Azure VM to CloudService model."""
        service = azure_provider._convert_to_cloud_service(
            mock_vm, mock_instance_view, "test-rg", "eastus"
        )
        
        assert service.provider == CloudProvider.AZURE
        assert service.service_type == "Virtual Machine"
        assert service.name == "test-vm-1"
        assert service.region == "eastus"
        assert service.status == "running"
        
        # Check metadata
        assert service.metadata["vm_size"] == "Standard_B2s"
        assert service.metadata["resource_group"] == "test-rg"
        assert service.metadata["os_type"] == "Linux"
        assert service.metadata["image"]["publisher"] == "Canonical"
        assert service.metadata["tags"]["env"] == "test"
    
    def test_convert_to_cloud_service_without_hardware_profile(self, azure_provider, mock_instance_view):
        """Test conversion when hardware profile is not available."""
        vm = Mock()
        vm.id = "/subscriptions/test-subscription-123/resourceGroups/test-rg/providers/Microsoft.Compute/virtualMachines/test-vm"
        vm.name = "test-vm"
        vm.location = "eastus"
        vm.provisioning_state = "Succeeded"
        vm.tags = None
        vm.hardware_profile = None
        vm.storage_profile = Mock()
        vm.storage_profile.os_disk = None
        vm.storage_profile.image_reference = None
        vm.network_profile = Mock()
        vm.network_profile.network_interfaces = None
        
        service = azure_provider._convert_to_cloud_service(
            vm, mock_instance_view, "test-rg", "eastus"
        )
        
        assert service.metadata["vm_size"] is None
        assert service.metadata["os_type"] is None
    
    def test_convert_to_cloud_service_with_unknown_power_state(self, azure_provider, mock_vm):
        """Test conversion when power state is not available."""
        instance_view = Mock()
        instance_view.statuses = None
        
        service = azure_provider._convert_to_cloud_service(
            mock_vm, instance_view, "test-rg", "eastus"
        )
        
        assert service.status == "Unknown"
