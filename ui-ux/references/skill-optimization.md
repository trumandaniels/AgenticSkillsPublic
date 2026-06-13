# Skill Optimization

Use this reference when improving the `ui-ux` skill, testing whether guidance helps, creating design-evaluation prompts, or deciding whether to add more references, scripts, examples, or assets.

## Contract First

Before editing the skill, define the contract:

- What inputs should trigger the skill?
- What outputs should it produce?
- What workflow steps must happen?
- What behavior is forbidden?
- What should be checked deterministically?
- What needs visual, judge, or human review?
- What is the release gate?

For this skill, the core contract is: produce UI/UX guidance or implementation that is grounded in the actual product context, improves user workflow clarity, covers important states, respects accessibility and responsiveness, and is visually verified when implementation changes are meaningful.

## Keep the Skill Focused

Prefer focused modules over comprehensive manuals:

- Keep `SKILL.md` as the concise router and default workflow.
- Put deeper material in references that are loaded only when relevant.
- Add scripts only for checks that must be deterministic or repeated.
- Prune examples or rules that do not improve behavior in test prompts.
- Avoid turning the skill into a general design textbook.

## Suggested Evaluation Cases

Maintain representative prompts such as:

- Redesign a dense SaaS dashboard for faster scanning.
- Review a settings page for hierarchy, states, and accessibility.
- Turn a product idea into an app layout with object model and golden workflows.
- Improve a frontend implementation with screenshots at desktop and mobile widths.
- Design empty, loading, error, and success states for an AI-assisted workflow.
- Critique an editor/workbench UI for selection scope, command discovery, undo, and review state.
- Evaluate a design proposal against user evidence and product constraints.

## Dataset Splits

For serious optimization, keep:

- `dev_golden`: representative design tasks and good target traits.
- `dev_negative`: generic, decorative, or workflow-blind outputs to beat.
- `dev_adversarial`: ambiguous briefs, conflicting constraints, tiny screens, long labels, and misleading screenshots.
- `locked_regression`: fixed cases rerun on every skill change.
- `holdout`: unseen cases used only for milestone decisions.
- `judge_calibration`: human-labeled examples if using LLM judges.

## Evaluation Stack

Use hybrid evaluation:

- Deterministic: syntax, required files, no placeholders, accessibility tooling, contrast, layout overflow checks, screenshot existence, test/build success.
- Visual: desktop/mobile screenshots, no incoherent overlap, correct framing, realistic density, text fit.
- Rubric: workflow clarity, object model, state coverage, information hierarchy, accessibility, implementation fit, restraint, polish.
- Human/expert: taste, domain fit, trust, and whether the interface feels usable.

For frontend changes, visual verification is part of the release gate when a local rendered target is available.

## Rubric

Score or review these dimensions:

- **Context grounding**: uses the actual app, user, constraints, and component system.
- **Object model**: names the primary object and persistent structures.
- **Workflow**: optimizes real user paths rather than surface decoration.
- **State coverage**: includes loading, empty, error, success, disabled, selected, and destructive states when relevant.
- **Accessibility**: preserves semantic controls, labels, focus, keyboard use, contrast, and target size.
- **Responsiveness**: handles mobile and desktop without overlap, clipping, or unstable layout.
- **Visual hierarchy**: directs attention clearly and avoids ornamental noise.
- **Implementation sympathy**: matches the repo's design system, tokens, components, and constraints.
- **Verification**: includes screenshots, tests, or concrete inspection notes where practical.

## Failure Modes

Watch for:

- Pretty but workflow-blind screens.
- Marketing-page treatment for operational tools.
- Missing states beyond the happy path.
- Unclear selection scope or destructive action scope.
- Text that clips or buttons that resize the layout.
- Generic accessibility claims without keyboard/focus implications.
- New components that ignore the existing system.
- Overloaded `SKILL.md` content that would be better as a reference.
- Evaluation by taste alone with no task, state, or evidence criteria.

## Promotion Gate

Promote a skill revision only when:

- It validates structurally.
- It improves or preserves locked regression behavior.
- It does not bloat the root skill with rarely used detail.
- It gives clearer routing to references.
- It avoids regressions in frontend implementation guidance.
- Any new script or checker has been run successfully.
