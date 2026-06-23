#!/usr/bin/env python3
"""Lightweight SkillOpt-style local scoring, gating, and staging.

This harness intentionally avoids model serving and heavyweight ML. Codex or a
human creates candidate edits; this script runs local judges and stages only
candidates that beat the current validation score.
"""

from __future__ import annotations

import argparse
import datetime as dt
import filecmp
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class CaseResult:
    id: str
    split: str
    hard: float
    soft: float
    passed: bool
    reason: str
    weight: float = 1.0
    stdout: str = ""
    stderr: str = ""
    returncode: int | None = None


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            try:
                item = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_no}: invalid JSON: {exc}") from exc
            if "id" not in item:
                raise SystemExit(f"{path}:{line_no}: case is missing id")
            if "judge" not in item:
                raise SystemExit(f"{path}:{line_no}: case {item['id']!r} is missing judge")
            items.append(item)
    return items


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_text(value: str | None, path_value: str | None, base_dir: Path) -> str:
    if path_value:
        path = resolve_path(path_value, base_dir)
        return path.read_text(encoding="utf-8")
    return value or ""


def resolve_path(raw: str, base_dir: Path) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = base_dir / path
    return path


def run_command(command: str, cwd: Path, timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd),
        shell=True,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def maybe_prepare(case: dict[str, Any], base_dir: Path, timeout: int) -> tuple[bool, str, str, int | None]:
    prepare = case.get("prepare")
    if not prepare:
        return True, "", "", None
    if not isinstance(prepare, dict) or prepare.get("type", "command") != "command":
        return False, "", "prepare must be a command judge", None
    cwd = resolve_path(str(prepare.get("cwd", ".")), base_dir)
    proc = run_command(str(prepare["command"]), cwd, int(prepare.get("timeout", timeout)))
    if proc.returncode != 0:
        return False, proc.stdout, proc.stderr, proc.returncode
    return True, proc.stdout, proc.stderr, proc.returncode


def score_command(case: dict[str, Any], judge: dict[str, Any], base_dir: Path, timeout: int) -> CaseResult:
    cwd = resolve_path(str(judge.get("cwd", ".")), base_dir)
    proc = run_command(str(judge["command"]), cwd, int(judge.get("timeout", timeout)))
    passed = proc.returncode == int(judge.get("pass_returncode", 0))
    return CaseResult(
        id=str(case["id"]),
        split=str(case.get("split", "val")),
        hard=1.0 if passed else 0.0,
        soft=1.0 if passed else 0.0,
        passed=passed,
        reason="command exited with expected code" if passed else "command failed",
        weight=float(case.get("weight", 1.0)),
        stdout=proc.stdout[-8000:],
        stderr=proc.stderr[-8000:],
        returncode=proc.returncode,
    )


def score_regex(case: dict[str, Any], judge: dict[str, Any], base_dir: Path) -> CaseResult:
    text = load_text(judge.get("text"), judge.get("path"), base_dir)
    flags = 0
    for flag in judge.get("flags", []):
        if str(flag).lower() == "ignorecase":
            flags |= re.IGNORECASE
        elif str(flag).lower() == "multiline":
            flags |= re.MULTILINE
        elif str(flag).lower() == "dotall":
            flags |= re.DOTALL
    matched = re.search(str(judge["pattern"]), text, flags) is not None
    expect_match = bool(judge.get("expect_match", True))
    passed = matched == expect_match
    return CaseResult(
        id=str(case["id"]),
        split=str(case.get("split", "val")),
        hard=1.0 if passed else 0.0,
        soft=1.0 if passed else 0.0,
        passed=passed,
        reason="regex expectation met" if passed else "regex expectation failed",
        weight=float(case.get("weight", 1.0)),
    )


def normalize_text(text: str, enabled: bool) -> str:
    if not enabled:
        return text
    return re.sub(r"\s+", " ", text.strip())


def score_exact(case: dict[str, Any], judge: dict[str, Any], base_dir: Path) -> CaseResult:
    actual = load_text(judge.get("actual"), judge.get("actual_path"), base_dir)
    expected = load_text(judge.get("expected"), judge.get("expected_path"), base_dir)
    normalize = bool(judge.get("normalize", False))
    passed = normalize_text(actual, normalize) == normalize_text(expected, normalize)
    return CaseResult(
        id=str(case["id"]),
        split=str(case.get("split", "val")),
        hard=1.0 if passed else 0.0,
        soft=1.0 if passed else 0.0,
        passed=passed,
        reason="exact match" if passed else "exact mismatch",
        weight=float(case.get("weight", 1.0)),
    )


