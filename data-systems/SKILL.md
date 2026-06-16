---
name: data-systems
description: Design data applications, data platforms, distributed data systems, enterprise application architectures, conceptual enterprise data models, and system architectures with source-governed reasoning, explicit tradeoffs, and validation gates. Use when Codex needs to design or critique data-intensive applications, enterprise layering, domain logic patterns, service layers, object-relational mapping, repositories, gateways, units of work, identity maps, lazy loading, remote facades, DTOs, session state, offline concurrency, storage engines, pipelines, analytics layers, search/RAG/memory systems, replication, partitioning, transactions, consistency, consensus, schema evolution, CDC, event streaming, derived data, migrations/backfills, observability/data-quality plans, ADRs, enterprise model patterns, parties/assets/activities/geography/time models, metadata, information resources, accounting links, contracts, facilities, manufacturing, laboratory, banking, oil-field, highway, or other domain data models.
---

# Data Systems

## Overview

Use this skill to turn vague data-system requests into decision-quality architecture: clarify workload constraints, choose the right data model and application pattern, design flows and boundaries, state assumptions, and verify failure modes. Prefer compact doctrine and decision resources over loading large source material into context.

## Core Workflow

1. Classify the task: new architecture, critique/review, migration/backfill, pipeline design, analytics layer, search/RAG/memory, observability, conceptual model, enterprise application structure, distributed-system tradeoff, or ADR.
2. Gather minimum context before choosing: users/actors, read/write patterns, latency, freshness, scale, consistency needs, domain-logic complexity, UI/API clients, transaction boundaries, compliance/privacy, failure tolerance, team maturity, budget, deployment constraints, and acceptable operational complexity.
3. Ask targeted questions only for high-impact unknowns. For low-impact unknowns, proceed with explicit assumptions.
4. Load the smallest relevant resources:
   - `references/architecture-workflow.md` for the general design procedure and output shape.
   - `references/enterprise-application-architecture.md` for Fowler/PoEAA doctrine on layers, domain logic, persistence mapping, distribution, concurrency, session state, and performance vocabulary.
   - `references/poeaa-pattern-catalog.md` for concise routing across enterprise application patterns such as Transaction Script, Domain Model, Table Module, Service Layer, Data Mapper, Unit of Work, Repository, Remote Facade, DTO, and session/offline lock patterns.
   - `references/data-intensive-systems.md` for reliability/scalability/maintainability, data models, storage engines, workload analysis, and composite data-system framing.
   - `references/distributed-data.md` for replication, partitioning, transactions, isolation anomalies, partial failures, clocks, consistency, and consensus boundaries.
   - `references/encoding-evolution.md` for schema evolution, wire/durable encodings, API compatibility, rolling upgrades, and message/dataflow interfaces.
   - `references/derived-data.md` for systems of record, derived data, batch, stream processing, CDC, event sourcing, materialized views, and exactly-once/idempotence design.
   - `references/enterprise-model-patterns.md` when the task asks for conceptual enterprise data modeling or domain model patterns.
   - `references/generic-enterprise-model.md` when modeling parties, locations, assets, activities, time, information resources, or accounting links.
   - `references/domain-patterns.md` when adapting the generic model to facilities, HR, contracts, manufacturing, labs, banking, oil fields, highways, or other industries.
   - `references/decision-trees.md` when choosing data model, storage, consistency, computation mode, enterprise app layering, domain logic, persistence mapping, remote boundary, session/concurrency, retrieval/memory, migration, conceptual-model scope, distributed-data strategy, derived-data strategy, or domain pattern.
   - `references/knowledge-boundaries.md` when adding or revising doctrine, examples, source indexes, or evals.
   - `references/validation.md` before finalizing recommendations or when reviewing an existing design.
5. Produce an architecture answer with: context summary, assumptions, recommended design, alternatives rejected, tradeoffs, failure modes, validation plan, and next implementation steps.
6. Separate doctrine from examples. Do not promote a prior example, anecdote, or generated output into a rule unless it is stable, reusable, and source-backed.
7. When citing source material from indexes, return evidence packages: one decision node, one or two doctrine snippets, anchored source evidence, and at most one compatible exemplar.

## Decision Discipline

Use decision trees for recurring high-impact branches:

- Enterprise application structure: presentation/domain/data source layers, service boundary, local vs remote calls, session state, and offline concurrency.
- Domain logic: Transaction Script, Domain Model, Table Module, Service Layer, and mixed/refactoring paths.
- Persistence mapping: Table Data Gateway, Row Data Gateway, Active Record, Data Mapper, Unit of Work, Identity Map, Lazy Load, Metadata Mapping, Query Object, Repository, and inheritance/relationship mapping.
- Conceptual enterprise model: architect's view, business semantics, abstraction level, pattern family, and technology independence.
- Data model: relational, document, graph, key-value, columnar, event-sourced, vector, or hybrid.
- Storage/platform: OLTP database, warehouse, lake/lakehouse, stream log, cache, search index, vector store, object store.
- Replication/consistency: single-leader, multi-leader, leaderless, synchronous/asynchronous replication, bounded staleness, read-your-writes, monotonic reads, causal consistency, linearizability, and consensus-backed coordination.
- Partitioning: key-range, hash, compound keys, secondary indexes, skew/hotspot mitigation, rebalancing, and routing.
- Transactions: invariant scope, isolation level, lost updates, write skew, phantom reads, serializability, idempotent workflows, sagas, outbox, and distributed transaction risk.
- Encoding/evolution: backward/forward compatibility, rolling upgrades, schema versioning, unknown fields, and message/API contracts.
- Computation and derived data: request-time, batch, streaming, materialized views, CDC, event sourcing, reverse ETL, rebuild/replay, reconciliation, and serving freshness.
- Search/RAG/memory: lexical, semantic, hybrid, reranking, graph links, curated doctrine, source-index retrieval.
- Migration/backfill: dual writes, shadow reads, replay, cutover, reconciliation, rollback.
- Observability/data quality: contracts, lineage, freshness, volume, distribution, schema, semantic checks.

When a decision tree exists, follow it before free-form recommendation. When it does not, use the core workflow and add a candidate decision node only if the branch is likely to recur.

## Output Standards

Prefer concrete architecture artifacts over generic advice:

- Name the main entities, data flows, interfaces, layers, and boundaries.
- State which system owns each durable record and which stores are derived.
- Identify invariants and how they are enforced.
- Explain how data changes propagate and how stale or failed propagation is detected.
- State expected consistency guarantees from the user's perspective, not only database product labels.
- State whether boundaries are in-process, inter-process, or remote, and adjust interface granularity accordingly.
- Include operational checks: metrics, logs, traces, data-quality probes, reconciliation, backup/restore, replay/rebuild, and runbooks.
- Mark unresolved risks separately from ordinary tradeoffs.

## Resource Map

- `references/architecture-workflow.md`: design process, context checklist, and output templates.
- `references/enterprise-application-architecture.md`: doctrine distilled from Martin Fowler et al.'s *Patterns of Enterprise Application Architecture*.
- `references/poeaa-pattern-catalog.md`: compact PoEAA pattern routing catalog.
- `references/data-intensive-systems.md`: doctrine distilled from Martin Kleppmann's *Designing Data-Intensive Applications* on foundational goals, data models, storage, and workload analysis.
- `references/distributed-data.md`: DDIA-derived replication, partitioning, transaction, partial-failure, consistency, and consensus doctrine.
- `references/encoding-evolution.md`: DDIA-derived encoding, schema evolution, API, and message-compatibility doctrine.
- `references/derived-data.md`: DDIA-derived systems-of-record, batch, stream, CDC, event-sourcing, materialized-view, and fault-tolerant processing doctrine.
- `references/enterprise-model-patterns.md`: doctrine distilled from David C. Hay's *Enterprise Model Patterns*.
- `references/generic-enterprise-model.md`: reusable Level 0 and Level 1 entity-pattern families.
- `references/domain-patterns.md`: Level 2 and Level 3 adaptation patterns for functions and industries.
- `references/decision-trees.md`: compact decision-tree schemas and starter branches.
- `references/knowledge-boundaries.md`: memory/doctrine governance and promotion rules.
- `references/validation.md`: review rubric, eval dimensions, and regression checks.
- `references/knowledge-policy.json`: machine-readable boundary classes for future ingestion.
- `decision/*.json`: starter decision nodes for reusable high-impact choices, including conceptual modeling, enterprise-pattern selection, enterprise app architecture, distributed data, encoding evolution, and derived data.
- `examples/*.jsonl`: compact exemplars and anti-exemplars tagged by applicability.
- `evals/*.jsonl`: starter representative tasks for forward-testing this skill.
- `indexes/source-manifest.schema.json`: starter schema for future immutable source manifests and anchored chunks.
- `indexes/enterprise-model-patterns.manifest.json`: anchored index for the enterprise-modeling source book used to fill this scaffold.
- `indexes/designing-data-intensive-applications.manifest.json`: anchored index for the data-intensive systems source book used to fill this scaffold.
- `indexes/patterns-of-enterprise-application-architecture.manifest.json`: anchored index for the enterprise application architecture source book used to fill this scaffold.
- `scripts/validate_resources.py`: validate JSON and JSONL resource files after edits.
