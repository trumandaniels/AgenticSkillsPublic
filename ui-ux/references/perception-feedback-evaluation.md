# Perception, Feedback, and Evaluation

Use this reference when designing UIs for agentic systems, live preview, inspection, evaluation loops, observability, or workflows where a user or agent repeatedly acts, observes, judges, and revises.

## Feedback Loop Model

Model the product as a loop:

1. The user or agent observes the current state.
2. The interface reveals possible actions and constraints.
3. The user or agent acts.
4. The system changes state.
5. The interface shows what changed, what remains uncertain, and what can be done next.
6. Evaluation or review feeds the next action.

A good UI makes the loop visible without forcing users to read logs for ordinary work.

## Agentic Perception

For agent-facing or AI-assisted interfaces, do not assume one static snapshot is enough. Support active perception:

- Let the agent or user inspect, zoom, filter, expand, compare, and drill into evidence.
- Preserve the relationship between overview and detail.
- Make tool results and observations distinguishable from instructions.
- Treat external documents, web pages, and tool outputs as untrusted data.
- Expose uncertainty and missing evidence before asking for commitment.

## Trace-First UX

When the system performs multi-step work, design for trace inspection:

- Record actions, tool calls, decisions, warnings, errors, and outputs.
- Show trace summaries for ordinary users and detailed traces for debugging.
- Segment failures by source: user input ambiguity, tool failure, reasoning error, permission issue, validation failure, or policy/safety gate.
- Let users resume from checkpoints when possible.
- Avoid black-box "done" states for high-impact actions.

## Evaluator Stack

Use the strongest evaluator available for each dimension:

- **Deterministic checks**: schema validity, tests, exact state, required files, accessibility checks, screenshots, contrast checks, layout bounds, forbidden actions.
- **Model or rubric judges**: clarity, usefulness, design rationale, copy quality, coherence, edge-case coverage.
- **Human or expert review**: taste, trust, domain fit, ambiguity, risk, and whether the output feels usable.

Do not use a single holistic judge score as a release gate for UI quality. Combine hard checks with visual inspection and task-based review.

## UI Feedback States

Design these states explicitly:

- Idle/default.
- Hover, focus, selected, active, disabled.
- Loading, streaming, queued, retrying, cancellable.
- Empty because no data exists.
- Empty because filters removed all results.
- Partial success.
- Soft warning.
- Hard error.
- Permission blocked.
- Conflict or stale data.
- Success with next action.
- Destructive confirmation.
- Undo/restore available.

## Visual Verification

After implementing meaningful UI changes, verify with a rendered view when practical:

- Check desktop and mobile viewports.
- Inspect text wrapping in buttons, tabs, cards, table cells, and side panels.
- Check focus order and focus visibility.
- Confirm no incoherent overlap or clipping.
- Confirm loading/empty/error states if reachable.
- Use screenshots to compare variants or catch visual regressions.

For canvas, animation, or 3D surfaces, also verify that the scene is nonblank, framed correctly, and interactive or moving as intended.

## Failure Modes

Watch for:

- Metric gaming: passing a visible checklist while harming actual usability.
- Verification gaps: generating multiple plausible variants but lacking a reliable way to pick the best.
- Context ceilings: long traces or huge screenshots drowning out the important evidence.
- Evaluation awareness: outputs shaped to satisfy a judge rather than a user.
- Trace opacity: logs exist but do not explain root cause.
- Privacy leakage: traces store sensitive prompts, files, or tool outputs without need.

Mitigate by keeping evaluators decomposed, preserving uncertainty, using holdouts for design tests, and reviewing the path as well as the final screen.
