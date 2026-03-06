---
name: consistency-review
description: 'Cross-artifact consistency review — identifies contradictions, assumption drift, strategic incoherence, repetition, and hedging'
---

# Consistency Review Module

**Purpose:** Review all artifacts plus governance files for cross-artifact issues using a summary-then-deep-dive approach (summarize each artifact individually, cross-compare summaries, then load only flagged artifact pairs for verification). Produces a conflicts file. Does NOT fix anything.

**Invoked by:** Lifecycle module at two points:
- **Pass 1:** When all artifacts reach REVISED status
- **Pass 2:** When pass 1 conflicts resolved and all artifacts reach FINAL REVIEW status

**Note:** The lifecycle module also performs a simpler dependency-scoped review inline (not via this module) when individual artifacts advance mid-workflow. This module is only invoked for the two full-pass reviews described above.

---

## Execution Sequence

### 1. Build Artifact Summaries (Context-Efficient)

Read `{run_dir}/lifecycle-status.yaml` to get the artifact list. Then, for each non-exempt artifact (skip `critiqueExempt: true`), read it and produce a **structured summary** (do NOT hold all artifacts in context simultaneously):

For each artifact, extract and store:
- **Key metrics:** Every number, percentage, dollar figure, timeline, or target with its exact value
- **Strategic positions:** Core claims about market, competition, customer, strategy
- **Cross-references:** Any explicit mention of another artifact's content
- **Governance values:** Any value that should trace to `{assumptions_file}` or `{decisions_file}`

Write each summary as a working note (not saved to disk — held in session context). Each summary should be 5-10 lines maximum.

After all summaries are built, read:
- `{assumptions_file}`
- `{decisions_file}`

### 2. Cross-Compare Summaries for Flags

Compare all summaries against each other and against governance files. Identify **potential issues** — cases where:
- The same metric appears with different values across summaries
- A strategic position in one summary contradicts another
- A governance value doesn't match an artifact's summary
- A fact appears in 3+ summaries (potential redundancy)
- Hedge language is used for a claim that governance files substantiate

Record each flag with: the issue type, which 2-3 artifacts are involved, and what specifically looks wrong.

### 3. Deep-Dive Verification

For each flag from step 2, load ONLY the 2-3 relevant artifact files (not all artifacts) and verify whether the flag is a real issue or a false positive from summarization. This targeted loading keeps context usage proportional to actual issues found, not total artifact count.

Discard false positives. Promote confirmed issues to the appropriate check below.

### 4. Check for Contradictions Between Artifacts

For every factual claim, number, or strategic position that appears in more than one artifact, verify they are consistent. Flag any case where:
- The same metric appears with different values (e.g., TAM stated as $5B in market analysis but $4.2B in financial projections)
- A strategic position taken in one artifact contradicts a position in another
- A customer segment described differently across artifacts
- Timeline or milestone inconsistencies between operations and financials

### 5. Check for Assumption Drift

For every variable that should be in `{assumptions_file}` (TAM, SAM, SOM, CAGR, pricing, CAC, LTV, growth rate, churn, team size, costs):
- Verify the value used in each artifact matches the value in assumptions.md
- Flag any artifact that uses a value not present in assumptions.md
- Flag any assumption that has been updated but artifacts still reference the old value

### 6. Check for Strategic Incoherence

Assess whether the artifacts, taken together, tell a coherent story:
- Does the competitive positioning actually address the market dynamics identified?
- Does the solution actually solve the customer problems identified?
- Does the business model actually capture the value proposition described?
- Does the GTM strategy actually reach the customer segments identified?
- Do the financial projections actually reflect the business model and GTM strategy?
- Do the risks actually cover the vulnerabilities implied by the other artifacts?
- Does the executive summary accurately synthesize all of the above?

### 7. Check for Governance Violations

- Every number in every artifact must trace to an entry in `{assumptions_file}`
- Every strategic decision must be consistent with `{decisions_file}`
- If an artifact contradicts a recorded decision, flag it (the decision may need updating, or the artifact may be wrong — the user decides)
- **Governance file freshness:** Check that every quantitative value in `{assumptions_file}` and every strategic conclusion in `{decisions_file}` matches the current artifact values. Governance files are the single source of truth — if they contain stale values from a prior model version, flag as BLOCKING. This is the most common source of governance drift: artifacts are revised through the critique cycle but governance files are not updated in sync.

### 8. Check for Cross-Artifact Repetition

For every fact, statistic, or argument that appears in more than two artifacts, assess whether each occurrence adds incremental value:

- **Canonical occurrence:** The artifact where the fact is most detailed, most contextually important, or first introduced in the dependency chain
- **Value-adding occurrence:** A different artifact where the fact is applied in a new context, combined with new data, or used to support a distinct argument
- **Redundant occurrence:** An artifact where the fact is restated without adding new context, application, or insight

Flag redundant occurrences as WARNING with:
- The repeated content (exact text or paraphrase)
- Which artifacts contain it (with section references)
- Which artifact is canonical
- Recommendation: remove from non-canonical locations, or replace with a brief cross-reference

### 9. Check for Hedging & Softening

For every claim in every artifact that uses hedge language ("may", "could", "potentially", "approximately", "estimated ~", "around", "roughly"):

1. Check if the claim is backed by a specific entry in `{assumptions_file}` or by evidence in the project's research outputs (`docs/research/`)
2. IF backed by evidence: Flag as WARNING — the language softens what the evidence supports. Recommend direct restatement.
3. IF NOT backed by evidence: Flag as WARNING — the claim is unsubstantiated. Recommend either:
   - Running `/deep-research` or `/guided-exploration` to substantiate
   - Removing the claim
   - Explicitly marking as `<!-- NEEDS-RESEARCH: {description} -->`
4. Do NOT recommend adding more hedge words as a fix.

### 10. Produce Conflicts File

Write findings to `{run_dir}/conflicts-pass-{pass_number}.md` using this format:

```markdown
# Consistency Review — Pass {pass_number}

**Date:** {date}
**Artifacts reviewed:** {count}
**Pass:** {pass_number} of 2

---

## BLOCKING Issues

### Contradiction: {short title}
- **Artifacts:** {which files conflict}
- **Details:** {what the conflict is, with specific quotes/numbers}
- **Severity:** BLOCKING
- **Suggested resolution:** {which artifact should be authoritative and why}

---

## WARNING Issues

### Inconsistency: {short title}
- **Artifacts:** {which files are affected}
- **Details:** {what the issue is}
- **Severity:** WARNING
- **Note:** {why this is a warning, not blocking}

### Repetition: {fact or statistic}
- **Artifacts:** {list of artifacts containing this fact}
- **Canonical location:** {artifact where it belongs}
- **Redundant in:** {artifacts where it should be removed or cross-referenced}
- **Severity:** WARNING
- **Recommendation:** Remove from {artifacts} or replace with cross-reference to {canonical artifact}

### Hedging: {claim text}
- **Artifacts:** {which artifacts contain this claim}
- **Evidence:** {source in assumptions.md or research, or "none found"}
- **Severity:** WARNING
- **Recommendation:** {Restate directly / Run /deep-research / Remove}

---

## Summary

- **BLOCKING issues:** {count}
- **WARNING issues:** {count}
- **Assessment:** {CLEAN — no blocking issues | NEEDS RESOLUTION — blocking issues must be addressed}
```

### 11. Return to Lifecycle Module

Report findings back to the lifecycle module:
- If CLEAN: all artifacts can advance to next lifecycle stage
- If NEEDS RESOLUTION: lifecycle module presents conflicts to user for resolution
