# Dashboard V2 Design Specification

**Prepared by:** Baker | **Date:** 18 August 2026 | **Status:** Interactive local dashboard implemented and validated

**Artifact scope:** This is the second visual-design iteration of the Version 1 dashboard. It does not replace the validated and repeatable pipeline described as Version 2 in the development plan.

## Objective

Turn the evidence-complete Version 1 reference into a user-facing executive dashboard that can be understood in ten seconds and explored without a presenter.

## Closed-state executive view

### Header

- `Project Northstar`
- `Treasury decision dashboard`
- Current governed scope and reconciliation status
- Search: `Search metrics, entities, banks…`
- Control: `Filters` with date, currency, region, entity, and bank
- Control: `Metric guide`

### Portfolio decision disclosure

Always visible:

- Label: `Decision`
- Headline: `Design and test; do not fund or execute yet.`
- Status: `Portfolio-wide · Validation required`
- Direction: prioritize delayed reporting sources and payment root causes; certify mobility before booking value

The expanded panel explains why the portfolio-wide stance does not change with filters and identifies the evidence needed before funding or execution.

### Decision-signal disclosures

| Section | Always-visible result | Supporting boundary |
|---|---|---|
| Reporting visibility | `23 / 55` · `accounts delayed` | `Calendar-date proxy · not start-of-day or elapsed-24-hour visibility` |
| Liquidity | `$0` · `funded case` | `14-day screen: $38.13m` · `Validated mobility: not established` · not surplus cash or transfer authority |
| Payment friction | `37.36%` · `2,839 of 7,600 records` | Supplied records only · association, not causation |

Expanded signal panels contain:

- Current-scope evidence and visual
- Interpretation
- Decision boundary
- Next action
- Link to the full Metric guide

The 7/14-day control lives inside the expanded Liquidity section. The Records/Exceptions/Repair time control lives inside the expanded Payment friction section.

### Evidence-gate disclosures

| Section | Always-visible result | Supporting boundary |
|---|---|---|
| Capacity evidence | `102.6 h/month vs 55.8 h/month` · process estimate 84% higher | Enterprise-global management estimate · filters do not apply · not a combined capacity or P&L baseline |
| Closure evidence | `4 validation candidates` · `$7.8k estimated annual fees` · no approved closures | 30 Jun 2026 snapshot · date filter does not apply · dimension filters apply |

Capacity detail remains enterprise-global. Closure detail follows selected currency, region, entity, and bank values. Neither section presents an approved or fundable benefit.

### Accordion behavior

All six primary sections are collapsed by default. Only one section may be open at a time across Decision, Reporting visibility, Liquidity, Payment friction, Capacity evidence, and Closure evidence. Opening another section closes the previous one; clicking the open header collapses it.

Applying filters preserves the open section and updates its summary and detail together. Reset collapses all sections. Empty scopes show `No matching data` and `—`, never a false zero percentage or retained portfolio value.

## Metric guide

The top-menu control and the button inside each expanded section open an accessible right-side dialog on the relevant topic.

The Metric guide is stable methodology, not a second results view. It contains:

- `Definition`
- `Formula / calculation`
- `Data source`
- `Method limit`

The guide does not repeat current values, interpretations, decision boundaries, or next actions. Those belong to the inline disclosure so the user can interpret evidence without leaving page context.

Do not hide `supplied`, `estimated`, `screening sensitivity`, `deduplicated`, `$0 funded case`, or `not established` in hover-only help.

## User-facing design rules

- Fit the fully collapsed default view in one 1440 × 900 desktop frame.
- Use table-like summary rows instead of fixed-height presentation cards.
- Keep all details collapsed by default and permit only one open section.
- Keep the decision answer, KPI meaning, essential evidence boundary, and chevron visible in every collapsed row.
- On desktop, use one-line summary rows and full-width detail content. On tablet and mobile, allow summaries and details to stack without clipping.
- Keep all toggle targets at least 44 px and use direct text; do not depend on color, hover, or icons alone.
- Preserve `$0` funded-case mobility, `not established`, and global-capacity labelling in the collapsed state.
- Keep current evidence and actions inline; reserve the Metric guide for definitions, formulas, sources, and method limits.
- Preserve Version 1 unchanged on its own Figma page.
- Use the existing Inter fallback because SF Pro renders without glyphs through the current Figma automation integration.

## Acceptance criteria

- A reviewer can state `design and test—not fund or execute` within ten seconds.
- A reviewer can scan all five signal/gate summaries without opening a section.
- No chart, detailed control, warning block, or evidence table is expanded by default.
- Opening one primary section closes the previously open section.
- Search expands and focuses the correct section; methodology search opens the Metric guide.
- Applying filters updates the collapsed summary and open detail together without auto-opening another section.
- `$38.13m` remains a screen; `$0` remains the funded case; mobility remains `not established`.
- Payment evidence remains deduplicated and limited to matching supplied records.
- Capacity remains visibly global and closure/capacity figures remain non-fundable.
- Empty or incomplete scopes show `No matching data` or `—`, never stale portfolio values or false zero percentages.
- Keyboard navigation supports Enter/Space, arrow keys, Home/End, and Escape.
- The Metric guide contains no duplicate current-result or next-action content.

## Figma build record

- File: `Project Northstar — Dashboard V1`
- Page: `Dashboard V2 — Executive View`
- Closed-state frame: `Project Northstar — Dashboard V2` (`11:3`)
- Canvas: 1440 × 900, with the original Version 1 frame preserved unchanged.
- Visual QA: 49 text layers use Inter; no zero-size text, overflow, placeholder layers, or missing required evidence language remain.
- Implementation: the Figma frame remains the palette and typography reference; the browser dashboard extends it with the inline progressive-disclosure model specified here.

## Implemented interaction model

The browser implementation adds only interactions that support a decision or reveal its evidence:

- **Inline progressive disclosure:** six summary rows expose current evidence in place; one-open-at-a-time behavior keeps the page concise.
- **Dashboard search:** expands metric sections, applies explicit dimension/account context, and routes methodology queries to the Metric guide.
- **Governed filters:** applies an inclusive date range plus single-select currency, region, entity, and bank. Visibility and payments use the selected period; liquidity uses the period end date; closures use account dimensions; capacity remains global.
- **Liquidity horizon:** switches governed 7-day and 14-day evidence inside the open Liquidity section. Validated mobility remains `not established`, and the funded case remains `$0`.
- **Payment measure:** switches records, exceptions, and repair minutes inside the open Payment friction section while preserving the deduplicated cohort union.
- **Metric guide:** provides definition, formula, source, and method-limit reference without duplicating current evidence or actions.
- **Reset:** clears search and filters, restores the full-period/14-day/payment-record baseline, and collapses all sections.
- **Accessible navigation:** native disclosure behavior handles Enter/Space; arrow keys, Home/End, and Escape provide fast keyboard movement and collapse with focus return.

These interactions make the artifact behave like an analytical application rather than a static slide. Free-form thresholds, recommendation scores, funding controls, and execution actions remain intentionally excluded.
