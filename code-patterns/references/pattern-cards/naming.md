# Naming Pattern Cards

Source base: `book1` (*Code Simplicity*), especially `book1:chapter-7-simplicity`.

## Card: name-for-communication-and-readability

```yaml
id: name-for-communication-and-readability
name: Choose names that fully communicate without overwhelming the line
category: naming
use_when:
  - a variable, function, class, or module name hides its purpose
  - a name is so long that the surrounding expression becomes hard to scan
avoid_when:
  - the symbol is public and consumers or migration risk have not been inspected
  - the rename is stylistic and nearby conventions already communicate clearly
required_context:
  - symbol scope
  - call sites and consumers
  - frequency of use in expressions
  - nearby naming conventions
  - domain vocabulary
move: Rename the symbol so a reader can understand what it is or does from the name and its local context.
recipe:
  - inspect the call sites where the name appears
  - choose the shortest name that still carries the needed meaning
  - keep the name consistent with nearby code
  - rerun tests or type checks that cover the affected consumers
tradeoffs:
  - longer names can clarify rarely used concepts
  - shorter names can improve dense expressions when the context is already clear
source_anchors:
  - book1:chapter-7-simplicity
  - book1:appendix-laws
conflicts:
  - rename-broadly-vs-protect-api
validation:
  - a reader should not need to open the implementation just to understand the symbol's role
  - the changed lines should remain easy to scan
```

## Card: align-code-with-ubiquitous-language

```yaml
id: align-code-with-ubiquitous-language
name: Align code, tests, and discussion around the same domain language
category: naming
use_when:
  - domain experts, tickets, tests, and code use different words for the same concept
  - developers translate between business terms and technical names in their heads
  - a term used repeatedly in conversation is absent from the design
avoid_when:
  - the term belongs outside the current bounded context
  - the code is purely technical infrastructure with no domain meaning
required_context:
  - domain terms used by experts or users
  - current class, method, module, and test names
  - bounded context for the term
  - cases where the term is awkward, ambiguous, or contradictory
move: Rename or reshape code so important domain concepts have the same names in speech, tests, documents, and implementation.
recipe:
  - collect terms used in real scenarios and tests
  - compare them to names in code
  - identify translation layers, missing concepts, and false synonyms
  - rename or introduce model elements in small tested steps
  - update tests to use the same domain terms
tradeoffs:
  - shared language improves model/code alignment
  - forcing one term across different bounded contexts can create false unity
source_anchors:
  - book2:chapter-2-ubiquitous-language
  - book2:chapter-3-model-driven-design
conflicts:
  - single-shared-model-vs-bounded-contexts
  - rename-broadly-vs-protect-api
validation:
  - a domain scenario can be narrated using names visible in the code
  - domain experts and developers use the same term within the same context
```

## Card: intention-revealing-interface

```yaml
id: intention-revealing-interface
name: Name public interfaces by purpose rather than mechanism
category: naming
use_when:
  - a caller must inspect implementation to know what a method or class is for
  - a method name describes mechanics rather than the domain effect
  - tests read like implementation scripts instead of scenario statements
avoid_when:
  - the element is an internal mechanism intentionally hidden from domain code
  - the current name is conventional in the framework and changing it would confuse readers
required_context:
  - caller code
  - tests written from the client developer perspective
  - ubiquitous language terms
  - public API compatibility
move: Rename classes, methods, and arguments so callers can infer purpose and effect without reading internals.
recipe:
  - write or inspect a behavior test from the caller's point of view
  - identify names that force mechanical thinking
  - rename toward the domain intention
  - keep implementation details behind the interface
  - run tests and review caller readability
tradeoffs:
  - intention-revealing names can make interfaces more stable and expressive
  - too much domain jargon can confuse code outside the bounded context
source_anchors:
  - book2:chapter-10-supple-design
  - book2:chapter-2-ubiquitous-language
conflicts:
  - rename-broadly-vs-protect-api
validation:
  - caller code reads as a domain action or question
  - tests demonstrate intended behavior without exposing implementation details
```
