# AI Agent Project Management Guide

> **Purpose**: Enable AI agents to autonomously manage GitHub Projects
> **Audience**: AI Agents, Automation Scripts
> **Last Updated**: 2026-03-05

---

## 🎯 Overview

This guide provides AI agents with the tools and workflows needed to manage the CloudServiceManager project using GitHub Projects and automation scripts.

---

## 📊 Project Information

**Project Details:**
- **Owner**: PLAYER1-r7
- **Repository**: CloudServiceManager
- **Project Number**: 1
- **Project Name**: CloudServiceManager Development
- **Total Issues**: 7
- **Project URL**: https://github.com/users/PLAYER1-r7/projects/1

---

## 🛠️ Management Tools

### 1. Project Manager Script

**Location**: `.github/project_manager.py`

**Capabilities:**
- Display project status
- Recommend next tasks based on priority
- Generate progress reports
- Update item statuses (future)

**Usage:**

```bash
# Display full project overview
python .github/project_manager.py all

# Show current status only
python .github/project_manager.py status

# Get task recommendations
python .github/project_manager.py recommend

# Generate progress report
python .github/project_manager.py report
```

### 2. GitHub CLI Commands

**List Project Items:**
```bash
gh project item-list 1 --owner PLAYER1-r7 --format json
```

**View Specific Issue:**
```bash
gh issue view 2 --repo PLAYER1-r7/CloudServiceManager
```

**Update Issue Status (via project):**
```bash
# Note: Requires field ID lookup
gh project item-edit \
  --project-id 1 \
  --owner PLAYER1-r7 \
  --id <ITEM_ID> \
  --field-id Status \
  --text "In Progress"
```

**Add Issue to Project:**
```bash
gh project item-add 1 \
  --owner PLAYER1-r7 \
  --url https://github.com/PLAYER1-r7/CloudServiceManager/issues/2
```

---

## 📋 Task Priority System

### High Priority (Start Immediately) 🔴

**#2: CloudService データモデル完成・テスト**
- **Why**: Foundation for all provider implementations
- **Blocking**: #5 (AWS), #3 (GCP), #7 (Azure), #1 (CLI)
- **Dependencies**: None
- **Action**: Start immediately

**#6: クラウドプロバイダー認証実装**
- **Why**: Required for all cloud provider integrations
- **Blocking**: #5 (AWS), #3 (GCP), #7 (Azure)
- **Dependencies**: None
- **Action**: Start in parallel with #2

### Medium Priority (Next Steps) 🟡

**#5: Week 2: AWS プロバイダー実装**
- **Why**: First concrete provider implementation
- **Dependencies**: #2 (Model), #6 (Auth)
- **Action**: Start after #2 and #6 are done

**#1: list-services コマンド実装完成**
- **Why**: User-facing CLI command
- **Dependencies**: #2 (Model), #5 (at least one provider)
- **Action**: Start after #5 has basic functionality

### Low Priority (Future) 🟢

**#3: Week 3: GCP プロバイダー実装**
- **Dependencies**: #2 (Model), #6 (Auth)
- **Action**: After #5 is complete

**#7: Week 3: Azure プロバイダー実装**
- **Dependencies**: #2 (Model), #6 (Auth)
- **Action**: After #3 is complete

**#4: Week 4: 統合テストと最適化**
- **Dependencies**: All above issues
- **Action**: Final polish before release

---

## 🔄 AI Agent Workflow

### Daily Routine

1. **Check Project Status**
   ```bash
   python .github/project_manager.py status
   ```

2. **Get Recommendations**
   ```bash
   python .github/project_manager.py recommend
   ```

3. **Select Task**
   - Choose highest priority task not blocked
   - Verify dependencies are complete

4. **Update Status to "In Progress"**
   ```bash
   # Manual via GitHub UI for now
   # Automation coming soon
   ```

5. **Work on Task**
   - Create feature branch
   - Implement changes
   - Write tests
   - Update documentation

6. **Create Pull Request**
   ```bash
   gh pr create \
     --title "feat: implement CloudService model (#2)" \
     --body "Closes #2\n\nImplements the unified CloudService data model with comprehensive tests."
   ```

7. **Move to "In Review"**
   - Update project board status

8. **After Merge**
   - Issue auto-closes
   - Move to "Done" in project
   - Generate progress report

### Before Starting Any Task

**MANDATORY Checks:**

```bash
# 1. Read issue details
gh issue view <NUMBER> --repo PLAYER1-r7/CloudServiceManager

# 2. Check dependencies
python .github/project_manager.py recommend

# 3. Verify documentation
cat docs/03_API_DESIGN.md  # Check specifications
cat docs/01_PREREQUISITES.md  # Check constraints

# 4. Confirm no blockers
python .github/project_manager.py status
```

### During Task Execution

**Update Progress:**

1. **Make Regular Commits**
   ```bash
   git commit -m "feat(model): add CloudService base class (#2)"
   git commit -m "test(model): add CloudService validation tests (#2)"
   ```

2. **Reference Issue in Commits**
   - Always include `(#ISSUE_NUMBER)` in commit messages
   - Use conventional commits format

3. **Push Frequently**
   ```bash
   git push -u origin feature/issue-2-cloudservice-model
   ```

### After Task Completion

**Checklist:**

- [ ] All tests passing
- [ ] Code coverage ≥ 80%
- [ ] Documentation updated
- [ ] PR created and linked to issue
- [ ] Project status updated to "In Review"
- [ ] Generate progress report

**Generate Progress Report:**
```bash
python .github/project_manager.py report
```

---

## 📈 Progress Tracking

### Current State (2026-03-05)

