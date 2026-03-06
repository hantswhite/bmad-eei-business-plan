---
name: research-triage-prompt
description: 'Research sync triage — assesses which plan sections are affected by new research or playbook artifacts'
---

# Research Triage Assessment

You are assessing which business plan sections need revision based on new research evidence.

## Research Artifact

**File:** {research_path}
**Type:** {research_type}

### Summary

{research_summary}

### Recommendation

{research_recommendation}

---

## Plan Sections

{section_topic_map}

---

## Instructions

For each plan section listed above:

1. Read the research summary and recommendation carefully
2. Compare each key finding against the section's topic keywords
3. Assess whether the research contains material new evidence that would change the section's content
4. Only flag a section if the research provides **substantive new evidence** — not tangential mentions

### Impact Ratings

- **high** — research contains findings that contradict, materially update, or add significant new evidence. Section needs substantive rewrite.
- **moderate** — research supplements or refines existing content. Section needs targeted updates, not a full rewrite.
- Do NOT include sections with low or no impact.

### Special Rules

- **12-executive-summary**: Do NOT include in your output. It auto-cascades if any other section is affected.
- Be conservative — only flag sections where the research genuinely changes what the section should say, not where it's merely related to the topic.

## Output

Return ONLY valid YAML. Do not wrap in code fences. Do not include text before or after.

### Example 1: Research affects multiple sections

artifact: "report-03-pe-deal-structures.md"
affected_sections:
  - id: "07-business-model"
    reason: "PE deal structure data changes revenue model assumptions for advisory conversion"
    impact: "high"
  - id: "10-financial-projections"
    reason: "New deal economics require updated unit economics and margin assumptions"
    impact: "moderate"
unaffected_sections: ["01-context", "03-market-analysis", "04-competitive-positioning", "05-customer-problem", "06-solution-value-prop", "08-go-to-market", "09-operations-team", "11-risks-mitigants"]

### Example 2: Research affects no sections

artifact: "exploration-report.md"
affected_sections: []
unaffected_sections: ["01-context", "03-market-analysis", "04-competitive-positioning", "05-customer-problem", "06-solution-value-prop", "07-business-model", "08-go-to-market", "09-operations-team", "10-financial-projections", "11-risks-mitigants"]

### Your output (follow the exact format above)

artifact: "{research_filename}"
affected_sections:
  - id: "{section_id}"
    reason: "One sentence explaining what specific finding affects this section"
    impact: "high|moderate"
unaffected_sections: ["{list of section IDs not affected}"]
