# Generic Enterprise Model Patterns

Use this reference for Level 0 and Level 1 conceptual data modeling.

## Reusable Template

Most model families can be decomposed into:

- `Thing`: the actual business instance.
- `Thing Type`: a fundamental category of things.
- `Thing Specification`: a detailed type that can specify an asset or activity enough for offering, cataloging, or execution.
- `Thing Relationship`: an actual association between instances.
- `Thing Type Relationship`: a design or allowed association between types/specifications.
- `Thing Name` and `Thing Identifier`: historical and authority-sensitive labels/codes.
- `Thing Characteristic`: descriptive property definitions.
- `Thing Characteristic Value`: sourced, dated values for an instance or type/specification.
- `Thing Role`: a party's responsibility, participation, or management role involving a thing.

## Party Pattern

Use `Party` for people and organizations when they share names, identifiers, relationships, characteristics, contracts, addresses, or roles.

Apply this pattern when the domain includes customers, vendors, employees, agencies, households, departments, partners, or legal counterparties.

Key structures:

- `Party Type` reproduces and extends the subtype tree.
- `Party Relationship` captures membership, family, organization structure, affiliation, or other party-to-party associations with effective dates.
- `Party Name` and `Party Identifier Value` handle multiple names, name history, multiple identifier authorities, and type constraints.
- `Party Characteristic` keeps variable descriptors out of rigid columns.
- Roles should usually represent `customer`, `employee`, `vendor`, `owner`, `manager`, or `issuer` rather than making those separate person-like entities.

## Geographic Location Pattern

Use `Geographic Location` for places, not for facilities or addresses.

Core subtypes:

- `Geographic Area`: geopolitical, management, natural, or surveyed areas.
- `Geographic Point`: point coordinates.
- `Geographic Solid`: three-dimensional bounded spaces.
- `Geographic Line`: paths or routes.

Key structures:

- `Geographic Location Relationship` captures containment, boundary definition, overlap, and other spatial relations.
- `Geographic Name` and `Geographic Identifier` handle standards, languages, history, and authorities.
- `Geographic Characteristic` handles demographic, physical, or management descriptors.
- `Geographic Role` connects parties to places, such as jurisdiction or management.

Do not confuse land or spatial extent with the organization governing it, the facility placed on it, or a postal address.

## Asset Pattern

Use `Asset` for physical things of value: discrete items, inventory, lots, buildings, materials, equipment, and products.

Key distinctions:

- `Asset`: the actual item, lot, building, or inventory quantity.
- `Asset Type`: generic category.
- `Asset Specification`: catalog/specification-level description of a model, material grade, or product/service offering.
- `Asset Structure`: actual component usage.
- `Asset Type Structure`: designed bill-of-materials or allowed composition.

Use asset characteristics when product or asset properties vary by type/specification. Use structures for assemblies, materials, components, and actual build differences.

## Activity Pattern

Use `Activity` for work or actions that occur over time. Use `Event` for point-in-time occurrences that trigger or result from activities.

Key structures:

- `Activity Type`: generic category.
- `Activity Specification`: procedure, service, recipe, routing, or instruction set.
- `Activity Structure`: composition, work breakdown, and dependencies.
- `Activity Type Structure`: planned or specified composition/dependency.
- `Trigger`: connection from an event to the activity it causes.
- `Activity Role`: parties' participation, management, communication, or direct labor roles.

For workflow design, model both what is supposed to happen and what actually happened.

## Time Pattern

Use dates as attributes for operational facts when the date simply locates a transaction, event, effective period, or activity duration.

Use time entities when the system needs dimensional navigation by day, month, quarter, year, language-specific names, fiscal calendars, or multiple levels of date precision.

## Information Resource Pattern

Use `Information Resource` when documents, images, reports, software, messages, or web pages are business-significant objects in their own right.

Separate:

- `Information Resource Definition`: the underlying contents and structure.
- `Information Resource Instance`: a physical or electronic copy.
- `Information Resource Relationship`: composition or reference between resources.
- `Concept`, `Expression`, and `Business Term`: semantic links between resources and business concepts.
- `Distribution`, `Role`, and `Disposition`: sending, authorship/ownership, archiving, destruction, and holds.

Do not model every report as a canonical data entity. Model an information resource only when the resource itself is governed, transmitted, approved, retained, or otherwise business-significant.

## Accounting Pattern

Use accounting patterns when financial records need to link to real-world parties, assets, activities, contracts, or cost centers.

Core concepts:

- `Account` and `Account Type`: asset, liability, equity, revenue, expense, and local chart categories.
- `Cost Center`: organizational or business object being accounted for.
- `Rollup Scheme`: a coherent way to aggregate accounts without double counting.
- Accounting transactions must satisfy balancing rules that usually live in application logic, not only in the model.

Use accounting as a model of business effects, not as a replacement for the underlying real-world facts that caused those effects.