```
Total Issues: 7
✅ Done: 0 (0.0%)
🚀 In Progress: 0
🔍 In Review: 0
📋 Backlog/Todo: 7

Overall Completion: 0.0%
```

### Milestone Targets

**Week 2 (Current):**
- Complete: #2, #6, #5, #1
- Target: 57% completion (4/7 issues)

**Week 3:**
- Complete: #3, #7
- Target: 86% completion (6/7 issues)

**Week 4:**
- Complete: #4
- Target: 100% completion

---

## 🤖 AI Agent Decision Framework

### When to Start a Task

**Criteria:**
1. ✅ All dependencies completed
2. ✅ No higher priority tasks available
3. ✅ Required documentation read
4. ✅ Development environment ready
5. ✅ Clear understanding of requirements

### When to Ask for Help

**Scenarios:**
- 🔴 Blocked by external dependency
- 🔴 Unclear requirements after reading docs
- 🔴 Technical constraint preventing implementation
- 🔴 Breaking changes needed
- 🟡 Multiple implementation approaches viable

### When to Update Documentation

**ALWAYS update when:**
- ✅ Completing a task
- ✅ Discovering new constraints
- ✅ Changing API design
- ✅ Adding dependencies
- ✅ Modifying file structure

---

## 📊 Status Definitions

### Backlog
- **Meaning**: Not yet started, awaiting prioritization
- **Action**: Review and prioritize
- **Next**: Move to "Todo" when ready to start

### Todo
- **Meaning**: Prioritized, ready to start
- **Action**: Select for immediate work
- **Next**: Move to "In Progress" when starting

### In Progress
- **Meaning**: Actively being worked on
- **Action**: Complete implementation and testing
- **Next**: Create PR, move to "In Review"

### In Review
- **Meaning**: PR submitted, awaiting review/merge
- **Action**: Address review comments
- **Next**: After merge, move to "Done"

### Done
- **Meaning**: Completed, tested, merged, deployed
- **Action**: Celebrate! 🎉
- **Next**: Pick next task from "Todo"

---

## 🎯 Quick Reference Commands

### Check What to Work On

```bash
# Full overview
python .github/project_manager.py all

# Quick recommendations
python .github/project_manager.py recommend
```

### Start Working on Issue #2

```bash
# 1. View issue
gh issue view 2 --repo PLAYER1-r7/CloudServiceManager

# 2. Create branch
git checkout -b feature/issue-2-cloudservice-model

# 3. Update status manually in GitHub Project UI to "In Progress"

# 4. Work on implementation...
```

### Complete a Task

```bash
# 1. Push final changes
git push -u origin feature/issue-2-cloudservice-model

# 2. Create PR
gh pr create --title "feat: implement CloudService model (#2)" --body "Closes #2"

# 3. Update project status to "In Review" in GitHub UI

# 4. After merge, check progress
python .github/project_manager.py report
```

### Generate Status Report

```bash
# Full report
python .github/project_manager.py report

# Share with user or in discussion
python .github/project_manager.py all > status_report.txt
```

---

## 🔗 Integration with Documentation

### Before Starting Any Issue

**MUST READ (in order):**

1. `docs/01_PREREQUISITES.md` - Constraints and rules
2. `docs/02_PROJECT_PLAN.md` - Architecture overview
3. `docs/03_API_DESIGN.md` - Specifications for the feature
4. Issue body on GitHub - Specific requirements

### During Implementation

**REFERENCE:**
- `docs/03_API_DESIGN.md` - API specifications
- Issue checklist - Task breakdown
- `tests/` - Existing test patterns

### After Completion

**UPDATE:**
- `docs/05_DEVELOPMENT_CHECKLIST.md` - Mark completed
- Relevant API docs if changes made
- README.md if new features added

---

## 📝 Best Practices for AI Agents

### DO ✅

- Always check dependencies before starting
- Update project status at each stage
- Reference issues in all commits
- Write comprehensive tests (80%+ coverage)
- Update documentation immediately
- Generate progress reports regularly
- Ask for clarification when uncertain
- Follow the priority system

### DON'T ❌

- Start tasks with unmet dependencies
- Work on multiple issues simultaneously
- Skip testing or documentation
- Forget to update project status
- Ignore priority recommendations
- Push code without tests
- Close issues without verification

---

## 🚀 Getting Started

**First Steps for AI Agent:**

1. **Verify Setup**
   ```bash
   gh auth status  # Should show 'project' scope
   python .github/project_manager.py status  # Should work
   ```

2. **Review Current State**
   ```bash
   python .github/project_manager.py all
   ```

3. **Select First Task**
   - Based on recommendations: #2 or #6
   - Both are high priority with no dependencies

4. **Read Documentation**
   - All docs in `docs/` directory
   - Issue details on GitHub

5. **Begin Implementation**
   - Create branch
   - Update project status
   - Start coding!

---

## 📌 Important Links

- **Project Board**: https://github.com/users/PLAYER1-r7/projects/1
- **Issues**: https://github.com/PLAYER1-r7/CloudServiceManager/issues
- **Repository**: https://github.com/PLAYER1-r7/CloudServiceManager
- **Documentation**: `/docs/` directory

---

## 🤝 Human Handoff Points

**When to Involve User:**

1. **Major Design Decisions**
   - Architecture changes
   - Breaking API changes
   - New dependencies

2. **Blockers**
   - External service issues
   - Credential problems
   - Unclear requirements

3. **Milestones**
   - Week completion
   - Major feature completion
   - Release preparation

4. **Approval Required**
   - Before starting Week 3+ tasks
   - Before making breaking changes
   - Before adding new cloud providers

---

**Ready to start autonomous project management!** 🚀

Use: `python .github/project_manager.py all` to begin.
