#!/usr/bin/env python3
"""
GitHub Repository Automatic Setup Script

This script automates all GitHub repository configuration:
- Creates labels
- Creates milestones
- Creates GitHub Project board
- Configures branch protection rules
- Creates the first GitHub Issue

Usage:
    # REQUIRED: Use GitHub CLI (only permitted authentication method)
    gh auth login  # Login first if not authenticated
    python .github/setup_github.py

Requirements:
    - GitHub CLI (`gh`) installed and authenticated (REQUIRED)
    - See docs/01_PREREQUISITES.md - "GitHub Authentication Rule (MANDATORY)"
    
    ⚠️ FORBIDDEN: Personal Access Tokens (PAT) are NOT permitted by project policy
    - Classic PAT: ghp_xxxx - FORBIDDEN
    - Fine-grained PAT: github_pat_xxxx - FORBIDDEN
    - Exception: GitHub Actions built-in GITHUB_TOKEN for CI/CD only

Environment Variables:
    GITHUB_OWNER: Repository owner (auto-detected from git remote if available)
    GITHUB_REPO: Repository name (auto-detected from git remote if available)
    GITHUB_TOKEN: Only for GitHub Actions CI/CD (auto-provided by GitHub)
"""

import json
import os
import subprocess
import sys
from typing import Dict, List, Optional, Tuple

import requests
from github import Github
from github.GithubException import GithubException

# Configuration
LABELS = {
    "bug": {"color": "d73a49", "description": "Bug reports and issues"},
    "enhancement": {"color": "28a745", "description": "Feature requests"},
    "documentation": {"color": "0075ca", "description": "Documentation updates"},
    "task": {"color": "ffc107", "description": "General tasks and work items"},
    "high-priority": {"color": "800000", "description": "Urgent, high priority work"},
    "blocked": {"color": "ff9800", "description": "Blocked by dependencies"},
    "in-progress": {"color": "6f42c1", "description": "Currently being worked on"},
    "needs-review": {"color": "1f97c6", "description": "Awaiting review/feedback"},
}

MILESTONES = [
    {
        "title": "v1.0.0",
        "description": "Phase 1 MVP - AWS, GCP, Azure provider support",
    },
    {
        "title": "v1.1.0",
        "description": "Phase 1 enhancements - Additional features",
    },
    {
        "title": "v2.0.0",
        "description": "Phase 2 - Web application converted to FastAPI",
    },
]

PROJECT_NAME = "Development Tracking"
PROJECT_COLUMNS = ["Backlog", "To Do", "In Progress", "In Review", "Done"]

FIRST_ISSUE = {
    "title": "[TASK] Set Up GitHub Project Board and Initial Milestones",
    "body": """# GitHub Project Setup Task

Complete all GitHub repository configuration and project board setup.

## Subtasks

- [ ] Create 8 GitHub Labels (see labels table below)
- [ ] Create 3 Milestones (v1.0.0, v1.1.0, v2.0.0)
- [ ] Create GitHub Project board "Development Tracking"
- [ ] Configure branch protection for `develop` branch
- [ ] Configure branch protection for `main` branch
- [ ] Enable CI/CD workflow verification
- [ ] Create automation rules for project board
- [ ] Link initial issues to project board
- [ ] Verify all configuration is complete

## Labels Reference

| Label | Purpose |
|-------|---------|
| `bug` | Bug reports and issues |
| `enhancement` | Feature requests |
| `documentation` | Documentation updates |
| `task` | General tasks and work items |
| `high-priority` | Urgent, high priority work |
| `blocked` | Blocked by dependencies |
| `in-progress` | Currently being worked on |
| `needs-review` | Awaiting review/feedback |

## Effort Estimate

Medium (3-4 hours)

## Related Documentation

- [INITIAL_SETUP.md](.github/INITIAL_SETUP.md) - Step-by-step setup guide
- [GITHUB_SETUP.md](.github/GITHUB_SETUP.md) - Detailed configuration instructions

## Acceptance Criteria

- [x] All labels created in GitHub Issues
- [x] All milestones created 
- [x] GitHub Project board created with 5 columns
- [x] Branch protection enabled for `develop` and `main`
- [x] CI/CD status checks configured
- [x] Project automation rules enabled
- [x] First issues created and linked
- [x] Team members notified of setup completion
""",
    "labels": ["task", "high-priority"],
}


