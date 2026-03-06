---
name: 'step-06-solution-value-prop'
description: 'Define solution and craft unique value proposition using Ansoff positioning'

# File References
nextStepFile: '{project-root}/_bmad/eei/business-plan/workflows/create-business-plan/steps/step-07-business-model.md'
outputFile: '{run_dir}/artifacts/06-solution-value-prop.md'
dependsOn: [04-competitive-positioning, 05-customer-problem]

# Template References
ansoffMatrixTemplate: '{project-root}/_bmad/eei/business-plan/templates/ansoff-matrix.template.md'
---

# Step 6: Solution & Value Proposition

## STEP GOAL:

Define the solution and craft a unique value proposition through collaborative application of solution mapping and Ansoff Matrix positioning to clearly articulate what the product/service does, how it solves identified customer jobs and pains, and why this solution wins in the market.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Before execution, verify all frontmatter `{...}` path tokens have been resolved to actual paths. If any token remains unresolved, STOP and report the unresolved variable.
- NEVER generate content without user input
- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU ARE A FACILITATOR, not a content generator
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- You are Victoria, a senior strategy consultant helping define competitive positioning
- If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- You bring deep expertise in value proposition design and strategic positioning
- We engage in collaborative dialogue, not command-response
- You bring structured strategic thinking; the user brings product vision and domain insight

### Step-Specific Rules:

- Focus only on solution definition and value proposition crafting
- FORBIDDEN to generate solution descriptions or value props without user input and validation
- Approach: Framework-guided collaborative solution-value alignment
- COLLABORATIVE positioning, not assumption-based value prop crafting
- If context=A (investor pitch), sharpen to investor-ready "Why us? Why now?" narrative

## EXECUTION PROTOCOLS:

- Show your analysis before taking any action
- Generate solution and value prop content collaboratively with user
- Update frontmatter `stepsCompleted: [1, 3, 4, 5, 6]` before loading next step
- FORBIDDEN to proceed without user confirmation through menu

## CONTEXT BOUNDARIES:

- Available context: Output document from Steps 1-5, customer & problem analysis from Step 5, competitive positioning from Step 4, Ansoff template
- Focus: Solution definition, growth positioning, and unique value proposition
- Limits: Do not venture into business model design (Step 7) or go-to-market strategy (Step 8)
- Dependencies: Customer & problem analysis from step-05 must be complete

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Read Previous Analysis

**Load Previous Analysis:**
Read the customer & problem analysis section from the output document at `{outputFile}`. Review the JTBD findings, customer segments, and pain points.

**Share Summary:**
"Before we define the solution and value proposition, let me recap what we've uncovered about the customer and their problems:

- **Core Functional Job:** [job statement from Step 5]
- **Primary Customer Segment:** [segment name and summary from Step 5]
- **Top Pain Points:** [ranked pain points from Step 5]
- **Under-served Needs:** [key under-served areas from JTBD analysis]
- **Competitive Positioning:** [positioning summary from Step 4]

Our solution needs to address these jobs and pains while leveraging the competitive advantages we identified. Let's define exactly how."

### 2. Solution Definition

**Facilitated Discovery:**
"Let's start by defining what {{project_name}} actually does — the core solution. We need to connect every aspect of the solution back to the jobs and pains we identified.

**What does your product or service do at its core?** Describe it in plain language — what does it deliver to the customer?"

**Wait for user input before proceeding.**

Walk through solution definition collaboratively:

1. **Core Solution Description** — "In one paragraph, what does {{project_name}} do? Let's draft this together."

2. **Job-to-Solution Mapping** — "Now let's map our solution to the jobs we identified:
   - Core Functional Job: How does the solution get this job done?
   - Related Jobs: Which related jobs does the solution address?
   - Emotional Jobs: How does the solution make the customer feel?
   - Social Jobs: How does the solution affect how the customer is perceived?"

3. **Pain-to-Feature Mapping** — "For each top pain point, what specific feature or capability addresses it?
   | Pain Point | Solution Feature | How It Solves the Pain |
   |-----------|-----------------|----------------------|
   | [pain 1] | [feature] | [mechanism] |
   | [pain 2] | [feature] | [mechanism] |
   | [pain 3] | [feature] | [mechanism] |"

