# Dashboard Development Plan

**Prepared by:** Baker | **Date:** 16 August 2026 | **Status:** Development plan

**Scope:** Three staged versions using the existing Week 1 and Week 2 evidence base

## Development principle

I will prove that the dashboard improves a real decision before adding automation or scoring. Each visual must state the decision it supports, its denominator and period, its evidence boundary, and the action or validation it triggers.

## Version 1 — Decision-useful minimum viable dashboard

### Objective

Test whether a small dashboard built from the committed Week 1 and Week 2 outputs gives the Treasurer a clearer, faster path from evidence to decision.

### Key features

- Five executive measures: reporting delay, the 14-day liquidity screen, the deduplicated priority-payment union, process-capacity evidence, and account-closure candidates.
- Four compact views tied to explicit decisions:
  1. Reporting timeliness by source method — which delayed sources should enter a visibility pilot?
  2. Liquidity interpretation ladder and threshold stability — should option design continue while validated mobility remains unfunded?
  3. Mutually exclusive payment cohorts and the deduplicated union — which populations should enter root-cause review?
  4. Capacity and account screens — which apparent benefits must remain validation items?
- Visible source, period, denominator, evidence label, limitation, and next action for every measure.
- No recommendation score, predictive model, or new benefit claim.

### Approach

Use only committed processed CSVs and definitions already reconciled in the Week 2 metric contract. Build a static or lightweight local prototype, then walk it through the three Week 2 decisions and record which views clarify, duplicate, or distract from the story.

### Expected output

A one-page prototype, a chart-to-decision map, and a short review log showing which measures should be kept, changed, or removed before development continues.

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

- A CSV contract covering required files, columns, data types, grain, keys, permitted values, date coverage, and metric denominators.
- Blocking checks for missing files or columns, duplicate keys, broken relationships, invalid domains, impossible values, failed control totals, and incomplete periods.
- Warning checks for missingness, stale extracts, population changes, and unusual movements that require review but may not invalidate the full refresh.
- A validation report showing the failed rule, affected file or field, severity, and required correction.
- Reproducible transformations, source-to-chart lineage, refresh timestamp, and denominator-aware filters.

### Approach

Extend the existing Python and pandas workflow rather than create a second calculation layer. Load source files through one validation boundary, generate canonical dashboard tables, compare them with committed control totals, and add regression tests for both valid and intentionally invalid CSV fixtures.

### Expected output

A refreshable local dashboard, documented CSV and KPI contracts, a machine-readable validation report, automated tests, and a short refresh and failure-recovery runbook.

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

- Option and pilot comparisons using criteria and weights approved before results are scored.
- Separate assessment of value, evidence quality, feasibility, risk/control, and time to outcome; cash release, P&L, capacity, and risk are never added into one benefit number.
- Recommendation states such as `Advance design`, `Validate`, and `Hold / no scale`, each linked to explicit pass, open-gate, or stop conditions.
- Confidence labels based on source quality, reconciliation, validation status, sensitivity stability, counterevidence, and owner confirmation.
- Driver-level explanations, sensitivity views, evidence links, and an approval record; no unexplained composite score.

### Approach

Agree the decision criteria and weights with the accountable owners before comparing options. Encode the approved rules, test alternative weights and downside cases, prevent a strong modeled value from overriding a failed control, and require human approval for any recommendation change.

### Expected output

A governed decision-support dashboard, scoring and confidence rubric, sensitivity view, traceable recommendation rationale, and decision record suitable for the Week 4 executive pack.

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
- `program/CONSULTING_STANDARDS.md`
