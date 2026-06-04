# Autoresearch Pattern

## Source Shape

`karpathy/autoresearch` demonstrates a compact autonomous research loop:

- Keep the repository small enough for an agent to understand.
- Mark some files as fixed infrastructure and one file as the editable experiment surface.
- Use one ground-truth metric and one fixed evaluation budget.
- Run a baseline before editing.
- Commit each candidate, run the evaluator, log the metric, and keep only improvements.
- Continue autonomously until interrupted when the user has requested an open-ended run.

The original repo applies this to a single-GPU language model training setup. `prepare.py` is fixed data/evaluation infrastructure, `train.py` is the editable model/training file, `program.md` is the agent instruction file, and `val_bpb` is the metric to minimize.

## Transferable Invariants

Preserve these invariants when adapting the pattern:

1. Fixed evaluator: use the same command and parsing rule for baseline and candidates.
2. Fixed budget: hold time, input size, data, seed policy, hardware, and environment steady unless explicitly testing one of those variables.
3. Narrow edit surface: name files that may be changed and files that must remain read-only.
4. Objective metric: prefer a scalar score. For multi-metric goals, define a primary metric and tie-breakers before running candidates.
5. Reversible state: isolate the loop on a branch or copy so bad experiments can be discarded without touching user work.
6. Persistent ledger: record every attempt, including crashes and regressions, so repeated failures inform the next hypothesis.
7. Simplicity pressure: keep simpler code for ties or tiny improvements, and reject complexity that is not paid for by the metric.

## Generic Ledger

Use tab-separated rows so descriptions can contain commas safely:

```text
commit	metric	status	description
abc1234	1.000000	keep	baseline
def5678	0.982000	keep	cache parsed inputs
bad9999	1.041000	discard	replace search with heuristic
eee0000	0.000000	crash	vectorized path shape mismatch
```

Change the metric column name when useful, for example `val_bpb`, `latency_ms`, `pass_rate`, `accuracy`, or `cost_usd`.

## Candidate Lifecycle

Use this lifecycle for each trial:

1. Store the previous-best commit or diff state.
2. Apply exactly one candidate idea.
3. Commit or otherwise checkpoint the candidate.
4. Run the evaluator to a log file if output is long.
5. Parse the metric and inspect errors if parsing fails.
6. Append a ledger row.
7. Keep the candidate only when it beats the contract.
8. Otherwise return to the previous-best state without disturbing unrelated user changes.

## Research Triggers

Research new approaches when:

- Three or more local variations fail to improve the metric.
- The bottleneck or metric behavior is unclear.
- The code uses a domain-specific technique that has known best practices.
- The next idea would be a large rewrite and needs evidence first.

Prefer primary sources: official docs, papers, implementation notes, source repositories, benchmark reports, and issue discussions from maintainers. Summarize only the tactic you will try and why it should affect the metric.

## Failure Modes

Guard against these common failures:

- Changing the evaluator or data and claiming a metric improvement.
- Keeping a noisy benchmark win after one lucky run.
- Mixing several changes and learning nothing from the result.
- Overfitting to a toy test while harming the user-facing goal.
- Reverting user work while discarding a candidate.
- Filling context with long logs instead of extracting the metric and relevant traceback.
- Continuing to retry an idea family after the ledger shows it repeatedly fails.
