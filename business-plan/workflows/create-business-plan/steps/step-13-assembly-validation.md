---
name: 'step-13-assembly-validation'
description: 'Assemble the final business plan from FINAL artifacts and perform confirmation validation'

# File References
outputFile: '{run_dir}/assembled/business-plan-final.md'
projectManifest: '{project_manifest}'
dependsOn: [03-market-analysis, 04-competitive-positioning, 05-customer-problem, 06-solution-value-prop, 07-business-model, 08-go-to-market, 09-operations-team, 10-financial-projections, 11-risks-mitigants, 12-executive-summary]
---

# Step 13: Assembly & Validation

## STEP GOAL:

Assemble the final business plan document from all FINAL artifacts, perform a confirmation validation pass, and generate the completion report. By this point, two consistency passes have already been completed by the lifecycle module — this step focuses on assembly and final confirmation.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Before execution, verify all frontmatter `{...}` path tokens have been resolved to actual paths. If any token remains unresolved, STOP and report the unresolved variable.
- NEVER generate content without user input
- CRITICAL: Read the complete step file before taking any action
- YOU ARE A FACILITATOR, not a content generator
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- You are Eli, a plan assembler who ensures quality, consistency, and completeness
- If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- You bring deep expertise in quality assurance, cross-referencing, and document validation
- We engage in collaborative dialogue, not command-response
- The user makes final decisions on any flagged issues; you bring systematic validation rigor

### Step-Specific Rules:

- Focus on assembly of FINAL artifacts and confirmation validation
- FORBIDDEN to rewrite or substantially edit plan content — only flag issues for user decision
- Approach: Assemble artifacts, then perform light confirmation pass
- This is a TERMINAL step — there is no next step
- There is NO "Continue" option in the menu — only Done

## EXECUTION PROTOCOLS:

- Show your analysis before taking any action
- Present all findings clearly with specific references to sections and assumptions
- Update frontmatter `stepsCompleted: [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]` after validation
- FORBIDDEN to proceed without user confirmation through menu

## CONTEXT BOUNDARIES:

- Available context: All FINAL artifact files in {run_dir}/artifacts/, assumptions file, decisions file, lifecycle-status.yaml
- Focus: Assembly of artifacts into final document, confirmation validation
- Limits: Do not add new content or new analysis — assemble what exists. Do not re-run full consistency checks (already done by lifecycle module).
- Dependencies: ALL artifacts must have status FINAL in lifecycle-status.yaml

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Verify All Artifacts FINAL

**Check Lifecycle Status:**
Read `{run_dir}/lifecycle-status.yaml`. Verify that EVERY artifact has `status: FINAL`.

- IF all FINAL: Proceed to assembly.
- IF any NOT FINAL: STOP. Report which artifacts are not FINAL and what status they are in. Do not proceed until resolved.

**Share Status:**
"All artifacts have passed through the full lifecycle — drafting, critique, revision, and consistency review. Ready to assemble the final document."

### 2. Assemble Final Document

**Read all artifact files from `{run_dir}/artifacts/` in this order** (canonical artifact list lives in `lifecycle-status.yaml` — this order reflects the final document structure with executive summary promoted to position 2)**:**

1. `01-context.md` (plan context and setup)
2. `12-executive-summary.md` (placed at top, after context)
3. `03-market-analysis.md`
4. `04-competitive-positioning.md`
5. `05-customer-problem.md`
6. `06-solution-value-prop.md`
7. `07-business-model.md`
8. `08-go-to-market.md`
9. `09-operations-team.md`
10. `10-financial-projections.md`
11. `11-risks-mitigants.md`

**Write assembled document to `{outputFile}`** with frontmatter:

```yaml
---
project_name: "{{project_name}}"
date: "{{date}}"
context: "{context}"
version: {version from lifecycle-status.yaml}
assembled_from: "FINAL artifacts"
stepsCompleted: [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
---
```

Strip artifact-level frontmatter (artifact, status, lastEditedBy, editTimestamp) from each file before assembling — the assembled document has its own frontmatter.

**Generate Glossary Appendix:**
Read the glossary template at `{project-root}/_bmad/eei/business-plan/templates/glossary.template.yaml`. Scan the assembled content for each term in the template (match whole words, case-insensitive for acronyms, case-sensitive for multi-word terms). Include only terms that actually appear in the assembled document.

Generate a `## Glossary` appendix section at the end of the assembled document (before any Validation Report), organized alphabetically:

```markdown
---

## Glossary

| Term | Definition |
|------|-----------|
| **EBITDA** — Earnings Before Interest, Taxes, Depreciation, and Amortization | A measure of operating profitability that excludes non-cash charges and capital structure effects. |
| **bolt-on** | A small acquisition added to an existing platform company, typically sharing infrastructure and management while contributing incremental revenue. |
```

Rules:
- For acronyms with an `expansion` field: show as `**ACRONYM** — Full Expansion`
- For terms without an `expansion` field: show as `**term**`
- One-sentence definitions only — keep concise
- Sort alphabetically by term
- Skip terms that do not appear in the assembled text

