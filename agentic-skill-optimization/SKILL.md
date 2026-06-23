---
name: agentic-skill-optimization
description: Diagnose, revise, and empirically validate existing Codex skills with leakage-safe benchmarks, frozen baseline/candidate copies, independent subagent trials, measured old-vs-new comparisons, process checks, and research-backed rules for minimal modular skill changes. Use when Codex needs to improve a skill package, evaluate whether a skill change actually helps, design skill benchmarks, run paired subagent evaluations, prevent benchmark contamination, or decide whether to keep or discard proposed skill edits.
---

# Agentic Skill Optimization

## Overview

Improve an existing skill only when there is evidence it performs better. First inspect the skill and diagnose likely failure modes, then create an isolated candidate revision, define a leakage-safe benchmark, and compare the frozen old skill against the frozen new skill using paired subagent runs.

Treat [references/research-report-skill-optimization-updated.md](references/research-report-skill-optimization-updated.md) as the gold-standard research source for how to actually change skills. Read it before substantial skill edits. Use the other research reports as supplemental sources only when their topic is relevant.

For benchmark setup details, read [references/benchmark-protocol.md](references/benchmark-protocol.md) before creating evaluation cases or launching subagents.

## Reference Routing

Load references deliberately:

- Read [research-report-skill-optimization-updated.md](references/research-report-skill-optimization-updated.md) for the primary rules: minimal modular skills, paired controls, realistic retrieval pressure, process evaluation, robustness slices, leakage audits, and measured skill deltas.
- Read [research-report-skill-optimization.md](references/research-report-skill-optimization.md) for broader academic and industry background, Pareto optimization, hierarchy, reviewer/verifier loops, interface design, and skill-evolution methods.
- Read [research-report-feedback-loops-agent-perception.md](references/research-report-feedback-loops-agent-perception.md) when designing evaluators, trace grading, feedback loops, observability, judge reliability checks, or anti-Goodhart safeguards.
- Read [research-report-memory-system.md](references/research-report-memory-system.md) when the target skill involves memory, retrieval, progressive disclosure, context management, skill routing, or long-horizon knowledge maps.

Do not load every research report by default. Start with the updated optimization report, then load supplemental reports only for the diagnosis or benchmark question at hand.

## Core Contract

Use this workflow for skill improvement, not style-only rewriting. Maintain these invariants:

- Freeze a baseline copy of the original skill before editing.
- Separate diagnosis material from final holdout benchmark cases.
- Run identical task prompts against old and new skill variants.
- Optimize for a Pareto frontier: success rate, faithfulness, process compliance, cost, latency, safety, and maintainability.
- Keep the new skill only when the benchmark shows a real improvement without unacceptable regressions.

If subagents are unavailable, prepare the benchmark and candidate but stop before claiming measured improvement. Report that validation is pending.

## Change Rules

Before editing, decide which lever is likely to matter. Prefer the smallest lever that addresses the diagnosed failure:

- Triggering: improve frontmatter description, naming, and routing cues.
- Interface: reduce ambiguous tool or action choices; align instructions with the agent's natural execution surface.
- Procedure: make sequence, branch conditions, stop conditions, and expected artifacts explicit.
- Progressive disclosure: move detailed protocols into references and repeated deterministic work into scripts.
- Verification: add hard gates, process checks, and task-specific validation steps.
- Robustness: add ambiguity, missing-input, noise, or retrieval-pressure cases to the benchmark before adding bulky instructions.

Do not make a skill bigger just because it failed. Bloated skills often lose by increasing context load, ambiguity, and retrieval friction.

## Workflow

### 1. Inspect the Skill

Read the target skill's `SKILL.md` completely. Read only directly relevant references, scripts, metadata, and recent user feedback needed to understand behavior.

Record a concise diagnosis:

