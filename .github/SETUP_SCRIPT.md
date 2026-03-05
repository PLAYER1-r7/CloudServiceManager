# GitHub Automatic Setup Script

Automated script to configure all GitHub repository settings without manual UI interaction.

## What This Script Does

- ✅ Creates 8 GitHub Labels (bug, enhancement, documentation, task, high-priority, blocked, in-progress, needs-review)
- ✅ Creates 3 Milestones (v1.0.0, v1.1.0, v2.0.0)
- ✅ Creates GitHub Project board "Development Tracking"
- ✅ Configures branch protection for `develop` and `main` branches
- ✅ Creates the first GitHub Issue with all required subtasks
- ✅ Sets up proper labels and milestone linking

## Prerequisites

1. **Python 3.8+** installed
2. **GitHub CLI (`gh`)** - **REQUIRED** ✨
   - Personal Access Tokens (PAT) are **FORBIDDEN** by project policy
   - See `docs/01_PREREQUISITES.md` - "GitHub Authentication Rule (MANDATORY)"
   - Only exception: GitHub Actions built-in `GITHUB_TOKEN` for CI/CD

3. **Required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Git repository already created** on GitHub

---

## Authentication Methods

### Method 1: GitHub CLI (Recommended) ✨

**Why use GitHub CLI?**
- ✅ No need to create or manage tokens manually
- ✅ Automatic authentication via OAuth
- ✅ Tokens are stored securely by GitHub CLI
- ✅ Works across all repositories

**Installation:**

```bash
# macOS (Homebrew)
brew install gh

# Linux (Debian/Ubuntu)
sudo apt install gh

# Linux (Other)
# See: https://github.com/cli/cli/blob/trunk/docs/install_linux.md

# Windows
# Download from: https://cli.github.com/
```

**Setup:**

```bash
# 1. Login to GitHub
gh auth login

# Follow the interactive prompts:
# - Select: GitHub.com
# - Protocol: HTTPS (recommended)
# - Authentication: Login with a web browser

# 2. Verify authentication
gh auth status

# 3. Run the setup script
cd /workspaces/CloudServiceManager
python .github/setup_github.py
```

The script will automatically:
- ✅ Detect GitHub CLI authentication
- ✅ Retrieve token from `gh`
- ✅ Auto-detect repository from git remote
- ✅ Run setup without any prompts

---

### Method 2: Fine-grained Personal Access Token ⚠️ FORBIDDEN BY PROJECT POLICY

**⚠️ THIS METHOD IS NOT PERMITTED IN THIS PROJECT**

Per `docs/01_PREREQUISITES.md` - "GitHub Authentication Rule (MANDATORY)":
- ❌ Personal Access Tokens (Fine-grained) are **FORBIDDEN**
- ✅ Use GitHub CLI (`gh`) instead
- Only exception: GitHub Actions built-in token for CI/CD

**How to create:**

1. Go to **https://github.com/settings/tokens?type=beta**
2. Click **"Generate new token"**
3. **Token name**: `CloudServiceManager Setup`
4. **Expiration**: `7 days` (recommended for one-time setup)
5. **Repository access**: 
   - Select **"Only select repositories"**
   - Choose your `CloudServiceManager` repository
6. **Permissions** - Select these repository permissions:
   - ☑️ **Contents**: Read and write
   - ☑️ **Issues**: Read and write
   - ☑️ **Metadata**: Read-only (auto-selected)
   - ☑️ **Pull requests**: Read and write
   - ☑️ **Administration**: Read and write (for branch protection)
   - ☑️ **Projects**: Read and write (for project boards)
7. Click **"Generate token"**
8. **Copy the token** (starts with `github_pat_`)

**Usage:**

```bash
export GITHUB_TOKEN="github_pat_xxxxxxxxxxxx"
export GITHUB_OWNER="your_username"
export GITHUB_REPO="CloudServiceManager"

python .github/setup_github.py
```

---

### Method 3: Classic Personal Access Token ⚠️ FORBIDDEN BY PROJECT POLICY

**⚠️ THIS METHOD IS NOT PERMITTED IN THIS PROJECT**

