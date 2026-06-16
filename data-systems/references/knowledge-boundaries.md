# Knowledge Boundaries

The skill should remember only guidance that is stable, reusable, and source-backed. Keep raw sources immutable and searchable; promote distilled doctrine only after review.

## Boundary Classes

- `workflow`: steps needed on nearly every use; belongs in `SKILL.md`.
- `doctrine`: reusable source-backed principles; belongs in `references/*.md`.
- `decision_node`: repeated branching logic; belongs in `decision/*.json`.
- `source_chunk`: immutable source evidence; belongs in `indexes/` or an external retrieval store.
- `example`: compact exemplar or anti-exemplar; belongs in `examples/*.jsonl`.
- `eval_fixture`: regression or forward-test task; belongs in `evals/*.jsonl`.
- `candidate_memory`: field lesson awaiting review; keep separate from doctrine.
- `omit`: low-reuse, unsupported, stale, or misleading content.

## Promotion Rules

Promote to doctrine only when all are true:

- The claim affects architecture decisions.
- The claim recurs across likely tasks.
- The claim has provenance or is accepted local operating doctrine.
- The claim can be phrased as a constraint, tradeoff, checklist item, or decision rule.

Do not promote:

- Vendor marketing copy without qualification.
- One-off implementation anecdotes.
- Generated recommendations without source support.
- Examples whose assumptions are not tagged.
- Temporary user preferences as global doctrine.

## Provenance Expectations

Future source-backed claims should store:

- `source_id`
- `version_or_edition`
- `heading_path`
- `anchor_id`
- `claim_type`
- `status`: `active`, `superseded`, `disputed`, or `contextual`
- `last_reviewed_at`

Contradictions should be represented as competing claims with context, not silently overwritten.
