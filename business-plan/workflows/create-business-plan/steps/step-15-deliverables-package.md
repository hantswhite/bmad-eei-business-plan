---
name: 'step-15-deliverables-package'
description: 'Generate PDFs for all playbooks and research reports, consolidate into deliverables folder with associated documents section'

# File References
sourceDir: '{run_dir}/assembled'
deliverablesDir: '{project-root}/deliverables'
dependsOn: [03-market-analysis, 04-competitive-positioning, 05-customer-problem, 06-solution-value-prop, 07-business-model, 08-go-to-market, 09-operations-team, 10-financial-projections, 11-risks-mitigants, 12-executive-summary]

# CSS Template References
playbookCss: '{playbook_css_template}'
explorationCss: '{exploration_css_template}'
researchCss: '{research_css_template}'
planCss: '{project-root}/_bmad/eei/business-plan/templates/pdf-style.template.css'

# Source Paths
playbookSources: '{project-root}/docs/plans/*-playbook.md'
researchSources: '{project-root}/docs/research/*/report-*.md'
explorationSources: '{project-root}/docs/research/*/exploration-report.md'
---

# Step 15: Deliverables Package

## STEP GOAL:

Generate professional PDFs for all playbooks and research reports, consolidate all outputs (business plan + playbooks + research) into a single `deliverables/` folder with consistent `<type>-<slug>` naming, inject an Associated Documents section into the business plan, and produce a README manifest.

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

- Focus on PDF generation and file organization — do not modify any plan, playbook, or research content
- FORBIDDEN to alter any plan text, numbers, or analysis — formatting and rendering only
- The only content modification is injecting the Associated Documents section into the business plan copy
- CSS is loaded from template files, NOT written inline
- This is a TERMINAL step — there is no next step
- There is NO "Continue" option in the menu — only Regenerate, Regenerate Type, or Done

## EXECUTION PROTOCOLS:

- Show your analysis before taking any action
- Present all rendering results clearly with file sizes and page counts
- FORBIDDEN to proceed without user confirmation through menu
- FORBIDDEN to alter any document text, numbers, or analysis — formatting and rendering only

## CONTEXT BOUNDARIES:

- Available context: Step 14 outputs in {sourceDir}, playbook sources at {playbookSources}, research sources at {researchSources} and {explorationSources}
- CSS templates: {playbookCss}, {explorationCss}, {researchCss}, {planCss}
- Focus: PDF generation, file consolidation, naming convention enforcement
- Limits: Do not modify source content. Do not edit CSS templates — local copies only if customization is needed.
- Dependencies: Step 14 must be complete — business plan PDFs must exist in {sourceDir}

## NAMING CONVENTION

All files in `{deliverablesDir}` follow `<type>-<slug>.{md,pdf}`:

| Type | Source Pattern | Slug Derivation |
|------|---------------|-----------------|
| `bp` | Step 13/14 outputs | `business-plan`, `executive-summary` |
| `playbook` | `docs/plans/*-playbook.md` | Strip date prefix (`YYYY-MM-DD-`) and `-playbook` suffix from filename |
| `exploration` | `docs/research/*/exploration-report.md` | Human-readable short slug from parent directory name (strip date prefix, truncate to key topic) |
| `research` | `docs/research/*/report-*.md` | Strip `report-` prefix from filename |

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Verify Prerequisites

**Check Step 14 Outputs:**
Verify that `{sourceDir}` contains at minimum:
- `business-plan-final.md` (assembled plan)
- `bp-asp-business-plan.pdf` (or the project-name-normalized PDF)
- `bp-asp-executive-summary.pdf` (or the project-name-normalized PDF)
- `executive-summary.html`
- `bp-style.css` (or equivalent CSS file)

**Scan Source Documents:**
- Count playbook files matching `{playbookSources}`
- Count exploration reports matching `{explorationSources}`
- Count research reports matching `{researchSources}`

**Check CSS Templates:**
Verify all four CSS templates exist: `{playbookCss}`, `{explorationCss}`, `{researchCss}`, `{planCss}`

- IF all prerequisites met: Proceed.
- IF step 14 outputs missing: STOP. Report that Step 14 must be completed first.
- IF any CSS template missing: STOP. Report which template is missing.

