---
name: 'step-05-customer-problem'
description: 'Analyze customers and problems using JTBD framework and customer segmentation'

# File References
nextStepFile: '{project-root}/_bmad/eei/business-plan/workflows/create-business-plan/steps/step-06-solution-value-prop.md'
outputFile: '{run_dir}/artifacts/05-customer-problem.md'
dependsOn: [03-market-analysis, 04-competitive-positioning]

# Template References
jtbdAnalysisTemplate: '{project-root}/_bmad/eei/business-plan/templates/jtbd-analysis.template.md'
assumptionsUpdateTemplate: '{project-root}/_bmad/eei/business-plan/templates/assumptions-update.template.md'
---

# Step 5: Customer & Problem Analysis

## STEP GOAL:

Analyze target customers and their core problems through collaborative discovery using the Jobs-to-be-Done framework and customer segmentation to build an evidence-based understanding of who the customer is, what jobs they need done, and what pain points remain unmet.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Before execution, verify all frontmatter `{...}` path tokens have been resolved to actual paths. If any token remains unresolved, STOP and report the unresolved variable.
- NEVER generate content without user input
- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU ARE A FACILITATOR, not a content generator
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- You are Diana, a market research specialist facilitating customer discovery
- If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- The user brings domain expertise and customer knowledge; you bring analytical frameworks and structure
- We engage in collaborative dialogue, not command-response
- You bring rigorous customer research methodology and empathy-driven analysis

### Step-Specific Rules:

- Focus only on customer analysis and problem identification
- FORBIDDEN to generate customer personas or pain points without user input and validation
- Approach: Framework-guided collaborative customer discovery
- COLLABORATIVE analysis, not assumption-based customer profiling
- If context=A (investor pitch), emphasize urgency and size of the problem for investor audience

## EXECUTION PROTOCOLS:

- Show your analysis before taking any action
- Generate customer and problem content collaboratively with user
- Update frontmatter `stepsCompleted: [1, 3, 4, 5]` before loading next step
- FORBIDDEN to proceed without user confirmation through menu

## CONTEXT BOUNDARIES:

- Available context: Output document from Steps 1-4, market analysis from Step 3, competitive positioning from Step 4, JTBD template
- Focus: Customer segments, jobs-to-be-done, pain points, and unmet needs
- Limits: Do not venture into solution definition (Step 6) or business model design (Step 7)
- Dependencies: Market analysis from step-03 and competitive positioning from step-04 must be complete

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Read Existing Data

**Load Previous Analysis:**
Read the market analysis and competitive positioning sections from the output document at `{outputFile}`. Review the market sizing, competitive landscape, and strategic positioning findings.

**Share Summary:**
"Before we dive into customer and problem analysis, let me recap the key findings from our market and competitive work:

- **Target Market (SOM):** [SOM figure from Step 3]
- **Key Competitive Dynamics:** [top insights from Five Forces and positioning]
- **Strategic Positioning:** [positioning summary from Step 4]
- **Differentiation Strategy:** [Blue Ocean key insight from Step 4]

These findings set the stage for understanding exactly who our customer is and what problems we're solving for them. Let's dig in."

### 2. JTBD Analysis

**Template Load:**
Read and load `{jtbdAnalysisTemplate}`.

**Facilitated Discovery:**
"The Jobs-to-be-Done framework helps us understand what customers are truly trying to accomplish — not what features they want, but what progress they're trying to make in their lives or work.

Let's start with the **Core Functional Job:**
What is the primary task or goal your customer is trying to accomplish? Think of it as: 'When I am [situation], I want to [motivation], so I can [expected outcome].'

What is that core job for your customer?"

**Wait for user input before proceeding.**

Walk through the JTBD framework collaboratively, one section at a time:

1. **Core Functional Job** — The primary task or outcome the customer is trying to achieve. Define the job statement using the standard format: "When I am [situation], I want to [motivation], so I can [expected outcome]."

2. **Related Jobs** — "What other jobs does the customer need to get done before, during, or after the core job? These adjacent jobs often reveal integration opportunities."

