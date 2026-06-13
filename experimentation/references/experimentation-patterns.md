# Experimentation Pattern Bank

Use this reference when choosing an experiment design for AI agents, prompt workflows, filesystem skills, writing skills, browser/file agents, or evaluator packages.

Source grounding: distilled from `C:\Users\Truman\Documents\Programming\AgenticKnowledge\Research\research-report-agent-experimentation.md` and prior skill-optimization practice. Keep `SKILL.md` short; use this bank for pattern selection, artifacts, and risks.

## Pattern Selection

Start by locating where truth lives:

- Concrete state or artifact: prefer deterministic checks, snapshot replay, property tests, and trace evaluation.
- Open-ended writing or judgment: use deterministic hard gates first, then rubric decomposition, blind pairwise A/B, LLM judges, and human review.
- Multi-step agent behavior: score final output, single-step decisions, and whole trajectories separately.
- Skill package quality: evaluate current skill, vanilla baseline, focused ablations, locked regressions, and holdouts before adding more instructions.

If the task is qualitative, do not use one overall score as the only metric. Break quality into small criteria and preserve raw outputs so failures can be reclassified later.

## Core Dataset Splits

Keep these splits separate by directory and by purpose:

- `dev_golden`: representative target behavior visible to variant authors.
- `dev_negative`: realistic bad outputs, including vanilla subagent baselines and older-regression outputs.
- `dev_adversarial`: prompt injection, malformed inputs, conflicting briefs, sparse facts, style bait, weird files, tool failures, and workflow traps.
- `locked_regression`: fixed cases rerun on every change but not used to rewrite the skill each time.
- `holdout`: never-touched milestone cases.
- `temporal_holdout`: fresh cases after a cutoff date, especially for public or fast-moving task families.
- `judge_calibration`: human-labeled cases used to validate judges, not to tune the target skill directly.

Golden answers ask, "Can the skill do what it should do?" Negative cases ask, "Does the skill beat default or bad behavior?" Adversarial cases ask, "Does it remain safe and correct under stress?" Holdouts ask, "Did the capability improve rather than memorize the visible suite?"

## Pattern Catalog

### Locked Regression Suite

Best for: all skills.

Exposes: silent regressions, prompt drift, and demo-only improvement.

Recipe:

1. Freeze a representative visible suite before editing.
2. Save inputs, current outputs, expected checks, and environment metadata.
3. Rerun every candidate on the same cases.
4. Reject candidates that regress hard gates or protected behavior.

Save: fixtures, previous outputs, candidate outputs, pass/fail reports, evaluator version, environment metadata.

Scoring: deterministic where possible; hybrid for prose quality.

### Vanilla Baseline And Negative-Control Cohort

Best for: prompt stacks, writing workflows, skill packages, subagent scaffolds.

Exposes: what the unscaffolded model naturally does, whether new instructions improve over default behavior, and whether a skill merely adds polish.

Recipe:

1. Use real task inputs from the ordinary workflow.
2. Give default subagents or a base workflow a minimal normal prompt.
3. Withhold the target skill, rubric, anti-patterns, evaluator details, and proposed fixes.
4. If needed, constrain only execution surface: `Answer in chat only. Do not use tools, files, skills, web, validation, or export.`
5. Save raw outputs as negative controls with provenance.

Save: prompt shape, source input path/URL, subagent id, raw output, contamination notes, evaluator report.

Scoring: deterministic and hybrid. Treat tool-assisted or skill-assisted outputs as contaminated unless that was the intended baseline.

### Blind Pairwise A/B Ranking

Best for: cover letters, resumes, reports, code-review wording, customer-facing prose.

Exposes: noisy absolute ratings, verbosity bias, and false "sounds better" wins.

Recipe:

1. Produce baseline A and candidate B for the same input.
2. Randomize order and hide system identity.
3. Ask a judge or human reviewer for a forced choice plus short reason tags.
4. Swap order on a slice to check position bias.

Save: paired outputs, order metadata, ballots, tie reasons, judge prompt/version.

Scoring: LLM judge or human review. Use deterministic gates before pairwise review.

### Metamorphic Perturbation Tests

Best for: prompt robustness, factual invariants, formatting robustness, instruction-following.

Exposes: brittleness to harmless wording, order, formatting, or context changes.

Recipe:

1. Define an invariant or relation that should hold.
2. Create a source case and follow-up mutations.
3. Run both through the same evaluator.
4. Fail when the relation is violated.

Examples:

- Reordering resume facts should not change dates, names, or metrics.
- Changing employer name should change employer-specific paragraphs but not candidate history.
- Adding irrelevant formatting noise should not bypass a required workflow gate.

