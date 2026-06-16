# Abstraction Pattern Cards

Source base: `book1` (*Code Simplicity*), especially `book1:chapter-5-change` and `book1:chapter-8-complexity`.

## Card: abstract-only-known-present-need

```yaml
id: abstract-only-known-present-need
name: Be only as generic as the current known need requires
category: abstractions
use_when:
  - code has speculative extension points or unused flexibility
  - a proposed abstraction is justified mainly by predicted future requirements
  - a generic path hides user-facing specifics
avoid_when:
  - multiple current variants already exist and change together
  - external complexity must be hidden behind a simpler interface
required_context:
  - current requirement
  - evidence of real variants
  - unused code or configuration paths
  - user-facing specificity that may be lost
  - maintenance cost of the abstraction
move: Remove or avoid generic machinery until there is evidence it is needed now.
recipe:
  - ask what present problem the abstraction solves
  - remove unused extension points or leave them unbuilt
  - keep code specific enough to report domain/user meaning clearly
  - add an abstraction later when a real second case appears
tradeoffs:
  - postponing abstraction can leave some duplication temporarily
  - premature abstraction can be costly because real future needs often differ from predictions
source_anchors:
  - book1:chapter-5-change
  - book1:appendix-laws
conflicts:
  - add-abstraction-vs-keep-concrete-code
  - remove-duplication-vs-preserve-meaning
validation:
  - no unused paths remain from guessed future needs
  - the code still handles current specific cases clearly
```

## Card: choose-entity-or-value-object

```yaml
id: choose-entity-or-value-object
name: Model identity only where continuity matters
category: abstractions
use_when:
  - an object has a unique ID by habit but may only describe attributes
  - two objects can have identical attributes but still need to be distinguished
  - mutability or sharing bugs suggest identity/value confusion
avoid_when:
  - the distinction is irrelevant to the task and changing it would be broad churn
  - framework terminology such as entity does not match the domain meaning
required_context:
  - whether users care which instance it is
  - lifecycle and continuity requirements
  - equality rules
  - sharing and mutability behavior
  - persistence and lookup needs
move: Use entities for conceptual identity across time; use value objects for interchangeable descriptive concepts, preferably immutable.
recipe:
  - ask whether replacing the instance with equal attributes would matter
  - define entity identity explicitly when continuity matters
  - make value objects conceptually whole and immutable where practical
  - remove artificial IDs from values unless infrastructure forces them
  - update equality, persistence, and tests to match the model
tradeoffs:
  - entities require lifecycle and identity discipline
  - value objects simplify sharing, copying, testing, and calculations
source_anchors:
  - book2:chapter-5-model-elements
  - book2:glossary
conflicts:
  - add-abstraction-vs-keep-concrete-code
validation:
  - equality and persistence behavior match the domain distinction
  - value objects can be safely copied or shared according to mutability rules
```

## Card: model-domain-service-only-for-real-domain-activity

```yaml
id: model-domain-service-only-for-real-domain-activity
name: Use a domain service for stateless operations that do not belong on an entity or value
category: abstractions
use_when:
  - an important domain operation coordinates multiple model objects
  - forcing the operation onto one object distorts that object's responsibility
  - a procedural manager object is hosting a meaningful domain activity
avoid_when:
  - the behavior naturally belongs to an entity or value object
  - the service would strip domain objects of their behavior
  - the operation is technical infrastructure or application coordination
required_context:
  - ubiquitous language for the operation
  - candidate entity/value owners
  - state held by the operation
  - layer where the responsibility belongs
move: Introduce a stateless domain service whose interface is expressed in domain model terms.
recipe:
  - name the operation as a domain activity
  - confirm no entity or value naturally owns it
  - define parameters and results as domain objects
  - keep application and infrastructure concerns outside the domain service
  - test the service through domain scenarios
tradeoffs:
  - services prevent awkward object responsibilities
  - excessive services can lead to an anemic model
source_anchors:
  - book2:chapter-5-model-elements
  - book2:chapter-4-layered-architecture
conflicts:
  - rich-domain-model-vs-simple-smart-ui
validation:
  - the service is stateless
  - entity and value objects still carry their natural behavior
```

## Card: make-implicit-concept-explicit

