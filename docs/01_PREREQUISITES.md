# Prerequisites and Constraints

> **⚠️ READ THIS FIRST - CRITICAL**  
> This document contains the fundamental prerequisites, technical constraints, and critical design decisions for the entire project.

---

## **📋 Document Metadata**

- **Purpose**: Define project fundamentals, technical constraints, and critical decisions
- **Audience**: AI Agents, New Developers, Project Reviewers
- **Prerequisites**: Basic knowledge of Python and Cloud Services (AWS/GCP/Azure)
- **Last Updated**: 2026-03-05

---

## **🎯 Project Overview**

### Project Name
**Cloud Service Manager**

### Project Purpose
Develop a CLI tool to discover and manage resources across multiple cloud providers (AWS, GCP, Azure) with a unified interface

### Current Phase
**Phase 1: CLI Development** - Command-line tool implementation

### Future Vision
**Phase 2: Web Application** - Expand to FastAPI-based web application (NOT to be implemented currently)

---

## **🔧 Technology Stack (Confirmed)**

### Programming Language
- **Python 3.11+** (Required)
  - Reason: Improved type hints, performance enhancements, latest language features

### Frameworks & Libraries
| Category | Selected Technology | Reason |
|---------|---------------------|---------|
| **CLI Framework** | Typer | Modern, type-safe, automatic documentation generation |
| **AWS SDK** | boto3 | Official AWS SDK, comprehensive service support |
| **GCP SDK** | google-cloud-compute | Official GCP SDK |
| **Azure SDK** | azure-mgmt-compute | Official Azure SDK |
| **Table Display** | rich | Beautiful CLI output, table formatting |
| **Testing Framework** | pytest | Python standard, rich plugin ecosystem |

### Development Environment
- **Docker + DevContainer**: Unified development environment, reproducibility
- **OS**: Debian GNU/Linux 13 (trixie) on DevContainer
- **Virtual Environment**: Use Python virtual environment at `/opt/venv`

---

## **📐 Architecture Constraints**

