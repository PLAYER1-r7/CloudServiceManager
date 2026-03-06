# CLI Design and API Specification

> **📖 Reading Order**: 3rd - Read before implementing features

---

## **📋 Document Metadata**

- **Purpose**: Detailed definition of CLI commands and API specifications
- **Audience**: AI Agents, Implementers
- **Prerequisites**: Must have read `01_PREREQUISITES.md` and `02_PROJECT_PLAN.md`
- **Last Updated**: 2026-03-05

---

## **🎯 CLI Overview**

### Command Name
**`cloudmgr`** - Short for Cloud Manager

### Design Philosophy
- **Unified Interface**: Same command structure for all cloud providers
- **Intuitive**: Follow standard CLI patterns (similar to kubectl, aws-cli)
- **Flexible Output**: Users can choose output format based on their use case
- **Type-Safe**: Leverage Typer for type checking and automatic validation

---

## **📝 Command Specifications**

### 1. list-services Command

#### Overview
List all services from specified cloud providers

#### Signature
\`\`\`bash
cloudmgr list-services [OPTIONS]
\`\`\`

#### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| \`--provider\` | \`-p\` | Choice[aws\|gcp\|azure\|all] | \`all\` | Target cloud provider |
| \`--region\` | \`-r\` | str | \`None\` | Region filter (provider-specific) |
| \`--format\` | \`-f\` | Choice[json\|table\|csv] | \`table\` | Output format |

#### Usage Examples

\`\`\`bash
# List all services from all providers in table format (default)
cloudmgr list-services

# List only AWS services in JSON format
cloudmgr list-services --provider aws --format json

# List GCP services in us-central1 region only
cloudmgr list-services -p gcp -r us-central1

# List all services in CSV format (for export)
cloudmgr list-services --format csv
\`\`\`

#### Output Format Specifications

##### Table Format (Default)
- **Library Used**: \`rich.table.Table\`
- **Features**: 
  - Color support
  - Automatic column width adjustment
  - Clean formatting with borders

**Output Example**:
\`\`\`
CloudServices
┏━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Provider ┃ Service Type ┃ Name                ┃ Region      ┃ Status  ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━┩
│ aws      │ EC2          │ i-0123456789abcdef0 │ us-east-1   │ running │
│ gcp      │ Compute      │ instance-1          │ us-central1 │ RUNNING │
│ azure    │ Virtual Mach │ vm-01               │ eastus      │ unknown │
└──────────┴──────────────┴─────────────────────┴─────────────┴─────────┘
\`\`\`

##### JSON Format
- **Format**: JSON array
- **Use Case**: Programmatic processing, pipeline integration

**Schema**:
\`\`\`json
[
  {
    "provider": "aws",
    "service_type": "EC2",
    "name": "i-0123456789abcdef0",
    "region": "us-east-1",
    "status": "running",
    "created_at": "2024-01-15T10:30:00Z",
    "metadata": {
      "instance_type": "t2.micro",
      "image_id": "ami-0123456789abcdef0"
    }
  }
]
\`\`\`

**Field Specifications**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| \`provider\` | string | ✅ | "aws" \| "gcp" \| "azure" |
| \`service_type\` | string | ✅ | Service type (EC2, Compute, etc.) |
| \`name\` | string | ✅ | Resource name or ID |
| \`region\` | string | ✅ | Region name |
| \`status\` | string | ✅ | Status (provider-specific) |
| \`created_at\` | string | ✅ | ISO 8601 formatted datetime |
| \`metadata\` | object | ✅ | Provider-specific additional information (dict) |

##### CSV Format
- **Format**: Header row + Data rows
- **Use Case**: Import to spreadsheets, data analysis tools

**Output Example**:
\`\`\`csv
provider,service_type,name,region,status,created_at,metadata
aws,EC2,i-0123456789abcdef0,us-east-1,running,2024-01-15T10:30:00Z,"{""instance_type"": ""t2.micro""}"
gcp,Compute,instance-1,us-central1,RUNNING,2024-01-14T08:20:00Z,"{""machine_type"": ""n1-standard-1""}"
\`\`\`

**Note**: metadata is escaped as JSON string

---

### 2. get-service Command (Future Implementation)

#### Overview
Get detailed information about a specific cloud service

#### Signature
\`\`\`bash
cloudmgr get-service [OPTIONS]
\`\`\`

#### Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| \`--provider\` | \`-p\` | Choice[aws\|gcp\|azure] | **Required** | Target cloud provider |
| \`--id\` | \`-i\` | str | **Required** | Service identifier (instance ID, etc.) |
| \`--format\` | \`-f\` | Choice[json\|table\|csv] | \`json\` | Output format |

#### Usage Examples

\`\`\`bash
# Get AWS EC2 instance details
cloudmgr get-service --provider aws --id i-0123456789abcdef0

# Get GCP instance details
cloudmgr get-service -p gcp -i instance-1
\`\`\`

---

### 3. init-config Command (Future Implementation)

#### Overview
Guide cloud provider credential configuration

#### Signature
\`\`\`bash
cloudmgr init-config
\`\`\`

#### Purpose
- Interactively guide users through credential configuration
- Generate configuration files
- Validate credentials

---

## **🗂️ Data Models**

### CloudService (Unified Service Model)

Convert all cloud provider resources to this model.

\`\`\`python
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class CloudService:
    """
    Unified cloud service representation
    
    Map all cloud provider (AWS, GCP, Azure) resources to this common model.
    """
    provider: str                   # "aws" | "gcp" | "azure"
    service_type: str               # "EC2", "Compute Engine", "Virtual Machine", etc.
    name: str                       # Resource name or ID
    region: str                     # Region or zone
    status: str                     # Status (provider-specific)
    created_at: str                 # ISO 8601 formatted timestamp
    metadata: Dict[str, Any]        # Provider-specific additional information
\`\`\`

**Field Details**:

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| \`provider\` | str | ✅ | Provider identifier | "aws", "gcp", "azure" |
| \`service_type\` | str | ✅ | Service type | "EC2", "Compute", "Virtual Machine" |
| \`name\` | str | ✅ | Resource name/ID | "i-0123abc", "instance-1", "vm-01" |
| \`region\` | str | ✅ | Region/Zone | "us-east-1", "us-central1-a", "eastus" |
| \`status\` | str | ✅ | Resource status | "running", "RUNNING", "stopped" |
| \`created_at\` | str | ✅ | Creation datetime (ISO 8601) | "2024-01-15T10:30:00Z" |
| \`metadata\` | dict | ✅ | Additional information (dict) | \`{"instance_type": "t2.micro"}\` |

### CloudProvider (Enum)

\`\`\`python
from enum import Enum

class CloudProvider(str, Enum):
    """Supported cloud providers"""
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"
\`\`\`

---

## **⚠️ Error Handling**

The CLI properly handles the following errors:

### Authentication Errors
- **Cause**: Credentials not configured or invalid
- **Example Message**: \`Error: AWS credentials not found. Please configure credentials.\`
- **Exit Code**: 1

### Region Errors
- **Cause**: Invalid region specified
- **Example Message**: \`Error: Invalid region 'us-invalid-1' for provider 'aws'\`
- **Exit Code**: 2

### Network Errors
- **Cause**: API connection failure
- **Example Message**: \`Error: Failed to connect to AWS API. Check network connection.\`
- **Exit Code**: 3

### Provider Errors
- **Cause**: Unsupported provider
- **Example Message**: \`Error: Unsupported provider 'oracle'\`
- **Exit Code**: 4

**Error Handling Principles**:
- ✅ Display clear error messages
- ✅ Return appropriate exit codes
- ✅ Suggest solutions when possible
- ✅ Show stack traces only in debug mode

---

## **🔧 Implementation Guidelines**

### Provider Implementation Pattern

Each provider implements the following interface:

\`\`\`python
from abc import ABC, abstractmethod
from typing import List, Optional

class CloudProviderBase(ABC):
    """Base class for cloud providers"""
    
    @abstractmethod
    def list_services(self, region: Optional[str] = None) -> List[CloudService]:
        """
        Retrieve list of services
        
        Args:
            region: Region filter (optional)
            
        Returns:
            List of CloudService objects
        """
        pass
    
    @abstractmethod
    def get_service(self, service_id: str) -> CloudService:
        """
        Get specific service details
        
        Args:
            service_id: Service identifier
            
        Returns:
            CloudService object
        """
        pass
\`\`\`

### Implementation Checklist

When implementing a new provider:
- [ ] Inherit from \`CloudProviderBase\`
- [ ] Implement \`list_services()\` method
- [ ] Implement \`get_service()\` method
- [ ] Use provider-specific SDK
- [ ] Convert to unified model (\`CloudService\`)
- [ ] Implement error handling
- [ ] Create unit tests (using mocks)
- [ ] Write docstrings (with type hints)

---

**Last Updated**: 2026-03-05  
**Next Document**: [04_SETUP.md](04_SETUP.md)

---

## **🌐 Phase 2 API Skeleton (FastAPI)**

Phase 2 has started with a minimal FastAPI backend skeleton.

### Base Implementation

- Entry point: `src/api/main.py`
- Framework: FastAPI
- Goal: Reuse existing provider implementations via API endpoints

### Endpoints (Initial)

#### `GET /health`
- Purpose: Liveness/readiness check
- Response:

```json
{
  "status": "ok"
}
```

#### `GET /services`
- Purpose: List services from one or all providers with filtering, sorting, and pagination
- Query parameters:
  - `provider`: `aws | gcp | azure | all` (default: `all`)
  - `region`: Optional region/zone filter
  - `status`: Optional status filter (e.g., `running`, `stopped`)
  - `service_type`: Optional service type filter (e.g., `EC2`, `Compute Engine`)
  - `sort_by`: Sort field - `name | provider | status | created_at | region | service_type` (default: `name`)
  - `sort_order`: Sort order - `asc | desc` (default: `asc`)
  - `limit`: Maximum number of results to return (1-1000, default: 100)
  - `offset`: Number of results to skip (≥0, default: 0)
- Response: Paginated response with metadata
  ```json
  {
    "items": [/* CloudService objects */],
    "total": 250,
    "limit": 100,
    "offset": 0,
    "has_more": true
  }
  ```
- Examples:
  ```bash
  # Filter by status
  GET /services?status=running
  
  # Filter by service type
  GET /services?service_type=EC2
  
  # Sort by creation date (descending)
  GET /services?sort_by=created_at&sort_order=desc
  
  # Pagination: first page (items 0-99)
  GET /services?limit=100&offset=0
  
  # Pagination: second page (items 100-199)
  GET /services?limit=100&offset=100
  
  # Combined: running EC2 instances sorted by name, paginated
  GET /services?provider=aws&service_type=EC2&status=running&sort_by=name&limit=50
  ```

#### `GET /services/{provider}/{service_id}`
- Purpose: Retrieve a specific service from a provider
- Path parameters:
  - `provider`: `aws | gcp | azure`
  - `service_id`: provider-specific service identifier
- Response: `CloudService`
- Errors:
  - `400`: unsupported provider
  - `404`: service not found

### Test Coverage

- New test file: `tests/test_api_main.py`
- Covered scenarios:
  - `/health` success
  - `/services` list response with pagination
  - `/services` with status filter
  - `/services` with service_type filter
  - `/services` with sorting (asc/desc)
  - `/services` with combined filters and sorting
  - `/services` pagination with limit
  - `/services` pagination with offset
  - `/services` has_more flag validation
  - `/services/{provider}/{service_id}` success
  - `/services/{provider}/{service_id}` not found

### Production Features (Version 2.0.0-beta)

#### CORS Configuration
- **Purpose**: Enable frontend applications to call the API
- **Allowed Origins**:
  - `http://localhost:3000` (React default)
  - `http://localhost:8080` (Vue default)
  - `http://localhost:4200` (Angular default)
  - `http://localhost:5173` (Vite default)
- **Configuration**: See `CORSMiddleware` in `src/api/main.py`

#### Rate Limiting
- **Implementation**: SlowAPI middleware
- **Limits**:
  - `GET /health`: 100 requests/minute
  - `GET /services`: 30 requests/minute
  - `GET /services/{provider}/{service_id}`: 60 requests/minute
- **Error Response**: `429 Too Many Requests` when limit exceeded

#### API Key Authentication (Optional)
- **Header**: `X-API-Key`
- **Enabled**: Set environment variable `ENABLE_API_AUTH=true`
- **Configuration**: Set `API_KEY` environment variable with expected key
- **Default**: Disabled (no authentication required)
- **Error Response**: `401 Unauthorized` for invalid/missing key when enabled

#### Caching
- **Implementation**: LRU cache for cache key generation
- **Purpose**: Improve response times for repeated queries
- **Configuration**: Maximum 128 cached keys

#### OpenAPI Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Tags**: 
  - `health`: Health check endpoints
  - `services`: Service management operations
- **Version**: 2.0.0-beta

**Last Updated**: 2026-03-06
