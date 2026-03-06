---
name: lifecycle-reintake
description: 'Reference re-intake processing — handles reference document changes between sessions'
---

# Reference Re-Intake Processing

**Invoked by:** `lifecycle.md` when session-start reference change detection finds modified, added, or removed files in `{reference_documents}`.

---

## 1. Present Changes to User

"{user_name}, I've detected changes in your reference documents since the last intake ({reference_intake.last_run}):

| Change | Document |
|--------|----------|
| {Added/Modified/Removed} | {filename} |

I'll re-run reference intake and determine which plan sections are affected.

Ready to proceed?"

**Wait for user confirmation before proceeding.**

## 2. Archive Previous Brief

Copy `{reference_intake.brief_file}` to `{run_dir}/reference-brief-v{version}.md` as a versioned backup. This backup is used for comparison in step 4.

## 3. Execute Step 00 in Re-Intake Mode

Read fully and follow step-00-reference-intake.md. Step 00 detects re-intake mode via the `{re_intake}` flag set by workflow.md. In re-intake mode, step 00:
- Runs the full extraction pipeline on all documents (not just changed ones — evidence routing may shift)
- Writes the new brief to `{run_dir}/reference-brief.md`
- Updates `reference_intake.hashes` with new SHA-256 values for all files
- Updates `reference_intake.last_run` to current date
- During interactive review, focuses on changed sections only (see step 00 re-intake mode)

## 4. Produce Change Summary

After the new brief is finalized, compare it against the archived brief (`{run_dir}/reference-brief-v{version}.md`) section by section.

For each `## For Step {NN}` section:
- **No change**: Step is unaffected
- **Change detected**: Write an English summary of what changed (new evidence added, evidence removed, values updated, reclassified items)

Write the change summary to `{run_dir}/reference-change-summary-v{version+1}.md`:

```markdown
# Reference Change Summary — v{N} → v{N+1}

**Trigger:** Reference documents updated on {date}
**Files changed:** {list of added/modified/removed files}

## Step {NN}: {Step Name}
**Impact:** {English summary of what changed in this step's evidence}

## Steps unaffected: {comma-separated list of unaffected step numbers}
```

Present the change summary to the user.

## 5. Cascade Affected Steps

1. Set `00-reference-intake` status to FINAL (critique-exempt, new brief)
2. Increment `version` in `lifecycle-status.yaml`
3. For each step with a changed brief section:
   - Trigger cascade invalidation — set artifact to DRAFT
   - Walk dependency graph forward: for each artifact that depends on this one (directly or transitively), set to DRAFT
4. For each step with an unchanged brief section AND no invalidated dependency:
   - FAST-TRACK — keep FINAL status
   - Append audit note to artifact frontmatter: `auditNote: "Reviewed against reference intake v{N+1}; no material change to evidence base"`
5. Steps that are unchanged but have an invalidated dependency: triaged using existing CASCADE INVALIDATION triage process (load `lifecycle-cascade.md`, section: Triage Downstream Artifacts)

Log to `cascade_log`:

```yaml
- timestamp: "{date}"
  trigger: "00-reference-intake"
  reason: "Reference documents updated: {list of changed files}"
  invalidated: ["{list of all invalidated artifact IDs}"]
  fast_tracked: ["{list of fast-tracked artifact IDs}"]
  version_before: {N}
  version_after: {N+1}
```

## 6. Ship Re-Intake Results

Commit and push:
- `{run_dir}/reference-brief.md`
- `{run_dir}/reference-brief-v{version}.md` (archived previous)
- `{run_dir}/reference-change-summary-v{version+1}.md`
- `lifecycle-status.yaml`

Commit message: `intake: re-run reference intake v{N+1}`

## 7. Resume Cascade Processing

For each invalidated artifact, in dependency order, follow the cascade triage process in `lifecycle-cascade.md`. Each triage verdict (REVISE or FAST-TRACK) triggers a ship commit per the SHIP-IT INTEGRATION rules in `lifecycle.md`.

When all artifacts are FINAL again:
- If step 13 assembly had previously completed: re-run step 13 to reassemble
- If workflow was still in progress: resume from the next pending step via Dependency Gate
