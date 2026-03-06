# GitHub Initial Setup Checklist

This checklist documents all the GitHub setup tasks required for the Cloud Service Manager project.

## Pre-Setup Requirements

- [ ] Repository created on GitHub
- [ ] Repository cloned locally
- [ ] Admin access to repository settings
- [ ] Team members invited to repository

## Step 1: Create GitHub Labels

Priority: **HIGH** - Do this first for consistency

Go to: **Settings** → **Labels** (or **Issues** → **Labels**)

Required labels:
- [ ] `bug` (Red #d73a49) - Bug reports and issues
- [ ] `enhancement` (Green #28a745) - Feature requests  
- [ ] `documentation` (Blue #0075ca) - Documentation updates
- [ ] `task` (Yellow #ffc107) - General tasks and work items
- [ ] `high-priority` (Dark Red #800000) - Urgent, high priority work
- [ ] `blocked` (Orange #ff9800) - Blocked by dependencies
- [ ] `in-progress` (Purple #6f42c1) - Currently being worked on
- [ ] `needs-review` (Cyan #1f97c6) - Awaiting review/feedback

## Tooling Policy (Mandatory)

Priority: **CRITICAL** - Apply this rule before operational work

- [ ] If required software is missing, install it first (for example: `gh`, `jq`, `rg`)
- [ ] Avoid fallback workflows when installation is possible
- [ ] Use alternatives only when installation is blocked by permissions/network/policy
- [ ] If an alternative is used, record the blocker and reason in the related issue/PR comment
- [ ] Revisit and install the missing software as soon as the blocker is removed
- [ ] After software installation, reflect required changes in `.devcontainer/` (Dockerfile, `devcontainer.json`, post-create scripts, package lists)
- [ ] If authentication is required for tools/services, explicitly request authentication before proceeding (for example: `gh auth login`, cloud CLI login)
- [ ] Do not continue privileged operations while unauthenticated; request auth first and resume after verification

## Step 2: Create Milestones

Priority: **HIGH** - Essential for release planning

Go to: **Issues** → **Milestones**

Milestones to create:
- [ ] `v1.0.0` - Due date: (set target date)
  - Description: Phase 1 MVP - AWS, GCP, Azure provider support
- [ ] `v1.1.0` - Due date: (set target date)
  - Description: Phase 1 enhancements - Additional features
- [ ] `v2.0.0` - Due date: (set target date)
  - Description: Phase 2 - Web application converted to FastAPI

## Step 3: Create GitHub Project

Priority: **HIGH** - Essential for task management

Go to: **Projects** → **New Project**

Configuration:
- [ ] Project name: `Development Tracking`
- [ ] Description: `Tracks all development tasks, features, and bugs across sprints`
- [ ] View type: `Table`
- [ ] Create the project

### Configure Project Fields

In project settings, create these custom fields:
- [ ] **Status** (Single select)
  - Options: Backlog, To Do, In Progress, In Review, Done
- [ ] **Priority** (Single select)
  - Options: Critical, High, Medium, Low
- [ ] **Effort** (Single select)
  - Options: Small (1-2h), Medium (2-4h), Large (4+ hours)
- [ ] **Type** (Single select)
  - Options: Bug, Feature, Task, Documentation

## Step 4: Configure Branch Protection

Priority: **CRITICAL** - Essential for code quality

Go to: **Settings** → **Branches** → **Add rule**

### For `develop` branch:

- [ ] Branch name pattern: `develop`
- [ ] Require PR before merge: **YES**
  - [ ] Require at least 1 approval
- [ ] Require status checks to pass: **YES**
- [ ] Require up-to-date before merge: **YES**
- [ ] Include administrators: **YES**

### For `main` branch:

- [ ] Branch name pattern: `main`
- [ ] Require PR before merge: **YES**
  - [ ] Require at least 1 approval
  - [ ] Require code owner reviews: **YES** (if applicable)
- [ ] Require status checks to pass: **YES**
- [ ] Require up-to-date before merge: **YES**
- [ ] Restrict push access: **YES** (optional, restrict to release process only)
- [ ] Include administrators: **YES**

## Step 5: Set Up GitHub Actions CI/CD

Priority: **HIGH** - Enables automated testing

Files to check:
- [ ] `.github/workflows/ci.yml` exists and configured
  - Should run tests on: push to develop/main, all PRs
  - Should run linting and code quality checks
  - Should run type checking
  - Should measure code coverage

### Verify CI/CD:
- [ ] Push a test commit to develop
- [ ] Verify workflow runs in **Actions** tab
- [ ] Status check appears on PR if created

## Step 6: Create Issue Templates

Priority: **MEDIUM** - Improves issue consistency

Files to verify:
- [ ] `.github/ISSUE_TEMPLATE/bug_report.md` exists
- [ ] `.github/ISSUE_TEMPLATE/feature_request.md` exists
- [ ] `.github/ISSUE_TEMPLATE/task.md` exists

### Test templates:
- [ ] Create test bug report issue
- [ ] Create test feature request issue
- [ ] Verify templates auto-populate

## Step 7: Create First Issues

Priority: **MEDIUM** - Start tracking work

First issues to create:
- [ ] **[TASK] Set Up GitHub Project Board** (#1)
  - Assign to yourself
  - Add to Milestone: v1.0.0
  - Add labels: `task`, `high-priority`
  - Description in `.github/FIRST_ISSUE.md`

- [ ] **[FEATURE] Implement AWS Provider** (#2)
  - Assign to appropriate team member
  - Add to Milestone: v1.0.0
  - Add labels: `enhancement`
  - Description from PROJECT_PLAN.md

- [ ] **[FEATURE] Implement GCP Provider** (#3)
  - Assign to appropriate team member
  - Add to Milestone: v1.0.0
  - Add labels: `enhancement`

- [ ] **[FEATURE] Implement Azure Provider** (#4)
  - Assign to appropriate team member
  - Add to Milestone: v1.0.0
  - Add labels: `enhancement`

## Step 8: Configure Project Automation

Priority: **MEDIUM** - Automates workflow updates

In **Project Settings** → **Automation**:

- [ ] **When issue is opened**: Auto-add to Backlog
- [ ] **When pull request opened**: Move to In Progress
- [ ] **When pull request merged**: Move to Done
- [ ] **When issue closed**: Move to Done

## Step 9: Verify Setup

Priority: **MEDIUM** - Ensure everything works

Test procedures:
- [ ] Create test feature branch from develop
- [ ] Make a test commit
- [ ] Create test PR to develop
- [ ] Verify CI/CD runs automatically
- [ ] Verify status checks appear
- [ ] Verify PR cannot be merged without approval
- [ ] Request approval and merge
- [ ] Verify develop is protected
- [ ] Attempt to push to develop directly (should fail)

## Step 10: Document Setup

Priority: **LOW** - For future reference

- [ ] Review `.github/GITHUB_SETUP.md`
- [ ] Update with actual repository URL
- [ ] Share setup guide with team
- [ ] Add link to README.md: "See [GitHub Setup](.github/GITHUB_SETUP.md)"
- [ ] Update team wiki/documentation with GitHub workflow

## Step 11: Team Training

Priority: **LOW** - Onboarding

- [ ] Share `.github/GITHUB_SETUP.md` with team
- [ ] Share `.github/FIRST_ISSUE.md` with team
- [ ] Explain branch strategy and workflow
- [ ] Explain how to create/link issues to PRs
- [ ] Explain how to use project board
- [ ] Explain GitHub PR review process

## Post-Setup Maintenance

Once setup is complete:

### Weekly Tasks
- [ ] Review project board status
- [ ] Update issue status and progress
- [ ] Monitor milestone completion
- [ ] Check CI/CD pipeline for failures

### Per Release
- [ ] Create release milestone
- [ ] Assign relevant issues
- [ ] Track milestone progress
- [ ] Create release notes
- [ ] Tag release on GitHub

---

## Useful GitHub Links

- [Branch protection rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Issue templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests)

---

**Last Updated**: 2026-03-06  
**Status**: Ready for implementation
