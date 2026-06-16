# Derived Data Doctrine

Source: Martin Kleppmann, *Designing Data-Intensive Applications*, Part III.

## Systems Of Record And Derived Data

Separate authoritative facts from derived views.

- A system of record holds the canonical version of a fact. New authoritative facts are first written there.
- Derived data is computed from other data: caches, search indexes, denormalized views, recommendation features, materialized views, analytics marts, and serving tables.
- Derived data is redundant but often essential for read performance, search, analytics, and product experience.
- A derived system must have a rebuild/replay path or a reconciliation process. If it cannot be recreated or checked from source, it has quietly become a source of record.

## Batch Processing

Batch jobs operate on bounded input and produce derived output.

- Immutable inputs and deterministic outputs make retry and recovery easier.
- Partitioning brings related records together, often by sorting, hashing, or grouping on keys.
- Fault tolerance comes from retrying failed tasks and exposing only successful output.
- Batch joins include sort-merge joins, broadcast hash joins, and partitioned hash joins; pick based on data size, partitioning, and skew.
- Batch is a strong fit for backfills, historical recomputation, analytics, search-index builds, feature generation, and reconciliation.
- Include completion SLOs, late-arriving data policy, idempotent output writes, and rerun semantics.

## Stream Processing

Streams are unbounded event sequences processed continually.

- Events are immutable records of something that happened and are commonly grouped into topics or streams.
- Messaging systems differ on overload behavior: drop, buffer, or backpressure. Name the choice because it determines failure semantics.
- Durable partitioned logs support replay, multiple consumers, CDC, and derived-view maintenance.
- Stream-table joins use a changelog to maintain local state for enrichment.
- Table-table joins combine changelog streams to maintain materialized views.
- Stream-stream joins require event-time/window rules, late-event handling, and state-retention limits.
- Distinguish event time from processing time. Windows need watermarks, lateness policy, and correction behavior.

## CDC, Event Sourcing, And Materialized Views

- Change data capture turns database writes into an event stream for downstream indexes, caches, warehouses, and services.
- Event sourcing stores domain events as the canonical record and derives current state from replay. Use it only when event history is a real domain asset and replay/versioning complexity is acceptable.
- Materialized views are derived state. They need source ownership, propagation mechanism, lag monitoring, rebuild, and reconciliation.
- Exactly-once processing is usually achieved by a combination of deterministic processing, checkpointing, transactions, idempotent writes, deduplication keys, or atomic output commits. State which layer provides the guarantee.

## Derived Data Output Checks

For any derived-data architecture, state:

- canonical source for each fact;
- derivation path and freshness target;
- lag, loss, duplication, and out-of-order behavior;
- replay/backfill/rebuild plan;
- reconciliation checks against the source of record;
- failure behavior when derived state is missing, stale, corrupt, or partially rebuilt.
