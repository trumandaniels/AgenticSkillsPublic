# UI Audit Passes

Use this reference when the user asks for auditable UI/UX practices, automated checks, package recommendations, or verification passes before finalizing frontend work.

Automated UI/UX audits are partial but useful. They can catch many accessibility, semantic HTML, performance, best-practice, and visual-regression issues, but they cannot prove that an interface is usable, understandable, inclusive, or polished. Pair them with manual UX review, keyboard checks, screen-reader smoke tests, responsive inspection, and user/task evidence when risk is meaningful.

## Install And Run Policy

- Do not install audit packages into this skill. Install tooling in the target project only, after the user approves the dependency and any generated config.
- Prefer existing project scripts and dependencies before adding new packages.
- Prefer project-local dev dependencies over global installs when practical.
- Ask before creating screenshot baselines, changing CI config, adding report uploads, or running slow audits.
- If a tool needs a local server, build, auth state, or production-like route, state that dependency before running the audit.

## Ask Before Running

When a frontend can be rendered or a target URL exists, offer this prompt:

```text
Optional UI audit passes are available for this app. Do you want me to run any now? I can run:
1. Accessibility scan with axe/Playwright or Pa11y.
2. Lighthouse performance, accessibility, best-practices, and SEO audit.
3. Visual screenshot regression with Playwright.
4. Component accessibility checks with Storybook a11y or jest-axe.
5. Keyboard/focus/responsive manual smoke check.

Running install commands may add dev dependencies or config files; I will ask before installing or changing project files.
```

## Audit Selection Matrix

- Static design critique only: no package install. Use the review checklist plus manual accessibility and workflow reasoning.
- Existing Playwright project: add `@axe-core/playwright` for rendered-page accessibility and use Playwright screenshots for visual regression.
- Storybook project: add `@storybook/addon-a11y` and use story-level a11y checks for component states.
- Jest, React Testing Library, or DOM unit tests: add `jest-axe` for component-level accessibility assertions.
- JSX/React codebase with ESLint: add `eslint-plugin-jsx-a11y` for static semantic and ARIA linting.
- Public URL or runnable local server: run Lighthouse or Lighthouse CI for page-level performance/accessibility/best-practices signals.
- Route list or sitemap available: use Pa11y or Pa11y CI for repeatable page accessibility scans.
- Visual redesign or layout-sensitive work: use Playwright screenshot comparisons, plus manual desktop/mobile inspection.

## Optional Audit Passes

### Rendered Accessibility With Playwright And Axe

Use for page states that can be opened in a browser. This catches issues such as missing labels, color contrast, duplicate IDs, invalid ARIA, and WCAG-tagged rule violations.

Typical project install, after approval:

```bash
npm install --save-dev @playwright/test @axe-core/playwright
npx playwright install
```

Recommended use:

- Scan representative routes and states, not only the home page.
- Prefer WCAG A/AA tags for release gates.
- Treat violations as evidence to inspect, not as the full accessibility story.
- Add manual keyboard and screen-reader smoke checks for high-risk flows.

### Pa11y Or Pa11y CI

Use for quick URL-based accessibility scans or CI checks across a page list. Pa11y CLI is good for one-off page checks; Pa11y CI is better when there is a stable list of URLs.

Recommended use:

- Start with public or unauthenticated routes.
- Add authenticated routes only when test auth is available and safe.
- Record the route list and thresholds so repeated runs are comparable.

### Storybook Accessibility

Use when components and states already live in Storybook. The `@storybook/addon-a11y` addon runs axe-based checks against stories and can report violations, passes, and incomplete checks.

Typical install, after approval:

```bash
npx storybook add @storybook/addon-a11y
```

Recommended use:

- Cover disabled, loading, error, selected, empty, and overflow states as stories.
- Use `parameters.a11y.test: 'todo'` for known issues during migration and `'error'` for CI-blocking checks once stable.

### Jest-Axe

Use for unit or component tests where the rendered DOM is available in JSDOM.

Typical install, after approval:

```bash
npm install --save-dev jest jest-axe jest-environment-jsdom
```

Recommended use:

- Pair with React Testing Library or the project's existing component renderer.
- Assert `toHaveNoViolations()` on meaningful component states.
- Do not rely on it for color contrast; axe color-contrast checks do not work in JSDOM.

### JSX Accessibility Linting

Use `eslint-plugin-jsx-a11y` in React/JSX projects to catch static semantic, alt-text, ARIA, interaction, and label issues before runtime.

Recommended use:

- Use the plugin's recommended config first; strict rules can be adopted after existing issues are understood.
- Configure component mapping when design-system components wrap native controls.
- Treat lint as a fast early gate, not a substitute for rendered accessibility testing.

### Lighthouse And Lighthouse CI

Use Lighthouse for page-level performance, accessibility, best-practices, and SEO signals. Use Lighthouse CI when the project has a build and server/static output suitable for repeatable CI audits.

Recommended use:

- Run against production-like builds when possible.
- Start with reporting before strict CI gates if the project has not tracked performance before.
- Add assertions once the team understands the baseline.
- Avoid public report uploads for private products unless the user explicitly approves.

### Playwright Visual Regression

Use Playwright screenshot comparisons for UI changes where layout, spacing, wrapping, or component composition could regress.

Recommended use:

- Capture stable states with deterministic data and disabled flaky animations where possible.
- Keep the browser, OS, viewport, and fonts consistent across runs.
- Review and commit baselines intentionally; do not blindly update snapshots.

### Manual Smoke Checks

Run these even when automated checks pass:

- Keyboard-only traversal reaches every control in a sensible order.
- Focus indicators are visible and not clipped.
- Screen reader names for key controls are meaningful.
- Text does not overlap, clip, or overflow at mobile and desktop viewports.
- Interactive targets are large enough and not crowded.
- Color is not the only signal for status or validation.
- Reduced-motion preferences are respected.
- Loading, empty, error, and success states are understandable without surrounding explanation.

## Limits To State Clearly

- Automated accessibility scans catch only a subset of WCAG and usability issues.
- Lighthouse scores are signals, not a UX quality score.
- Screenshot tests can be flaky across operating systems, browsers, fonts, and animation states.
- Component tests do not prove full workflow accessibility.
- Static linting cannot see runtime state, rendered styling, or dynamic content.
- Authenticated, personalized, or data-heavy apps need representative fixtures before audits are meaningful.

## Source Links

- Playwright accessibility testing: https://playwright.dev/docs/accessibility-testing
- Playwright visual comparisons: https://playwright.dev/docs/test-snapshots
- Storybook accessibility testing: https://storybook.js.org/docs/writing-tests/accessibility-testing
- jest-axe: https://github.com/NickColley/jest-axe
- eslint-plugin-jsx-a11y: https://github.com/jsx-eslint/eslint-plugin-jsx-a11y
- Lighthouse docs: https://github.com/GoogleChrome/lighthouse/blob/main/docs/readme.md
- Lighthouse CI getting started: https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/getting-started.md
- Pa11y: https://pa11y.org/
