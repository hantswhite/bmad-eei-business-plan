---
name: lifecycle
description: 'Document lifecycle orchestration — manages artifact status, critique gating, cascade invalidation, consistency review, and assembly gating'
---

# Document Lifecycle Module

**Purpose:** Orchestrate between-step quality gates for the business plan workflow. After each step produces an artifact, this module manages its progression through DRAFT > CRITIQUE > REVISED > FINAL REVIEW > FINAL before allowing the next step to begin.

**Invoked by:** `workflow.md` after each step completes (user selects C).

---

## LIFECYCLE STAGES

| Stage | Status | Trigger |
|-------|--------|---------|
| 1 | DRAFT | Artifact file written by step |
| 2 | CRITIQUE | Lifecycle spawns isolated critique agent |
| 3 | REVISED | User incorporates critique feedback |
| 4 | FINAL REVIEW | Consistency check (dependency-scoped mid-workflow; full pass near end) |
| 5 | FINAL | Approved, ready for assembly or downstream use |

---

## GOVERNANCE FILE SYNC

**Rule:** `{assumptions_file}` and `{decisions_file}` are the single source of truth for all quantitative and strategic values. They must always reflect the latest artifact values.

**When to sync:**
1. **After every REVISED transition** — the drafting agent checks whether revised values are also tracked in governance files and updates them (see step 4 Menu Handling).
2. **During cascade invalidation** — governance files are flagged for review as part of the cascade (see CASCADE INVALIDATION step 2).
3. **During consistency review** — governance file accuracy is a first-class check (already enforced by `{consistency_review}` steps 3 and 5). BLOCKING issues in governance files are resolved before Pass 2.

**What to sync:** Any value that appears in both an artifact and a governance file — including but not limited to: EBITDA figures, exit multiples, MOIC, FCF trajectory, retention rates, advisory conversion rates, seller pool figures, pricing tiers, deal cadence, and debt metrics.

**Commit rule:** When governance files are updated during a REVISED transition, include them in the same commit as the artifact revision. When updated during consistency review resolution, commit separately with message: `fix(governance): sync {assumptions_file|decisions_file} with restated model v{version}`.

---

## INITIALIZATION

When the lifecycle module is first loaded (during workflow initialization):

1. **Create run directory** at `{planning_artifacts}/business-plan-{project_name}-{date}/`
2. **Create subdirectories:** `artifacts/`, `critiques/`, `assembled/`
3. **Initialize `lifecycle-status.yaml`** with:
   - `version: 1`
   - `context:` (set by step-01)
   - `created:` and `last_updated:` timestamps
   - All artifact entries with `status: null`, their `dependsOn` arrays, and `agent` assignments
   - Empty `cascade_log`
   - Two `consistency_reviews` entries (pass 1 and pass 2) with null timestamps
4. **Store `{run_dir}`** variable for use by all steps

### Initial lifecycle-status.yaml Structure