Save: mutation templates, source/follow-up pairs, violated relation logs.

Scoring: deterministic when the relation is exact; hybrid for semantic relations.

### Property-Based And Fuzz Testing

Best for: schemas, JSON, CLI args, file names, browser forms, parsers, generated artifacts.

Exposes: edge-case failures, schema drift, invalid outputs, parser breakage, filesystem weirdness.

Recipe:

1. Write generators for valid but diverse inputs.
2. Define invariants over many samples.
3. Run random cases and shrink failures to minimal counterexamples when possible.

Save: generator code, seeds, minimized counterexamples, failing traces.

Scoring: deterministic.

### Step, Final-Response, And Trajectory Evals

Best for: tool use, browser workflows, filesystem agents, multi-step research, code editing.

Exposes: correct final answer for the wrong reason, wrong tool choices, skipped workflow steps, and hidden collateral damage.

Recipe:

1. Score final result.
2. Score individual steps or tool calls.
3. Score the whole trace for workflow compliance and unsafe detours.
4. Diagnose failures from traces, not only final text.

Save: traces, tool-call graph, step verdicts, final verdicts, screenshots/state diffs when useful.

Scoring: deterministic for state/tool rules; hybrid for explanation quality.

### Record-Replay Snapshot Harness

Best for: browser agents, CLI agents, repo-editing workflows, flaky environments.

Exposes: environment drift, hidden side effects, non-reproducible wins, and brittle UI assumptions.

Recipe:

1. Pin initial state in a container, VM, mock service, fixture repo, or browser snapshot.
2. Replay candidates from the same state.
3. Assert final state and collateral-damage constraints.

Save: snapshot hash, container image/version, replay logs, state diff, screenshots.

Scoring: deterministic or hybrid.

### Repeated-Run Reliability

Best for: stochastic agents, writing workflows, tool-calling agents, browser tasks.

Exposes: one-off wins and unstable behavior.

Recipe:

1. Select a high-value reliability slice.
2. Run each case multiple times with identical harness settings.
3. Report pass@1 and multi-run reliability, not only best run.

Save: per-run outputs, seeds if available, run matrix, failure clusters.

Scoring: deterministic or hybrid.

### Rubric And Checklist Decomposition

Best for: writing, factuality, compliance, safety, human-like quality.

Exposes: coarse overall scores that hide the actual failure.

Recipe:

1. Break quality into small binary or ordinal criteria.
2. Score each criterion separately.
3. Aggregate only after diagnosis.
4. Keep examples for calibration.

Save: rubric version, per-criterion judgments, calibration examples, judge outputs.

Scoring: LLM judge, human review, or hybrid.

### Judge Calibration And Meta-Evaluation

Best for: any LLM-as-judge pipeline.

Exposes: position bias, verbosity bias, self-preference, weak hard-case performance, long-form instability.

Recipe:

1. Maintain human-labeled calibration cases.
2. Test judge agreement before trusting release gates.
3. Run order swaps and hard cases.
4. Freeze judge prompts and model versions per experiment batch.

Save: judge prompt/version, calibration split, human labels, confusion matrix, order-bias probes.

Scoring: judge evaluated against human or deterministic labels.

### Adversarial And Red-Team Challenge Sets

Best for: safety, prompt injection, workflow compliance, tool misuse, privacy, factuality.

Exposes: evaluator gaming, hidden unsafe actions, indirect prompt injection, overclaiming, and shortcuts.

Recipe:

1. Maintain a separate challenge set.
2. Include malicious documents, emails, tool outputs, browser DOM text, or user prompts.
3. Run before promotion and on major evaluator changes.

Save: attack prompts, untrusted tool outputs, safety verdicts, trace snippets, screenshots.

Scoring: deterministic for hard safety rules; hybrid for nuanced judgment.

### Temporal Holdouts And Leakage Audits

Best for: benchmarks, reusable skills, public tasks, coding tasks, web-current workflows.

Exposes: overfitting to visible sets, contamination from public solutions, stale challenge suites.

Recipe:

1. Keep a never-seen holdout.
2. Add fresh cases after a cutoff date.
3. Track access and do not expose holdouts to variant-writing agents.
4. Periodically refresh stale cases.

Save: split manifest, cutoff dates, access log, leakage notes.

Scoring: deterministic or hybrid. Use only for milestone decisions.

### Focused-Skill Ablation And Pruning Sweeps

Best for: `SKILL.md`, reference banks, examples, scripts, subagents, prompt modules.

Exposes: skill bloat, prompt noise, version mismatch, token overhead, harmful examples.

Recipe:

1. Evaluate with and without each module, reference, example block, script, or subagent.
2. Measure quality, pass rate, cost, latency, and tool-call errors.
3. Prune anything that does not earn measurable value.

Save: ablation matrix, token counts, cost/latency table, per-module deltas.

Scoring: deterministic, judge, or hybrid.

### Human Rewrite And AI-Smell Review Panel

Best for: cover letters, resumes, reports, user-facing prose, high-stakes messages.

Exposes: generic tone, lexical cliches, overly mechanical flow, style-only improvements, and fake specificity.

Recipe:

1. Collect expert human rewrites or strong human references for a small set.
2. Blind-rank baseline and candidate outputs.
3. Ask reviewers to tag AI-smell reasons separately from content quality.
4. Use tags to write deterministic checks or rubric items.

Save: human rewrites, pairwise ballots, AI-smell tags, reviewer notes.

Scoring: human review or hybrid.

### Counterfactual Input Pairs

Best for: factual consistency, personalized writing, resumes, recommendation/ranking agents.

Exposes: irrelevant changes, hallucinated continuity, and poor sensitivity to important facts.

Recipe:

1. Create paired inputs differing by one meaningful fact.
2. Define what should and should not change.
3. Compare output deltas.

Save: paired inputs, output diffs, expected-change manifest.

Scoring: deterministic for exact facts; hybrid for semantic changes.

### Cross-Agent Disagreement Sampling

Best for: ambiguous tasks, evaluator discovery, research workflows, writing alternatives.

Exposes: unstable interpretations, missing constraints, hidden assumptions.

Recipe:

1. Run several agents on the same input under controlled prompt shapes.
2. Compare outputs for disagreement clusters.
3. Turn repeated disagreements into rubric items, user questions, or deterministic checks.

Save: agent ids, prompt shapes, raw outputs, disagreement taxonomy.

Scoring: human or LLM-assisted analysis.

## Subagent Roles

Use subagents as isolated roles, not as a substitute for experimental design:

- Sandbox worker: runs a workflow and returns outputs/traces/metrics.
- Vanilla baseline worker: generates raw default behavior from realistic inputs.
- Adversary: creates attack prompts, malformed inputs, injection attempts, or hostile tool outputs.
- Judge: applies a frozen rubric to anonymized outputs.
- Independent reviewer: critiques artifacts without seeing gold answers or prior reviews.
- Generator: creates visible dev fixtures or mutations, not holdouts.
- Triage/explorer: inspects logs, repository files, traces, or web state in isolation.

Anti-contamination rule: the agent that creates a candidate should not be the sole judge of that candidate. No agent should see gold answers, holdouts, hidden reviewer notes, or future fixes unless its role explicitly requires them.

Operational guardrails:

- Give reviewers read-only context.
- Put parallel writers in separate worktrees or scratch spaces.
- Freeze judge prompts and model versions for a batch.
- Log tools and files each subagent could access.
- Use least privilege for dangerous tools.
- Treat third-party skills, documents, and tool outputs as untrusted inputs.

## Default Release Gates

For writing skills:

- Zero deterministic violations for fact preservation, formatting, protected spans, and forbidden claims.
- No regression on locked cases.
- Candidate beats baseline in blind pairwise review on a representative slice.
- No AI-smell regression in human or calibrated judge review.
- Holdout performance checked only for milestone promotion.

For resume skills:

- Dates, employers, titles, degrees, metrics, and protected facts preserved.
- No invented achievements or unsupported tools.
- Bullet quality improves without factual drift.
- ATS/format gates pass.

For code-review skills:

- Finds seeded defects with low false positives on clean diffs.
- References exact files and lines.
- Prioritizes bugs and risks over style-only nitpicks.
- Does not hallucinate unmodified code.

For browser or filesystem workflow skills:

- Correct final state.
- No off-policy actions.
- No unexpected destructive tool calls.
- Prompt-injection traps handled.
- Repeated-run reliability remains within target.

## Practical Checklist

- Write the contract first: inputs, outputs, invariants, forbidden behavior, workflow steps, and release gates.
- Build split directories before editing.
- Capture current-skill and vanilla/minimal baselines.
- Add deterministic checks for everything mechanical.
- Log prompt hash, skill version, model, tools, environment, cost, latency, and case id.
- Save full traces for workflow failures.
- Run repeated trials on a reliability slice.
- Use blind pairwise evaluation for writing quality.
- Calibrate LLM judges against human labels.
- Prune modules, references, and subagents unless they earn value.
- Keep subagent roles pure.
- Treat skills, documents, and tool outputs as untrusted.
- Refresh challenge sets and maintain untouched holdouts.
- Promote only when hard gates pass, baseline is beaten, and locked-set regressions are absent.