Per `docs/01_PREREQUISITES.md` - "GitHub Authentication Rule (MANDATORY)":
- ❌ Personal Access Tokens (Classic) are **STRICTLY FORBIDDEN**
- ✅ Use GitHub CLI (`gh`) instead

<details>
<summary>Historical reference only (DO NOT USE)</summary>

**Only if you cannot use GitHub CLI or Fine-grained PAT:**

1. Go to **https://github.com/settings/tokens/new**
2. **Note**: `CloudServiceManager Setup`
3. **Expiration**: `7 days`
4. **Select scopes**:
   - ☑️ `repo` (Full control of private repositories)
   - ☑️ `admin:repo_hook` (Write access to hooks)
   - ☑️ `project` (Read/write access to projects)
5. Click **"Generate token"**
6. Copy the token (starts with `ghp_`)

**Usage:**

```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
python .github/setup_github.py
```

</details>

---

## Usage Examples

### Example 1: Using GitHub CLI (Simplest)

```bash
# One-time setup
gh auth login

# Run the script
cd /workspaces/CloudServiceManager
python .github/setup_github.py
```

Output:
```
============================================================
🚀 GitHub Repository Automatic Setup
============================================================

🔐 Checking authentication methods...
✓ Found GitHub CLI authentication
✓ Successfully retrieved token from GitHub CLI
✓ Auto-detected repository: myusername/CloudServiceManager

✓ Authenticated as: myusername
✓ Repository: myusername/CloudServiceManager

📋 Creating labels...
  ✅ Created label: bug
  ...
```

### Example 2: Using Fine-grained PAT

```bash
export GITHUB_TOKEN="github_pat_11ABCD...XYZ"
export GITHUB_OWNER="myusername"
export GITHUB_REPO="CloudServiceManager"

python .github/setup_github.py
```

### Example 3: Interactive Mode

```bash
# Just run the script - it will guide you
python .github/setup_github.py

# The script will prompt:
# - Authentication method selection
# - Repository owner
# - Repository name
```

### Example 4: From Development Container

```bash
# Inside VS Code dev container
cd /workspaces/CloudServiceManager

# If GitHub CLI is installed in container:
gh auth login
python .github/setup_github.py

# Or use environment variables:
export GITHUB_TOKEN="github_pat_xxxx"
export GITHUB_OWNER="myusername"
export GITHUB_REPO="CloudServiceManager"
python .github/setup_github.py
```

## Script Output Example

### Using GitHub CLI (Recommended)

```
============================================================
🚀 GitHub Repository Automatic Setup
============================================================

🔐 Checking authentication methods...
✓ Found GitHub CLI authentication
✓ Successfully retrieved token from GitHub CLI
✓ Auto-detected repository: myusername/CloudServiceManager

✓ Authenticated as: myusername
✓ Repository: myusername/CloudServiceManager

📋 Creating labels...
  ✅ Created label: bug
  ✅ Created label: enhancement
  ✅ Created label: documentation
  ✅ Created label: task
  ✅ Created label: high-priority
  ✅ Created label: blocked
  ✅ Created label: in-progress
  ✅ Created label: needs-review

📅 Creating milestones...
  ✅ Created milestone: v1.0.0
  ✅ Created milestone: v1.1.0
  ✅ Created milestone: v2.0.0

📊 Creating GitHub Project board...
  ✅ Created GitHub Project: Development Tracking

🔒 Configuring branch protection...
  ✅ Configured protection for: develop
  ✅ Configured protection for: main

📝 Creating first GitHub Issue...
  ✅ Created first issue: https://github.com/myusername/CloudServiceManager/issues/1

============================================================
✅ GitHub Setup Complete!
============================================================

📦 Repository: myusername/CloudServiceManager
🔗 URL: https://github.com/myusername/CloudServiceManager

✓ Labels created: 8
✓ Milestones created: 3
✓ Project board: Development Tracking
✓ Branch protection: develop, main

📋 Next Steps:
1. Verify labels in Issues → Labels
2. Check milestones in Issues → Milestones
3. View project at Projects tab
4. Confirm branch protection in Settings → Branches
5. See first issue: #1

============================================================
```

