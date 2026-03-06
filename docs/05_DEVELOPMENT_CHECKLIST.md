# Development Checklist

> **📖 Reading Order**: 5th - Track development progress

---

## **📋 Document Metadata**

- **Purpose**: Track development setup progress and next steps
- **Audience**: AI Agents, Developers
- **Prerequisites**: Environment setup completed per `04_SETUP.md`
- **Last Updated**: 2026-03-06

---

## **✅ Initial DevContainer Setup**

### Automated Setup Completed

- [x] Created `Dockerfile` with Python 3.11 environment
- [x] Configured `devcontainer.json` with:
  - VS Code extensions for Python development
  - Python formatting (Black) and linting (Ruff)
  - Auto-format on save
  - Forwarded ports for web development
- [x] Created `requirements.txt` with all dependencies
- [x] Configured project structure

### Documentation Created ✅

- [x] `00_README_DOCS.md` - Documentation reading guide
- [x] `01_PREREQUISITES.md` - Prerequisites and constraints
- [x] `02_PROJECT_PLAN.md` - Project overview and roadmap
- [x] `03_API_DESIGN.md` - CLI design documentation
- [x] `04_SETUP.md` - Development setup guide
- [x] `05_DEVELOPMENT_CHECKLIST.md` - This file
- [x] `README.md` - Main project documentation
- [x] `docs_ja/` - Japanese documentation (synchronized)

### Code Structure ✅

- [x] CLI entry point (`src/cli/main.py`)
- [x] Data models (`src/cli/models/service.py`) - **Issue #2 ✅ DONE (95% coverage)**
- [x] AWS provider (`src/cli/providers/aws.py`)
- [x] GCP provider (`src/cli/providers/gcp.py`)
- [x] Azure provider (`src/cli/providers/azure.py`)
- [x] Tests structure (`tests/`)

### Issue Completion Status 📊

#### ✅ Completed

- **Issue #2**: CloudService Pydantic Model (DONE)
  - Created Pydantic CloudService model with 7 required fields
  - ISO 8601 datetime validation
  - 95% test coverage (31 tests passed)
  - Version: 1.0.0.0 → 1.0.1.8

- **Issue #6**: Cloud Provider Authentication (DONE - PR #18 merged)
  - CloudAuthBase abstract base class (84 lines)
  - AWSAuth implementation (156 lines) - boto3 Session, env vars, credentials file, IAM role
  - GCPAuth implementation (179 lines) - Application Default Credentials, service account
  - AzureAuth implementation (168 lines) - DefaultAzureCredential chain
  - CloudAuthManager for multi-cloud management (217 lines)
  - Comprehensive test suite (46 tests, 62% coverage)
  - Dependencies added: azure-mgmt-resource
  - Version: 1.0.1.8 → 1.0.2.0

- **Issue #5**: AWS Provider Implementation (DONE)
  - AWSProvider class with AWSAuth integration (99 lines)
  - EC2 instance listing across single or all regions
  - CloudService model conversion with comprehensive metadata
  - Error handling for unauthorized regions and missing instances
  - Support for multiple authentication methods via AWSAuth
  - Comprehensive test suite (17 tests, 85% coverage)
  - Created `test_aws_provider.py` with complete test coverage
  - All tests passing (130 passed, 3 skipped)
  - Version: 1.0.2.0 → 1.0.3.0

- **Issue #3**: GCP Provider Implementation (DONE)
  - GCPProvider class with GCPAuth integration (255 lines)
  - Compute Engine instance listing across single or all zones
  - CloudService model conversion with comprehensive metadata
  - Error handling for unauthorized zones and missing instances
  - Support for multiple authentication methods via GCPAuth
  - Comprehensive test suite (17 tests, 79% coverage)
  - Created `test_gcp_provider.py` with complete test coverage
  - All tests passing (17 passed)
  - Version: 1.0.3.0 → 1.0.4.0

