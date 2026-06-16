# Error Handling Pattern Cards

Source base: `book1` (*Code Simplicity*) and `book3` (*Grokking the System Design Interview*).

## Card: preserve-specific-error-meaning

```yaml
id: preserve-specific-error-meaning
name: Keep errors specific enough to help the user or caller
category: error-handling
use_when:
  - generic abstraction turns domain failures into vague technical errors
  - callers cannot tell what went wrong or what recovery is possible
  - over-generic code hides a useful distinction such as input type or operation
avoid_when:
  - detailed errors would expose sensitive implementation details
  - the caller truly needs only one domain-level failure
required_context:
  - actual failure modes
  - user or caller recovery needs
  - abstraction boundary
  - observability and logging path
move: Report or propagate errors at the most helpful domain level while keeping shared plumbing simple.
recipe:
  - identify what the user or caller needs to know
  - avoid flattening distinct failures into one generic message too early
  - centralize repeated mechanics without erasing domain meaning
  - test representative failure paths
tradeoffs:
  - specific errors can require more modeling
  - overly generic errors reduce helpfulness and make debugging harder
source_anchors:
  - book1:chapter-5-change
  - book1:chapter-8-complexity
conflicts:
  - add-abstraction-vs-keep-concrete-code
validation:
  - each important failure path answers what happened and what can be done next
  - shared handling still avoids copy/paste mechanics
```

## Card: make-overload-policy-explicit

```yaml
id: make-overload-policy-explicit
name: Make throttling, retry, and overload responses explicit at the boundary
category: error-handling
use_when:
  - callers can exceed safe request rates or resource limits
  - retry behavior may amplify load or duplicate work
  - rate limiting is based on unclear actor identity such as IP, user, tenant, or API key
avoid_when:
  - the code path is purely internal and already bounded by a stronger upstream contract
  - adding throttling would mask a correctness bug that should be fixed directly
required_context:
  - actor identity
  - quota scope and time window
  - retry semantics
  - storage or cache used for counters
  - user-facing failure response
  - abuse and shared-identity cases
move: Define how the boundary behaves under excess load before centralizing or generalizing the handler.
recipe:
  - decide whether limits apply per user, IP, tenant, token, API, or a hybrid
  - choose the time-window and counter strategy from the needed precision and memory cost
  - define the response for rejected, delayed, retried, and duplicate requests
  - consider sharding and caching for hot counters only with a consistency story
  - test both allowed and rejected cases, including shared-IP or unauthenticated paths where relevant
tradeoffs:
  - explicit overload policy protects the system and gives callers recoverable errors
  - rate limiting can unfairly block shared identities or create denial-of-service vectors if the actor key is wrong
source_anchors:
  - book3:rate-limiter
  - book3:caching
  - book3:consistent-hashing
  - book1:chapter-8-complexity
conflicts:
  - preserve-specific-error-meaning-vs-hide-internals
  - premature-optimization-vs-latent-scale-risk
validation:
  - callers receive a clear, documented overload signal
  - quota counters are bounded in memory and partitioned consistently enough for the promise
```