**Share Status:**
"Prerequisites verified:
- Business plan: assembled + 2 PDFs ready
- Playbooks: {count} found
- Exploration reports: {count} found
- Research reports: {count} found
- CSS templates: all 4 present

Ready to build the deliverables package."

### 2. Create Deliverables Directory

**Create or clean the directory:**

```bash
rm -rf {deliverablesDir}
mkdir -p {deliverablesDir}
```

**Share Progress:**
"Deliverables directory created at `{deliverablesDir}`."

### 3. Copy & Rename Business Plan Outputs

Copy from `{sourceDir}` to `{deliverablesDir}` with `bp-` prefix naming:

| Source | Destination |
|--------|-------------|
| `business-plan-final.md` | `bp-business-plan.md` |
| `bp-{project_name}-business-plan.pdf` | `bp-business-plan.pdf` |
| `bp-{project_name}-executive-summary.pdf` | `bp-executive-summary.pdf` |
| `executive-summary.html` | `bp-executive-summary.html` |

**Share Progress:**
"Business plan outputs copied: bp-business-plan.md, bp-business-plan.pdf, bp-executive-summary.pdf, bp-executive-summary.html"

### 4. Generate Playbook PDFs

For each file matching `{playbookSources}`:

1. **Derive slug:** Strip date prefix and `-playbook` suffix from filename.
   Example: `2026-03-05-acquisition-playbook.md` → slug = `acquisition`

2. **Extract metadata from content:**
   - Title: first `# ` heading
   - Classification: the `**Classification:**` line if present, else first subtitle line
   - Version: the `**Version:**` line if present
   - Date: the `**Date:**` line if present

3. **Build HTML:**
   - Read `{playbookCss}` and embed in `<style>` tags
   - Build cover page div:
     ```html
     <div class="cover">
       <p class="type-label">Playbook</p>
       <h1>{title without "Playbook:" prefix}</h1>
       <p class="classification">{classification}</p>
       <p class="date">{date}</p>
       <p class="confidential">CONFIDENTIAL</p>
       <p class="version">{version}</p>
     </div>
     ```
   - Convert remaining markdown content to HTML via Pandoc
   - Wrap in full HTML document structure

4. **Render PDF** via WeasyPrint:
   - Output: `{deliverablesDir}/playbook-{slug}.pdf`

5. **Copy markdown:**
   - Copy source file to `{deliverablesDir}/playbook-{slug}.md`

6. **Record:** Store title, slug, classification (one line), file size, page count for later reporting.

**Share Progress:**
"Generated {count} playbook PDFs:
| Playbook | Pages | Size |
|----------|-------|------|
| playbook-{slug} | {pages} | {size} |
..."

### 5. Generate Exploration PDFs

For each file matching `{explorationSources}`:

1. **Derive slug:** From parent directory name, strip date prefix and truncate to key topic.
   Examples:
   - `2026-02-26-smb-accounting-owner-wants` → `smb-owner-wants`
   - `2026-02-26-smb-accounting-selling-partnering` → `selling-partnering`

2. **Extract metadata from content:**
   - Title: first `# ` heading (often starts with "Cross-Cutting" or "Exploration Report:")
   - First paragraph after the heading (used as abstract)

3. **Build HTML:**
   - Read `{explorationCss}` and embed in `<style>` tags
   - Build cover page div:
     ```html
     <div class="cover">
       <p class="type-label">Exploration Report</p>
       <h1>{title}</h1>
       <p class="scope">{one-line description of exploration scope}</p>
       <p class="date">{date from directory name}</p>
       <p class="confidential">CONFIDENTIAL</p>
     </div>
     ```
   - Extract the first paragraph or summary section and wrap in abstract box:
     ```html
     <div class="abstract-box">
       <p class="abstract-label">Summary</p>
       {abstract content}
     </div>
     ```
   - Convert remaining markdown content to HTML via Pandoc
   - Wrap in full HTML document structure

4. **Render PDF** via WeasyPrint:
   - Output: `{deliverablesDir}/exploration-{slug}.pdf`

5. **Copy markdown:**
   - Copy source file to `{deliverablesDir}/exploration-{slug}.md`

6. **Record:** Store title, slug, abstract first sentence, file size, page count.

**Share Progress:**
"Generated {count} exploration report PDFs:
| Report | Pages | Size |
|--------|-------|------|
| exploration-{slug} | {pages} | {size} |
..."

