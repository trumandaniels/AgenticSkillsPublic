# Dimensional Database Design

Use this reference for data warehouse database modeling: facts, dimensions, star schemas, snowflakes, grain, retention, surrogate keys, and separation from OLTP systems.

## Why Warehouse Models Differ

OLTP and warehouse workloads have opposing needs.

- OLTP: high concurrency, small transactions, frequent updates, fast response for many users, normalized integrity.
- Warehouse: few analytical users, huge reads, historical data, batch loads, ad hoc reporting, long-running queries, denormalized access.

A standard normalized relational OLTP model is too granular for large warehouse queries. Warehouses need fewer joins and simpler structures because fact tables can contain millions, billions, or more rows.

## Core Structures

- Fact table: historical transaction/measurement records. Often very large and append-heavy.
- Dimension table: descriptive/static context for facts, such as time, customer, product, location, seller, category, or shipper.
- Star schema: one fact table directly connected to a single layer of dimensions.
- Snowflake schema: normalized dimensions split into additional levels.
- Data mart: a smaller subject-area warehouse, often one or a few fact tables with shared dimensions.

Prefer star schemas for end-user reporting and query speed unless snowflaking is justified by maintenance, hierarchy reuse, or dimension size.

## Grain And Retention

Define the fact grain before table design:

- one row per transaction,
- one row per line item,
- one row per daily/monthly summary,
- one row per event,
- one row per state snapshot.

Lowest-grain historical detail is safest for unknown future analytics, but costs storage, load time, and management effort. If summarizing or deleting detail, define irreversible-loss risk, retention policy, and whether materialized summaries can be rebuilt.

## Surrogate Keys

Surrogate keys are especially useful in warehouses because source systems may identify the same business object differently. Use warehouse surrogate keys to unify cross-source identities while preserving source natural keys for lineage and audit.

## Referential Integrity

Referential integrity still matters in warehouses, but enforcement may be lighter or staged:

- enforce/validate during loads,
- keep primary/foreign-key structure for join clarity and optimizer help,
- allow nullable/unknown dimension references only with explicit unknown members or quality rules,
- monitor orphaned facts and dimension drift.

## Modeling Steps

1. Identify business processes or analytical subject areas.
2. Choose fact tables from historical transactions or measurements.
3. Define grain.
4. Identify dimensions that describe facts.
5. Decide star vs snowflake based on query simplicity, hierarchy maintenance, and performance.
6. Choose surrogate/natural key mapping.
7. Decide retention and summarization strategy.
8. Add indexes, materialized views, partitions, and data marts based on workload.

## Failure Modes

- Using OLTP-normalized schemas directly for reporting.
- Snowflaking dimensions so deeply that analysts face large joins.
- Fact grain is unclear or mixed within one fact table.
- Deleting/summarizing detail before future reporting requirements are understood.
- No identity strategy for cross-source entities.
- Warehouse loads update many existing rows when append or versioning would be cheaper.