class GitHubSetup:
    """Handle GitHub repository automatic setup."""

    def __init__(self, token: str, owner: str, repo: str):
        """
        Initialize GitHub setup handler.

        Args:
            token: GitHub personal access token
            owner: Repository owner/organization
            repo: Repository name
        """
        self.token = token
        self.owner = owner
        self.repo = repo
        self.gh = Github(token)
        self.repository = self.gh.get_user(owner).get_repo(repo)
        self.api_base = "https://api.github.com"

    def create_labels(self) -> bool:
        """Create all required labels."""
        print("\n📋 Creating labels...")
        try:
            for label_name, label_info in LABELS.items():
                try:
                    self.repository.create_label(
                        name=label_name,
                        color=label_info["color"],
                        description=label_info["description"],
                    )
                    print(f"  ✅ Created label: {label_name}")
                except GithubException as e:
                    if e.status == 422:  # Label already exists
                        print(f"  ⚠️  Label already exists: {label_name}")
                    else:
                        raise
            return True
        except Exception as e:
            print(f"  ❌ Error creating labels: {e}")
            return False

    def create_milestones(self) -> bool:
        """Create all required milestones."""
        print("\n📅 Creating milestones...")
        try:
            for milestone in MILESTONES:
                try:
                    self.repository.create_milestone(
                        title=milestone["title"],
                        description=milestone["description"],
                    )
                    print(f"  ✅ Created milestone: {milestone['title']}")
                except GithubException as e:
                    if e.status == 422:  # Milestone already exists
                        print(f"  ⚠️  Milestone already exists: {milestone['title']}")
                    else:
                        raise
            return True
        except Exception as e:
            print(f"  ❌ Error creating milestones: {e}")
            return False

    def create_project_board(self) -> Optional[str]:
        """
        Create GitHub Project board using GraphQL API.

        Returns:
            Project ID if successful, None otherwise
        """
        print("\n📊 Creating GitHub Project board...")
        try:
            query = """
            mutation CreateProject($name: String!, $repositoryId: ID!) {
              createProject(input: {name: $name, repositoryId: $repositoryId}) {
                project {
                  id
                  name
                }
              }
            }
            """

            variables = {
                "name": PROJECT_NAME,
                "repositoryId": self.repository.node_id,
            }

            result = self._graphql_request(query, variables)

            if result and "createProject" in result:
                project_id = result["createProject"]["project"]["id"]
                print(f"  ✅ Created GitHub Project: {PROJECT_NAME}")
                return project_id
            else:
                print(f"  ⚠️  Project may already exist: {PROJECT_NAME}")
                # Try to find existing project
                return self._find_project_id()

        except Exception as e:
            print(f"  ❌ Error creating project: {e}")
            return None

    def _find_project_id(self) -> Optional[str]:
        """Find existing project ID by name."""
        try:
            query = """
            query GetProjects($owner: String!, $repo: String!) {
              repository(owner: $owner, name: $repo) {
                projects(first: 10) {
                  nodes {
                    id
                    name
                  }
                }
              }
            }
            """

            variables = {"owner": self.owner, "repo": self.repo}
            result = self._graphql_request(query, variables)

            if result and "repository" in result:
                for project in result["repository"]["projects"]["nodes"]:
                    if project["name"] == PROJECT_NAME:
                        return project["id"]
            return None
        except Exception as e:
            print(f"  ⚠️  Could not find project: {e}")
            return None

    def create_branch_protection(self) -> bool:
        """Configure branch protection rules for develop and main branches."""
        print("\n🔒 Configuring branch protection...")
        try:
            branches = {
                "develop": {
                    "required_status_checks": {
                        "strict": True,
                        "contexts": ["build", "test", "lint"],
                    },
                    "required_pull_request_reviews": {
                        "dismiss_stale_reviews": True,
                        "require_code_owner_reviews": False,
                        "required_approving_review_count": 1,
                    },
                    "enforce_admins": True,
                    "allow_force_pushes": False,
                    "allow_deletions": False,
                },
                "main": {
                    "required_status_checks": {
                        "strict": True,
                        "contexts": ["build", "test", "lint"],
                    },
                    "required_pull_request_reviews": {
                        "dismiss_stale_reviews": True,
                        "require_code_owner_reviews": False,
                        "required_approving_review_count": 1,
                    },
                    "enforce_admins": True,
                    "allow_force_pushes": False,
                    "allow_deletions": False,
                },
            }

            for branch_name, protection_rules in branches.items():
                try:
                    branch = self.repository.get_branch(branch_name)
                    self._update_branch_protection(branch_name, protection_rules)
                    print(f"  ✅ Configured protection for: {branch_name}")
                except GithubException as e:
                    if e.status == 404:
                        print(f"  ⚠️  Branch does not exist: {branch_name}")
                    else:
                        print(f"  ⚠️  Could not configure {branch_name}: {e}")

            return True
        except Exception as e:
            print(f"  ❌ Error configuring branch protection: {e}")
            return False

    def _update_branch_protection(self, branch: str, rules: Dict) -> None:
        """Update branch protection via REST API."""
        url = f"{self.api_base}/repos/{self.owner}/{self.repo}/branches/{branch}/protection"
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }

        response = requests.put(url, json=rules, headers=headers)
        if response.status_code not in [200, 201]:
            print(f"    Warning: {response.status_code} - {response.text}")

    def create_first_issue(self, milestone_id: Optional[str] = None) -> bool:
        """Create the first GitHub Issue."""
        print("\n📝 Creating first GitHub Issue...")
        try:
            # Get milestone if available
            milestone = None
            if milestone_id:
                try:
                    milestone = self.repository.get_milestone(int(milestone_id))
                except:
                    pass

            issue = self.repository.create_issue(
                title=FIRST_ISSUE["title"],
                body=FIRST_ISSUE["body"],
                milestone=milestone,
            )

            # Add labels
            issue.add_to_labels(*FIRST_ISSUE["labels"])

            print(f"  ✅ Created first issue: {issue.html_url}")
            return True
        except Exception as e:
            print(f"  ❌ Error creating first issue: {e}")
            return False

    def _graphql_request(self, query: str, variables: Dict) -> Optional[Dict]:
        """Make GraphQL API request."""
        headers = {
            "Authorization": f"token {self.token}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            f"{self.api_base}/graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )

        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                raise Exception(f"GraphQL error: {data['errors']}")
            return data.get("data")
        else:
            raise Exception(
                f"GraphQL request failed: {response.status_code} - {response.text}"
            )

    def print_summary(self) -> None:
        """Print setup summary."""
        print("\n" + "=" * 60)
        print("✅ GitHub Setup Complete!")
        print("=" * 60)
        print(f"\n📦 Repository: {self.owner}/{self.repo}")
        print(f"🔗 URL: https://github.com/{self.owner}/{self.repo}")
        print(f"\n✓ Labels created: {len(LABELS)}")
        print(f"✓ Milestones created: {len(MILESTONES)}")
        print(f"✓ Project board: {PROJECT_NAME}")
        print(f"✓ Branch protection: develop, main")
        print("\n📋 Next Steps:")
        print("1. Verify labels in Issues → Labels")
        print("2. Check milestones in Issues → Milestones")
        print("3. View project at Projects tab")
        print("4. Confirm branch protection in Settings → Branches")
        print(f"5. See first issue: #{self.repository.get_issues()[0].number}")
        print("\n" + "=" * 60)


