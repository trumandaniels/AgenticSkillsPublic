# Knowledge Boundary Policy

Store only compact guidance that changes coding behavior.

Current processed source:
- `book1`: *Code Simplicity* by Max Kanat-Alexander.
- `book2`: *Domain-Driven Design* by Eric Evans.
- `book3`: *Grokking the System Design Interview*.

Treat only books listed as `processed-v1` in `source-map.md` as source-grounded. When new books appear in the source directory, add anchors before citing or carding them.

Include:
- inspection questions that prevent bad refactors
- decision trees where the right move depends on local evidence
- source-grounded pattern cards with use and avoid conditions
- validation checks that catch behavior or readability regressions
- source anchors that make rules traceable without long quotations

Exclude:
- motivational prose
- chapter summaries
- generic slogans such as "write clean code"
- large copied examples
- rules that cannot name their required context or failure mode

Use raw source books only when prepared references are insufficient or a conflict needs original nuance.
