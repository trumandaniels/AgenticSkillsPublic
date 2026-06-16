# API Boundary Pattern Cards

Source base: `book1` (*Code Simplicity*), `book2` (*Domain-Driven Design*), and `book3` (*Grokking the System Design Interview*).

## Card: redesign-boundary-one-step-at-a-time

```yaml
id: redesign-boundary-one-step-at-a-time
name: Move boundary-specific complexity behind stable operations incrementally
category: api-boundaries
use_when:
  - technology-specific details are spread through the codebase
  - supporting a new backend, platform, database, or protocol would multiply conditionals
  - callers must understand external complexity to do ordinary work
avoid_when:
  - only one call site exists and the direct code is already simple
  - the proposed boundary is speculative and not needed for a current feature
required_context:
  - current external dependency
  - current feature or migration need
  - repeated operations
  - consumers and compatibility constraints
  - tests for old and new behavior
move: Centralize boundary operations in small tested steps instead of spreading special cases everywhere.
recipe:
  - replace standardizable calls one file or operation at a time
  - create focused helpers for nonstandard operations
  - migrate callers incrementally
  - keep validating existing behavior after each step
tradeoffs:
  - incremental migration takes patience
  - spreading boundary conditionals can double complexity and exceed maintenance capacity
source_anchors:
  - book1:chapter-8-complexity
conflicts:
  - add-abstraction-vs-keep-concrete-code
  - rewrite-vs-redesign-in-place
validation:
  - existing behavior still works after each step
  - new boundary support needs less code than scattered conditionals would require
```

## Card: isolate-domain-layer

```yaml
id: isolate-domain-layer
name: Keep domain logic out of UI, application coordination, and infrastructure
category: api-boundaries
use_when:
  - business rules live in controllers, widgets, database scripts, reports, or adapters
  - UI or persistence changes risk changing domain behavior
  - automated tests are awkward because domain logic is mixed with technology
avoid_when:
  - the app is intentionally a simple Smart UI with few business rules and modest ambition
  - extracting a domain layer would exceed the task scope without immediate risk reduction
required_context:
  - business rule locations
  - application orchestration responsibilities
  - infrastructure and persistence mechanics
  - tests around the rule
move: Move domain rules into a domain layer expressed in model terms and keep application services thin.
recipe:
  - identify the rule and current technical host
  - add or find the domain object/service that should own the rule
  - move behavior in a small tested step
  - leave UI/application code to coordinate and delegate
  - keep infrastructure details behind interfaces or repositories
tradeoffs:
  - isolation makes complex domains easier to evolve
  - simple data-entry apps may not justify model-driven overhead
source_anchors:
  - book2:chapter-4-layered-architecture
  - book2:chapter-3-model-driven-design
conflicts:
  - rich-domain-model-vs-simple-smart-ui
validation:
  - domain rule tests can run without UI or persistence details where practical
  - application code reads as orchestration, not business policy
```

## Card: aggregate-boundary-for-invariants

```yaml
id: aggregate-boundary-for-invariants
name: Use aggregate roots to protect consistency boundaries
category: api-boundaries
use_when:
  - callers directly mutate objects that should be consistent together
  - transaction scope is unclear
  - invariants span a cluster of related entities and values
avoid_when:
  - the relationship does not require immediate consistency
  - a large aggregate would create avoidable contention or loading cost
required_context:
  - invariants
  - transaction boundaries
  - global vs local identity
  - external references
  - persistence and concurrency behavior
move: Define an aggregate root and route external changes through it so invariants are enforced atomically.
recipe:
  - identify the consistency rules that must hold after each change
  - choose the entity with global identity as root
  - prevent external references to internal members except transiently
  - make repository access target aggregate roots
  - test invariant enforcement at the root
tradeoffs:
  - aggregates make consistency boundaries explicit
  - oversized aggregates can harm concurrency and performance
source_anchors:
  - book2:chapter-6-lifecycle
conflicts:
  - add-abstraction-vs-keep-concrete-code
validation:
  - no external code persists direct references to aggregate internals
  - every committed aggregate change satisfies its invariants
```

## Card: repository-for-aggregate-root-access

