# Problem Map

Use this file when the question is a real startup decision and the answer depends on gathering the right context instead of brainstorming harder.

## How To Use This File

1. Pick one primary problem.
2. Gather only the context that would change the recommendation.
3. Prefer observed behavior over founder opinion.
4. After classifying the problem, open `pattern-index.md` and load only the 1-2 matching files from `patterns/`.
5. If key facts are missing, say so and name the fastest way to collect them.

## Pattern Hints By Problem Type

- Double down, pivot, or kill -> `patterns/market-pull-probing.md`, `patterns/audience-first-discovery.md`
- Choose the right ICP, audience, or segment -> `patterns/audience-first-discovery.md`, `patterns/distribution-plus-taste.md`
- Decide what to build next -> `patterns/simplicity-before-surface-area.md`, `patterns/temporary-friction-for-learning.md`
- Price, package, and choose the right monetization motion -> `patterns/pricing-for-customer-quality.md`, `patterns/free-surface-as-distribution.md`, `patterns/open-source-convenience-layer.md`
- Pick a distribution or go-to-market motion -> `patterns/launch-where-buyers-already-are.md`, `patterns/intent-led-content-and-seo.md`, `patterns/distribution-plus-taste.md`
- Diagnose a growth stall -> `patterns/temporary-friction-for-learning.md`, `patterns/simplicity-before-surface-area.md`
- Improve activation, onboarding, and retention -> `patterns/temporary-friction-for-learning.md`, `patterns/simplicity-before-surface-area.md`
- Manage simplicity, support, and operational load -> `patterns/simplicity-before-surface-area.md`, `patterns/founder-light-operations.md`
- Hire, delegate, or automate -> `patterns/founder-light-operations.md`
- Build a sellable, founder-light business -> `patterns/founder-light-operations.md`

These patterns show up repeatedly across the transcript set:

- Distribution is part of the product decision. If the team cannot reliably reach the buyer, that is not a "later marketing problem."
- Pricing changes customer type, support burden, and seriousness. It is not only a revenue lever.
- Simplicity compounds for small teams by reducing support, onboarding friction, and operational drag.
- Audience and community proximity are strong advantages when they reveal real pain and real language.
- It is sometimes rational to trade short-term conversion for faster learning, but only when the question is specific and the learning window is short.
- Growth usually breaks earlier in messaging, activation, or retention than founders first assume.
- Good documentation, process clarity, and low founder dependence make a business both easier to run and easier to sell.
- Product Hunt is usually amplification, not validation.
- Freemium works best when free usage creates more distribution or materially improves activation.
- Low prices can buy the wrong customers and overload support.
- Packaging should match how the customer wants to buy and consume value, not just the default SaaS subscription template.
- Support is often the first leverage hire in a growing bootstrapped SaaS.
- Documentation can be a growth asset for technical products, but it should not be used to hide a confusing UX.

## Evidence Hierarchy

Default evidence order:

1. retained usage, revenue, and expansion behavior
2. repeated customer interviews, sales calls, and churn reasons
3. attribution, funnel, and search-demand analytics
4. founder intuition, competitor moves, and market narrative

Do not let polite interest, vanity traffic, or broad trend excitement outrank retained customer behavior.

## 1. Double Down, Pivot, Or Kill

Use for:
- "Should we keep investing in this product?"
- "Should we pivot?"
- "Is this worth going all in on?"

Context to gather:
- 3-6 month trend in active usage, paid conversions, revenue, and churn
- the strongest repeated use case and who pays for it
- founder-product fit or unfair advantage
- current channel access or audience edge
- support burden and complexity required to keep growing

Acquire it by:
- reviewing cohorts, activation rates, and revenue trend
- reading the last 10-20 churn, trial-loss, and support conversations
- listing concrete customer use cases and who asked for them
- checking whether any segment already pulls the product without heavy persuasion

Interpret it like this:
- double down when there is repeated usage, a clear payer, and a believable channel to reach more of them
- pivot when there is signal, but it is concentrated in a different segment, use case, or activation model than the current one
- kill or pause when usage is shallow, customer pull is vague, and the team has no distribution edge that would rescue the bet
- do not count sunk cost, compliments, or one-off enthusiasm as evidence

## 2. Choose The Right ICP, Audience, Or Segment

Use for:
- "Who should we serve?"
- "Should we narrow our ICP?"
- "Should we build for developers, marketers, agencies, or enterprise?"

Context to gather:
- who uses the product, who pays, who retains, and who refers
- current workaround and urgency for each segment
- ACV, retention, and support cost by segment
- whether the founder already has audience, trust, or community access with one segment
- language the best customers naturally use to describe the problem

