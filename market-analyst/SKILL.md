---
name: market-analyst
description: Market analysis and opportunity evaluation for startups, new products, SaaS ideas, vertical software, AI tools, marketplaces, and other business concepts. Use when Codex needs to assess market attractiveness, competitive landscape, market openings and wedges, differentiation, customer and buyer understanding, GTM feasibility, pricing and revenue potential, defensibility, timing, execution feasibility, category strategy, or failure modes.
---

# Market Analyst

## Overview

Use this skill to evaluate whether a market or product idea is worth pursuing and where a small entrant can realistically win. Be evidence-seeking, direct, and decision-oriented: separate what is known, what is inferred, and what must be validated next.

For the canonical evaluation question bank, read `references/questions.md` when the user asks for a structured market analysis, due diligence memo, opportunity scorecard, competitive review, wedge search, GTM assessment, or failure-mode analysis.

## Core Workflow

1. Define the opportunity in one sentence: customer, painful job, current alternative, proposed product, and buyer.
2. Choose the relevant categories from `references/questions.md`; do not force every category when the user asks a narrow question.
3. Gather evidence before making confident claims when current market facts matter. Use recent primary or high-quality sources for market size, competitors, pricing, regulation, and news-sensitive claims.
4. Analyze from the entrant's perspective. A large market is not attractive unless there is a reachable customer segment, a credible wedge, and a reason incumbents or substitutes leave room.
5. Distinguish customers, users, economic buyers, influencers, and blockers. Name who feels pain and who pays.
6. Identify market openings with specificity: underserved segment, workflow gap, distribution advantage, regulatory shift, platform change, cost curve change, behavior change, or incumbent constraint.
7. Pressure-test the business model: acquisition motion, sales cycle, ACV or price point, gross margin, retention, expansion, implementation burden, and support load.
8. End with a clear recommendation, confidence level, biggest unknowns, and the next validation steps.

## Output Patterns

For a full market memo, use:

- `Verdict`: pursue, test narrowly, wait, or avoid.
- `Why now`: what changed and why the opportunity is open.
- `Best wedge`: the smallest specific customer segment and use case worth testing.
- `Competitive reality`: key incumbents, substitutes, and likely responses.
- `Buyer and GTM`: who pays, how to reach them, and what conversion friction exists.
- `Business quality`: pricing, margins, retention, expansion, and scale constraints.
- `Defensibility`: what advantage could compound if the entrant gets traction.
- `Failure modes`: what most likely kills the idea.
- `Validation plan`: the next 3-7 tests, ordered by risk reduction.

For a quick answer, use:

- `Short verdict`
- `Main reason`
- `Best next test`
- `Watch-out`

## Scoring Guidance

Use scores sparingly. When helpful, score each relevant category from 1 to 5 and explain the score in one sentence. Do not average scores mechanically; weight the decision around the user's goal, constraints, and stage.

Suggested interpretation:

- `5`: unusually strong evidence or favorable structure.
- `4`: promising with manageable risks.
- `3`: plausible but unproven or mixed.
- `2`: weak, crowded, hard to reach, or structurally unattractive.
- `1`: strong reason to avoid unless the premise changes.

## Evidence Discipline

When external facts are unstable, browse or otherwise verify. This includes current competitors, funding, pricing pages, market reports, legal or regulatory changes, platform rules, search trends, and recent news.

Label evidence quality:

- `Observed`: sourced fact, user-provided fact, or directly inspected artifact.
- `Inferred`: reasoned conclusion from observed facts.
- `Unknown`: material claim that still needs validation.

Prefer concrete market facts over generic business language. Replace broad claims like "large and growing market" with the actual segment, buyer urgency, budget source, and adoption friction.

## Useful Prompts

- "Evaluate this startup idea and tell me whether it is worth pursuing."
- "Map the competitive landscape and find a wedge for a small entrant."
- "Pressure-test the GTM and pricing for this product."
- "What would kill this idea?"
- "Should this be positioned in an existing category or as a new category?"
