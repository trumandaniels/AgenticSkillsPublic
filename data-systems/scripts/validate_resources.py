#!/usr/bin/env python3
"""Validate data-systems skill resource JSON and JSONL files."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def load_jsonl(path: Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if line.strip():
                try:
                    json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{path}:{line_number}: {exc}") from exc


def main() -> int:
    for dirname in ["references", "decision", "examples", "evals", "indexes"]:
        directory = ROOT / dirname
        if not directory.exists():
            raise FileNotFoundError(f"Missing resource directory: {directory}")

    for path in ROOT.rglob("*.json"):
        load_json(path)

    for path in ROOT.rglob("*.jsonl"):
        load_jsonl(path)

    print("OK: data-systems resource files are valid JSON/JSONL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
