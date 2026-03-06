# Gap Analysis Framework

Systematic assessment of research gaps and missing playbooks based on current project state. Cross-references the business plan, assumptions, decisions, existing research, and existing playbooks to identify what's unvalidated, under-researched, or missing operational coverage.

## Inputs

Read ALL of these before analysis:

1. `{assumptions_file}` — key variables and their sources
2. `{decisions_file}` — strategic decisions and their evidence basis
3. `{run_dir}/assembled/business-plan-final.md` — assembled plan content
4. `docs/research/` — list all subdirectories (existing research coverage)
5. `docs/plans/` — list all playbook/plan files (existing operational coverage)
6. `{run_dir}/lifecycle-status.yaml` — artifact status and critique history

## Analysis 1: Research Gaps

For each assumption in `{assumptions_file}`, assess:

| Assumption | Source Quality | Research Coverage | Gap Severity |
|-----------|---------------|-------------------|-------------|
| {variable} | {Validated/Researched/Estimated/Asserted} | {link to research or "None"} | {Critical/High/Medium/Low/None} |

**Source Quality definitions:**
- **Validated** — backed by first-party data (e.g., Kelly's actual P&L)
- **Researched** — backed by deep-research or guided-exploration output
- **Estimated** — derived from industry benchmarks or analogies
- **Asserted** — stated without primary evidence

**Gap Severity criteria:**
- **Critical** — assumption is load-bearing for Year 1 execution and has no research backing
- **High** — assumption affects financial model or competitive positioning, has weak evidence
- **Medium** — assumption affects Years 2-3 execution, has partial evidence
- **Low** — assumption affects long-term thesis, has partial evidence
- **None** — adequately researched or validated

For each decision in `{decisions_file}`, assess:
- Is the evidence basis still current?
- Are there downstream implications that haven't been researched?
- Did the decision reference research that has since been superseded?

Additionally, scan the assembled plan for:
- Claims tagged `<!-- NEEDS-RESEARCH -->`
- Assertions using hedging language ("likely", "approximately", "we believe") without citations
- Financial projections that depend on unresearched market dynamics
- Competitive claims that lack direct evidence

### Research Gap Output

Present gaps in three tiers:

**Tier 1 — Research before first deal:**
| # | Topic | Why Critical | Blocked Assumptions | Suggested Method |
|---|-------|-------------|---------------------|-----------------|
| {n} | {topic} | {what fails without this} | {assumption refs} | {/deep-research or /guided-exploration + scoping notes} |

**Tier 2 — Research before Year 2:**
(same table format)

**Tier 3 — Research to validate long-term thesis:**
(same table format)

## Analysis 2: Playbook Gaps

Inventory existing playbooks and operational documents:
- List each playbook/plan in `docs/plans/` with a one-line summary
- List each research output in `docs/research/` with a one-line summary

Cross-reference against the operational model described in the plan. For each major operational domain, assess coverage:

| Domain | Existing Coverage | Gap | Priority |
|--------|------------------|-----|----------|
| Deal sourcing & pipeline | {what exists} | {what's missing} | {Critical/High/Medium/Low} |
| Deal execution & close | {what exists} | {what's missing} | {Critical/High/Medium/Low} |
| Post-acquisition integration | {what exists} | {what's missing} | {Critical/High/Medium/Low} |
| Client retention & growth | {what exists} | {what's missing} | {Critical/High/Medium/Low} |
| Advisory conversion | {what exists} | {what's missing} | {Critical/High/Medium/Low} |
| Technology platform | {what exists} | {what's missing} | {Critical/High/Medium/Low} |
| Talent & staffing | {what exists} | {what's missing} | {Critical/High/Medium/Low} |
| Capital & financing | {what exists} | {what's missing} | {Critical/High/Medium/Low} |
| Regulatory & compliance | {what exists} | {what's missing} | {Critical/High/Medium/Low} |
| Seller sourcing & relationships | {what exists} | {what's missing} | {Critical/High/Medium/Low} |

**Priority criteria:**
- **Critical** — needed before first bolt-on acquisition
- **High** — needed in Year 1
- **Medium** — needed by Year 2-3
- **Low** — needed for long-term scaling

### Playbook Gap Output

Present recommended playbooks:

**Must-have (before first deal):**
| # | Playbook | Scope | Dependencies |
|---|----------|-------|-------------|
| {n} | {name} | {what it covers} | {research that should come first} |

**Should-have (Year 1-2):**
(same table format)

**Nice-to-have (Year 2+):**
(same table format)

## Analysis 3: Cross-Reference

Identify research that should feed into playbook development:
- Which research gaps, once filled, would directly inform a missing playbook?
- Which playbooks could be started now with existing research, and which are blocked?
- What's the optimal sequencing? (research X → playbook Y → research Z → playbook W)

### Recommended Execution Order

Present a prioritized action list:

| # | Action | Type | Depends On | Unlocks |
|---|--------|------|-----------|---------|
| {n} | {description} | {Research/Playbook} | {prior action # or "None"} | {downstream action #s} |

## Presentation

After completing all three analyses, present:

1. **Executive summary** — 3-5 sentence overview of gaps and recommended priorities
2. **Research gaps** (Tier 1/2/3 tables)
3. **Playbook gaps** (Must-have/Should-have/Nice-to-have tables)
4. **Recommended execution order** (sequenced action list)
5. **Menu:** [DR] Start deep-research on top gap [GE] Start guided-exploration on top gap [PB] Start developing top playbook [DA] Done

### Menu Handling

- IF DR: Ask which research gap to investigate, then invoke `/deep-research` with the topic and scoping notes from the gap table
- IF GE: Ask which research gap to investigate, then invoke `/guided-exploration` with the topic and scoping notes from the gap table
- IF PB: Ask which playbook to develop, then begin collaborative playbook creation using the relevant agent (Victoria for strategy, Marcus for financial, Ray for operations, Diana for market)
- IF DA: Session complete
