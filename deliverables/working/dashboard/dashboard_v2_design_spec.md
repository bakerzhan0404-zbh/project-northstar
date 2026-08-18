# Dashboard V2 Design Specification

**Prepared by:** Baker | **Date:** 18 August 2026 | **Status:** Interactive local dashboard implemented and validated

**Artifact scope:** This is the second visual-design iteration of the Version 1 dashboard. It does not replace the validated and repeatable pipeline described as Version 2 in the development plan.

## Objective

Turn the evidence-complete Version 1 reference into a user-facing executive dashboard that can be understood in ten seconds and explored without a presenter.

## Closed-state executive view

### Header

- `Project Northstar`
- `Treasury decision dashboard`
- `Week 1–2 diagnostic snapshot · 1 Jan–30 Jun 2026 · supplied data, not live operations`
- Status: `Reconciled to supplied controls · source certification open`
- Search: `Search metrics, entities, banks…`
- Control: `Filters` with date, currency, region, entity, and bank
- Control: `Metric guide`

### Decision banner

**Design and test; do not fund or execute yet.**

Prioritize delayed reporting sources and payment root causes; certify mobility before booking value.

### Signal 1 — Reporting visibility

- Headline: `23 / 55`
- Label: `accounts are delayed`
- Interpretation: `Every delayed account uses portal or spreadsheet reporting.`
- Boundary: `Reporting-date proxy—not start-of-day or elapsed-24-hour performance.`
- Action: `Pilot portal/spreadsheet reporting`

### Signal 2 — Liquidity

- Headline: `$0`
- Label: `validated mobility`
- Interpretation: `$38.13m is a 14-day screening sensitivity—not surplus cash or transfer authorization.`
- Action: `Certify mobility before funding`

### Signal 3 — Payment friction

- Headline: `≈74%`
- Label: `of exceptions and repair effort`
- Interpretation: `Concentrated in a 2,839-record deduplicated priority union.`
- Boundary: `Within 7,600 supplied records only; association, not causation.`
- Action: `Run reason-coded root-cause review`

### Guardrail strip

**Evidence gates still open**

- `Capacity not fundable · 102.60 h process estimate is 84% above the 55.78 h payment-file estimate`
- `Closure value not fundable · 4 validation candidates · $7.8k estimated fees · no approved closures`

## Metric guide

The main-screen control opens an accessible right-side dialog. It contains five sections: `Definition`, `Calculation`, `Data source`, `Interpretation limit`, and `Next action`.

Move the following detail out of the executive view and into the dialog:

- Current selected-account and account-day visibility measures.
- Liquidity components, selected 7/14-day reference, as-of date, formula, and interpretation limits.
- Payment-union numerator, matching denominator, selected share, deduplication rule, and overlap boundary.
- Process-capacity and closure-candidate definitions, formulas, sources, and interpretation limits.

Do not hide `supplied`, `estimated`, `screening sensitivity`, `deduplicated`, or `$0 validated` in hover-only help.

## User-facing design rules

- Fit the default view in one 1440 × 900 desktop frame.
- Use one primary decision banner, three equal signal cards, and one subordinate guardrail strip.
- Make the cards answer-first: number, meaning, boundary, next action.
- Use direct labels and text; do not depend on color alone.
- Provide progressive disclosure through the evidence drawer rather than dense footnotes.
- Preserve Version 1 unchanged on its own Figma page.
- Use the existing Inter fallback because SF Pro renders without glyphs through the current Figma automation integration.

## Acceptance criteria

- A reviewer can state `design and test—not fund or execute` within ten seconds.
- A reviewer identifies the three priority signals within thirty seconds.
- `$38.13m` is described as a screen and `$0` as the validated mobility line.
- The 2,839 payment union is understood as deduplicated and limited to 7,600 supplied records.
- Capacity and closure figures are rejected as funded benefits.
- Evidence details remain reachable without crowding the closed state.
- Applying date, currency, region, entity, or bank updates the relevant numerator and denominator together.
- Invalid and empty scopes retain no stale portfolio metric and never imply a false zero percentage.
- The Metric guide exposes definitions, formulas, sources, interpretation limits, and next actions for the current scope.
- Capacity remains labelled as an enterprise-global baseline when account filters are active.

## Figma build record

- File: `Project Northstar — Dashboard V1`
- Page: `Dashboard V2 — Executive View`
- Closed-state frame: `Project Northstar — Dashboard V2` (`11:3`)
- Canvas: 1440 × 900, with the original Version 1 frame preserved unchanged.
- Visual QA: 49 text layers use Inter; no zero-size text, overflow, placeholder layers, or missing required evidence language remain.
- Implementation: the Figma frame is now the visual reference for the local browser dashboard in `dashboard/`.

## Implemented interaction model

The browser implementation adds only controls that change a decision-relevant interpretation:

- **Liquidity horizon:** switches the governed 7-day and 14-day screening evidence. The screen, buffer, as-of evidence, boundary, and accessible announcement update together. Validated mobility remains `not established`, and the funded case remains `$0`.
- **Payment measure:** switches the same four mutually exclusive cohorts between records, exceptions, and repair minutes. The numerator, denominator, unit, cohort bars, union share, and explanation update together; the 342-record overlap remains counted once.
- **Dashboard search:** locates metrics and applies explicit entity, bank, region, currency, or account context without silently hiding cards.
- **Governed filters:** applies an inclusive date range plus single-select currency, region, entity, and bank. Visibility and payments use the selected period; liquidity uses the period end date; closures use account dimensions; capacity remains visibly global.
- **Metric guide:** opens a keyboard-accessible right-side dialog to the relevant definition, formula, source, interpretation limit, and next action for the current scope.
- **Reset:** clears search and filters and restores the full-period, 14-day, payment-record baseline.

These interactions make the artifact analytical rather than slide-like while preserving the concise closed state. Free-form thresholds, recommendation scores, funding controls, and execution actions remain intentionally excluded.
