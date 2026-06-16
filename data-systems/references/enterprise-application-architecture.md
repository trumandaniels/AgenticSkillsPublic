# Enterprise Application Architecture Doctrine

Source: Martin Fowler, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, and Randy Stafford, *Patterns of Enterprise Application Architecture*, local source `C:\Users\Truman\Documents\Programming\AgenticKnowledge\Experts\Data\patterns-of-enterprise-application-architecture.md`. This file is compact doctrine and routing guidance; do not reproduce long source passages.

## Scope

Use PoEAA doctrine when the design question is about enterprise applications: persistent data, business processes, complex and changing business rules, multiple users, database access, UI/API clients, integration with other systems, and transaction/session concerns.

Do not treat these patterns as a universal mandate. Fowler's framing is explicitly choice-oriented: simple systems need simple architecture, and patterns must be finished in the context of the project.

## Layering Doctrine

The core enterprise application layers are:

- Presentation: display information, accept user or client commands, and translate input into application operations.
- Domain: the real point of the system, including validations, calculations, business rules, workflow-relevant domain decisions, and invariant logic.
- Data source: communication with databases, messaging systems, transaction managers, packages, and external systems.

Keep domain and data-source code independent of presentation code. A useful leak test: if adding a command-line interface or replacing the database would force business-rule duplication, logic is probably in the wrong layer.

Separate logical layers even when they run in one process. Do not turn every logical layer into a physical tier; process boundaries add latency, deployment complexity, interface ceremony, and failure modes.

## Performance Vocabulary

Name the performance concern before prescribing architecture:

- Response time: time to complete a request.
- Responsiveness: time to acknowledge user action or show progress.
- Latency: minimum time to get any response, especially across a remote boundary.
- Throughput: work completed per unit time.
- Load sensitivity/degradation: how performance changes as load increases.
- Capacity: maximum effective load or throughput before unacceptable degradation.
- Scalability: how adding resources changes performance.

Measure before and after optimization. Minimize remote calls as an architectural rule because latency is not made transparent by middleware.

## Domain Logic Doctrine

Choose domain logic organization by domain complexity, team skill, database/tool constraints, and expected evolution:

- Transaction Script: one procedure per business transaction. Use for simple business logic, straightforward CRUD/workflow, and teams that need speed and clarity.
- Domain Model: object model that combines behavior and data. Use for complex, volatile, interacting business rules where duplication and conditional sprawl would grow quickly.
- Table Module: one object per database table or record set, operating on tabular data. Use when the platform and UI tooling revolve around Record Set-like structures.
- Service Layer: application boundary and operation set. Use when there are multiple clients, multiple transactional resources, cross-cutting transaction/security concerns, or application workflow coordination.

Prefer a thin Service Layer over a rich Domain Model when the domain should remain reusable and application workflow/transaction coordination needs a stable boundary. Do not put all business behavior in a service layer by habit; decide whether behavior is domain logic or application coordination.

## Persistence Mapping Doctrine

Separate SQL/data-source access from domain and presentation logic even in simple systems. The persistence pattern should fit the domain logic pattern:

- Transaction Script pairs well with Table Data Gateway or Row Data Gateway.
- Table Module pairs naturally with Table Data Gateway and Record Set-like data.
- Simple Domain Model can use Active Record if classes align closely with tables.
- Rich Domain Model usually needs Data Mapper, often with Unit of Work and Identity Map.
- Repository and Query Object are useful when a rich domain model has many query shapes, multiple data sources, or a need for collection-like access to persisted objects.

Use Unit of Work when tracking created, changed, deleted, and read objects becomes nontrivial. Use Identity Map when mutable database-backed objects can be loaded more than once in a session. Use Lazy Load only when it avoids extra database calls for data not always needed; watch for ripple loading.

## Distribution Doctrine

Do not distribute fine-grained objects. Design fine-grained objects for in-process collaboration, then add coarse-grained remote boundaries only where a real process/network boundary is required.

When remote access is required:

- Use Remote Facade as a thin, coarse-grained boundary over fine-grained objects.
- Use Data Transfer Object to move enough data in one call.
- Keep domain logic out of Remote Facade.
- Prefer clustering copies of the same application process over splitting object classes across nodes for imagined scalability.
- Consider asynchronous messaging when responsiveness, decoupling, or integration semantics fit better than synchronous RPC.

## Concurrency And Session Doctrine

Distinguish system transactions from business transactions. A user-level business transaction may span multiple requests and cannot usually hold a database transaction open the whole time.

- Use Optimistic Offline Lock when conflicts are rare or cheap to retry.
- Use Pessimistic Offline Lock when conflicts are likely or user work would be too costly to lose.
- Use Coarse-Grained Lock when a group of related objects should be treated as one lockable unit.
- Use Implicit Lock to reduce the chance that developers bypass the chosen locking strategy.
- Treat inconsistent reads as seriously as lost updates when calculations depend on data read but not modified.

Choose session state by amount of data, security, failover, clustering, and development effort:

- Client Session State: best for tiny non-sensitive state or session identifiers; validate and protect anything returned by the client.
- Server Session State: simplest for programming, especially when platform support handles passivation/failover.
- Database Session State: useful for stateless servers and failover, but increases database traffic and pending-state complexity.
