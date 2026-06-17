# Metadata Map

Use this reference when the task is about a metadata repository, enterprise metamodel, glossary/catalog design, metadata governance, or traceability across business and technical views. Distillations here come from David C. Hay's *Data Model Patterns: A Metadata Map* and should be used as compact doctrine, not as copied source text.

## Core Thesis

Metadata is not only "data about data." For architecture work, treat it as the data that describes the structure and operation of the organization's use of information and the systems that manage that information. It covers business language, data structures, processes, people, locations, timing/events, motivations/rules, implementation designs, and production inventories.

The useful dividing line is audience and level of abstraction:

- Business metadata: terms, concepts, definitions, fact types, rules, stewardship, responsibilities, business processes, events, and organizational meaning.
- Technical metadata: data models, tables, columns, program modules, interfaces, constraints, deployed databases, programs, network components, users, events, logs, and enforcement mechanisms.
- Meta-metadata: the metamodel that describes the metadata repository itself.

Do not collapse the map to only database tables and columns. A table/column catalog is one cell in a larger architecture map.

## Architecture Framework

Organize metadata with a row/column matrix inspired by enterprise architecture frameworks.

Rows:

- Planner/scope: enterprise direction, boundaries, lists of major things, functions, locations, people, schedules, and mission/vision.
- Business owner/model of business: business language, divergent data models, business process models, logistics, organization charts, state transitions, strategies, policies, and rules.
- Architect/model of fundamental concepts: technology-independent models such as convergent entity-relationship models, essential process flows, roles, entity life histories, and business-rule models.
- Designer/technology model: database design, system/program design, hardware/software distribution, user interface/security, event processing, and implementable rule design.
- Builder/detailed representation: physical storage, program specifications, network protocols, screen/security code, timing definitions, and rule logic.
- Functioning system/inventory: deployed databases, program inventory, communications facilities, trained users, actual events/logs, and enforced rules.

Columns:

- Data: what the enterprise cares about and how information about it is represented.
- Activities: how the enterprise carries out work.
- Locations: where operations, systems, and communications occur.
- People/organizations: who performs, owns, stewards, secures, and uses the metadata and systems.
- Time/events: when work is triggered and how event types drive processes.
- Motivation: why the enterprise acts, including ends, means, policies, rules, constraints, and quality.

## Abstraction Discipline

Use rows to prevent category mistakes:

- A business glossary term is not the same artifact as an entity class, table, or column.
- A business process is not the same artifact as an essential system process, program module, or deployed job.
- A business event type is not the same artifact as a program event, cron trigger, queue message, or log row.
- A business rule is not automatically a database constraint; it may map to a data model constraint, programmed validation, operational control, or data-quality measurement.

When designing a metadata repository, state which rows and columns are in scope. If scope spans multiple rows, define the mapping entity that connects them, such as concept-to-entity, entity-to-table, process-to-program, role-to-access-control, rule-to-constraint, or event-type-to-program-trigger.

## Repository Boundary

Include metadata when it helps development, maintenance, operations, governance, warehouse/catalog use, lineage, or quality management. Exclude ordinary business instance data unless that data acts as metadata, such as reference data constraining valid values.

Reference data can sit on the boundary. Product type, account status, geography code sets, and other controlled vocabularies may be business data while also constraining attributes and therefore functioning as metadata. Name the owner and lifecycle explicitly.

## Stewardship

Reliable metadata needs responsible parties:

- concept or term owner,
- symbol/glossary steward,
- data model steward,
- process/rule owner,
- quality standard owner,
- implementation owner,
- production-system owner.

Metadata without stewardship decays into an inventory snapshot. Ask who can define, approve, change, and retire each artifact.

## Output Pattern

For metadata designs, return:

- the row/column scope,
- core metadata objects,
- mapping relationships between business and technical views,
- stewardship and approval responsibilities,
- lineage from concept/rule/process/event to implementation,
- data-quality and freshness controls for the metadata repository itself,
- exclusions and deferred cells.
