# GitHub Repository Configuration Guide

## Branch Protection Rules

To set up branch protection rules for `main` and `develop` branches, follow these steps in GitHub:

### For `develop` branch:

1. Go to **Settings** → **Branches**
2. Under "Branch protection rules", click **Add rule**
3. Set **Branch name pattern** to `develop`
4. Enable:
   - ✅ **Require a pull request before merging**
     - ✅ Require approvals (at least 1)
     - ✅ Require status checks to pass before merging
   - ✅ **Require branches to be up to date before merging**
   - ✅ **Include administrators** (so rules apply to all)
5. Click **Create**

### For `main` branch:

1. Add rule for branch name pattern: `main`
2. Enable:
   - ✅ **Require a pull request before merging**
     - ✅ Require approvals (at least 1 reviewer)
     - ✅ Require status checks to pass before merging
     - ✅ Require code reviews from code owners (if applicable)
   - ✅ **Require branches to be up to date before merging**
   - ✅ **Require status checks to pass** (select: linter, tests, type-check)
   - ✅ **Include administrators**
   - ✅ **Restrict who can push to matching branches** (optional)
3. Click **Create**

## GitHub Project Board Setup

### ✅ Status: Project Created (2026-03-05)

**Project Details:**
- ✅ Project created manually via GitHub UI
- 📋 7 Issues available for tracking (#1-#7)
- 📖 Workflow guide: [PROJECT_WORKFLOW.md](PROJECT_WORKFLOW.md)
- 📚 Setup guide: [GITHUB_PROJECT_SETUP.md](GITHUB_PROJECT_SETUP.md)

### Next Steps:

1. **Add Issues to Project**:
   - Navigate to your project board
   - Click **"+ Add item"**
   - Type `#` and select issues #1 through #7

2. **Organize Issues**:
   - Move #2 and #6 to "Todo" (High priority)
   - Move #5 and #1 to "Next Up"
   - Move #3, #7, #4 to "Future"

3. **Add Custom Fields** (Optional):
   - Priority (High, Medium, Low)
   - Week (Week 2, Week 3, Week 4)
   - Provider (AWS, GCP, Azure, Common)

### Original Instructions (for reference):

1. Go to **Projects** tab (top-right of repository)
2. Click **New project**
3. Set **Project name**: "Development Tracking"
4. Set **Description**: "Tracks all development tasks, features, and bug fixes"
5. Keep **Table** as view type
6. Click **Create project**

### Configure columns/fields:

Use custom fields:
- **Status**: Single select (Backlog, To Do, In Progress, In Review, Done)
- **Priority**: Single select (Critical, High, Medium, Low)
- **Effort**: Single select (Small, Medium, Large)
- **Type**: Single select (Bug, Feature, Task, Documentation)

### Add automation:

Go to **Project settings** → **Automation**:
1. **When issue is opened**: Move to "Backlog"
2. **When PR is opened**: Move to "In Progress"
3. **When PR is merged**: Move to "Done"

## GitHub Project Board Workflow

```
Backlog → To Do → In Progress → In Review → Done
   ↓        ↓         ↓           ↓         ↓
[Prioritize] [Schedule] [Develop] [Review] [Release]
```

1. **Backlog**: New issues awaiting prioritization
2. **To Do**: Prioritized, ready to start
3. **In Progress**: Currently being worked on
4. **In Review**: PR submitted, awaiting review
5. **Done**: Merged and verified

## Required GitHub Labels

Create these labels for consistent issue categorization:

| Label | Color | Description |
|-------|-------|-------------|
| `bug` | 🔴 Red (#d73a49) | Bug reports |
| `enhancement` | 🟢 Green (#28a745) | Feature requests |
| `documentation` | 🔵 Blue (#0075ca) | Documentation updates |
| `task` | 🟡 Yellow (#ffc107) | General tasks |
| `high-priority` | 🔴 Dark Red (#800000) | High priority issues |
| `blocked` | 🟠 Orange (#ff9800) | Blocked by other issues |
| `in-progress` | 🟣 Purple (#6f42c1) | Currently being worked on |
| `needs-review` | 🔵 Cyan (#1f97c6) | Waiting for review |

To create labels:
1. Go to **Issues** tab
2. Click **Labels** (left sidebar)
3. Click **New label**
4. Fill in label name, color, and description
5. Click **Create label**

## Milestones Setup

Create milestones for releases:

1. Go to **Issues** tab
2. Click **Milestones** (left sidebar)
3. Click **New milestone**
4. **Title**: `v1.0.0` (or version number)
5. **Description**: Release goals and timeline
6. **Due date**: Target release date
7. Click **Create milestone**

Repeat for each planned release (v1.0.0, v1.1.0, etc.)

## Code Review Process

1. **Developer creates PR** from feature branch to `develop`
2. **Automated checks run** (CI/CD pipeline via GitHub Actions)
3. **Reviewer reviews** code and requests changes if needed
4. **Developer addresses** feedback
5. **Reviewer approves** the PR
6. **PR is merged** to `develop` (deletes feature branch)
7. **Issue is automatically** moved to "Done" (via automation)

## First Issue Template

Use [.github/ISSUE_TEMPLATE/](../ISSUE_TEMPLATE/) for these templates:
- `bug_report.md` - For bug reports
- `feature_request.md` - For feature requests
- `task.md` - For general tasks

## Integration with Development

When working on an issue:

1. Create feature branch: `git checkout -b feature/issue-name`
2. Make changes and commits
3. Push branch and create PR with: `Closes #123`
4. Go through review process
5. Merge to `develop`
6. Issue automatically marked as done

---

For more information, see [01_PREREQUISITES.md](../../../docs/01_PREREQUISITES.md#github-features-usage-mandatory)
