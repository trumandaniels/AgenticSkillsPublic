# Normalization And Denormalization

Use this reference when deciding how far to normalize a relational schema, how to detect anomalies and dependencies, or when to denormalize for performance/usability.

## Why Normalize

Normalization organizes data, removes unnecessary duplication, reduces update/insert/delete anomalies, and clarifies dependencies. It is a progressive refinement process: each normal form builds on the previous one.

Common anomaly targets:

- Insert anomaly: child/detail data appears without the required parent/master fact.
- Delete anomaly: deleting a parent leaves orphaned child records, unless cascading or cleanup is intentional.
- Update anomaly: the same fact must be changed in multiple places and can become inconsistent.

Dependency vocabulary:

- Functional dependency: one value determines another.
- Determinant: the value that determines another value.
- Full functional dependency: non-key values depend on the whole key, not part of a composite key.
- Transitive dependency: a value depends indirectly through another non-key value.
- Multivalued dependency: a key has multiple independent value sets.
- Cyclic dependency: dependencies form a loop.
- Candidate key: a field or field combination that could uniquely identify a row.

## Normal Form Routing

- 1NF: eliminate repeating groups and make rows uniquely identifiable.
- 2NF: remove partial dependencies on part of a composite key; separate static/reference data from transactional detail.
- 3NF: remove transitive dependencies; non-key facts should not determine other non-key facts.
- BCNF: every determinant is a candidate key; useful in edge cases, often too granular commercially.
- 4NF: eliminate multiple independent multivalued dependencies.
- 5NF: eliminate cyclic/join dependencies.
- DKNF: idealized domain/key completeness; treat mostly as a conceptual benchmark.

In most commercial OLTP systems, 3NF is a common stopping point. Beyond 3NF can create many tables, complex joins, and poor performance. Use deeper normal forms only when the integrity benefit is concrete and the workload can tolerate the complexity.

## Stop Criteria

Stop normalizing when:

- additional tables mainly satisfy mathematical purity,
- query joins become hard to write or tune,
- the table split does not match application or user needs,
- values are stable/static enough to remain together,
- application code or constraints can manage the edge condition more simply,
- the workload is analytical/warehouse-oriented and favors denormalized shape.

Do not denormalize below 1NF for normal relational OLTP design. Repeating groups and list-in-field structures usually harm integrity and queryability.

## Denormalization Doctrine

Denormalization reverses some normalization to improve usability, performance, or analytical access. It is not a formal method; it depends on workload, query patterns, application knowledge, and production evidence.

Common denormalization moves:

- keep nullable or rarely used fields in a table when variable-length storage makes split tables pointless,
- avoid separating every candidate key into separate tables,
- collapse over-normalized static reference tables,
- store calculated values when recomputation is too expensive and reconciliation is defined,
- collapse snowflake dimensions into star dimensions for warehouse reporting,
- retain dimensions/facts at a grain that supports expected analysis.

Risks:

- duplicate facts drift,
- update logic becomes more complex,
- constraints move from schema to application/procedure,
- denormalized fields become stale,
- later requirements need missing detail.

## OLTP vs Warehouse

OLTP schemas often benefit from normalization through 3NF because concurrent small updates need integrity. Warehouses usually favor denormalized dimensional structures because large joins over granular normalized tables are too slow and hard for analysts.

When in doubt, separate systems of record from derived analytical structures. Keep the OLTP source correct; build denormalized serving/warehouse structures with explicit refresh, lineage, and reconciliation.

## Output Checks

- Name the anomalies/dependencies being removed.
- State target normal form and why.
- State why deeper normal forms are rejected or accepted.
- If denormalizing, state duplicated data, source of truth, refresh/update path, and stale-value detection.
- Check join count and query complexity against workload.