Acquire it by:
- breaking revenue, expansion, and churn down by segment
- interviewing best customers and recent lost deals
- reviewing support tickets and sales notes by segment
- observing communities where these customers already talk: niche Slack, Discord, Reddit, forums, or email lists

Interpret it like this:
- prefer the segment with painful, frequent problems, clear willingness to pay, reachable distribution, and tolerable support cost
- if an audience exists but the pain is weak, that is still weak demand
- if the pain is real but the team cannot reach that segment repeatedly, distribution risk belongs in the decision
- narrow before broadening when the product, messaging, or channel still feels mushy

## 3. Decide What To Build Next

Use for:
- "What should we build next?"
- "Should we add this feature?"
- "How do we prioritize roadmap work?"

Context to gather:
- core activation and retention bottlenecks
- repeated requests from best customers, not just loud users
- features or missing capabilities correlated with churn, stalled onboarding, or expansion
- current complexity and support cost of the product
- whether the request sharpens the core use case or dilutes it

Acquire it by:
- checking product analytics for dropoff and successful paths
- tagging feature requests by customer type and revenue tier
- reading churn reasons, support tickets, and sales objections
- comparing retained customers against poor-fit customers asking for extras

Interpret it like this:
- prioritize work that improves activation, retention, expansion, or speed-to-value for the best customers
- deprioritize requests from poor-fit users or low-value edge cases
- choose features that deepen the strongest use case over features that broaden the product without clear demand
- complexity is a real cost; every feature should earn its place through revenue, retention, or decisive learning

## 4. Price, Package, And Choose The Right Monetization Motion

Use for:
- "Should we raise prices?"
- "Should we do freemium?"
- "Should this be self-serve, sales-assisted, or enterprise?"

Context to gather:
- current conversion, retention, expansion, and churn by plan or entry path
- support and infrastructure cost by customer type
- time-to-value and how much help customers need to succeed
- evidence of willingness to pay and price sensitivity
- whether the product has a built-in viral or PLG loop
- whether the value is consumed continuously, in bursts, or as an expanding library of assets
- whether an LTD or AppSumo-style offer would create reviews, distribution, or advocacy, not just cash

Acquire it by:
- comparing plan-level cohorts and support load
- reading win-loss notes, churn reasons, and pricing objections
- reviewing onboarding data to see whether customers succeed alone or need help
- running pricing or packaging tests when traffic volume allows it

Interpret it like this:
- pricing is a customer filter; lower prices can increase volume while degrading support economics and customer quality
- freemium works best when free users help create more users or when marginal cost and support load stay low
- choose a sales motion that matches ACV and implementation complexity
- optimize activation model for retained customers, not raw leads, demo volume, or trial starts
- if the product is naturally shared, a free plan can keep the loop alive better than a trial
- if the product is not naturally shared and support cost is real, default away from freemium
- if the product is a library, education, or resource membership, a one-time or annual model can fit buyer behavior better than monthly nagging
- if considering LTDs, require low variable cost, explicit limits, a usable plan, and a clear reason beyond cash

## 5. Pick A Distribution Or Go-To-Market Motion

Use for:
- "Should we do content, SEO, outbound, partnerships, or Product Hunt?"
- "What channel should we focus on?"
- "How do we launch this?"

Context to gather:
- where the target customer already pays attention
- the team's actual strengths, audience, credibility, and channel access
- previous channel results tied to activated and retained customers
- time, cash, and skill required for each channel
- whether messaging and onboarding are already strong enough to support new traffic

Acquire it by:
- checking channel-to-activation-to-retention attribution
- listing existing assets: audience, community access, brand, SEO footprint, integrations, partners
- reviewing prior experiments for cost, time-to-signal, and quality of users
- checking search demand and keyword difficulty when SEO is in the option set

Interpret it like this:
- choose repeatable channels the team can sustain, not the cleverest channel on paper
- existing audience or distribution advantage often beats an abstract "best practice" channel
- content and SEO work when tied to real customer questions and when the product can capture that intent
- if messaging, activation, or retention are weak, new channels will mostly amplify the weakness
- Product Hunt is best used once the product already has signal, users, and some proof that people care
- launch where the audience already is, not where founders like to talk about launching

## 6. Diagnose A Growth Stall

Use for:
- "Why are we not growing?"
- "What is the bottleneck?"
- "Should we get more traffic or fix the product?"

Context to gather:
- acquisition, activation, retention, expansion, and churn by cohort
- traffic-to-signup-to-paid conversion
- churn timing and the top reasons people fail to stick
- segment mix and plan mix
- whether new customers behave differently from existing best customers

