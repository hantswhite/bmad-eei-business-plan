# BMAD EEI Business Plan

An expansion pack for the [BMAD Framework](https://github.com/bmadcode/BMAD-METHOD) that adds a 15-step context-adaptive business plan workflow with integrated strategy frameworks, document lifecycle management, and PDF generation.

## Prerequisites

- BMAD v6.0.4+ installed in your project (core, bmm, or bmb modules)
- Python 3.8+ (for validation tests)
- WeasyPrint 68+ (for PDF generation, optional)
- Pandoc (for full plan PDF, optional)

## Installation

```bash
# Add as git submodule
git submodule add https://github.com/hantswhite/bmad-eei-business-plan.git _bmad/eei

# Run setup (generates config.yaml, symlinks slash commands)
./_bmad/eei/setup.sh

# Commit
git add .gitmodules _bmad/eei/config.yaml .claude/commands/bmad-eei-bp-*
git commit -m "feat: add bmad-eei-business-plan extension"
```

## Updating

```bash
cd _bmad/eei && git pull origin main && cd ../..
./_bmad/eei/setup.sh   # picks up any new slash commands
git add _bmad/eei .claude/commands/
git commit -m "chore: update bmad-eei-business-plan"
```

## What's Included

- **6 agents:** Strategy Consultant (Victoria), Financial Analyst (Marcus), Market Analyst (Diana), Operations Planner (Ray), Plan Assembler (Eli), Critique Agent
- **24 templates:** Strategy frameworks (SWOT, VRIO, Blue Ocean, Wardley, etc.), plan formats, PDF styles
- **15-step workflow:** Context setup through deliverables packaging, with document lifecycle (DRAFT -> CRITIQUE -> REVISED -> FINAL REVIEW -> FINAL)
- **13 slash commands:** Agent activations, lifecycle management, PDF generation
- **Validation tests:** 15 suites, 32+ structural checks

## Configuration

After running `setup.sh`, edit `config.yaml` to customize:

- `project_name` / `user_name` — project identity
- `research_enforcement` — strict / standard / permissive
- `research_paths` — glob patterns for research document detection
- Governance file paths (`assumptions_file`, `decisions_file`, etc.)

## Structure

```
business-plan/
  agents/          # 6 specialist agents
  config/          # persona-grid.yaml, section-topic-map.yaml
  templates/       # strategy frameworks, CSS, plan formats
  workflows/       # 15-step workflow with lifecycle management
  commands/        # 13 slash command source files
tests/             # structural validation suite
config.template.yaml
setup.sh
```

## License

Proprietary. All rights reserved.
