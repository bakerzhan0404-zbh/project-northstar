# Dashboard V2 Design Specification

**Prepared by:** Baker | **Date:** 16 August 2026 | **Status:** Closed-state Figma view complete; evidence view in progress

**Artifact scope:** This is the second visual-design iteration of the Version 1 dashboard. It does not replace the validated and repeatable pipeline described as Version 2 in the development plan.

## Objective

Turn the evidence-complete Version 1 reference into a user-facing executive dashboard that can be understood in ten seconds and explored without a presenter.

## Closed-state executive view

### Header

- `Project Northstar`
- `Treasury decision dashboard`
- `Week 1–2 diagnostic snapshot · 1 Jan–30 Jun 2026 · supplied data, not live operations`
- Status: `Reconciled to supplied controls · source certification open`
- Control: `Evidence & definitions`

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

## Evidence and definitions drawer

The main-screen control opens an accessible right-side drawer. It contains five sections: `What this means`, `Evidence`, `Decision boundary`, `Next action`, and `Definition & source`.

Move the following detail out of the executive view and into the drawer:

- Full reporting-source breakdown and the 9,955 account-day measures.
- Liquidity waterfall, 7-day reference, threshold survival table, and excluded buffer inputs.
- Four mutually exclusive payment cohorts, the 342-record overlap control, and exact exception and repair shares.
- Process-capacity detail, closure candidate dependencies, formulas, lineage, file names, and test counts.

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

## Figma build record

- File: `Project Northstar — Dashboard V1`
- Page: `Dashboard V2 — Executive View`
- Closed-state frame: `Project Northstar — Dashboard V2` (`11:3`)
- Canvas: 1440 × 900, with the original Version 1 frame preserved unchanged.
- Visual QA: 49 text layers use Inter; no zero-size text, overflow, placeholder layers, or missing required evidence language remain.
- Next build step: add and validate the open `Evidence & definitions` state without increasing the closed-state density.
