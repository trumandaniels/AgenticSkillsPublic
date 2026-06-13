# Memory and Context

Use this reference when a UI/UX task depends on long-horizon product context, design rationale, user research, private knowledge, trace history, or evidence-backed decisions.

## Core Principle

Long context is not a memory strategy. Keep the active context small, retrieve only what is relevant, and preserve durable design knowledge in structured files or product surfaces.

For UI/UX work, memory should answer:

- What decisions have already been made?
- What user evidence supports them?
- What alternatives were rejected and why?
- What constraints or brand/product rules must persist?
- What did prior testing reveal?
- What should future agents or designers not rediscover?

## Progressive Disclosure

Use a layered structure:

- **Discovery layer**: names, descriptions, tags, routes, and short summaries.
- **Procedure layer**: concise workflows and checklists.
- **Reference layer**: detailed design rationale, research notes, examples, and constraints.
- **Evidence layer**: screenshots, transcripts, metrics, usability notes, issue traces, and source artifacts.

Load detailed material only when it changes the decision.

## Design Memory Types

- **Working memory**: immediate task, current files, current screen, visible bug, active constraints.
- **Episodic memory**: what was tried, what failed, what changed, what the user approved, and why.
- **Semantic memory**: durable product facts, design principles, reusable patterns, component rules, brand constraints.
- **Evidence memory**: user quotes, transcript spans, screenshots, telemetry, expert notes, tickets, and benchmark cases.
- **Decision memory**: explicit tradeoffs, rejected alternatives, acceptance criteria, and unresolved questions.

## Evidence Hierarchy

When summarizing research or transcripts:

1. Preserve raw evidence with source, timestamp, author/speaker, and context.
2. Create atomic evidence spans for one coherent claim or observation.
3. Build standalone cards that resolve pronouns and name what question the evidence answers.
4. Build theme summaries only after the evidence layer is stable.
5. Use summaries to route; use leaf evidence to support claims.

Do not answer final product questions from summaries alone when user-facing or high-stakes decisions depend on the evidence.

For expert design testimonials, use `expert-testimonial-memory-map.md` for the concrete memory layers, source boundaries, synthesis rules, and conflict-resolution policy.

## Retrieval Guidance

Use multiple retrieval views when the source corpus is large:

- Lexical search for exact phrases, product names, UI labels, issue IDs, and quotes.
- Semantic search for fuzzy concepts and paraphrased needs.
- Metadata filters for speaker, date, product area, persona, platform, source type, or confidence.
- Reranking when candidate sets are large or noisy.

Evaluate retrieval before evaluating generation. If the right evidence is not retrieved, the design answer will be weak no matter how polished the prose sounds.

## Context Hygiene for UI Work

- Prefer current rendered screens, nearby code, design tokens, and product constraints over generic advice.
- Keep stale screenshots, old traces, and superseded design decisions out of active context unless comparing history.
- Summarize long reports into task-specific claims before implementation.
- Use subagents or separate passes for broad research, visual critique, implementation, and evaluation when context would otherwise become crowded.
- Record durable discoveries in the project or skill only after they prove reusable.

## When to Build Memory Into the Product

Add visible product memory when users need continuity:

- saved filters and views;
- recent projects or objects;
- version history and named checkpoints;
- comments, decisions, and approvals;
- audit trails;
- reusable presets, templates, and command history;
- onboarding progress or dismissed guidance;
- collaboration presence and review state.

Keep memory explainable and reversible. Users should be able to inspect, edit, reset, or ignore stored preferences when they affect behavior.
