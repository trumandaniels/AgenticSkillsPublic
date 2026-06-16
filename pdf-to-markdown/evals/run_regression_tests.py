#!/usr/bin/env python3
"""Regression tests for the pdf-to-markdown skill."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
CONVERTER = SKILL_DIR / "scripts" / "convert_pdf_to_markdown.py"
AUDITOR = SKILL_DIR / "scripts" / "audit_markdown_quality.py"
TMP_ROOT = Path(os.environ.get("PDF_TO_MARKDOWN_EVAL_TMP", ".pdf_to_markdown_eval_tmp"))


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def assert_true(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


_CASE_COUNTER = 0


def run_audit(auditor, markdown: str, assets: dict[str, bytes] | None = None) -> int:
    global _CASE_COUNTER
    _CASE_COUNTER += 1
    root = TMP_ROOT / f"case_{_CASE_COUNTER:03d}"
    root.mkdir(parents=True, exist_ok=True)
    md = root / "case.md"
    md.write_text(markdown, encoding="utf-8")
    if assets:
        for relpath, content in assets.items():
            target = root / relpath
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
    return auditor.audit(md, root, max_lookback=10)


def main() -> int:
    converter = load_module(CONVERTER, "pdf_to_markdown_converter")
    auditor = load_module(AUDITOR, "pdf_to_markdown_auditor")
    failures: list[str] = []

    cml_sample = """<CML.ARR ID="array3" EL.TYPE=FLOAT NAME="ATOMIC ORBITAL ELECTRON POPULATIONS"
SIZE= 30 GLO.ENT=CML.THE.AOEPOPS>
1.17947 0.95091 0.97175 1.00000
</CML.ARR>"""
    cml_output = "\n".join(converter.page_to_markdown(cml_sample, infer_headings=True, keep_line_breaks=False))
    assert_true(cml_output.startswith("```xml\n<CML.ARR"), "CML sample should render as fenced xml", failures)
    assert_true("### <CML" not in cml_output and "## SIZE=" not in cml_output, "CML sample must not become headings", failures)

    figure_bad = """Intro paragraph.

### Wall Tree Snake Rope

### Elephant Elephant Elephant Elephant

![Figure snapshot](assets/figure.png)

Figure 1.1 Example.
"""
    assert_true(run_audit(auditor, figure_bad, {"assets/figure.png": b"png"}) > 0, "Figure label soup should fail audit", failures)

    figure_good = """Intro paragraph.

![Figure snapshot](assets/figure.png)

Figure 1.1 Example.
"""
    assert_true(run_audit(auditor, figure_good, {"assets/figure.png": b"png"}) == 0, "Clean figure snapshot should pass audit", failures)

    missing_image = "![Missing](assets/missing.png)\n"
    assert_true(run_audit(auditor, missing_image) > 0, "Missing image should fail audit", failures)

    raw_sidebar = """> Body before.

## <<SIDE BAR>>

Sidebar text.

/square4

## <<END SIDE BAR>>
"""
    assert_true(run_audit(auditor, raw_sidebar) > 0, "Raw sidebar markers and square4 should fail audit", failures)

    clean_sidebar = """> [!NOTE]
> **Sidebar: Organic order**
>
> Sidebar text.
"""
    assert_true(run_audit(auditor, clean_sidebar) == 0, "Clean callout sidebar should pass audit", failures)

    inline_sidebar = "Body text. <<Sidebar>> Inline sidebar text. <<End sidebar>> More body text.\n"
    assert_true(run_audit(auditor, inline_sidebar) > 0, "Inline raw sidebar markers should fail audit", failures)

    raw_toc = """## Table of Contents

Acknowledgements ................................................................ 6
1. Crunching Knowledge ........................................................ 15

## Acknowledgements
"""
    assert_true(run_audit(auditor, raw_toc) > 0, "TOC dot leaders/page numbers should fail audit", failures)

    clean_toc = """## Table of Contents

- [Acknowledgements](#acknowledgements)
- [Crunching Knowledge](#crunching-knowledge)

## Acknowledgements
## Crunching Knowledge
"""
    assert_true(run_audit(auditor, clean_toc) == 0, "Linked TOC without page numbers should pass audit", failures)

    print(f"cases=9 failures={len(failures)}")
    for failure in failures:
        print(f"FAIL: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
