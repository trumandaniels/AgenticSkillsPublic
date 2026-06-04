# Conversion Quality Guide

Use this reference after the first PDF-to-Markdown extraction.

## Cleanup Checklist

- Remove repeated headers, footers, watermarks, and page numbers if they interrupt reading.
- Repair paragraph wrapping caused by PDF line breaks.
- Join words split by line-end hyphenation when the split is clearly mechanical.
- Preserve intentional hard breaks in addresses, poetry, code, forms, or legal clauses.
- Promote section labels to headings only when they are short, title-like, and structurally repeated.
- Keep list nesting shallow unless indentation is clear from the extracted text.
- Verify links and email addresses survived extraction; PDF text extraction often loses link targets.
- Mark missing figures with concise notes such as `[Figure omitted: caption text]` only when the source indicates the figure.

## Tables

PDF table extraction is unreliable without layout-aware tooling.

Use a Markdown table only when:

- The header row and columns are clear.
- Each row has the same number of cells.
- Cell contents are short enough to stay readable.

Otherwise, use a simple list or fenced text block and say the table needs manual review.

## Scanned PDFs

A scanned PDF may contain no embedded text. If extraction returns empty pages or garbled fragments, stop and ask for OCR-capable tooling. Do not infer the document from file names, surrounding context, or visible page images unless OCR or image inspection is actually performed.

## Final Review

Before delivering the Markdown file:

- Open the generated `.md` and skim beginning, middle, and end.
- Check the first page title and final page content are present.
- Search for broken artifacts like isolated single letters, repeated page numbers, or excessive blank lines.
- Tell the user if images, charts, tables, forms, or scanned pages were not fully converted.
