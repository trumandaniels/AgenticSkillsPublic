---
name: experimentation
description: Autonomous optimization workflow for improving code toward a measurable goal through repeated hypotheses, edits, evaluation, logging, research, and keep-or-discard decisions. Use when Codex is asked to autonomously improve performance, quality, benchmark scores, model metrics, agent behavior, prompts, algorithms, tests, or any codebase with a concrete objective; especially when the user asks to iterate, experiment, try approaches, self-evaluate, optimize, run overnight, or research new methods while measuring progress.
---

# Experimentation

## Overview

Run a bounded autonomous research loop: establish a baseline, make one motivated change, evaluate it against a fixed metric, keep measured improvements, discard regressions, log the result, and repeat until the budget or user stops the run.

This skill generalizes the `karpathy/autoresearch` pattern beyond ML training. Read [references/autoresearch-pattern.md](references/autoresearch-pattern.md) when you need the source pattern, loop invariants, or guardrails.

## Fit Check

Use this workflow only when the task has, or can be given, a measurable evaluator:

- A command that returns a score, test result, benchmark, quality metric, generated artifact score, or comparable acceptance signal.
- A clear optimization direction: lower is better, higher is better, pass/fail with tie-breakers, or a multi-metric priority order.
- A reversible code surface: git branch, clean working tree, or an explicitly isolated scratch copy.

If no evaluator exists, create the smallest credible one first. If the goal cannot be evaluated locally, ask the user for the missing evaluator or constraints before starting the loop.

## Setup

1. Define the experiment contract:
   - Goal: the user-facing outcome to improve.
   - Metric: exact command, parse rule, and optimization direction.
   - Budget: iterations, time, cost, or stopping threshold. If the user asks to keep going autonomously, continue until interrupted while still giving periodic concise updates.
   - Scope: files allowed to edit and files that are read-only.
   - Tie-breakers: prefer simpler code, fewer dependencies, lower resource use, and smaller diffs when metric changes are negligible.
2. Protect the workspace:
   - Inspect `git status --short` before editing.
   - Create or confirm a dedicated branch such as `experiment/<date>-<goal>`.
   - Do not overwrite, reset, or remove user changes. If unrelated dirty files exist, leave them alone; if they affect the experiment, work around them or ask.
3. Create an untracked ledger, usually `experiments.tsv`, with columns:

```text
commit	metric	status	description
```

Add optional columns only when they help compare runs, such as `duration_s`, `memory_gb`, `tokens`, `score_secondary`, or `notes`.

4. Run the baseline before changing code. Record the current commit or worktree state, metric, runtime, and any warnings.

## Experiment Loop

Repeat this loop:

1. Re-read the current best result, recent failed attempts, and relevant code.
2. Generate one hypothesis with a reason it could improve the metric.
3. Research when stuck, when the domain is unfamiliar, or when repeated local ideas stop improving. Prefer official docs, papers, benchmark writeups, and source code over broad web summaries.
4. Make the smallest coherent change that tests the hypothesis. Avoid mixing independent ideas in one trial.
5. Commit the candidate on the experiment branch before evaluation when the repo is clean enough to do so.
6. Run the fixed evaluator with output redirected to a log file when verbose.
7. Parse the metric using the same rule as the baseline.
8. Classify the run:
   - `keep`: primary metric improves, or metric ties while code is meaningfully simpler or cheaper.
   - `discard`: metric regresses, tie-breakers lose, or the change adds unjustified complexity.
   - `crash`: evaluator fails, times out, OOMs, or cannot produce a valid metric.
9. Append one ledger row with the commit, metric, status, and a terse description.
10. If keeping, advance from that commit. If discarding, revert only your own candidate changes and return to the previous best state.

For discard handling, prefer the least destructive reversible action that fits the repo state. `git revert` is safest for published/shared branches. `git reset --hard <previous-best>` is acceptable only on a dedicated local experiment branch after confirming the reset would remove only commits and files created by this loop.

## Choosing Experiments

Favor experiments that directly target the observed bottleneck or failure mode:

- Performance: profile first, then reduce hot-path work, allocation, I/O, synchronization, or algorithmic complexity.
- Model or ML quality: vary data, objective, architecture, optimizer, schedule, regularization, context length, batch composition, or evaluation leakage controls.
- Agent or prompt quality: tighten instructions, add examples, add validation tools, improve state tracking, reduce ambiguity, or split brittle workflows into deterministic scripts.
- Product quality: create scenario tests, measure task completion, reduce latency, improve error handling, and remove confusing UI states.
- Reliability: reproduce failures, add narrow regression tests, improve invariants, and measure flake rate.

When several directions are plausible, try cheap/high-signal changes before expensive rewrites. After multiple failures, summarize what has been ruled out and pivot to a different family of ideas.

## Evaluation Discipline

Keep comparisons fair:

- Run the same evaluator, same dataset/inputs, same environment, and same time budget unless the experiment contract explicitly changes.
- Treat evaluator changes as infrastructure work; do not compare scores before and after evaluator changes as if they are the same metric.
- Repeat noisy benchmarks enough to avoid keeping random variance. Use median or best-of-N only if declared before comparing.
- Watch for metric gaming. Preserve the user's real goal over the local proxy.
- Prefer a small real improvement with a clean diff over a fragile gain that makes future work harder.

## Reporting

During long runs, report compact progress:

- Current best metric and baseline delta.
- Number of kept, discarded, and crashed attempts.
- The best idea so far and the next direction.
- Any blocker that prevents meaningful evaluation.

At the end, provide:

- Best commit or file state.
- Baseline versus final metric.
- Ledger location.
- Notable failed approaches.
- Remaining risks, especially evaluator noise or coverage gaps.
