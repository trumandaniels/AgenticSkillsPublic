# Encoding And Evolution Doctrine

Source: Martin Kleppmann, *Designing Data-Intensive Applications*, Chapter 4.

## Compatibility First

Data outlives code. Rolling upgrades, long-lived records, asynchronous messages, mobile clients, caches, and replicas mean old and new code often coexist.

- Backward compatibility: new code can read data written by old code.
- Forward compatibility: old code can read data written by new code.
- Prefer schema evolution rules that tolerate added optional fields and unknown fields.
- Preserve unknown fields when records may round-trip through older services.
- Make breaking changes explicit with versioned topics, APIs, tables, or envelopes and a migration/backfill plan.

## Encoding Choices

- Avoid language-specific serialization formats for durable storage or cross-service contracts unless all readers and writers are deliberately locked to that runtime.
- JSON, XML, and CSV are broadly interoperable but have ambiguity around numbers, binary data, dates, schemas, and required fields.
- Schema-driven binary encodings such as Protocol Buffers, Thrift, and Avro can be compact and evolvable, but require schema governance and compatibility testing.
- Use human-readable encodings where inspection and ad hoc integration matter more than size or speed.
- Use compact schema-driven encodings where traffic volume, storage volume, latency, and type compatibility justify the additional tooling.

## Dataflow Modes

Evaluate compatibility at every dataflow boundary:

- Database writes and reads: old code may read records written by new code and vice versa; migrations must respect both directions during rollout.
- Service APIs: remote calls are not local function calls. Expect timeouts, retries, partial failure, changed contracts, and independently deployed clients.
- Message passing: producers and consumers are decoupled in time; old consumers may process new messages after deployment, and new consumers may replay old messages.
- Events and CDC logs: schemas become historical facts. Plan for replay from old event shapes.

## Output Checks

Any architecture answer that changes schemas, APIs, topics, durable records, or encodings should state:

- compatibility direction required;
- allowed field changes and rejected breaking changes;
- rollout order and rollback behavior;
- replay/backfill implications;
- contract tests or schema-registry checks;
- owner of schema governance.
