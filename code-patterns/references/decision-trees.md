# Decision Trees

Use these before applying pattern cards.

## Refactor Or Leave Alone

1. Identify the concrete evidence of a problem. Do not fix code because it merely looks unfashionable.
2. Rank the possible change by user value, implementation effort, and future maintenance effort.
3. Check behavior protection: existing tests, characterization tests, or small manual verification.
4. Prefer the smallest change that solves the evidenced problem, because larger changes increase defect risk.
5. If pain is weak, evidence is missing, or validation is unavailable, leave the code alone or add tests first.

## Extract Function

1. Scan call sites and current tests.
2. Find a coherent substep that makes the surrounding piece simpler for its target reader.
3. Check variable lifetime, mutation, error propagation, and resource lifetime.
4. Extract only if the new piece is simpler, self-contained, and easier to understand than the original chunk.
5. Validate behavior and reread both caller and extracted piece.

## Introduce Abstraction

1. Confirm a present, known need rather than a predicted future need.
2. Separate semantic duplication from coincidental shape similarity.
3. Confirm the abstraction preserves user/domain specificity rather than flattening useful distinctions.
4. Introduce the abstraction only when it reduces implementation and maintenance effort now.
5. If the abstraction makes the code more complex, treat it as overengineering.

## Rename

1. Determine whether the symbol is local, module-private, or public.
2. Inspect nearest readers and domain vocabulary.
3. Rename locally when meaning is clear and consumers are bounded.
4. For public names, preserve compatibility or stage migration.

## Comment

1. Ask whether the comment explains what, why, constraints, or history.
2. Replace "what" comments with clearer code when possible.
3. Keep or improve rationale comments that preserve decisions not visible in code.
4. Remove stale comments only after confirming the code/test suite carries the needed meaning.

## Domain Model Alignment

1. Listen for domain terms in requirements, tests, tickets, and user language that are absent from code.
2. Check whether the current code expresses those concepts directly or only through procedures, reports, queries, or technical names.
3. If a missing concept would simplify discussion, remove duplication, or move domain logic into the domain layer, model it explicitly.
4. Keep the implementation tied to the model; if implementation forces a different language, update the model discussion too.
5. Validate with domain scenarios, tests, and code names that use the same language.

## Entity, Value Object, Or Service

1. If continuity and identity matter across time or representations, model an entity and define identity explicitly.
2. If only attributes matter and instances are interchangeable, model a value object and prefer immutability.
3. If the operation is a meaningful domain activity that does not naturally belong to an entity or value object, model a stateless domain service.
4. If creation is complex or must enforce aggregate invariants, use a factory.
5. If persistent aggregate roots need global lookup, use a repository and keep clients out of storage mechanics.

## Model Boundary

1. Identify whether terms have one meaning or multiple meanings across teams, modules, schemas, or external systems.
2. If one unified model is intended, add tests and communication loops to keep it unified.
3. If meanings legitimately differ, name the bounded contexts and prevent direct model leakage.
4. Translate at explicit boundaries, and test the translations.

## Core Domain Refactoring Priority

1. Identify the core domain: the specialized model area that differentiates the product and carries the most user/business value.
2. Separate generic subdomains and support mechanisms from the core when they add cognitive load without specialized knowledge.
3. When refactoring time is scarce, choose work that clarifies the core domain or its relationship to supporting elements before peripheral polish.
4. Keep generic subdomains correct and isolated, but avoid spending core-team attention on broad generality unless the core needs it now.
5. Validate priority decisions against scenarios: the core should be easier to understand, test, and evolve after the change.

## Domain Module Organization

1. Inspect package/module names and ask what domain story they tell.
2. Treat modules as part of the model, not just file containers or technical layers.
3. Prefer conceptual cohesion inside modules and low coupling between modules.
4. Resist framework or pattern-based packaging when it splits one conceptual object or crams unrelated concepts together.
5. Rename or move modules in small tested steps when the current structure hides the domain model or blocks deeper refactoring.

## Scale Or Performance Boundary

1. Clarify the requirement before choosing a mechanism: latency target, throughput, data volume, read/write ratio, availability, reliability, and manageability.
2. Define the interface and data model so the code boundary matches how callers and data will flow.
3. Estimate enough capacity to identify likely pressure points; avoid speculative scale work when the current need is small.
4. Choose the narrowest mechanism that matches the access pattern: cache for repeated reads, index for targeted lookup, load balance for stateless request distribution, partition for data volume or hot-path isolation.
5. Check the downside: invalidation, write amplification, hot partitions, cross-shard operations, replica consistency, operational observability, and failure recovery.
6. Validate with metrics, tests, or a focused load/failure check before claiming the boundary is improved.

## Async Or Realtime Boundary

1. Decide whether the caller needs an immediate answer, eventual processing, or continuous updates.
2. Use a queue when work can be decoupled and retried; define producers, consumers, delivery semantics, ordering needs, and idempotency before changing the call path.
3. Use polling only when latency and empty-response overhead are acceptable.
4. Use long-polling when server events are sporadic and HTTP compatibility matters.
5. Use SSE when updates flow server-to-client and the client does not need the same channel for writes.
6. Use WebSockets when bidirectional low-overhead communication is actually required.
7. Validate timeout, reconnect, retry, duplicate message, and slow-consumer behavior.
