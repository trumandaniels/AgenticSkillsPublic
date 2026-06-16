# Routing Guide

Load the narrowest file that can answer the task.

| Request or symptom | Load first | Inspect before acting | Optional next file |
|---|---|---|---|
| Broad readability review | `review-checklists.md` | hotspots, long functions, comments, nesting, surprising names | matching pattern-card file |
| Refactor a function | `decision-trees.md`, `pattern-cards/functions.md` | call sites, tests, abstraction level, error paths | `conflicts-and-tradeoffs.md` |
| Improve names | `pattern-cards/naming.md` | symbol scope, consumers, domain vocabulary, exported status | `pattern-cards/api-boundaries.md` |
| Align code with domain language | `pattern-cards/naming.md`, `pattern-cards/abstractions.md` | domain terms, expert language, code names, model boundaries | `pattern-cards/api-boundaries.md` |
| Reorganize modules, packages, or namespaces in domain code | `pattern-cards/abstractions.md`, `decision-trees.md` | conceptual cohesion, package coupling, domain story, framework constraints | `conflicts-and-tradeoffs.md` |
| Remove or rewrite comments | `pattern-cards/comments.md` | whether names, types, or tests can carry the meaning | `conflicts-and-tradeoffs.md` |
| Reduce duplication | `pattern-cards/duplication.md` | semantic sameness, ownership, divergence risk | `pattern-cards/abstractions.md` |
| Judge an abstraction | `pattern-cards/abstractions.md` | number of real variants, consumer count, hidden cost | `conflicts-and-tradeoffs.md` |
| Choose entity/value/service/factory/repository | `pattern-cards/abstractions.md`, `pattern-cards/api-boundaries.md` | identity, lifecycle, invariants, creation/access needs | `decision-trees.md` |
| Improve testability | `pattern-cards/testability.md` | hidden I/O, nondeterminism, seams, fixture cost | `pattern-cards/api-boundaries.md` |
| Clarify errors | `pattern-cards/error-handling.md` | failure modes, retry semantics, user impact, observability | `pattern-cards/api-boundaries.md` |
| API boundary decision | `pattern-cards/api-boundaries.md` | consumers, compatibility, versioning, contracts | `conflicts-and-tradeoffs.md` |
| Multiple models or legacy integration | `pattern-cards/api-boundaries.md` | bounded contexts, translation points, ownership, tests | `conflicts-and-tradeoffs.md` |
| Prioritize DDD refactoring work | `decision-trees.md`, `conflicts-and-tradeoffs.md` | core domain, generic subdomains, support components, current pain, business differentiation | matching pattern-card file |
| Scalability, latency, throughput, or bottleneck review in existing code | `pattern-cards/api-boundaries.md`, `pattern-cards/testability.md` | current requirements, traffic shape, data volume, hot paths, failure modes, observability | `conflicts-and-tradeoffs.md` |
| Cache, index, sharding, or storage choice | `pattern-cards/api-boundaries.md` | read/write ratio, access patterns, consistency needs, hot keys, invalidation, write cost | `decision-trees.md` |
| Rate limiting, retry, overload, or backpressure behavior | `pattern-cards/error-handling.md` | actor identity, quota semantics, abuse cases, memory cost, user-facing failure response | `pattern-cards/api-boundaries.md` |
| Load balancing, failover, proxying, or edge routing | `pattern-cards/api-boundaries.md`, `pattern-cards/testability.md` | health checks, statelessness, sticky state, routing algorithm, redundancy, observability | `conflicts-and-tradeoffs.md` |
| Queue, worker, async processing, or notification flow | `pattern-cards/api-boundaries.md`, `pattern-cards/error-handling.md` | producer/consumer contract, delivery guarantee, ordering, retry, idempotency, queue growth | `pattern-cards/testability.md` |
| Long-polling, WebSocket, SSE, or realtime update choice | `pattern-cards/api-boundaries.md` | update direction, connection lifetime, client count, latency tolerance, fallback behavior | `conflicts-and-tradeoffs.md` |

If the category is still unclear after reading this file, inspect more code before loading more references.
