---
name: 'step-14-pdf-generation'
description: 'Generate professional investor-facing PDFs from assembled business plan'

# File References
sourceFile: '{run_dir}/assembled/business-plan-final.md'
cssTemplate: '{project-root}/_bmad/eei/business-plan/templates/pdf-style.template.css'
outputDir: '{run_dir}/assembled'
dependsOn: [03-market-analysis, 04-competitive-positioning, 05-customer-problem, 06-solution-value-prop, 07-business-model, 08-go-to-market, 09-operations-team, 10-financial-projections, 11-risks-mitigants, 12-executive-summary]
---

# Step 14: PDF Generation

## STEP GOAL:

Generate two professional, investor-facing PDF documents from the assembled business plan: an executive summary PDF and a full business plan PDF. The assembled markdown is converted to HTML, styled with the project CSS template, and rendered via WeasyPrint. No plan content is modified — this step is purely a formatting and rendering operation.

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
- You bring deep expertise in document formatting, typesetting, and professional presentation
- We engage in collaborative dialogue, not command-response
- The user makes final decisions on any styling or formatting issues; you bring systematic rendering rigor

### Step-Specific Rules:

- Focus on converting the assembled plan to professional PDF output
- FORBIDDEN to modify plan content — only format for PDF output
- The Validation Report section is EXCLUDED from all investor-facing PDFs
- YAML frontmatter is EXCLUDED from all investor-facing PDFs
- CSS is loaded from the template file, NOT written inline
- This is a TERMINAL step — there is no next step
- There is NO "Continue" option in the menu — only Regenerate, Customize Styling, or Done

## EXECUTION PROTOCOLS:

- Show your analysis before taking any action
- Present all rendering results clearly with file sizes and page counts
- FORBIDDEN to proceed without user confirmation through menu
- FORBIDDEN to alter any plan text, numbers, or analysis — formatting and rendering only

## CONTEXT BOUNDARIES:

- Available context: Assembled business plan at {sourceFile}, CSS template at {cssTemplate}
- Focus: Markdown-to-HTML conversion, CSS styling, WeasyPrint rendering
- Limits: Do not modify plan content. Do not add new content or analysis. Do not edit the CSS template directly — local copies only.
- Dependencies: Step 13 must be complete — the assembled document at {sourceFile} must exist

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Verify Prerequisites

**Check Assembled Document:**
Verify that `{sourceFile}` exists and contains content. Read its frontmatter to extract `project_name`, `date`, and `version`.

**Check CSS Template:**
Verify that `{cssTemplate}` exists and is readable. Read its contents — this will be embedded in the HTML output.

- IF both exist: Proceed to PDF generation.
- IF assembled document missing: STOP. Report that Step 13 (Assembly & Validation) must be completed first. Do not proceed.
- IF CSS template missing: STOP. Report that the CSS template is missing at the expected path. Do not proceed.

**Share Status:**
"Prerequisites verified. The assembled business plan and CSS template are both present. Ready to generate investor-facing PDFs."

### 2. Prepare Executive Summary HTML

**Extract Executive Summary:**
Read `{sourceFile}` and extract only the Executive Summary section (the content under the `# Executive Summary` heading, up to the next `# ` heading).

**Convert to Metric-First HTML:**
The executive summary uses a custom investor-focused layout (NOT the shared plan CSS). Build a self-contained HTML document with inline styles optimized for scanability:

1. **Cover page** — project name + tagline describing the business in one line + subtitle "Executive Summary" + date + CONFIDENTIAL + version
2. **Key Metrics Bar** — 4-6 metric boxes in a flex row immediately after the cover. Extract the most important numbers from the content: raise amount, Y10 revenue, base MOIC, downside MOIC floor, total acquisitions, and "Day 1 EBITDA+" or equivalent. Each box: large value (16pt bold navy) + small uppercase label (7.5pt gray). Light background (#f0f4f8) with navy top border.
3. **Thesis Callout** — dark navy box (#1a3a5c background, white text) with 2-3 sentence investment thesis extracted from the content
4. **Sections** — restructure the executive summary content for scanability:
   - Use bullet points instead of prose for key statistics (The Opportunity)
   - Use highlight boxes (`<div class="highlight">`) for unit economics and key financial facts
   - Use side-by-side tables (2-column flex layout) for revenue tiers and deal structure
   - Consolidate return scenarios into a single table (Scenario × Multiple × EV × Equity × MOIC)
   - Tighten team credentials to one line per person
   - End with "The Ask" section featuring use-of-proceeds table + EBITDA highlight box
5. **Heading levels** — use `<h2>` for main sections, `<h3>` for subsections (no `<h1>` in body — the cover serves as the title)

The goal is 4-5 content pages where Page 1 (after cover) delivers the full thesis and key metrics in under 10 seconds of scanning.

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{custom exec summary CSS — see assembled/executive-summary.html for reference}
</style>
</head>
<body>
<div class="cover">
  <h1>{{project_name}}</h1>
  <p class="tagline">{{one-line business description}}</p>
  <p class="subtitle">Executive Summary</p>
  <p class="date">{{date}}</p>
  <p class="confidential">CONFIDENTIAL</p>
  <p class="version">v{{version}}</p>
</div>
<div class="metrics-bar">
  <div class="metric-box"><p class="metric-value">{{value}}</p><p class="metric-label">{{label}}</p></div>
  ...
</div>
<div class="thesis-box">
  <p class="thesis-label">The Thesis</p>
  <p>{{2-3 sentence investment thesis}}</p>
</div>
{restructured executive summary sections}
</body>
</html>
```

**Share Progress:**
"Executive summary HTML prepared with metric-first investor layout, cover page, and embedded styling."

### 3. Prepare Full Business Plan HTML

**Read Full Document:**
Read the complete `{sourceFile}`.

**Strip Excluded Sections:**
- Remove the `## Validation Report` section and everything below it (this is internal, not investor-facing)
- Remove YAML frontmatter (the `---` delimited block at the top of the file)
- KEEP the `## Glossary` section — it is investor-facing and should appear as the final section in the PDF (after Risks & Mitigants, before any stripped content)

**Convert to HTML:**
Convert the remaining markdown to HTML.

**Add Cover Page:**
Prepend a cover page div:

```html
<div class="cover">
  <h1>{{project_name}}</h1>
  <p class="subtitle">Business Plan</p>
  <p class="date">{{date}}</p>
  <p class="confidential">CONFIDENTIAL</p>
  <p class="version">v{{version}}</p>
</div>
```

**Generate Table of Contents:**
Scan the HTML for all `<h1>` elements. Build a table of contents div. Page numbers are rendered automatically by CSS via `target-counter()` — each `<a>` element's `::after` pseudo-element resolves to the target page number:

```html
<div class="toc">
  <h2>Table of Contents</h2>
  <ul>
    <li><a href="#section-id">Section Title</a></li>
    ...
  </ul>
</div>
```

Add `id` attributes to each `<h1>` element so the TOC links work. Add `class="section-break"` to each `<h1>` element so major sections start on a new page. The CSS template handles page number rendering — no additional HTML attributes are needed.

**Wrap with Full HTML Structure:**
Build the complete HTML document:

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{contents of cssTemplate}
</style>
</head>
<body>
{cover page div}
{table of contents div}
{business plan HTML content with section-break classes and IDs on H1 elements}
</body>
</html>
```

**Share Progress:**
"Full business plan HTML prepared with cover page, table of contents, and section breaks."

### 4. Render PDFs via WeasyPrint

**Render Executive Summary PDF:**
Use WeasyPrint to render the executive summary HTML to PDF:
- Output path: `{outputDir}/bp-{project_name}-executive-summary.pdf`
- Normalize `project_name` to lowercase with hyphens (replace spaces and special characters)

**Render Full Business Plan PDF:**
Use WeasyPrint to render the full business plan HTML to PDF:
- Output path: `{outputDir}/bp-{project_name}-business-plan.pdf`
- Normalize `project_name` to lowercase with hyphens (replace spaces and special characters)

**Report Results:**
For each PDF, report:
- File path
- File size (human-readable, e.g., "245 KB")
- Number of pages

**Share Results:**
"PDF generation complete.

**Executive Summary:**
- Path: `{outputDir}/bp-{project_name}-executive-summary.pdf`
- Size: {size}
- Pages: {count}

**Full Business Plan:**
- Path: `{outputDir}/bp-{project_name}-business-plan.pdf`
- Size: {size}
- Pages: {count}

Use [DP] Deliverables Package to consolidate all outputs (plan + playbooks + research) into `deliverables/`."

### 5. Ship PDFs

**Git Commit:**
Stage and commit the generated PDF files:

```bash
git add {outputDir}/bp-{project_name}-executive-summary.pdf {outputDir}/bp-{project_name}-business-plan.pdf {outputDir}/executive-summary.html {outputDir}/business-plan.html
git commit -m "pdf: generate investor PDFs v{version}"
```

**Share Status:**
"PDFs committed to the repository."

### 6. Present TERMINAL MENU

**This is a TERMINAL step — there is no "Continue" option.**

**Select an Option:** [RG] Regenerate PDFs [CS] Customize Styling [DP] Deliverables Package [DA] Done

#### Menu Handling Logic:

- IF RG: Return to [Step 4: Render PDFs via WeasyPrint](#4-render-pdfs-via-weasyprint) and re-render both PDFs from the existing HTML.
- IF CS: Copy the CSS template from `{cssTemplate}` to `{outputDir}/pdf-style.css` (if not already copied). Open the local copy for the user to edit. After edits, return to [Step 3: Prepare Full Business Plan HTML](#3-prepare-full-business-plan-html) to rebuild HTML with the updated CSS and re-render. The template at `{cssTemplate}` is canonical and is NOT modified — only the local copy in `{outputDir}` is edited.
- IF DP: Load and follow `{project-root}/_bmad/eei/business-plan/workflows/create-business-plan/steps/step-15-deliverables-package.md`
- IF DA: Session is complete. No further action required.
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#6-present-terminal-menu)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- There is NO "Continue" option — this is the final step
- User can chat or ask questions — always respond and then end with display again of the menu options
- [DP] chains to Step 15 for full deliverables packaging; [DA] ends the session

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Assembled document at {sourceFile} verified present before proceeding
- CSS template at {cssTemplate} verified present before proceeding
- Project name, date, and version extracted from assembled document frontmatter
- Executive summary section correctly extracted from assembled document
- Validation Report section excluded from all investor-facing PDFs
- YAML frontmatter excluded from all investor-facing PDFs
- Executive summary cover includes project name H1, tagline, subtitle, date, CONFIDENTIAL, and version
- Executive summary has key metrics bar (4-6 metric boxes) immediately after cover page
- Executive summary has thesis callout box with 2-3 sentence investment thesis
- Executive summary uses metric-first investor layout (bullets over prose, highlight boxes, 2-column tables, return scenarios table)
- Full business plan cover generated with project name H1, subtitle, date, CONFIDENTIAL, and version
- Full business plan includes generated table of contents in a `<div class="toc">` with CSS-driven page numbers
- Section breaks applied via `class="section-break"` on H1 elements
- CSS embedded from template file, not written inline
- Both PDFs rendered via WeasyPrint with correct output filenames
- File sizes and page counts reported to user
- PDFs committed with message `pdf: generate investor PDFs v{version}`
- Terminal menu presented with [RG] Regenerate [CS] Customize Styling [DP] Deliverables Package [DA] Done
- [DP] chains to Step 15 for full deliverables packaging
- [CS] edits a local copy in outputDir, never the canonical CSS template

### FAILURE:

- Proceeding without verifying assembled document and CSS template exist
- Modifying any plan content (text, numbers, analysis)
- Including the Validation Report section in investor-facing PDFs
- Including YAML frontmatter in investor-facing PDFs
- Writing CSS inline instead of embedding from the template file
- Editing the canonical CSS template at {cssTemplate} instead of a local copy
- Not generating cover pages for both PDFs
- Not generating a table of contents for the full business plan PDF
- Not adding section-break classes to H1 elements in the full plan
- Not reporting file sizes and page counts after rendering
- Not committing PDFs to git
- Including a "Continue" option (this is a terminal step)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
