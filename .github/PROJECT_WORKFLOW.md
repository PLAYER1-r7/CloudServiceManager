# GitHub Project Workflow Guide

## 🎯 Quick Start - Project Created ✅

Your GitHub Project is now set up! Here's how to use it effectively.

---

## 📋 Current Issues (7 total)

| # | Issue | Week | Type | Priority |
|---|-------|------|------|----------|
| #2 | CloudService データモデル完成・テスト | - | Model/Data | 🔴 High |
| #6 | クラウドプロバイダー認証実装 | - | Security | 🔴 High |
| #5 | Week 2: AWS プロバイダー実装 | Week 2 | Provider | 🟡 Medium |
| #1 | list-services コマンド実装完成 | - | CLI | 🟡 Medium |
| #3 | Week 3: GCP プロバイダー実装 | Week 3 | Provider | 🟢 Low |
| #7 | Week 3: Azure プロバイダー実装 | Week 3 | Provider | 🟢 Low |
| #4 | Week 4: 統合テストと最適化 | Week 4 | Testing | 🟢 Low |

---

## 🗂️ Recommended Project Structure

### Board View Columns

```
┌─────────────┬──────────────┬──────────────┬─────────┐
│   📋 Todo   │ 🚀 In Prog   │  🧪 Review   │ ✅ Done │
├─────────────┼──────────────┼──────────────┼─────────┤
│ #2 Model    │              │              │         │
│ #6 Auth     │              │              │         │
├─────────────┼──────────────┼──────────────┼─────────┤
│   Next Up   │              │              │         │
├─────────────┼──────────────┼──────────────┼─────────┤
│ #5 AWS      │              │              │         │
│ #1 CLI      │              │              │         │
├─────────────┼──────────────┼──────────────┼─────────┤
│   Future    │              │              │         │
├─────────────┼──────────────┼──────────────┼─────────┤
│ #3 GCP      │              │              │         │
│ #7 Azure    │              │              │         │
│ #4 Testing  │              │              │         │
└─────────────┴──────────────┴──────────────┴─────────┘
```

### Custom Fields to Add

**Priority**
- 🔴 High - Blockers for other work
- 🟡 Medium - Important features
- 🟢 Low - Nice to have

**Week**
- Week 1 (✅ Complete)
- Week 2 (Current)
- Week 3
- Week 4

**Provider**
- AWS
- GCP
- Azure
- Common (shared functionality)

**Status**
- 📋 Todo
- 🚀 In Progress
- 🧪 In Review
- ✅ Done
- 🔄 Blocked

---

## 🔄 Daily Workflow

### Morning Routine

```bash
# 1. Check project status
gh issue list --repo PLAYER1-r7/CloudServiceManager --json number,title,state

# 2. View specific issue
gh issue view 2 --repo PLAYER1-r7/CloudServiceManager

# 3. Start working on an issue
# → Move card to "In Progress" in project board
```

### During Development

1. **Create a branch** for the issue
   ```bash
   git checkout -b feature/issue-2-cloudservice-model
   ```

2. **Make commits** referencing the issue
   ```bash
   git commit -m "feat: implement CloudService model (#2)"
   ```

3. **Push and create PR**
   ```bash
   git push -u origin feature/issue-2-cloudservice-model
   gh pr create --title "Implement CloudService model" --body "Closes #2"
   ```

4. **Update project board**
   - Move card to "In Review"

### After PR Merge

1. **Issue auto-closes** when PR is merged
2. **Move card to "Done"** in project board
3. **Start next issue** from Todo column

---

## 📊 Project Views

### View 1: By Week (Timeline)

Filter by week labels to see weekly progress:
- `week-2`: #5 AWS
- `week-3`: #3 GCP, #7 Azure
- `week-4`: #4 Testing

### View 2: By Provider

Group by provider to see cloud-specific work:
- `aws`: #5, #6
- `gcp`: #3, #6
- `azure`: #6, #7

### View 3: By Priority

Focus on high-priority items first:
- High: #2 (Model), #6 (Auth)
- Medium: #5 (AWS), #1 (CLI)
- Low: #3, #7, #4

---

## 🎯 Recommended Development Order

### Phase 1: Foundation (Week 2 - Current)

1. **#2 CloudService データモデル完成・テスト** 🔴
   - Define unified data model
   - Write model tests
   - Dependency: None (start immediately)

2. **#6 クラウドプロバイダー認証実装** 🔴
   - Implement auth for AWS, GCP, Azure
   - Environment variable handling
   - Credential validation
   - Dependency: None (can run in parallel with #2)

### Phase 2: AWS Implementation (Week 2)

3. **#5 Week 2: AWS プロバイダー実装** 🟡
   - Implement AWS EC2 discovery
   - Map to CloudService model
   - Dependencies: #2 (Model), #6 (Auth)

4. **#1 list-services コマンド実装完成** 🟡
   - Complete CLI command
   - Output formatting (table, JSON, CSV)
   - Dependencies: #2 (Model), #5 (at least one provider)

### Phase 3: Multi-Cloud (Week 3)

5. **#3 Week 3: GCP プロバイダー実装** 🟢
   - GCP Compute Engine integration
   - Dependencies: #2 (Model), #6 (Auth)

6. **#7 Week 3: Azure プロバイダー実装** 🟢
   - Azure Virtual Machine integration
   - Dependencies: #2 (Model), #6 (Auth)

### Phase 4: Integration & Polish (Week 4)

7. **#4 Week 4: 統合テストと最適化** 🟢
   - Integration tests across all providers
   - Performance optimization
   - Documentation updates
   - Dependencies: All previous issues

---

## 🔗 Quick Links

- **Repository**: https://github.com/PLAYER1-r7/CloudServiceManager
- **Issues**: https://github.com/PLAYER1-r7/CloudServiceManager/issues
- **Projects**: https://github.com/PLAYER1-r7/CloudServiceManager/projects
- **Pull Requests**: https://github.com/PLAYER1-r7/CloudServiceManager/pulls

---

## 💡 Best Practices

### Issue Management

✅ **DO:**
- Update issue status regularly
- Add comments about progress/blockers
- Link related PRs to issues
- Use labels consistently
- Reference issues in commits

❌ **DON'T:**
- Leave stale issues open
- Work on multiple issues simultaneously
- Forget to update project board
- Skip testing before closing

### Project Board

✅ **DO:**
- Move cards as work progresses
- Keep "In Progress" to 1-2 items max
- Archive completed sprints
- Add notes/comments to cards
- Review board weekly

❌ **DON'T:**
- Let cards accumulate in one column
- Skip the Review step
- Close issues without testing
- Forget to celebrate completion! 🎉

---

## 🎉 Next Steps

1. ✅ Project created
2. 📋 **Add all 7 issues to project** (Next step)
3. 🏷️ **Organize into columns**
4. 🎨 **Add custom fields** (Priority, Week, Provider)
5. 🚀 **Start with #2 (Model) and #6 (Auth)**

Ready to start development! 🚀