```yaml
id: repository-for-aggregate-root-access
name: Access persistent aggregate roots through repositories in model terms
category: api-boundaries
use_when:
  - client code builds SQL, ORM queries, or storage mechanics directly
  - domain logic leaks into query code
  - tests are hard because persistence is entangled with domain behavior
avoid_when:
  - the object is internal to an aggregate and should be reached by traversal
  - a value object is being globally searched only because identity has not been modeled clearly
required_context:
  - aggregate roots needing global access
  - query criteria in domain terms
  - persistence technology
  - transaction ownership
move: Provide repository methods that act like a conceptual collection of aggregate roots and hide storage mechanics from clients.
recipe:
  - list objects that truly need global lookup
  - create repository methods using ubiquitous language
  - return domain objects or summaries, not persistence rows
  - keep transaction control outside ordinary repository methods unless local convention says otherwise
  - provide in-memory or fake repositories for tests when useful
tradeoffs:
  - repositories keep clients model-focused and testable
  - careless repository use can hide expensive queries that developers still need to understand
source_anchors:
  - book2:chapter-6-lifecycle
  - book2:chapter-4-layered-architecture
conflicts:
  - improve-testability-vs-minimize-change
validation:
  - clients no longer compose persistence mechanics for ordinary domain lookup
  - repository tests cover expensive or semantically important queries
```

## Card: bounded-context-and-anticorruption-layer

```yaml
id: bounded-context-and-anticorruption-layer
name: Protect model integrity with named bounded contexts and translation layers
category: api-boundaries
use_when:
  - the same term means different things in different teams, modules, or systems
  - legacy or external models leak into new domain code
  - integrations pass primitive data whose meaning is assumed rather than translated
avoid_when:
  - one team owns a unified model and can keep it integrated with tests and communication
  - integration is unnecessary and separate ways would be cheaper
required_context:
  - models in play
  - ownership and team boundaries
  - code/schema boundaries
  - points of contact
  - translation rules and tests
move: Name each bounded context, make the context map explicit, and translate between models at a protected boundary.
recipe:
  - identify where each model applies
  - name the contexts in the team's language
  - describe contact points and data/function flow
  - introduce translators, adapters, or an anticorruption layer where model leakage is risky
  - test boundary translations with domain examples
tradeoffs:
  - bounded contexts preserve clarity and allow different models to evolve
  - translation layers cost effort and should be justified by integration value
source_anchors:
  - book2:chapter-14-model-integrity
  - book2:chapter-10-supple-design
conflicts:
  - single-shared-model-vs-bounded-contexts
validation:
  - a developer can tell which context a file or concept belongs to
  - foreign model terms do not appear in core domain code except inside translation code
```

## Card: requirements-capacity-before-scale-mechanism

```yaml
id: requirements-capacity-before-scale-mechanism
name: Clarify requirements and capacity before adding scale machinery
category: api-boundaries
use_when:
  - code adds caching, partitioning, queues, replicas, or load balancing without stated pressure
  - a performance change claims scalability but does not name latency, throughput, or data volume
  - API shape or data model is being decided for an existing high-traffic path
avoid_when:
  - the mechanism is already required by platform policy and the task is only local integration
  - the code path is small, stable, and not under current or near-term scale pressure
required_context:
  - functional requirements
  - latency and throughput expectations
  - data volume and growth estimate
  - read/write ratio
  - callers and API contract
  - current bottleneck evidence
move: State the requirement, interface, rough capacity, and likely bottleneck before changing architecture.
recipe:
  - identify what the code must support now
  - estimate requests, storage, bandwidth, or fanout only as precisely as needed
  - map requests to APIs and data entities
  - name the bottleneck the mechanism is meant to relieve
  - defer mechanisms that solve only imagined scale
tradeoffs:
  - lightweight estimation prevents expensive accidental architecture
  - too much estimation can slow a small bug fix
source_anchors:
  - book3:system-design-process
  - book3:distributed-characteristics
  - book1:chapter-5-change
conflicts:
  - add-abstraction-vs-keep-concrete-code
  - premature-optimization-vs-latent-scale-risk
validation:
  - the change can name the requirement and pressure it addresses
  - the chosen mechanism matches observed or credible near-term load
```

## Card: cache-hot-read-paths-with-invalidation-plan

```yaml
id: cache-hot-read-paths-with-invalidation-plan
name: Cache repeated reads only with a source-of-truth and invalidation policy
category: api-boundaries
use_when:
  - repeated reads dominate a path and downstream calls or queries are the bottleneck
  - recently or frequently requested data is likely to be requested again
  - static or derived data can be served faster near the caller
avoid_when:
  - correctness requires fresh data and no consistency policy exists
  - write traffic dominates and cache updates would add more cost than value
required_context:
  - source of truth
  - read/write ratio
  - freshness tolerance
  - invalidation or update strategy
  - eviction policy
  - cache placement and key choice
move: Add cache behavior only when the stale-data and eviction story is explicit.
recipe:
  - identify the repeated read and expected hit pattern
  - choose cache location close to the caller without hiding ownership
  - define invalidation, write-through, write-around, or write-back behavior
  - choose eviction based on actual access pattern
  - test stale-data and miss paths, not only hits
tradeoffs:
  - caches can turn impossible latency targets into feasible ones
  - cache coherence and write-back durability risks can create subtle defects
source_anchors:
  - book3:caching
  - book3:consistent-hashing
conflicts:
  - premature-optimization-vs-latent-scale-risk
validation:
  - a developer can explain when cached data changes or expires
  - tests or manual checks cover cache hit, miss, invalidation, and stale-data behavior
```

