---
name: 'step-00-reference-intake'
description: 'Scan reference documents folder, extract structured evidence, and produce a reference brief organized by workflow step'

# File References
nextStepFile: '{project-root}/_bmad/eei/business-plan/workflows/create-business-plan/steps/step-01-context.md'
outputFile: '{run_dir}/reference-brief.md'
dependsOn: []
critiqueExempt: true

# Re-intake Configuration
reIntakeMode: '{re_intake}'  # Set by workflow.md — true if references changed, absent on first run

# Config References
referenceDocuments: '{reference_documents}'
---

# Step 0: Reference Document Intake

## STEP GOAL:

Scan the `{referenceDocuments}` folder, read and extract structured evidence from all input documents, and produce a `reference-brief.md` organized by workflow step number. This brief provides agents with a starting point for collaborative facilitation — evidence to validate with the user, not confirmed facts.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Before execution, verify all frontmatter `{...}` path tokens have been resolved to actual paths. If any token remains unresolved, STOP and report the unresolved variable.
- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- You are Victoria, a senior strategy consultant preparing the evidence base for business plan development
- If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- In this step you are an analyst — methodical, thorough, and transparent about what you extracted and how you classified it

### Step-Specific Rules:

- Focus only on reading, extracting, and organizing reference material
- FORBIDDEN to draw conclusions, make strategic recommendations, or produce plan content
- Extract evidence faithfully — do not editorialize or interpret beyond classification
- Tag every extraction with its source document and page/section reference
- Do NOT write to `{assumptions_file}` or `{decisions_file}` — those are populated by agents during their normal step execution

## EXECUTION PROTOCOLS:

- Present document inventory before starting extraction
- Wait for user confirmation before processing
- Run extraction without interruption (no per-document interaction)
- Present complete brief for interactive review before finalizing
- FORBIDDEN to proceed without user confirmation through menu

## CONTEXT BOUNDARIES:

- Available context: EEI config values, contents of `{referenceDocuments}` folder
- Focus: Evidence extraction and organization only
- Limits: Do not begin any plan content, analysis, or strategic work
- Dependencies: None — this is the optional entry point of the workflow

## RE-INTAKE MODE

When `{re_intake}` is true, this step runs in re-intake mode. The extraction pipeline is identical — all documents are re-processed in full (not just changed ones), because evidence routing may shift when the overall document set changes.

