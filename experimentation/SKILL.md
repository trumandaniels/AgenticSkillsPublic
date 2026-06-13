---
name: experimentation
description: Autonomous optimization workflow for improving code, prompts, agents, skills, benchmarks, or other measurable systems through repeated hypotheses, isolated variants, evaluation, logging, and keep-or-discard decisions. Use when Codex is asked to autonomously improve performance, quality, benchmark scores, model metrics, agent behavior, prompt behavior, skill packages, workflows, tests, or any codebase with a concrete objective; especially when the user asks to iterate, experiment, self-evaluate, optimize, run overnight, improve a skill, build an evaluator, compare variants, or research new methods while measuring progress.
---

# Experimentation

## Overview

Run a bounded autonomous research loop: establish a baseline, make one motivated change, evaluate it against a fixed metric, keep measured improvements, discard regressions, log the result, and repeat until the budget or user stops the run.

This skill generalizes the `karpathy/autoresearch` pattern beyond ML training. Read [references/autoresearch-pattern.md](references/autoresearch-pattern.md) when you need the source pattern, loop invariants, or guardrails.

For choosing an experiment design, dataset split, subagent role, evaluator stack, or release gate, read [references/experimentation-patterns.md](references/experimentation-patterns.md). Use it as the pattern bank for locked regressions, vanilla baselines, perturbation tests, property/fuzz tests, trajectory evals, snapshot replay, repeated-run reliability, rubric decomposition, judge calibration, adversarial sets, holdouts, ablations, and human AI-smell review.

For optimizing filesystem-based skills or prompt/workflow packages, read [references/skill-optimization.md](references/skill-optimization.md). That mode adds package inspection, golden cases, isolated variants, approval gates, and durable learnings.

## Fit Check

Use this workflow only when the task has, or can be given, a measurable evaluator:

- A command that returns a score, test result, benchmark, quality metric, generated artifact score, or comparable acceptance signal.
- A clear optimization direction: lower is better, higher is better, pass/fail with tie-breakers, or a multi-metric priority order.
- A reversible code surface: git branch, clean working tree, or an explicitly isolated scratch copy.

If no evaluator exists, create the smallest credible one first. If the goal cannot be evaluated locally, ask the user for the missing evaluator or constraints before starting the loop.

For qualitative outputs, define a decomposed rubric with hard gates before making changes. Use deterministic checks first, then LLM judging only for traits that cannot be mechanically measured.

When the bottleneck is unclear, use `references/experimentation-patterns.md` to choose a diagnostic pattern before editing: vanilla baselines for default failure distribution, ablations for prompt/skill bloat, perturbation tests for brittleness, trajectory evals for workflow failures, or blind pairwise review for writing quality.

## Setup

1. Define the experiment contract:
   - Goal: the user-facing outcome to improve.
   - Metric: exact command, parse rule, and optimization direction.
   - Budget: iterations, time, cost, or stopping threshold. If the user asks to keep going autonomously, continue until interrupted while still giving periodic concise updates.
   - Scope: files allowed to edit and files that are read-only.
   - Tie-breakers: prefer simpler code, fewer dependencies, lower resource use, and smaller diffs when metric changes are negligible.
   - Gates: protected behaviors that must not regress, such as factuality, safety, privacy, latency, cost, or existing passing cases.
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
- Skill package quality: improve routing metadata, progressive disclosure, reference structure, evaluator coverage, tool sequence reliability, or failure-mode guidance.
- Product quality: create scenario tests, measure task completion, reduce latency, improve error handling, and remove confusing UI states.
- Reliability: reproduce failures, add narrow regression tests, improve invariants, and measure flake rate.

When several directions are plausible, try cheap/high-signal changes before expensive rewrites. After multiple failures, summarize what has been ruled out and pivot to a different family of ideas.

Use the pattern bank to match experiment families to failure modes. Prefer locked regression suites for drift, vanilla negative controls for default-output comparison, metamorphic perturbations for brittle prompts, record-replay snapshots for environment drift, repeated-run reliability for stochastic outputs, judge calibration for LLM-scored metrics, temporal holdouts for contamination risk, focused ablations for skill bloat, and human AI-smell panels for high-stakes prose.

For prompt, writing, and skill-package quality work, create "vanilla output" baselines when subagents are available and the user has explicitly authorized subagent use. Spawn isolated default subagents with the real task inputs and the minimal ordinary user prompt, such as `make a cover letter for this job`, while withholding the target skill, desired rubric, anti-pattern list, evaluator details, and proposed fixes. If needed, constrain only the execution surface, for example `answer in chat only; do not use tools, files, skills, web, validation, or export`, so the subagent produces raw default output instead of invoking the optimized workflow. Save the raw outputs with provenance as negative controls before designing new gates or examples. Use them to learn the typical failure distribution; do not edit them into better examples or let variant-writing agents see hidden holdouts.

## Evaluation Discipline

Keep comparisons fair:

- Run the same evaluator, same dataset/inputs, same environment, and same time budget unless the experiment contract explicitly changes.
- Treat evaluator changes as infrastructure work; do not compare scores before and after evaluator changes as if they are the same metric.
- Repeat noisy benchmarks enough to avoid keeping random variance. Use median or best-of-N only if declared before comparing.
- Watch for metric gaming. Preserve the user's real goal over the local proxy.
- Prefer a small real improvement with a clean diff over a fragile gain that makes future work harder.

For skill or prompt optimization, keep holdout cases hidden from variant-writing context when possible. Reject variants that improve visible examples by weakening general instructions, leaking hidden answers, adding brittle overfit rules, or increasing hallucination risk.

When using vanilla subagent baselines, keep comparisons fair: all subagents should receive the same candidate/context packet shape, comparable real task inputs, and the same execution constraints. Record which agent produced each output, the source input path or URL, the prompt shape, and whether tools or skills were disabled. Treat accidental tool-assisted or skill-assisted outputs as contaminated baselines; discard or label them separately instead of mixing them with raw default outputs.

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