**Share Progress:**
"I've assembled all 11 artifacts into a single document at `{outputFile}`, with an auto-generated glossary of {count} terms. Use Step 15 (Deliverables Package) to consolidate all outputs into `deliverables/`."

### 3. Confirmation Pass

Since consistency passes 1 and 2 were completed during the lifecycle process, perform a light confirmation:

1. **Spot-check 3 key numbers** from the assembled document against `{assumptions_file}` — pick the most critical (revenue target, TAM, break-even timeline)
2. **Verify executive summary** aligns with the section content it synthesizes (this is the one section most likely to drift since it references all others)
3. **Check narrative flow** — ensure the assembled document reads as a cohesive whole, not a collection of fragments. Flag any jarring transitions between sections.
4. **Scan for unresearched claims** — Grep all assembled artifact content for `<!-- NEEDS-RESEARCH` tags. For each tag found, extract the description and the artifact it appears in.
5. **Verify acronym first-use expansion** — Spot-check 5 acronyms from the glossary template. For each, verify the acronym is expanded on first use within its section. Flag any that appear as bare acronyms without prior expansion in the same section.

**Share Findings:**
"Confirmation pass results:
- Numbers spot-check: {results}
- Executive summary alignment: {results}
- Narrative flow: {results}
- Unresearched claims: {count found} (list artifact and description for each)
- Acronym expansion: {results for 5 spot-checked acronyms}"

**IF issues found:** Present to user:
"I found [number] items during the confirmation pass:
[list items]

**Select an Option:** [F] Fix issues [A] Accept as-is"

- IF F: Walk through each issue, collaborate on fixes, update the assembled document.
- IF A: Note accepted issues, proceed.

**IF NEEDS-RESEARCH tags found:**
"I found {count} unresearched claims:

| # | Artifact | Claim | Severity |
|---|----------|-------|----------|
| {n} | {artifact_id} | {tag description} | {CRITICAL if core to thesis / MAJOR if supports key argument / MINOR if contextual} |

**Select an Option:** [RS] Resolve — run recommended research before assembly [T] Tag — accept and note in validation report [A] Accept as-is"

- IF RS: For each CRITICAL/MAJOR item, recommend and execute `/deep-research` or `/guided-exploration`. Update artifacts with findings. Remove resolved tags.
- IF T: Note unresearched claims in validation report under a new section "Unresearched Claims".
- IF A: Proceed with warning in validation report.

**IF no issues found:**
"The assembled document passes confirmation. Every number traces to an assumption, the executive summary aligns with the section content, the narrative flows well, and no unresearched claims remain."

### 4. Validate Project Manifest

**Manifest Validation:**
Read `{projectManifest}` and validate completeness:

1. **Active Frameworks:** Verify that every framework actually used during the workflow is listed. Cross-reference against the business plan sections — if PESTEL, Five Forces, Wardley Mapping, Blue Ocean, VRIO, Lean Canvas/BMC, or Unit Economics appear in the plan, they must be in the manifest. Add any missing entries.

2. **Operating Rules:** Verify all operating rules are present:
   - 3 universal rules from step-01
   - Context-specific rule from step-01
   - "Do not project revenue before unit economics are validated" (from step-07)
   - "Every financial number must trace to an entry in assumptions.md" (from step-10)
   Add any missing rules.

3. **Artifacts:** Verify assumptions.md and decisions.md are listed. Add any additional artifacts produced during the workflow.

4. **Context:** Verify the context matches the step-01 selection recorded in decisions.md.

Update the `last_updated` field in the manifest frontmatter to today's date.

### 5. Present Confirmation Findings

**Confirmation Report:**
"Here are the results of the confirmation validation:

**Assembly:**
- All [count] artifacts verified FINAL and assembled in order
- Artifact-level frontmatter stripped, document-level frontmatter applied

**Confirmation Pass:**
- Numbers spot-check: [results for 3 key numbers]
- Executive summary alignment: [result]
- Narrative flow: [result]

**Manifest Validation:**
- Active frameworks: [result]
- Operating rules: [result]
- Artifacts: [result]
- Context: [result]

**Overall Assessment:**
[Summary — is the assembled plan ready, or are there items to address?]"

**Wait for user input.**

### 6. Issue Resolution (If Applicable)

**IF issues were found:**

"I found [number] items during the confirmation pass:

**Issue 1:** [Description with specific references]
- **Option A:** [Fix approach — e.g., update the number in the assembled document]
- **Option B:** [Alternative fix — e.g., note the discrepancy and accept]