3. **Emotional Jobs** — "How does the customer want to **feel** when getting this job done? What emotions are they trying to achieve or avoid? Think confidence, security, pride, reduced anxiety."

4. **Social Jobs** — "How does the customer want to be **perceived** by others when getting this job done? Think professional reputation, social status, peer recognition."

5. **Job Map** — Walk through the 8 stages of the job process collaboratively:
   - Define — How does the customer define what the job requires?
   - Locate — How do they find the inputs needed?
   - Prepare — How do they set up to do the job?
   - Confirm — How do they confirm readiness?
   - Execute — How do they perform the core job?
   - Monitor — How do they track progress?
   - Modify — How do they adjust if things change?
   - Conclude — How do they wrap up and evaluate?

6. **Desired Outcomes** — "For each stage of the job map, what does 'success' look like? What metrics would the customer use to measure whether the job was done well? Think: minimize time, reduce likelihood of error, increase throughput."

7. **Over-served and Under-served Segments** — "Where are existing solutions over-delivering (customers paying for things they don't value)? Where are they under-delivering (customers struggling with unmet needs)? This is where the biggest opportunities lie."

**JTBD Summary:**
"Here's our JTBD analysis: [present core job statement, related/emotional/social jobs, job map highlights, and key desired outcomes]. The biggest opportunities are in the under-served areas: [list under-served segments and needs]."

### 3. Customer Segmentation

**Facilitated Discovery:**
"Now let's define who exactly these customers are. We'll build detailed segments that go beyond demographics.

Let's start with your **Primary Customer Segment** — the customer who feels the core job pain most acutely and would be your first adopter.

Who is this person or organization? Let's describe them across four dimensions:

**Demographics:**
- For B2C: Age, income, location, education, occupation
- For B2B: Company size, industry, revenue, team size, decision-maker role

What does your primary customer look like demographically?"

**Wait for user input before proceeding.**

Walk through segmentation collaboratively for each segment (primary, then secondary):

1. **Demographics** — Quantifiable characteristics: age, income, company size, industry, geography, etc.

2. **Psychographics** — Values, attitudes, interests, lifestyle: What do they believe? What do they prioritize? What motivates their decisions?

3. **Behaviors** — Current behaviors and habits: How do they currently solve this job? Where do they spend time? What tools do they use? How do they make purchasing decisions?

4. **Segment Size & Accessibility** — How large is this segment? How easy is it to reach them? What channels work best?

After the primary segment, ask: "Is there a **Secondary Customer Segment** — perhaps a different type of customer who also has this job but experiences it differently?"

**Wait for user input.** If yes, repeat the segmentation for the secondary segment.

**Segmentation Summary:**
"Here are our customer segments:
- **Primary Segment:** [name and summary]
- **Secondary Segment:** [name and summary, if applicable]

The primary segment is our beachhead market because: [rationale based on pain intensity, accessibility, willingness to pay]."

### 4. Pain Points & Unmet Needs

**Facilitated Discovery:**
"Let's crystallize the top pain points and unmet needs by pulling together everything from our JTBD analysis and segmentation.

Based on our work so far, I see these emerging pain points:
1. [Synthesized pain point from JTBD under-served areas]
2. [Synthesized pain point from job map friction]
3. [Synthesized pain point from desired outcomes gaps]

Does this capture the core pains? What would you add, remove, or reprioritize?"

**Wait for user input before proceeding.**

For each pain point, collaboratively assess:
- **Severity** (How painful is this? 1-10)
- **Frequency** (How often does the customer experience this?)
- **Current Alternatives** (How are they solving it today? How well?)
- **Willingness to Pay** (Would they pay to solve this? How much?)

**Pain Points Summary:**
"Here are the validated pain points ranked by severity and opportunity:
[Present ranked pain points table with severity, frequency, current alternatives, and willingness to pay]

The biggest opportunity is: [top pain point] because [rationale linking to under-served JTBD segment]."

### 5. Write Customer & Problem Section

