# ProPlay Source Map

This reference preserves the source trail for Agentic Skill Scaffolding. Read it before installing or substantially customizing a ProPlay-inspired scaffold.

## Primary Sources

- Paper PDF: https://arxiv.org/pdf/2606.12780
- Paper HTML: https://arxiv.org/html/2606.12780v1
- Repository: https://github.com/antman9914/proplay

## What To Borrow

ProPlay is useful here as an architectural pattern and as a source of local mechanics. For Codex skills, borrow these ideas and implement them with local scripts where practical:

- Preplay before execution: use learned procedural memory to sketch a likely high-level path before starting the task.
- Procedure graph: represent reusable task stages as nodes and useful transitions as edges.
- Reliability records: treat transitions as context-sensitive evidence, not hard rules; maintain reward-weighted task embedding records locally.
- Episodic refinement: update memory after attempts using success, failure, correction, validation signal, executed traces, and local reward proxies.
- Failure retrieval: consult similar failure patterns before acting so the next run can avoid known traps.
- Soft guidance: let the plan guide the agent while allowing user instructions and fresh observations to override it.

## What To Port With Local Boundaries

Port the paper's procedural mechanics when they can run locally: trace-aware episode records, graph node and edge updates, reward/outcome-weighted transition reliability, task-specific reliability scoring with local embeddings, failure-suffix retrieval, and optional local environment adapters.

Do not require paid API calls, OpenAI API keys, hosted benchmark services, or direct benchmark dependencies by default. The ProPlay repo's programmatic LLM runner can be treated as reference code, but a Codex-native scaffold should let the current Codex run or a fresh Codex subagent provide the reasoning step while deterministic local scripts maintain the memory state.

Do not claim that a scaffolded skill has improved merely because memory files were added. Improvement requires held-out evaluation, ideally with fresh Codex subagents.

## Repository Components To Map Conceptually

The ProPlay repository separates the benchmark-agnostic framework from benchmark-specific environments. Map those pieces into Codex skill scaffolding like this:

- Graph logic -> `references/procedure-graph.json`, `scripts/retrieve_memory.py`, and `scripts/refine_graph.py`.
- Environment interface -> the target skill's existing workflow, available tools, deterministic validators, tests, simulators, or optional local adapter scripts.
- LLM client -> the current Codex run or a fresh Codex subagent, not a paid API call from a script.
- Benchmark folders -> held-out user tasks or representative local artifacts.
- Episode traces -> compact planned traces, executed traces, productive prefixes, failure suffixes, reward/outcome signals, and evidence pointers, not full transcripts.

## Codex-Native Adaptation

A target skill should gain these local files or sections:

1. A short `SKILL.md` Procedural Memory section that says when to read memory, how to preplay, when to capture, and when to refine.
2. `references/procedure-memory.md`, a human-readable guide for the target skill's retrieve-preplay-execute-capture-refine loop.
3. `references/procedure-graph.json`, a compact machine-readable memory store with nodes, edges, episodes, failure patterns, capture policy, retrieval policy, and optional environment interfaces.
4. `scripts/retrieve_memory.py`, a local retrieval script using required sentence-transformer embeddings, RRF, and transition reliability.
5. `scripts/record_episode.py`, a local capture script for compact trace/reward-aware episodes.
6. `scripts/refine_graph.py`, a local graph-update script for nodes, edges, reward-weighted reliability, and failure patterns.

Use `scripts/init_procedural_memory.py` from this skill to create the default files. Then adapt the generated memory reference to the domain.

## Evaluation Pattern

Use fresh Codex subagents as the Codex-native replacement for the repo's programmatic agent runs:

```text
Use $target-skill at <absolute-target-skill-path> to complete this user request:
<held-out task>
```

For clean comparisons, keep a baseline copy of the target skill before adding procedural memory, run the same held-out tasks against baseline and scaffolded variants, and score outputs before drawing conclusions.