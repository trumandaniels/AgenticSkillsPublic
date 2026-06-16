---
name: code-patterns
description: Use for code readability review, refactoring choices, naming, comments, duplication, abstraction, domain-modeling, testability, error handling, API-boundary, storage, caching, queues, real-time transport, partitioning, scalability, and maintainability tradeoffs in existing code. Use when Codex needs to inspect local code context before choosing or critiquing a code-quality move. Do not use for style-only formatting, framework setup, greenfield architecture design, or broad rewrites without concrete code evidence.
---

# Code Patterns

Treat this skill as a decision system, not a style guide. Optimize for better coding behavior: inspect the right evidence, choose the smallest useful move, and validate that behavior and readability improved.

## Fast Path

1. Classify the request:
   - readability review
   - refactor existing code
   - naming or comments
   - duplication, abstraction, or domain-modeling
   - testability, error handling, API boundary, or scale/performance boundary
2. Inspect local evidence before applying any pattern:
   - call sites and consumers
   - tests and current behavior
   - public API or compatibility commitments
   - data flow, side effects, errors, and resource lifetime
   - framework idioms and nearby code conventions
3. Load the smallest relevant reference:
   - Use `references/routing-guide.md` when the task category is unclear.
   - Use `references/decision-trees.md` before making refactoring or design moves.
   - Use `references/review-checklists.md` for broad readability reviews.
   - Use one file under `references/pattern-cards/` only after the problem class is confirmed.
   - Use `references/conflicts-and-tradeoffs.md` when two patterns pull in opposite directions.
4. Prefer no change over a clever change when behavior risk is high, tests are missing, the API boundary is unclear, or the move adds indirection without semantic gain.
5. After edits, run relevant tests, lint, type checks, or focused validation. Review the diff for legibility and back out or narrow the change if the code did not clearly improve.

## Source Grounding

This skill currently includes operational guidance distilled from:

- `book1`: *Code Simplicity* by Max Kanat-Alexander
- `book2`: *Domain-Driven Design* by Eric Evans
- `book3`: *Grokking the System Design Interview*

Do not invent guidance from unprocessed books. When additional source books are added, populate:

- `references/source-map.md` with stable book and section anchors
- each `references/pattern-cards/*.md` file with source-grounded cards
- `references/taxonomy.md` with the final category map

Keep source excerpts short. Store anchors, section IDs, and compact operational rules rather than long summaries.

## Pattern Card Contract

Each substantive pattern should eventually include:

- `id`
- `name`
- `category`
- `use_when`
- `avoid_when`
- `required_context`
- `move`
- `recipe`
- `tradeoffs`
- `source_anchors`
- `conflicts`
- `validation`

Do not apply a pattern unless its `use_when` matches and its `avoid_when` does not.