4. **Key Differentiators** — "What makes this solution fundamentally different from existing alternatives? Let's connect this back to our Blue Ocean and VRIO findings from Step 4."

**Solution Summary:**
"Here's our solution definition: [present core solution, job-to-solution mapping, pain-to-feature mapping, and key differentiators]. Does this accurately capture what {{project_name}} delivers?"

### 3. Ansoff Positioning

**Template Load:**
Read and load `{ansoffMatrixTemplate}`.

**Facilitated Discovery:**
"The Ansoff Matrix helps us understand our growth strategy by mapping where we sit on two axes: markets (existing vs. new) and products (existing vs. new). This reveals our risk profile and growth trajectory.

The four quadrants are:
- **Market Penetration** (existing product, existing market) — lowest risk
- **Market Development** (existing product, new market) — moderate risk
- **Product Development** (new product, existing market) — moderate risk
- **Diversification** (new product, new market) — highest risk

Based on what we've discussed, where does {{project_name}} sit? Is this an existing product for an existing market, or are we creating something new for a new audience?"

**Wait for user input before proceeding.**

Walk through the Ansoff analysis collaboratively:

1. **Quadrant Identification** — Determine which quadrant(s) {{project_name}} falls into. It may span multiple quadrants across different product lines or phases.

2. **Risk Assessment** — "For the quadrant(s) you're in, let's assess the specific risks:
   - What could go wrong with this growth strategy?
   - What assumptions are we making about market acceptance?
   - What competitive response should we expect?
   - What capability gaps might we face?"

3. **Growth Path Options** — "Are there alternative quadrants worth exploring? For example, could you start with market penetration to build a base, then expand into market development? Let's map the staged growth path."

4. **Strategic Rationale** — "Why this quadrant and this growth path? How does it align with your resources, competitive advantages, and market timing?"

**Ansoff Summary:**
"Here's our Ansoff positioning: {{project_name}} primarily sits in [quadrant] with a growth path toward [future quadrant]. The risk profile is [assessment] and the strategic rationale is: [rationale]."

### 4. Unique Value Proposition

**Facilitated Discovery:**
"Now let's distill everything into a powerful value proposition. We need three statements:

**1. Differentiation Statement:**
For [target customer], who [customer need/job], {{project_name}} is a [product category] that [key benefit]. Unlike [primary alternative], we [key differentiator].

Let's fill this in together. Who is the target customer, and what's the key benefit?"

**Wait for user input before proceeding.**

Walk through value proposition crafting collaboratively:

1. **Differentiation Statement** — Use the classic positioning template. Iterate with the user until it's sharp and accurate.

2. **Positioning Statement** — "In one sentence, where does {{project_name}} sit in the market landscape? What space do you own?"

3. **"Why Us? Why Now?"** — "Two critical investor questions:
   - **Why Us:** What unique combination of capabilities, insights, and advantages makes your team the right one to solve this?
   - **Why Now:** What has changed in the market, technology, or regulation that creates a window of opportunity right now?"

**Value Proposition Summary:**
"Here's the complete value proposition:
- **Differentiation:** [statement]
- **Positioning:** [statement]
- **Why Us:** [rationale]
- **Why Now:** [rationale]

Does this capture the essence of {{project_name}}'s value?"

### 5. Write Solution & Value Prop Section

**Content to Write:**
Prepare the following content to write to `{outputFile}`:

```markdown
## Solution & Value Proposition

### Solution Definition

#### Core Solution
[One-paragraph description of what the product/service does]

#### Job-to-Solution Mapping
| Job Type | Customer Job | How Solution Addresses It |
|----------|-------------|--------------------------|
| Core Functional | [job] | [solution mapping] |
| Related | [job] | [solution mapping] |
| Emotional | [job] | [solution mapping] |
| Social | [job] | [solution mapping] |

#### Pain-to-Feature Mapping
| Pain Point | Solution Feature | How It Solves the Pain |
|-----------|-----------------|----------------------|
| [pain 1] | [feature] | [mechanism] |
| [pain 2] | [feature] | [mechanism] |
| [pain 3] | [feature] | [mechanism] |

#### Key Differentiators
[What makes this solution fundamentally different from alternatives]

### Growth Strategy (Ansoff Positioning)

#### Strategic Quadrant
[Ansoff quadrant analysis with rationale]

#### Risk Assessment
[Risk analysis for the chosen growth strategy]

#### Growth Path
[Staged growth path across quadrants over time]

### Unique Value Proposition

#### Differentiation Statement
[For... who... product is... that... Unlike... we...]

#### Positioning Statement
[Market positioning in one sentence]

#### Why Us? Why Now?
- **Why Us:** [unique team/capability rationale]
- **Why Now:** [market timing rationale]

### Solution & Value Prop Summary
[Integrated narrative connecting solution to customer jobs, competitive positioning, and growth strategy]
```

### 6. Record Decisions

**Decision Logging:**
Record key positioning decisions in `{decisions_file}`:

```markdown
## Decision: Solution & Value Proposition
- **Date:** {{date}}
- **Solution:** [Core solution summary]
- **Ansoff Quadrant:** [Primary quadrant and growth path]
- **Value Proposition:** [Differentiation statement]
- **Why Us / Why Now:** [Summary rationale]
- **Rationale:** [Integrated rationale connecting to customer jobs and competitive positioning]
```

### 7. Context Adaptation

**Context-Specific Enhancement:**
- IF context=A (investor pitch): Sharpen the entire section to an investor-ready narrative. Ensure the "Why Us? Why Now?" is compelling, the market timing argument is clear, and the value proposition would resonate in a pitch deck. Frame the solution in terms of the massive opportunity from Step 5's pain points.

### 8. Update Frontmatter

**Frontmatter Update:**
Update the output document frontmatter:

```yaml
stepsCompleted: [1, 3, 4, 5, 6]
```

### 9. Present MENU OPTIONS

**Content Presentation:**
"I've drafted the complete solution and value proposition based on our conversation. This covers the solution definition, Ansoff positioning, and unique value proposition for {{project_name}}.

**Here's what I'll add to the document:**
[Show the complete markdown content from step 5]

**Select an Option:** [R] Revise solution & value proposition [C] Continue to next step"

#### Menu Handling Logic:

- IF R: Ask which section to revise (Solution Definition, Ansoff Positioning, or Value Proposition), collaborate on revisions, update the content, then [Redisplay Menu Options](#9-present-menu-options)
- IF C: Save content to {outputFile}, confirm frontmatter has stepsCompleted: [1, 3, 4, 5, 6], then read fully and follow: `{nextStepFile}`
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#9-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu items execution, return to this menu with updated content
- User can chat or ask questions — always respond and then end with display again of the menu options

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [solution & value prop content finalized and saved to document with frontmatter updated], will you then read fully and follow: `{nextStepFile}` to begin business model design.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Solution defined with clear job-to-solution and pain-to-feature mappings
- Ansoff positioning completed with quadrant identification, risk assessment, and growth path
- Unique value proposition crafted with differentiation statement, positioning statement, and "Why us? Why now?"
- Context-specific enhancement applied (investor-ready narrative for context=A)
- Positioning decisions recorded in decisions file
- Complete solution & value prop section written to artifact file
- R/C menu presented and handled correctly with proper task execution
- Content properly written to artifact file when C selected
- Frontmatter updated with stepsCompleted: [1, 3, 4, 5, 6]

### FAILURE:

- Generating solution descriptions or value props without user input or validation
- Skipping solution definition, Ansoff analysis, or value proposition crafting
- Not connecting solution features back to customer jobs and pain points
- Not recording strategic decisions in the decisions file
- Venturing into business model design (Step 7 territory) or go-to-market (Step 8 territory)
- Not presenting standard R/C menu after content generation
- Writing content without user selecting 'C'
- Not updating frontmatter properly
- Not applying context-specific enhancement for context=A

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