def canonical_json(path: Path) -> str:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def score_golden(case: dict[str, Any], judge: dict[str, Any], base_dir: Path) -> CaseResult:
    actual = resolve_path(str(judge["actual_path"]), base_dir)
    expected = resolve_path(str(judge["expected_path"]), base_dir)
    mode = str(judge.get("mode", "text")).lower()
    if mode == "json":
        passed = canonical_json(actual) == canonical_json(expected)
    elif mode == "bytes":
        passed = filecmp.cmp(actual, expected, shallow=False)
    else:
        normalize = bool(judge.get("normalize", False))
        passed = normalize_text(actual.read_text(encoding="utf-8"), normalize) == normalize_text(
            expected.read_text(encoding="utf-8"), normalize
        )
    return CaseResult(
        id=str(case["id"]),
        split=str(case.get("split", "val")),
        hard=1.0 if passed else 0.0,
        soft=1.0 if passed else 0.0,
        passed=passed,
        reason="golden match" if passed else "golden mismatch",
        weight=float(case.get("weight", 1.0)),
    )


def score_manual(case: dict[str, Any], judge: dict[str, Any]) -> CaseResult:
    accepted = bool(judge.get("accepted", False))
    soft = float(judge.get("soft", 1.0 if accepted else 0.0))
    return CaseResult(
        id=str(case["id"]),
        split=str(case.get("split", "val")),
        hard=1.0 if accepted else 0.0,
        soft=max(0.0, min(1.0, soft)),
        passed=accepted,
        reason=str(judge.get("reason", "manual acceptance" if accepted else "manual rejection")),
        weight=float(case.get("weight", 1.0)),
    )


def score_case(case: dict[str, Any], base_dir: Path, timeout: int) -> CaseResult:
    ok, stdout, stderr, returncode = maybe_prepare(case, base_dir, timeout)
    if not ok:
        return CaseResult(
            id=str(case["id"]),
            split=str(case.get("split", "val")),
            hard=0.0,
            soft=0.0,
            passed=False,
            reason="prepare failed",
            weight=float(case.get("weight", 1.0)),
            stdout=stdout[-8000:],
            stderr=stderr[-8000:],
            returncode=returncode,
        )
    judge = case["judge"]
    kind = str(judge.get("type", "")).lower()
    if kind == "command":
        return score_command(case, judge, base_dir, timeout)
    if kind == "regex":
        return score_regex(case, judge, base_dir)
    if kind == "exact":
        return score_exact(case, judge, base_dir)
    if kind == "golden":
        return score_golden(case, judge, base_dir)
    if kind == "manual":
        return score_manual(case, judge)
    raise SystemExit(f"case {case['id']!r}: unsupported judge type {kind!r}")


def aggregate(results: list[CaseResult]) -> dict[str, Any]:
    total_weight = sum(max(0.0, r.weight) for r in results)
    if total_weight <= 0:
        hard = soft = 0.0
    else:
        hard = sum(r.hard * r.weight for r in results) / total_weight
        soft = sum(r.soft * r.weight for r in results) / total_weight
    return {
        "hard": hard,
        "soft": soft,
        "passed": all(r.passed for r in results),
        "cases_total": len(results),
        "cases_passed": sum(1 for r in results if r.passed),
    }


def select_gate_score(summary: dict[str, Any], metric: str, mixed_weight: float) -> float:
    hard = float(summary.get("hard", 0.0))
    soft = float(summary.get("soft", 0.0))
    if metric == "hard":
        return hard
    if metric == "soft":
        return soft
    if metric == "mixed":
        weight = max(0.0, min(1.0, mixed_weight))
        return (1.0 - weight) * hard + weight * soft
    raise SystemExit(f"unknown gate metric {metric!r}")


def cmd_score(args: argparse.Namespace) -> int:
    cases_path = Path(args.cases).resolve()
    base_dir = Path(args.base_dir).resolve() if args.base_dir else cases_path.parent
    wanted_split = args.split
    cases = [
        case
        for case in read_jsonl(cases_path)
        if wanted_split == "all" or str(case.get("split", "val")) == wanted_split
    ]
    if not cases:
        raise SystemExit(f"no cases found for split {wanted_split!r}")
    results = [score_case(case, base_dir, int(args.timeout)) for case in cases]
    payload = {
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "cases_path": str(cases_path),
        "base_dir": str(base_dir),
        "split": wanted_split,
        "summary": aggregate(results),
        "results": [asdict(result) for result in results],
    }
    write_json(Path(args.out), payload)
    summary = payload["summary"]
    print(
        f"{summary['cases_passed']}/{summary['cases_total']} passed "
        f"hard={summary['hard']:.4f} soft={summary['soft']:.4f}"
    )
    return 0 if summary["passed"] else 1 if args.fail_on_case_failure else 0


