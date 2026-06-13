#!/usr/bin/env python3
"""Convert a text-based PDF into conservative Markdown.

This script is intentionally dependency-light: it uses pypdf, which is commonly
available in Codex workspaces. It is best for PDFs with embedded text. It does
not OCR scanned pages or recover complex layout.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, List, Sequence

try:
    from pypdf import PdfReader
except ImportError as exc:  # pragma: no cover - exercised by environment
    raise SystemExit("Missing dependency: install pypdf or use a Python runtime that includes it.") from exc

BULLET_CHARS = {
    "\u2022": "-",
    "\u25e6": "-",
    "\u25aa": "-",
    "\u2013": "-",
    "\u2014": "-",
}

LIST_RE = re.compile(r"^(?:[-*+]|\d{1,3}[.)]|[A-Za-z][.)])\s+")
ORDERED_RE = re.compile(r"^(\d{1,3})[.)]\s+(.*)$")
WHITESPACE_RE = re.compile(r"[ \t]+")
SENTENCE_END_RE = re.compile(r"[.!?:;,)\]]$")
MARKUP_RE = re.compile(r"^</?[A-Za-z][\w:.-]*(?:\s+[^<>]*)?>$")
ASSIGNMENT_DENSE_RE = re.compile(r"(?:\b[\w:.-]+\s*=\s*\"?[^\s>\"]+\"?\s*){2,}")
NUMERIC_DATA_RE = re.compile(r"^[\d\s.+\-Ee]+$")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert a text-based PDF to Markdown.")
    parser.add_argument("pdf", type=Path, help="Input PDF path")
    parser.add_argument("-o", "--output", type=Path, help="Output Markdown path; defaults to input name with .md")
    parser.add_argument("--title", help="Optional H1 title to place at the top")
    parser.add_argument("--no-page-breaks", action="store_true", help="Do not insert <!-- page N --> comments")
    parser.add_argument("--keep-line-breaks", action="store_true", help="Preserve extracted line breaks instead of reflowing paragraphs")
    parser.add_argument("--no-infer-headings", action="store_true", help="Disable heading inference")
    return parser.parse_args(argv)


def extract_text_pages(pdf_path: Path) -> List[str]:
    reader = PdfReader(str(pdf_path))
    pages: List[str] = []
    for page in reader.pages:
        try:
            text = page.extract_text(extraction_mode="layout")
        except TypeError:
            text = page.extract_text()
        pages.append(text or "")
    return pages


def normalize_line(line: str) -> str:
    for source, replacement in BULLET_CHARS.items():
        line = line.replace(source, replacement)
    line = line.replace("\u00a0", " ")
    line = line.replace("\ufb01", "fi").replace("\ufb02", "fl")
    return WHITESPACE_RE.sub(" ", line).strip()


def is_probable_heading(line: str) -> bool:
    if not line or LIST_RE.match(line):
        return False
    if is_probable_code_or_data_line(line):
        return False
    if len(line) > 96 or len(line.split()) > 14:
        return False
    if SENTENCE_END_RE.search(line):
        return False
    letters = [ch for ch in line if ch.isalpha()]
    if not letters:
        return False
    uppercase_ratio = sum(1 for ch in letters if ch.isupper()) / len(letters)
    words = [word.strip("'\"") for word in line.split()]
    title_words = sum(1 for word in words if word[:1].isupper() and not word.isupper())
    if uppercase_ratio > 0.72 and len(letters) >= 4:
        return True
    if len(words) <= 4 and title_words == len(words):
        return True
    if len(words) <= 9 and title_words >= max(2, len(words) - 2):
        return True
    return False


def is_probable_code_or_data_line(line: str) -> bool:
    """Reject common literal examples before heading inference runs."""
    stripped = line.strip()
    if MARKUP_RE.match(stripped):
        return True
    if stripped.startswith(("<", "</")) or stripped.endswith((">", "/>")):
        return True
    if ASSIGNMENT_DENSE_RE.search(stripped):
        return True
    if NUMERIC_DATA_RE.match(stripped) and len(stripped.split()) >= 4:
        return True
    return False


def heading_level(line: str) -> int:
    if line.isupper() and len(line) <= 64:
        return 2
    return 3


def normalize_list_item(line: str) -> str:
    ordered = ORDERED_RE.match(line)
    if ordered:
        return f"{ordered.group(1)}. {ordered.group(2).strip()}"
    if line[:1] in {"-", "*", "+"}:
        return f"- {line[1:].strip()}"
    if re.match(r"^[A-Za-z][.)]\s+", line):
        return f"- {line[2:].strip()}"
    return line


def join_paragraph(lines: Sequence[str]) -> str:
    output = ""
    for line in lines:
        if not output:
            output = line
            continue
        if output.endswith("-") and line[:1].islower():
            output = output[:-1] + line
        else:
            output += " " + line
    return output.strip()


def emit_paragraph(buffer: List[str], output: List[str], keep_line_breaks: bool) -> None:
    if not buffer:
        return
    if keep_line_breaks:
        output.extend(buffer)
    else:
        output.append(join_paragraph(buffer))
    output.append("")
    buffer.clear()


def code_fence_language(lines: Sequence[str]) -> str:
    if any(line.strip().startswith(("<", "</")) for line in lines):
        return "xml"
    return ""


def emit_code_block(buffer: List[str], output: List[str]) -> None:
    if not buffer:
        return
    language = code_fence_language(buffer)
    output.append(f"```{language}")
    output.extend(buffer)
    output.append("```")
    output.append("")
    buffer.clear()


def page_to_markdown(text: str, *, infer_headings: bool, keep_line_breaks: bool) -> List[str]:
    output: List[str] = []
    paragraph: List[str] = []
    code_block: List[str] = []

    for raw_line in text.splitlines():
        line = normalize_line(raw_line)
        if not line:
            emit_code_block(code_block, output)
            emit_paragraph(paragraph, output, keep_line_breaks)
            continue

        if is_probable_code_or_data_line(line):
            emit_paragraph(paragraph, output, keep_line_breaks)
            code_block.append(line)
            continue

        emit_code_block(code_block, output)

        if infer_headings and is_probable_heading(line):
            emit_paragraph(paragraph, output, keep_line_breaks)
            output.append(f"{'#' * heading_level(line)} {line}")
            output.append("")
            continue

        if LIST_RE.match(line):
            emit_paragraph(paragraph, output, keep_line_breaks)
            output.append(normalize_list_item(line))
            continue

        paragraph.append(line)

    emit_code_block(code_block, output)
    emit_paragraph(paragraph, output, keep_line_breaks)
    return output


def compact_blank_lines(lines: Iterable[str]) -> List[str]:
    compacted: List[str] = []
    blank_count = 0
    for line in lines:
        if line.strip():
            blank_count = 0
            compacted.append(line.rstrip())
        else:
            blank_count += 1
            if blank_count <= 1:
                compacted.append("")
    while compacted and not compacted[-1].strip():
        compacted.pop()
    return compacted


def convert(pdf_path: Path, *, title: str | None, page_breaks: bool, keep_line_breaks: bool, infer_headings: bool) -> tuple[str, List[int]]:
    pages = extract_text_pages(pdf_path)
    empty_pages: List[int] = []
    lines: List[str] = []

    if title:
        lines.extend([f"# {title.strip()}", ""])

    for index, page_text in enumerate(pages, start=1):
        if not page_text.strip():
            empty_pages.append(index)
            if page_breaks:
                lines.extend([f"<!-- page {index}: no extractable text -->", ""])
            continue
        if page_breaks:
            lines.extend([f"<!-- page {index} -->", ""])
        lines.extend(page_to_markdown(page_text, infer_headings=infer_headings, keep_line_breaks=keep_line_breaks))

    markdown = "\n".join(compact_blank_lines(lines)) + "\n"
    return markdown, empty_pages


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    if not args.pdf.exists():
        print(f"Input PDF not found: {args.pdf}", file=sys.stderr)
        return 2
    output_path = args.output or args.pdf.with_suffix(".md")
    markdown, empty_pages = convert(
        args.pdf,
        title=args.title,
        page_breaks=not args.no_page_breaks,
        keep_line_breaks=args.keep_line_breaks,
        infer_headings=not args.no_infer_headings,
    )
    output_path.write_text(markdown, encoding="utf-8")
    print(f"Wrote {output_path}")
    if empty_pages:
        page_list = ", ".join(str(page) for page in empty_pages)
        print(f"Warning: no extractable text on page(s): {page_list}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