Acquire it by:
- building or reading a simple funnel and cohort dashboard
- reviewing the last 90 days of churn, failed onboarding, and lost deals
- separating metrics by segment and acquisition channel
- watching support volume and categories for repeated friction

Interpret it like this:
- identify the single constraint first instead of calling everything "growth"
- weak activation or retention usually outrank new channel testing as the main bottleneck
- optimize for customers and retained revenue, not just leads, clicks, or trial volume
- if a segment acquires well but churns quickly, the issue is often fit, promise, or onboarding rather than top-of-funnel

## 7. Improve Activation, Onboarding, And Retention

Use for:
- "How do we reduce churn?"
- "How do we improve onboarding?"
- "Should we change free trial, freemium, demo, or self-serve onboarding?"

Context to gather:
- time to first value
- behaviors correlated with long-term retention
- top early dropoff points
- churn reasons and when they appear
- expansion or upsell triggers among healthy accounts
- whether the team has a specific unanswered question that warrants a temporary high-touch or segmented onboarding flow

Acquire it by:
- comparing retained users with churned users
- reviewing onboarding sessions, support conversations, and setup friction
- interviewing recent churned and newly successful customers
- mapping the first 30-90 days by segment

Interpret it like this:
- shorten time to value and make the core outcome obvious
- solve early confusion before chasing upsells
- churn in a specific segment can indicate wrong ICP, wrong promise, or wrong activation model
- use the first 90 days as the main proving window for whether onboarding really works
- if the main problem is ignorance rather than volume, temporarily add friction for the segment you need to understand and treat the lost signups as research cost

## 8. Manage Simplicity, Support, And Operational Load

Use for:
- "Should we add this complexity?"
- "Why is support overwhelming us?"
- "How do we stay lean with a small team?"

Context to gather:
- support volume, categories, and response burden
- repetitive manual work and founder interruptions
- bugs, reliability issues, and workflow complexity
- feature sprawl and how often advanced features are actually used
- documentation quality for users and team

Acquire it by:
- categorizing the last 50 support interactions
- listing repeated manual tasks and how often they occur
- reviewing usage of advanced features and the incidents they create
- checking whether docs or product changes could remove recurring tickets

Interpret it like this:
- simplicity is strategic leverage for small teams, not aesthetic minimalism
- recurring support pain is often a product, docs, or scope problem before it is a hiring problem
- avoid features that create disproportionate support debt for unclear upside
- document and automate repeated work after the founder understands it deeply enough to standardize it
- do not use documentation as a substitute for fixing a confusing core workflow
- if the product is technical, docs and support can also be part of the acquisition strategy

## 9. Hire, Delegate, Or Automate

Use for:
- "Who should we hire next?"
- "Should we delegate support?"
- "What should stay with the founder?"

Context to gather:
- founder time split for the last 1-2 weeks
- tasks only the founder can do versus tasks someone else can own
- runway and expected ROI of a hire
- process clarity and documentation quality
- operational pain caused by the current bottleneck

Acquire it by:
- doing a simple founder time audit
- listing recurring tasks, who currently owns them, and what breaks if they slip
- checking whether the process is already repeatable enough to hand off
- mapping which tasks are learning-rich and which are repetitive

Interpret it like this:
- the founder should stay close to customers and signal-rich work until the pattern is understood
- first leverage often comes from support or operations handoff once the process is documented
- do not hire to mask fuzzy process, weak product, or avoidable complexity
- automation works best on repetitive, measurable workflows with clear failure cases
- support is often the best first hire once growth creates real inbound pain
- do the role long enough to understand what great looks like before hiring a leader for it

## 10. Build A Sellable, Founder-Light Business

Use for:
- "How do we make this business sellable?"
- "How do we reduce founder dependence?"
- "What would a buyer care about?"

Context to gather:
- how much revenue, knowledge, or trust is tied to the founder personally
- documentation for operations, customer support, and reporting
- profitability, predictability, and segment clarity
- team ownership and who can run the business day to day
- financial, legal, and diligence hygiene

Acquire it by:
- asking what breaks if the founder disappears for 30 days
- reviewing SOPs, help center docs, reporting, and key-person dependencies
- doing a mock buyer diligence pass
- checking whether revenue and support quality survive without constant founder intervention

Interpret it like this:
- a good business is usually a sellable business
- documentation, profitability, trust, and low founder dependence expand strategic options
- a business that cannot operate without the founder has an operating problem before it has an exit problem
- make the business easier to run first; sellability often follows
- small, simple, profitable products can be highly sellable even without large teams
- use a 30-day founder absence test to find the real key-person dependencies