- **Issue #7**: Azure Provider Implementation (DONE)
  - AzureProvider class with AzureAuth integration (310 lines)
  - Virtual Machine listing across single or all resource groups and regions
  - CloudService model conversion with comprehensive metadata
  - Error handling for unauthorized resource groups and missing VMs
  - Support for multiple authentication methods via AzureAuth
  - Power state extraction from instance views
  - Comprehensive test suite (16 tests, 83% coverage)
  - Created `test_azure_provider.py` with complete test coverage
  - All tests passing (16 passed)
  - Version: 1.0.4.0 → 1.0.5.0

- **Issue #1**: list-services Command Implementation (DONE)
  - Implemented provider selection with strict choices (`aws|gcp|azure|all`)
  - Added robust multi-provider aggregation with partial-failure warnings
  - Added JSON/table/CSV output handling using unified `CloudService` serialization
  - Fixed table rendering for string-based provider values
  - Added unit tests for JSON/CSV output and failure handling behavior
  - All CLI tests passing
  - Version: 1.0.5.0 → 1.0.6.0

- **Issue #4**: Integration Tests and Optimization (DONE)
  - Added CLI integration test suite (`tests/test_cli_integration.py`)
  - Added multi-provider aggregation integration verification
  - Added region filter pass-through integration verification
  - Added get-service provider dispatch integration verification
  - Re-enabled AWS integration tests previously skipped due mocking setup
  - Optimized deterministic output ordering in `main.py`
  - Optimized CSV output generation with batched row serialization
  - Full test suite stabilized at `172 passed, 1 skipped`
  - CLI unit + integration coverage for `src/cli/main.py` reached 85%
  - Version: 1.0.6.0 → 1.0.7.0

- **Phase 2**: Web API Skeleton (IN PROGRESS)
  - Created FastAPI application skeleton (`src/api/main.py`)
  - Implemented core endpoints:
    - `GET /health` - Health check endpoint
    - `GET /services` - List services with provider/region filtering
    - `GET /services/{provider}/{service_id}` - Get specific service details
  - Added fault-tolerant provider initialization (skips unavailable providers)
  - **Enhanced `/services` endpoint with:**
    - Status filtering (`?status=running`)
    - Service type filtering (`?service_type=EC2`)
    - Flexible sorting (`?sort_by=name&sort_order=desc`)
    - Support for 6 sort fields: name, provider, status, created_at, region, service_type
  - Created comprehensive API test suite (`tests/test_api_main.py`, 8 tests passing)
  - Created API startup script (`scripts/start_api.sh`)
  - Updated README.md and API design docs with filtering/sorting examples
  - Dependencies added: fastapi, uvicorn, httpx
  - Interactive API docs available at `/docs` and `/redoc`
  - Version: 1.0.7.0 → 2.0.0-alpha

#### 🚧 In Progress
None currently idle

#### 📋 Pending
None

### GitHub Repository Setup ✅

- [x] Installed GitHub CLI (`gh`)
- [x] Authenticated with GitHub (Fine-grained token)
- [x] Created remote repository: https://github.com/PLAYER1-r7/CloudServiceManager
- [x] Pushed initial commit
- [x] Created 7 GitHub Issues for development tracking
  - CloudService model implementation
  - Cloud provider authentication
  - AWS/GCP/Azure provider implementations
  - list-services command implementation
  - Integration tests and optimization

---

## **🎯 Next Steps**

### 1. View Development Tasks

All development tasks are tracked as GitHub Issues:

```bash
# List all issues
gh issue list --repo PLAYER1-r7/CloudServiceManager

# View issue details
gh issue view 5 --repo PLAYER1-r7/CloudServiceManager  # Example: Week 2 - AWS Implementation

# Filter by week
gh issue list --repo PLAYER1-r7/CloudServiceManager --label "week-2"
```

