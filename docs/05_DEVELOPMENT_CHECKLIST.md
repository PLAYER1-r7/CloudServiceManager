# Development Checklist

> **📖 Reading Order**: 5th - Track development progress

---

## **📋 Document Metadata**

- **Purpose**: Track development setup progress and next steps
- **Audience**: AI Agents, Developers
- **Prerequisites**: Environment setup completed per `04_SETUP.md`
- **Last Updated**: 2026-03-05

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
- [x] Data models (`src/cli/models/service.py`)
- [x] AWS provider (`src/cli/providers/aws.py`)
- [x] GCP provider (`src/cli/providers/gcp.py`)
- [x] Azure provider (`src/cli/providers/azure.py`)
- [x] Tests structure (`tests/`)

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
pyt

---

**Last Updated**: 2026-03-05  
**Previous Document**: [04_SETUP.md](04_SETUP.md)hon -m src.cli.main list-services
python -m src.cli.main list-services --provider aws --format json
```

## Troubleshooting

### Container won't build

```bash
docker volume prune          # Clean up old volumes
docker system prune         # Clean up unused images/containers
# Then reopen in container
```

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