```yaml
version: 1
context: null  # Set by step-01: A (investor) | B (market-entry) | C (internal)
created: "{date}"
last_updated: "{date}"

reference_intake:
  last_run: null
  brief_file: null
  hashes: {}

research_registry:
  last_scan: null
  artifacts: []

artifacts:
  00-reference-intake:
    status: null
    agent: victoria
    dependsOn: []
    lastUpdated: null
    critiqueExempt: true

  01-context:
    status: null
    agent: victoria
    dependsOn: []
    lastUpdated: null
    critiqueExempt: true

  03-market-analysis:
    status: null
    agent: diana
    dependsOn: [01-context]
    lastUpdated: null
    critiqueAgent: market-analyst-critic
    critiqueFile: null

  04-competitive-positioning:
    status: null
    agent: victoria
    dependsOn: [01-context, 03-market-analysis]
    lastUpdated: null
    critiqueAgent: strategy-critic
    critiqueFile: null

  05-customer-problem:
    status: null
    agent: diana
    dependsOn: [03-market-analysis, 04-competitive-positioning]
    lastUpdated: null
    critiqueAgent: customer-critic
    critiqueFile: null

  06-solution-value-prop:
    status: null
    agent: victoria
    dependsOn: [04-competitive-positioning, 05-customer-problem]
    lastUpdated: null
    critiqueAgent: solution-critic
    critiqueFile: null

  07-business-model:
    status: null
    agent: victoria
    dependsOn: [05-customer-problem, 06-solution-value-prop]
    lastUpdated: null
    critiqueAgent: business-model-critic
    critiqueFile: null

  08-go-to-market:
    status: null
    agent: ray
    dependsOn: [05-customer-problem, 07-business-model]
    lastUpdated: null
    critiqueAgent: gtm-critic
    critiqueFile: null

  09-operations-team:
    status: null
    agent: ray
    dependsOn: [07-business-model, 08-go-to-market]
    lastUpdated: null
    critiqueAgent: operations-critic
    critiqueFile: null

  10-financial-projections:
    status: null
    agent: marcus
    dependsOn: [03-market-analysis, 04-competitive-positioning, 05-customer-problem, 06-solution-value-prop, 07-business-model, 08-go-to-market, 09-operations-team]
    lastUpdated: null
    critiqueAgent: financial-critic
    critiqueFile: null

  11-risks-mitigants:
    status: null
    agent: victoria
    dependsOn: [03-market-analysis, 04-competitive-positioning, 05-customer-problem, 06-solution-value-prop, 07-business-model, 08-go-to-market, 09-operations-team, 10-financial-projections]
    lastUpdated: null
    critiqueAgent: risks-critic
    critiqueFile: null

  12-executive-summary:
    status: null
    agent: eli
    dependsOn: [03-market-analysis, 04-competitive-positioning, 05-customer-problem, 06-solution-value-prop, 07-business-model, 08-go-to-market, 09-operations-team, 10-financial-projections, 11-risks-mitigants]
    lastUpdated: null
    critiqueAgent: executive-summary-critic
    critiqueFile: null

cascade_log: []

consistency_reviews:
  - pass: 1
    timestamp: null
    conflicts_file: null
  - pass: 2
    timestamp: null
    conflicts_file: null
```

---

## AFTER-STEP PROCESSING

When a step completes (user selects C) and the artifact file has been written:

**Context refresh rule:** Before each stage transition below, re-read `{lifecycle_status}` and `{project-root}/_bmad/eei/config.yaml` to ensure you are operating on current state. This prevents stale variable references after context compression in long sessions.

### 1. Update Lifecycle Status

Set artifact status to DRAFT in `lifecycle-status.yaml`. Update `lastUpdated` timestamp.

### 2. Check Critique Exemption

