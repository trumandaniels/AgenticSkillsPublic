---
name: entrepreneurship
description: Provide startup and SaaS decision support for small software businesses. Use when Codex needs to choose or critique product strategy, pricing, packaging, freemium, content or SEO strategy, launch motion, customer segment focus, support model, feature prioritization, growth experiments, or founder tradeoffs. Best for ambiguous business questions where the user needs a recommendation, explicit assumptions, downside analysis, metrics, and the next highest-leverage move instead of generic startup advice. Also use when the user asks what successful bootstrapped founders actually did, wants transcript-grounded examples, or says "be more specific" about a startup or software-business decision.
---

# Entrepreneurship

Make decisions like an operator protecting runway, focus, and learning rate. Favor customer truth, distribution reality, and reversible bets over elaborate theory.

## Quick Start

1. Reconstruct the business context: stage, product, buyer, traction, constraints, and the actual decision.
2. Read `references/memory-map.md` first when the request is non-trivial or touches several decision types.
3. Read `references/problem-map.md` to find the matching startup problem and gather only the context that will change the answer.
4. Read `references/pattern-index.md` and load only the 1-2 matching files under `references/patterns/`.
5. Read a matching founder card under `references/founders/` only when a named example or source-specific constraint will sharpen the recommendation.
6. Read `references/decision-playbook.md` before making meaningful product, pricing, positioning, go-to-market, retention, or operating recommendations.
7. Turn the question into a clear decision statement with options, constraints, and a time horizon.
8. Compare options on customer pain, speed to learning, distribution feasibility, revenue or retention impact, reversibility, and operational burden.
9. Prefer the smallest decisive next move when evidence is weak, and say exactly what context to collect next if the recommendation depends on it.
10. Run `references/feedback-loop.md` when the decision is high-stakes or the answer feels generic, overconfident, or under-instrumented.
11. Return a recommendation, why it wins now, key assumptions, main risks, what to measure, the immediate next step, and when helpful the named founder move plus the exact part to copy and the exact part not to cargo-cult.

## Runtime Architecture

Use the interview corpus as a pattern system, not a quote dump.

- Router: `memory-map.md` and `problem-map.md`
- Decision pattern library: `pattern-index.md` and `references/patterns/*.md`
- Founder-specific nuance: `references/founders/*.md`
- Output discipline: `decision-playbook.md`
- Quality control: `feedback-loop.md`
- Ingestion workflow for new interviews: `interview-extraction-template.md`

Default runtime order:
- classify the decision
- load 1-2 matching patterns
- load 0-1 founder cards only if they materially change the call
- make the recommendation
- run the feedback loop if needed

## Workflow

### 1. Rebuild the operating context

Capture or infer:
- stage: idea, pre-PMF, early PMF, growth, or unclear
- product and the job it helps customers do
- target customer, buyer, user, and current workaround
- traction signals: usage, pipeline, revenue, retention, churn, win-loss, or direct customer pull
- resources: runway, team size, founder time, technical constraints, channel access
- current bottleneck
- decision deadline
- downside if the recommendation is wrong

If key context is missing, make explicit assumptions and lower confidence.

### 2. Classify the decision before solving it

Use one primary decision bucket:
- product focus and roadmap
- pricing, packaging, and monetization model
- ICP, audience, positioning, and messaging
- acquisition, distribution, and go-to-market
- activation, onboarding, and retention
- simplicity, support, hiring, and operating cadence
- sellability and founder dependence

Do not blend several separate decisions unless they are tightly coupled.

After classifying the decision, load the matching checklist from `references/problem-map.md`, then load the smallest relevant pattern file or two from `references/patterns/`.

### 3. Turn the question into a real decision

State:
- the objective
- the options being compared
- the key constraint
- the evidence that matters most
- the time horizon
- what would count as success or failure

If the user asks an open-ended question, rewrite it internally as: "Choose X over Y because Z under constraints A and B."

### 4. Gather the context that actually changes the answer

Default evidence sources:
- product analytics and cohort retention
- sales notes, win-loss, and churn reasons
- support tickets and onboarding friction
- pricing, plan, and expansion data
- channel attribution and search demand
- direct customer conversations

Evidence order:
- observed behavior and retained revenue
- repeated customer language and interviews
- attribution and usage analytics
- founder intuition and market narrative

Prefer direct evidence from real customers over abstract market theory.

### 5. Evaluate options with startup lenses

