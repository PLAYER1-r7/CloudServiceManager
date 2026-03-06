"""
Tests for GCP provider implementation.

Comprehensive tests for GCPProvider class including:
- Authentication integration
- Instance listing
- Instance retrieval
- Zone handling
- Error handling
"""

# pyright: reportUnknownParameterType=false, reportUnknownArgumentType=false, reportUnknownVariableType=false, reportUnknownMemberType=false, reportMissingParameterType=false

from unittest.mock import Mock, patch

import pytest
from google.api_core.exceptions import GoogleAPIError, NotFound, PermissionDenied
from google.cloud import compute_v1

from src.cli.auth.gcp_auth import GCPAuth
from src.cli.models.service import CloudProvider
from src.cli.providers.gcp import GCPProvider


class TestGCPProvider:
    """Test suite for GCP provider."""
    
    @pytest.fixture
    def mock_auth(self):
        """Fixture providing a mocked GCPAuth."""
        mock = Mock(spec=GCPAuth)
        mock.is_authenticated.return_value = True
        mock._project_id = "test-project-123"
        mock._credentials = Mock()
        
        return mock
    
    @pytest.fixture
    def mock_instance(self):
        """Fixture providing a mocked GCP Instance."""
        instance = Mock(spec=compute_v1.Instance)
        instance.id = "1234567890"
        instance.name = "test-instance-1"
        instance.machine_type = "projects/test-project/zones/us-central1-a/machineTypes/n1-standard-1"
        instance.status = compute_v1.Instance.Status.RUNNING
        instance.creation_timestamp = "2024-01-15T10:30:00Z"
        instance.can_ip_forward = False
        instance.cpu_platform = "Intel Broadwell"
        
        # Network interfaces
        interface = Mock()
        interface.network_ip = "10.128.0.2"
        access_config = Mock()
        access_config.nat_ip = "34.123.45.67"
        interface.access_configs = [access_config]
        instance.network_interfaces = [interface]
        
        # Tags
        instance.tags = Mock()
        instance.tags.items = ["http", "https"]
        
        # Labels
        instance.labels = {"env": "test", "team": "engineering"}
        
        return instance
    
    @pytest.fixture
    def gcp_provider(self, mock_auth: GCPAuth):
        """Fixture providing GCPProvider with mocked auth."""
        with patch('src.cli.providers.gcp.compute_v1.InstancesClient'):
            with patch('src.cli.providers.gcp.compute_v1.ZonesClient'):
                return GCPProvider(auth=mock_auth)
    
    def test_initialization_with_auth(self, mock_auth):
        """Test GCPProvider initialization with provided auth."""
        with patch('src.cli.providers.gcp.compute_v1.InstancesClient'):
            with patch('src.cli.providers.gcp.compute_v1.ZonesClient'):
                provider = GCPProvider(auth=mock_auth)
                assert provider.auth == mock_auth
                assert provider.project_id == "test-project-123"
    
    def test_initialization_without_auth(self):
        """Test GCPProvider initialization without auth (creates new GCPAuth)."""
        with patch('src.cli.providers.gcp.GCPAuth') as mock_auth_class:
            mock_auth_instance = Mock()
            mock_auth_instance.is_authenticated.return_value = True
            mock_auth_instance._project_id = "test-project-456"
            mock_auth_instance._credentials = Mock()
            mock_auth_class.return_value = mock_auth_instance
            
            with patch('src.cli.providers.gcp.compute_v1.InstancesClient'):
                with patch('src.cli.providers.gcp.compute_v1.ZonesClient'):
                    provider = GCPProvider(project_id="test-project-456")
                    
                    mock_auth_class.assert_called_once_with(project_id="test-project-456")
                    assert provider.project_id == "test-project-456"
    
    def test_initialization_fails_without_credentials(self):
        """Test that initialization fails when not authenticated."""
        with patch('src.cli.providers.gcp.GCPAuth') as mock_auth_class:
            mock_auth_instance = Mock()
            mock_auth_instance.is_authenticated.return_value = False
            mock_auth_class.return_value = mock_auth_instance
            
            with pytest.raises(RuntimeError, match="GCP authentication failed"):
                GCPProvider()
    
    def test_initialization_fails_without_project_id(self):
        """Test that initialization fails when project_id is not found."""
        with patch('src.cli.providers.gcp.GCPAuth') as mock_auth_class:
            mock_auth_instance = Mock()
            mock_auth_instance.is_authenticated.return_value = True
            mock_auth_instance._project_id = None
            mock_auth_class.return_value = mock_auth_instance
            
            with pytest.raises(RuntimeError, match="GCP project ID not found"):
                GCPProvider()
    
    def test_list_services_single_zone(self, gcp_provider, mock_auth, mock_instance):
        """Test listing services from a single zone."""
        # Mock zones
        gcp_provider.zones_client = Mock()
        
        # Mock instances
        gcp_provider.instances_client = Mock()
        gcp_provider.instances_client.list.return_value = [mock_instance]
        
        # Call list_services with specific zone
        services = gcp_provider.list_services(region="us-central1-a")
        
        assert len(services) == 1
        assert services[0].name == "test-instance-1"
        assert services[0].provider == CloudProvider.GCP
        assert services[0].service_type == "Compute Engine"
        assert services[0].region == "us-central1-a"
        assert services[0].status == "RUNNING"
        assert isinstance(services[0].created_at, str)
    
    def test_list_services_all_zones(self, gcp_provider, mock_auth, mock_instance):
        """Test listing services from all zones."""
        # Mock zones
        zone_mock = Mock()
        zone_mock.name = "us-central1-a"
        gcp_provider.zones_client = Mock()
        gcp_provider.zones_client.list.return_value = [zone_mock]
        
        # Mock instances
        gcp_provider.instances_client = Mock()
        gcp_provider.instances_client.list.return_value = [mock_instance]
        
        # Call list_services without zone filter
        services = gcp_provider.list_services()
        
        assert len(services) == 1
        assert services[0].name == "test-instance-1"
    
    def test_list_services_multiple_zones(self, gcp_provider, mock_auth, mock_instance):
        """Test listing services from multiple zones."""
        # Mock zones
        zone1 = Mock()
        zone1.name = "us-central1-a"
        zone2 = Mock()
        zone2.name = "us-central1-b"
        gcp_provider.zones_client = Mock()
        gcp_provider.zones_client.list.return_value = [zone1, zone2]
        
        # Create second instance
        instance2 = Mock(spec=compute_v1.Instance)
        instance2.id = "9876543210"
        instance2.name = "test-instance-2"
        instance2.machine_type = "projects/test-project/zones/us-central1-b/machineTypes/n1-standard-2"
        instance2.status = compute_v1.Instance.Status.RUNNING
        instance2.creation_timestamp = "2024-01-16T11:45:00Z"
        instance2.can_ip_forward = True
        instance2.cpu_platform = "Intel Broadwell"
        
        interface2 = Mock()
        interface2.network_ip = "10.128.0.3"
        access_config2 = Mock()
        access_config2.nat_ip = "34.123.45.68"
        interface2.access_configs = [access_config2]
        instance2.network_interfaces = [interface2]
        instance2.tags = Mock()
        instance2.tags.items = ["http"]
        instance2.labels = {}
        
        # Mock instances client to return different instances for different zones
        gcp_provider.instances_client = Mock()
        gcp_provider.instances_client.list.side_effect = [[mock_instance], [instance2]]
        
        # Call list_services without zone filter
        services = gcp_provider.list_services()
        
        assert len(services) == 2
        assert services[0].name == "test-instance-1"
        assert services[0].region == "us-central1-a"
        assert services[1].name == "test-instance-2"
        assert services[1].region == "us-central1-b"
    
    def test_list_services_empty_zones(self, gcp_provider):
        """Test listing services when no zones are available."""
        # Mock zones (empty)
        gcp_provider.zones_client = Mock()
        gcp_provider.zones_client.list.return_value = []
        
        # Call list_services without zone filter
        services = gcp_provider.list_services()
        
        assert len(services) == 0
    
    def test_list_services_permission_denied_single_zone(self, gcp_provider, mock_instance):
        """Test handling PermissionDenied error for a zone."""
        # Mock zones
        zone1 = Mock()
        zone1.name = "us-central1-a"
        zone2 = Mock()
        zone2.name = "us-central1-b"
        gcp_provider.zones_client = Mock()
        gcp_provider.zones_client.list.return_value = [zone1, zone2]
        
        # Mock instances client to raise PermissionDenied for first zone
        gcp_provider.instances_client = Mock()
        gcp_provider.instances_client.list.side_effect = [
            PermissionDenied("Access denied"),
            [mock_instance]
        ]
        
        # Call list_services
        services = gcp_provider.list_services()
        
        # Should skip the denied zone and continue
        assert len(services) == 1
        assert services[0].name == "test-instance-1"
    
    def test_list_services_not_found_zone(self, gcp_provider, mock_instance):
        """Test handling NotFound error for a zone."""
        # Mock zones
        zone1 = Mock()
        zone1.name = "us-central1-a"
        zone2 = Mock()
        zone2.name = "us-central1-b"
        gcp_provider.zones_client = Mock()
        gcp_provider.zones_client.list.return_value = [zone1, zone2]
        
        # Mock instances client to raise NotFound for first zone
        gcp_provider.instances_client = Mock()
        gcp_provider.instances_client.list.side_effect = [
            NotFound("Zone not found"),
            [mock_instance]
        ]
        
        # Call list_services
        services = gcp_provider.list_services()
        
        # Should skip the notfound zone and continue
        assert len(services) == 1
    
    def test_get_service_in_specific_zone(self, gcp_provider, mock_instance):
        """Test retrieving a specific instance in a specific zone."""
        # Mock instances client
        gcp_provider.instances_client = Mock()
        gcp_provider.instances_client.get.return_value = mock_instance
        
        # Call get_service with zone
        service = gcp_provider.get_service("test-instance-1", region="us-central1-a")
        
        assert service is not None
        assert service.name == "test-instance-1"
        assert service.region == "us-central1-a"
    
    def test_get_service_in_all_zones(self, gcp_provider, mock_instance):
        """Test retrieving a specific instance by searching all zones."""
        # Mock zones
        zone1 = Mock()
        zone1.name = "us-central1-a"
        zone2 = Mock()
        zone2.name = "us-central1-b"
        gcp_provider.zones_client = Mock()
        gcp_provider.zones_client.list.return_value = [zone1, zone2]
        
        # Mock instances client to raise NotFound for first zone, then return instance
        gcp_provider.instances_client = Mock()
        gcp_provider.instances_client.get.side_effect = [
            NotFound("Instance not found"),
            mock_instance
        ]
        
        # Call get_service without zone
        service = gcp_provider.get_service("test-instance-1")
        
        assert service is not None
        assert service.name == "test-instance-1"
        assert service.region == "us-central1-b"
    
    def test_get_service_not_found(self, gcp_provider):
        """Test retrieving a non-existent instance."""
        # Mock zones
        zone1 = Mock()
        zone1.name = "us-central1-a"
        gcp_provider.zones_client = Mock()
        gcp_provider.zones_client.list.return_value = [zone1]
        
        # Mock instances client to raise NotFound
        gcp_provider.instances_client = Mock()
        gcp_provider.instances_client.get.side_effect = NotFound("Instance not found")
        
        # Call get_service
        service = gcp_provider.get_service("nonexistent")
        
        assert service is None
    
    def test_convert_to_cloud_service(self, gcp_provider, mock_instance):
        """Test conversion from GCP Instance to CloudService model."""
        service = gcp_provider._convert_to_cloud_service(mock_instance, "us-central1-a")
        
        assert service.provider == CloudProvider.GCP
        assert service.service_type == "Compute Engine"
        assert service.name == "test-instance-1"
        assert service.region == "us-central1-a"
        assert service.status == "RUNNING"
        
        # Check metadata
        assert service.metadata["id"] == "1234567890"
        assert service.metadata["machine_type"] == "n1-standard-1"
        assert service.metadata["internal_ip"] == "10.128.0.2"
        assert service.metadata["external_ip"] == "34.123.45.67"
        assert service.metadata["zone"] == "us-central1-a"
        assert "http" in service.metadata["tags"]
        assert service.metadata["labels"]["env"] == "test"
    
    def test_convert_to_cloud_service_without_network_interfaces(self, gcp_provider):
        """Test conversion when network interfaces are not available."""
        instance = Mock(spec=compute_v1.Instance)
        instance.id = "1234567890"
        instance.name = "test-instance"
        instance.machine_type = "projects/test/zones/us-central1-a/machineTypes/n1-standard-1"
        instance.status = compute_v1.Instance.Status.STOPPED
        instance.creation_timestamp = "2024-01-15T10:30:00Z"
        instance.can_ip_forward = False
        instance.cpu_platform = "Intel Broadwell"
        instance.network_interfaces = None
        instance.tags = None
        instance.labels = {}
        
        service = gcp_provider._convert_to_cloud_service(instance, "us-central1-a")
        
        assert service.metadata["internal_ip"] is None
        assert service.metadata["external_ip"] is None
    
    def test_get_all_zones(self, gcp_provider):
        """Test retrieving all available zones."""
        # Mock zones
        zone1 = Mock()
        zone1.name = "us-central1-a"
        zone2 = Mock()
        zone2.name = "us-central1-b"
        zone3 = Mock()
        zone3.name = "us-east1-b"
        
        gcp_provider.zones_client = Mock()
        gcp_provider.zones_client.list.return_value = [zone1, zone2, zone3]
        
        # Call _get_all_zones
        zones = gcp_provider._get_all_zones()
        
        assert len(zones) == 3
        assert "us-central1-a" in zones
        assert "us-central1-b" in zones
        assert "us-east1-b" in zones
    
    def test_get_all_zones_api_error(self, gcp_provider):
        """Test handling GoogleAPIError when listing zones."""
        gcp_provider.zones_client = Mock()
        gcp_provider.zones_client.list.side_effect = GoogleAPIError("API failed")
        
        with pytest.raises(GoogleAPIError):
            gcp_provider._get_all_zones()
