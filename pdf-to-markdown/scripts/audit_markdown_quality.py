#!/usr/bin/env python3
"""Audit Markdown converted from PDFs for common extraction artifacts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


HEADINGIZED_CODE_RE = re.compile(
    r"^#{1,6}\s+(?:</?[A-Za-z][\w:.-]*\b|[\w:.-]+\s*=|[\"']?SELECT\b|[A-Z0-9_]+\s+WHERE\b)"
)
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
RAW_SIDEBAR_RE = re.compile(r"<<\s*(?:END\s+)?SIDE\s*BAR\s*>>|<<\s*SIDEBAR\b[^>]*>>", re.IGNORECASE)
DECORATIVE_ARTIFACT_RE = re.compile(r"^(?:/square4\s*)+$", re.IGNORECASE)
TOC_HEADING_RE = re.compile(r"^#{1,6}\s+(?:table of contents|contents)\s*$", re.IGNORECASE)
HEADING_RE = re.compile(r"^#{1,6}\s+")
TOC_DOT_LEADER_RE = re.compile(r"(?:\.{3,}|…{2,}).*\b\d{1,4}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit converted Markdown for PDF extraction artifacts.")
    parser.add_argument("markdown", type=Path, help="Markdown file to audit")
    parser.add_argument("--root", type=Path, help="Root directory for relative image references")
    parser.add_argument(
        "--max-lookback",
        type=int,
        default=10,
        help="Lines before an image to inspect for label-fragment heading clusters",
    )
    return parser.parse_args()


def is_labelish(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith("![") or stripped.startswith("Figure "):
        return False
    if stripped.startswith(("### ", "#### ", "##### ", "###### ")):
        return True
    if len(stripped) <= 90 and not stripped.endswith((".", "?", "!", ":")):
        return True
    return False


def audit(markdown_path: Path, root: Path, max_lookback: int) -> int:
    text = markdown_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    issue_count = 0

    for index, line in enumerate(lines, start=1):
        if HEADINGIZED_CODE_RE.match(line):
            print(f"{markdown_path}:{index}: headingized-code: {line}")
            issue_count += 1
        if RAW_SIDEBAR_RE.search(line):
            print(f"{markdown_path}:{index}: raw-sidebar-marker: {line}")
            issue_count += 1
        if DECORATIVE_ARTIFACT_RE.match(line.strip()):
            print(f"{markdown_path}:{index}: decorative-artifact: {line}")
            issue_count += 1

    in_toc = False
    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        if TOC_HEADING_RE.match(stripped):
            in_toc = True
            continue
        if in_toc and HEADING_RE.match(stripped):
            in_toc = False
        if in_toc and TOC_DOT_LEADER_RE.search(stripped):
            print(f"{markdown_path}:{index}: toc-dot-leader-page-number: {line}")
            issue_count += 1

    for index, line in enumerate(lines):
        match = IMAGE_RE.search(line)
        if not match:
            continue

        image_ref = match.group(1)
        image_path = (root / image_ref).resolve()
        if not image_path.exists():
            print(f"{markdown_path}:{index + 1}: missing-image: {image_ref}")
            issue_count += 1

        start = max(0, index - max_lookback)
        window = lines[start:index]
        suffix_start = 0
        for offset, candidate in enumerate(window):
            if candidate.strip() and not is_labelish(candidate):
                suffix_start = offset + 1
        window = window[suffix_start:]
        start = start + suffix_start
        suspicious_headings = [
            (start + offset + 1, candidate)
            for offset, candidate in enumerate(window)
            if candidate.startswith(("### ", "#### ", "##### ", "###### "))
        ]
        nonblank_window = [candidate for candidate in window if candidate.strip()]
        has_cluster = len(suspicious_headings) >= 2 or (
            len(suspicious_headings) >= 1 and len(nonblank_window) >= 3
        ) or len(nonblank_window) >= 3
        if has_cluster and all(is_labelish(candidate) for candidate in nonblank_window):
            joined = " | ".join(f"{line_no}: {candidate}" for line_no, candidate in suspicious_headings)
            print(f"{markdown_path}:{index + 1}: image-label-cluster before {image_ref}: {joined}")
            issue_count += 1

    return issue_count


def main() -> int:
    args = parse_args()
    if not args.markdown.exists():
        print(f"Markdown file not found: {args.markdown}", file=sys.stderr)
        return 2
    root = args.root or args.markdown.parent
    issues = audit(args.markdown, root, args.max_lookback)
    print(f"issues={issues}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