```yaml
id: make-implicit-concept-explicit
name: Promote hidden domain concepts into explicit model elements
category: abstractions
use_when:
  - domain experts use a term missing from code
  - reports, queries, or scripts contain repeated domain logic
  - a design area is awkward to explain or every new requirement adds complexity
avoid_when:
  - the term is only a synonym for an existing concept in the same context
  - the concept belongs to a different bounded context
required_context:
  - language used in conversations and tickets
  - duplicated logic or awkward responsibilities
  - domain expert feedback
  - tests or scenarios that demonstrate the concept
move: Add or reshape model elements so the hidden concept becomes visible in code and tests.
recipe:
  - listen for missing terms and awkward explanations
  - sketch the concept with domain experts or examples
  - move related behavior from scripts/reports/queries into the model
  - rename tests and code around the new term
  - iterate if the new model still feels awkward
tradeoffs:
  - explicit concepts can remove duplication and improve communication
  - premature concepts can add vocabulary without payoff
source_anchors:
  - book2:chapter-9-implicit-concepts
  - book2:chapter-2-ubiquitous-language
conflicts:
  - add-abstraction-vs-keep-concrete-code
validation:
  - domain scenarios become easier to express
  - related logic is less duplicated and less technical
```

## Card: factory-for-complex-creation

```yaml
id: factory-for-complex-creation
name: Encapsulate complex creation and invariant setup in a factory
category: abstractions
use_when:
  - clients assemble complex objects or aggregates manually
  - constructors expose internal structure or concrete subclasses
  - creation must enforce invariants atomically
avoid_when:
  - direct construction is simple, complete, and invariant-safe
  - a factory would hide a performance-sensitive implementation choice the caller must control
required_context:
  - aggregate boundary
  - required invariants at creation
  - client knowledge of internals
  - concrete classes or hierarchy being hidden
move: Move complex creation to a factory or factory method that returns a valid complete product.
recipe:
  - identify all required inputs for a valid object or aggregate
  - choose a natural factory site or standalone factory
  - make the operation atomic
  - enforce or delegate invariant checks
  - keep client code independent of internals
tradeoffs:
  - factories reduce client coupling
  - unnecessary factories obscure simple value objects or straightforward constructors
source_anchors:
  - book2:chapter-6-lifecycle
conflicts:
  - add-abstraction-vs-keep-concrete-code
validation:
  - clients can request a valid product without assembling internals
  - invalid creation cannot return an invalid object silently
```

## Card: organize-modules-by-domain-story

```yaml
id: organize-modules-by-domain-story
name: Organize domain modules around conceptual cohesion
category: abstractions
use_when:
  - domain code is packaged by technical pattern such as entities, services, repositories, or DTOs
  - one conceptual object is split across packages and hard to understand
  - package names do not appear in the team's domain language
  - changing a domain concept requires touching unrelated modules
avoid_when:
  - the code is infrastructure or framework glue where technical packaging is the clearest convention
  - moving modules would create broad churn without improving model comprehension
required_context:
  - current package/module graph
  - domain concepts and scenarios
  - coupling between modules
  - framework or deployment constraints
  - tests and import/update blast radius
move: Reshape domain packages so each module groups concepts readers should think about together.
recipe:
  - ask what story the current modules tell about the domain
  - find modules with low conceptual cohesion or high cross-module chatter
  - look for an overlooked concept that would group related behavior more naturally
  - choose names that can enter the ubiquitous language
  - move code in small tested steps, preserving public imports when needed
tradeoffs:
  - domain modules reduce cognitive load and support deeper model refactoring
  - package moves can be disruptive and may need staged compatibility
source_anchors:
  - book2:chapter-5-modules
  - book2:chapter-3-model-driven-design
  - book2:chapter-2-ubiquitous-language
conflicts:
  - technical-package-shape-vs-domain-module-story
  - rename-broadly-vs-protect-api
validation:
  - module names explain major domain concepts without opening every file
  - related domain behavior is easier to find and reason about after the move
```

## Card: wrap-unfixable-external-complexity

```yaml
id: wrap-unfixable-external-complexity
name: Hide unavoidable external complexity behind a simple local wrapper
category: abstractions
use_when:
  - complexity comes from hardware, platform, database, vendor API, or another boundary you cannot simplify directly
  - callers repeatedly handle the same external complexity
avoid_when:
  - the wrapper would merely rename an already simple interface
  - the boundary behavior is not yet understood well enough to simplify
required_context:
  - external system behavior
  - caller needs
  - repeated special cases
  - failure modes
move: Create a small interface that gives local code the simplest useful view of the external complexity.
recipe:
  - identify the smallest caller-facing operation
  - centralize the external-specific details
  - preserve domain-specific errors or results
  - migrate callers in small tested steps
tradeoffs:
  - wrappers add an abstraction layer
  - a good wrapper reduces repeated complexity and change cost
source_anchors:
  - book1:chapter-8-complexity
conflicts:
  - add-abstraction-vs-keep-concrete-code
validation:
  - callers become simpler
  - external-specific code is easier to find and change
```
