# B-Tree And LSM Tradeoffs

Use this reference when choosing or troubleshooting storage access methods such as B-Trees, B+Trees, copy-on-write trees, Bw-Trees, LSM trees, SSTables, Bloom filters, and compaction.

## B-Tree Family

B-Trees and B+Trees organize sorted keys into pages and keep tree height small for disk access. They are strong for:

- point lookups,
- range scans,
- ordered iteration,
- update-in-place workloads,
- primary and secondary indexes in mutable stores.

Important implementation details:

- separator keys guide search,
- internal pages route to child pages,
- leaf pages hold records or record pointers,
- node splits/merges preserve balance,
- sibling links and high keys help concurrent traversal,
- bulk loading can build compact trees efficiently,
- compression and prefix techniques reduce page footprint,
- vacuum/defragmentation may be required after churn.

Variants:

- Copy-on-write trees avoid in-place overwrite and can simplify snapshots, at the cost of write amplification and garbage collection.
- Lazy/adaptive trees defer some maintenance for write efficiency.
- Bw-Trees use delta/update chains and compare-and-swap style concurrency, trading read consolidation and garbage collection complexity for latch-free updates.

## LSM Family

LSM trees buffer writes in memory and flush sorted runs/SSTables to disk, then compact them. They are strong for:

- high write throughput,
- append-heavy workloads,
- SSD-friendly sequential writes,
- workloads that tolerate compaction and read amplification,
- storage systems where immutable files simplify concurrency and recovery.

Important implementation details:

- memtable absorbs writes,
- SSTables store immutable sorted runs,
- write-ahead log protects in-memory writes before flush,
- Bloom filters avoid unnecessary table reads for absent keys,
- merge iteration reads across levels/runs,
- tombstones represent deletes until compaction removes them,
- compaction reconciles versions and reclaims space.

## Amplification Tradeoff

Use the RUM-style lens:

- Read amplification: how many structures must be consulted for one lookup.
- Write amplification: how many physical writes one logical write causes.
- Space amplification: how much extra storage is retained for indexes, old versions, tombstones, or compaction.

B-Trees often favor reads/ranges and predictable lookup paths, but random updates can cause page churn. LSMs often favor write throughput and sequential IO, but compaction, tombstones, and multiple levels can hurt reads and space.

## Secondary Indexes

Secondary indexes are not free in either family:

- B-Tree secondary indexes add update work and may require extra lookup indirection.
- LSM secondary indexes may be attached to SSTables or maintained separately and can multiply compaction/write costs.

For high-write systems, justify each secondary index by concrete query value.

## Choosing Direction

Prefer B-Tree-like storage when:

- range scans and ordered access are central,
- point reads must be stable and low-latency,
- update rate is moderate,
- workload needs mature transactional indexes.

Prefer LSM-like storage when:

- writes are very high volume,
- append/batch ingestion dominates,
- sequential IO matters,
- background compaction is operationally acceptable,
- occasional read amplification can be offset with filters/caches.

## Failure Modes

- LSM compaction backlog causes latency spikes or disk pressure.
- Tombstones accumulate and make reads slow until compaction.
- Bloom filters are missing/mis-sized and absent-key reads touch many files.
- B-Tree pages fragment after churn and need maintenance.
- Copy-on-write trees accumulate garbage without cleanup.
- Too many secondary indexes turn writes into many writes.