- Triggering: whether the frontmatter description fires for the right tasks and avoids wrong tasks.
- Workflow: whether the body gives enough sequence, decision rules, and stop conditions.
- Progressive disclosure: whether details belong in `SKILL.md`, references, scripts, or assets.
- Validation: whether the skill tells agents how to verify outputs and process compliance.
- Evaluation readiness: whether real task prompts, hard gates, and scoring rules can measure improvement.
- Failure modes: where a capable agent would likely drift, overfit, leak context, skip checks, misuse tools, or produce unmeasured claims.

Do not edit yet unless the skill is broken in a way that prevents inspection.

### 2. Create Isolated Copies

Create two working copies:

- `baseline`: exact original skill, read-only for the experiment.
- `candidate`: editable copy for proposed changes.

Keep paths explicit in notes. Do not let benchmark-running subagents see the diagnosis, expected answer, proposed fix, benchmark rubric, or old/new label.

### 3. Design the Benchmark

Define three representative benchmark tasks. Each task should be a realistic user request that would trigger the target skill and require the skill to add value beyond default agent behavior.

For each task, specify:

- Input artifact or prompt.
- Allowed tools and constraints.
- Expected output format.
- Hard gates for unacceptable failures.
- Process checks for required steps, tool use, verification, and source handling.
- A 0-5 quality score plus any cost, latency, token, or maintainability notes.
- Contamination checks.

Use diagnostic examples to understand failures, but do not reuse them as final holdout tasks. If the candidate was tuned after seeing a holdout result, mark that holdout spent and create a fresh one for the final comparison.

### 4. Revise the Candidate

Make the smallest coherent set of changes that targets the diagnosis. Prefer:

- Better trigger metadata over more body text when invocation is the problem.
- Clear step order and decision rules over broad advice.
- Reference files for detailed protocols that are needed only sometimes.
- Scripts for repeated deterministic operations.
- Explicit verification gates over vague quality language.
- Reviewer, verifier, or trace-checking steps when tool calls or factual claims are consequential.

Avoid adding examples that mirror hidden benchmark cases. Avoid bloating `SKILL.md` with generic reasoning advice Codex already knows.

### 5. Run Paired Subagent Evaluation

Run three paired comparisons, one pair per benchmark task:

1. Launch one subagent with the baseline skill copy and the task prompt.
2. Launch a separate subagent with the candidate skill copy and the same task prompt.
3. Repeat for all three tasks.

This produces six total task-solving subagent runs: `3 tasks x 2 variants`.

Use neutral prompts such as:

```text
Use $target-skill at <skill-path> to complete this user request:
<benchmark task>
```

Do not say the run is an evaluation. Do not reveal whether the skill is old or new. Do not tell the subagent what you changed or what you expect to improve.

If the skill's value is uncertain, add a no-skill or default-agent control as a diagnostic baseline, but keep the required old-vs-new comparison unchanged.

### 6. Score and Decide

Score outputs using the pre-registered rubric before looking for explanations. Prefer blind labels such as `A` and `B` during scoring when practical.

Keep the candidate only if:

- It passes all hard gates.
- It wins on at least two of three tasks, or wins one and ties two with a clear simplicity, reliability, cost, or latency advantage.
- It does not create a serious regression in trigger accuracy, safety, factuality, process compliance, tool discipline, or maintainability.

If results are mixed, either make one more targeted iteration with a fresh final holdout or report the candidate as unproven. Do not claim improvement from cherry-picked examples.

## Reporting

End with:

- Baseline path and candidate path or final installed path.
- Diagnosis summary.
- Benchmark task list, without leaking hidden answer keys if future reuse matters.
- Six-run comparison table with task, variant label, hard-gate result, process result, score, cost/latency notes if available, and winner.
- Decision: keep, revise again, or discard.
- Residual risks such as small sample size, noisy judging, weak evaluator reliability, contamination risk, or benchmark coverage gaps.

When installing a revised skill, validate the folder with the standard skill validator and mention whether validation passed.