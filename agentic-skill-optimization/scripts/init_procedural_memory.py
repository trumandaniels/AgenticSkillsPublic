#!/usr/bin/env python3
"""Initialize ProPlay-inspired procedural memory files for a Codex skill."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

PROCEDURAL_SECTION = """## Procedural Memory

For tasks that resemble prior episodes, read `references/procedure-memory.md` and inspect `references/procedure-graph.json` before drafting the task plan.

Use the procedure graph to preplay a likely path: select relevant procedure nodes, note reliable transitions, and identify failure patterns to avoid. Treat the preplay as soft guidance; user instructions and fresh task evidence override stale memory.

Default to automatic capture. Before the final response, record a compact episode with `scripts/record_episode.py` when the run contains reusable procedural signal. Skip only when the episode is low-signal, sensitive beyond safe summarization, or part of a held-out evaluation that should remain uncontaminated.

End with a procedural-memory receipt: `recorded <episode_id>` or `skipped because <reason>`.
"""

RECORD_EPISODE_SCRIPT = r'''#!/usr/bin/env python3
"""Append compact procedural-memory episodes to procedure-graph.json."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

REQUIRED = {"task_family", "request_summary", "outcome", "procedures_used", "lessons"}


def load_episode(args: argparse.Namespace) -> dict:
    if args.episode_json:
        episode = json.loads(args.episode_json)
    elif args.episode_file:
        episode = json.loads(Path(args.episode_file).read_text(encoding="utf-8-sig"))
    else:
        raise SystemExit("Provide --episode-json or --episode-file")

    missing = sorted(REQUIRED - set(episode))
    if missing:
        raise SystemExit(f"Episode missing required keys: {', '.join(missing)}")

    if "id" not in episode or not episode["id"]:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        family = str(episode["task_family"]).lower().replace(" ", "-")[:32]
        episode["id"] = f"episode_{stamp}_{family}"

    episode.setdefault("failure_patterns", [])
    episode.setdefault("sensitivity", "none")
    episode.setdefault("evidence_ref", "current-thread")
    return episode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", help="Path to references/procedure-graph.json")
    parser.add_argument("--episode-json", help="Compact episode JSON object")
    parser.add_argument("--episode-file", help="Path to a JSON file containing one episode object")
    args = parser.parse_args()

    graph_path = Path(args.graph)
    graph = json.loads(graph_path.read_text(encoding="utf-8-sig"))
    episode = load_episode(args)

    episodes = graph.setdefault("episodes", [])
    if any(existing.get("id") == episode["id"] for existing in episodes):
        raise SystemExit(f"Episode id already exists: {episode['id']}")

    episodes.append(episode)
    graph_path.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
    print(f"recorded={episode['id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def read_skill_name(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8-sig")
    match = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return skill_md.parent.name
    for line in match.group(1).splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip('"\'')
    return skill_md.parent.name