def cmd_gate(args: argparse.Namespace) -> int:
    current = json.loads(Path(args.current).read_text(encoding="utf-8"))
    candidate = json.loads(Path(args.candidate).read_text(encoding="utf-8"))
    metric = args.metric
    current_score = select_gate_score(current["summary"], metric, float(args.mixed_weight))
    candidate_score = select_gate_score(candidate["summary"], metric, float(args.mixed_weight))
    accepted = candidate_score > current_score

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    stage_dir = Path(args.stage_dir) / stamp
    stage_dir.mkdir(parents=True, exist_ok=False)

    manifest: dict[str, Any] = {
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "accepted": accepted,
        "metric": metric,
        "mixed_weight": float(args.mixed_weight),
        "current_score": current_score,
        "candidate_score": candidate_score,
        "delta": candidate_score - current_score,
        "current_result": str(Path(args.current).resolve()),
        "candidate_result": str(Path(args.candidate).resolve()),
        "candidate_artifact": "",
        "live_artifact": "",
    }

    if args.candidate_artifact:
        candidate_artifact = Path(args.candidate_artifact).resolve()
        staged_name = "proposed_" + candidate_artifact.name
        shutil.copy2(candidate_artifact, stage_dir / staged_name)
        manifest["candidate_artifact"] = str(stage_dir / staged_name)
    if args.live_artifact:
        manifest["live_artifact"] = str(Path(args.live_artifact).resolve())

    write_json(stage_dir / "manifest.json", manifest)
    write_json(stage_dir / "current_result.json", current)
    write_json(stage_dir / "candidate_result.json", candidate)
    report = [
        "# SkillOpt-Lite Gate Report",
        "",
        f"- Accepted: `{str(accepted).lower()}`",
        f"- Metric: `{metric}`",
        f"- Current score: `{current_score:.4f}`",
        f"- Candidate score: `{candidate_score:.4f}`",
        f"- Delta: `{candidate_score - current_score:.4f}`",
        "",
        "## Decision",
        "",
        "Candidate staged for review." if accepted else "Candidate rejected by strict gate.",
        "",
    ]
    (stage_dir / "report.md").write_text("\n".join(report), encoding="utf-8")
    print(f"{'ACCEPT' if accepted else 'REJECT'} delta={candidate_score - current_score:.4f} staging={stage_dir}")
    return 0 if accepted else 1


def cmd_adopt(args: argparse.Namespace) -> int:
    staging = Path(args.staging).resolve()
    manifest = json.loads((staging / "manifest.json").read_text(encoding="utf-8"))
    if not manifest.get("accepted") and not args.force:
        raise SystemExit("staged candidate was not accepted; pass --force to adopt anyway")
    candidate = manifest.get("candidate_artifact")
    live = manifest.get("live_artifact")
    if not candidate or not live:
        raise SystemExit("manifest must contain candidate_artifact and live_artifact")
    candidate_path = Path(candidate)
    live_path = Path(live)
    backup_dir = staging / "backup"
    backup_dir.mkdir(exist_ok=True)
    if live_path.exists():
        shutil.copy2(live_path, backup_dir / live_path.name)
    shutil.copy2(candidate_path, live_path)
    manifest["adopted_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
    write_json(staging / "manifest.json", manifest)
    print(f"adopted {candidate_path} -> {live_path}")
    return 0


def cmd_sample_cases(args: argparse.Namespace) -> int:
    sample = [
        {
            "id": "unit-tests",
            "split": "val",
            "judge": {"type": "command", "command": "pytest -q", "cwd": "."},
        },
        {
            "id": "format-check",
            "split": "val",
            "judge": {"type": "regex", "path": "artifact.txt", "pattern": "^Result:", "flags": ["multiline"]},
        },
        {
            "id": "manual-review",
            "split": "val",
            "judge": {"type": "manual", "accepted": False, "reason": "set true after user accepts"},
        },
    ]
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(json.dumps(item, ensure_ascii=False) for item in sample) + "\n", encoding="utf-8")
    print(out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SkillOpt-Lite local scoring and gate harness")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_score = sub.add_parser("score", help="score JSONL cases")
    p_score.add_argument("--cases", required=True)
    p_score.add_argument("--split", default="val", choices=["train", "val", "test", "all"])
    p_score.add_argument("--base-dir", default="")
    p_score.add_argument("--out", required=True)
    p_score.add_argument("--timeout", type=int, default=120)
    p_score.add_argument("--fail-on-case-failure", action="store_true")
    p_score.set_defaults(func=cmd_score)

    p_gate = sub.add_parser("gate", help="compare current and candidate score files")
    p_gate.add_argument("--current", required=True)
    p_gate.add_argument("--candidate", required=True)
    p_gate.add_argument("--metric", default="hard", choices=["hard", "soft", "mixed"])
    p_gate.add_argument("--mixed-weight", type=float, default=0.5)
    p_gate.add_argument("--stage-dir", required=True)
    p_gate.add_argument("--candidate-artifact", default="")
    p_gate.add_argument("--live-artifact", default="")
    p_gate.set_defaults(func=cmd_gate)

    p_adopt = sub.add_parser("adopt", help="adopt a staged candidate after review")
    p_adopt.add_argument("--staging", required=True)
    p_adopt.add_argument("--force", action="store_true")
    p_adopt.set_defaults(func=cmd_adopt)

    p_sample = sub.add_parser("sample-cases", help="write a starter cases.jsonl")
    p_sample.add_argument("--out", required=True)
    p_sample.set_defaults(func=cmd_sample_cases)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
