# GitHub Projects Setup Guide

## Overview

This guide explains how to set up GitHub Projects for CloudServiceManager development tracking.

---

## Method 1: Browser-Based Setup (Recommended - No Token Update Required)

### Step 1: Create a New Project

1. Go to: https://github.com/PLAYER1-r7/CloudServiceManager/projects
2. Click **"New project"** button (green button in top-right)
3. Choose a template:
   - **Board** (Recommended) - Kanban-style board with columns
   - **Table** - Spreadsheet-like view
   - **Roadmap** - Timeline view

### Step 2: Configure Project

**Project Name**: `CloudServiceManager Development`  
**Description**: Multi-cloud resource management CLI tool development tracking  
**Visibility**: Public (same as repository)

### Step 3: Add Issues to Project

All development tasks are already tracked as Issues:

- [#1](https://github.com/PLAYER1-r7/CloudServiceManager/issues/1) - CloudService データモデル完成・テスト
- [#2](https://github.com/PLAYER1-r7/CloudServiceManager/issues/2) - クラウド認証メカニズム実装
- [#3](https://github.com/PLAYER1-r7/CloudServiceManager/issues/3) - Week 3: GCP プロバイダー実装
- [#4](https://github.com/PLAYER1-r7/CloudServiceManager/issues/4) - Week 4: 統合テストと最適化
- [#5](https://github.com/PLAYER1-r7/CloudServiceManager/issues/5) - Week 2: AWS プロバイダー実装
- [#6](https://github.com/PLAYER1-r7/CloudServiceManager/issues/6) - list-services コマンド実装完成
- [#7](https://github.com/PLAYER1-r7/CloudServiceManager/issues/7) - Week 3: Azure プロバイダー実装

**To add issues:**
1. In your project view, click **"+ Add item"**
2. Type `#` to search existing issues
3. Select each issue (#1-#7)
4. Organize into columns (Todo, In Progress, Done)

### Step 4: Customize Views (Optional)

**Recommended Columns for Board View:**
- 📋 **Backlog** - Planned but not started
- 🚀 **Todo** - Ready to start
- 🔄 **In Progress** - Actively working
- 🧪 **In Review** - Testing/Code review
- ✅ **Done** - Completed

**Add custom fields:**
- Priority (High, Medium, Low)
- Week (Week 1, Week 2, Week 3, Week 4)
- Provider (AWS, GCP, Azure, Common)

---

## Method 2: GitHub CLI Setup (Advanced - Requires Token Update)

### Prerequisites

Update GitHub CLI token with `project` scope:

```bash
# Refresh token with project scope
gh auth refresh -s project

# Verify token has project scope
gh auth status
```

### Create Project via CLI

```bash
# Create a new project for the repository
gh project create \
  --owner PLAYER1-r7 \
  --title "CloudServiceManager Development" \
  --description "Multi-cloud resource management CLI tool development tracking" \
  --format board

# Note: This will return a project ID/URL
```

### Add Issues to Project

```bash
# First, get the project number from the URL
# Example URL: https://github.com/users/PLAYER1-r7/projects/1
# Project number is: 1

# Add issues to project (replace <PROJECT_NUMBER> with actual number)
gh project item-add <PROJECT_NUMBER> --owner PLAYER1-r7 --url https://github.com/PLAYER1-r7/CloudServiceManager/issues/1
gh project item-add <PROJECT_NUMBER> --owner PLAYER1-r7 --url https://github.com/PLAYER1-r7/CloudServiceManager/issues/2
gh project item-add <PROJECT_NUMBER> --owner PLAYER1-r7 --url https://github.com/PLAYER1-r7/CloudServiceManager/issues/3
gh project item-add <PROJECT_NUMBER> --owner PLAYER1-r7 --url https://github.com/PLAYER1-r7/CloudServiceManager/issues/4
gh project item-add <PROJECT_NUMBER> --owner PLAYER1-r7 --url https://github.com/PLAYER1-r7/CloudServiceManager/issues/5
gh project item-add <PROJECT_NUMBER> --owner PLAYER1-r7 --url https://github.com/PLAYER1-r7/CloudServiceManager/issues/6
gh project item-add <PROJECT_NUMBER> --owner PLAYER1-r7 --url https://github.com/PLAYER1-r7/CloudServiceManager/issues/7
```

### List All Issues in Project

```bash
gh project item-list <PROJECT_NUMBER> --owner PLAYER1-r7 --format table
```

---

## Recommended Project Structure

### Week-Based Organization

**Week 1: Foundation** ✅
- [x] DevContainer setup
- [x] Documentation
- [x] GitHub repository & issues

**Week 2: AWS Implementation** (Current)
- [ ] #1 CloudService model + tests
- [ ] #2 Cloud authentication
- [ ] #5 AWS provider implementation

**Week 3: GCP & Azure Implementation**
- [ ] #3 GCP provider implementation
- [ ] #7 Azure provider implementation

**Week 4: Integration & Polish**
- [ ] #6 list-services command completion
- [ ] #4 Integration tests & optimization

---

## Project Automation (Optional)

### Auto-Move Cards

You can set up automation rules:
- When an issue is created → Move to "Todo"
- When a PR is opened → Move to "In Review"
- When a PR is merged → Move to "Done"

### Status Sync with Issues

Enable "Status" field to sync with Issue state:
- Open issues → Automatically in "Todo" or "In Progress"
- Closed issues → Automatically in "Done"

---

## Useful Commands

```bash
# View project in browser
gh project view <PROJECT_NUMBER> --owner PLAYER1-r7 --web

# List all projects
gh project list --owner PLAYER1-r7

# Edit project details
gh project edit <PROJECT_NUMBER> --owner PLAYER1-r7 --title "New Title"

# Close project (when Phase 1 is complete)
gh project close <PROJECT_NUMBER> --owner PLAYER1-r7
```

---

## Next Steps After Project Creation

1. **Link repository to project** (automatic if created from repo)
2. **Add team members** (if applicable)
3. **Set up automation rules** for workflow efficiency
4. **Create project views**:
   - By Week (filter by week label)
   - By Provider (filter by provider label)
   - By Priority
5. **Update project regularly** as you complete tasks

---

## Resources

- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub CLI Projects Documentation](https://cli.github.com/manual/gh_project)
- [Project Automation Guide](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project)
