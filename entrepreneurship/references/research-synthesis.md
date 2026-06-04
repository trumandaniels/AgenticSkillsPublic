# Research Synthesis

This file captures the design choices behind the `entrepreneurship` skill. It is not required for normal use. Read it when improving the skill, tightening the evaluator, or explaining why the structure is intentionally minimal.

## Core Design Choices

### 1. Keep the skill focused and compact

The strongest pattern in the skill research is that curated, focused skills outperform bloated or generic guidance. This skill therefore keeps the runtime surface small:

- one lean `SKILL.md`
- one primary operating reference: `decision-playbook.md`
- one evaluator loop: `feedback-loop.md`
- one routing file: `memory-map.md`

That structure follows the finding that procedural artifacts work best when they are explicit, modular, and easy to retrieve without drowning the agent in context.

### 2. Use progressive disclosure on purpose

The research repeatedly shows that skill effectiveness drops as retrieval gets noisier and context becomes more realistic. To counter that:

- the trigger description is broad enough to fire on real business questions
- the body stays short enough to remain useful in-context
- detailed logic moves into references that are loaded only when needed

This preserves context budget while keeping the deeper playbook available.

### 3. Treat evaluation like measurement, not vibes

The feedback-loop research argues that judges are measurement instruments and should not be trusted casually. This skill uses a simple judge checklist and explicit decision rules so the second pass can catch:

- generic advice
- false certainty
- poor stage fit
- missing assumptions
- weak instrumentation

The goal is not perfect objectivity. The goal is a cleaner, more reliable self-check.

### 4. Score the process, not just the conclusion

Outcome-only judgment is weak for business advice because polished language can hide weak reasoning. The skill therefore asks whether the recommendation:

- identified the real bottleneck
- considered alternatives
- matched the company's stage
- named assumptions and downside
- produced an executable next move

That reflects the research emphasis on process evaluation and trace-level observability.

### 5. Prefer reversible bets and explicit learning loops

In small startups, many decisions should be treated as bets under constraint rather than permanent strategy declarations. The playbook therefore gives extra weight to:

- time-to-learning
- reversibility
- founder focus cost
- direct customer signal

This reduces the chance of overcommitting to elegant but under-validated plans.

### 6. Avoid Goodhart traps

The feedback-loop research warns that once a score becomes the target, systems can optimize the proxy instead of reality. For a business skill, that means:

- do not optimize for vanity metrics alone
- do not recommend growth before value is retained
- do not confuse activity with validated demand
- do not let a scoring rubric replace judgment about the actual business

### 7. Encode operator priors from real founders, not just generic startup advice

The transcript set adds a second layer beyond the research reports: what experienced bootstrapped operators repeatedly optimize for in practice. Across the founder material, several patterns recur:

- choose products and segments where the team has real distribution access or community proximity
- get specific enough that the niche itself sharpens copy, referrals, and support load
- use pricing to shape customer quality and support burden, not just top-line revenue
- choose packaging that matches how customers consume value, not just whatever looks most like SaaS
- prefer simple products and simple motions because complexity taxes small teams twice, once in build cost and again in support cost
- diagnose growth through activation, messaging, and retention before reaching for more channels
- sometimes trade short-term conversion for faster learning by adding temporary high-touch onboarding for the segment that matters
- build documentation, process clarity, and delegation paths early because operational quality and sellability reinforce each other

That is why the skill now includes `problem-map.md`: the main gap was not more abstract guidance, but a reusable map from business problem -> required context -> acquisition method -> interpretation rules.

## Source Inputs

- `/mnt/c/Users/Truman/Downloads/OutsideInfo/Research/research-report-skill-optimization.md`
- `/mnt/c/Users/Truman/Downloads/OutsideInfo/Research/research-report-feedback-loops-agent-perception.md`
- `/mnt/c/Users/Truman/Downloads/OutsideInfo/Experts/Entrepreneurship/How to indie-hack to $600K ARR Jon Yongfook Cockle (Bannerbear).txt`
- `/mnt/c/Users/Truman/Downloads/OutsideInfo/Experts/Entrepreneurship/76 Distribution & Taste w Adam Wathan.txt`
- `/mnt/c/Users/Truman/Downloads/OutsideInfo/Experts/Entrepreneurship/How to Build and Sell an Audience-First Business with Arvid Kahl Mind Meld Podcast #33.txt`
- `/mnt/c/Users/Truman/Downloads/OutsideInfo/Experts/Entrepreneurship/Interview John O'Nolan, Co-Founder & CEO of Ghost, on staying true to your values, pricing, & more.txt`
- `/mnt/c/Users/Truman/Downloads/OutsideInfo/Experts/Entrepreneurship/How Baremetrics Used Transparency to Grow to $1.5M ARR.txt`
- `/mnt/c/Users/Truman/Downloads/OutsideInfo/Experts/Entrepreneurship/Build a Sellable Business with Andrew Gazdecki.txt`
- `/mnt/c/Users/Truman/Downloads/OutsideInfo/Experts/Entrepreneurship/How Tally bootstrapped to $100k MRR with a team of 3 With Marie Martens.txt`
- `/mnt/c/Users/Truman/Downloads/OutsideInfo/Experts/Entrepreneurship/Freemium, Content Marketing + Finding the Source of Your Best Customers with Ruben Gamez.txt`
- `/mnt/c/Users/Truman/Downloads/OutsideInfo/Experts/Entrepreneurship/From Zero to Millions Danny Postma Reveals AI App Strategies for Success.txt`
- `/mnt/c/Users/Truman/Downloads/OutsideInfo/Experts/Entrepreneurship/Optimizing Your Way to a Dream Exit.txt`
- `/mnt/c/Users/Truman/Downloads/OutsideInfo/Experts/Entrepreneurship/Building a $400kyear SaaS with Damon Chen — The Bootstrapped Founder #164.txt`
- `/mnt/c/Users/Truman/Downloads/OutsideInfo/Experts/Entrepreneurship/How to Run a Profitable One-person Internet Business Using AI - Ep. 14 with Ben Tossell.txt`
- `/mnt/c/Users/Truman/Downloads/OutsideInfo/Experts/Entrepreneurship/How I Built a 7-Figure Business in Less than A Year with AI Ben Tossell.txt`
- `/mnt/c/Users/Truman/Downloads/OutsideInfo/Experts/Entrepreneurship/Factory Ai Building an AI Startup With $0 on Marketing.txt`
- `/mnt/c/Users/Truman/Downloads/OutsideInfo/Experts/Entrepreneurship/How to Build & Sell a Startup – Workshop with Sahil Lavingia, Andrew Gazdecki and Ben Tossell.txt`
- `/mnt/c/Users/Truman/Downloads/OutsideInfo/Experts/Entrepreneurship/Bootstrapping a SaaS Product to $36k MRR(1).txt`
- `/mnt/c/Users/Truman/Downloads/OutsideInfo/Experts/Entrepreneurship/The AppSumo Treasure Trove with Ruben Gamez.txt`
- `/mnt/c/Users/Truman/Downloads/OutsideInfo/Experts/Entrepreneurship/Ruben Gamez — Cracking the E-Signature Market.txt`

## Intended Behavior

This skill should feel like a concise operator's brain:

- clarify the decision
- ask for the discriminating evidence
- surface tradeoffs
- recommend one path
- explain why now
- define what to watch
- create a clean next move
