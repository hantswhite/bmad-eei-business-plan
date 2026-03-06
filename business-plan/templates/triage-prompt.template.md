---
name: triage-prompt
description: 'Cascade revision triage — assesses whether upstream changes materially impact a downstream artifact'
---

# Triage Assessment Prompt

You are the {drafting_agent_persona} who originally produced `{downstream_artifact}`.

The following upstream artifact has been revised:
- **Artifact:** `{upstream_artifact}`
- **Changes:**

{diff_or_summary_of_changes}

---

Read `{downstream_artifact}` and assess:

## 1. Material Impact

Does this upstream change alter any claims, numbers, or reasoning in this artifact? For each affected section:
- **Section:** {section name}
- **What changes:** {description of required update}
- **Why:** {how the upstream change invalidates or alters this content}

## 2. No Impact

Which sections remain valid regardless of the upstream change? For each:
- **Section:** {section name}
- **Why unaffected:** {brief rationale}

## 3. Verdict

Select ONE:

- **REVISE** — Material changes needed. List specific changes required.
- **FAST-TRACK** — No material impact. Recommend restoring to FINAL with audit note: "Reviewed against v{version} changes to {upstream_artifact}; no material impact identified."
