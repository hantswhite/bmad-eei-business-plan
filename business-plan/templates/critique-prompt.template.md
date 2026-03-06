---
name: critique-prompt
description: 'Adversarial critique prompt template — used by critique-agent.md with persona from persona-grid.yaml'
---

# Critique Prompt

You are {persona_description}.
You have NOT been involved in drafting this document.

Read `{artifact_file}` cold and provide:

1. **Claims likely to draw scrutiny** — The three claims most likely to draw scrutiny. For each: why it would be questioned, and what evidence is missing to support it.

2. **Internal inconsistencies** — Places where this section conflicts with itself. Specific references to the conflicting statements.

3. **Logical gaps** — Conclusions that don't follow from the evidence presented. Where the reasoning skips steps or assumes what it should prove.

4. **Preemptive response** — What a well-prepared {role} would say to preempt your strongest objection.

5. **Evidence & editorial discipline** — For each material claim in the artifact, assess substantiation and language:

   **Substantiation gaps:** Identify claims that lack a specific, citable source. For each: state the claim, classify severity, note what evidence is missing, and recommend whether `/deep-research` or `/guided-exploration` would resolve it. Do not recommend hedging or softening as a fix.

   Severity classification:
   - **CRITICAL** — Claim is core to the investment thesis, deal economics, or addressable market. Must be researched before artifact advances.
   - **MAJOR** — Claim supports a key argument or competitive positioning. Must be researched before artifact advances (under strict enforcement).
   - **MINOR** — Claim is contextual, illustrative, or supporting. Can be tagged `<!-- NEEDS-RESEARCH -->` or accepted with directional language.

   **Hedging language:** Identify instances where evidence exists (in the artifact itself, in assumptions.md, or in referenced research) but the language softens it with "may", "could", "potentially", "approximately", or "estimated". For each: quote the hedged text, cite the supporting evidence, and provide the direct restatement.

   **Redundancy within this artifact:** Identify content that restates the same point without adding value. For each: cite both locations and recommend which to keep and which to cut.

   **Undefined acronyms and jargon:** Identify acronyms used without expansion on first use within this artifact, and domain-specific terms (e.g., "bolt-on", "tuck-in", "roll-up", "earnout") used without inline definition for non-specialist readers. For each: cite the first occurrence and provide the expansion or definition that should be added.

   **Prior-version references:** Flag any language that references prior drafts, versions, or revision history (e.g., "was previously X", "corrected from", "updated in v2", "the earlier draft stated"). Each artifact must read as the current truth. Revision history belongs in git and critique files, not in plan content.

   Present as an actionable condensation plan the revision agent can execute.

Do not soften feedback. Flag weak reasoning explicitly rather than suggesting it "could be strengthened."

---

## Output Format

Write your critique to `{critique_output_file}` using this structure:

```
# Critique: {artifact_name}

**Critic:** {persona_description}
**Date:** {date}
**Artifact:** {artifact_file}

## Claims Under Scrutiny

### 1. {claim}
- **Why this draws scrutiny:** {reasoning}
- **Missing evidence:** {what's needed}

### 2. {claim}
- **Why this draws scrutiny:** {reasoning}
- **Missing evidence:** {what's needed}

### 3. {claim}
- **Why this draws scrutiny:** {reasoning}
- **Missing evidence:** {what's needed}

## Internal Inconsistencies

{list each with specific line/section references}

## Logical Gaps

{list each with the reasoning chain that breaks}

## Strongest Objection and Preemptive Response

**Objection:** {your strongest objection}
**What {role} should say:** {preemptive response}

## Evidence & Editorial Discipline

### Substantiation Gaps

| Claim | Severity | Missing Evidence | Recommended Action |
|-------|----------|-----------------|-------------------|
| {claim text} | CRITICAL / MAJOR / MINOR | {what's needed} | /deep-research: {query} OR /guided-exploration: {premise} |

### Hedging Language

| Hedged Text | Supporting Evidence | Direct Restatement |
|-------------|--------------------|--------------------|
| "{hedged quote}" | {evidence source} | "{direct version}" |

### Redundancy

| Content | Location 1 | Location 2 | Recommendation |
|---------|-----------|-----------|----------------|
| {repeated content} | {section/line} | {section/line} | Keep at {location}, cut from {location} |

### Undefined Acronyms & Jargon

| Term | First Occurrence | Expansion / Definition |
|------|-----------------|----------------------|
| {acronym or term} | {section/paragraph} | {expansion or plain-English definition} |

### Prior-Version References

| Text | Location | Rewrite |
|------|----------|---------|
| "{text referencing prior version}" | {section/paragraph} | "{rewrite as current truth}" |

### Condensation Plan

{Numbered list of specific actions for the revision agent to execute}

## Summary Verdict

{1-2 sentence overall assessment: is this artifact ready for revision, or does it need fundamental rework?}
```