## Card: partition-by-access-pattern-and-hotspots

```yaml
id: partition-by-access-pattern-and-hotspots
name: Choose partition keys from access patterns and hot-spot risk
category: api-boundaries
use_when:
  - one database, table, service, or queue cannot handle current data or traffic
  - a shard key is being introduced or reviewed
  - cross-partition joins, transactions, or referential integrity become expensive
avoid_when:
  - the data set and traffic fit comfortably without partitioning
  - the proposed partition key is chosen only because it is easy to hash
required_context:
  - dominant queries and write paths
  - data distribution
  - hot entities or tenants
  - cross-shard operations
  - rebalancing strategy
  - consistency and transaction needs
move: Partition around real access paths, avoiding keys that concentrate load or force frequent cross-shard work.
recipe:
  - list the hottest reads and writes
  - identify entities with uneven distribution or celebrity behavior
  - compare horizontal, vertical, directory, hash, and composite options
  - check joins, transactions, referential integrity, and rebalancing impact
  - prefer consistent hashing or directory indirection only when node churn or rebalancing justifies the complexity
tradeoffs:
  - partitioning can improve performance, manageability, and availability
  - it can also move referential integrity and joins into application code
source_anchors:
  - book3:sharding-partitioning
  - book3:consistent-hashing
  - book3:ticketmaster-concurrency
conflicts:
  - premature-optimization-vs-latent-scale-risk
validation:
  - hot entities are distributed or explicitly handled
  - the design names the operations that become harder after sharding
```

## Card: choose-storage-by-access-and-consistency-needs

```yaml
id: choose-storage-by-access-and-consistency-needs
name: Pick storage from access pattern, transaction, and consistency needs
category: api-boundaries
use_when:
  - code or schema changes assume SQL, NoSQL, document, key-value, graph, or column storage
  - a repository or adapter hides storage tradeoffs that affect callers
  - availability, consistency, or partition tolerance matters to behavior
avoid_when:
  - the project already has a mandated storage layer and the task does not touch its limits
  - storage choice is being used to avoid modeling the domain or access pattern
required_context:
  - data shape
  - query pattern
  - transaction and ACID needs
  - growth and distribution expectations
  - consistency and availability requirements
  - operational constraints
move: Match the storage boundary to how the system reads, writes, scales, and recovers.
recipe:
  - identify whether the data is structured, relational, document-like, graph-like, or key-addressed
  - determine whether transactions and strong consistency are central to correctness
  - check whether vertical scale is enough or horizontal scale is required
  - make CAP-style tradeoffs explicit for distributed storage
  - expose storage limits through repository or boundary tests where callers rely on them
tradeoffs:
  - SQL often protects structured data and transactions well
  - NoSQL options can improve horizontal scale or flexible schemas while reducing transactional guarantees
source_anchors:
  - book3:sql-nosql-cap
  - book2:chapter-6-lifecycle
conflicts:
  - rich-domain-model-vs-simple-smart-ui
  - premature-optimization-vs-latent-scale-risk
validation:
  - storage choice follows named access and consistency needs
  - code does not promise guarantees the storage cannot provide
```

## Card: add-indexes-from-observed-access-patterns

```yaml
id: add-indexes-from-observed-access-patterns
name: Add indexes for observed reads while accounting for write cost
category: api-boundaries
use_when:
  - a query path scans too much data or cannot meet latency expectations
  - an index is proposed as a performance fix
  - a table or collection has both hot reads and significant writes
avoid_when:
  - the query is rare, bounded, or already fast enough
  - write throughput is the real bottleneck and the index is not needed for a hot read
required_context:
  - query plan or evidence of slow lookup
  - columns or keys used for access
  - read frequency
  - insert/update/delete frequency
  - index size and maintenance cost
move: Add or keep indexes only when they match real lookup paths and justify their write overhead.
recipe:
  - identify the specific lookup or ordering requirement
  - confirm the index can support that access path
  - estimate or measure write amplification
  - remove unused indexes when they only tax writes
  - validate with query plans or performance checks
tradeoffs:
  - indexes can make targeted reads practical on large data sets
  - every maintained index slows writes and consumes storage
source_anchors:
  - book3:indexes
conflicts:
  - premature-optimization-vs-latent-scale-risk
validation:
  - the hot query improves or is explainably protected
  - write-heavy paths still meet their needs after index maintenance cost
```

## Card: balance-traffic-across-healthy-redundant-nodes

