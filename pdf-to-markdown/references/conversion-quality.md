# Conversion Quality Guide

Use this reference after the first PDF-to-Markdown extraction.

## Cleanup Checklist

- Remove repeated headers, footers, watermarks, and page numbers if they interrupt reading.
- Repair paragraph wrapping caused by PDF line breaks.
- Join words split by line-end hyphenation when the split is clearly mechanical.
- Preserve intentional hard breaks in addresses, poetry, code, forms, or legal clauses.
- Promote section labels to headings only when they are short, title-like, and structurally repeated.
- Do not promote code, markup, data arrays, configuration lines, or stack traces to headings. Lines containing angle-bracket tags, repeated `KEY=VALUE` attributes, or long runs of numbers should usually be fenced code blocks.
- Keep list nesting shallow unless indentation is clear from the extracted text.
- Verify links and email addresses survived extraction; PDF text extraction often loses link targets.
- Mark missing figures with concise notes such as `[Figure omitted: caption text]` only when the source indicates the figure.
- Around figures, remove OCR/text-layer label fragments that duplicate a captured snapshot and read out of order. Keep the figure snapshot and caption; recreate as Mermaid only when the relationships are unambiguous.
- Convert explicit sidebar markers such as `<<SIDE BAR>>`, `<<SIDEBAR BEGIN>>`, and `<<END SIDE BAR>>` into Markdown blockquotes or callouts. Remove marker text and stray glyph artifacts such as `/square4` when they only represent decorative separators.

## Tables

PDF table extraction is unreliable without layout-aware tooling.

Use a Markdown table only when:

- The header row and columns are clear.
- Each row has the same number of cells.
- Cell contents are short enough to stay readable.

Otherwise, use a simple list or fenced text block and say the table needs manual review.

## Code, Markup, and Data Examples

Use fenced code blocks for literal examples extracted from the PDF, including:

- XML, HTML, SGML, CML, or other angle-bracket markup.
- Configuration or record formats with repeated `KEY=VALUE` attributes.
- Numeric vectors, matrices, logs, stack traces, terminal output, and serialized data.

If the extraction split a literal block into bogus Markdown headings, remove the heading markers and rebuild the block with an appropriate fence such as `xml`, `json`, `text`, or no language tag when unsure.

## Figures and Diagrams

PDF text extraction often emits diagram labels in reading-order fragments. These should not remain as prose or headings when they duplicate the visual.

Use this order of preference:

1. Keep or create an image snapshot when the visual layout carries meaning.
2. Recreate as Mermaid only when nodes, labels, and relationships are clear from the source.
3. Use a short omitted-figure note only when the figure cannot be captured or reconstructed.

After figure cleanup, search for leftover label fragments near each image reference and verify the surrounding prose still reads naturally.

## Sidebars and Callouts

When the source has an explicit sidebar, preserve it as an aside instead of normal body prose.

Recommended rendering:

```markdown
> [!NOTE]
> **Sidebar: Short descriptive title**
>
> Sidebar text...
>
> Source or attribution line.
```

If the sidebar contains a quoted excerpt plus surrounding author commentary, keep all of it in the same callout and use paragraph breaks to separate commentary, quotation, attribution, and follow-up explanation. Do not use headings like `## <<SIDE BAR>>`.

## Scanned PDFs

A scanned PDF may contain no embedded text. If extraction returns empty pages or garbled fragments, stop and ask for OCR-capable tooling. Do not infer the document from file names, surrounding context, or visible page images unless OCR or image inspection is actually performed.

## Final Review

Before delivering the Markdown file:

- Open the generated `.md` and skim beginning, middle, and end.
- Check the first page title and final page content are present.
- Search for broken artifacts like isolated single letters, repeated page numbers, or excessive blank lines.
- Search for `^#+\s*</`, `^#+\s*[\w.-]+=`, and long numeric lines promoted near headings; these usually indicate code/data blocks were misrendered.
- Search figure-heavy chapters for nearby orphan labels, repeated captions, or headings made from diagram text.
- Search for raw sidebar markers (`<<SIDE`, `SIDEBAR`) and decorative extraction artifacts (`/square4`) near sidebars.
- Tell the user if images, charts, tables, forms, or scanned pages were not fully converted.
