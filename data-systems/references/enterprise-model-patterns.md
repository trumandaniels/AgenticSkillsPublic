# Enterprise Model Patterns Doctrine

Source: David C. Hay, *Enterprise Model Patterns: Describing the World, The UML Version*.
Local source: `C:\Users\Truman\Documents\Programming\AgenticKnowledge\Experts\Data\enterprise-model-patterns.md`

Use this reference when a data-system task is really a conceptual enterprise-modeling task: finding stable business concepts, separating business semantics from technology design, or adapting generic model patterns to a domain.

## Core Position

- Model the architect's view before the designer's view. The conceptual model should describe business semantics and fundamental structures, not tables, services, UI screens, queues, ORM classes, or current system artifacts.
- Treat a model like a map: select the level of detail and the details shown according to the problem being solved.
- Prefer stable concepts over current procedures. Forms, current systems, and workflow workarounds are often clues, not canonical entities.
- Use patterns as starting points. A pattern is not the finished model for a real enterprise; adapt language, constraints, and detail to the domain.
- Keep model diagrams communicative. Notation, layout, and architectural grouping all matter because the model is a conversation tool with business people and designers.

## Abstraction Levels

- Level 0: the most abstract reusable template. Use `Thing`, `Thing Type`, `Thing Specification`, names, identifiers, relationships, characteristics, roles, information resources, and accounting links.
- Level 1: the generic enterprise model. Use `Party`, `Geographic Location`, `Asset`, `Activity`, and `Time` as broad business domains.
- Level 2: functional-area patterns inside organizations. Use when modeling facilities, HR, marketing/communications, contracts, manufacturing, or laboratory work.
- Level 3: industry-specific examples. Use when generic enterprise patterns need renamed concepts, deeper subtype trees, modified concepts, or specialized structures.

## Modeling Heuristics

- Start with the language of the business, then normalize concepts into stable pattern families.
- Ask whether a candidate entity is a thing of business significance or merely a representation used by a current system.
- For each entity family, decide whether the task needs instances, types, specifications, relationships, names/identifiers, characteristics, roles, or all of them.
- Use separate name and identifier structures when names change over time, multiple authorities issue identifiers, or identifier types differ by entity type.
- Use characteristic-value structures when descriptive properties vary widely by type, change over time, have multiple sources, need legal values, or require units of measure.
- Use roles to connect parties to things, activities, locations, information resources, and assets without collapsing the party into the thing being managed.
- Model time explicitly. Use dates as transaction attributes for operational facts; use date/time entities when dimensional analysis requires navigation by calendar structure.

## Anti-Patterns

- Treating `Customer`, `Employee`, or `Vendor` as separate fundamental persons instead of roles or relationships involving parties.
- Treating a document, form, report, or screen as canonical when it merely describes or queries other business facts.
- Encoding every possible descriptive property as a column when the property set varies by type and source.
- Choosing technology-specific structures before the conceptual model is clear.
- Assuming a single global identifier exists for parties, assets, or locations without a stewardship and matching strategy.
- Letting a domain example override the generic pattern without identifying what changed: name, subtype depth, selected concept, or specialized detail.

## Output Expectations

When applying this doctrine, produce:

1. The selected abstraction level.
2. The core entity families and why they are fundamental.
3. Instance/type/specification distinctions.
4. Relationship, role, name, identifier, characteristic, and time structures.
5. Business rules that cannot be expressed by structure alone.
6. How the conceptual model maps to later physical design choices without being determined by them.
