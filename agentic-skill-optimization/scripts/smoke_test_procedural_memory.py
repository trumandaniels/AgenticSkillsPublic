#!/usr/bin/env python3
"""Smoke-test the generated procedural-memory scaffold for this skill."""

from __future__ import annotations

import argparse
import importlib.util
import json
import py_compile
import shutil
import subprocess
import uuid
import sys
import tempfile
from pathlib import Path


EXPECTED_FILES = [
    "references/procedure-memory.md",
    "references/procedure-graph.json",
    "scripts/retrieve_memory.py",
    "scripts/record_episode.py",
    "scripts/refine_graph.py",
]

REQUIRED_GRAPH_KEYS = {
    "schema_version",
    "skill",
    "capture_policy",
    "retrieval_policy",
    "nodes",
    "edges",
    "episodes",
    "failure_patterns",
    "environment_interfaces",
    "refinement_policy",
}


def run(cmd: list[str], cwd: Path | None = None, expect_ok: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if expect_ok and result.returncode != 0:
        raise AssertionError(
            "Command failed:\n"
            + " ".join(cmd)
            + f"\nexit={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}"
        )
    return result


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def has_sentence_transformers() -> bool:
    return importlib.util.find_spec("sentence_transformers") is not None


def make_target(root: Path) -> Path:
    target = root / "target-skill"
    target.mkdir()
    (target / "SKILL.md").write_text(
        "---\nname: smoke-test-skill\ndescription: disposable generated scaffold test\n---\n\n"
        "# Smoke Test Skill\n\nDo disposable test work.\n",
        encoding="utf-8",
    )
    return target


def writable_scratch() -> Path:
    candidates = [Path.cwd() / "work" / "procedural_memory_smoke_tmp", Path.cwd() / "procedural_memory_smoke_tmp", Path(tempfile.gettempdir()) / "procedural_memory_smoke_tmp"]
    for scratch in candidates:
        try:
            scratch.mkdir(parents=True, exist_ok=True)
            probe = scratch / f"probe-{uuid.uuid4().hex}.tmp"
            probe.write_text("ok", encoding="utf-8")
            probe.unlink()
            return scratch
        except OSError:
            continue
    raise AssertionError("No writable scratch directory available for smoke test")


def compile_python(path: Path) -> None:
    scratch = writable_scratch()
    cfile = scratch / f"{path.stem}-{uuid.uuid4().hex}.pyc"
    try:
        py_compile.compile(str(path), cfile=str(cfile), doraise=True)
    finally:
        cfile.unlink(missing_ok=True)


def validate_graph(graph_path: Path) -> dict:
    graph = json.loads(graph_path.read_text(encoding="utf-8-sig"))
    missing = REQUIRED_GRAPH_KEYS - set(graph)
    check(not missing, f"procedure-graph.json missing keys: {sorted(missing)}")
    check(graph["retrieval_policy"].get("method") == "hybrid_rrf_dense_reliability", "wrong retrieval method")
    check(graph["retrieval_policy"].get("dense_required") is True, "dense retrieval should be required")
    check(graph["retrieval_policy"].get("reliability_weight") == 0.15, "missing reliability weight")
    check(graph["capture_policy"].get("mode") == "auto", "capture mode should be auto")
    check(graph["capture_policy"].get("before_final_required") is True, "before-final capture should be required")
    check(graph["capture_policy"].get("skip_requires_confirmation") is True, "skip confirmation should be required")
    check(graph["refinement_policy"].get("method") == "local_trace_reward_reliability", "wrong refinement method")
    check(graph["refinement_policy"].get("api_calls_required") is False, "refinement should not require API calls")
    return graph


def validate_no_paid_api_calls(target: Path) -> None:
    banned = ["import openai", "from openai", "OPENAI_API_KEY", "api_key", "anthropic", "requests.post"]
    for script in [target / "scripts" / "retrieve_memory.py", target / "scripts" / "record_episode.py", target / "scripts" / "refine_graph.py"]:
        text = script.read_text(encoding="utf-8")
        found = [token for token in banned if token in text]
        check(not found, f"{script.name} contains paid/API-looking tokens: {found}")


def record_episode(target: Path) -> str:
    graph_path = target / "references" / "procedure-graph.json"
    result = run([
        sys.executable,
        str(target / "scripts" / "record_episode.py"),
        str(graph_path),
        "--task-family",
        "smoke",
        "--request-summary",
        "smoke test trace-aware capture",
        "--outcome",
        "completed",
        "--reward",
        "1.0",
        "--planned-trace",
        "proc_retrieve,proc_execute",
        "--executed-trace",
        "proc_retrieve,proc_execute,proc_validate",
        "--lesson",
        "Executed trace should be persisted for refinement.",
        "--evidence-ref",
        "smoke-test",
    ])
    line = result.stdout.strip()
    check(line.startswith("recorded="), f"unexpected record output: {line}")
    episode_id = line.split("=", 1)[1]
    graph = json.loads(graph_path.read_text(encoding="utf-8-sig"))
    episode = graph["episodes"][-1]
    check(episode["id"] == episode_id, "recorded episode id not persisted")
    check(episode["reward"] == 1.0, "episode reward not persisted")
    check(episode["planned_trace"] == ["proc_retrieve", "proc_execute"], "planned trace not parsed")
    check(episode["executed_trace"] == ["proc_retrieve", "proc_execute", "proc_validate"], "executed trace not parsed")
    return episode_id


def embedding_checks(target: Path, episode_id: str) -> str:
    check(has_sentence_transformers(), "sentence_transformers is required; embedding refinement/retrieval must not be skipped")
    graph_path = target / "references" / "procedure-graph.json"
    run([sys.executable, str(target / "scripts" / "refine_graph.py"), str(graph_path), "--episode-id", episode_id])
    graph = json.loads(graph_path.read_text(encoding="utf-8-sig"))
    check(len(graph["nodes"]) >= 3, "refinement did not add trace nodes")
    check(len(graph["edges"]) >= 2, "refinement did not add trace edges")
    check(any(edge.get("reliability_vector_sum") for edge in graph["edges"]), "edges missing reliability vectors")
    result = run([
        sys.executable,
        str(target / "scripts" / "retrieve_memory.py"),
        str(graph_path),
        "--query",
        "smoke test trace-aware capture",
        "--json",
    ])
    payload = json.loads(result.stdout)
    check(payload.get("fusion") == "hybrid_rrf_dense_reliability", "retrieval fusion mismatch")
    return "PASS embedding-backed refinement/retrieval exercised"


def smoke(skill_dir: Path, keep_tmp: bool) -> int:
    init_script = skill_dir / "scripts" / "init_procedural_memory.py"
    check(init_script.exists(), f"missing init script: {init_script}")
    compile_python(init_script)
    temp_dir = writable_scratch() / f"run-{uuid.uuid4().hex}"
    temp_dir.mkdir(parents=True, exist_ok=False)
    try:
        target = make_target(temp_dir)
        result = run([sys.executable, str(init_script), str(target), "--patch-skill", "--force"])
        check("refine_script=" in result.stdout, "init output did not report refine_script")
        for rel in EXPECTED_FILES:
            check((target / rel).exists(), f"generated file missing: {rel}")
        skill_text = (target / "SKILL.md").read_text(encoding="utf-8")
        check("## Procedural Memory" in skill_text, "target SKILL.md was not patched")
        check("refine_graph.py" in skill_text, "target SKILL.md does not mention refinement")
        validate_graph(target / "references" / "procedure-graph.json")
        for rel in ["scripts/retrieve_memory.py", "scripts/record_episode.py", "scripts/refine_graph.py"]:
            compile_python(target / rel)
            run([sys.executable, str(target / rel), "--help"])
        validate_no_paid_api_calls(target)
        episode_id = record_episode(target)
        embedding_result = embedding_checks(target, episode_id)
        print("PASS generated scaffold contract checks")
        print("PASS generated script compile/help checks")
        print("PASS trace-aware capture checks")
        print(embedding_result)
        if keep_tmp:
            print(f"kept_temp={temp_dir}")
            temp_dir = None  # type: ignore[assignment]
        return 0
    finally:
        if temp_dir is not None and temp_dir.exists() and not keep_tmp:
            shutil.rmtree(temp_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", default=str(Path(__file__).resolve().parents[1]), help="Path to the agentic-skill-scaffolding skill directory")
    parser.add_argument("--keep-tmp", action="store_true", help="Keep the disposable generated target skill")
    args = parser.parse_args()
    return smoke(Path(args.skill_dir).resolve(), args.keep_tmp)


if __name__ == "__main__":
    raise SystemExit(main())
