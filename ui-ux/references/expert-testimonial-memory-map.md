# Expert Testimonial Memory Map

Use this reference when UI/UX work depends on expert interviews, talks, transcripts, design-leader testimony, or conflicting design advice. The goal is to preserve expert nuance as evidence, not convert every expert sentence into a universal rule.

## Source Boundary

Treat expert testimonials as an evidence corpus, not as the skill's root instructions.

The expected source corpus can include UI expert transcripts, talks, PDFs, notes, and research reports such as a local `AgenticKnowledge/Experts/UI` collection. Keep that corpus as source material outside this skill; store only the rules for turning it into memory here.

Belongs in the memory map:

- named expert claims, stories, examples, and cautions;
- source metadata such as title, speaker, timestamp or page, date, transcript quality, and topic;
- reusable design principles that are supported by multiple sources or repeated expert emphasis;
- context boundaries: product type, audience, organization scale, platform, risk level, and era;
- conflicts and minority views, with the conditions under which each view applies.

Does not belong in the memory map:

- raw full transcripts copied into the skill;
- uncited quotes or claims whose source cannot be recovered;
- task-specific user preferences that have not proved reusable;
- generic design slogans with no decision pressure;
- a flattened "best practice" when experts disagree because they are optimizing different contexts.

## Artifact Boundary

Keep these artifacts separate:

- **Source corpus**: raw transcripts, PDFs, talk notes, videos, and research reports. These are evidence, not instructions.
- **Derived memory**: spans, cards, themes, and decision rules generated from the source corpus.
- **Runtime context**: the current product, codebase, screenshots, user request, and constraints.
- **Skill instructions**: this file and `SKILL.md`, which describe how to retrieve, judge, and apply the evidence.

Do not store derived memory back into `SKILL.md` unless it is a durable decision rule. Do not store raw source text in reference files unless it is a short exemplar needed to define a checker or schema.

## Memory Layers

Use a conservative four-layer map.

### L0: Raw Source Evidence

The raw transcript, PDF, video, talk, or notes stay outside the skill unless the user explicitly asks to bundle them. Preserve source path or URL, speaker, timestamp/page, and raw wording.

Use L0 for:

- exact quote requests;
- attribution disputes;
- checking whether a summary overreached;
- high-stakes design claims.

### L1: Evidence Spans

Create one span per coherent expert claim, story, warning, or rule. Keep one dominant expert voice per span.

Each span should include:

- `span_id`
- `expert`
- `source_title`
- `source_ref`
- `timestamp_or_page`
- `source_type`
- `transcript_quality`
- `claim`
- `context`
- `design_domain`
- `confidence`
- `tags`

Do not merge experts at this layer.

### L2: Expert Cards

Create standalone cards that summarize one expert's position on one topic.

Each card should include:

- `expert`
- `topic`
- `position`
- `why_it_matters`
- `applies_when`
- `does_not_apply_when`
- `supporting_span_ids`
- `tensions`
- `confidence`

Example topics:

- user research and usability testing;
- goal-directed design and personas;
- direct manipulation, modes, undo, and interaction safety;
- iconography, metaphor, and recognizability;
- power tools, craft, beauty, and quality;
- data, intuition, and product judgment;
- prototyping, AI tools, and fidelity;
- design culture, critique, and decision ownership.

### L3: Theme Nodes

Create cross-expert theme nodes only after L1 and L2 are useful.

Each theme node should separate:

- `consensus`
- `disagreements`
- `minority_views`
- `decision_rules`
- `experts_covered`
- `evidence_span_ids`

Use theme nodes to route and synthesize. Do not use them as final evidence without expanding back to expert cards or spans.

### L4: Decision Rules

Promote a rule to L4 only when it is reusable, context-bounded, and supported by either expert consensus or strong task evidence.

A decision rule must include:

- `rule`
- `default_action`
- `strongest_context`
- `exceptions`
- `what_would_change_the_decision`
- `evidence_basis`

Suggested derived-memory layout for a project that builds the corpus:

