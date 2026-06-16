# Duplication Pattern Cards

Source base: `book1` (*Code Simplicity*), especially `book1:chapter-6-defects`.

## Card: single-source-of-truth-for-information

```yaml
id: single-source-of-truth-for-information
name: Keep each piece of information in one authoritative place
category: duplication
use_when:
  - the same string, rule, value, or code block appears in multiple places
  - a future change would require many synchronized edits
  - copy/paste code has already diverged accidentally
avoid_when:
  - similar-looking code represents different business meanings
  - centralization would create a vague abstraction that hides important differences
required_context:
  - duplicated locations
  - semantic sameness
  - likely change coupling
  - ownership boundaries
move: Centralize the shared information or behavior so future changes require the fewest edits.
recipe:
  - list the duplicated occurrences
  - confirm they mean the same thing
  - choose the smallest shared function, constant, template, or module
  - replace call sites in small tested steps
tradeoffs:
  - centralization can reduce defect risk by shrinking future changes
  - over-centralization can blur rules that should remain separate
source_anchors:
  - book1:chapter-6-defects
  - book1:appendix-laws
conflicts:
  - remove-duplication-vs-preserve-meaning
  - add-abstraction-vs-keep-concrete-code
validation:
  - a representative future change can be made in one place
  - behavior remains identical at replaced sites
```

## Card: distinguish-duplicate-concept-from-false-cognate

```yaml
id: distinguish-duplicate-concept-from-false-cognate
name: Separate true duplicate concepts from same-named concepts in different contexts
category: duplication
use_when:
  - two modules use the same term with different behavior
  - teams share code because names match, then add context-specific fields or rules
  - duplicate concepts appear across bounded contexts
avoid_when:
  - the code is inside one bounded context and should be unified
  - differences are accidental drift rather than legitimate model differences
required_context:
  - term meanings by team or module
  - bounded context boundaries
  - data/schema ownership
  - integration requirements
  - tests that expose expected behavior in each context
move: Unify true duplicates inside one context; split false cognates and translate between contexts when meanings differ.
recipe:
  - compare examples and rules for each use of the term
  - decide whether one model should own the concept
  - rename split concepts when meanings differ
  - add translation or anticorruption boundaries when integration is needed
  - add tests that lock each meaning
tradeoffs:
  - unifying duplicates reduces maintenance
  - merging false cognates corrupts both models
source_anchors:
  - book2:chapter-14-model-integrity
  - book1:chapter-6-defects
conflicts:
  - single-shared-model-vs-bounded-contexts
  - remove-duplication-vs-preserve-meaning
validation:
  - every same-named concept has one meaning within a bounded context
  - integration points translate explicitly rather than sharing accidental structure
```