### 6. Generate Research PDFs

For each file matching `{researchSources}`:

1. **Derive slug:** Strip `report-` prefix from filename (keep `.md` stripped too).
   Example: `report-deal-structure-mechanics-sub-2mm.md` → `deal-structure-mechanics-sub-2mm`

2. **Extract metadata from content:**
   - Title: first `# ` heading (usually the research question)
   - Summary: content of `## Summary` section
   - Recommendation: content of `## Recommendation` section (if present)

3. **Build HTML:**
   - Read `{researchCss}` and embed in `<style>` tags
   - Build cover page div:
     ```html
     <div class="cover">
       <p class="type-label">Research Report</p>
       <h1>{title}</h1>
       <p class="scope">{source exploration or "Deep Research"}</p>
       <p class="date">{date from directory name}</p>
       <p class="confidential">CONFIDENTIAL</p>
     </div>
     ```
   - Wrap Summary in summary box:
     ```html
     <div class="summary-box">
       <p class="summary-label">Summary</p>
       {summary content}
     </div>
     ```
   - If Recommendation section exists, wrap in recommendation box:
     ```html
     <div class="recommendation-box">
       <p class="recommendation-label">Recommendation</p>
       {recommendation content}
     </div>
     ```
   - Convert remaining markdown content (excluding Summary and Recommendation which are already placed) to HTML via Pandoc
   - Wrap in full HTML document structure

4. **Render PDF** via WeasyPrint:
   - Output: `{deliverablesDir}/research-{slug}.pdf`

5. **Copy markdown:**
   - Copy source file to `{deliverablesDir}/research-{slug}.md`

6. **Record:** Store title, slug, summary first sentence, file size, page count.

**Share Progress:**
"Generated {count} research report PDFs:
| Report | Pages | Size |
|--------|-------|------|
| research-{slug} | {pages} | {size} |
..."

### 7. Inject Associated Documents Section

**Read the business plan copy:**
Read `{deliverablesDir}/bp-business-plan.md`.

**Build the Associated Documents section:**

```markdown
---

## Associated Documents

The following supporting documents accompany this business plan. Each is available in both markdown and PDF format.

### Playbooks

| Document | Description |
|----------|-------------|
| [{title}](playbook-{slug}.pdf) | {classification or one-line description} |
...

### Research Reports

| Document | Type | Description |
|----------|------|-------------|
| [{title}](exploration-{slug}.pdf) | Exploration | {first sentence of abstract} |
| [{title}](research-{slug}.pdf) | Deep Research | {first sentence of summary} |
...
```

**Inject into the plan:**
Insert the Associated Documents section immediately before `## Glossary` in the business plan. If no Glossary section exists, append before the Validation Report section. If neither exists, append at the end.

**Write the updated file:**
Write to `{deliverablesDir}/bp-business-plan.md`.

**Regenerate the full plan PDF:**
Re-run the step 14 pipeline for the full plan only:
1. Read the updated `bp-business-plan.md`
2. Strip YAML frontmatter and Validation Report section
3. Convert to HTML via Pandoc
4. Add cover page, TOC, section breaks (same as step 14)
5. Embed CSS from `{planCss}`
6. Render via WeasyPrint to `{deliverablesDir}/bp-business-plan.pdf`

**Share Progress:**
"Associated Documents section injected ({playbook_count} playbooks, {research_count} research reports). Business plan PDF regenerated."

### 8. Generate README.md Manifest

Write `{deliverablesDir}/README.md`:

```markdown
# Deliverables Package

**Project:** {project_name}
**Generated:** {date}
**Version:** v{version}

## Contents

### Business Plan

| File | Format | Pages | Size |
|------|--------|-------|------|
| bp-business-plan | [MD](bp-business-plan.md) / [PDF](bp-business-plan.pdf) | {pages} | {size} |
| bp-executive-summary | [PDF](bp-executive-summary.pdf) / [HTML](bp-executive-summary.html) | {pages} | {size} |

### Playbooks ({count})

| File | Format | Pages | Size |
|------|--------|-------|------|
| playbook-{slug} | [MD](playbook-{slug}.md) / [PDF](playbook-{slug}.pdf) | {pages} | {size} |
...

### Exploration Reports ({count})

| File | Format | Pages | Size |
|------|--------|-------|------|
| exploration-{slug} | [MD](exploration-{slug}.md) / [PDF](exploration-{slug}.pdf) | {pages} | {size} |
...

### Research Reports ({count})

| File | Format | Pages | Size |
|------|--------|-------|------|
| research-{slug} | [MD](research-{slug}.md) / [PDF](research-{slug}.pdf) | {pages} | {size} |
...

---

**Total:** {total_files} files ({total_md} markdown, {total_pdf} PDF, {total_other} other)
**Combined size:** {total_size}
```

