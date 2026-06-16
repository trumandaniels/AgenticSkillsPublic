# Domain Pattern Adaptation

Use this reference for Level 2 functional patterns and Level 3 industry adaptations from *Enterprise Model Patterns*.

## Adaptation Moves

- Rename generic concepts when the domain language is specific but the structure is unchanged.
- Elaborate subtypes when the generic model is correct but the domain needs a deeper hierarchy.
- Modify selected concepts when an industry uses a familiar term with a different underlying structure.
- Add specialized detail when the industry has unique physical, legal, procedural, or measurement structures.
- Keep most of the enterprise model generic. Industry-specific models usually specialize only a few areas.

## Level 2 Functional Patterns

### Facilities

Use facilities when a place has purpose and operation, not merely geography. Facilities connect geographic locations, parties, assets, and activities. Treat addresses as specialized location/facility descriptors with jurisdictional variation.

### Human Resources

Treat employment as a role/relationship between a person and organization, not as a kind of person. Include positions, assignments, hiring, education, certifications, benefits, compensation, and accounting implications when relevant.

### Marketing And Communications

Model communications as activities involving parties, channels, procedures, information resources, and context. Avoid reducing communication to a message table when originator, recipient, campaign, medium, procedure, and purpose matter.

### Contracts

Treat contracts as agreements among parties that oblige activities and/or assets, often in exchange for payment. Model contract roles, costs, deliveries, line items, terms, and fulfillment.

### Manufacturing

Build on assets and activities. Distinguish product/asset specifications, work orders, routing steps, production steps, material movement, equipment utilization, labor usage, cost capture, and actual versus standard cost.

### Laboratory

Use laboratory patterns for controlled observation and measurement. Model samples, procedures, test methods, laboratory tests, observations, expected observations, parameters, assets/instruments, and derived parameters.

## Level 3 Industry Patterns

### Criminal Justice

Often adapts generic enterprise concepts with domain-specific names. Model cases, evidence, case events, status, people/organizations, roles, and categories.

### Microbiology

Mostly elaborates asset specifications into deeper scientific subtype structures. Model chemical elements, compounds, biological structures, composition, products, and packaging as specialized asset/specification patterns.

### Banking

Modifies familiar concepts. Financial instruments and accounts often behave like agreements/contracts rather than physical products. Model instrument specifications, instruments, characteristics, components, agreements, roles, delivery of services, geography, and currency.

### Oil Field Production

Adds specialized facility and asset detail. Model surface and subsurface facilities, wellbores, completions, well assemblies, facility structures, purposes/products, assembly structures, and physical characteristics.

### Highway Maintenance

Adds network and path detail. Model paths, nodes, intersections, crossings, grade separation, flows, physical assets, asset placement, and geographic referencing.

## Choosing A Domain Pattern

1. Identify which Level 1 family dominates: party, geography, asset, activity, time, information, or accounting.
2. Decide whether Level 2 functional patterns cover the need.
3. If industry-specific, identify whether the adaptation is renaming, subtype elaboration, concept modification, or specialized detail.
4. Preserve business language, but do not let local vocabulary hide generic structures.
5. State which parts remain generic and which are genuinely domain-specific.
