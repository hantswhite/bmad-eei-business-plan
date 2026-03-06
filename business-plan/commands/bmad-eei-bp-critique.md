---
name: 'eei-bp-critique'
description: 'Manually trigger adversarial critique on a specific business plan artifact'
---

IT IS CRITICAL THAT YOU FOLLOW THIS COMMAND:

1. LOAD the FULL @{project-root}/_bmad/eei/config.yaml and store all variables
2. Ask the user which artifact to critique (list available artifacts from {run_dir}/artifacts/)
3. Ask the user to confirm the plan context (A/B/C) if not already known
4. LOAD the FULL @{project-root}/_bmad/eei/business-plan/agents/critique-agent.md
5. Pass the artifact_id, artifact_file, context, and critique_output_file parameters
6. Follow the critique agent's activation instructions exactly
