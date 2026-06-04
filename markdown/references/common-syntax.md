# Common Markdown Syntax

Use this reference for portable Markdown or when the user asks for exact syntax.

## Baseline Syntax

| Goal | Preferred syntax | Notes |
| --- | --- | --- |
| H1/H2/H3 | `#`, `##`, `###` | Keep heading levels sequential. |
| Bold | `**text**` | Prefer asterisks for broad compatibility. |
| Italic | `*text*` | Avoid ambiguous underscores inside identifiers. |
| Blockquote | `> quoted text` | Repeat `>` for multi-paragraph quotes. |
| Ordered list | `1. item` | Repeated `1.` is acceptable in many renderers, but preserve local style. |
| Unordered list | `- item` | Prefer one marker style per file. |
| Inline code | `` `code` `` | Use for commands, paths, literals, and API names. |
| Code block | Fenced triple backticks | Add a language tag when known. |
| Horizontal rule | `---` | Keep blank lines around it. |
| Link | `[label](https://example.com)` | Use descriptive labels. |
| Image | `![alt text](image.png)` | Add a title only when useful. |

## Extended Syntax

These are common but not universal. Use them when the renderer supports them.

| Goal | Syntax | Notes |
| --- | --- | --- |
| Table | pipe table with separator row | Keep cells short; escape literal pipes. |
| Footnote | `Text[^1]` plus `[^1]: Note` | Supported by GitHub and many docs tools. |
| Heading ID | `### Title {#id}` | Common in static-site engines, not universal. |
| Definition list | `Term` then `: definition` | Renderer support varies. |
| Strikethrough | `~~text~~` | Common in GFM. |
| Task list | `- [ ] task`, `- [x] done` | Common in GitHub issues and READMEs. |
| Highlight | `==text==` | Not portable. |
| Subscript/superscript | `H~2~O`, `X^2^` | Renderer support varies. |

## Practical Checks

- Put blank lines around headings, lists, blockquotes, code fences, tables, and HTML blocks.
- Escape Markdown control characters when they should display literally.
- In tables, align columns for readability but do not depend on spacing for rendering.
- For nested lists, use consistent indentation from nearby files.
- For Markdown inside HTML blocks, test the renderer; many parsers stop parsing Markdown inside raw HTML.
- For generated docs, avoid editing generated regions manually unless the tool's markers are updated too.
