# Relational Database Design

Use this reference when turning requirements into a practical relational database model: ERDs, tables, fields, relationships, datatypes, DDL, and implementation/tuning steps. Distilled from Gavin Powell's *Beginning Database Design*.

## Design Objective

Design the database before building it. The database model underpins applications, SQL, reporting, maintenance, and future change. Late table-structure changes are expensive because applications and queries depend on the model.

The design goal is not mathematical perfection; it is a structure that satisfies business operations, preserves integrity, supports expected queries, performs acceptably, and remains understandable to developers and users.

## Workflow

Use this practical sequence:

1. Requirements analysis: discover what the business does, what information is needed, who uses it, expected outputs, special cases, scale, performance, and existing systems.
2. Conceptual design: draw ERDs, identify tables/entities, fields/attributes, and relationships. Keep technical details light enough to preserve analytical clarity.
3. Logical design: turn the ERD into DDL-oriented table definitions, constraints, keys, and relationship structures. Check generated DDL before vendor-specific execution.
4. Physical design: account for storage, datatypes, large objects, partitions, indexes, table organization, materialized copies, and vendor features.
5. Tuning: revisit indexes, normalization, denormalization, constraints, security, materialized views, clustering, and physical layout using actual or expected workload.

These steps are iterative. Do not delay all performance thinking until after implementation, because table structure controls SQL shape.

## Analysis Guidance

Analysis is about what is required, not how to implement it. Capture:

- company objectives and operational subject areas,
- core business processes and paper/system trails,
- users, roles, managers, operational employees, technical staff, and their different perspectives,
- business rules that imply tables, relationships, constraints, and validation,
- existing databases, spreadsheets, paper systems, and application behavior,
- expected workload: OLTP, reporting, warehouse, or hybrid,
- performance and scalability requirements,
- budget, staffing, training, maintenance, and timelines.

Do not rely only on technical staff. End users know what the system must do; managers provide scope and objectives; operational employees provide detail; technical staff expose current constraints, defects, and workarounds.

## Modeling Doctrine

- Each table should usually represent one subject/topic.
- Build for application and user needs; avoid designs only the modeler can understand.
- Use abstraction to reduce special-case table sprawl, but preserve genuine special cases when abstraction would make the model unusable.
- Treat existing paper forms and spreadsheets as evidence, not as canonical schema. Extract the entities, fields, relationships, defaults, and rules they imply.
- Rewrites should analyze why the old system is inadequate before copying old structures.
- Generic or industry-standard models can help as references, but may contain irrelevant tables or miss company-specific requirements.

## OLTP, Warehouse, Hybrid

Design structure from workload:

- OLTP: many concurrent users, small transactions, fast single-record or short-list access, high integrity needs, careful indexing, limited ad hoc querying.
- Data warehouse: few users, huge reads, batch loads, historical data, ad hoc analysis, denormalized dimensional structures, summaries/materialized views.
- Hybrid: cost-effective for smaller environments, but risks mixing incompatible concurrency and throughput needs.

Operational OLTP databases and analytical warehouses often need separation because they use hardware, locking, memory, I/O, normalization, and query patterns differently.

## Output Pattern

For practical database-design answers, return:

- workload classification,
- analysis assumptions and open questions,
- core tables/entities and relationships,
- key and referential-integrity choices,
- normalization/denormalization stance,
- datatype and constraint notes,
- index/physical-design notes,
- migration/construction/implementation steps,
- validation queries and data-quality checks.
