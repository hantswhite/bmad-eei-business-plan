---
name: create-business-plan
description: 'Create a context-adaptive business plan with integrated strategy frameworks. Use when the user wants to create a business plan, strategic plan, or investor-ready plan.'
---

# Business Plan Workflow

**Goal:** Create comprehensive, context-adaptive business plans through collaborative step-by-step discovery. Integrates Wardley Mapping, Porter's Five Forces, PESTEL, Blue Ocean, VRIO, JTBD, Ansoff, and SWOT frameworks.

**Your Role:** Strategy Consultant (Victoria) as lead facilitator. Other specialist agents are invoked per step: Diana (Market Analyst) for market analysis and JTBD, Marcus (Financial Analyst) for unit economics and projections, Ray (Operations Planner) for GTM and operations, Eli (Plan Assembler) for final assembly and validation.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self contained instruction file that is a part of an overall workflow that must be followed exactly
- **Just-In-Time Loading**: Only the current step file is in memory - never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimization allowed
- **State Tracking**: Document progress in output file frontmatter using `stepsCompleted` array when a workflow produces a document
- **Artifact-Per-Step Output**: Each step writes to its own artifact file. The lifecycle module manages quality gates between steps. Final assembly happens only after all artifacts reach FINAL status.
- **Document Lifecycle**: Each step produces an independent artifact file. Artifacts progress through DRAFT > CRITIQUE > REVISED > FINAL REVIEW > FINAL before the next step begins. The lifecycle module orchestrates between-step quality gates.

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: If the step has a menu with Continue as an option, only proceed to next step when user selects 'C' (Continue)
5. **SAVE STATE**: Update `stepsCompleted` in frontmatter before loading next step
6. **LOAD NEXT**: When directed, read fully and follow the next step file
7. **LIFECYCLE GATE**: After completing a step, hand control to the lifecycle module. The lifecycle module manages critique, revision, consistency review, and dependency gating before the next step loads. Exception: critique-exempt steps (00 and 01) update `lifecycle-status.yaml` directly and proceed to the next step — the lifecycle module would immediately advance them to FINAL, so they bypass it for efficiency.
8. **REFERENCE CONTEXT**: If `{run_dir}/reference-brief.md` exists, read the section headed `## For Step {current_step_number}` before beginning facilitation. Present the extracted evidence to the user as a starting point: "Based on your reference documents, here's what I have as a starting point for this section: [evidence]. Let's validate and build on this together." Do NOT treat reference evidence as confirmed — it must be validated through the normal collaborative process.

### Critical Rules (NO EXCEPTIONS)

- **NEVER** load multiple step files simultaneously
- **ALWAYS** read entire step file before execution
- **NEVER** skip steps or optimize the sequence
- **ALWAYS** update frontmatter of output files when writing the final output for a specific step
- **ALWAYS** follow the exact instructions in the step file
- **ALWAYS** halt at menus and wait for user input
- **NEVER** create mental todo lists from future steps
- **ALWAYS** hand control to the lifecycle module after a step completes (critique-exempt steps handle their own status update)
- **NEVER** load the next step until the lifecycle module confirms all dependencies are FINAL
- **NEVER** assemble the final document until all artifacts are FINAL

---

## INITIALIZATION SEQUENCE

### 1. Configuration Loading

Load and read full config from {project-root}/_bmad/eei/config.yaml and resolve:

- `project_name`, `output_folder`, `planning_artifacts`, `user_name`, `communication_language`, `document_output_language`, `user_skill_level`, `assumptions_file`, `decisions_file`, `project_manifest`, `reference_documents`
- `lifecycle_status`, `persona_grid`, `critique_agent`, `lifecycle_module`, `consistency_review`

### 2. Lifecycle Module Loading

Read and load the lifecycle module from `{lifecycle_module}`. Follow its INITIALIZATION section to:
- Create the run directory at `{planning_artifacts}/business-plan-{project_name}-{date}/`
- Create subdirectories: `artifacts/`, `critiques/`, `assembled/`
- Initialize `lifecycle-status.yaml`
- Store `{run_dir}` variable

### 3. Reference Change Detection

Check if `{reference_documents}` directory exists and contains files (ignore `.gitkeep`).

- **IF empty or missing:** Skip to step 5.

Read `lifecycle-status.yaml` and check `reference_intake.last_run`:

- **IF `last_run` is null (first run):** Proceed to step 4 (first-time intake).
- **IF `last_run` has a value (prior intake exists):**
  - Compute SHA-256 hash for every file in `{reference_documents}/` (ignoring `.gitkeep`)
  - Compare computed hashes against `reference_intake.hashes` in `lifecycle-status.yaml`
  - Classify each file as: `added` (new file, no stored hash), `removed` (stored hash, no file), `modified` (hash mismatch), or `unchanged` (hash match)
  - **IF all files unchanged:** Skip re-intake. Resume workflow from wherever it left off (read `lifecycle-status.yaml` to determine current state, follow RECOVERY FROM INTERRUPTED SESSIONS).
  - **IF any files changed:** Set `{re_intake}` flag to true. Set `{reference_changes}` to the classified change list. Proceed to step 4 (re-intake).

### 4. Reference Intake

- **IF `{re_intake}` is true:** Hand control to the lifecycle module's REFERENCE RE-INTAKE PROCESSING section, passing `{reference_changes}`.
- **IF first run (no `{re_intake}` flag):** Read fully and follow: `{project-root}/_bmad/eei/business-plan/workflows/create-business-plan/steps/step-00-reference-intake.md`

### 5. First Step EXECUTION

Read fully and follow: `{project-root}/_bmad/eei/business-plan/workflows/create-business-plan/steps/step-01-context.md` to begin the workflow.