```text
ui-expert-memory/
  sources/
    manifest.jsonl
  spans/
    ui_expert_spans.jsonl
  cards/
    expert_cards.jsonl
  themes/
    theme_nodes.jsonl
  rules/
    decision_rules.jsonl
  eval/
    retrieval_questions.jsonl
    conflict_cases.jsonl
```

This layout is illustrative; use the host project's conventions when they already exist.

## Expert Lanes

Use these lanes to classify expert evidence. A lane is a retrieval hint, not a ranking of importance.

- **Usability science**: user testing, empirical measurement, iteration, task success, findability, comprehension. Examples: Jakob Nielsen, Steve Krug.
- **Goal-directed design**: personas, user goals, field research, working backward from user intent, complex-system caution. Examples: Alan Cooper.
- **Human-centered and emotional design**: beauty, delight, control, visceral/behavioral/reflective response, social and environmental consequences. Examples: Don Norman, Brenda Laurel.
- **Interaction safety and learnability**: modelessness, undo, error recovery, human interface patterns, simplicity, learnability. Examples: Larry Tesler, Jef Raskin.
- **Iconography and visual language**: recognizable symbols, metaphor, silhouettes, pixel constraints, personality, durable icon meaning. Examples: Susan Kare.
- **Craft and product culture**: design tenets, quality bars, critique culture, taste, details, customer love, last-mile polish. Examples: Bob Baxley, Katie Dill, Alex Schleifer, Ethan Eismann.
- **Data and intuition**: analytics, qualitative signals, customer logs, prototype evidence, judgment under uncertainty. Examples: Julie Zhuo, Katie Dill.
- **AI and future interfaces**: AI as design material, agentic interaction, generated prototypes, personalization, human oversight, model limitations. Examples: Matias Duarte, Don Norman, Bob Baxley, Katie Dill.

When a source fits multiple lanes, tag all relevant lanes. Do not force one expert into one lane permanently; the lane belongs to the claim, not the person.

## Retrieval Rules

- For exact wording, retrieve L0/L1 with lexical search and metadata filters.
- For "what does expert X think," retrieve L2 filtered by expert, then expand to L1.
- For "what do experts say," retrieve L3, require at least two expert lanes when possible, then expand to L2/L1.
- For compare/contrast, retrieve each expert separately before synthesis.
- For design implementation, retrieve decision rules first, then inspect current product context before applying them.
- For conflicts, retrieve both sides and state the context that makes each rule sensible.

## Authority and Boundaries

Use this priority order when evidence conflicts:

1. Explicit user requirements and current product constraints.
2. Safety, accessibility, legal, privacy, and destructive-action constraints.
3. Direct evidence from the current product: screenshots, code, telemetry, support tickets, user research, and usability tests.
4. Expert evidence that matches the product context.
5. Cross-expert consensus across different lanes.
6. Single-expert testimony.
7. General aesthetic preference.

Do not let expert advice override rendered evidence from the actual interface. Do not let current interface conventions preserve a known usability or accessibility problem.

## Conflict Decision Rules

When rules conflict, first classify the conflict:

- **Goal conflict**: experts optimize different user outcomes.
- **Audience conflict**: advice differs for novice, expert, consumer, enterprise, developer, admin, or accessibility users.
- **Maturity conflict**: discovery, beta, growth, and mature products need different rules.
- **Surface conflict**: marketing page, editor, dashboard, mobile flow, command tool, and AI assistant surfaces have different density and explanation needs.
- **Risk conflict**: finance, health, privacy, destructive actions, and public communication require stricter recovery and evidence.
- **Evidence conflict**: quantitative telemetry, qualitative research, expert testimony, and rendered UI inspection point in different directions.

Resolve by naming which conflict type is active, then apply the most specific rule that matches the current product context.

### Prototype Early vs Wait to Draw

Use low-fidelity or no-fidelity framing when the problem, object model, or decision criteria are still unclear. Use prototypes once there is a hypothesis to test, a flow to align on, or a technical interaction to feel.

Nuance:

