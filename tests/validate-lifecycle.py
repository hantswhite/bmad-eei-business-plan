#!/usr/bin/env python3
"""Structural validation for EEI Business Plan lifecycle configuration.

Checks that the dependency graph, persona grid, step frontmatter,
and config references are internally consistent. Run from project root:

    python3 tests/validate-lifecycle.py
"""

import os
import re
import sys
import yaml
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LIFECYCLE_MD = PROJECT_ROOT / "_bmad/eei/business-plan/workflows/create-business-plan/lifecycle.md"
PERSONA_GRID = PROJECT_ROOT / "_bmad/eei/business-plan/config/persona-grid.yaml"
CONFIG_YAML = PROJECT_ROOT / "_bmad/eei/config.yaml"
STEPS_DIR = PROJECT_ROOT / "_bmad/eei/business-plan/workflows/create-business-plan/steps"

passed = 0
failed = 0
errors = []


def ok(msg):
    global passed
    passed += 1
    print(f"  PASS  {msg}")


def fail(msg):
    global failed
    failed += 1
    errors.append(msg)
    print(f"  FAIL  {msg}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def extract_yaml_block(md_path):
    """Extract the lifecycle-status.yaml code block from lifecycle.md."""
    text = md_path.read_text()
    match = re.search(r"```yaml\n(version: 1.*?)```", text, re.DOTALL)
    if not match:
        return None
    return yaml.safe_load(match.group(1))


def extract_frontmatter(md_path):
    """Extract YAML frontmatter from a step file."""
    text = md_path.read_text()
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return None
    return yaml.safe_load(match.group(1))


# ---------------------------------------------------------------------------
# Test 1: Lifecycle YAML structure
# ---------------------------------------------------------------------------

def test_lifecycle_structure():
    print("\n[1] Lifecycle YAML structure")

    schema = extract_yaml_block(LIFECYCLE_MD)
    if schema is None:
        fail("Could not extract lifecycle-status.yaml from lifecycle.md")
        return

    ok("Extracted lifecycle-status.yaml template from lifecycle.md")

    required_top_keys = {"version", "context", "created", "last_updated", "artifacts", "cascade_log", "consistency_reviews", "research_registry"}
    missing = required_top_keys - set(schema.keys())
    if missing:
        fail(f"Missing top-level keys: {missing}")
    else:
        ok(f"All {len(required_top_keys)} top-level keys present")

    artifacts = schema.get("artifacts", {})
    if not artifacts:
        fail("No artifacts defined")
        return

    for art_id, art in artifacts.items():
        required = {"status", "agent", "dependsOn", "lastUpdated"}
        missing = required - set(art.keys())
        if missing:
            fail(f"Artifact {art_id} missing keys: {missing}")

    ok(f"All {len(artifacts)} artifacts have required keys")
    return schema


# ---------------------------------------------------------------------------
# Test 2: Dependency graph acyclicity
# ---------------------------------------------------------------------------

def test_no_cycles(schema):
    print("\n[2] Dependency graph — no cycles")

    if schema is None:
        fail("Skipped — no schema")
        return

    artifacts = schema["artifacts"]
    graph = {aid: art.get("dependsOn", []) for aid, art in artifacts.items()}

    def has_cycle(node, visited, stack):
        visited.add(node)
        stack.add(node)
        for dep in graph.get(node, []):
            if dep not in visited:
                if has_cycle(dep, visited, stack):
                    return True
            elif dep in stack:
                return True
        stack.discard(node)
        return False

    visited = set()
    cycle_found = False
    for node in graph:
        if node not in visited:
            if has_cycle(node, visited, set()):
                fail(f"Cycle detected involving {node}")
                cycle_found = True

    if not cycle_found:
        ok(f"No cycles in dependency graph ({len(graph)} nodes)")


# ---------------------------------------------------------------------------
# Test 3: All dependsOn targets exist
# ---------------------------------------------------------------------------

def test_deps_exist(schema):
    print("\n[3] Dependency targets exist")

    if schema is None:
        fail("Skipped — no schema")
        return

    artifacts = schema["artifacts"]
    art_ids = set(artifacts.keys())
    bad = []
    for aid, art in artifacts.items():
        for dep in art.get("dependsOn", []):
            if dep not in art_ids:
                bad.append(f"{aid} depends on unknown {dep}")

    if bad:
        for b in bad:
            fail(b)
    else:
        ok("All dependency targets reference existing artifacts")


# ---------------------------------------------------------------------------
# Test 4: Persona grid covers all non-exempt artifacts
# ---------------------------------------------------------------------------

def test_persona_coverage(schema):
    print("\n[4] Persona grid coverage")

    if schema is None:
        fail("Skipped — no schema")
        return

    grid = yaml.safe_load(PERSONA_GRID.read_text())
    personas = grid.get("personas", {})
    contexts = {"A", "B", "C"}

    non_exempt = [
        aid for aid, art in schema["artifacts"].items()
        if not art.get("critiqueExempt", False)
    ]

    missing = []
    for aid in non_exempt:
        if aid not in personas:
            missing.append(f"{aid}: no persona entry")
            continue
        for ctx in contexts:
            if ctx not in personas[aid]:
                missing.append(f"{aid} x context {ctx}: no persona")

    if missing:
        for m in missing:
            fail(m)
    else:
        ok(f"All {len(non_exempt)} non-exempt artifacts x 3 contexts covered ({len(non_exempt) * 3} personas)")


# ---------------------------------------------------------------------------
# Test 5: Step files have required frontmatter
# ---------------------------------------------------------------------------

def test_step_frontmatter():
    print("\n[5] Step file frontmatter")

    step_files = sorted(STEPS_DIR.glob("step-*.md"))
    if not step_files:
        fail("No step files found")
        return

    ok(f"Found {len(step_files)} step files")

    for sf in step_files:
        fm = extract_frontmatter(sf)
        if fm is None:
            fail(f"{sf.name}: no frontmatter")
            continue

        if "name" not in fm:
            fail(f"{sf.name}: missing 'name' in frontmatter")

        # Steps 03-12 must have outputFile and dependsOn
        step_num = re.search(r"step-(\d+)", sf.name)
        if step_num:
            n = int(step_num.group(1))
            if 3 <= n <= 12:
                if "outputFile" not in fm:
                    fail(f"{sf.name}: missing 'outputFile'")
                if "dependsOn" not in fm:
                    fail(f"{sf.name}: missing 'dependsOn'")

    ok("All step files have required frontmatter fields")


# ---------------------------------------------------------------------------
# Test 6: Step dependsOn matches lifecycle.md canonical graph
# ---------------------------------------------------------------------------

def test_step_deps_match_lifecycle(schema):
    print("\n[6] Step dependsOn matches lifecycle.md")

    if schema is None:
        fail("Skipped — no schema")
        return

    artifacts = schema["artifacts"]
    step_files = sorted(STEPS_DIR.glob("step-*.md"))

    # Map step number to artifact ID
    step_to_artifact = {}
    for aid in artifacts:
        match = re.match(r"(\d+)-", aid)
        if match:
            step_to_artifact[int(match.group(1))] = aid

    mismatches = []
    for sf in step_files:
        fm = extract_frontmatter(sf)
        if fm is None or "dependsOn" not in fm:
            continue

        step_num = re.search(r"step-(\d+)", sf.name)
        if not step_num:
            continue
        n = int(step_num.group(1))

        aid = step_to_artifact.get(n)
        if aid is None:
            continue

        canonical = sorted(artifacts[aid].get("dependsOn", []))
        step_deps = sorted(fm["dependsOn"])

        if canonical != step_deps:
            mismatches.append(
                f"{sf.name} ({aid}): step has {step_deps}, lifecycle has {canonical}"
            )

    if mismatches:
        for m in mismatches:
            fail(m)
    else:
        ok("All step dependsOn arrays match lifecycle.md canonical graph")


# ---------------------------------------------------------------------------
# Test 7: Config.yaml references valid files
# ---------------------------------------------------------------------------

def test_config_references():
    print("\n[7] Config.yaml file references")

    config = yaml.safe_load(CONFIG_YAML.read_text())
    file_keys = {
        "persona_grid": "_bmad/eei/business-plan/config/persona-grid.yaml",
        "critique_agent": "_bmad/eei/business-plan/agents/critique-agent.md",
        "lifecycle_module": "_bmad/eei/business-plan/workflows/create-business-plan/lifecycle.md",
        "consistency_review": "_bmad/eei/business-plan/workflows/create-business-plan/consistency-review.md",
        "glossary_template": "_bmad/eei/business-plan/templates/glossary.template.yaml",
        "gap_analysis_template": "_bmad/eei/business-plan/templates/gap-analysis.template.md",
        "playbook_css_template": "_bmad/eei/business-plan/templates/playbook-style.template.css",
        "exploration_css_template": "_bmad/eei/business-plan/templates/exploration-style.template.css",
        "research_css_template": "_bmad/eei/business-plan/templates/research-style.template.css",
    }

    for key, expected_suffix in file_keys.items():
        val = config.get(key, "")
        # Strip {project-root}/ prefix
        rel = val.replace("{project-root}/", "")
        full = PROJECT_ROOT / rel
        if not full.exists():
            fail(f"config.{key} -> {rel} does not exist")
        elif not str(full).endswith(expected_suffix.replace("/", os.sep)):
            fail(f"config.{key} points to unexpected path: {rel}")
        else:
            ok(f"config.{key} -> {rel}")

    # Validate research_enforcement key
    enforcement = config.get("research_enforcement")
    valid_modes = {"strict", "standard", "permissive"}
    if enforcement is None:
        fail("config.research_enforcement key is missing")
    elif enforcement not in valid_modes:
        fail(f"config.research_enforcement = '{enforcement}' — must be one of {valid_modes}")
    else:
        ok(f"config.research_enforcement = '{enforcement}'")


# ---------------------------------------------------------------------------
# Test 8: Cascade invalidation — forward-walk coverage
# ---------------------------------------------------------------------------

def test_cascade_coverage(schema):
    print("\n[8] Cascade invalidation — forward-walk coverage")

    if schema is None:
        fail("Skipped — no schema")
        return

    artifacts = schema["artifacts"]

    # Build reverse graph: for each artifact, which artifacts depend on it
    dependents = defaultdict(set)
    for aid, art in artifacts.items():
        for dep in art.get("dependsOn", []):
            dependents[dep].add(aid)

    # For each non-leaf artifact, verify it has at least one dependent
    non_exempt = [
        aid for aid, art in artifacts.items()
        if not art.get("critiqueExempt", False)
    ]

    # The last artifact (12-executive-summary) won't have dependents in the lifecycle
    # (step-13 assembly is not tracked as an artifact)
    leaf = "12-executive-summary"
    interior = [aid for aid in non_exempt if aid != leaf]

    orphans = [aid for aid in interior if aid not in dependents]
    if orphans:
        for o in orphans:
            fail(f"{o} has no dependents — cascade can't propagate through it")
    else:
        ok(f"All {len(interior)} interior artifacts have downstream dependents")

    # Verify that invalidating 01-context reaches all artifacts (transitive)
    def forward_walk(start):
        reached = set()
        queue = [start]
        while queue:
            node = queue.pop(0)
            for dep in dependents.get(node, set()):
                if dep not in reached:
                    reached.add(dep)
                    queue.append(dep)
        return reached

    reached = forward_walk("01-context")
    all_non_exempt = set(non_exempt)
    unreached = all_non_exempt - reached - {"01-context"}
    if unreached:
        fail(f"Invalidating 01-context doesn't reach: {unreached}")
    else:
        ok(f"Invalidating 01-context cascades to all {len(reached)} downstream artifacts")


# ---------------------------------------------------------------------------
# Test 9: lifecycle.md contains reference_intake block
# ---------------------------------------------------------------------------

def test_reference_intake_block(schema):
    print("\n[9] Lifecycle YAML — reference_intake block")

    if schema is None:
        fail("Skipped — no schema")
        return

    ri = schema.get("reference_intake")
    if ri is None:
        fail("No reference_intake block in lifecycle-status.yaml template")
        return

    ok("reference_intake block present")

    required_keys = {"last_run", "brief_file", "hashes"}
    missing = required_keys - set(ri.keys())
    if missing:
        fail(f"reference_intake missing keys: {missing}")
    else:
        ok(f"All {len(required_keys)} reference_intake keys present")


# ---------------------------------------------------------------------------
# Test 10: lifecycle.md contains REFERENCE RE-INTAKE PROCESSING section
# ---------------------------------------------------------------------------

def test_reintake_section():
    print("\n[10] Lifecycle.md — re-intake and ship-it sections")

    text = LIFECYCLE_MD.read_text()

    required_sections = [
        "REFERENCE RE-INTAKE PROCESSING",
        "SHIP-IT INTEGRATION",
    ]

    for section in required_sections:
        if section in text:
            ok(f"Found '{section}' section in lifecycle.md")
        else:
            fail(f"Missing '{section}' section in lifecycle.md")


# ---------------------------------------------------------------------------
# Test 11: Config.yaml has research_paths as a list
# ---------------------------------------------------------------------------

def test_research_paths_config():
    print("\n[11] Config.yaml — research_paths key")

    config = yaml.safe_load(CONFIG_YAML.read_text())
    rp = config.get("research_paths")
    if rp is None:
        fail("config.research_paths key is missing")
    elif not isinstance(rp, list):
        fail(f"config.research_paths must be a list, got {type(rp).__name__}")
    elif len(rp) == 0:
        fail("config.research_paths is an empty list")
    else:
        ok(f"config.research_paths has {len(rp)} glob patterns")


# ---------------------------------------------------------------------------
# Test 12: section_topic_map config key and file exists
# ---------------------------------------------------------------------------

SECTION_TOPIC_MAP = PROJECT_ROOT / "_bmad/eei/business-plan/config/section-topic-map.yaml"

def test_section_topic_map_config():
    print("\n[12] Config.yaml — section_topic_map key and file")

    config = yaml.safe_load(CONFIG_YAML.read_text())
    stm = config.get("section_topic_map")
    if stm is None:
        fail("config.section_topic_map key is missing")
        return

    rel = stm.replace("{project-root}/", "")
    full = PROJECT_ROOT / rel
    if not full.exists():
        fail(f"config.section_topic_map -> {rel} does not exist")
    else:
        ok(f"config.section_topic_map -> {rel}")


# ---------------------------------------------------------------------------
# Test 13: section_topic_map covers all non-exempt artifact IDs
# ---------------------------------------------------------------------------

def test_section_topic_map_coverage(schema):
    print("\n[13] Section topic map — artifact coverage")

    if schema is None:
        fail("Skipped — no schema")
        return

    if not SECTION_TOPIC_MAP.exists():
        fail("section-topic-map.yaml does not exist — skipping coverage check")
        return

    stm = yaml.safe_load(SECTION_TOPIC_MAP.read_text())
    sections = stm.get("sections", {})
    section_ids = set(sections.keys())

    non_exempt = {
        aid for aid, art in schema["artifacts"].items()
        if not art.get("critiqueExempt", False)
    }

    missing = non_exempt - section_ids
    if missing:
        for m in missing:
            fail(f"section-topic-map.yaml missing entry for {m}")
    else:
        ok(f"All {len(non_exempt)} non-exempt artifacts covered in section topic map")


# ---------------------------------------------------------------------------
# Test 14: Lifecycle YAML — research_registry block
# ---------------------------------------------------------------------------

def test_research_registry_block(schema):
    print("\n[14] Lifecycle YAML — research_registry block")

    if schema is None:
        fail("Skipped — no schema")
        return

    rr = schema.get("research_registry")
    if rr is None:
        fail("No research_registry block in lifecycle-status.yaml template")
        return

    ok("research_registry block present")

    required_keys = {"last_scan", "artifacts"}
    missing = required_keys - set(rr.keys())
    if missing:
        fail(f"research_registry missing keys: {missing}")
    else:
        ok(f"All {len(required_keys)} research_registry keys present")


# ---------------------------------------------------------------------------
# Test 15: Entry point wiring — menu links and slash command targets
# ---------------------------------------------------------------------------

COMMANDS_DIR = PROJECT_ROOT / ".claude/commands"

def test_entry_points():
    print("\n[15] Entry point wiring — menu links and slash commands")

    broken = []

    # 1. Validate "Load and follow" targets in step files and lifecycle files
    workflow_dir = STEPS_DIR.parent
    md_files = list(STEPS_DIR.glob("step-*.md")) + list(workflow_dir.glob("lifecycle*.md"))
    load_pattern = re.compile(
        r'Load and follow\s+`'
        r'(?:\{project-root\}/)?'    # optional {project-root}/ prefix
        r'([^`]+\.md)`'              # capture the path
    )

    for md_file in md_files:
        text = md_file.read_text()
        for match in load_pattern.finditer(text):
            target = match.group(1)
            # Skip config-token-only refs like {consistency_review}
            if target.startswith("{") and not target.startswith("_bmad"):
                continue
            full = PROJECT_ROOT / target
            if not full.exists():
                broken.append(f"{md_file.name}: 'Load and follow' target missing: {target}")

    # 2. Validate slash command file targets
    for cmd_file in sorted(COMMANDS_DIR.glob("bmad-eei-bp-*.md")):
        text = cmd_file.read_text()
        # Match @{project-root}/path or LOAD the FULL @{project-root}/path
        target_pattern = re.compile(
            r'@\{project-root\}/([^\s,]+\.(?:md|yaml))'
        )
        for match in target_pattern.finditer(text):
            target = match.group(1)
            full = PROJECT_ROOT / target
            if not full.exists():
                broken.append(f"{cmd_file.name}: slash command target missing: {target}")

    if broken:
        for b in broken:
            fail(b)
    else:
        ok("All 'Load and follow' targets in step/lifecycle files resolve to existing files")
        ok("All slash command targets in EEI commands resolve to existing files")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("EEI Business Plan — Lifecycle Structural Validation")
    print("=" * 60)

    schema = test_lifecycle_structure()
    test_no_cycles(schema)
    test_deps_exist(schema)
    test_persona_coverage(schema)
    test_step_frontmatter()
    test_step_deps_match_lifecycle(schema)
    test_config_references()
    test_cascade_coverage(schema)
    test_reference_intake_block(schema)
    test_reintake_section()
    test_research_paths_config()
    test_section_topic_map_config()
    test_section_topic_map_coverage(schema)
    test_research_registry_block(schema)
    test_entry_points()

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed:
        print("\nFailed checks:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("\nAll checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