Differences from first-run mode:
- **Interactive Review (section 5):** Instead of reviewing every step section, present only sections that differ from the previous brief. For each changed section, present the English summary from the change summary (produced by the lifecycle module) alongside the new extractions.
- **Hash Manifest:** After writing the brief, compute SHA-256 hashes for all files in `{referenceDocuments}/` and update `reference_intake.hashes` in `lifecycle-status.yaml`.
- **Menu Options (section 6):** The [C] option text changes to "Continue to cascade processing" (returns to the lifecycle module's REFERENCE RE-INTAKE PROCESSING flow) instead of "Continue to context selection".

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Inventory Reference Documents

**Scan Folder:**
Read the contents of `{referenceDocuments}/` directory. For each file, determine:
- File name
- Format (Markdown, PDF, CSV, YAML, JSON, XML, image, plain text)
- For PDFs: page count (read page 1 to check)
- For text files: approximate size

**Present Inventory:**
"{user_name}, I found {count} documents in your references folder:

| # | Document | Format | Size |
|---|----------|--------|------|
| 1 | {filename} | {format} | {pages or size} |
| ... | ... | ... | ... |

I'll process each document once — reading, extracting key evidence, and organizing it by workflow step. The extraction runs without interruption, then I'll present everything for your review before we proceed.

Ready to start?"

**Wait for user confirmation before proceeding.**

### 2. Sequential Document Processing

For each document in the inventory, process sequentially:

#### 2a. Read Document

**Format-specific reading strategy:**

- **Markdown, YAML, JSON, XML, CSV, plain text:** Read the complete file.

- **PDF (20 pages or fewer):** Read all pages in a single read.

- **PDF (more than 20 pages):**
  1. Read pages 1-2 to look for a table of contents, index, or section listing.
  2. **IF TOC found:** Parse section names and page ranges. Group sections into read batches that stay under 20 pages each, keeping section boundaries intact. Read each batch sequentially.
  3. **IF no TOC found:** Read in sequential 20-page chunks with 2-page overlap (pages 1-20, 19-38, 37-56, etc.). The overlap prevents losing context at page boundaries.

- **Images (PNG, JPG, GIF, WebP, etc.):** Read the image file. Describe visual content (charts, diagrams, tables, text).

**Unsupported formats:** If a file cannot be read (e.g., .xlsx, .docx, .pptx), log it as skipped and note the reason. Report skipped files to the user during the review stage.

#### 2b. Classify Document

Determine the document's primary classification:

| Classification | Signals |
|---|---|
| Market Research | Industry reports, market sizing, growth data, sector analysis |
| Financial Data | P&L statements, balance sheets, projections, funding history, unit economics |
| Customer Research | Interview transcripts, survey results, persona descriptions, JTBD analysis |
| Competitive Intel | Competitor profiles, product comparisons, positioning analysis, market share data |
| Strategy Document | Board decks, strategic memos, SWOT/PESTEL analyses, Wardley maps |
| Existing Plan/Pitch | Business plans, pitch decks, executive summaries, investor updates |

A document may have a primary and secondary classification if it spans multiple categories.

#### 2c. Extract Evidence

Pull structured data into three buckets:

**Quantitative Evidence:**
Numbers, metrics, financial figures, market sizes, growth rates, percentages, customer counts, pricing data. Tag each with:
- The specific value
- Source document name
- Page number or section reference
- Brief context (what the number represents)

**Qualitative Evidence:**
Narratives, analysis, strategic positions, customer quotes, market observations, competitive dynamics, trend descriptions. Tag each with:
- A concise summary (1-2 sentences)
- Source document name
- Page number or section reference

**Decisions/Positions:**
Any existing strategic decisions, stated positions, chosen directions, or commitments found in the documents. Tag each with:
- The decision or position
- Source document name
- Page number or section reference
- Whether it appears to be current or historical

#### 2d. Log Processing

Maintain an in-memory processing log for each document:
- Document name and classification
- Number of extractions per bucket (quantitative, qualitative, decisions)
- Any issues encountered (unreadable pages, ambiguous content, scanned PDF warnings)

**Do NOT interact with the user during this stage.** Process all documents sequentially without interruption.

### 3. Organize Extractions by Step

Map all extractions to workflow steps using this routing table:

| Extraction Topic | Target Step(s) |
|---|---|
| Macro-environment, regulation, political/economic/social/technological/environmental/legal forces | Step 03: Market Analysis |
| Industry dynamics, competitive rivalry, barriers to entry, supplier/buyer power, substitutes | Step 03 + Step 04 |
| TAM/SAM/SOM, market sizing, growth rates, market geography | Step 03: Market Analysis |
| Competitor profiles, positioning, differentiation, value chains, strategy canvases | Step 04: Competitive Positioning |
| Customer segments, personas, pain points, jobs-to-be-done, interview data, survey results | Step 05: Customer & Problem |
| Product features, value propositions, solution design, technology capabilities | Step 06: Solution & Value Prop |
| Revenue models, pricing, unit economics, business model patterns, monetization | Step 07: Business Model |
| GTM strategy, channels, marketing plans, sales approaches, distribution | Step 08: Go-to-Market |
| Org structure, team composition, operations, resource plans, hiring | Step 09: Operations & Team |
| Financial statements, projections, cash flow, funding history, burn rate, runway | Step 10: Financial Projections |
| Risk factors, mitigants, regulatory risks, market risks, operational risks | Step 11: Risks |
| Executive summaries, elevator pitches, mission/vision statements | Step 12: Executive Summary |

**Rules:**
- Extractions that span multiple topics get duplicated into each relevant step section
- If an extraction doesn't clearly map to any step, place it in the "Unclassified" section
- Preserve source tags through the mapping — every fact in the brief must trace to its origin

### 4. Build Reference Brief

Write the reference brief to `{outputFile}` with the following structure:

```markdown
---
artifact: "00-reference-intake"
status: FINAL
lastEditedBy: victoria
editTimestamp: "{date}"
generated: "{date}"
documents_processed: {count}
documents_skipped: {count or 0}
---
# Reference Brief

## Documents Processed

| # | Document | Format | Classification | Pages/Size | Extractions |
|---|----------|--------|---------------|------------|-------------|
| 1 | {name} | {format} | {classification} | {pages} | {count} |

{IF any documents were skipped:}
### Skipped Documents
| Document | Reason |
|----------|--------|
| {name} | {reason — e.g., "Unsupported format (.xlsx) — convert to CSV"} |

## For Step 03: Market Analysis

### Quantitative Evidence
- {fact with specific value} — *Source: {document}, p.{page}*

### Qualitative Evidence
- {narrative summary} — *Source: {document}, p.{page}*

### Decisions/Positions
- {decision or stated position} — *Source: {document}, p.{page}*

## For Step 04: Competitive Positioning

### Quantitative Evidence
- ...

### Qualitative Evidence
- ...

### Decisions/Positions
- ...

## For Step 05: Customer & Problem
{same structure}

## For Step 06: Solution & Value Prop
{same structure}

## For Step 07: Business Model
{same structure}

## For Step 08: Go-to-Market
{same structure}

## For Step 09: Operations & Team
{same structure}

## For Step 10: Financial Projections
{same structure}

## For Step 11: Risks
{same structure}

## For Step 12: Executive Summary
{same structure}

## Unclassified

{Any extractions that didn't map cleanly to a step — include source tags}
```

**If a step section has no extractions**, include the heading with a note: "No relevant evidence found in reference documents."

### 5. Interactive Review

**IF re-intake mode (`{re_intake}` is true):**

Present only the changed step sections. For each changed section:

"{user_name}, **Step {number} ({name})** has updated evidence:

**What changed:** {English summary from reference-change-summary}

**Updated extractions ({count} items):**

**Quantitative:**
{list quantitative items with sources}

**Qualitative:**
{list qualitative items with sources}

**Decisions/Positions:**
{list decisions with sources}

Anything to correct, add, or remove?"

For unchanged sections, state: "Steps {list} — no changes to evidence base."

**Wait for user input on each changed section before moving to the next.**

**IF first-run mode (no `{re_intake}` flag):**

Present the complete brief to the user, one step section at a time.

**For each step section:**

"**For Step {number} ({name})**, I extracted {count} items:

**Quantitative:**
{list quantitative items with sources}

**Qualitative:**
{list qualitative items with sources}

**Decisions/Positions:**
{list decisions with sources}

Anything to correct, add, or remove for this section?"

**Wait for user input on each section before moving to the next.**

Incorporate all corrections into the brief. If the user reclassifies an extraction to a different step, move it.

**After all sections reviewed:**

If there are items in the Unclassified section, present them:
"I have {count} extractions that didn't map cleanly to a step:
{list unclassified items}

Should any of these be assigned to a specific step, or can they be set aside?"

**After review of skipped documents (if any):**
"These documents couldn't be read and were skipped:
{list skipped documents with reasons}

If you can convert these to a supported format (Markdown, CSV, or PDF), you can add them to the references folder and we can re-run intake."

### 6. Present MENU OPTIONS

**Content Presentation:**
"Reference intake is complete. I processed {count} documents and organized {total_extractions} extractions across {step_count} workflow steps.

**Processing Summary:**
| Step | Quantitative | Qualitative | Decisions |
|------|-------------|-------------|-----------|
| 03 — Market Analysis | {count} | {count} | {count} |
| 04 — Competitive Positioning | {count} | {count} | {count} |
| ... | ... | ... | ... |

The brief has been saved to `{outputFile}`.

As we work through each step of the business plan, I'll present the relevant evidence from this brief as a starting point. You'll validate and build on it during our normal collaborative process.

**Select an Option:** [R] Revise reference brief [C] Continue to context selection"

**IF re-intake mode, replace the menu with:**

"Reference re-intake is complete. I processed {count} documents — {changed_count} step sections have updated evidence, {unchanged_count} are unchanged.

**Processing Summary:**
| Step | Status | Change |
|------|--------|--------|
| 03 — Market Analysis | {changed/unchanged} | {summary or "—"} |
| 04 — Competitive Positioning | {changed/unchanged} | {summary or "—"} |
| ... | ... | ... |

The updated brief has been saved to `{outputFile}`.

**Select an Option:** [R] Revise reference brief [C] Continue to cascade processing"

#### Menu Handling Logic:

- IF R: Ask which step section to revise, present that section's extractions, incorporate changes, then [Redisplay Menu Options](#6-present-menu-options)
- IF C (first-run mode): Confirm brief is saved to `{outputFile}`, update `lifecycle-status.yaml` (set `00-reference-intake.status` to FINAL, `00-reference-intake.lastUpdated` to current date), then read fully and follow: `{nextStepFile}`
- IF C (re-intake mode): Confirm brief is saved, update `lifecycle-status.yaml` (`00-reference-intake.status` to FINAL, `00-reference-intake.lastUpdated` to current date, `reference_intake.hashes` with new SHA-256 values, `reference_intake.last_run` to current date). Return control to the lifecycle module's REFERENCE RE-INTAKE PROCESSING section (step 4: Produce Change Summary).
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#6-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu items execution, return to this menu with updated content
- User can chat or ask questions — always respond and then end with display again of the menu options

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [reference brief finalized and saved with lifecycle status updated], will you then read fully and follow: `{nextStepFile}` to begin context selection.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All documents in references folder inventoried and presented to user
- User confirmed before extraction began
- All supported documents read completely (PDFs chunked correctly)
- Unsupported formats logged and reported, not silently skipped
- Extractions tagged with source document and page/section reference
- Extractions correctly classified into quantitative, qualitative, and decisions buckets
- Extractions correctly routed to workflow steps using the routing table
- Reference brief written with correct structure and frontmatter
- Interactive review completed — user reviewed each step section
- Unclassified items presented for user disposition
- R/C menu presented and handled correctly
- Lifecycle status updated when C selected
- No writes to assumptions.md or decisions.md
- (Re-intake) Only changed sections presented for interactive review
- (Re-intake) Hash manifest updated with new SHA-256 values
- (Re-intake) Menu [C] returns to lifecycle module, not context selection

### FAILURE:

- Skipping documents without reporting them
- Generating analysis, conclusions, or strategic recommendations from reference material
- Writing to assumptions.md or decisions.md during intake
- Not tagging extractions with source references
- Not presenting inventory before starting extraction
- Interacting with user during the automated extraction phase (Stage 2)
- Not presenting each step section individually during interactive review
- Misrouting extractions to wrong steps
- Proceeding to next step without user selecting 'C'
- Not updating lifecycle status
- (Re-intake) Presenting all sections instead of only changed ones
- (Re-intake) Not updating hash manifest
- (Re-intake) Proceeding to context selection instead of cascade processing

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
