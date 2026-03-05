# Setup Guide

> **📖 Reading Order**: 4th - Refer to this when setting up the environment

---

## **📋 Document Metadata**

- **Purpose**: Provide development environment setup procedures
- **Audience**: New Developers, AI Agents (during environment setup)
- **Prerequisites**: Must have read `01_PREREQUISITES.md`
- **Last Updated**: 2026-03-05

---

## **🎯 Setup Overview**

This guide covers setup for:
1. ✅ Docker DevContainer development environment
2. ✅ Python 3.11+ and dependencies
3. ✅ Cloud provider credentials (AWS/GCP/Azure)
4. ✅ Development tools (pytest, black, ruff, etc.)

---

## **📋 Prerequisites**

Ensure the following are installed:

| Requirement | Version | Verification Command |
|------------|---------|---------------------|
| **Docker** | 20.10+ | \`docker --version\` |
| **VS Code** | Latest | - |
| **Remote - Containers Extension** | Latest | Check in VS Code Extensions || **GitHub CLI** | 2.46+ | `gh --version` |

### GitHub Account Setup
- GitHub account (for code collaboration)
- Fine-grained Personal Access Token (for authentication)
- See "Step 4: GitHub Setup" below
### Cloud Accounts (Optional)
To work with actual cloud resources:
- AWS account
- GCP project
- Azure subscription

---

## **🚀 Setup Steps**

### Step 1: Open Project in VS Code

1. Open this project folder in VS Code
   \`\`\`bash
   code /workspaces/CloudServiceManager
   \`\`\`

2. Click the **Remote Container icon** in the bottom-left corner
   Or press \`Ctrl+Shift+P\` (Mac: \`Cmd+Shift+P\`) to open the command palette

3. Select **"Remote-Containers: Reopen in Container"**

4. Wait for container build (first time: 2-3 minutes)

---

### Step 2: Verify Python Environment

Execute the following in the DevContainer:

\`\`\`bash
# Check Python version (should be 3.11+)
python --version
# Output example: Python 3.11.x

# Check pip version
pip --version

# Verify Python virtual environment path
which python
# Output: /opt/venv/bin/python
\`\`\`

**Current Environment**:
- Python: 3.11+
- Virtual Environment: \`/opt/venv\` (automatically activated)
- OS: Debian GNU/Linux 13 (trixie)

---

### Step 3: Install Project Dependencies

\`\`\`bash
# Install packages from requirements.txt
pip install -r requirements.txt

# Verify installation
pip list | grep -E "typer|boto3|google-cloud|azure"
\`\`\`

**Main Packages Installed**:
- typer[all] - CLI framework
- boto3 - AWS SDK
- google-cloud-compute - GCP SDK  
- azure-mgmt-compute - Azure SDK
- rich - CLI output
- pytest, pytest-cov - Testing framework

---

### Step 4: GitHub Setup (For Code Collaboration)

The project is hosted on GitHub. Initialize Git and set up remote:

#### Step 4a: Initialize Local Git Repository

```bash
cd /workspaces/CloudServiceManager

# Initialize git (if not already done)
git init

# Configure user information
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add all files and commit
git add -A
git commit -m "Initial commit: Project structure and documentation"
```

#### Step 4b: GitHub CLI Authentication

For secure authentication without Classic tokens (recommended approach):

```bash
# Install GitHub CLI (if not available)
apt update && apt install -y gh

# Authenticate with GitHub CLI
gh auth login

# Select GitHub.com
# Choose: Authenticate via web browser
# Follow the browser prompts to authorize the application

# Verify authentication
gh auth status
# Output should show: ✓ Logged in to github.com account <username>
```

#### Step 4c: Create Remote Repository

For new repositories:

```bash
# Create repository on GitHub and push code
gh repo create CloudServiceManager --public --source=. --remote=origin --push
```

For existing repositories:

```bash
# Add remote and push
git remote add origin https://github.com/PLAYER1-r7/CloudServiceManager.git
git push -u origin master
```

**Repository Information**:
- **URL**: https://github.com/PLAYER1-r7/CloudServiceManager
- **Owner**: PLAYER1-r7
- **Visibility**: Public
- **Default Branch**: master

Verify connection:

```bash
git remote -v
# Should output:
# origin  https://github.com/PLAYER1-r7/CloudServiceManager.git (fetch)
# origin  https://github.com/PLAYER1-r7/CloudServiceManager.git (push)
```

---

### Step 5: View Project Issues

Development tasks are tracked as GitHub Issues. View them with:

```bash
# List all issues
gh issue list --repo PLAYER1-r7/CloudServiceManager

# View specific issue
gh issue view <issue-number> --repo PLAYER1-r7/CloudServiceManager