### Using Fine-grained PAT

```
============================================================
🚀 GitHub Repository Automatic Setup
============================================================

🔐 Checking authentication methods...
ℹ️  GitHub CLI not found or not authenticated
   Install: https://cli.github.com/
   Or use a Personal Access Token instead
✓ Found GITHUB_TOKEN environment variable
  Token type: Fine-grained

✓ Auto-detected from git: myusername/CloudServiceManager

✓ Authenticated as: myusername
✓ Repository: myusername/CloudServiceManager

📋 Creating labels...
  ✅ Created label: bug
  ✅ Created label: enhancement
  ✅ Created milestone: v2.0.0

📊 Creating GitHub Project board...
  ✅ Created GitHub Project: Development Tracking

🔒 Configuring branch protection...
  ✅ Configured protection for: develop
  ✅ Configured protection for: main

📝 Creating first GitHub Issue...
  ✅ Created first issue: https://github.com/myusername/CloudServiceManager/issues/1

============================================================
✅ GitHub Setup Complete!
============================================================

📦 Repository: myusername/CloudServiceManager
🔗 URL: https://github.com/myusername/CloudServiceManager

✓ Labels created: 8
✓ Milestones created: 3
✓ Project board: Development Tracking
✓ Branch protection: develop, main

📋 Next Steps:
1. Verify labels in Issues → Labels
2. Check milestones in Issues → Milestones
3. View project at Projects tab
4. Confirm branch protection in Settings → Branches
5. See first issue: #1

============================================================
```

## Troubleshooting

### GitHub CLI Issues

#### "GitHub CLI not found"

```
ℹ️  GitHub CLI not found or not authenticated
   Install: https://cli.github.com/
```

**Solution**: Install GitHub CLI:

```bash
# macOS
brew install gh

# Linux (Debian/Ubuntu)
sudo apt install gh

# Or download from: https://cli.github.com/
```

#### "Not authenticated"

```bash
# Login to GitHub
gh auth login

# Verify authentication
gh auth status
```

Should show:
```
✓ Logged in to github.com as YOUR_USERNAME (/path/to/.config/gh/hosts.yml)
✓ Git operations for github.com configured to use https protocol.
✓ Token: gho_************************************
```

### Token Authentication Issues

#### "401 Unauthorized" Error

```
❌ GitHub API error: 401
   Check your personal access token
```

**Solution**: Verify your personal access token is correct and has not expired.

### "404 Not Found" Error

```
❌ GitHub API error: 404
   Check that owner and repository name are correct
```

**Solution**: Ensure:
- Repository exists on GitHub
- Owner username is correct (not display name)
- Repository name is exact (case-sensitive)

### "Branch does not exist" Warning

```
⚠️  Branch does not exist: develop
```

**Solution**: Create the branch manually first:

```bash
git checkout -b develop
git push -u origin develop
```

### Token Scope Issues

#### Fine-grained PAT - Missing Permissions

```
❌ GitHub API error: 403 Resource not accessible by personal access token
```

**Solution**: Verify your Fine-grained PAT has these **Repository permissions**:

Required permissions:
- ☑️ **Administration**: Read and write (for branch protection)
- ☑️ **Contents**: Read and write (for repository access)
- ☑️ **Issues**: Read and write (for creating issues)
- ☑️ **Metadata**: Read-only (auto-selected)
- ☑️ **Projects**: Read and write (for project boards)
- ☑️ **Pull requests**: Read and write (for PR configuration)

**How to fix:**
1. Go to https://github.com/settings/tokens?type=beta
2. Find your token and click **Edit**
3. Update **Repository permissions** with the above list
4. **Save changes**
5. Run the script again

#### Classic PAT - Missing Scopes

If using Classic PAT (not recommended), the token must have these scopes:

If you get permission errors, the token might lack required scopes:

**Solution**: Create a new token with these scopes:
- ☑️ `repo` (Full control of private repositories)
- ☑️ `admin:repo_hook` (Write access to hooks)
- ☑️ `project` (Read/write access to projects)

### Labels Already Exist

