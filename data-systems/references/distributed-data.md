# Distributed Data Doctrine

Source: Martin Kleppmann, *Designing Data-Intensive Applications*, Part II. This file distills replication, partitioning, transactions, partial failures, consistency, and consensus into reusable design checks.

## Replication

Replication is used for low latency, high availability, read scalability, and disconnected or geographically distributed operation. The hard part is not copying bytes; it is handling changes while preserving user-visible guarantees.

- Single-leader replication simplifies write ordering because all writes flow through one leader. It is easy to understand, but failover, replication lag, and leader unavailability dominate the risk profile.
- Synchronous replication improves durability/freshness but increases write latency and availability risk. Asynchronous replication lowers latency but can lose recent writes during failover.
- Multi-leader replication helps with multi-region writes and disconnected operation, but concurrent writes require conflict detection, resolution, and user/domain semantics for merges.
- Leaderless replication uses quorums, read repair, anti-entropy, version vectors, siblings, and tombstones. It can remain available under some faults, but callers must understand stale reads, conflicting versions, and delete semantics.
- Name the read guarantee: read-your-writes, monotonic reads, consistent-prefix reads, bounded staleness, causal consistency, linearizability, or best-effort eventual convergence.

## Partitioning

Partitioning is for datasets or throughput that exceed one machine, but every partitioning scheme creates operational consequences.

- Key-range partitioning supports ordered scans and range queries, but monotonic keys and uneven ranges create hot partitions.
- Hash partitioning spreads load more evenly, but weakens range access and can make locality-sensitive queries expensive.
- Compound keys can preserve useful locality in one prefix while hashing or distributing a suffix; use when both range access and write distribution matter.
- Document-partitioned secondary indexes keep writes local but make global secondary-index reads scatter/gather.
- Term-partitioned or global secondary indexes can make reads targeted, but writes touch multiple partitions and often become asynchronous.
- Rebalancing, routing metadata, and partition ownership changes are production events. Include throttling, observability, and human override for high-risk clusters.

## Transactions And Isolation

Transactions reduce many fault and concurrency cases to abort/retry. They are most valuable when invariants span multiple objects, multiple indexes, denormalized data, or a read-decision-write workflow.

- Atomicity: failed work is not half-applied.
- Isolation: concurrent transactions do not observe unsafe intermediate states.
- Durability: committed data survives expected faults.
- Read committed prevents dirty reads and dirty writes, but not read skew, lost updates, write skew, or phantoms.
- Snapshot isolation prevents many read-skew cases and is commonly implemented with MVCC, but write skew can still violate cross-row invariants.
- Serializable isolation is the safest application abstraction for complex invariants, implemented by serial execution, two-phase locking, or serializable snapshot isolation.
- Weak isolation pushes anomaly handling into application code. Make that choice only when invariants are local, approximate data is acceptable, or compensating controls are explicit.

## Distributed System Failure Model

Distributed systems have partial failures. Some nodes may be healthy, some paused, some slow, and the network may lose, delay, duplicate, or reorder messages. Timeouts detect symptoms, not truth.

- If a request times out, the caller usually cannot know whether the operation failed, succeeded, or is still running.
- Physical clocks can drift, jump forward/backward, or be observed with unknown error bounds. Avoid using wall-clock time as proof of order or ownership unless the system provides explicit bounded-clock guarantees.
- Processes can pause for garbage collection, scheduling, page faults, or live migration. A paused process may resume after other nodes declared it dead.
- Fencing tokens are required when a stale leader, lease holder, or lock holder could continue writing after replacement.
- Test fault assumptions empirically: partitions, packet loss, clock skew, process pauses, disk loss/corruption, failed restore, and degraded-but-not-dead nodes.

## Consistency And Consensus

Consistency models are user-facing contracts, not product slogans.

- Linearizability makes replicated data look like a single up-to-date copy. It is simple for application logic but often slower and less available across high-latency or partitioned networks.
- Causality orders events by cause and effect. It allows concurrent branches and merges, reducing coordination compared with global linearizability.
- Serializability is about transaction interleavings; linearizability is about recency of individual operations. They are related but not the same requirement.
- Consensus is required for fault-tolerant agreement on one irrevocable decision. Common equivalents include leader election, membership, total order broadcast, distributed transaction commit, uniqueness decisions, and linearizable compare-and-set.
- Do not hand-roll consensus. Use a proven database, coordination service, or consensus-backed log when the design needs automatic failover, membership, locks/leases, or globally unique decisions.
