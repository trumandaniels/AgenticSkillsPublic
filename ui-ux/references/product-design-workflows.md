# Product Design Workflows

Use this reference for complex product surfaces, professional editors, dashboards, workbenches, and beta products where workflow design matters as much as visual polish.

## Core Principle

Organize the UI around the user's object of interest, not around a feature list. A strong product surface makes these questions obvious:

- What am I working on?
- What state is it in?
- What is selected or focused?
- What can I safely do next?
- How do I preview, undo, compare, or recover?

## Object Model First

Name the canonical unit of work before choosing layout:

- **Document**: sections, paragraphs, comments, suggestions, versions.
- **Canvas object**: frames, layers, selections, masks, transforms, properties.
- **Timeline object**: clips, tracks, playheads, ranges, markers, sequence state.
- **Workbench resource**: files, tabs, panels, search results, tasks, logs, extensions.
- **Operational record**: accounts, tickets, users, orders, tasks, filters, approvals.
- **Domain object**: the user's real object, constraint, validation state, and review state.

If the object cannot be named in one noun phrase, the information architecture is probably not ready.

## Layout Families

- **Document-centric**: command band, structure/navigation, central reading or writing surface, review/properties. Use for prose, reports, contracts, notes, and review-heavy workflows.
- **Canvas-centric**: tools/assets, layers or structure, central canvas, inspector/properties. Use for spatial composition, interface design, diagrams, image editing, and object manipulation.
- **Timeline-centric**: browser/source, viewer, timeline, inspector/meters. Use when sequencing and timing dominate.
- **Workbench-centric**: explorer/activity rail, editor, panels, status, command palette. Use when users move among many related resources.
- **Operational dashboard**: navigation, filters, dense tables/lists, detail side panel, bulk actions, status and audit signals. Use when scanning, comparison, and repeated action dominate.
- **Hybrid focus mode**: normal workspace plus contextual actions near the current object. Use to shorten common actions without making the whole UI visually dense.

Do not copy a famous product layout unless its primary object and workflow match the new domain.

## Golden Workflow Spine

For a beta or new tool, optimize 3-5 golden workflows end to end. A generic editor workflow:

1. Create or import the object.
2. Organize it into a clear structure.
3. Select an object, range, or record.
4. Manipulate with live preview.
5. Commit non-destructively or cancel.
6. Review, annotate, validate, or approve.
7. Export, publish, archive, or hand off.
8. Save a checkpoint or version.

For operational products, a generic workflow:

1. Find the relevant item through search, filters, or alerts.
2. Understand status, ownership, risk, and next action.
3. Compare or inspect details without losing list context.
4. Act individually or in bulk.
5. Confirm risky changes.
6. Verify outcome and preserve an audit trail.

## Persistent Structures vs Transient Commands

Keep persistent structures stable and inspectable:

- files, pages, layers, clips, tracks, records, comments, versions, filters, saved views.

Keep transient commands discoverable but visually subordinate:

- tools, modes, menus, quick actions, keyboard shortcuts, command search.

Confusion rises when transient controls masquerade as durable state, or when durable state is hidden behind temporary menus.

## Selection, Focus, and Scope

Selection is the center of the interaction model. Always make the scope of the next command visible:

- Show selected object/range/row/card in the surface.
- Show selected object's properties in one predictable place.
- Keep keyboard focus visually distinct from selection.
- Confirm only irreversible actions; make ordinary edits undoable.
- For multi-step edits, provide preview, commit, and cancel without losing context.

## Novice to Expert

Support dual-path operation:

- Provide a visible path for novices.
- Provide command search, shortcuts, saved presets, customization, or bulk actions for experts.
- Reveal accelerators in menus, tooltips, contextual bars, and command search.
- Teach only the next meaningful step; avoid front-loading the whole feature map.

## Beta Scorecard

For beta design reviews, score:

- Task success for top workflows.
- Time to first meaningful output.
- Recovery from mistakes and undo/restore success.
- Navigation dead ends, misclicks, and command search usage.
- p95 latency for select, drag, preview, save, export, and reopen.
- Review/collaboration flow completion when relevant.
- Shortcut or power-feature adoption by repeat users.
- Crash-free sessions, autosave recovery, and corrupted-state incidents.

Use the scorecard to decide what to simplify, not only what to add.
