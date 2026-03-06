---
name: lifecycle-research-sync
description: 'Research sync processing — integrates new research and playbook artifacts into the business plan'
---

# Research Sync Processing

**Invoked by:** `lifecycle.md` when session-start research scan or the `/eei-bp-research-sync` command detects new or changed research artifacts.

---

## 1. Present Changes to User

"{user_name}, I've detected changes in your research library since the last scan ({research_registry.last_scan}):

| Status | Artifact |
|--------|----------|
| {New/Changed} | {short name from filename} |

I'll analyze each to determine which plan sections need updating.

Ready to proceed?"

**Wait for user confirmation before proceeding.**

## 2. Extract Research Summaries

For each queued artifact:

1. Read the file
2. Extract the `## Summary` section content
3. Extract the `## Recommendation` section content (if present; omit if absent)
4. Store as `{research_summary}` and `{research_recommendation}`
5. Determine `{research_type}`: "deep-research" (report-*.md), "guided-exploration" (exploration-report.md), or "playbook" (*-playbook.md)

## 3. Triage Each Artifact

For each queued artifact, invoke the triage agent:

1. Load triage prompt from `{project-root}/_bmad/eei/business-plan/templates/research-triage-prompt.template.md`
2. Load section topic map from `{section_topic_map}`
3. Substitute placeholders:
   - `{research_path}` — full path to the research artifact
   - `{research_type}` — deep-research, guided-exploration, or playbook
   - `{research_summary}` — extracted summary text
   - `{research_recommendation}` — extracted recommendation text (or "No recommendation section.")
   - `{research_filename}` — filename only
   - `{section_topic_map}` — formatted section map (one section per line: `{id}: {topics}`)
4. Parse the YAML output: `affected_sections` and `unaffected_sections`
5. If output is unparseable, warn user and skip this artifact (register it but don't cascade)

## 4. Present Consolidated Triage Results

Merge triage results across all queued artifacts into a single table:

"Research triage complete. Proposed plan updates:

| Research Artifact | Affected Section | Impact | Reason |
|---|---|---|---|
| {short name} | {section_id} | {impact} | {reason} |

Sections not affected: {comma-separated list of unaffected section IDs}

**Select an Option:** [A] Accept and cascade [E] Edit (add/remove sections) [S] Skip (register without cascading)"

### Menu Handling:

- **IF A:** Proceed to step 5 (cascade)
- **IF E:** User specifies changes (add section X with reason, remove section Y). Update the triage results, then re-present the table with [A] / [S] options.
- **IF S:** Register all queued artifacts in `research_registry` with their triage results and updated hashes. Set `research_registry.last_scan` to today. Commit: `research-sync: register {count} artifacts (skipped cascade)`. **Stop — no cascade.**
- **IF any other input:** Respond to user, then redisplay menu.

## 5. Execute Cascade

1. **Collect directly affected sections** from all triage results (deduplicated — a section flagged by multiple artifacts only resets once)
2. **Auto-add 12-executive-summary** if any other section is affected
3. **Walk dependency graph forward**: for each directly affected section, find all artifacts that `dependsOn` it (directly or transitively) and add them to the invalidation set
4. **Classify each invalidated artifact**:
   - **Directly affected** (in triage results): reset to DRAFT, will receive evidence injection
   - **Indirectly affected** (dependency cascade only): reset to DRAFT, will go through standard REVISE vs FAST-TRACK triage
   - **Unaffected and no invalidated dependency**: FAST-TRACK — keep FINAL status
5. **Increment `version`** in `lifecycle-status.yaml`
6. **Log** to `cascade_log`:

```yaml
- timestamp: "{date}"
  trigger: "research-sync"
  reason: "New research: {list of artifact short names}"
  new_artifacts:
    - "{path to report 1}"
    - "{path to report 2}"
  invalidated: ["{list of all invalidated artifact IDs}"]
  fast_tracked: ["{list of fast-tracked artifact IDs}"]
  version_before: {N}
  version_after: {N+1}
```

7. **Register** all queued artifacts in `research_registry.artifacts`:
   - New artifacts: add entry with path, hash, summary (first sentence of `## Summary`), registered date, and triage_result
   - Changed artifacts: update hash, summary, registered date, and triage_result
8. Set `research_registry.last_scan` to today
9. **Ship**: commit `lifecycle-status.yaml` with message: `research-sync: cascade from {count} new artifacts v{N+1}`

## 6. Report Cascade

"**Research sync cascade triggered.**

The following artifacts have been reset to DRAFT:

**Directly affected (will receive new research evidence):**
{list with section names and which research artifact triggered them}

**Indirectly affected (will be triaged for upstream changes):**
{list with section names}

**Fast-tracked (no changes needed):**
{list with section names}

Version incremented from {N} to {N+1}.

We'll revise directly affected sections first (with research evidence injected), then triage indirect dependents."

## 7. Revise Directly Affected Sections

For each directly affected section, in dependency order:

1. **Build evidence injection block.** For each research artifact that mapped to this section in the triage results:
   - Extract `## Summary` and `## Recommendation` from the research file
   - Format as:

```markdown
## New Research Evidence

The following research has been produced since this section was last finalized.
Incorporate relevant findings into your revision.

### {title extracted from # heading of research report}
{Summary section content}

{Recommendation section content, if present}

**Source:** {path to full report}
(Read the full report if you need detail on a specific finding.)
```

2. **Invoke the drafting agent** for this section's step file. Pass the evidence injection block as additional context (appended after the existing reference brief context in the step's CONTEXT BOUNDARIES section).
3. **Run full lifecycle**: DRAFT > CRITIQUE > REVISED > FINAL REVIEW > FINAL (standard after-step processing).

## 8. Triage Indirectly Affected Sections

For each indirectly affected section (dependency cascade only, not directly matched by research), in dependency order:

1. Use the existing `triage-prompt.template.md` (REVISE vs FAST-TRACK)
2. The `{diff_or_summary_of_changes}` is: "Upstream sections were revised based on new research evidence. The following research triggered the cascade: {list of artifact names and one-line summaries}."
3. **IF REVISE**: Return to drafting agent for delta revision. No research evidence injection — the agent reconciles with the updated upstream artifact.
4. **IF FAST-TRACK**: Set to FINAL with audit note.

## 9. Post-Cascade Completion

When all artifacts are FINAL again:

1. Run Consistency Pass 2
2. Reassemble (Step 13)
3. Regenerate PDFs (Step 14)
4. Copy to project root

Same as existing post-cascade flow.