Default lenses:
- customer pain and urgency
- strength of existing demand or distribution access
- expected impact on retention, revenue, or learning
- cost in cash, time, and founder attention
- reversibility
- strategic fit with the current stage
- operational load and support burden
- concentration risk and downside severity

In high uncertainty, give extra weight to time-to-learning and reversibility.

### 6. Match the decision to real operator patterns

Before recommending a move, check for a strong pattern match in `references/patterns/`.

Borrow a pattern only when:
- buyer behavior matches
- channel structure matches
- cost structure matches
- stage and team constraints match

If no pattern clearly fits, fall back to `references/decision-playbook.md` and recommend a smaller test rather than forcing a founder analogy.

### 7. Prefer learning-efficient moves

When evidence is weak:
- choose the cheapest test that can disconfirm the key assumption
- preserve runway and founder attention
- avoid changing too many variables at once
- prefer direct customer signal over proxy metrics

When evidence is strong:
- commit clearly
- define the review point
- instrument success and failure

### 8. Return decision-useful output

Default deliverable:
- recommendation
- why this option wins now
- rejected alternatives and why
- assumptions and confidence level
- biggest risks
- metrics and review window
- immediate next step
- if a founder pattern fits, the founder name, the exact trigger that makes it fit, and the non-obvious constraint that made the move work
- if key evidence is missing, the top three facts to gather next and the fastest way to get them

## Reference Files

- `references/memory-map.md`: what to load, when to load it, and which source material supports which part of the skill
- `references/problem-map.md`: recurring startup decision types, the context each one needs, how to acquire it, and how to interpret it
- `references/pattern-index.md`: chooser for the pattern library; maps decisions to the smallest relevant pattern files
- `references/patterns/`: one file per reusable founder-tested business pattern with fit conditions, failure modes, and what to copy versus not copy
- `references/founders/`: one file per founder with context, signature moves, misuse risk, and source interviews
- `references/decision-playbook.md`: core startup and SaaS decision workflow, scoring lenses, red flags, and output template
- `references/feedback-loop.md`: clean creator-judge loop for improving a recommendation without muddying evaluation
- `references/interview-extraction-template.md`: canonical structure for turning a new interview into reusable patterns instead of another raw summary
- `references/research-synthesis.md`: compact rationale distilled from the user's research on skill structure and feedback loops
- `references/operator-patterns.md`: legacy synthesis file kept for maintenance and broad cross-pattern review
- `references/founder-casebook.md`: legacy synthesis file kept for maintenance and comparison across founders
- `references/goldmine-playbooks.md`: legacy synthesis file kept for maintenance and deeper corpus review

## Working Rules

- Optimize for survival, focus, and validated learning.
- Tie recommendations to stage, constraints, and available evidence.
- Prefer narrow, specific bets over broad startup cliches.
- Separate reversible tests from irreversible commitments.
- Treat distribution as part of product strategy, not a post-hoc marketing task.
- Treat pricing as segmentation and support-load design, not just monetization.
- If recommending freemium or free tools, name the exact built-in loop that makes free worthwhile.
- If recommending content, name the buyer pain, the asset type, the intent level, and the channel or source it should target.
- If recommending growth, say whether the path assumes market pull, distribution leverage, or brute-force acquisition.
- If recommending a founder pattern, say which exact founder move fits, what condition made it work there, and what would make it fail here.
- If the differentiator is technical, translate it into buyer language before recommending how to position it.
- If using an interview-grounded example, say what to copy and what not to copy.
- Fix retention and activation before scaling acquisition when usage is weak.
- Prefer simplicity when small-team leverage or support burden is a constraint.
- Do not recommend motions that require distribution, cash, or team capacity the business does not have.
- When a founder-tested pattern clearly fits, say so plainly and explain why it fits this case.
- Do not cargo-cult famous founder tactics; only reuse patterns when the product mechanics and buyer behavior actually match.
- When a founder pattern fits, name the founder and the exact trigger that makes it fit this case.
- When recommending a calm-business path, define what "enough" means in revenue, complexity, team size, and founder lifestyle terms.
- Name tradeoffs explicitly.
- Say "not yet" when the right move is to delay or avoid a commitment.
- Never fake market evidence, certainty, or customer understanding.

## Example Triggers

- "Help me decide what this SaaS should do next."
- "Pressure-test this startup idea like an operator."
- "Should we narrow our ICP or add more features?"
- "Pick between outbound, content, partnerships, or PLG for this product."
- "Tell me if this pricing change is smart or premature."
- "Audit this founder plan for focus, leverage, and risk."
- "Turn this messy business question into a decision and next experiment."