**Development Issues Created**:
- [#1](https://github.com/PLAYER1-r7/CloudServiceManager/issues/1) - CloudService データモデル完成・テスト
- [#2](https://github.com/PLAYER1-r7/CloudServiceManager/issues/2) - クラウド認証メカニズム実装
- [#3](https://github.com/PLAYER1-r7/CloudServiceManager/issues/3) - Week 3: GCP プロバイダー実装
- [#4](https://github.com/PLAYER1-r7/CloudServiceManager/issues/4) - Week 4: 統合テストと最適化
- [#5](https://github.com/PLAYER1-r7/CloudServiceManager/issues/5) - Week 2: AWS プロバイダー実装
- [#6](https://github.com/PLAYER1-r7/CloudServiceManager/issues/6) - list-services コマンド実装完成
- [#7](https://github.com/PLAYER1-r7/CloudServiceManager/issues/7) - Week 3: Azure プロバイダー実装

### 2. Open in DevContainer

```bash
# In VS Code:
# 1. Press Ctrl+Shift+P (or Cmd+Shift+P on macOS)
# 2. Type: Remote-Containers: Reopen in Container
# 3. Wait for container build (2-3 minutes first time)
```

### 3. Verify Installation

```bash
python --version        # Should be Python 3.11+
pip list               # Should show installed packages
pytest --version       # Should be installed
```

### 4. Set Up Cloud Credentials

See [04_SETUP.md](04_SETUP.md) for provider-specific setup:

- AWS: Set `~/.aws/credentials` or `AWS_*` environment variables
- GCP: Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable
- Azure: Set `AZURE_*` environment variables or use `az login`

### 5. Test the Setup

```bash
# Run CLI help
python -m src.cli.main --help

# Run unit tests
pytest tests/

# Run tests with coverage
pytest --cov=src tests/
```

### 5. Use Project Management Tools

```bash
# Check what to work on next
python .github/project_manager.py all

# View task recommendations
python .github/project_manager.py recommend

# Track progress
python .github/project_manager.py report
```

**AI Agent Guide**: See [.github/AI_AGENT_PROJECT_GUIDE.md](../.github/AI_AGENT_PROJECT_GUIDE.md)

### ⚠️ GitHub Project Status Management (MANDATORY)

**Rule: You MUST update the Project status when starting work on an Issue**

```bash
# When starting work on an issue
bash .github/scripts/update_project_status.sh <ISSUE_NUMBER> "In progress"

# After creating a PR (waiting for review)
bash .github/scripts/update_project_status.sh <ISSUE_NUMBER> "In review"

# After PR merge (completed)
bash .github/scripts/update_project_status.sh <ISSUE_NUMBER> "Done"
```

Available statuses: `Backlog`, `Ready`, `In progress`, `In review`, `Done`

Detailed workflow guide: [.github/PROJECT_WORKFLOW.md](../.github/PROJECT_WORKFLOW.md)

### 6. Start Development

- Read [02_PROJECT_PLAN.md](02_PROJECT_PLAN.md) for overview
- Check [03_API_DESIGN.md](03_API_DESIGN.md) for CLI commands
- Follow priority recommendations from project manager
- Implement cloud provider features
- Write tests for new functionality

---

## **📊 Current Development Status**

### Current Version

**VERSION: 1.0.7.0** (as of 2026-03-06)

Version format: `W.X.Y.Z`
- W (Major): User-directed strategic changes
- X (Minor): User-directed feature additions
- Y (Development): Incremented on each develop branch push
- Z (Commit): Incremented on each commit

See [01_PREREQUISITES.md](01_PREREQUISITES.md) for detailed versioning rules.

### ✅ Completed Work

#### Issue #2: CloudService データモデル完成・テスト (DONE)
- **Status**: ✅ Completed and merged to develop
- **PR**: [#17](https://github.com/PLAYER1-r7/CloudServiceManager/pull/17)
- **Achievements**:
  - Migrated from dataclass to Pydantic BaseModel
  - Implemented strict field validation
  - Added ISO 8601 timestamp validation
  - Created serialization/deserialization methods
  - **Test Coverage**: 95% (target: 80%+)
  - **Tests**: 27 unit tests + 6 integration tests = 31 passed, 2 skipped
- **Files Changed**: 39 files (+7,016/-34 lines)
- **Version**: 1.0.0.1 → 1.0.0.6 (6 commits)
- **Merged**: 2026-03-05

**Key deliverables**:
- `src/cli/models/service.py` - Pydantic-based CloudService model
- `tests/test_models.py` - Comprehensive unit tests
- `tests/test_aws_integration.py` - AWS provider integration tests

#### Project Management Automation (DONE)
- **Status**: ✅ Implemented
- **Tool**: `.github/scripts/update_project_status.sh`
- **Rule**: MANDATORY status updates when starting/completing Issues
- **Workflow**: Backlog → In progress → In review → Done
- **Documentation**: [.github/PROJECT_WORKFLOW.md](../.github/PROJECT_WORKFLOW.md)

#### Development Environment Improvements (DONE)
- **Status**: ✅ Completed
- **Added**: Ruff linter (modern replacement for Flake8)
- **Updated**: `requirements.txt`, `Dockerfile`
- **Benefit**: Faster linting, better error messages

#### GitHub Infrastructure (DONE)
- **Status**: ✅ Completed
- **Added**:
  - CI/CD workflow (`.github/workflows/ci.yml`)
  - Issue templates with auto-labeling
  - GitHub Discussion automation scripts
  - Branch protection rules (develop + main)
  - Setup automation scripts

### 🚧 In Progress

- None. All Phase 1 issues (#1 - #7) are completed.

### 📅 Upcoming Work

1. Prepare Phase 2 API planning tasks.
2. Define FastAPI endpoints and data contract proposals.
3. Add release notes and tag Phase 1 completion.

### 📈 Progress Metrics

- **Issues Completed**: 7/7 (100%)
- **Test Coverage**: 85% (overall `src` coverage)
- **CLI Coverage**: 85% (`src/cli/main.py` unit + integration)
- **Test Results**: 172 passed, 1 skipped
- **Version**: 1.0.7.0

---

## **🛠️ Development Commands**

# After creating a PR (waiting for review)
bash .github/scripts/update_project_status.sh <ISSUE_NUMBER> "In review"

# After PR merge (completed)
bash .github/scripts/update_project_status.sh <ISSUE_NUMBER> "Done"
```

Available statuses: `Backlog`, `Ready`, `In progress`, `In review`, `Done`

Detailed workflow guide: [.github/PROJECT_WORKFLOW.md](../.github/PROJECT_WORKFLOW.md)

### 6. Start Development

- Read [02_PROJECT_PLAN.md](02_PROJECT_PLAN.md) for overview
- Check [03_API_DESIGN.md](03_API_DESIGN.md) for CLI commands
- Follow priority recommendations from project manager
- Implement cloud provider features
- Write tests for new functionality

---

## **🛠️ Development Commands**

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type check
mypy src/

# Run tests
pytest
pytest -v                    # Verbose
pytest --cov=src            # Coverage report
pytest -k "aws"             # Run specific tests

# CLI Usage
python -m src.cli.main list-services
python -m src.cli.main list-services --provider aws --format json
```

## Troubleshooting

### Container won't build

```bash
docker volume prune          # Clean up old volumes
docker system prune         # Clean up unused images/containers
# Then reopen in container
```

---

**Last Updated**: 2026-03-06  
**Previous Document**: [04_SETUP.md](04_SETUP.md)

### Dependencies not installing

```bash
pip cache purge
pip install -r requirements.txt --force-reinstall
```

### Credentials not working

```bash
# Verify environment variables
echo $AWS_ACCESS_KEY_ID
echo $AZURE_SUBSCRIPTION_ID
echo $GOOGLE_APPLICATION_CREDENTIALS

# Check credential files
ls -la ~/.aws/credentials
```

## Technology Stack

| Component            | Version | Purpose         |
| -------------------- | ------- | --------------- |
| Python               | 3.11+   | Core language   |
| Typer                | 0.9+    | CLI framework   |
| Boto3                | 1.28+   | AWS SDK         |
| google-cloud-compute | 1.13+   | GCP SDK         |
| azure-mgmt-compute   | 30+     | Azure SDK       |
| Black                | 23+     | Code formatting |
| Flake8               | 6+      | Linting         |
| Pytest               | 7+      | Testing         |

## Team Notes

- All documentation is in English for AI agent compatibility
- Use conventional commits for git messages
- Maintain >80% test coverage
- Document public APIs with docstrings
- Update docs when adding features
