# PoEAA Pattern Routing Catalog

Source: *Patterns of Enterprise Application Architecture*. Use this as a routing map, not a replacement for design judgment.

## Domain Logic Patterns

- Transaction Script: organize business logic as procedures, usually one per business transaction. Best for simple logic and fast delivery. Fails when duplication and conditional complexity grow.
- Domain Model: object model of domain concepts with both behavior and data. Best for complex, volatile business logic. Requires stronger OO skill and more sophisticated persistence mapping.
- Table Module: one class per table or record set. Best where platform tools, UI binding, and transactional disconnected record sets make tabular structures the natural unit.
- Service Layer: application boundary exposing operations to clients. Best with multiple clients, cross-resource transactions, security/transaction control, or workflow/application coordination.

## Data Source Architectural Patterns

- Table Data Gateway: one object handles all SQL for a table, view, or query. Strong fit for Table Module and Transaction Script.
- Row Data Gateway: one object per row. Strong fit for Transaction Script; avoid as primary pattern for rich Domain Model.
- Active Record: domain object includes simple persistence plus simple domain logic. Good when objects align closely with tables.
- Data Mapper: mapper layer keeps domain objects and database schema independent. Use for rich Domain Model, legacy schemas, complex mapping, or independent evolution.

## Object-Relational Behavioral Patterns

- Unit of Work: tracks new, dirty, deleted, and sometimes read objects, then coordinates commit order, transactions, and concurrency checks.
- Identity Map: ensures one in-memory object per database identity in a session. Needed for mutable loaded objects; also useful as a session cache.
- Lazy Load: placeholder/proxy/value holder/ghost that loads related data only when used. Use when data requires an extra call and is not always needed; avoid ripple-loading cascades.

## Object-Relational Structural And Metadata Patterns

- Identity Field: store database identity in the object; prefer stable surrogate keys when object identity needs to survive schema changes.
- Foreign Key Mapping: map object references to foreign keys.
- Association Table Mapping: map many-to-many associations with a link table.
- Dependent Mapping: let a parent control persistence of dependent child objects that do not have independent identity.
- Embedded Value: map a small value object into columns of the owning row.
- Serialized LOB: serialize an object graph into a large object column when parts are not queried independently.
- Single Table Inheritance: one table for hierarchy; simple and refactoring-friendly, but may waste columns and centralize load.
- Class Table Inheritance: table per class; normalized but join-heavy.
- Concrete Table Inheritance: table per concrete class; fast simple reads but brittle to superclass changes and harder for integrity.
- Metadata Mapping: store mapping rules as data for code generation or reflection; useful when mapping code becomes repetitive.
- Query Object: represent database queries as objects in domain terms; useful with Data Mapper and Metadata Mapping.
- Repository: collection-like access to domain objects, hiding mapping and query construction; useful in large rich-domain systems and for multiple data sources/testing.

## Web Presentation Patterns

- Model View Controller: separate model, view, and controller responsibilities in web presentation.
- Page Controller: one controller per page/action; good for simple or document-oriented sites.
- Front Controller: one handler for all requests; good for complex navigation, shared request processing, and central dispatch.
- Template View: embed presentation markers in templates; common and tool-supported.
- Transform View: transform domain/data outputs into HTML or other views, often via XSLT-like tooling; can improve testability.
- Two Step View: first produce logical screen data, then transform to a common look-and-feel.
- Application Controller: centralize screen-flow and command dispatch decisions when navigation grows complex.

## Distribution Patterns

- Remote Facade: coarse-grained remote API over fine-grained local objects. Thin boundary only; no domain logic.
- Data Transfer Object: serializable data carrier for remote calls. Shape by client needs, keep simple, and use assemblers to isolate DTOs from the domain model.

## Offline Concurrency Patterns

- Optimistic Offline Lock: detect conflicts at commit with versions or comparable checks. Default when conflicts are rare.
- Pessimistic Offline Lock: prevent conflicts by reserving data across a business transaction. Use when conflicts are likely or expensive.
- Coarse-Grained Lock: lock a group of related objects as one unit.
- Implicit Lock: hide/enforce locking inside framework code so callers cannot forget it.

## Session State Patterns

- Client Session State: store state on client; strongest server statelessness, weakest trust/security, poor for large state.
- Server Session State: store serialized state on server; simplest programming model, needs failover/clustering support.
- Database Session State: store session state as committed database data; supports stateless servers and failover, but adds database load and pending-state complexity.

## Base Patterns

- Gateway: isolate access to external resources or APIs.
- Mapper: move data between independent representations.
- Layer Supertype: common superclass for layer-wide behavior.
- Separated Interface: place an interface in one package while implementation lives elsewhere to control dependencies.
- Registry: well-known object lookup; use sparingly and mind thread/session scope.
- Value Object: small immutable value with equality by value.
- Money: value object for monetary arithmetic and allocation.
- Special Case: object representing a common exceptional/null case.
- Plugin: link classes during configuration rather than hard-coding dependencies.
- Service Stub: substitute a service for tests.
- Record Set: in-memory tabular data structure.
