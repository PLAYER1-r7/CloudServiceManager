# Cloud Service Manager

A unified CLI application to discover and manage cloud resources across AWS, Azure, and Google Cloud Platform.

## Features

- **Multi-Cloud Support**: AWS, Azure, GCP
- **Service Discovery**: List all compute instances across providers
- **Multiple Output Formats**: JSON, Table, CSV
- **Unified Interface**: Single CLI for all cloud providers
- **Credential Management**: Support for native cloud authentication

## Quick Start

### Prerequisites

- Docker and Docker Compose
- VS Code with Remote Containers extension
- Cloud provider credentials (optional, for actual cloud integration)

### Development Setup

1. **Clone the repository**

```bash
git clone <repository-url>
cd CloudServiceManager
```

2. **Open in Dev Container**

- In VS Code, use the Remote Containers extension
- Click the green remote indicator (bottom-left)
- Select "Reopen in Container"

3. **Install dependencies** (automatic in container)

```bash
pip install -r requirements.txt
```

4. **Configure cloud credentials**
   See [04_SETUP.md](docs/04_SETUP.md) for detailed instructions.

## Usage

### List all cloud services

```bash
python -m src.cli.main list-services
```

### List services from a specific provider

```bash
python -m src.cli.main list-services --provider aws
python -m src.cli.main list-services --provider gcp --format json
```

### Filter by region

```bash
python -m src.cli.main list-services --provider aws --region us-east-1
```

### Output formats

```bash
# Table (default)
python -m src.cli.main list-services --format table

# JSON
python -m src.cli.main list-services --format json

# CSV
python -m src.cli.main list-services --format csv
```

See [03_API_DESIGN.md](docs/03_API_DESIGN.md) for complete CLI documentation.

## Development Workflow

### ⚠️ GitHub Project Status Management (MANDATORY)

**Rule: Issue作業開始時は必ずProjectのステータスを更新してください**

```bash
# Issue作業開始時
bash .github/scripts/update_project_status.sh <ISSUE_NUM> "In progress"

# PR作成後 (レビュー待ち)
bash .github/scripts/update_project_status.sh <ISSUE_NUM> "In review"

# PR Merge後 (完了)
bash .github/scripts/update_project_status.sh <ISSUE_NUM> "Done"
```

See [.github/PROJECT_WORKFLOW.md](.github/PROJECT_WORKFLOW.md) for detailed workflow guide.

## Documentation

### 📚 Documentation Structure

This project maintains **dual-language documentation**:

- **`/docs`** - English documentation (optimized for AI agents)
- **`/docs_ja`** - Japanese documentation (for human developers)

### 🌐 User Wiki

For end-user guides and troubleshooting, use the GitHub Wiki:

- **[Wiki Home](https://github.com/PLAYER1-r7/CloudServiceManager/wiki)**
- **[Getting Started](https://github.com/PLAYER1-r7/CloudServiceManager/wiki/Getting-Started)**
- **[FAQ](https://github.com/PLAYER1-r7/CloudServiceManager/wiki/FAQ)**

### 📂 Directory Responsibility (MANDATORY)

- **`/docs` and `/docs_ja`**: Product implementation documentation (architecture, API/CLI specs, setup, constraints, checklists)
- **`/.github`**: Repository operation and GitHub workflow documentation (Issues/PR/Projects workflow, branch protection, automation scripts, agent operation guides)
- **Rule**: Place documents by purpose first. If a topic spans both domains, keep the primary source in the correct directory and cross-link from the other.
- **Reference**: See [docs/00_README_DOCS.md](docs/00_README_DOCS.md) for the full documentation policy.

### 📖 Reading Order (MANDATORY)

**Read documentation in this order:**

1. **⚠️ [docs/01_PREREQUISITES.md](docs/01_PREREQUISITES.md)** - *Start here*
   - Tech stack, constraints, critical design decisions
   - Development rules and policies
   - Git workflow, version control, authentication, and GitHub usage
   
2. **[docs/02_PROJECT_PLAN.md](docs/02_PROJECT_PLAN.md)**
   - Project overview, architecture, roadmap
   
3. **[docs/03_API_DESIGN.md](docs/03_API_DESIGN.md)**
   - CLI specifications and command documentation
   
4. **[docs/04_SETUP.md](docs/04_SETUP.md)**
   - Development environment setup procedures
   
5. **[docs/05_DEVELOPMENT_CHECKLIST.md](docs/05_DEVELOPMENT_CHECKLIST.md)**
   - Feature tracking and development progress

**Complete documentation guide**: [docs/00_README_DOCS.md](docs/00_README_DOCS.md)

**Japanese versions available**: See `/docs_ja` for Japanese translations (same structure as `/docs`)

### 📝 Documentation Rules (MANDATORY)

- **Language Separation**: `/docs` = English (AI-optimized), `/docs_ja` = Japanese (human-optimized)
- **Synchronization**: Always update both English AND Japanese versions together
- **Consistency**: Maintain identical structure and content across both language versions
- **Update After Work**: Documentation must be updated whenever you complete work (no exception)

### 🔄 Key Development Rules

Detailed rules are in [01_PREREQUISITES.md](docs/01_PREREQUISITES.md). Quick reference:

| Rule | Location |
|------|----------|
| **Git Workflow** | `develop` branch for development, feature branches from develop, PRs required | [Branch Strategy](docs/01_PREREQUISITES.md#branch-strategy) |
| **Version Control** | W.X.Y.Z format: W/X user-directed, Y=develop push count, Z=commit count | [Versioning Strategy](docs/01_PREREQUISITES.md#versioning-strategy) |
| **GitHub Authentication** | GitHub CLI (`gh`) REQUIRED; Personal Access Tokens FORBIDDEN | [GitHub Authentication Rule](docs/01_PREREQUISITES.md#github-authentication-rule-mandatory) |
| **Authentication** | Always request credentials; never bypass or use placeholders | [Authentication Request Rule](docs/01_PREREQUISITES.md#authentication-request-rule-mandatory) |
| **Missing Commands** | Install required commands; never skip or find alternatives | [Command Not Found Rule](docs/01_PREREQUISITES.md#command-not-found-rule-mandatory) |
| **Directory Operations** | Always verify directory structure before operations | [Directory Operation Rule](docs/01_PREREQUISITES.md#directory-operation-rule-mandatory) |
| **Incremental Development** | Create 1-3 files at a time; prevent network timeouts | [Incremental Development Rule](docs/01_PREREQUISITES.md#incremental-development-rule-mandatory) |
| **GitHub Usage** | Use Issues, PRs, Milestones, Projects for active project management | [GitHub Features Usage](docs/01_PREREQUISITES.md#github-features-usage-mandatory) |
| **Project Management** | Every task must have a GitHub Issue; track all work explicitly | [Project Management with GitHub](docs/01_PREREQUISITES.md#project-management-with-github-mandatory) |

---

## 📊 Project Management

This project uses **GitHub Projects** for task tracking and workflow management.

### 🎯 Quick Links

- **📋 [GitHub Issues](https://github.com/PLAYER1-r7/CloudServiceManager/issues)** - View all tasks
- **📊 [GitHub Projects](https://github.com/PLAYER1-r7/CloudServiceManager/projects)** - Project board
- **🔀 [Pull Requests](https://github.com/PLAYER1-r7/CloudServiceManager/pulls)** - Code reviews

### 📝 Current Issues (7 total)

#### ✅ Completed Issues (2/7)

| Issue | Title | Completion |
|-------|-------|-----------|
| [#2](https://github.com/PLAYER1-r7/CloudServiceManager/issues/2) | CloudService データモデル完成・テスト | ✅ Mar 2026 |
| [#6](https://github.com/PLAYER1-r7/CloudServiceManager/issues/6) | クラウドプロバイダー認証実装 | ✅ Mar 2026 |

#### 🚧 Ongoing & Planned Issues (5/7)

| Issue | Title | Week | Priority |
|-------|-------|------|----------|
| [#5](https://github.com/PLAYER1-r7/CloudServiceManager/issues/5) | Week 2: AWS プロバイダー実装 | Week 2 | 🟡 Medium |
| [#1](https://github.com/PLAYER1-r7/CloudServiceManager/issues/1) | list-services コマンド実装完成 | - | 🟡 Medium |
| [#3](https://github.com/PLAYER1-r7/CloudServiceManager/issues/3) | Week 3: GCP プロバイダー実装 | Week 3 | 🟢 Low |
| [#7](https://github.com/PLAYER1-r7/CloudServiceManager/issues/7) | Week 3: Azure プロバイダー実装 | Week 3 | 🟢 Low |
| [#4](https://github.com/PLAYER1-r7/CloudServiceManager/issues/4) | Week 4: 統合テストと最適化 | Week 4 | 🟢 Low |

### 📚 Project Management Guides

- **[.github/AI_AGENT_PROJECT_GUIDE.md](.github/AI_AGENT_PROJECT_GUIDE.md)** - 🤖 AI Agent project management guide (START HERE)
- **[.github/project_manager.py](.github/project_manager.py)** - Automated project management script
- **[.github/PROJECT_WORKFLOW.md](.github/PROJECT_WORKFLOW.md)** - Daily workflow and best practices
- **[.github/GITHUB_PROJECT_SETUP.md](.github/GITHUB_PROJECT_SETUP.md)** - Project setup guide
- **[.github/GITHUB_SETUP.md](.github/GITHUB_SETUP.md)** - GitHub configuration guide

### 🤖 Quick Project Commands

```bash
# Check project status and get recommendations
python .github/project_manager.py all

# View current status
python .github/project_manager.py status

# Get task recommendations
python .github/project_manager.py recommend

# Generate progress report
python .github/project_manager.py report
```

---

## Project Structure

```
CloudServiceManager/
├── docs/                          # 📄 Documentation (English)
│   ├── 00_README_DOCS.md         # Documentation guide
│   ├── 01_PREREQUISITES.md       # ⚠️ READ FIRST - Critical! Constraints & rules
│   ├── 02_PROJECT_PLAN.md        # Architecture & roadmap
│   ├── 03_API_DESIGN.md          # CLI specifications
│   ├── 04_SETUP.md               # Development setup
│   └── 05_DEVELOPMENT_CHECKLIST.md # Progress tracking
│
├── docs_ja/                        # 📄 Documentation (Japanese)
│   └── (Same structure as docs/)
│
├── .devcontainer/                  # Dev container config
├── src/
│   └── cli/
│       ├── main.py                # CLI entry point
│       ├── models/
│       │   └── service.py          # Data models
│       └── providers/              # Cloud provider implementations
│           ├── aws.py              # AWS provider
│           ├── gcp.py              # GCP provider
│           └── azure.py            # Azure provider
│
├── tests/                          # Unit tests
├── config.py                       # Configuration (includes VERSION)
├── requirements.txt                # Python dependencies
├── pytest.ini                      # Pytest config
└── README.md                       # This file
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_aws_provider.py

# Verbose output
pytest -v
```

### Code Quality

```bash
# Format code
black src/

# Lint
flake8 src/

# Type check
mypy src/
```

## Architecture

### Provider Pattern

Each cloud provider implements a consistent interface:

- `list_services()`: Fetch all services from the provider
- `get_service()`: Get a specific service by ID

### Data Flow

```
CLI Command
    ↓
Provider Manager
    ↓
Cloud Provider (AWS/GCP/Azure)
    ↓
Cloud APIs
    ↓
Data Aggregation
    ↓
Output Formatter (JSON/Table/CSV)
    ↓
User
```

## Future Roadmap

### Phase 2: Web Application

- Convert CLI backend to FastAPI
- Build React frontend
- Add authentication (OAuth2)
- Persistent storage with database

### Phase 3: Advanced Features

- Real-time monitoring
- Resource cost analysis
- Automated actions (start/stop/delete)
- Multi-account management
- Custom dashboards

## GitHub Setup

### Initial Repository Configuration

**Two options for configuring GitHub:**

#### Option 1: Automated Setup Script (Recommended) ✨

**Quick Start: [.github/QUICK_START.md](.github/QUICK_START.md)** - 日本語の簡単ガイド

Use the automated Python script with **GitHub CLI** (no token needed):

```bash
# 1. Install GitHub CLI (if not already installed)
# macOS: brew install gh
# Linux: sudo apt install gh
# Windows: https://cli.github.com/

# 2. Login to GitHub (one-time setup)
gh auth login

# 3. Run the setup script
python .github/setup_github.py
```

**Alternative: Use Fine-grained Personal Access Token**

```bash
export GITHUB_TOKEN="github_pat_xxxxxxxxxxxx"  # Fine-grained PAT
export GITHUB_OWNER="your_username"
export GITHUB_REPO="CloudServiceManager"

python .github/setup_github.py
```

**Documentation:**
- **[.github/QUICK_START.md](.github/QUICK_START.md)** - 🇯🇵 簡単スタートガイド（日本語）
- **[.github/SETUP_SCRIPT.md](.github/SETUP_SCRIPT.md)** - 🇬🇧 Complete usage guide (English)

This script automatically:
- Creates 8 GitHub Labels
- Creates 3 Milestones
- Creates GitHub Project board
- Configures branch protection
- Creates the first GitHub Issue

**Authentication methods** (project policy):
1. **GitHub CLI** (`gh`) - ✅ **REQUIRED** (only permitted method)
2. **GitHub Actions built-in token** - ✅ Permitted for CI/CD only
3. **Personal Access Tokens (any type)** - ❌ **FORBIDDEN** by project policy

⚠️ See [docs/01_PREREQUISITES.md](docs/01_PREREQUISITES.md) - "GitHub Authentication Rule (MANDATORY)"

#### Option 2: Manual GitHub UI Configuration

Follow the step-by-step checklist:

- **[.github/INITIAL_SETUP.md](.github/INITIAL_SETUP.md)** - Manual checklist for GitHub UI configuration
  - Create labels (8 required labels for issue tracking)
  - Create milestones (v1.0.0, v1.1.0, v2.0.0)
  - Configure GitHub Project board for task management
  - Set up branch protection rules for `develop` and `main`
  - Enable CI/CD workflow automation

- **[.github/GITHUB_SETUP.md](.github/GITHUB_SETUP.md)** - Detailed setup guide with instructions
  - Branch protection configuration
  - GitHub Project board setup
  - CI/CD pipeline configuration
  - Issue templates

### GitHub Templates

Issue templates are pre-configured for consistent issue creation:

- **[.github/ISSUE_TEMPLATE/bug_report.md](.github/ISSUE_TEMPLATE/bug_report.md)** - Report bugs
- **[.github/ISSUE_TEMPLATE/feature_request.md](.github/ISSUE_TEMPLATE/feature_request.md)** - Request features
- **[.github/ISSUE_TEMPLATE/task.md](.github/ISSUE_TEMPLATE/task.md)** - Create tasks

### CI/CD Automation

The project includes automated GitHub Actions workflow:

- **[.github/workflows/ci.yml](.github/workflows/ci.yml)** - Continuous Integration/Deployment
  - Automatic testing (Python 3.11, 3.12)
  - Linting with Ruff
  - Code formatting check with Black
  - Type checking with mypy
  - Code coverage reporting
  - Security checks for hardcoded credentials

**Status checks are required to pass before merging PRs.**

## Contributing

### Before You Start

1. **⚠️ Read [01_PREREQUISITES.md](docs/01_PREREQUISITES.md) first** - Contains all development rules
2. **[.github/INITIAL_SETUP.md](.github/INITIAL_SETUP.md)** - If setting up GitHub (one-time, follow checklist)
3. Create a GitHub Issue for your work (track all work explicitly)
4. Create a feature branch from `develop`: `feature/your-feature-name`
5. Ensure all tests pass and documentation is updated before creating PR

### Pull Request Process

1. Create PR against `develop` (never directly to `main`)
2. Link related GitHub Issues in PR description: `Closes #123`
3. Ensure all CI/CD checks pass
4. Request code review from team members
5. Address feedback and merge after approval

### Development Guidelines

- Write tests for all new features (coverage target: 80%+)
- Follow PEP 8 style guide; use Black for formatting
- Add type hints to all functions
- Document public APIs with docstrings
- **Update documentation after every change** (mandatory)

## Troubleshooting

### Container Issues

- Ensure Docker daemon is running
- Delete .devcontainer volume: `docker volume prune`
- Rebuild container: Reopen in Container

### Credential Issues

- Verify environment variables are set correctly
- Check credential file permissions
- See [04_SETUP.md](docs/04_SETUP.md) for provider-specific setup
- Refer to [Authentication & Security Policy](docs/01_PREREQUISITES.md#-authentication--security-policy) in Prerequisites

## License

MIT License

## Contact

For questions or issues, please create a GitHub issue.
