# Testability Pattern Cards

Source base: `book1` (*Code Simplicity*), `book2` (*Domain-Driven Design*), and `book3` (*Grokking the System Design Interview*).

## Card: test-precise-intended-behavior

```yaml
id: test-precise-intended-behavior
name: Test a precise behavior question and observe the answer
category: testability
use_when:
  - code changed and there is no reliable proof it still behaves as intended
  - a test is vague, unobserved, flaky, or not tied to a behavior expectation
  - a refactor needs characterization before movement
avoid_when:
  - the current task is pure formatting with no behavior impact
  - adding tests would require a broad design rewrite beyond the task scope
required_context:
  - intended behavior
  - observable result
  - relevant environment or input conditions
  - existing test harness
move: Add or run tests that ask a specific behavior question and fail visibly when the answer is wrong.
recipe:
  - state the behavior being protected
  - choose the smallest test or manual check that observes it
  - run it before and after risky changes when possible
  - prefer automated checks for code that will change again
tradeoffs:
  - tests cost time to write and maintain
  - without accurate testing, claims about behavior are guesses
source_anchors:
  - book1:chapter-9-testing
  - book1:appendix-laws
conflicts:
  - improve-testability-vs-minimize-change
validation:
  - the test fails for the wrong behavior and passes for the intended behavior
  - failures are visible and diagnosable
```

## Card: assert-domain-rules-at-the-interface

```yaml
id: assert-domain-rules-at-the-interface
name: Capture domain assertions and boundary translations in focused tests
category: testability
use_when:
  - an interface promises a domain result but tests only implementation mechanics
  - a method has side effects or invariants that callers must rely on
  - code translates between bounded contexts or external systems
avoid_when:
  - the assertion belongs to a different context and should be tested there
  - the behavior is not stable enough to specify yet
required_context:
  - domain rule or postcondition
  - public interface
  - bounded context boundary
  - input and output domain objects
  - failure signal
move: Write tests that state what must be true in domain terms after an operation or translation.
recipe:
  - name the rule in ubiquitous language
  - express the setup and expected result through public interfaces
  - cover successful and failing cases
  - for translations, test both semantic mapping and important loss/ambiguity
  - keep tests close to the boundary they protect
tradeoffs:
  - assertions make encapsulation safer and interfaces more predictable
  - overly brittle tests can freeze implementation details
source_anchors:
  - book2:chapter-10-supple-design
  - book2:chapter-14-model-integrity
  - book1:chapter-9-testing
conflicts:
  - improve-testability-vs-minimize-change
validation:
  - a failing assertion identifies the broken domain promise
  - context boundary tests catch translation drift
```

## Card: verify-bottlenecks-and-failure-modes

```yaml
id: verify-bottlenecks-and-failure-modes
name: Prove scale and reliability claims with focused observations
category: testability
use_when:
  - code claims a scalability, latency, throughput, reliability, or availability improvement
  - a bottleneck fix lacks before/after evidence
  - new cache, partition, replica, or load-balancing behavior changes system assumptions
avoid_when:
  - the task is a small local refactor with no performance or failure-mode claim
  - a full load test is disproportionate and a smaller measurement can answer the question
required_context:
  - stated requirement or hypothesis
  - latency, throughput, error, or recovery signal
  - representative traffic or data shape
  - failure mode under discussion
  - available metrics, logs, tests, or manual probe
move: Attach a small, explicit validation to each scale or reliability claim.
recipe:
  - state the claim in measurable terms
  - choose the narrowest test, metric, trace, or manual check that can falsify it
  - include hit/miss, degraded, or failure paths when a boundary mechanism is involved
  - capture before/after evidence where practical
  - leave an operational signal when the failure would recur in production
tradeoffs:
  - focused measurements avoid pretending that architecture diagrams prove behavior
  - exhaustive performance testing can exceed the task and should be reserved for high-risk paths
source_anchors:
  - book3:system-design-process
  - book3:distributed-characteristics
  - book3:load-balancing
  - book3:redundancy-replication
  - book1:chapter-9-testing
conflicts:
  - improve-testability-vs-minimize-change
  - optimize-performance-vs-preserve-simplicity
validation:
  - the evidence names what was measured and why it represents the risky path
  - failure or degraded-mode behavior is observable, not only assumed
```