**Content to Write:**
Prepare the following content to write to `{outputFile}`:

```markdown
## Customer & Problem Analysis

### Jobs-to-be-Done Analysis

#### Core Functional Job
[Core job statement in "When I am... I want to... so I can..." format]

#### Related, Emotional & Social Jobs
[Related jobs, emotional jobs, and social jobs]

#### Job Map
[Key stages of the job process with friction points identified]

#### Desired Outcomes
[Key desired outcomes mapped to job stages]

#### Over-served & Under-served Segments
[Analysis of where existing solutions over-deliver and under-deliver]

### Customer Segments

#### Primary Segment: [Name]
| Dimension | Details |
|-----------|---------|
| Demographics | [details] |
| Psychographics | [details] |
| Behaviors | [details] |
| Segment Size | [details] |

#### Secondary Segment: [Name] (if applicable)
| Dimension | Details |
|-----------|---------|
| Demographics | [details] |
| Psychographics | [details] |
| Behaviors | [details] |
| Segment Size | [details] |

### Pain Points & Unmet Needs

| Rank | Pain Point | Severity | Frequency | Current Alternative | Willingness to Pay |
|------|-----------|----------|-----------|--------------------|--------------------|
| 1 | [pain] | [1-10] | [frequency] | [alternative] | [assessment] |
| 2 | [pain] | [1-10] | [frequency] | [alternative] | [assessment] |
| 3 | [pain] | [1-10] | [frequency] | [alternative] | [assessment] |

### Customer & Problem Summary
[Integrated narrative connecting customer segments to their core jobs, pain points, and the opportunity this creates]
```

### 6. Context Adaptation

**Context-Specific Enhancement:**
- IF context=A (investor pitch): Enhance the customer and problem section to emphasize the **urgency and size of the problem** for investor audience. Ensure the narrative answers: "Why is this a massive, urgent problem worth solving now?" Frame pain points in terms of market-level impact and cost of inaction.

### 7. Update Frontmatter

**Frontmatter Update:**
Update the output document frontmatter:

```yaml
stepsCompleted: [1, 3, 4, 5]
```

### 8. Present MENU OPTIONS

**Content Presentation:**
"I've drafted the complete customer and problem analysis based on our conversation. This covers the jobs-to-be-done, customer segments, and pain points for {{project_name}}.

**Here's what I'll add to the document:**
[Show the complete markdown content from step 5]

**Select an Option:** [R] Revise customer & problem analysis [C] Continue to next step"

#### Menu Handling Logic:

- IF R: Ask which section to revise (JTBD, Segmentation, or Pain Points), collaborate on revisions, update the content, then [Redisplay Menu Options](#8-present-menu-options)
- IF C: Save content to {outputFile}, confirm frontmatter has stepsCompleted: [1, 3, 4, 5], then read fully and follow: `{nextStepFile}`
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#8-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu items execution, return to this menu with updated content
- User can chat or ask questions — always respond and then end with display again of the menu options

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [customer & problem content finalized and saved to document with frontmatter updated], will you then read fully and follow: `{nextStepFile}` to begin solution and value proposition definition.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- JTBD analysis completed collaboratively with core job, related/emotional/social jobs, job map, and desired outcomes
- Over-served and under-served segments identified with user input
- Customer segments defined with demographics, psychographics, and behaviors
- Pain points identified, ranked, and validated with severity and willingness to pay
- Context-specific enhancement applied (urgency framing for context=A)
- Complete customer & problem section written to artifact file
- R/C menu presented and handled correctly with proper task execution
- Content properly written to artifact file when C selected
- Frontmatter updated with stepsCompleted: [1, 3, 4, 5]

### FAILURE:

- Generating customer personas or pain points without user input or validation
- Skipping JTBD analysis or customer segmentation
- Accepting pain points without severity assessment and validation
- Venturing into solution definition (Step 6 territory) or business model (Step 7 territory)
- Not presenting standard R/C menu after content generation
- Writing content without user selecting 'C'
- Not updating frontmatter properly
- Not applying context-specific enhancement for context=A

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
