# Architecture Workflow

## Minimum Context Checklist

Collect or infer the smallest useful set of constraints before recommending architecture:

- Product goal and user-facing workflow.
- Core entities and relationships.
- Read paths, write paths, and expected contention.
- Latency, freshness, throughput, and availability targets.
- Data volume, growth, retention, and deletion needs.
- Consistency, transaction, and audit requirements.
- Privacy, compliance, tenancy, and access-control constraints.
- Team maturity, operational budget, and existing platform commitments.

Ask when an unknown can change the recommended storage, consistency, or propagation model. Otherwise state the assumption and continue.

## Design Procedure

1. Define the system boundary and primary data owners.
2. Identify canonical records versus derived views, caches, indexes, and exports.
3. Pick the data model before the product names of databases.
4. Map writes first, including idempotency, retries, conflict handling, and rollback.
5. Map reads second, including query shapes, freshness, and derived-state maintenance.
6. Choose computation modes: request-time, batch, streaming, materialized view, or CDC.
7. Add observability and data-quality checks at every boundary crossing.
8. Review failure modes before finalizing tools.

## Recommended Output Shape

Use this structure for design answers unless the user requested another format:

1. Context and assumptions.
2. Recommended architecture.
3. Data model and ownership.
4. Write path and transaction/consistency strategy.
5. Read path and derived data.
6. Operational plan: observability, data quality, backfill, recovery.
7. Alternatives considered.
8. Risks, open questions, and next steps.

## Review Lens

Treat a design as incomplete until it names what happens when:

- The same event is delivered twice.
- A downstream consumer is offline.
- Schema changes are deployed gradually.
- Backfills and live writes overlap.
- A cache/index/search store is stale.
- A tenant or user requests deletion/export.
- Metrics say the data is fresh but semantically wrong.