**Share Progress:**
"README manifest generated with {total_files} entries."

### 9. Report Results

Present a summary to the user:

"**Deliverables package complete.**

| Type | Count | Total Pages | Total Size |
|------|-------|-------------|------------|
| Business Plan | 2 PDFs + 1 MD + 1 HTML | {pages} | {size} |
| Playbooks | {count} × (MD + PDF) | {pages} | {size} |
| Exploration Reports | {count} × (MD + PDF) | {pages} | {size} |
| Research Reports | {count} × (MD + PDF) | {pages} | {size} |
| **Total** | **{total} files** | **{total_pages} pages** | **{total_size}** |

All files are in `deliverables/` with `<type>-<slug>` naming."

### 10. Ship

**Git Commit:**

```bash
git add deliverables/
git commit -m "deliverables: generate package with {N} PDFs v{version}"
git push
```

**Share Status:**
"Deliverables package committed and pushed."

### 11. Present TERMINAL MENU

**This is a TERMINAL step — there is no "Continue" option.**

**Select an Option:** [RG] Regenerate All [RS] Regenerate Specific Type [DA] Done

#### Menu Handling Logic:

- IF RG: Return to [Step 2: Create Deliverables Directory](#2-create-deliverables-directory) and rebuild everything from scratch.
- IF RS: Ask which type to regenerate (Playbooks / Explorations / Research / Business Plan). Jump to the corresponding step (4, 5, 6, or 7). After regeneration, update README manifest (step 8) and re-ship (step 10).
- IF DA: Session is complete. No further action required.
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#11-present-terminal-menu)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- There is NO "Continue" option — this is the final step
- User can chat or ask questions — always respond and then end with display again of the menu options
- The only way to end is [DA] Done

## CRITICAL STEP COMPLETION NOTE

This is a TERMINAL step of the business plan workflow. There is no next step file. When the user selects [DA], the workflow is complete.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Step 14 outputs verified present before proceeding
- All CSS templates verified present before proceeding
- Deliverables directory created fresh (prior contents removed)
- Business plan outputs copied with `bp-` prefix naming
- All playbook sources found and processed
- All exploration reports found and processed
- All research reports found and processed
- Playbook PDFs have cover page with "PLAYBOOK" type label, title, classification, date, CONFIDENTIAL
- Exploration PDFs have cover page with "EXPLORATION REPORT" type label, title, scope, date, CONFIDENTIAL
- Exploration PDFs have abstract box with summary content
- Research PDFs have cover page with "RESEARCH REPORT" type label, title (question form), date, CONFIDENTIAL
- Research PDFs have summary box and recommendation box (if recommendation exists)
- CSS embedded from template files, not written inline
- All files follow `<type>-<slug>.{md,pdf}` naming convention
- Associated Documents section injected into bp-business-plan.md before Glossary
- Associated Documents section has Playbooks table and Research Reports table with relative PDF links
- Business plan PDF regenerated after Associated Documents injection
- README.md manifest generated with file sizes and page counts
- Results reported with counts and sizes per type
- Deliverables committed with message `deliverables: generate package with {N} PDFs v{version}`
- Terminal menu presented with [RG] Regenerate All [RS] Regenerate Type [DA] Done

### FAILURE:

- Proceeding without verifying step 14 outputs and CSS templates exist
- Modifying any source document content (text, numbers, analysis)
- Not creating cover pages for all PDF types
- Using wrong type label on cover pages
- Not following `<type>-<slug>` naming convention
- Not injecting Associated Documents section into the business plan
- Not regenerating the business plan PDF after injection
- Writing CSS inline instead of embedding from template files
- Editing canonical CSS templates instead of local copies
- Not generating README manifest
- Not reporting file sizes and page counts
- Not committing deliverables to git
- Including a "Continue" option (this is a terminal step)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