# Filter issues by label
gh issue list --repo PLAYER1-r7/CloudServiceManager --label "week-2"
```

**Created Development Issues**:
- CloudService データモデル完成・テスト (#1)
- クラウド認証メカニズム実装 (#2)
- Week 3: GCP プロバイダー実装 (#3)
- Week 4: 統合テストと最適化 (#4)
- Week 2: AWS プロバイダー実装 (#5)
- list-services コマンド実装完成 (#6)
- Week 3: Azure プロバイダー実装 (#7)

See [GitHub Issues](https://github.com/PLAYER1-r7/CloudServiceManager/issues) for full details.

---

## **🔐 Cloud Provider Authentication Setup**

### AWS Authentication Setup

#### Method 1: AWS Credentials File (Recommended)

Create \`~/.aws/credentials\` file:

\`\`\`bash
mkdir -p ~/.aws
cat <<EOF > ~/.aws/credentials
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
EOF
\`\`\`

#### Method 2: Environment Variables

\`\`\`bash
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
export AWS_DEFAULT_REGION=us-east-1  # Optional
\`\`\`

**Verification**:
\`\`\`bash
# Verify authentication with AWS CLI (boto3 uses the same credentials)
aws sts get-caller-identity
\`\`\`

---

### GCP Authentication Setup

#### Creating Service Account Key

1. Create service account in GCP Console
2. Download key (JSON)
3. Set environment variable

\`\`\`bash
# Set service account key path
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"

# Make it persistent (add to .bashrc or .zshrc)
echo 'export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"' >> ~/.bashrc
\`\`\`

**Verification**:
\`\`\`bash
# Verify authentication with gcloud
gcloud auth list
\`\`\`

---

### Azure Authentication Setup

#### Method 1: Azure CLI (Recommended)

\`\`\`bash
# Login with Azure CLI
az login

# Verify subscription
az account show
\`\`\`

#### Method 2: Service Principal (Environment Variables)

\`\`\`bash
export AZURE_SUBSCRIPTION_ID=your_subscription_id
export AZURE_CLIENT_ID=your_client_id
export AZURE_CLIENT_SECRET=your_client_secret
export AZURE_TENANT_ID=your_tenant_id
\`\`\`

**Verification**:
\`\`\`bash
# List Azure resource groups
az group list
\`\`\`

---

## **🧪 Setup Verification**

### Verification Commands

\`\`\`bash
# Display CLI help
python -m src.cli.main --help

# Run tests
pytest

# Run tests with verbose output
pytest -v

# Run tests with coverage
pytest --cov=src tests/
\`\`\`

**Expected Output Example**:
\`\`\`
======================== test session starts ========================
collected X items

tests/test_main.py::test_example PASSED                        [100%]

======================== X passed in 0.XXs =========================
\`\`\`

---

## **🛠️ Development Tools Usage**

### Code Formatting (Black)

\`\`\`bash
# Format src/ and tests/
black src/ tests/

# Dry run (check changes only)
black --check src/ tests/
\`\`\`

### Linting (Ruff)

\`\`\`bash
# Run linter
ruff check src/ tests/

# Auto-fix
ruff check --fix src/ tests/
\`\`\`

### Type Checking (mypy)

\`\`\`bash
# Run type checker
mypy src/
\`\`\`

---

## **📝 Frequently Used Commands**

| Purpose | Command |
|---------|---------|
| CLI Help | \`python -m src.cli.main --help\` |
| List Services | \`python -m src.cli.main list-services\` |
| Run All Tests | \`pytest\` |
| Run Tests (Verbose) | \`pytest -v\` |
| Coverage | \`pytest --cov=src\` |
| Code Formatting | \`black src/ tests/\` |
| Linting | \`ruff check src/\` |
| Type Checking | \`mypy src/\` |

---

## **🔧 Troubleshooting**

### Issue: Python not found
\`\`\`bash
# Solution: Manually activate virtual environment
source /opt/venv/bin/activate
\`\`\`

### Issue: Dependency errors
\`\`\`bash
# Solution: Reinstall requirements.txt
pip install --upgrade -r requirements.txt
\`\`\`

### Issue: AWS authentication error
\`\`\`bash
# Solution: Verify credentials file
cat ~/.aws/credentials

# Or check environment variables
echo $AWS_ACCESS_KEY_ID
\`\`\`

### Issue: Tests failing
\`\`\`bash
# Solution: Run tests in verbose mode
pytest -vv --tb=short

# Run specific test only
pytest tests/test_main.py::test_specific_function -v
\`\`\`

---

**Last Updated**: 2026-03-05  
**Next Document**: [05_DEVELOPMENT_CHECKLIST.md](05_DEVELOPMENT_CHECKLIST.md)