def procedure_memory_text(skill_name: str) -> str:
    return f"""# Procedural Memory

This file supports a ProPlay-inspired, Codex-native procedural memory loop for `${skill_name}`.

## When To Read

Read this file and inspect `procedure-graph.json` before starting tasks that resemble prior episodes, before applying user corrections, and before subagent forward-tests.

## Capture Policy

Default mode is `auto`.

Before the final response, record a compact episode when the run contains reusable procedural signal. Skip only when the episode is low-signal, sensitive beyond safe summarization, or part of a held-out evaluation that should remain uncontaminated.

Every final answer should include a receipt:

```text
Procedural memory: recorded episode_YYYYMMDD_short_slug.
```

or:

```text
Procedural memory: skipped because <specific reason>.
```

For sensitive tasks, summarize or ask for confirmation before writing memory. Do not store private details when a reusable procedural lesson is enough.

## Preplay

1. Identify the current task family.
2. Select relevant procedure nodes and reliable or emerging transitions from `procedure-graph.json`.
3. Check matching failure patterns.
4. Draft a short task-specific procedural plan.
5. Treat that plan as soft guidance. User instructions and fresh evidence override stale memory.

## Execute

Use the target skill's normal workflow. Let procedural memory guide sequencing and checks, but do not skip domain-specific instructions, validation gates, or tool requirements already present in `SKILL.md`.

## Capture

Before the final response, create a compact episode object and run:

```bash
python scripts/record_episode.py references/procedure-graph.json --episode-json '{{"task_family":"example-family","request_summary":"Compact task summary","outcome":"completed","procedures_used":[],"lessons":[],"failure_patterns":[],"sensitivity":"none","evidence_ref":"current-thread"}}'
```

Record only reusable signal:

- Procedures that helped.
- Transitions that seemed reliable or contested.
- User corrections with future value.
- Failure patterns worth avoiding.
- Evidence pointers that are safe to store.

Do not store full transcripts, hidden benchmark answers, or unnecessary personal data.

## Refine

After capture, optionally update nodes, edges, and failure patterns when the episode provides enough evidence. Keep reliability conservative until repeated evidence supports it.

## Training Instructions

Use these prompts to train the skill over time:

```text
Use ${skill_name} on this task and auto-record a compact procedural-memory episode unless it is low-signal or sensitive.
```

```text
Update ${skill_name} procedural memory from this correction. Store only reusable procedures, transition evidence, and failure patterns.
```

```text
For this run, do not record procedural memory. Treat it as held-out evaluation.
```

```text
Forward-test ${skill_name} with a fresh Codex subagent on this held-out task. Do not reveal expected answers or prior diagnosis.
```

## Contamination Rules

Keep held-out prompts, evaluator rubrics, and hidden expected answers out of memory until they are no longer needed for clean evaluation.
"""


def insert_section(skill_md: Path) -> bool:
    text = skill_md.read_text(encoding="utf-8-sig")
    if "## Procedural Memory" in text:
        return False
    frontmatter = re.match(r"(---\s*\n.*?\n---\s*\n)", text, re.DOTALL)
    insert_at = frontmatter.end() if frontmatter else 0
    heading = re.search(r"^# .+$", text[insert_at:], re.MULTILINE)
    if heading:
        insert_at += heading.end()
    new_text = text[:insert_at].rstrip() + "\n\n" + PROCEDURAL_SECTION.strip() + "\n\n" + text[insert_at:].lstrip()
    skill_md.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target_skill", help="Path to the target skill directory")
    parser.add_argument("--patch-skill", action="store_true", help="Insert a Procedural Memory section into SKILL.md")
    parser.add_argument("--force", action="store_true", help="Overwrite existing procedure-memory files")
    args = parser.parse_args()

    target = Path(args.target_skill).expanduser().resolve()
    skill_md = target / "SKILL.md"
    if not skill_md.exists():
        raise SystemExit(f"SKILL.md not found: {skill_md}")

    skill_name = read_skill_name(skill_md)
    references = target / "references"
    scripts = target / "scripts"
    references.mkdir(exist_ok=True)
    scripts.mkdir(exist_ok=True)

    memory_md = references / "procedure-memory.md"
    graph_json = references / "procedure-graph.json"
    record_script = scripts / "record_episode.py"

    if args.force or not memory_md.exists():
        memory_md.write_text(procedure_memory_text(skill_name), encoding="utf-8")

    if args.force or not graph_json.exists():
        graph = {
            "schema_version": 1,
            "skill": skill_name,
            "capture_policy": {
                "mode": "auto",
                "before_final_required": True,
                "receipt_required": True,
                "sensitive_data": "summarize_or_skip",
            },
            "nodes": [],
            "edges": [],
            "episodes": [],
            "failure_patterns": [],
        }
        graph_json.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")

    if args.force or not record_script.exists():
        record_script.write_text(RECORD_EPISODE_SCRIPT, encoding="utf-8")

    patched = insert_section(skill_md) if args.patch_skill else False

    print(f"target={target}")
    print(f"skill={skill_name}")
    print(f"memory={memory_md}")
    print(f"graph={graph_json}")
    print(f"record_script={record_script}")
    print(f"capture_mode=auto")
    print(f"patched_skill={str(patched).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())