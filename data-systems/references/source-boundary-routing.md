# Source Boundary Routing

Use this reference when multiple book doctrines apply, when an architecture answer spans conceptual, application, relational, distributed, and storage layers, or when a design starts treating one layer's artifact as truth for another layer.

## Layer Ownership

| Layer or question | Governing source | Use it for | Boundary |
| --- | --- | --- | --- |
| Conceptual enterprise meaning | *Enterprise Model Patterns* | architect-view entity classes, relationships, party/asset/activity/location/time/information/accounting patterns, stable business semantics | Do not let current tables, screens, APIs, queues, or vendor products define the conceptual model. Only model things significant to the enterprise. |
| Metadata, stewardship, traceability | *Data Model Patterns: A Metadata Map* | business vs technical metadata, architecture-framework row/column coverage, glossary, rules, lineage, owners, reference-data governance | Do not reduce metadata to a table/column catalog. Reference data can be business data and metadata when it constrains legal values. |
| Enterprise application structure | *Patterns of Enterprise Application Architecture* | presentation/domain/data-source layering, domain logic pattern, Service Layer, persistence mapping, Repository, Unit of Work, session state, offline concurrency, remote facades, DTOs | Do not distribute fine-grained domain objects. Keep domain collaboration local and expose coarse interfaces at unavoidable remote boundaries. |
| Data-intensive system composition | *Designing Data-Intensive Applications* | reliability/scalability/maintainability, workload parameters, source-of-record vs derived data, schema evolution, CDC, streams, replication, partitioning, transactions, consistency, rebuild/replay | Do not confuse a tool type with ownership. A database, cache, index, warehouse, or stream can be source-of-record or derived depending on how the application uses it. |
| Practical relational design | *Beginning Database Design* | requirements analysis, ERDs, tables, fields, keys, constraints, datatypes, normal forms, practical denormalization, OLTP vs warehouse schemas, indexing and physical design | Do not pursue mathematical purity past usefulness. Stop normalization where integrity gains are concrete and denormalize only with source-of-truth and reconciliation clarity. |
| Storage and distributed internals | *Database Internals* | row/column layout, pages, B-Trees, LSM/SSTables, Bloom filters, WAL/recovery, buffering, amplification, failure detectors, leader election, anti-entropy, distributed commit, consensus | Do not overfit product internals unless a bottleneck, durability question, or failure mode depends on them. Compare systems by workload simulation and operating evidence, not labels or popularity. |

## Conflict Rules

- Conceptual truth vs physical shape: preserve the conceptual source-of-truth model; map physical schemas, derived views, and indexes back to it.
- Domain model vs remote distribution: keep rich object collaboration in-process; use Remote Facade and DTOs for coarse remote use cases.
- Normalization vs read performance: normalize the source of record enough to prevent known anomalies; denormalize caches, warehouses, materialized views, and search indexes as derived data with refresh and reconciliation plans.
- Metadata vs operational data: if a value describes, constrains, classifies, governs, or traces other data or processes, model its metadata role and assign stewardship even if it is also operational data.
- Strong consistency vs availability or latency: name the invariant and user-visible guarantee before choosing serializability, linearizability, consensus, sagas, idempotency, or eventual reconciliation.
- Storage-engine choice vs product label: reason from access patterns, read/write/space amplification, page/cache behavior, WAL/recovery semantics, compaction cost, and operational evidence.
- User interview specifics vs reusable abstraction: collect concrete examples, then abstract only where it simplifies without erasing genuine special cases.
- Warehouse/reporting needs vs OLTP needs: keep transactional ownership separate from analytical grains, summaries, history, and star/snowflake structures unless the scale is intentionally small enough for one model.

## Evidence Package

When answering a cross-layer design, include:

- The primary governing layer and any secondary layers.
- The chosen decision node, usually `decision/source-boundary-routing.json` plus one specialized decision tree.
- Source anchors from the relevant manifests, not every book.
- A boundary statement for each artifact: conceptual model, application/domain model, relational schema, system of record, derived store, metadata repository, and storage/distribution mechanism.
- Validation checks that fit the layer: semantic review, rule/stewardship review, unit/integration tests, data-quality probes, reconciliation, replay/rebuild drill, workload benchmark, or crash/failover evidence.

## Output Checklist

- State which layer each recommendation belongs to.
- Name what must not be inferred from that layer.
- State owners for durable facts and derived projections.
- Identify invariants and where they are enforced.
- Give a migration or feedback path when the design may need to move between patterns later.
