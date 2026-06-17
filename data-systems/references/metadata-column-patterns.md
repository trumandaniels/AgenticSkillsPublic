# Metadata Column Patterns

Use this reference to route metadata design across the six architecture columns from *Data Model Patterns: A Metadata Map*.

## Data Column

Business-owner view:

- Business concept: meaning recognized by a semantic community.
- Business term: a word or phrase in a language and context used to represent one concept.
- Symbol/signifier: term, phrase, word, graphic, or icon used in a context.
- Semantic community and speech community: the groups that share meaning and language.
- Ontology/taxonomy: vocabulary or classification managed by a community.
- Proposition: assertion connecting concepts; can be true or false.
- Fact type: proposition type whose facts must hold; foundation for models and rules.

Architect view:

- Entity class: a class of things about which information is held.
- Attribute: an assignment of a domain/characteristic to an entity class.
- Relationship role: participation of an entity class in a relationship.
- Domain: reusable definition of allowed values, format, length, precision, default, or other characteristic.

Designer/functioning views:

- Map entity classes and attributes to tables, columns, object classes, files, messages, or other technical representations.
- Track production databases, schemas, copies, extracts, reference sets, and owners.

Design guidance:

- Model business meaning before physical design.
- Represent synonyms, homonyms, language/context, and semantic-community ownership.
- Do not assume every important business concept appears in the data model.
- Treat domains and controlled reference values as metadata when they constrain attributes.

## Activities Column

Business-owner view:

- Activity is the broad family.
- Function is work described by purpose, without sequence, mechanism, or performer.
- Business process is work as performed, often with sequence, mechanisms, parties, and artifacts.
- Process maps, use cases, IDEF, DFDs, and UML activity models expose overlapping metadata; normalize them into activity, flow, mechanism, actor, input, output, and decomposition concepts.

Architect view:

- System process is a technology-independent response or data transformation, often organized around external event types.
- Essential processes separate what must happen from how current mechanisms happen.

Designer/functioning views:

- Program module, job, workflow, interface, service operation, batch step, or automation can implement process metadata.
- Inventory should connect deployed program components to the processes/functions they support.

Design guidance:

- Separate function hierarchy from process sequence.
- Do not use a current process map as the canonical conceptual model without extracting the underlying function, event, data, and responsibility metadata.
- Connect process metadata to data touched, event types that trigger it, parties/roles that perform it, and rules that constrain it.

## Locations Column

Locations metadata covers geographic places, organizational sites, operating locations, networks, and deployed system locations.

Business-owner view:

- Enterprise locations, offices, facilities, logistics networks, and relationships among places.
- Processes, parties, and motivational directives may be scoped by location.

Architect/designer/functioning views:

- Roles at locations, communication paths, hardware/software distribution, network design, system inventory, database instances, and deployment nodes.

Design guidance:

- Distinguish real-world place, business facility/site, logical operating location, network node, and deployed runtime location.
- Use location metadata for jurisdiction, privacy, latency, routing, availability, local process variation, and data-residency decisions.

## People And Organizations Column

People/organization metadata identifies who performs, owns, manages, stewards, approves, uses, and secures information and systems.

Core patterns:

- Party: person or organization.
- Party relationship: employment, organizational structure, sponsorship, responsibility, ownership, or other role relation.
- Management/stewardship role: assignment of a party to manage a concept, symbol, rule, quality standard, system artifact, or production component.
- Access role: authorization and responsibility for interacting with data, screens, programs, or metadata.

Design guidance:

- Model employee, vendor, customer, steward, programmer, DBA, and rule owner as roles/relationships, not inherent subtypes of person.
- Connect access roles to user interface/security design and production controls.
- Every governed metadata object should have a responsible party or role.

## Events And Timing Column

Timing metadata is about event types and schedules, not only timestamps.

Business-owner view:

- Business event type: category of happenings that trigger business processes.
- External business event type: outside enterprise control, including incoming requests, arrivals, receipts, incidents, or temporal/calendar triggers.
- Internal business event type: triggered by enterprise-controlled process completion or state transition.

Architect view:

- System event type: data-relevant event that triggers essential processing or state transition.
- Entity life history/state model: how entity instances move through states.

Designer/functioning views:

- Program event type, trigger, job schedule, queue message, notification, callback, or log event.
- Actual events/logs belong to functioning-system inventory and observability.

Design guidance:

- Separate business event, system event, program event, and log occurrence.
- For event-driven systems, map event type -> triggering source -> process response -> data state change -> rule constraints -> implementation mechanism.
- Temporal events are first-class: month end, renewal date, SLA deadline, embargo lift, retention expiry.

## Motivation Column

Motivation metadata explains why action is taken and why constraints exist.

Business-owner view:

- Vision and mission.
- Ends: desired results, goals, objectives.
- Means: mission, strategy, tactic, course of action.
- Directives: policies and business rules.
- Influencers and assessments: factors that shape plans and constraints.

Architect/designer/functioning views:

- System constraints on data, processes, and state changes.
- Database constraints, programmed validations, workflow controls, and enforced rules.
- Data-quality measurements and operational evidence.

Design guidance:

- Business rules are built on terms, concepts, propositions, and fact types; do not store them as free-floating text only.
- Trace policy -> business rule -> fact type/concept -> system constraint -> enforcement mechanism -> quality/evidence.
- Separate a non-actionable policy from an actionable rule and from the technical control that enforces it.
