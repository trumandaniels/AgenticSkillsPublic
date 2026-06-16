"""Lightweight validator for code-patterns pattern card files."""

from __future__ import annotations

from pathlib import Path
import sys


REQUIRED_MARKERS = ("use_when", "avoid_when", "required_context", "source_anchors")


def main() -> int:
    skill_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    card_dir = skill_dir / "references" / "pattern-cards"
    if not card_dir.is_dir():
        print(f"missing pattern-card directory: {card_dir}")
        return 1

    failures: list[str] = []
    for path in sorted(card_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for marker in REQUIRED_MARKERS:
            if marker not in text:
                failures.append(f"{path.name}: missing {marker}")

    if failures:
        print("\n".join(failures))
        return 1

    print("pattern card validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