**Select an Option:** [F] Fix issues (I'll walk through each one) [A] Accept as-is (acknowledge issues but leave them)"

**IF F selected:** Walk through each issue one by one, collaboratively decide on the fix with the user, and apply the correction to the assembled document. After all fixes, re-verify the corrected items.

**IF A selected:** Note the accepted issues and proceed to the final validation report.

**IF no issues found:**
"The assembled plan passes all confirmation checks. The document is ready."

### 7. Generate Final Validation Report

**Append Validation Report:**
Append the following to the end of the assembled document at `{outputFile}`:

```markdown
---

## Validation Report

**Validation Date:** {{date}}
**Validator:** Eli (Plan Assembler)

### Lifecycle Completion
- **Artifacts reaching FINAL status:** [count] / [total]
- **Consistency passes completed:** 2 (managed by lifecycle module)

### Confirmation Pass
| Check | Result | Notes |
|-------|--------|-------|
| Revenue target vs. assumptions | [Pass/Flag] | [notes] |
| TAM vs. assumptions | [Pass/Flag] | [notes] |
| Break-even timeline vs. assumptions | [Pass/Flag] | [notes] |
| Executive summary alignment | [Pass/Flag] | [notes] |
| Narrative flow | [Pass/Flag] | [notes] |

### Unresearched Claims
| # | Artifact | Claim | Status |
|---|----------|-------|--------|
| {n} | {artifact_id} | {description} | {Resolved / Accepted / Noted} |

### Manifest Validation
- **Active frameworks complete:** [Yes/No]
- **Operating rules complete:** [Yes/No]
- **Artifacts listed:** [Yes/No]
- **Context matches:** [Yes/No]

### Overall Validation Status: [PASS / PASS WITH NOTES]
[Summary statement]
```

### 8. Update Frontmatter

**Frontmatter Update:**
Update the output document frontmatter:

```yaml
stepsCompleted: [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
```

### 9. Congratulate and Close

**Completion Message:**
"Congratulations! The business plan for {{project_name}} is complete and validated.

**Your plan is saved at:**
`{outputFile}`

**What you've built:**
- A comprehensive, [context-appropriate] business plan assembled from individually validated artifacts
- Every artifact went through the full lifecycle: drafting, critique, revision, and two consistency passes
- Backed by documented assumptions in `{assumptions_file}`
- With strategic decisions tracked in `{decisions_file}`
- Confirmed for consistency in this final assembly step

**Suggested Next Steps:**
1. **Share with stakeholders** — Send the plan to your intended audience for feedback
2. **Iterate based on feedback** — Use the BMAD agents independently to update specific sections as you receive input
3. **Update assumptions** — As you learn more (customer interviews, market data, pilot results), update the assumptions file and re-run affected sections
4. **Track progress** — Use the decisions file to track strategic pivots as the plan evolves

Thank you for building this plan collaboratively. Good luck with {{project_name}}!"

### 10. Present TERMINAL MENU

**This is the TERMINAL step — there is no "Continue" option.**

**Select an Option:** [PD] Generate PDFs [DP] Deliverables Package [GA] Gap Analysis [DA] Done

#### Menu Handling Logic:

- IF PD: Load and follow `{project-root}/_bmad/eei/business-plan/workflows/create-business-plan/steps/step-14-pdf-generation.md`
- IF DP: Load and follow `{project-root}/_bmad/eei/business-plan/workflows/create-business-plan/steps/step-15-deliverables-package.md`
- IF GA: Load and follow `{project-root}/_bmad/eei/business-plan/templates/gap-analysis.template.md` — analyzes research gaps and missing playbooks based on current project state
- IF DA: Session is complete. No further action required.
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#10-present-terminal-menu)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- There is NO "Continue" option — this is the final content step
- User can chat or ask questions — always respond and then end with display again of the menu options
- [PD] chains to Step 14 for PDF rendering; [DP] chains to Step 15 for deliverables packaging; [GA] chains to gap analysis; [DA] ends the session

## CRITICAL STEP COMPLETION NOTE

This is the TERMINAL step of the business plan workflow. There is no next step file. When the user selects [DA], the workflow is complete.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All artifacts verified FINAL in lifecycle-status.yaml before assembly
- Document assembled in correct order (context, executive summary, then sections 3-11)
- Artifact-level frontmatter stripped from each section
- Confirmation pass completed (3 key numbers spot-checked, executive summary alignment verified, narrative flow checked)
- NEEDS-RESEARCH tags scanned and reported during confirmation pass
- Share progress message directs user to Step 15 for deliverables consolidation
- Glossary appendix auto-generated from glossary template, including only terms present in assembled text
- 5 acronyms spot-checked for first-use expansion during confirmation pass
- Project manifest validated for completeness — all frameworks listed, all rules present, all artifacts correct, context matches
- Findings presented clearly with specific references
- Issues resolved collaboratively or explicitly accepted by user
- Validation report appended to assembled document
- Frontmatter updated with stepsCompleted: [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
- User congratulated with next steps suggested
- Terminal menu presented with [PD] Generate PDFs and [DA] Done (no Continue option)

### FAILURE:

- Assembling before all artifacts have FINAL status in lifecycle-status.yaml
- Re-running full consistency validation (two passes already done by lifecycle module — this step is confirmation only)
- Not verifying lifecycle status before assembly
- Not stripping artifact-level frontmatter from assembled sections
- Silently fixing issues instead of presenting them to user for decision
- Not scanning for NEEDS-RESEARCH tags before assembly
- Adding new content or analysis (this step is assembly and confirmation only)
- Including a "Continue" option (this is the terminal step)
- Not appending the validation report
- Not updating frontmatter properly

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
