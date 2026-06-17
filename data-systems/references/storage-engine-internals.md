# Storage Engine Internals

Use this reference when a design, review, or incident depends on how a database stores, buffers, recovers, and exposes data inside a node. Distilled from Alex Petrov's *Database Internals*.

## Scope

Database products differ most strongly in how they store data and how they distribute data. Use this reference for node-local storage behavior. Use `distributed-database-internals.md` for multi-node coordination.

## Layout Choices

- Row-oriented layout: keeps all fields for a row together; best for point lookups, OLTP-style updates, and retrieving many columns of one record.
- Column-oriented layout: keeps values for a column together; best for scans, aggregation, compression, and analytical access over fewer columns.
- Memory-based stores: optimize for RAM access but still need durability strategy if data must survive crashes.
- Disk/SSD-based stores: must reason about pages, sequential vs random IO, write amplification, and recovery.

Do not choose a database only by API label. Match workload to layout, storage medium, durability, and access path.

## Files, Pages, And Records

Storage engines turn logical records into binary files. Important concepts:

- data files and index files may be separate or integrated,
- pages/blocks are the unit of IO and cache management,
- page headers hold metadata,
- slotted pages support variable-size cells/records by using indirection,
- overflow pages handle values too large for an ordinary page,
- checksums detect corruption,
- versioning helps compatibility and evolution of file formats.

Design implication: variable-size records, large objects, and update/delete churn can create fragmentation. Plan vacuum/compaction/maintenance and avoid assuming logical delete equals immediate physical reclaim.

## Buffer Management

Most disk-based engines keep a page cache or buffer pool. Reason about:

- kernel page cache vs database-managed cache,
- cache eviction policy,
- dirty page flushing,
- prefetch and immediate eviction for scan-heavy work,
- page pinning/locking,
- write-back pressure.

Performance symptoms often trace to cache miss rate, eviction churn, or scan workloads evicting hot OLTP pages.

## Recovery

Durability requires persistent recovery protocol. Common ingredients:

- write-ahead logging before dirty pages are flushed,
- redo and undo semantics,
- operation logs vs physical/data logs,
- checkpointing,
- steal/no-steal and force/no-force buffer policies,
- crash recovery that rebuilds a consistent state after partial writes.

When reviewing durability, ask what is acknowledged to the caller, what is on stable storage, what can be replayed, and what can be rolled back.

## Concurrency Control

Concurrency-control mechanisms include:

- optimistic concurrency control,
- multiversion concurrency control,
- pessimistic/lock-based control,
- latches for in-memory structure protection,
- locks for transaction-level logical isolation,
- deadlock prevention/detection,
- B-Tree-specific latch coupling and sibling-link techniques.

Do not confuse latches with transaction locks. Latches protect internal structures briefly; locks protect logical data access according to isolation semantics.

## Operational Checks

For storage-engine-sensitive recommendations, include:

- access pattern: point lookup, range scan, append, update, delete, aggregation,
- IO pattern: random vs sequential,
- cache behavior,
- recovery objective and acknowledged durability,
- maintenance path: compaction, vacuum, defragmentation, checkpointing,
- isolation/concurrency symptoms,
- vendor-specific evidence to gather: metrics, query plans, compaction logs, checkpoint logs, WAL volume, page/cache stats.
