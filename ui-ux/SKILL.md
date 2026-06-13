---
name: ui-ux
description: Design, critique, and refine user interfaces and product experiences for web apps, desktop apps, mobile layouts, dashboards, workflows, design systems, prototypes, and frontend implementation. Use when Codex needs to plan or improve UI/UX, review screens for usability and polish, translate product intent into interface structure, create interaction states, improve accessibility and responsive behavior, or make implementation guidance more visually and experientially coherent.
---

# UI / UX

## Overview

Use this skill to make product interfaces clear, useful, polished, and implementable. Treat UI and UX as a product-design problem first: understand the user's job, shape the workflow, then refine visual hierarchy, interaction, accessibility, and implementation details.

## Core Workflow

1. Identify the product surface, user, primary job, platform, and constraints.
2. Define the main workflow before styling individual components.
3. Prioritize the information architecture: what users must notice first, compare, change, confirm, or recover from.
4. Design states, not only the default view: loading, empty, error, partial, disabled, hover/focus, selected, success, destructive, and permission-limited states.
5. Check responsive behavior early. Specify how navigation, grids, tables, forms, modals, toolbars, and media adapt across small and large viewports.
6. Apply visual design with restraint: hierarchy, spacing, alignment, contrast, typography, color, motion, and affordances should support the task.
7. Verify accessibility basics: keyboard flow, focus visibility, labels, semantic structure, contrast, target size, reduced motion, and non-color-only signals.
8. When implementing, inspect the existing app's design system and component patterns before introducing new UI primitives.
9. Validate the result visually when possible with screenshots or browser inspection, especially after frontend changes.

## Design Guidance

- Start from the user's intent, not from decorative layout. Name the decision or action the screen is helping with.
- Make the primary action obvious, secondary actions available, and dangerous actions deliberate.
- Prefer direct manipulation and familiar controls: tabs for parallel views, menus for option sets, switches or checkboxes for binary choices, sliders or steppers for bounded numeric input, and icon buttons for compact tool actions.
- Keep dense operational tools scannable. Use calm surfaces, predictable navigation, compact controls, stable table/grid layouts, and clear filters rather than marketing-style composition.
- Use cards only for repeated items, modals, and genuinely framed tools. Avoid nested cards and page sections that look like floating cards.
- Choose typography by context. Use hero-scale type only for real heroes; use tighter headings inside dashboards, panels, sidebars, toolbars, forms, and cards.
- Keep color functional. Use semantic color for status and risk; avoid one-note palettes dominated by a single hue family unless the product already requires it.
- Make layout stable. Reserve dimensions for boards, toolbars, tiles, media, counters, buttons, and dynamic labels so hover states and data changes do not shift the interface.
- Use motion to clarify continuity or feedback, not to distract. Respect reduced-motion preferences.

## Review Checklist

When critiquing or revising a UI, look for:

- **Purpose**: The screen's job is obvious within a few seconds.
- **Hierarchy**: The most important content and action have clear priority.
- **Workflow**: Common paths are short; destructive or irreversible paths are guarded.
- **State coverage**: Empty, loading, error, success, and edge states are designed.
- **Responsiveness**: Content does not overlap, clip awkwardly, or rely on desktop-only assumptions.
- **Accessibility**: Interactive controls are labeled, keyboard-reachable, visible when focused, and not color-dependent.
- **Copy**: Labels are specific, brief, and action-oriented; helper text appears where decisions are made.
- **Consistency**: Components, spacing, radius, icons, and patterns match the surrounding product.
- **Polish**: Alignment, spacing, contrast, text wrapping, and visual rhythm feel intentional.

## Implementation Guidance

- Inspect existing files for component conventions, design tokens, CSS architecture, icon libraries, routing, and state management before editing.
- Reuse the local component system whenever it can express the design cleanly.
- Prefer semantic HTML and native controls before custom controls.
- Use stable responsive constraints such as `minmax`, `clamp` for spacing or container width, `aspect-ratio`, `min-width: 0`, explicit grid tracks, and predictable overflow behavior.
- Do not scale font size directly with viewport width. Use responsive layout and sensible type steps instead.
- Ensure text fits inside buttons, tabs, chips, cards, table cells, and panels at realistic content lengths.
- Add visible focus states and preserve keyboard interaction when restyling controls.
- If using icons, use the project's existing icon library. Use `lucide` when available and no local icon system exists.
- Validate with a real rendered view when practical. Check at least one desktop and one mobile viewport for frontend work with meaningful layout changes.

## Output Patterns

For a design proposal, include:

- `Goal`: what the interface must help the user do.
- `Structure`: the screen, navigation, and major regions.
- `Key interactions`: primary flows, controls, and state changes.
- `States`: loading, empty, error, success, and edge behavior.
- `Visual system`: layout, spacing, typography, color, iconography, and motion direction.
- `Accessibility`: keyboard, focus, labels, contrast, target size, and reduced-motion notes.

For a UI review, lead with findings ordered by severity. Reference exact screens, components, files, or line numbers when available, and include concrete fixes rather than vague taste preferences.

For implementation work, summarize what changed, where it changed, and how it was visually or functionally verified.

## Useful Prompts

- "Use $ui-ux to redesign this dashboard for faster scanning."
- "Use $ui-ux to review this settings page for usability issues."
- "Use $ui-ux to turn this product idea into an app layout."
- "Use $ui-ux to improve the responsive behavior and polish of this frontend."
- "Use $ui-ux to design the empty, loading, error, and success states for this workflow."
