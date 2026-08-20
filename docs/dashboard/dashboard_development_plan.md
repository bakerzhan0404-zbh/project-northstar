# Dashboard Development Plan

**Prepared by:** Baker | **Date:** 16 August 2026 | **Status:** Version 1 prototype complete; user review pending

**Scope:** Three staged versions using the existing Week 1 and Week 2 evidence base

## Development principle

I will prove that the dashboard improves a real decision before adding automation or scoring. Each visual must state the decision it supports, its denominator and period, its evidence boundary, and the action or validation it triggers.

## Version 1 — Decision-useful minimum viable dashboard

### Objective

Test whether a small dashboard built from the committed Week 1 and Week 2 outputs gives the Treasurer a clearer, faster path from evidence to decision.

### Key features

- Three primary views tied to explicit decisions:
  1. Reporting timeliness by source method, led by the 23/55 delayed-account result — which portal and spreadsheet sources should enter a visibility pilot?
  2. Liquidity interpretation waterfall and threshold strip, ending at the $38.13 million 14-day screen and $0 established mobility — should option design continue while mobility remains unfunded?
  3. Mutually exclusive payment cohorts and the 2,839-record deduplicated priority union — which populations should enter root-cause review without double-counting the 342-record overlap?
- Two small `Not yet fundable` guardrail cards: 617.72 estimated manual hours per month and four closure-validation candidates with $7,800 of estimated fees.
- Visible source, period, denominator, evidence label, limitation, and next action for every measure.
- No recommendation score, predictive model, or new benefit claim.

### Approach

Use only committed processed CSVs and definitions already reconciled in the Week 2 metric contract. Build a static or lightweight local prototype, then walk it through the three Week 2 decisions and record which views clarify, duplicate, or distract from the story. Exit only when users can identify the supported decision and limitation for every retained view; remove unclear or unused views before Version 2.

### Expected output

A one-page prototype, a chart-to-decision map, a short review log, and an explicit `Go`, `Rework`, or `Stop` decision for Version 2.

The editable [Project Northstar — Dashboard V1](https://www.figma.com/design/A9ShhpMFBsXCyrCDbQXY5K) prototype is complete. It presents the three decision views and two validation guardrails on one page, keeps evidence limitations beside each result, and has passed internal layout and reconciliation checks. User decision walkthroughs remain the exit gate before Version 2.

### Risks

- Too many metrics could recreate the technical appendix instead of an executive dashboard.
- The $38.13 million screen could be mistaken for movable cash.
- Payment results could be generalized beyond the supplied 7,600 records or double-count the 342-record overlap.
- Date-level visibility could be mistaken for approved-cutoff or start-of-day performance.
- A polished layout could create confidence before usefulness is demonstrated.

## Version 2 — Validated and repeatable dashboard

### Objective

Turn the useful Version 1 views into a refreshable local dashboard that rejects invalid inputs, preserves metric definitions, and exposes data-quality failures before rendering results.

### Key features

- A dated source-control manifest and CSV contract covering the six source files, required columns, data types, grain, keys, permitted values, date semantics, and metric denominators. Current row counts are regression anchors, not permanent future limits.
- Blocking checks for missing files or columns, duplicate keys, broken relationships, invalid domains, impossible values, failed control totals, and incomplete periods.
- Warning checks for missingness, stale extracts, population changes, and unusual movements that require review but may not invalidate the full refresh; literal `None` remains a valid sweep category rather than a null.
- A validation report showing the failed rule, affected file or field, severity, and required correction.
- Fail-closed behavior for the affected domain or chart, a last-success timestamp, and no silent mixing of source vintages.
- Reproducible transformations, source-to-chart lineage, logged definition changes, and denominator-aware filters.

### Approach

Extend the existing Python and pandas workflow rather than create a second calculation layer. Load source files through one validation boundary, generate canonical dashboard tables, compare them with the dated manifest and committed regression controls, and add tests for valid and intentionally invalid CSV fixtures. Exit only when all blocking tests pass, warnings are visible and owned, totals reconcile, and an independent refresh reproduces the results.

### Expected output

A refreshable local dashboard, documented CSV and KPI contracts, a machine-readable validation report, automated tests, a refresh and failure-recovery runbook, and a signed readiness record for Version 3.

### Risks

- Schema or definition drift could silently change a chart or denominator.
- Partial or stale files could create a plausible but incomplete view.
- Flexible filters could produce small or misleading populations.
- Duplicating calculations between analysis code and dashboard code could break the single source of truth.
- Validation breadth and interface work could expand before the Version 1 decision story is proven.

## Version 3 — Governed recommendation and confidence layer

### Objective

Add transparent decision support only after the data pipeline is reliable, so recommendations and confidence reflect documented evidence, sensitivities, and control gates rather than an arbitrary score.

### Key features

- A `Gate first, score second` method: reconciliation, legal/local permissibility, control, resilience, ownership, service-continuity, and rollback gates are non-compensating; a critical failure cannot be averaged away.
- Option and pilot comparisons using criteria, thresholds, weights, and veto conditions approved before results are viewed or scored.
- Separate assessment of value, evidence quality, feasibility, risk/control, and time to outcome; cash release, P&L, capacity, and risk are never added into one benefit number.
- Recommendation states follow explicit rules: `Advance design` requires all critical gates to pass and the option to survive agreed downside tests; `Validate` means a material signal remains but a non-critical evidence or owner gate is open; `Hold / no scale` follows any critical gate failure or stop condition.
- Confidence remains separate from attractiveness and is capped by evidence rules:
  - `High` requires reconciled or certified evidence, stable sensitivities, accountable-owner confirmation, and no decision-critical open gate.
  - `Medium` permits validation or design when the calculation reconciles but operational, causal, or owner validation remains open; it cannot support funded value.
  - `Low` applies to assumptions, unverified populations or causes, stale evidence, or failed critical gates and supports only a hypothesis or hold state.
- Driver-level explanations, sensitivity views, evidence links, and an approval record; no unexplained composite score.

### Approach

Agree the decision criteria, thresholds, weights, and veto conditions with the accountable owners before comparing options. Encode the approved rules, test alternative weights plus the $21 million mobility, two-closure, 50-hour-per-month, and four-hour rollback cases, and show switching conditions rather than one opaque winner. Exit only when the same evidence reproduces the same label, material sensitivities and counterevidence are visible, no failed control is averaged away, and accountable owners approve the rationale.

### Expected output

A governed decision-support dashboard, published scoring and confidence rubric, driver and sensitivity view, traceable recommendation rationale, approval history, and decision record suitable for the Week 4 executive pack.

### Risks

- Numeric scoring could create false objectivity or hide weak evidence.
- Weight changes could be used to reverse-engineer a preferred answer.
- Correlated criteria could double-count the same evidence or benefit.
- Averages could allow a control failure to be offset by attractive value.
- Recommendations could become stale when evidence, ownership, or constraints change.
- Users could treat decision support as authorization to transfer cash, close accounts, or execute a pilot.

## Source baseline

- `deliverables/working/week_2/W2_metric_contract.md`
- `deliverables/working/week_2/W2_findings_log.md`
- `deliverables/working/week_2/W2_workplan.md`
- `deliverables/working/week_2/W2_submission_index.md`
- `client/DATA_DICTIONARY.md`
- `program/CONSULTING_STANDARDS.md`
- `tests/test_data_quality.py`
- `tests/test_week2_diagnostic.py`
