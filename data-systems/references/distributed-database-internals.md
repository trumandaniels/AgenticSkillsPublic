# Distributed Database Internals

Use this reference when the design or review depends on distributed-database behavior below the product label: failure models, clocks, delivery semantics, failure detection, leader election, consistency, anti-entropy, distributed commit, and consensus.

## Distributed Assumptions

Distributed systems are not single-node programs with slower calls. Always state assumptions about:

- network reliability, latency, bandwidth, and topology,
- local processing and queueing delays,
- backpressure and bounded queues,
- clock source, monotonicity, drift, and timestamp meaning,
- partial failures and partitions,
- failure model: crash-stop, crash-recovery, omission, arbitrary/Byzantine,
- synchrony: asynchronous, synchronous, or partially synchronous.

Do not rely on wall-clock timestamps for ordering unless the system explicitly provides bounded uncertainty or another ordering mechanism.

## Delivery Semantics

Retries can create duplicates. Lost acknowledgments can make the caller unsure whether an operation happened.

Reason in terms of:

- at-most-once delivery,
- at-least-once delivery,
- exactly-once processing illusion via idempotency, deduplication, sequence numbers, or transactions,
- FIFO/order guarantees,
- no-creation/no-duplication assumptions at the abstraction layer.

For side-effecting operations, require idempotency keys, dedupe tables, transactional outbox/inbox, or another explicit duplicate-control mechanism.

## Failure Detection

Failure detectors trade detection speed against false positives. Heartbeats, pings, phi-accrual detectors, outsourced heartbeats, and gossip-based detectors all depend on timing assumptions and workload conditions.

Use failure detection outputs as suspicion, not absolute truth, unless the larger protocol is designed to tolerate mistakes.

## Leader Election

Leader election coordinates authority for writes, membership, scheduling, or replication. Common families include bully-style, next-in-line, invitation, and ring algorithms; practical systems often embed election in consensus protocols.

Design checks:

- who can become leader,
- how split-brain is prevented,
- lease/term/epoch semantics,
- how stale leaders are fenced,
- how clients discover the leader,
- what happens during failover.

## Consistency Models

Name guarantees precisely:

- linearizability/atomic consistency,
- sequential consistency,
- causal consistency,
- read-your-writes,
- monotonic reads,
- writes-follow-reads,
- eventual consistency,
- tunable quorum consistency.

Quorum systems depend on replication factor N, write quorum W, and read quorum R, but overlapping quorums do not automatically solve all freshness, failure, or conflict semantics. State conflict handling, clock/versioning, and repair behavior.

## Anti-Entropy And Dissemination

Eventually consistent systems need convergence mechanisms:

- read repair,
- digest reads,
- hinted handoff,
- Merkle-tree comparison,
- version vectors,
- gossip dissemination,
- partial views/overlay networks.

Design checks:

- convergence trigger and cadence,
- how divergent replicas are detected,
- conflict resolution,
- repair bandwidth,
- stale-read exposure,
- observability for repair lag and inconsistency.

## Distributed Commit And Consensus

Two-phase commit coordinates atomic commit but can block on coordinator failure. Three-phase commit loosens blocking only under stronger timing assumptions. Systems such as Calvin, Spanner, and Percolator combine partitioning, ordering, timestamps, locks, and commit protocols differently.

Consensus protocols such as Paxos/Raft solve agreement under specific assumptions and are commonly used for replicated logs, membership, leader election, and metadata. Consensus is not a generic performance feature; it is a coordination cost paid to get a correctness property.

## Output Checks

- State the failure and synchrony model.
- Identify the coordination problem: membership, leader, replication, commit, ordering, or repair.
- Name the consistency guarantee from the user's perspective.
- Separate transport delivery from durable processing.
- Include duplicate handling and idempotency.
- Include observability for lag, suspicion, repair, leader changes, and quorum/consensus health.