- IF artifact is `00-reference-intake` or `01-context`: Set status to FINAL. Skip to [Dependency Gate](#6-dependency-gate).
- ELSE: Continue to critique.

### 3. Spawn Critique Agent

**Invoke critique agent in isolation (no prior context).**

**Implementation note:** Use the Task tool (or equivalent isolated execution context) to invoke the critique agent. This ensures true context isolation — the critique agent must NOT have access to the drafting conversation or any prior artifacts beyond the one being critiqued.

Parameters to pass:
- `{artifact_id}` — e.g., `03-market-analysis`
- `{artifact_file}` — full path to artifact in `{run_dir}/artifacts/`
- `{context}` — A, B, or C from `lifecycle-status.yaml`
- `{critique_output_file}` — `{run_dir}/critiques/{artifact_id}-critique.md`
- `{date}` — current date

The critique agent will:
1. Load persona from `{persona_grid}` using artifact_id and context
2. Read the artifact cold
3. Produce critique at `{critique_output_file}`

Update `lifecycle-status.yaml`: set `critiqueFile` for this artifact.

### 4. Present Critique to User

Display the critique to the user:

"**Critique of {artifact_name}:**

{critique_content}

The critique has been saved to `{critique_output_file}`.

**Your options:**
[R] Revise this artifact based on the critique
[D] Dismiss critique and keep artifact as-is (status advances to REVISED)
[Q] Ask questions about the critique"

**Menu Handling:**
- IF R: Return to the drafting agent (the agent that produced this artifact). User revises collaboratively, applying the critique's condensation plan in addition to addressing logical/evidence issues. Specifically:
  - Execute recommended cuts from the critique's condensation plan (section 5)
  - Replace hedged language with direct statements where the critique identified supporting evidence
  - For substantiation gaps flagged by the critique, apply research enforcement policy from `{config.research_enforcement}`:
    - **CRITICAL gaps:** If policy is `strict`, MUST run `/deep-research` or `/guided-exploration` before advancing. If policy is `standard`, present as WARNING and recommend research. If policy is `permissive`, may tag with `<!-- NEEDS-RESEARCH: {description} -->`.
    - **MAJOR gaps:** If policy is `strict`, MUST run `/deep-research` or `/guided-exploration` before advancing (same as CRITICAL). If policy is `standard`, recommend research; may tag with `<!-- NEEDS-RESEARCH: {description} -->` if infeasible. If policy is `permissive`, may tag with `<!-- NEEDS-RESEARCH: {description} -->`.
    - **MINOR gaps:** May tag with `<!-- NEEDS-RESEARCH: {description} -->` or accept with directional language (all policies).
  - Do not add defensive qualifiers ("This is honest:", "Year 1 reality check:"), meta-commentary, or unnecessary framing
  - **Never reference prior versions, drafts, or revision history in artifact content.** Each artifact must read as if it was always this way. No "was X, now Y", "corrected from", "updated from v1", "previously stated", or similar changelog language. The artifact is the current truth — revision history lives in git, critiques, and consistency review files, not in the plan itself.
  - **Governance sync:** After revising, check whether any values changed in the artifact that are also tracked in `{assumptions_file}` or `{decisions_file}`. If so, update the governance files to match. This prevents governance drift — governance files are the single source of truth and must always reflect the latest artifact values.
  When done, update artifact file (and governance files if changed) and set status to REVISED.
- IF D: Set status to REVISED (user accepts current version despite critique). Append note to artifact frontmatter: `critiqueAction: dismissed`.
- IF Q: Answer questions, then redisplay options.

### 5. Consistency Check (Dependency-Scoped or Full)

**Check: Are ALL non-exempt artifacts at REVISED or better?**

- **IF YES (near end of workflow — all content steps complete):**
  - Run **Consistency Pass 1**: Load and follow `{consistency_review}` with `pass_number: 1`
  - IF BLOCKING conflicts found:
    - Present `conflicts-pass-1.md` to user
    - For each BLOCKING conflict: user decides which artifact is authoritative
    - Non-authoritative artifacts get delta-revised (return to drafting agent for targeted changes)
    - Delta-revised artifacts go through critique again
    - Re-run consistency pass 1 until clean
  - IF clean:
    - Set ALL artifacts to FINAL REVIEW
    - Run **Consistency Pass 2**: Load and follow `{consistency_review}` with `pass_number: 2`
    - IF BLOCKING conflicts: flag as unusual, present to user, resolve
    - IF clean:
      - **Run Editorial Sweep** before promoting to FINAL:
        - **Per-artifact editorial sweep:** For each artifact at FINAL REVIEW:
          1. Run editorial-review-structure check (load `{project-root}/_bmad/core/tasks/editorial-review-structure.xml`): pass the artifact content, purpose="business plan section for investor audience", target_audience="investors and board members", reader_type="humans"
          2. Run editorial-review-prose check (load `{project-root}/_bmad/core/tasks/editorial-review-prose.xml`): pass the artifact content, reader_type="humans"
          3. Present combined findings as WARNING-level items (not BLOCKING — the artifact is already consistent)
          4. User decides: [T] Tighten (return to drafting agent to apply editorial fixes) | [A] Accept as-is
          5. IF T: Drafting agent applies editorial recommendations, updates artifact file. Status remains FINAL REVIEW (no re-critique needed for editorial changes).
          6. IF A: Proceed to next artifact.
        - **Cross-artifact editorial sweep** (once, after all individual sweeps):
          1. Read all artifacts together. Identify facts, statistics, or arguments that appear in 3+ artifacts without adding incremental value.
          2. For each: identify the canonical location (the artifact where the fact is most detailed or contextually important), recommend removal or cross-reference from other artifacts.
          3. Present findings to user with specific cut recommendations.
          4. User approves or rejects each recommendation. Apply approved cuts.
          5. Commit editorial changes: `editorial: tighten artifacts before FINAL v{version}`
      - Set ALL artifacts to FINAL
    - Proceed to Step 13 (assembly)

- **IF NO (mid-workflow — still building artifacts):**
  - Note: This dependency-scoped review is performed inline by the lifecycle module — it does NOT invoke the full consistency-review module.
  - Run **dependency-scoped review** for this artifact only:
    - Read this artifact and all artifacts in its `dependsOn` list
    - Check for contradictions, assumption drift, and governance violations between them only
    - IF issues found: present to user, resolve, delta-revise as needed
    - IF clean: Set artifact to FINAL REVIEW, then FINAL
  - Proceed to [Dependency Gate](#6-dependency-gate)

### 6. Dependency Gate

Before loading the next step:

1. Read `lifecycle-status.yaml`
2. Identify the next step's artifact ID
3. Look up its `dependsOn` array
4. Check that ALL dependencies have status FINAL
5. IF all FINAL: Load and follow the next step file
6. IF not all FINAL: Report which dependencies are incomplete and what needs to happen

---

## SHIP-IT INTEGRATION

After every status update in `lifecycle-status.yaml` during AFTER-STEP PROCESSING, commit and push the changed files.

**Commit rules by transition:**

| Transition | Files to `git add` | Commit message |
|---|---|---|
| → DRAFT | `{run_dir}/artifacts/{artifact_id}.md`, `{run_dir}/lifecycle-status.yaml` | `draft({artifact_id}): produce artifact v{version}` |
| → CRITIQUE | `{run_dir}/critiques/{artifact_id}-critique.md`, `{run_dir}/lifecycle-status.yaml` | `critique({artifact_id}): adversarial review v{version}` |
| → REVISED | `{run_dir}/artifacts/{artifact_id}.md`, `{run_dir}/lifecycle-status.yaml`, `{assumptions_file}` and/or `{decisions_file}` (if changed) | `revise({artifact_id}): incorporate critique feedback v{version}` |
| → FINAL REVIEW | `{run_dir}/lifecycle-status.yaml`, `{run_dir}/conflicts-pass-{N}.md` (if produced) | `review({artifact_id}): consistency check v{version}` |
| → FINAL | `{run_dir}/lifecycle-status.yaml` | `final({artifact_id}): approved v{version}` |

**Additional commit points:**

| Event | Files to `git add` | Commit message |
|---|---|---|
| Re-intake complete | See REFERENCE RE-INTAKE PROCESSING section 6 | `intake: re-run reference intake v{N}` |
| FAST-TRACK (batch) | `{run_dir}/lifecycle-status.yaml` | `fast-track: {count} artifacts unchanged by intake v{N}` |
| Assembly | `{run_dir}/assembled/business-plan-final.md`, `{run_dir}/lifecycle-status.yaml` | `assemble: final business plan v{N}` |
| Editorial sweep | `{run_dir}/artifacts/*.md`, `{run_dir}/lifecycle-status.yaml` | `editorial: tighten artifacts before FINAL v{N}` |
| PDF generation | `{run_dir}/assembled/*.pdf`, `{run_dir}/assembled/*.html` | `pdf: generate investor PDFs v{N}` |

**Execution rules:**
- Always `git add` specific files by name — never use `git add -A` or `git add .`
- Commit with the conventional message pattern shown above
- `git push` to the current branch after each commit
- If no branch or PR exists yet, create the branch and open a PR on the first ship
- When multiple steps are FAST-TRACKED simultaneously (e.g., batch from re-intake), commit as a single commit
- Ship commits happen automatically — do not wait for user confirmation

**PR management:**
- First ship creates the branch (if needed) and opens a PR
- Subsequent ships push additional commits to the same branch
- After step 13 assembly, update the PR body with a summary of all versions produced during this run

---

## REFERENCE RE-INTAKE PROCESSING

**Load and follow** `lifecycle-reintake.md` (in this directory) when session-start reference change detection detects modified, added, or removed files in `{reference_documents}`.

---

## RESEARCH SYNC PROCESSING

**Load and follow** `lifecycle-research-sync.md` (in this directory) when session-start research scan or the `/eei-bp-research-sync` command detects new or changed research artifacts.

---

## CASCADE INVALIDATION

**Load and follow** `lifecycle-cascade.md` (in this directory) when a FINAL artifact needs revision.

---

## STATUS DISPLAY

When asked for lifecycle status (via slash command or during workflow):

Read `lifecycle-status.yaml` and present:

```
Document Lifecycle Status — v{version}

| Artifact | Status | Last Updated | Critique |
|----------|--------|-------------|----------|
| 00-reference-intake | {status} | {date} | exempt |
| 01-context | {status} | {date} | exempt |
| 03-market-analysis | {status} | {date} | {critique file or pending} |
| 04-competitive-positioning | {status} | {date} | {critique file or pending} |
| 05-customer-problem | {status} | {date} | {critique file or pending} |
| 06-solution-value-prop | {status} | {date} | {critique file or pending} |
| 07-business-model | {status} | {date} | {critique file or pending} |
| 08-go-to-market | {status} | {date} | {critique file or pending} |
| 09-operations-team | {status} | {date} | {critique file or pending} |
| 10-financial-projections | {status} | {date} | {critique file or pending} |
| 11-risks-mitigants | {status} | {date} | {critique file or pending} |
| 12-executive-summary | {status} | {date} | {critique file or pending} |

Consistency Reviews:
- Pass 1: {completed/pending} {date if completed}
- Pass 2: {completed/pending} {date if completed}

Next action: {what needs to happen next based on current state}
```

---

## RECOVERY FROM INTERRUPTED SESSIONS

When resuming a workflow after session interruption:

1. **Read `lifecycle-status.yaml`** to determine current state
2. **Identify the last completed action** based on artifact statuses:
   - All artifacts `null`: Workflow hasn't started — begin from step-01
   - An artifact at `DRAFT` with no `critiqueFile`: Step completed but critique not yet run — spawn critique
   - An artifact at `CRITIQUE` with a `critiqueFile`: Critique completed but not yet presented to user — present critique
   - An artifact at `REVISED`: Consistency check pending — run appropriate check
   - `cascade_log` with incomplete `triage_results`: Cascade interrupted mid-triage — resume from next un-triaged artifact
   - `reference_intake.last_run` differs from today AND reference hashes don't match current files: Reference change detected mid-session — hand to REFERENCE RE-INTAKE PROCESSING
   - `cascade_log` with trigger `00-reference-intake` and incomplete `triage_results`: Re-intake cascade interrupted — resume triage from next un-triaged artifact
   - `research_registry.last_scan` differs from today AND research file hashes don't match: New research detected — hand to RESEARCH SYNC PROCESSING
   - `cascade_log` with trigger `research-sync` and incomplete processing: Research sync cascade interrupted — resume from next un-revised artifact
3. **Resume from the identified point** following the normal lifecycle flow