```
⚠️  Label already exists: bug
```

This is normal - the script is idempotent and won't fail if labels/milestones already exist. The "already exists" message just means the setup is partially complete.

## Script Details

### Configuration

The script defines all settings in code:

```python
LABELS = { ... }           # 8 labels to create
MILESTONES = [ ... ]       # 3 milestones
PROJECT_NAME = "..."       # Project board name
FIRST_ISSUE = { ... }      # First issue template
```

### API Methods Used

- **REST API v3** for:
  - Creating labels
  - Creating milestones
  - Creating issues
  - Branch protection
  
- **GraphQL API** for:
  - Creating GitHub Project board (Project v2)
  - Querying projects

### Idempotent Operations

The script is idempotent - it can be run multiple times safely:
- If labels exist, they're skipped
- If milestones exist, they're skipped  
- If project exists, it's found and used
- If issue exists, it's not duplicated

## Manual Verification Checklist

After running the script, verify in GitHub UI:

- [ ] **Labels** (Issues → Labels)
  - [ ] 8 labels exist with correct colors
  - [ ] Names: bug, enhancement, documentation, task, high-priority, blocked, in-progress, needs-review

- [ ] **Milestones** (Issues → Milestones)
  - [ ] v1.0.0, v1.1.0, v2.0.0 created

- [ ] **Project Board** (Projects tab)
  - [ ] "Development Tracking" project exists
  - [ ] 5 columns visible: Backlog, To Do, In Progress, In Review, Done

- [ ] **Branch Protection** (Settings → Branches)
  - [ ] `develop` branch protected with 1 approval required
  - [ ] `main` branch protected with 1 approval required

- [ ] **First Issue** (Issues tab)
  - [ ] Issue #1 exists with title "[TASK] Set Up GitHub Project Board and Initial Milestones"
  - [ ] Has labels: `task`, `high-priority`
  - [ ] Assigned to milestone v1.0.0 (optional)

## Security Notes

### Best Practices

✅ **Recommended: Use GitHub CLI**
- Tokens are managed securely by GitHub CLI
- No need to copy/paste tokens
- Automatic token rotation
- OAuth-based authentication

⚠️ **If using Fine-grained PAT:**
- Set shortest expiration needed (7 days for one-time setup)
- Use repository-specific access (not all repositories)
- Grant only required permissions
- Delete token after successful setup

❌ **Avoid Classic PATs:**
- Broad permissions across all repositories
- No automatic expiration
- Less secure than Fine-grained PATs
- GitHub plans to deprecate them

### Token Safety

- ✅ **DO**: Use environment variables (`export GITHUB_TOKEN=...`)
- ✅ **DO**: Delete tokens immediately after setup
- ✅ **DO**: Use GitHub CLI when possible
- ✅ **DO**: Rotate tokens regularly if reused
- ❌ **DON'T**: Commit tokens to git
- ❌ **DON'T**: Share tokens in chat/email
- ❌ **DON'T**: Use tokens in scripts that are committed
- ❌ **DON'T**: Grant more permissions than needed

### For CI/CD

If running this script in GitHub Actions, use the built-in `GITHUB_TOKEN`:

### For CI/CD

If running this script in GitHub Actions, use the built-in `GITHUB_TOKEN`:

```yaml
name: Setup GitHub Repository

on:
  workflow_dispatch:  # Manual trigger

jobs:
  setup:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      issues: write
      pull-requests: write
      repository-projects: write
      
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          
      - name: Run GitHub setup script
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_OWNER: ${{ github.repository_owner }}
          GITHUB_REPO: ${{ github.event.repository.name }}
        run: |
          python .github/setup_github.py
          
      - name: Verify setup
        run: |
          echo "✅ GitHub setup completed!"
          echo "Check Issues, Projects, and Settings"
```

**Note**: The built-in `${{ secrets.GITHUB_TOKEN }}` has limited permissions. For full functionality, you may need to create a GitHub App or use a Fine-grained PAT stored in Secrets.

---

**Last Updated**: 2026-03-05  
**Script Version**: 2.0.0 (with GitHub CLI support)  
**Status**: Production Ready
