# Documentation Reading Guide

## **Instructions for AI Agents**

Before working on this project, **you MUST read the documentation in the following order**.

### 📖 Required Reading Order

1. **[01_PREREQUISITES.md](01_PREREQUISITES.md)** ⚠️ **CRITICAL - READ FIRST**
   - Project prerequisites, constraints, and critical technical decisions
   - DO NOT start working without reading this file

2. **[02_PROJECT_PLAN.md](02_PROJECT_PLAN.md)**
   - Overall project overview, objectives, phases, and tech stack
   - Architecture and design principles

3. **[03_API_DESIGN.md](03_API_DESIGN.md)**
   - CLI command specifications and API design
   - Input/output formats, data models

4. **[04_SETUP.md](04_SETUP.md)**
   - Development environment setup procedures
   - Cloud provider authentication configuration

5. **[05_DEVELOPMENT_CHECKLIST.md](05_DEVELOPMENT_CHECKLIST.md)**
   - Development setup progress
   - Next features to implement

### 🤖 AI Agent Resources

**For Autonomous Project Management:**
- **[../.github/AI_AGENT_PROJECT_GUIDE.md](../.github/AI_AGENT_PROJECT_GUIDE.md)** - Complete AI agent project management guide
- **[../.github/project_manager.py](../.github/project_manager.py)** - Automated project management script
- **[../.github/PROJECT_WORKFLOW.md](../.github/PROJECT_WORKFLOW.md)** - Daily workflow and best practices

**Quick Commands:**
```bash
# Check what to work on next
python .github/project_manager.py recommend

# View full project status
python .github/project_manager.py all

# Generate progress report
python .github/project_manager.py report
```

---

## **Documentation Guidelines**

### For AI Agents

- **Structure**: Each document must be well-structured in Markdown with clear sections
- **Explicit**: Avoid implicit assumptions; state all constraints and decisions explicitly
- **Context**: Include "Purpose", "Audience", and "Prerequisites" at the beginning of each document
- **Consistency**: Maintain consistent terminology, naming conventions, and formatting across documents
- **Updates**: Record update dates when making significant changes
- **Language**: All documentation in `/docs` must be in **English** for AI agents. Japanese versions are maintained in `/docs_ja` for human readers.
- **Command Execution**: Always verify command usage before executing external commands. If usage errors occur, document the correct command in relevant documentation.
- **Wiki Synchronization**: When work changes user-facing usage, setup, workflows, or troubleshooting, update GitHub Wiki pages in addition to `/docs` and `/docs_ja`.

### Directory Responsibility Policy (MANDATORY)

To keep documentation discoverable and avoid duplication, this project separates documentation by responsibility:

- **`/docs` and `/docs_ja`**: Product and implementation documentation only
   - Architecture, API/CLI specifications, setup procedures, development constraints, and checklists
   - Content should answer: "How to build, run, and maintain the product"

- **`/.github`**: Repository operations and GitHub workflow documentation only
   - GitHub Projects workflow, issue/PR process, branch protection, automation scripts, and agent operation guides
   - Content should answer: "How to manage work in GitHub and repository operations"

Rules:
- Do not move product implementation specs into `/.github`.
- Do not place GitHub operation playbooks inside `/docs` or `/docs_ja`.
- If a document references both domains, keep the primary source in the correct directory and link to the other directory.
- When adding a new document, decide the directory by purpose first, then language.

### External Command Execution Rules

**MANDATORY when executing external commands (CLI, APIs, scripts, etc.):**

1. **Always check usage first**:
   - Run `command --help` or `command -h` before executing
   - Read official documentation if available
   - Verify all required arguments and options

2. **When usage errors occur**:
   - If a command fails due to incorrect usage
   - After correcting and successfully executing
   - **MUST document the correct usage** in:
     - Code comments (for commands in scripts)
     - `04_SETUP.md` (for setup/environment commands)
     - `05_DEVELOPMENT_CHECKLIST.md` (for development commands)
     - Relevant technical documentation

3. **Documentation format**:
   ```markdown
   ### Command: <command-name>
   **Purpose**: Brief description  
   **Usage**: command [OPTIONS] [ARGUMENTS]
   **Example**: actual-working-command --option value
   **Notes**: Important notes or common pitfalls
   ```

**Rule**: "Learn from mistakes - document corrected commands for future reference."

### Reading Patterns

```
When starting work:
  1. Read 01_PREREQUISITES.md first (mandatory)
  2. Refer to relevant documents based on the task
  
When starting project management (AI Agents):
  1. Read ../.github/AI_AGENT_PROJECT_GUIDE.md
  2. Run: python .github/project_manager.py all
  3. Review recommended tasks and dependencies
  4. Select highest priority task with no blockers
  
When implementing new features:
  1. Check constraints in 01_PREREQUISITES.md
  2. Review architecture in 02_PROJECT_PLAN.md
  3. Check specifications in 03_API_DESIGN.md
  4. Implement
  5. Write tests
  6. Update documentation (MANDATORY - see below)
  7. Update 05_DEVELOPMENT_CHECKLIST.md
  
When setting up environment:
  1. Check requirements in 01_PREREQUISITES.md
  2. Follow procedures in 04_SETUP.md
  3. Verify with 05_DEVELOPMENT_CHECKLIST.md
```

---

## **Document List**

| Filename | Purpose | Priority |
|----------|---------|----------|
| 00_README_DOCS.md | This file: Overall documentation guide | ⭐ Recommended |
| 01_PREREQUISITES.md | Prerequisites, constraints, critical decisions | ⚠️ MANDATORY |
| 02_PROJECT_PLAN.md | Project plan and architecture | ⚠️ MANDATORY |
| 03_API_DESIGN.md | CLI/API design specifications | ⚠️ Required for implementation |
| 04_SETUP.md | Development environment setup guide | ⚠️ Required for initial setup |
| 05_DEVELOPMENT_CHECKLIST.md | Development progress and checklist | ⭐ Recommended |

**AI Agent Project Management** (in `.github/` directory):

| Filename | Purpose | Audience |
|----------|---------|----------|
| AI_AGENT_PROJECT_GUIDE.md | Complete autonomous project management guide | 🤖 AI Agents |
| project_manager.py | Automated project tracking script | 🤖 AI Agents |
| PROJECT_WORKFLOW.md | Daily workflow and best practices | All |
| GITHUB_PROJECT_SETUP.md | GitHub Projects setup instructions | All |

---

## **Documentation Language Policy**

### Language Rules (MANDATORY)
- **`/docs`**: All documentation MUST be in **English** (optimized for AI agents)
- **`/docs_ja`**: All documentation MUST be in **Japanese** (for human developers)
- **NO mixing**: Do NOT mix languages within a single document
- **Synchronization**: When updating documentation, update BOTH English and Japanese versions

### Update Rules (MANDATORY)
**YOU MUST update documentation after completing ANY work:**
- ✅ Always update `/docs` (English) first
- ✅ Then immediately update `/docs_ja` (Japanese)
- ✅ If user-facing content changed, also update the GitHub Wiki (for example: Home, Getting-Started, FAQ)
- ✅ Update is not optional - it's a requirement
- ✅ See [01_PREREQUISITES.md](01_PREREQUISITES.md) for detailed update process

**Rule**: "No work is complete until documentation is updated."

---

**Last Updated**: 2026-03-05  
**Version**: 1.0.0
