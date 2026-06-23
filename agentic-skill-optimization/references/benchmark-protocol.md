# Benchmark Protocol

Use this protocol before evaluating old-vs-new skill performance. The gold-standard source for benchmark philosophy is [research-report-skill-optimization-updated.md](research-report-skill-optimization-updated.md); this file condenses that guidance into an execution checklist.

## Leakage Controls

- Freeze both skill variants before launching benchmark subagents.
- Keep diagnostic notes, suspected failures, proposed changes, rubrics, and expected answers out of subagent prompts.
- Do not use examples copied from the skill body as benchmark cases unless the goal is regression protection rather than generalization.
- Do not tune the candidate on final holdout results. If you do, replace those holdouts before the final measurement.
- Treat any run as contaminated if a subagent sees both variants, sees the rubric, sees another run's output, uses the wrong skill path, or receives extra context unavailable to the paired run.
- Preserve benchmark integrity with fresh or private tasks when possible; public examples and previous agent outputs are weaker evidence.

## Benchmark Shape

Use exactly three final tasks by default. Choose tasks that cover different realistic use modes:

- Common path: the skill's central workflow.
- Edge path: a realistic ambiguity, missing input, retrieval pressure, or constraint conflict.
- Quality path: a task where the skill's review, validation, process discipline, or judgment should matter.

Each task should be runnable by either variant with the same prompt. Keep task prompts self-contained enough that the subagent can act without private context, but do not include hidden evaluation criteria.

Where useful, add diagnostic controls outside the required six-run comparison:

- `no-skill`: default agent behavior without the target skill, to estimate true skill lift.
- `retrieval-pressure`: relevant and irrelevant skills/resources available, to test routing and selection.
- `robustness-slice`: noisy user request, tool failure, stale input, or ambiguous constraints.

Do not let optional controls replace the required old-vs-new paired comparison.

## Scoring Rubric

Pre-register hard gates, process checks, and a 0-5 score.

Hard gates should catch unacceptable failures, such as:

- Fabricated facts, paths, commands, results, or citations.
- Ignored user constraints.
- Unsafe or destructive tool use.
- Missing required deliverable.
- Failure to use the requested skill.
- Obvious benchmark contamination.

Process checks should catch hidden failures that can look fine in the final output:

- Required reference or source was not read.
- Tool output was simulated instead of observed.
- Verification step was skipped or claimed without evidence.
- Skill changed benchmark cases, labels, or scoring after seeing results.
- Output passed by style while failing trace, provenance, or faithfulness expectations.

Use this default 0-5 score unless the domain needs a custom rubric:

- `5`: Excellent result; complete, specific, verified, efficient, and easy to use.
- `4`: Good result; minor omissions or polish issues, no material failure.
- `3`: Acceptable but uneven; solves the core task with noticeable gaps.
- `2`: Weak; partial task completion or significant process errors.
- `1`: Mostly failed; output is difficult to use or misses the main goal.
- `0`: Invalid; hard-gate failure or no meaningful output.

Use the same scorer, rubric, and tie-breakers for all six runs. If using an LLM judge, check for obvious prompt sensitivity, position bias, and rubric gaming. Prefer deterministic checks whenever feasible.

## Subagent Prompt Template

Use one prompt per run. Replace only the skill path and task.

```text
Use $<skill-name> at <baseline-or-candidate-skill-path> to complete this user request.

User request:
<task prompt>
```

If the subagent tool supports isolated working directories, use a separate directory per run. Delete or ignore run artifacts before launching the paired run if artifacts could be discovered accidentally.

## Comparison Table

Record results in this shape:

```text
task_id	variant	skill_path	hard_gate	process_check	score	winner	notes
T1	A	<path>	pass	pass	4	yes	...
T1	B	<path>	pass	warn	3	no	...
```

Map `A/B` back to `baseline/candidate` only after scoring notes are complete.

## Decision Rules

Keep candidate:

- Candidate passes every hard gate.
- Candidate wins at least two tasks, or wins one and ties two while being simpler, cheaper, faster, or more reliable.
- Candidate does not lose on faithfulness, process compliance, maintainability, or safety.
- No hidden cost makes the skill worse to invoke, maintain, or validate.

Revise candidate:

- Candidate improves one important mode but regresses another.
- Failures are narrow, diagnosable, and fixable without changing the benchmark.
- A fresh final holdout can be created after revision.

Discard candidate:

- Candidate fails a hard gate.
- Candidate loses two or more tasks.
- Candidate wins only by overfitting visible benchmark details.
- Candidate adds complexity without measurable benefit.
- Candidate improves output style while worsening process, truthfulness, or robustness.