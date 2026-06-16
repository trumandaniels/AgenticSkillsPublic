# Function Pattern Cards

Source base: `book1` (*Code Simplicity*), especially `book1:chapter-6-defects`, `book1:chapter-7-simplicity`, and `book1:chapter-8-complexity`.

## Card: split-complex-piece-in-small-steps

```yaml
id: split-complex-piece-in-small-steps
name: Split one complex piece into simpler self-contained pieces
category: functions
use_when:
  - a function or file is hard to understand as one unit
  - a feature or bug fix is difficult because existing code is messy
  - a piece mixes details that can be understood independently
avoid_when:
  - splitting would scatter a small coherent behavior
  - tests or manual checks cannot protect the behavior being moved
  - the new pieces would be abstractions without a known present need
required_context:
  - current tests or characterization options
  - call sites
  - data flow and mutation
  - error and resource lifetime
  - smallest behavior-preserving step
move: Redesign the individual piece in the smallest safe increment, then continue only if the code is easier to deal with.
recipe:
  - identify the specific complexity blocking the current task
  - choose one small subpiece with a clear responsibility
  - move or extract that subpiece without changing behavior
  - validate behavior immediately
  - reread the diff and stop if the code did not become simpler
tradeoffs:
  - small steps reduce defect risk but may take several iterations
  - too many tiny pieces can add navigation cost
source_anchors:
  - book1:chapter-6-defects
  - book1:chapter-8-complexity
conflicts:
  - extract-helper-vs-keep-locality
  - improve-testability-vs-minimize-change
validation:
  - tests or focused manual checks still pass
  - the next feature or bug fix is easier to express after the split
```

## Card: separate-command-from-query

```yaml
id: separate-command-from-query
name: Move calculations into side-effect-free functions where possible
category: functions
use_when:
  - an operation both changes state and performs complex calculation
  - callers cannot predict the consequences of invoking a method
  - a calculation could return a value object instead of mutating existing state
avoid_when:
  - the behavior is inherently a simple state-changing command
  - splitting would obscure one tiny atomic operation
required_context:
  - state changes caused by the operation
  - returned values
  - invariants affected by the command
  - candidate value objects
  - existing tests
move: Keep commands simple and put as much domain logic as possible into side-effect-free functions.
recipe:
  - identify observable state changes
  - separate pure calculation from mutation
  - move complex calculation into a value object when the concept fits
  - make the command call the function and apply the result simply
  - add assertions or tests for both result and state change
tradeoffs:
  - pure functions are easier to combine and test
  - commands are still necessary for lifecycle changes
source_anchors:
  - book2:chapter-10-supple-design
  - book2:chapter-5-model-elements
conflicts:
  - improve-testability-vs-minimize-change
validation:
  - repeated function calls do not change observable state
  - the command's side effects are explicit and covered by tests
```

## Card: follow-conceptual-contours

```yaml
id: follow-conceptual-contours
name: Split or combine operations along meaningful domain contours
category: functions
use_when:
  - a class or function mixes concepts that change for different reasons
  - tiny pieces force clients to understand how fragments fit together
  - new requirements repeatedly cut across the same awkward boundary
avoid_when:
  - the split is based only on line count or technical layering
  - the domain concept is not yet understood well enough to name
required_context:
  - axes of recent change
  - domain concepts in scenarios
  - duplicated behavior
  - client readability
  - module and aggregate boundaries
move: Refactor toward cohesive units that match meaningful distinctions in the domain.
recipe:
  - identify where new requirements force broad or awkward edits
  - ask what domain concept explains the change boundary
  - split or combine behavior around that concept
  - preserve simple, intention-revealing interfaces
  - validate that the next similar change is more localized
tradeoffs:
  - following domain contours can improve future adaptability without predicting the future
  - over-splitting can make clients assemble fragments manually
source_anchors:
  - book2:chapter-10-supple-design
  - book2:chapter-9-implicit-concepts
conflicts:
  - extract-helper-vs-keep-locality
validation:
  - the refactor localizes an existing or imminent domain change
  - the resulting units can be named in the ubiquitous language
```
