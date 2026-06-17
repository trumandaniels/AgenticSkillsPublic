# Keys, Indexes, And Physical Design

Use this reference when choosing primary keys, foreign keys, surrogate keys, referential integrity, datatypes, indexes, views, materialized views, partitioning, clustering, and hardware-aware structures.

## Keys And Referential Integrity

- Primary key: unique row identifier.
- Foreign key: value in a child/detail table that references a parent/master primary key.
- Unique key: enforces uniqueness outside the primary key; not itself part of referential integrity.
- Surrogate key: artificial key, often integer/autocounter, used for stable efficient identity and cross-source integration.

Foreign keys usually need supporting indexes in high-concurrency OLTP systems. Many engines do not automatically create them. Missing foreign-key indexes can cause full scans and locking pressure during referential checks.

Use cascade actions deliberately. They solve some delete/update anomalies but can hide large changes behind one operation.

## Datatypes And Field Design

Choose datatypes to match business meaning, validation, storage, indexing, and query needs:

- prefer compact integer keys for primary/foreign keys and indexes,
- use fixed or code values only when they are genuinely controlled,
- split composite fields when parts are queried, validated, or independently updated,
- keep free text, large objects, and binary data out of hot transactional paths when possible,
- capture nullable/state-dependent requirements explicitly rather than defaulting every field to nullable.

Field refinement includes names, datatypes, defaults, formats, masks, check constraints, unique constraints, and whether logic belongs in schema, stored code, application code, or a quality check.

## Index Doctrine

Indexes speed reads by adding storage and write-maintenance cost. Indexes are not free.

Create indexes when:

- a large table is frequently filtered on a small subset of rows,
- joins use foreign keys under concurrency,
- sort/group/report patterns are stable and expensive,
- a uniqueness rule must be enforced,
- warehouse/reporting structures are read-heavy.

Avoid or defer indexes when:

- the table is tiny and table scans are cheaper,
- a large percentage of rows is usually read,
- the index is a large composite close to table size,
- values are mostly NULL or low selectivity,
- write-heavy OLTP tables already carry many indexes,
- report requirements are speculative.

Composite indexes are most useful when their leading columns match actual filters/sorts. Prefer fewer, smaller indexes. Periodically remove redundant or unused indexes.

## Workload-Specific Indexing

OLTP:

- index primary keys and important foreign keys,
- keep alternate indexes tightly controlled,
- avoid over-indexing write-heavy tables,
- prefer simple BTree-style indexes for changing data,
- monitor lock/contention and query plans after release.

Warehouse/reporting:

- use indexes, materialized views, clustering, partitions, and summaries when read-heavy workloads justify them,
- consider bitmap/read-only-style indexes only where updates are controlled,
- align partitions and summaries with load and query patterns,
- prefer star-schema simplicity before adding complex index structures.

## Views And Materialized Views

Views hide complexity but do not automatically improve performance. Use them for interface stability and query simplification.

Materialized views physically copy or summarize data. Use them when expensive joins or aggregations are frequent, especially in warehouses. Define refresh cadence, source of truth, query-rewrite expectations, and stale-data tolerance.

## Physical And Hardware-Aware Design

Consider partitioning, clustering, index-organized tables, RAID/storage layout, standby databases, replication, and grids/clustering only after workload and operational goals are clear.

- Partition for pruning, manageability, retention, and bulk loading, not as decoration.
- Clustering/index-organized structures can speed narrow access but may be brittle under heavy change.
- Standby/replication support availability and distribution; they do not replace schema correctness.
- Hardware can mask poor design only temporarily.

## Output Checks

- State read/write ratio and workload type.
- Name key choices and referential-integrity enforcement.
- Explain every proposed alternate index by query/filter/sort/use case.
- State write overhead and maintenance risk.
- Include stale-data and refresh rules for materialized structures.
- Prefer measured evidence before production index sprawl.