### Directory Structure (Fixed)
\`\`\`
/workspaces/CloudServiceManager/
├── docs/                    # Documentation (English, for AI agents)
├── docs_ja/                 # Documentation (Japanese, for humans)
├── src/
│   └── cli/
│       ├── main.py         # CLI entry point
│       ├── providers/      # Cloud provider implementations
│       │   ├── aws.py
│       │   ├── gcp.py
│       │   └── azure.py
│       └── models/         # Data models
│           └── service.py
├── tests/                  # Test code
├── config.py               # Configuration file
├── requirements.txt        # Python dependencies
└── pytest.ini             # pytest configuration
\`\`\`

### Module Organization
- **providers package**: Separate implementation for each cloud provider
- **models package**: Data classes, Pydantic models
- **main.py**: CLI command definitions (Typer application)

---

## **🚫 Technical Constraints**

### Mandatory Requirements
1. **Use Python 3.11 or later**
2. **Write type hints for ALL functions and methods**
3. **Build CLI using Typer**
4. **Separate each provider implementation under \`providers/\`**
5. **Add unit tests for all new features**

### Prohibited Practices
1. **DO NOT implement Phase 2 (Web Application) features**
2. **DO NOT add dependencies on external API services (use SDKs only)**
3. **Avoid using global variables**
4. **NEVER hardcode credentials in code**

### Coding Standards
- **Code Formatting**: Black (automatic formatting)
- **Linter**: Ruff or Flake8
- **Type Checker**: mypy (recommended)
- **Docstrings**: Google Style or NumPy Style

---

## **🔐 Authentication & Security Policy**

### Cloud Provider Authentication Methods
| Provider | Authentication Method |
|----------|----------------------|
| **AWS** | \`~/.aws/credentials\` or environment variables (\`AWS_ACCESS_KEY_ID\`, \`AWS_SECRET_ACCESS_KEY\`) |
| **GCP** | Service account JSON + environment variable (\`GOOGLE_APPLICATION_CREDENTIALS\`) |
| **Azure** | Azure CLI (\`az login\`) or environment variables (\`AZURE_SUBSCRIPTION_ID\`, etc.) |

### Security Requirements
- **Load credentials from environment variables or standard credential files**
- **DO NOT output credentials in logs**
- **Exclude credential files in \`.gitignore\`**
### Authentication Request Rule (MANDATORY)
When authentication is required for cloud providers or GitHub operations:

1. **MUST REQUEST authentication credentials** from user:
   - Do NOT attempt to bypass authentication
   - Do NOT use placeholder/dummy credentials
   - Do NOT hardcode default credentials
   - Do NOT make assumptions about credentials

2. **Required credentials include**:
   - Cloud provider credentials (AWS, GCP, Azure)
   - GitHub authentication (Personal Access Token or OAuth)
   - Any service-specific API keys or secrets

3. **Process when authentication is needed**:
   - Stop execution and clearly request credentials
   - Specify which service needs authentication
   - Provide setup instructions if credentials are not available
   - Wait for user to provide authentic credentials

**Rule**: \"If authentication is needed, always request it explicitly. Never attempt workarounds or substitute authentication.\"
---

## **📊 Data Model Specification**

### CloudService Model (Standardized Service Representation)
Map all cloud provider resources to this unified model:

\`\`\`python
@dataclass
class CloudService:
    provider: str        # "aws" | "gcp" | "azure"
    service_type: str    # "EC2", "Compute Engine", "Virtual Machine", etc.
    name: str            # Resource name or ID
    region: str          # Region name
    status: str          # Status (provider-specific)
    created_at: str      # Creation datetime (ISO 8601 format)
    metadata: dict       # Provider-specific additional information
\`\`\`

### Output Formats
- **table**: Default, using Rich library for readable tables
- **json**: JSON array format
- **csv**: CSV format (with headers)

---

## **🧪 Testing Policy**

### Testing Requirements
- **Add unit tests for all provider implementations**
- **Use mocks to simulate external API calls**
- **Coverage target: 80%+ (recommended)**

### Test Execution Commands
\`\`\`bash
pytest                    # Run all tests
pytest --cov=src         # With coverage report
pytest -v                # Verbose output
pytest -k "aws"          # Run specific tests only
\`\`\`

---

## **⚙️ Development Workflow**

### New Feature Development Procedure
1. Check constraints in \`01_PREREQUISITES.md\` (this file)
2. Review architecture in \`02_PROJECT_PLAN.md\`
3. Check specifications in \`03_API_DESIGN.md\`
4. Implement (including type hints and docstrings)
5. Create unit tests
6. Run \`pytest\`
7. **Update documentation** (see Documentation Policy below)
8. Update `05_DEVELOPMENT_CHECKLIST.md`

### Documentation Update Requirement
**CRITICAL**: After completing ANY work, you MUST update documentation:
- ✅ Update relevant technical documentation in `/docs` (English)
- ✅ Update corresponding documentation in `/docs_ja` (Japanese)
- ✅ Update `05_DEVELOPMENT_CHECKLIST.md` to reflect progress
- ✅ If adding new features, update `03_API_DESIGN.md`
- ✅ If changing architecture, update `02_PROJECT_PLAN.md`

### Code Change Checklist
- [ ] Added type hints?
- [ ] Written docstrings?
- [ ] Added unit tests?
- [ ] Does \`pytest\` pass?
- [ ] No hardcoded credentials?
- [ ] Updated documentation?
### External Command Execution Rules
**MANDATORY when executing external commands (CLI tools, APIs, etc.):**

1. **Always check usage first**:
   - Run `command --help` or `command -h` before executing
   - Read official documentation if available
   - Verify required arguments and options

2. **When usage errors occur**:
   - If a command fails due to incorrect usage
   - After correcting and successfully executing
   - **MUST document the correct usage** in one of:
     - Code comments (for commands in scripts)
     - `04_SETUP.md` (for setup/environment commands)
     - `05_DEVELOPMENT_CHECKLIST.md` (for development commands)
     - Relevant technical documentation

3. **Documentation format for commands**:
   ```markdown
   ### Command: <command-name>
   **Purpose**: Brief description
   **Usage**: 
   ```bash
   command [OPTIONS] [ARGUMENTS]
   ```
   **Example**:
   ```bash
   actual-working-command --option value
   ```
   **Notes**: Any important notes or common pitfalls
   ```

**Rule**: "Learn from mistakes - document corrected commands for future reference."
### Command Not Found Rule (MANDATORY)
When a command is required for execution but not found:

1. **MUST INSTALL the command**:
   - Do NOT skip the command because it's missing
   - Do NOT look for alternative commands
   - Do NOT attempt workarounds

2. **Installation process**:
   - Identify the correct package name for the command
   - Install using appropriate package manager:
     - Linux (Debian/Ubuntu): `apt-get update && apt-get install -y package-name`
     - Linux (Fedora/RHEL): `yum install -y package-name`
     - macOS: `brew install package-name`
     - Other: Use appropriate system package manager
   - Verify installation: `which command-name` or `command-name --version`
   - Proceed with original operation after successful installation

3. **Documentation requirement**:
   - After installing a missing command, document it:
     - Add installation instruction to `04_SETUP.md`
     - Include command name and installation method
     - Add verification step
     - Update in both English and Japanese versions

4. **Examples of scenarios**:
   - `git` command not found → Install git
   - `docker` command not found → Install docker
   - `python` command not found → Install python
   - `curl` command not found → Install curl

**Rule**: \"If a command is needed, install it. Never skip or find alternatives.\"

### Directory Operation Rule (MANDATORY)
When performing operations on directories:

1. **MUST VERIFY directory structure before operations**:
   - List the target directory: `ls -la <target-directory>`
   - Display current working directory: `pwd`
   - Verify the exact path before performing operations
   - Understand the directory hierarchy and contents

2. **Directory verification checklist**:
   - ✅ Is the path correct and absolute or relative as intended?
   - ✅ Does the directory exist?
   - ✅ Are the expected files/subdirectories present?
   - ✅ Do you have appropriate permissions?
   - ✅ Is this the intended directory (not a similarly named one)?

3. **Before destructive operations**:
   - **ALWAYS** list directory contents first: `ls -R <target-directory>`
   - **ALWAYS** verify you're in/targeting the correct location
   - **ALWAYS** confirm file/directory names match expectations
   - **NEVER** perform delete/remove operations without verification

4. **Common verification commands**:
   ```bash
   pwd                          # Show current directory
   ls -la <directory>           # List directory contents with details
   find <directory> -type f     # Find all files in directory
   tree <directory>             # Show directory tree (if installed)
   stat <directory>             # Show directory information
   ```

5. **Example workflow**:
   ```bash
   # Before deleting a directory:
   pwd                          # Verify current location
   ls -la /path/to/delete       # View contents first
   ls -la /path/to/delete/*     # See what's inside
   # THEN proceed with deletion only if confirmed
   rm -rf /path/to/delete
   ```

**Rule**: \"Always verify directory structure before operations. One confirmation prevents one mistake.\"

---

## **📦 Dependency Management**

### requirements.txt
All dependencies are managed in \`requirements.txt\`:

\`\`\`text
typer[all]          # CLI framework
boto3               # AWS SDK
google-cloud-compute # GCP SDK
azure-mgmt-compute  # Azure SDK
rich                # CLI output
pydantic            # Data validation
pytest              # Testing framework
pytest-cov          # Coverage measurement
\`\`\`

### Adding New Dependencies
1. Add to \`requirements.txt\`
2. Reinstall with \`pip install -r requirements.txt\`
3. Update documentation (this file)

---

## **🔄 Version Control**

### Git Workflow

#### Branch Strategy
- **`main` branch**: Production-ready code only
  - Stable, tested releases
  - QA-verified and production-ready
  - Protected branch (no direct commits)
  
- **`develop` branch**: Development integration branch
  - Latest development changes
  - Integration point for all features
  - Must be stable and tested
  - Protected branch (merge via PR only)

- **Feature/Fix branches**: Development work branches
  - Format: `feature/feature-name` or `bugfix/bug-name`
  - Created from: `develop` branch
  - Merged back to: `develop` branch
  - Deleted after successful merge

#### Development Workflow (MANDATORY)

1. **Start new work**:
   - Create feature/bugfix branch from `develop`
   - Branch naming: `feature/descriptive-name` or `bugfix/issue-number`
   - Example: `feature/list-services-gcp`, `bugfix/aws-auth-error`

2. **During development**:
   - Keep commits atomic and well-described
   - Commit frequently with clear messages
   - All tests must pass before committing

3. **Complete work**:
   - Ensure all tests pass locally: `pytest`
   - Push branch to remote
   - Create Pull Request (PR) to `develop`
   - Address code review feedback

4. **Merge to develop**:
   - PR must be approved by at least one reviewer
   - All CI/CD checks must pass
   - Squash commits if desired for cleaner history
   - Delete feature branch after merge

5. **Release to main**:
   - Only merge `develop` → `main` for releases
   - Verify all tests pass in `develop`
   - Create release PR from `develop` to `main`
   - Tag release with version number (e.g., `v1.0.0`)
   - Create release notes

#### Commit Message Standards
- **Format**: `Type: Brief description`
- **Types**: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`
- **Examples**:
  - `feat: add GCP provider support`
  - `fix: resolve AWS authentication timeout`
  - `docs: update API design specifications`
  - `test: add unit tests for Azure provider`

#### QA/Testing Requirements (MANDATORY)

Before merging to `develop` or `main`:
- ✅ All unit tests pass: `pytest --cov=src`
- ✅ Code coverage maintained above 80%
- ✅ No hardcoded credentials
- ✅ Type hints on all new functions
- ✅ Docstrings for all public methods
- ✅ Documentation updated (see Documentation Policy)
- ✅ Linting passes: `ruff check src/`
- ✅ Code formatted: `black src/`

Before merging to `main`:
- ✅ `develop` branch is fully tested and stable
- ✅ No outstanding issues blocking the release
- ✅ Release notes prepared
- ✅ Version number updated

#### Rule Summary
> "Never commit directly to main or develop. Always work on feature branches from develop. Verify quality before merging to develop, stability before releasing to main."

### Versioning Strategy

#### Version Numbering Format
**Format**: `W.X.Y.Z` (Starting from `1.0.0.0`)

#### Version Increment Rules

| Component | When to Increment | Trigger | Example |
|-----------|------------------|---------|----------|
| **W** (Major) | When user provides new major instructions/requirements | User request/direction | `1.5.10.15` → `2.0.10.15` |
| **X** (Minor) | When user provides new feature/refinement instructions | User request/direction | `1.0.5.10` → `1.1.5.10` |
| **Y** (Development) | When pushing changes to `develop` branch | `git push origin develop` | `1.0.5.10` → `1.0.6.10` |
| **Z** (Commit) | When creating a new commit | `git commit ...` | `1.0.5.10` → `1.0.5.11` |

#### Versioning Rules (MANDATORY)

1. **Starting Version**: `1.0.0.0` (Project initiation)

2. **Major Version (W) Increment**:
   - Triggered by user providing major new instructions or fundamental changes
   - Examples: Phase transition, major architecture redesign, complete feature set redesign
   - Increments W and resets X to 0 (e.g., `1.15.10.7` → `2.0.10.7`)
   - Y and Z continue incrementing independently

3. **Minor Version (X) Increment**:
   - Triggered by user providing new feature instructions or significant refinements
   - Examples: New CLI command, new provider support, new workflow
   - Increments only X (e.g., `1.0.5.3` → `1.1.5.3`)
   - Y and Z continue incrementing independently

4. **Development Version (Y) Increment**:
   - Incremented EACH TIME changes are pushed to `develop` branch
   - Applied after successful pull request merge to `develop`
   - Indicates development cycle progress
   - Z continues incrementing independently (e.g., `1.0.0.5` → `1.0.1.5`)

5. **Commit Version (Z) Increment**:
   - Incremented EACH TIME a new commit is created
   - Applied immediately when: `git commit ...` is executed
   - Tracks granular development progress
   - Continues incrementing without reset (e.g., `1.0.0.5` → `1.0.0.6`)

#### Version Management in Code

1. **Store version in**: `config.py`
   ```python
   VERSION = "1.0.0.0"
   ```

2. **Update version in commits**:
   - Before committing code, update VERSION in `config.py`
   - Increment Z component
   - Include version update in commit message: `chore: bump version to 1.0.0.X`

3. **Update version on develop pushes**:
   - After merging PR to `develop`, increment Y component
   - Create separate commit: `chore: bump dev version to 1.0.X.0`
   - Update `05_DEVELOPMENT_CHECKLIST.md` with current version
   - Z continues incrementing normally with subsequent commits

4. **Major/Minor updates**:
   - When user provides instructions incrementing W or X
   - Create commit with version update immediately
   - Update `05_DEVELOPMENT_CHECKLIST.md` and all documentation

#### Version Display in CLI

- Display version with: `python -m src.cli.main --version`
- Implement in main.py:
  ```python
  from config import VERSION
  
  @app.command()
  def version():
      """Display application version."""
      print(f"Cloud Service Manager v{VERSION}")
  ```

#### Rule Summary
> \"Version numbering reflects development pace: W increments reset X to 0, X increments independently, Y tracks development integration cycles independently, and Z tracks every atomic commit independently. Version must always be current in code.\"

### GitHub Features Usage (MANDATORY)

**Actively leverage GitHub features for project management and collaboration:**

1. **Issues for Tracking**:
   - Use GitHub Issues for bug reports, feature requests, and tasks
   - Label issues appropriately (`bug`, `enhancement`, `documentation`, etc.)
   - Assign issues to team members
   - Link issues to PRs: `Closes #123`
   - Update issue status and progress regularly

2. **Pull Requests for Code Review**:
   - **ALWAYS** use PRs for code changes (never commit directly to `main` or `develop`)
   - Write clear PR descriptions with purpose and changes
   - Link related issues: `Fixes #123` or `Relates to #456`
   - Request reviewers and address feedback
   - Enable PR status checks and require all checks to pass

3. **Discussions for Planning**:
   - Use GitHub Discussions for design decisions
   - Document architectural choices
   - Record problem-solving approaches
   - Share knowledge and lessons learned

4. **Project Boards for Organization**:
   - Create GitHub Projects board to track workflow
   - Organize issues into: `To Do`, `In Progress`, `In Review`, `Done`
   - Use automation with labels to update board status
   - Link PRs to project items

5. **Milestones for Release Planning**:
   - Group related issues and PRs into milestones for releases
   - Set due dates for major features/versions
   - Track progress toward release goals
   - Create milestones: `v1.0`, `v1.1`, etc.

6. **Tags and Releases**:
   - Create git tags for releases: `git tag -a v1.0.0 -m "Release version 1.0.0"`
   - Create GitHub Releases with release notes
   - Include changelog of features, fixes, and improvements
   - Attach release artifacts if applicable

7. **GitHub Actions for CI/CD**:
   - Set up automated testing on every PR
   - Run linting, type checking, and code formatting checks
   - Validate that all tests pass before allowing merges
   - Automate deployment processes

8. **Wiki and Documentation**:
   - Use GitHub Wiki for project documentation
   - Maintain setup guides and architecture documentation
   - Document common workflows and troubleshooting
   - Keep Wiki in sync with `docs/` folder

**Rule**: \"GitHub is not just for code storage; it's a platform for project management. Actively use its features to organize work, track progress, and document decisions.\"

### Project Management with GitHub (MANDATORY)

**Use GitHub features to manage project progress, tasks, and timelines:**

1. **Issues as Task Management**:
   - Create issues for **every** task, bug, and feature request
   - Use descriptive titles and detailed descriptions
   - **Add labels** for categorization: `bug`, `enhancement`, `documentation`, `high-priority`, `blocked`, etc.
   - **Estimate effort** using custom fields or issue templates
   - Break down large issues into smaller subtasks using task lists:
     ```markdown
     - [ ] Subtask 1
     - [ ] Subtask 2
     - [ ] Subtask 3
     ```
   - Link related issues with `Relates to #123` or `Duplicates #456`
   - Close issues only when work is **completely verified**

2. **Milestones for Time-Based Planning**:
   - Create milestones for each planned release: `v1.0.0`, `v1.1.0`, etc.
   - Set **realistic due dates** for milestones
   - Assign issues to appropriate milestones before starting work
   - Track progress toward milestone completion
   - Close milestones only when all issues are resolved and tested

3. **GitHub Projects for Workflow Visualization**:
   - Create a **single project board** for active development
   - Use standard columns: `Backlog` → `To Do` → `In Progress` → `In Review` → `Done`
   - **Automatically** add new issues to backlog
   - Move issues through columns as work progresses
   - Use automation rules:
     - Move to "In Progress" when PR is opened
     - Move to "In Review" when PR is marked ready for review
     - Move to "Done" when PR is merged
   - Review board status in daily/weekly standups

4. **Issue Templates for Consistency**:
   - Create issue templates in `.github/ISSUE_TEMPLATE/`:
     - `bug_report.md` - For bug reports
     - `feature_request.md` - For feature requests
     - `task.md` - For general tasks
   - Templates should include:
     - Clear description sections
     - Reproduction steps (for bugs)
     - Acceptance criteria (for features)
     - Labels to apply
     - Assignee suggestions

5. **Blocking and Dependencies**:
   - Use links to indicate blocked issues: `blocks #123` or `blocked by #456`
   - Prevent merging PRs for blocked features
   - Document why issues are blocked
   - Regularly review and unblock issues

6. **Progress Reports**:
   - Review project board **weekly**
   - Generate progress reports from completed issues
   - Track velocity: issues completed per week/sprint
   - Identify bottlenecks and blocked issues
   - Update stakeholders with milestone progress

7. **Backlog Grooming (Regular)**:
   - Review unassigned issues weekly
   - Estimate effort for new issues
   - Prioritize issues based on impact and dependencies
   - Remove or merge duplicate issues
   - Archive resolved/outdated issues

8. **Integration with Development**:
   - Link every PR to related issues
   - Use PR descriptions to reference issues: `Closes #123`
   - Require issues for all code changes (no untracked work)
   - Reference issues in commit messages when relevant
   - Update issues with progress comments

**Rule**: \"Every piece of work should be tracked in GitHub Issues. If it's not tracked, it doesn't exist from the project management perspective.\"

---

## **📝 Documentation Policy**

### Language Rules (MANDATORY)
- **`/docs`**: All documentation MUST be in **English** (optimized for AI agents to understand)
- **`/docs_ja`**: All documentation MUST be in **Japanese** (for human developers)
- **NO mixing**: Do NOT mix languages within a single document
- **Synchronization**: When updating documentation, BOTH English and Japanese versions MUST be updated
- **Consistency**: Maintain consistent structure and content between English and Japanese versions

### When to Update Documentation (MANDATORY)
**You MUST update documentation whenever you complete ANY of the following:**
- ✅ Implement a new feature
- ✅ Fix a bug
- ✅ Change architecture or design
- ✅ Modify API or CLI interface
- ✅ Update dependencies
- ✅ Change development workflow
- ✅ Complete a development milestone

**Rule**: "No work is complete until documentation is updated."

### Documentation Update Process
1. **Identify** which documents need updating
2. **Update English version** in `/docs` first
3. **Update Japanese version** in `/docs_ja` immediately after
4. **Verify** both versions have the same structure and information
5. **Update "Last Updated"** date in both versions
6. **Test** that all links and references work correctly

---

## **❓ When Unclear**

1. Re-read this file (\`01_PREREQUISITES.md\`)
2. Refer to related documents (\`02_PROJECT_PLAN.md\`, \`03_API_DESIGN.md\`)
3. Check existing code (\`src/cli/\`)
4. If still unclear, ASK instead of guessing

---

**Last Updated**: 2026-03-05  
**Review Required**: When tech stack changes, when new constraints are added