```yaml
id: balance-traffic-across-healthy-redundant-nodes
name: Route traffic only across healthy redundant capacity
category: api-boundaries
use_when:
  - one server, worker, cache, or database endpoint is becoming a bottleneck
  - the code assumes a load balancer or proxy but does not define health behavior
  - a scaling change needs multiple service instances or redundant entry points
avoid_when:
  - a single instance is enough and operational complexity would dominate
  - the service is stateful and no affinity or state-sharing plan exists
required_context:
  - traffic shape and request duration
  - health check signal
  - routing algorithm or policy
  - state/session affinity needs
  - redundant balancer or failover plan
  - observability for elevated errors or slow nodes
move: Put balancing behind an explicit health, routing, and failover contract instead of assuming more instances automatically improve reliability.
recipe:
  - confirm the bottleneck or availability requirement
  - define what makes a backend healthy or overloaded
  - choose a routing policy that matches request shape, such as round-robin, least connection, weighted, or IP hash
  - remove or externalize sticky state where possible
  - make the balancer itself redundant when it is on a critical path
  - test unhealthy-node and failover behavior
tradeoffs:
  - load balancing can improve responsiveness and availability
  - stateful backends and a nonredundant balancer can create new failure modes
source_anchors:
  - book3:load-balancing
  - book3:redundancy-replication
  - book3:distributed-characteristics
conflicts:
  - load-balancing-vs-sticky-state
  - premature-optimization-vs-latent-scale-risk
validation:
  - unhealthy nodes stop receiving traffic
  - a backend or balancer failure has a known user-facing and operational outcome
```

## Card: decouple-slow-or-spiky-work-with-queues

```yaml
id: decouple-slow-or-spiky-work-with-queues
name: Use queues for slow, spiky, or fanout work with explicit delivery semantics
category: api-boundaries
use_when:
  - request handlers perform slow processing that can finish later
  - clients or services need notifications, fanout, or offline delivery
  - traffic spikes should be absorbed without overloading downstream services
avoid_when:
  - callers need an immediate committed result before proceeding
  - the workflow cannot tolerate duplicate, delayed, or reordered work and no safeguards exist
required_context:
  - producer and consumer contract
  - delivery guarantee and acknowledgement behavior
  - ordering requirements
  - retry and dead-letter policy
  - idempotency key or duplicate-handling plan
  - queue depth and slow-consumer observability
move: Insert a queue only when the async boundary names what can happen later, twice, out of order, or not at all.
recipe:
  - split the synchronous response from background work
  - define request, response, or per-subscriber queues where needed
  - make consumers idempotent before enabling retries
  - decide what happens when the queue grows or a consumer is offline
  - expose queue depth, age, failures, and retry counts
tradeoffs:
  - queues improve loose coupling, burst handling, and offline delivery
  - they add eventual consistency, duplicate handling, and operational state
source_anchors:
  - book3:message-queues
  - book3:system-design-process
conflicts:
  - async-decoupling-vs-synchronous-simplicity
  - preserve-specific-error-meaning-vs-hide-internals
validation:
  - duplicate and retry cases are safe
  - queue backlog and failed messages are visible
```

## Card: choose-realtime-transport-by-direction-and-cost

```yaml
id: choose-realtime-transport-by-direction-and-cost
name: Match realtime transport to update direction, frequency, and connection cost
category: api-boundaries
use_when:
  - code uses polling, long-polling, WebSockets, or SSE for updates
  - a realtime feature has unclear latency, bidirectionality, or client-count assumptions
  - connection retries, timeouts, or empty responses are causing load or complexity
avoid_when:
  - ordinary request/response is sufficient
  - the feature can tolerate coarse refreshes and simpler polling is cheaper to operate
required_context:
  - update direction
  - event frequency and latency tolerance
  - number of connected clients
  - proxy and infrastructure support
  - timeout, reconnect, and fallback behavior
  - authentication and resource cleanup
move: Choose the simplest transport that matches the communication shape and operational cost.
recipe:
  - use polling for low-frequency updates where empty responses are acceptable
  - use long-polling for sporadic server events over ordinary HTTP
  - use SSE for server-to-client event streams
  - use WebSockets for bidirectional low-overhead conversation
  - test reconnects, timeouts, authorization expiry, and slow clients
tradeoffs:
  - persistent transports reduce update latency and repeated HTTP overhead
  - they require connection lifecycle, capacity, and fallback handling
source_anchors:
  - book3:realtime-transports
  - book3:load-balancing
conflicts:
  - persistent-connection-vs-polling-simplicity
  - load-balancing-vs-sticky-state
validation:
  - the selected transport matches the data direction and latency need
  - reconnect and timeout behavior is tested or manually verified
```
