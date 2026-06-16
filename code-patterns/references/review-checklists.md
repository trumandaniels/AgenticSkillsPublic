# Review Checklists

Use for broad readability or maintainability reviews. Findings should point to code evidence and a concrete next move.

## Hotspot Scan

- changes with unclear user value
- changes that solve predicted future needs rather than known present needs
- large changes that could be split into smaller behavior-preserving steps
- long functions with mixed abstraction levels
- names that require reading implementation to understand intent
- domain terms used by experts or tests that do not appear in code
- public methods whose names describe mechanics instead of purpose
- comments that restate code or contradict it
- duplicated branches that may or may not share business meaning
- duplicated concepts across modules that may actually be separate bounded contexts
- hidden I/O, time, randomness, global state, or network calls
- error handling that loses domain meaning or context
- over-generic code that hides specific user-facing cases
- domain logic mixed into UI, infrastructure, reports, or database queries
- domain modules/packages grouped by technical pattern rather than conceptual cohesion
- core-domain code receiving less clarity, testing, or refactoring attention than generic support code
- aggregate invariants enforced outside the aggregate root or not enforced atomically
- repositories or queries exposing persistence mechanics to clients
- scalability changes without stated requirements, traffic shape, or capacity assumptions
- cache code without an invalidation, eviction, or source-of-truth policy
- shard/partition keys that create hot partitions, cross-shard joins, or rebalancing traps
- indexes added without matching access patterns or write-cost review
- single points of failure in a boundary presented as reliable or highly available
- rate limiting that cannot explain actor identity, quota scope, or overload response
- performance claims without latency, throughput, error-rate, or alerting evidence
- load balancing that lacks health checks, redundant balancers, or a plan for stateful sessions
- queue-based workflows without delivery, retry, idempotency, ordering, or queue-growth semantics
- realtime update code using polling, long-polling, WebSockets, or SSE without matching data direction and connection costs
- public interfaces changed without compatibility analysis
- tests that do not ask a precise behavior question or expose failures clearly
- translation code between contexts that lacks focused tests

## Review Output Gate

For each issue, include:
- observed code evidence
- why it matters for readers or maintainers
- smallest useful change
- risk or stop condition
- validation needed

Skip generic advice that cannot name a file, symbol, branch, or behavior.
