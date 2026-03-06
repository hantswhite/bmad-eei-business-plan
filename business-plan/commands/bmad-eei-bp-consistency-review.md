---
name: 'eei-bp-consistency-review'
description: 'Manually trigger cross-artifact consistency review for business plan'
---

IT IS CRITICAL THAT YOU FOLLOW THIS COMMAND:

1. LOAD the FULL @{project-root}/_bmad/eei/config.yaml and store all variables
2. Locate the run directory at {planning_artifacts}/business-plan-{project_name}-*/
3. LOAD the FULL @{project-root}/_bmad/eei/business-plan/workflows/create-business-plan/consistency-review.md
4. Ask the user which pass number this is (1 or 2), or auto-detect from lifecycle-status.yaml
5. Follow the consistency review instructions exactly
6. Present findings to the user