- "Wait to draw" protects teams from prematurely converging on attractive but wrong visuals.
- "Prototype the path" works when the prototype is treated as a question, not as a finished answer.
- AI-generated high-fidelity mockups are useful for breadth after intent is stable; they are risky when they make an unresolved product idea feel falsely complete.

Decision rule:

- If the team is debating what problem to solve, write the object model, workflow, and constraints first.
- If the team is debating whether an interaction works, prototype and test it.

### Simplicity vs Power

Prefer simplicity for first contact, comprehension, and ordinary repeated tasks. Preserve power for expert users through progressive disclosure, command search, shortcuts, saved views, inspectors, bulk actions, and automation.

Nuance:

- Simple does not mean weak.
- Powerful does not mean visually dense.
- A professional tool can be dense when users need comparison and throughput, but density must be organized around stable structures.

Decision rule:

- Default surface covers the common path.
- Advanced power is reachable, searchable, reversible, and teachable.

### Data vs Intuition

Treat data as evidence about observed behavior, not as the whole truth. Treat intuition as a hypothesis formed from experience, not as a veto over evidence.

Nuance:

- Quantitative data can miss new behavior, long-term trust, small cohorts, and qualitative pain.
- Intuition can detect emerging patterns but can also preserve taste bias.
- Customer logs, sales calls, support tickets, prototype reactions, and usability observations are data too.

Decision rule:

- If data and intuition disagree, check instrumentation, cohort, time horizon, and what outcome is being optimized.
- Run a small qualitative or prototype test before choosing a purely aesthetic or purely metric-driven path.

### Beauty and Delight vs Usability

Usability is the floor; beauty and delight can raise trust, motivation, memorability, and emotional connection. Do not use delight to mask unclear workflow.

Nuance:

- For operational tools, beauty usually means clarity, rhythm, fit, and confidence rather than decorative flourish.
- For consumer, creative, or brand-led products, emotional response may be part of the core job.

Decision rule:

- First make the task understandable and recoverable.
- Then use craft, motion, iconography, and visual personality to reinforce meaning and trust.

### Consistency vs Innovation

Follow platform, product, and design-system conventions unless breaking them creates a clear user benefit that can be taught and recovered from.

Nuance:

- Consistency reduces learning cost.
- Innovation is justified when the existing pattern cannot express the new object model, AI behavior, or workflow.
- Compatibility with a bad interface can preserve the original mistake.

Decision rule:

- Keep familiar semantics for common controls.
- Break convention only with evidence, visible affordance, escape routes, and onboarding.

### User Requests vs User Goals

Listen to what users request, but design for the underlying goal and context of use.

Nuance:

- Users often describe solutions in the vocabulary of the current product.
- Field research and workflow observation reveal constraints that feature requests miss.
- Product teams still need judgment about what not to build.

Decision rule:

- Translate requests into jobs, constraints, and success criteria before designing features.
- Validate the proposed solution against the user's real workflow.

### Modes vs Contextual Tools

Avoid hidden or sticky modes that make the same action mean different things without clear feedback. Contextual tools are acceptable when the mode is visible, bounded, reversible, and easy to exit.

Nuance:

- Complex professional tools sometimes need modes.
- The harm comes from invisible scope, unclear state, and unrecoverable mistakes.

Decision rule:

- If a mode is necessary, show mode state persistently, explain what actions are affected, provide escape/undo, and avoid mode-dependent destructive actions.

### Design by Committee vs Collaboration

Use broad input for evidence, constraints, and critique. Keep decision ownership clear.

Nuance:

- Expert testimony often criticizes committee design because it diffuses taste and decision responsibility.
- Cross-functional collaboration is still essential for feasibility, data, support, sales, accessibility, and product strategy.

Decision rule:

- Invite many perspectives into discovery and critique.
- Assign one accountable decision owner for the final tradeoff.

### Speed and AI Generation vs Craft

Use AI to explore options, generate variants, summarize evidence, inspect screenshots, and accelerate repetitive production. Do not let speed become the design goal.

Nuance:

- Faster iteration is valuable only when the loop has good evaluation.
- Generated visuals can crowd out product thinking by looking more resolved than they are.
- Craft remains visible in edge cases, accessibility, copy, layout stability, and last-mile fit.

Decision rule:

- Use AI for breadth and mechanical acceleration.
- Use product context, user evidence, rendered verification, and expert critique for selection.

### Research Depth vs Shipping Speed

Use research depth when the decision is hard to reverse, high-risk, strategically central, or poorly understood. Use shipping speed when the change is low-risk, reversible, measurable, and the team can learn from real use.

Nuance:

- Usability science favors early user focus, empirical measurement, and iteration.
- Product cultures that prize shipping often learn fastest through prototypes and real usage.
- Both fail when the loop is weak: research can become theater, and shipping can become churn.

Decision rule:

- If the cost of being wrong is high, research before shipping.
- If the cost of being wrong is low and feedback is fast, ship a reversible version and measure.

### Accessibility vs Visual Novelty

Accessibility constraints beat novelty when they affect comprehension, operation, safety, or equal access. Visual novelty is welcome when it preserves semantics, focus, contrast, target size, assistive-tech behavior, and reduced-motion alternatives.

Nuance:

- A novel interface can still be accessible if its interaction model is explicit and testable.
- A conventional interface can still be inaccessible if labels, focus, contrast, or keyboard behavior are broken.

Decision rule:

- Preserve accessibility invariants first.
- Experiment with visual language only after the control remains operable, perceivable, understandable, and robust.

### Personalization vs Consistency

Use personalization when users differ meaningfully by role, expertise, locale, workflow, permissions, or repeated preferences. Preserve consistency for core navigation, safety states, command semantics, and shared collaboration surfaces.

Nuance:

- Personalization can reduce clutter and increase relevance.
- Excess personalization can make support, collaboration, learning, and documentation harder.
- AI-driven personalization needs transparency, reset controls, and privacy boundaries.

Decision rule:

- Personalize content, defaults, and shortcuts before changing core semantics.
- Give users inspection and reset paths when the system adapts behavior.

### Customer Love vs Business Constraints

Customer love is a strong design north star, but it cannot erase feasibility, reliability, accessibility, privacy, legal duties, or business survival.

Nuance:

- Craft cultures emphasize care in the last mile because users feel the accumulated details.
- Operational products must also protect throughput, performance, supportability, and predictable behavior.
- A delightful feature that increases support burden, privacy risk, or performance degradation may be a bad trade.

Decision rule:

- When customer love and business constraints conflict, search for a smaller expression of care that preserves trust and reliability.
- Do not ship delight that makes the core job slower, less accessible, less safe, or harder to support.

### Expert Testimony vs Current Product Evidence

Use expert testimony to generate hypotheses, frame tradeoffs, and avoid rediscovering known failures. Use current product evidence to decide what is true here.

Nuance:

- Expert advice can be strongly true in its original domain and wrong in a mismatched one.
- Product evidence can be misleading if instrumentation is poor, the sample is biased, or users have learned around a broken design.

Decision rule:

- If expert advice and current evidence conflict, inspect the product context, evidence quality, and user segment.
- Prefer a small test or reversible change over declaring either source universally right.

## Answering With Expert Evidence

When using expert testimonials in a response:

- Name whether the answer is based on consensus, a single expert, or a contextual rule.
- Cite or identify the expert and source when the user needs provenance.
- State applicability conditions.
- Preserve disagreement instead of forcing synthesis.
- Avoid long direct quotes; paraphrase unless exact wording matters.
- If source quality is weak, transcript attribution is uncertain, or evidence is thin, say so.

Default format for a conflict:

```text
Decision
Default rule
Why experts disagree
Use A when...
Use B when...
What evidence would change the decision
```

## Maintenance Rules

- Add new testimonials as L1 spans before writing theme summaries.
- Keep raw source text outside the skill unless it is short, licensed, and intentionally bundled.
- Do not merge across experts below L3.
- Mark transcript quality and source type.
- Version decision rules when evidence changes.
- Prune theme nodes that are vague, over-broad, or unsupported by spans.
