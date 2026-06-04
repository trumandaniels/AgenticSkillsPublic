---
name: markdown
description: Draft, edit, review, troubleshoot, or convert Markdown documents with attention to portable Markdown, GitHub Flavored Markdown, documentation quality, accessibility, tables, links, images, code fences, task lists, footnotes, front matter, callouts, Mermaid diagrams, badges, collapsible sections, and README/docs formatting. Use when Codex needs to create or improve Markdown files such as README.md, docs pages, changelogs, issue templates, Markdown emails, static-site content, or Markdown snippets for GitHub and similar renderers.
---

# Markdown

## Workflow

Start by identifying the target renderer and document purpose:

- **Portable Markdown**: Prefer basic syntax that works across Markdown apps. Read `references/common-syntax.md` when exact syntax or compatibility matters.
- **GitHub/docs Markdown**: Use GitHub Flavored Markdown patterns for tables, task lists, alerts, footnotes, Mermaid, badges, collapsible sections, and media. Read `references/advanced-patterns.md` for these.
- **Static-site Markdown**: Check whether front matter, shortcodes, MDX, or a site generator dialect is in play before editing syntax.

If the user gives an existing Markdown file, preserve its dialect, heading style, list style, line wrapping, front matter, and link conventions unless asked to modernize them.

## Writing Rules

- Use Markdown syntax before raw HTML when the syntax exists.
- Add raw HTML only when the target renderer supports it and Markdown cannot express the layout.
- Keep headings hierarchical with one `#` title unless the surrounding project uses another convention.
- Prefer fenced code blocks with a language tag.
- Use descriptive link text instead of bare URLs, except where bare URLs are intentionally rendered as embeds or autolinks.
- Give images meaningful alt text; use empty alt text only for decorative images.
- Avoid fragile formatting hacks in content intended for many renderers.
- Keep tables simple; move complex layouts to HTML, docs components, or prose.
- Validate that generated Markdown renders plausibly in the target environment before declaring it final.

## Editing Existing Files

When revising Markdown:

1. Inspect nearby files for local conventions.
2. Preserve front matter keys, comments, anchors, include directives, and generated sections unless the user asks to change them.
3. Check that heading links, relative links, image paths, reference definitions, and table alignment remain valid.
4. Keep prose changes separate from syntax-only cleanup when possible so diffs stay reviewable.

## Source Notes

This skill is grounded in the Markdown Guide cheat sheet and David Wells' `advanced-markdown` examples. Use those references as patterns, not as text to copy wholesale:

- Markdown Guide cheat sheet: https://www.markdownguide.org/cheat-sheet/
- Advanced Markdown: https://github.com/DavidWells/advanced-markdown
