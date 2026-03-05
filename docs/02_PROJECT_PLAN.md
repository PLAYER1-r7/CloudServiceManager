# Project Plan

> **📖 Reading Order**: 2nd - Read after `01_PREREQUISITES.md`

---

## **📋 Document Metadata**

- **Purpose**: Provide overall project plan, architecture, and development roadmap
- **Audience**: AI Agents, Project Managers, New Developers
- **Prerequisites**: Must have read `01_PREREQUISITES.md`
- **Last Updated**: 2026-03-05

---

## **🎯 Project Overview**

### Project Name
**Cloud Service Manager**

### Mission
Develop a tool to discover and manage resources across multiple cloud providers (AWS, Azure, GCP) with a unified interface

### Vision
Eliminate the complexity of multi-cloud environment resource management by enabling visualization and operation of all cloud resources through a unified interface

---

## **📅 Development Phases**

### Phase 1: CLI Development (Current Phase) ⚡

**Duration**: Week 1-4  
**Status**: 🚧 In Progress

**Goals**:
- ✅ Implement CLI tool to fetch and list cloud resources
- ✅ Support AWS, Azure, and GCP
- ✅ Display services in structured formats (JSON, table, CSV)
- ✅ Build foundation for Phase 2 (Web Application)

**Deliverables**:
- Working CLI tool (`cloudmgr` command)
- Provider integration implementations
- Unit tests (80%+ coverage)
- Complete documentation

### Phase 2: Web Application (Future Plan) 🔮

**Duration**: TBD (after Phase 1 completion)  
**Status**: ⏸️ Not Started

**Note**: ⚠️ **DO NOT implement Phase 2 features at this time**

**Plan Overview**:
- FastAPI-based REST API
- React frontend
- Real-time resource monitoring
- Dashboard functionality

---

## **🛠️ Technology Stack (Confirmed)**

| Category | Technology | Version | Selection Reason |
|---------|------------|---------|------------------|
| **Language** | Python | 3.11+ | Improved type hints, performance, latest features |
| **CLI Framework** | Typer | latest | Modern, type-safe, automatic documentation |
| **AWS SDK** | boto3 | latest | Official AWS, comprehensive service coverage |
| **GCP SDK** | google-cloud-compute | latest | Official GCP SDK |
| **Azure SDK** | azure-mgmt-compute | latest | Official Azure SDK |
| **Development Environment** | Docker + DevContainer | - | Environment consistency, reproducibility |
| **Testing** | pytest | latest | Standard, rich plugin ecosystem |
| **UI (CLI)** | rich | latest | Beautiful tables, color output |

---

## **📁 Project Structure (Fixed)**

\`\`\`
/workspaces/CloudServiceManager/
├── docs/                           # Documentation (English, for AI)
│   ├── 00_README_DOCS.md          # Documentation reading guide ⭐
│   ├── 01_PREREQUISITES.md        # Prerequisites (MUST READ) ⚠️
│   ├── 02_PROJECT_PLAN.md         # This file: Project plan
│   ├── 03_API_DESIGN.md           # CLI/API design specifications
│   ├── 04_SETUP.md                # Setup guide
│   └── 05_DEVELOPMENT_CHECKLIST.md # Development checklist
├── docs_ja/                        # Japanese documentation (for humans)
│   └── (Same structure as docs/)
├── .devcontainer/
│   ├── Dockerfile                 # Dev container image
│   └── devcontainer.json          # Dev container configuration
├── src/
│   └── cli/
│       ├── __init__.py
│       ├── main.py                # ✅ CLI entry point (Typer)
│       ├── providers/             # Cloud provider implementations
│       │   ├── __init__.py
│       │   ├── aws.py             # AWS implementation (boto3)
│       │   ├── gcp.py             # GCP implementation (google-cloud-compute)
│       │   └── azure.py           # Azure implementation (azure-mgmt-compute)
│       └── models/
│           └── service.py         # ✅ Data models (CloudService)
├── tests/                         # Unit tests
│   ├── __init__.py
│   └── test_main.py
├── config.py                      # Application configuration
├── requirements.txt               # Python dependencies (required)
├── pytest.ini                     # pytest configuration
└── README.md                      # Project README
\`\`\`

---

## **🎯 Phase 1 Key Features**

### 1. Unified Service Discovery
- **Purpose**: Fetch resources from all cloud providers
- **Implementation**: Use each provider's SDK and convert to unified model (`CloudService`)
- **Supported Resources**: EC2, Compute Engine, Virtual Machines

### 2. Multiple Output Format Support
- **table**: Default, using Rich library
- **json**: JSON array format (for programmatic use)
- **csv**: CSV format (for spreadsheet integration)

### 3. Filtering & Sorting
- Filter by provider (`--provider`)
- Filter by region (`--region`)
- Future: Filter by service type, status

### 4. Credential Management
- Support each provider's standard authentication methods
- Load from environment variables and configuration files
- **Security**: Never hardcode credentials

### 5. CLI Documentation
- Typer auto-generated help
- `--help` option
- Command examples provided

---

## **🗓️ Development Roadmap**

### Week 1: Project Initialization and CLI Framework ✅
- [x] DevContainer setup
- [x] Project structure creation
- [x] Typer CLI foundation implementation
- [x] Initial documentation creation

### Week 2: AWS Provider Implementation 🚧
- [ ] boto3 integration
- [ ] EC2 instance listing
- [ ] AWS authentication implementation
- [ ] Unit tests (AWS)

### Week 3: GCP & Azure Provider Implementation ⏳
- [ ] GCP Compute Engine integration
- [ ] Azure Virtual Machines integration
- [ ] Conversion to unified data model
- [ ] Unit tests (GCP, Azure)

### Week 4: Testing, Documentation, Optimization ⏳
- [ ] Integration tests
- [ ] Performance optimization
- [ ] Documentation finalization
- [ ] Release preparation

**Legend**: ✅Completed | 🚧In Progress | ⏳Not Started

---

## **📋 Development Requirements**

### Required Environment
- ✅ Docker & DevContainer support
- ✅ Python 3.11+ development environment
- ✅ Cloud provider credentials
- ✅ Git workflow

### Quality Requirements
- **Test Coverage**: 80%+
- **Type Hints**: All functions and methods must have type annotations
- **Documentation**: docstrings (Google Style)
- **Code Quality**: Black (formatting), Ruff (linting)

---

**Last Updated**: 2026-03-05  
**Next Document**: [03_API_DESIGN.md](03_API_DESIGN.md)
