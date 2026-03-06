---
name: 'eei-bp-research-sync'
description: 'Detect new research/playbooks and cascade-update affected business plan sections'
---

IT IS CRITICAL THAT YOU FOLLOW THIS COMMAND:

1. LOAD the FULL @{project-root}/_bmad/eei/config.yaml and store all variables
2. Locate the run directory at {planning_artifacts}/business-plan-{project_name}-*/
3. Read {run_dir}/lifecycle-status.yaml
4. Read the RESEARCH SYNC PROCESSING section from {lifecycle_module}
5. Execute the research sync flow:
   a. Scan for files matching patterns in config.research_paths
   b. Compare SHA-256 hashes against research_registry in lifecycle-status.yaml
   c. For new/changed artifacts: run triage, present results, cascade on user confirmation
6. If no new artifacts detected, report: "Research library is current, no plan updates needed."
