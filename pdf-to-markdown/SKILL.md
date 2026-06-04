---
name: pdf-to-markdown
description: Convert PDFs into clean Markdown while preserving document structure where possible. Use when Codex needs to extract text from PDF files and produce Markdown with headings, paragraphs, lists, page breaks, links noted in text, front matter when requested, or a cleaned .md output. Handles text-based PDFs with bundled pypdf tooling, guides OCR/scanned-PDF escalation, and supports post-processing for README/docs/article formatting.
---

# PDF To Markdown

## Workflow

1. Inspect the PDF request: identify whether the user wants a faithful extraction, a cleaned readable Markdown document, or a reorganized docs/article version.
2. Run `scripts/convert_pdf_to_markdown.py` for text-based PDFs.
3. Review the output for extraction damage: missing text, repeated headers/footers, broken paragraphs, page numbers, hyphenation, bad lists, and table loss.
4. Apply Markdown cleanup manually when needed. Read `references/conversion-quality.md` for cleanup heuristics and limits.
5. If pages are scanned images or extraction is mostly empty, do not fabricate content. Ask for OCR permission/tooling or use an available OCR-capable workflow.

## Quick Command

```bash
python /path/to/pdf-to-markdown/scripts/convert_pdf_to_markdown.py input.pdf -o output.md
```

Useful options:

```bash
python scripts/convert_pdf_to_markdown.py input.pdf -o output.md --title "Document Title"
python scripts/convert_pdf_to_markdown.py input.pdf -o output.md --no-page-breaks
python scripts/convert_pdf_to_markdown.py input.pdf -o output.md --keep-line-breaks
```

The converter is conservative. It extracts text, repairs common line wrapping and hyphenation, keeps lists readable, inserts optional page break comments, and infers likely headings. It does not recover images, charts, complex tables, annotations, or OCR text from scanned pages.

## Output Rules

- Preserve the source meaning and reading order; do not summarize unless the user asks.
- Use Markdown headings only when the PDF text clearly contains section titles.
- Keep page break comments (`<!-- page N -->`) when traceability matters; remove them for polished reading copies.
- Convert obvious bullets and numbered items into Markdown lists.
- Keep questionable tables as plain text or rebuild them manually only when the column structure is clear.
- Note unavailable content such as images, diagrams, signatures, or scanned pages instead of inventing it.

## When Extraction Fails

Treat these as OCR or layout cases:

- Many pages return empty text.
- Text is out of order because the PDF has columns or sidebars.
- Tables collapse into unreadable fragments.
- The PDF is mostly screenshots, scans, forms, handwriting, or image-only pages.

For these cases, report what failed and propose an OCR/layout-aware route before proceeding.
