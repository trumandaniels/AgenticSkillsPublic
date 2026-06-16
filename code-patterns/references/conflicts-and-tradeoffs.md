# Conflicts And Tradeoffs

Use when two good rules disagree.

| Tension | Default bias | Override when |
|---|---|---|
| Extract helper vs keep locality | Keep locality for short, single-use code | the extracted step has a strong domain name and reduces mixed abstraction levels |
| Remove duplication vs preserve meaning | Preserve meaning | branches are semantically identical and likely to change together |
| Add abstraction vs keep concrete code | Keep concrete code | the abstraction answers a known current need and lowers maintenance effort |
| Rename broadly vs protect API | Protect public API | migration path and compatibility plan are clear |
| Remove comments vs keep rationale | Remove stale or restating comments | the comment captures constraints, tradeoffs, or history not visible in code |
| Improve testability vs minimize change | Minimize design churn | hidden side effects make important behavior hard to verify |
| Optimize performance vs preserve simplicity | Preserve flexibility and simplicity | evidence shows a real user-facing performance problem in the exact code path |
| Rewrite vs redesign in place | Redesign in small steps | experiments show rewrite is cheaper, both systems can be maintained, and users can validate incremental delivery |
| Single shared model vs bounded contexts | Keep one model inside a clear context | terms have different meanings, teams own different models, or integration cost overwhelms unification |
| Rich domain model vs simple Smart UI | Use a rich model for complex domain logic | the app is simple data entry/display, has few business rules, and the team cannot support model-driven design |
| Generic subdomain vs core domain investment | Invest in the core domain | the concept differentiates the product or carries specialized business knowledge |
| Technical package shape vs domain module story | Prefer the domain story in domain code | framework constraints or deployment boundaries are essential and cannot be moved behind a clearer domain-facing structure |
| Premature optimization vs latent scale risk | Preserve simplicity until pressure is evidenced | requirements, capacity estimates, or production signals show a credible near-term bottleneck |
| Preserve specific error meaning vs hide internals | Preserve caller-recoverable meaning | details would leak sensitive internals or encourage unsafe retry behavior |
| Async decoupling vs synchronous simplicity | Keep synchronous flow when latency and reliability needs allow | slow work, spikes, fanout, or offline consumers justify queues and delivery semantics |
| Persistent connection vs polling simplicity | Prefer simpler polling when update frequency and overhead are low | latency, empty-response overhead, or bidirectional updates justify long-polling, SSE, or WebSockets |
| Load balancing vs sticky state | Keep request handling stateless where practical | correctness requires affinity and the state placement, failure, and rebalancing story is explicit |

When a conflict appears, state the deciding local evidence before choosing.
