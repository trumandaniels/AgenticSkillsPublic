# Validation

Validate architecture recommendations by testing whether the design is actionable, traceable, and resilient under failure.

## Recommendation Checks

- Does the answer state assumptions before recommendations?
- Does it identify canonical data owners and derived stores?
- Does it describe write paths, read paths, propagation, and consistency?
- Does it include failure modes and recovery plans?
- Does it separate required decisions from optional enhancements?
- Does it avoid vendor choice before workload shape is clear?
- Does it include data-quality and observability checks?

## Retrieval And Doctrine Checks

Use these when source indexes or doctrine files are involved:

- Retrieved evidence must match the decision context, not only keywords.
- Source anchors must support the claim being made.
- Examples must be compatible with the workload and constraints.
- Contradictory source claims must be surfaced with context.
- Missing source support should be marked as inference.

## Eval Dimensions

For forward-testing this skill, score:

- Context gathering quality.
- Branch-selection quality.
- Tradeoff clarity.
- Unsupported synthesis rate.
- Failure-mode coverage.
- Operational completeness.
- Citation/provenance quality when sources are used.

Prefer task-level evaluation over recall-only tests.