def check_gh_cli() -> bool:
    """Check if GitHub CLI is installed and authenticated."""
    try:
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def get_gh_token() -> Optional[str]:
    """Get GitHub token from GitHub CLI."""
    try:
        result = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def get_repo_from_git() -> Optional[Tuple[str, str]]:
    """Get repository owner and name from git remote."""
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            url = result.stdout.strip()
            # Parse GitHub URL (https or ssh)
            if "github.com" in url:
                # Extract owner/repo from URL
                # https://github.com/owner/repo.git
                # git@github.com:owner/repo.git
                parts = url.replace(".git", "").split("/")
                if len(parts) >= 2:
                    repo = parts[-1]
                    owner = parts[-2].split(":")[-1]  # Handle SSH format
                    return owner, repo
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def get_credentials() -> Tuple[str, str, str]:
    """
    Get GitHub credentials using GitHub CLI (REQUIRED by project policy).
    
    Project Policy: docs/01_PREREQUISITES.md - "GitHub Authentication Rule (MANDATORY)"
    - ✅ GitHub CLI (`gh`) is the ONLY permitted authentication method
    - ❌ Personal Access Tokens (PAT) are FORBIDDEN
    - Exception: GitHub Actions built-in GITHUB_TOKEN for CI/CD only
    """
    print("\n🔐 Checking authentication methods...")
    
    # Check if running in GitHub Actions CI/CD context
    is_github_actions = os.getenv("GITHUB_ACTIONS") == "true"
    
    # Check for environment token first (to detect policy violations)
    env_token = os.getenv("GITHUB_TOKEN")
    
    if env_token:
        # Detect token type
        if env_token.startswith("github_pat_"):
            if not is_github_actions:
                print("\n" + "=" * 70)
                print("❌ POLICY VIOLATION: Fine-grained Personal Access Token detected")
                print("=" * 70)
                print("\n⚠️  Personal Access Tokens (PAT) are FORBIDDEN by project policy")
                print("    See: docs/01_PREREQUISITES.md - 'GitHub Authentication Rule'")
                print("\n✅ Required: Use GitHub CLI instead:")
                print("    1. Install GitHub CLI: https://cli.github.com/")
                print("    2. Authenticate: gh auth login")
                print("    3. Run script again (no GITHUB_TOKEN needed)")
                print("\n❌ Unset GITHUB_TOKEN and use GitHub CLI:")
                print("    unset GITHUB_TOKEN")
                print("    gh auth login")
                print("\n" + "=" * 70)
                sys.exit(1)
        elif env_token.startswith("ghp_"):
            if not is_github_actions:
                print("\n" + "=" * 70)
                print("❌ POLICY VIOLATION: Classic Personal Access Token detected")
                print("=" * 70)
                print("\n⚠️  Personal Access Tokens (PAT) are STRICTLY FORBIDDEN")
                print("    See: docs/01_PREREQUISITES.md - 'GitHub Authentication Rule'")
                print("\n✅ Required: Use GitHub CLI instead:")
                print("    1. Install GitHub CLI: https://cli.github.com/")
                print("    2. Authenticate: gh auth login")
                print("    3. Run script again (no GITHUB_TOKEN needed)")
                print("\n❌ Unset GITHUB_TOKEN and use GitHub CLI:")
                print("    unset GITHUB_TOKEN")
                print("    gh auth login")
                print("\n" + "=" * 70)
                sys.exit(1)
        elif is_github_actions:
            # GitHub Actions built-in token is permitted
            print("✓ Found GitHub Actions built-in GITHUB_TOKEN (CI/CD)")
            print("  This is permitted for automated workflows")
            token = env_token
            
            # Get repo info from environment (GitHub Actions provides these)
            owner = os.getenv("GITHUB_REPOSITORY_OWNER") or os.getenv("GITHUB_OWNER")
            repo_full = os.getenv("GITHUB_REPOSITORY")  # format: owner/repo
            if repo_full and "/" in repo_full:
                owner, repo = repo_full.split("/", 1)
            elif not owner:
                owner = os.getenv("GITHUB_OWNER")
            
            if not repo:
                repo = os.getenv("GITHUB_REPO")
            
            if owner and repo:
                return token, owner, repo
    
    # Try GitHub CLI (REQUIRED method)
    if check_gh_cli():
        print("✓ Found GitHub CLI authentication")
        token = get_gh_token()
        if token:
            print("✓ Successfully retrieved token from GitHub CLI")
            
            # Try to get repo info from git
            repo_info = get_repo_from_git()
            if repo_info:
                owner, repo = repo_info
                print(f"✓ Auto-detected repository: {owner}/{repo}")
                return token, owner, repo
            
            # Fall back to environment or prompt for repo info
            owner = os.getenv("GITHUB_OWNER")
            repo = os.getenv("GITHUB_REPO")
            
            if not owner:
                owner = input("👤 Enter repository owner (username/org): ").strip()
            if not repo:
                repo = input("📦 Enter repository name: ").strip()
                
            if owner and repo:
                return token, owner, repo
    
    # GitHub CLI not found - show error with setup instructions
    print("\n" + "=" * 70)
    print("❌ GitHub CLI not found or not authenticated")
    print("=" * 70)
    print("\n⚠️  This project REQUIRES GitHub CLI for authentication")
    print("    Personal Access Tokens (PAT) are FORBIDDEN by project policy")
    print("    See: docs/01_PREREQUISITES.md - 'GitHub Authentication Rule'")
    print("\n✅ Setup GitHub CLI:")
    print("\n1. Install GitHub CLI:")
    print("   macOS:    brew install gh")
    print("   Linux:    sudo apt install gh")
    print("   Windows:  https://cli.github.com/")
    print("\n2. Authenticate:")
    print("   gh auth login")
    print("   (Follow prompts to login via browser)")
    print("\n3. Verify:")
    print("   gh auth status")
    print("   (Should show: ✓ Logged in to github.com)")
    print("\n4. Run this script again:")
    print("   python .github/setup_github.py")
    print("\n" + "=" * 70)
    sys.exit(1)


def main():
    """Main setup function."""
    print("=" * 60)
    print("🚀 GitHub Repository Automatic Setup")
    print("=" * 60)

    try:
        # Get credentials
        token, owner, repo = get_credentials()

        # Initialize setup handler
        setup = GitHubSetup(token, owner, repo)

        # Verify access
        print(f"\n✓ Authenticated as: {setup.gh.get_user().login}")
        print(f"✓ Repository: {owner}/{repo}")

        # Run setup steps
        results = {
            "labels": setup.create_labels(),
            "milestones": setup.create_milestones(),
            "project": setup.create_project_board() is not None,
            "branch_protection": setup.create_branch_protection(),
            "first_issue": setup.create_first_issue(),
        }

        # Print summary
        setup.print_summary()

        # Check if all steps completed
        if all(results.values()):
            print("\n✅ All setup steps completed successfully!")
            return 0
        else:
            print("\n⚠️  Some setup steps had warnings (see above)")
            return 1

    except GithubException as e:
        print(f"\n❌ GitHub API error: {e}")
        if e.status == 401:
            print("   Check your personal access token")
        elif e.status == 404:
            print("   Check that owner and repository name are correct")
        return 1
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
