# Decision Trees

Load the relevant `decision/*.json` file when a request hinges on a recurring architecture choice. Treat these trees as guidance, not a rules engine; reason from constraints and cite assumptions.

## Tree Schema

Each decision file should use:

- `decision_id`: stable short ID.
- `purpose`: what choice the tree supports.
- `required_context`: facts that can change the recommendation.
- `ask_if_missing`: high-impact unknowns that should trigger questions.
- `assume_if_low_risk`: acceptable default assumptions.
- `branches`: branch criteria and recommended direction.
- `failure_modes`: common ways the choice fails.
- `output_checks`: requirements for the final answer.

## Starter Routing

- Use `decision/conceptual-modeling.json` when the request is about conceptual enterprise data modeling, abstraction level, business semantics, or architect-view models.
- Use `decision/enterprise-pattern-selection.json` when selecting Party, Geographic Location, Asset, Activity, Information Resource, Accounting, or domain adaptation patterns.
- Use `decision/data-model-choice.json` when selecting relational, document, graph, event, vector, columnar, or hybrid modeling.
- Use `decision/storage-selection.json` when selecting operational stores, analytical stores, streams, object stores, indexes, or caches.
- Use `decision/computation-mode.json` when deciding request-time, batch, streaming, materialized view, CDC, or hybrid processing.
- Use `decision/enterprise-layering.json` when choosing presentation/domain/data-source boundaries, service layer placement, and local vs remote layer deployment.
- Use `decision/domain-logic-pattern.json` when choosing Transaction Script, Domain Model, Table Module, Service Layer, or a refactoring path between them.
- Use `decision/persistence-mapping-pattern.json` when choosing Table Data Gateway, Row Data Gateway, Active Record, Data Mapper, Repository, Unit of Work, Identity Map, Lazy Load, or O/R mapping tooling.
- Use `decision/remote-boundary-pattern.json` when deciding whether to distribute components, use Remote Facade/DTO, keep calls local, or prefer asynchronous integration.
- Use `decision/session-offline-concurrency.json` when choosing client/server/database session state, optimistic/pessimistic offline locks, coarse-grained locks, or implicit locking.
- Use `decision/derived-data-strategy.json` when designing caches, search indexes, materialized views, CDC, event sourcing, batch/stream pipelines, or serving tables.
- Use `decision/schema-evolution-encoding.json` when changing schemas, durable encodings, API contracts, event formats, or rolling-upgrade plans.
- Use `decision/transaction-consistency.json` when choosing isolation levels, transaction boundaries, serializability, sagas, idempotency, or consensus-backed coordination.
- Use `decision/partitioning-strategy.json` when choosing shard keys, partitioning method, secondary-index strategy, rebalancing, or routing.
- Use `decision/replication-strategy.json` when choosing single-leader, multi-leader, leaderless, synchronous/asynchronous replication, or user-visible read guarantees.

## Branching Rules

Ask before branching if the answer depends on compliance, hard latency, strict consistency, deletion requirements, or irreversible migration cost.

Assume and proceed when only rough scale, exact vendor, or future optional integrations are missing; mark the assumption clearly.

## Evidence Package Pattern

When source indexes exist, return:

- One matched decision node.
- One or two concise doctrine points.
- Two to five source anchors.
- At most one compatible example.

Do not let an example overrule branch criteria or source-backed doctrine.
