---
name: lifecycle-cascade
description: 'Cascade invalidation — manages downstream artifact revision when a FINAL artifact is modified'
---

# Cascade Invalidation

**Invoked by:** `lifecycle.md` when a FINAL artifact needs revision, or by `lifecycle-reintake.md` / `lifecycle-research-sync.md` when upstream changes propagate.

---

## 1. Identify Trigger

User specifies which artifact to revise and provides the reason.

## 2. Invalidate

- Set trigger artifact to DRAFT
- Walk dependency graph forward: for each artifact that has the trigger in its `dependsOn` (directly or transitively), set status to DRAFT
- **Flag governance files for review:** Mark `{assumptions_file}` and `{decisions_file}` as requiring verification against the revised artifacts. Governance files must be updated as part of the cascade resolution — not deferred to consistency review.
- Increment `version` in `lifecycle-status.yaml`
- Log to `cascade_log`:

```yaml
- timestamp: "{date}"
  trigger: "{artifact_id}"
  reason: "{user-provided reason}"
  invalidated: ["{list of all invalidated artifact IDs}"]
  version_before: {N}
  version_after: {N+1}
```

## 3. Report Cascade

Present to user:

"**Cascade invalidation triggered by revision of {artifact_name}.**

The following artifacts have been reset to DRAFT and will need review:
{list of invalidated artifacts with their names}

Version incremented from {N} to {N+1}.

We'll start with your revision of {trigger_artifact}, then triage each downstream artifact."

## 4. Revise Trigger Artifact

User revises the trigger artifact with the original drafting agent. Full lifecycle: DRAFT > CRITIQUE > REVISED > FINAL REVIEW > FINAL.

## 5. Triage Downstream Artifacts

For each invalidated dependent, in dependency order:

1. Load triage prompt template from `{project-root}/_bmad/eei/business-plan/templates/triage-prompt.template.md`
2. Substitute: `{drafting_agent_persona}` (from agent that produced the artifact), `{downstream_artifact}`, `{upstream_artifact}`, `{diff_or_summary_of_changes}`, `{version}`
3. Execute triage assessment

**IF REVISE verdict:**
- Return to drafting agent for delta revision (targeted changes only)
- Revised artifact goes through full lifecycle (CRITIQUE > REVISED > FINAL REVIEW > FINAL)
- If the delta revision introduces material changes, cascade fires forward for not-yet-triaged artifacts

**IF FAST-TRACK verdict:**
- Set artifact status to FINAL
- Append audit note to artifact frontmatter:
  `auditNote: "Reviewed against v{N} changes to {upstream_artifact}; no material impact identified"`

4. Log triage results in `cascade_log` entry under `triage_results`:

```yaml
triage_results:
  "{artifact_id}": REVISE | FAST-TRACK
```

## 6. Final Consistency Check

Once all artifacts are FINAL again, run Consistency Pass 2 to catch anything triage missed.

## 7. Reassemble

Invoke Step 13 to reassemble `business-plan-final.md` from all FINAL artifacts.
