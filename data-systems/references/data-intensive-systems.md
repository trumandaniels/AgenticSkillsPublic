# Data-Intensive Systems Doctrine

Source: Martin Kleppmann, *Designing Data-Intensive Applications*, local source `C:\Users\Truman\Documents\Programming\AgenticKnowledge\Experts\Data\designing-data-intensive-applications.md`. This file is a compact doctrine layer; do not reproduce long source passages.

## Designer Stance

Modern data applications are composite systems. A single user-facing feature may combine operational databases, caches, search indexes, message brokers, stream processors, batch jobs, warehouses, and application code that keeps those components aligned. Treat the application boundary as part of the data system, because it is often where consistency, freshness, retries, cache invalidation, and derived-state guarantees are actually implemented.

Use three global design goals as a first pass:

- Reliability: the system should continue doing the correct thing despite hardware faults, software faults, operator mistakes, bad inputs, overload, and partial failures.
- Scalability: the system should preserve acceptable performance as load grows, but only for named load parameters and access patterns.
- Maintainability: future operators and engineers should be able to understand, evolve, observe, and repair the system without hidden coupling or heroic knowledge.

## Workload And Performance Checklist

Do not call a design scalable until the load model is explicit:

- Define load parameters: reads per second, writes per second, data volume, hot keys, fan-out, fan-in, concurrency, tenant skew, query complexity, and freshness expectations.
- Define performance targets: median, high percentile, and tail latency; throughput; queueing delay; batch completion time; replay/backfill time; and user-visible staleness.
- Measure from the client perspective when possible, because queueing, retries, browser/mobile behavior, and load balancers affect observed latency.
- Distinguish read-heavy, write-heavy, mixed OLTP, and analytical workloads. Storage and indexing choices that help one frequently hurt another.
- Avoid generic scale claims. A design that scales for append-heavy event ingestion may be poor for ad hoc analytics or cross-tenant graph traversal.

## Data Model Doctrine

Data models shape the way engineers think about the problem. Pick the model that matches the relationship shape and change pressure, not the current storage fashion.

- Relational models fit shared entities, many-to-one and many-to-many relationships, joins, constraints, and durable integration boundaries.
- Document models fit mostly self-contained aggregate trees where reads commonly need the whole document and relationships outside the document are limited.
- Graph models fit domains where anything may relate to anything, relationship traversal is central, or entity types and relationship types evolve rapidly.
- Denormalization can reduce read-time joins but creates derived data that must be refreshed, reconciled, and repaired.
- Use stable identifiers for shared concepts. Repeating names or mutable labels across records is a long-term integration and localization trap.
- Polyglot persistence is valid when access patterns materially differ, but the design must name the canonical owner and propagation contract for each fact.

## Storage And Retrieval Doctrine

Every index is a trade: faster reads for slower writes, more storage, and more operational state. Add indexes from query evidence, not hope.

- OLTP systems typically serve many small, selective requests and care about seek latency, index maintenance, transactions, and predictable tail behavior.
- Analytical systems typically scan many rows/columns over fewer large queries and care about bandwidth, columnar layouts, compression, predicate pushdown, and partition pruning.
- B-tree-style storage is a good default for mutable indexed records and range access. Log-structured storage favors high write throughput and sequential IO but adds compaction and read-amplification concerns.
- Hash indexes fit exact-key lookups and can be extremely fast, but do not provide range scans.
- Columnar storage, compression, sort order, and materialized aggregates are central for analytics; do not force operational row stores to act as warehouses under heavy reporting load.
- Caches, search indexes, and materialized views are derived systems. Design invalidation, rebuild, lag monitoring, and source-of-truth fallback explicitly.

## Architecture Output Pattern

For a DDIA-grounded architecture answer, include:

- canonical systems of record and derived stores;
- read/write paths and freshness expectations;
- load parameters and high-percentile latency targets;
- indexes and storage choices tied to actual queries;
- failure modes for propagation, backfill, retries, and operator mistakes;
- validation gates: load tests, chaos/failure drills, data-quality checks, reconciliation, restore/replay tests, and observability.
