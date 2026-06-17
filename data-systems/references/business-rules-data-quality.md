# Business Rules And Data Quality

Use this reference when the design depends on policies, rules, constraints, derivations, validity, or data-quality evidence. The doctrine is distilled from the Motivation column of *Data Model Patterns: A Metadata Map*.

## Rule Levels

- Policy: broad directive that guides behavior but may not be directly actionable.
- Business rule: actionable directive that constrains or guides the enterprise.
- System constraint: architect-level expression of how a rule constrains data or process state.
- Technical enforcement: designer/builder-level implementation in database constraints, code, workflow, rule engines, access controls, or operational checks.
- Evidence: functioning-system logs, exceptions, data-quality measurements, and audits that show whether the rule is being enforced.

## Rule Foundations

Rules should connect to business meaning:

- terms and concepts define the vocabulary,
- propositions connect concepts,
- fact types define repeatable structures of facts,
- rules constrain allowed facts or state transitions,
- constraints/enforcement implement or monitor those rules.

Avoid rule catalogs that contain only prose. They should also identify the affected concept, fact type, entity class, attribute, relationship role, domain, process, event type, steward, owner, enforcement point, and quality check.

## Common Constraint Types

- Unique identifier: attributes and/or relationship roles that distinguish occurrences.
- Optionality: whether an attribute or role is mandatory, optional, or state/time dependent.
- Cardinality: maximum/minimum occurrence counts for roles or values.
- Referential integrity: whether relationships must point to valid existing occurrences.
- Domain constraint: legal values, format, length, precision, default, code set, or range.
- Derivation: formula or inference that produces a value from other facts.
- Exclusivity/inclusion: mutually exclusive or dependent role/value combinations.
- State constraint: rules that depend on lifecycle state.
- Access constraint: who may view, update, approve, retire, or administer data.

Simple ER notations often show identifiers, optionality, cardinality, domains, and derivations, but these are still constraints. Treat them as rule metadata when traceability, implementation, testing, or governance matter.

## Optionality And State

Avoid reducing optionality to one static flag if the business rule is conditional. Capture the basis for the rule:

- state of the entity,
- event that starts the obligation,
- deadline or temporal trigger,
- role or jurisdiction,
- source system,
- lifecycle phase,
- exception authority.

Example pattern: a field may be optional during intake, required before approval, and irrelevant after retirement. Model that as state-dependent constraint metadata rather than one nullable/not-null flag.

## Derivations

For every derived value, capture:

- source facts,
- formula or inference,
- effective period,
- rounding/precision,
- recomputation trigger,
- storage choice: virtual, materialized, cached, or persisted,
- reconciliation and stale-value detection.

Derived values bridge this skill's metadata-map doctrine and DDIA derived-data doctrine. State the source of record and the rebuild path.

## Enforcement Mapping

Map each important rule to one or more enforcement mechanisms:

- database key, foreign key, unique, check, domain, generated column, trigger, or procedure,
- application validation or domain model invariant,
- workflow approval or access control,
- stream/batch quality check,
- monitoring alert, exception queue, or audit report,
- manual control with responsible party.

When enforcement is split, name the canonical enforcement point and the secondary detection mechanisms. Duplicate validations are acceptable when they protect user experience or defense in depth, but the source of truth must be clear.

## Data Quality

Data quality is rule enforcement observed in production. Define measurements against business expectations, not only storage mechanics.

Useful dimensions:

- validity against domains and constraints,
- completeness against mandatory/state-dependent fields,
- uniqueness and identity resolution,
- referential integrity,
- consistency across sources and derived stores,
- timeliness/freshness,
- accuracy against authoritative evidence,
- lineage and steward accountability.

For quality plans, return: rule/concept, measurement, threshold, source, owner, detection cadence, remediation path, and exception workflow.
