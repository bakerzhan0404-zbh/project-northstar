# Week 2 — Submission Index

**Pack:** Current-State Diagnostic Pack

**Prepared by:** Baker

**Reporting date:** 16 August 2026

**Status:** Ready for mentor/client review; not client-approved

**Classification:** Confidential — Project Northstar simulated client material

## Executive review path — start here

1. [Weekly update](W2_weekly_update.md) — the 90-second recommendation, three findings, three decisions, and three requests
2. [Current-state diagnostic](W2_diagnostic_report.md) — the answer-first eight-page management report
3. [Five-slide diagnostic checkpoint PDF](W2_checkpoint_5-slidesdeck.pdf) — final rendered management deck; [speaker-note and provenance source](W2_checkpoint_deck.md)
4. [Findings log](W2_findings_log.md) — five promoted findings with confidence, counterevidence, and decision consequence

The executive spine is consistent across the rendered checkpoint and Markdown sources: **act on source-concentrated reporting and the deduplicated priority-payment gap; treat $38.13m as a 14-day screening result, not movable cash; constrain capacity and account value until evidence gates are satisfied.** The rendered five-page checkpoint is aligned to these sources and ready for mentor/client review.

## Operating-model and feasibility artifacts

| File | Purpose | Review status |
|---|---|---|
| [Targeted current-state process maps and RACI](W2_current_state_process_map_and_RACI.md) | Cash/payment handoffs, controls, likely causes, ownership, and pilot gates | Draft for process-owner validation |
| [Targeted maturity heatmap](W2_maturity_heatmap.md) | Observable current/target capability by dimension; no composite average | Provisional; process-owner validation required |
| [Updated issue tree](W2_issue_tree.md) | Supported, weakened, rejected, and unresolved hypotheses | Current through Week 2 |
| [Week 3 readiness workplan](W2_workplan.md) | Completed Week 2 tasks, Week 3 sequence, dependencies, and owners | Current; client decisions pending |

## Technical assurance and appendix

| File | Assurance role | Status |
|---|---|---|
| [Technical appendix](W2_technical_appendix.md) | Definitions, methods, reconciliations, sensitivities, detailed cuts, and unpromoted observations | Complete |
| [Metric and evidence contract](W2_metric_contract.md) | Denominators, liquidity ladder, evidence labels, and promotion rule | Active |
| [Analysis log](W2_analysis_log.md) | A06–A14 transformations, tests, results, counterevidence, and outputs | Current |
| [`src/week2_diagnostic.py`](../../../src/week2_diagnostic.py) | Reproducible analytical layer and output generation | Complete |
| [`tests/test_week2_diagnostic.py`](../../../tests/test_week2_diagnostic.py) | 69 diagnostic assertions | 69/69 pass |
| [`tests/test_data_quality.py`](../../../tests/test_data_quality.py) | Supplied data-quality suite | 10/10 pass |
| [Week 1 expanded control inventory](../../../data/processed/W1_data_quality_checks.csv) | Structural and logic controls carried into Week 2 | 52/52 pass |

## Cumulative engagement controls

| File | Week 2 update | Status |
|---|---|---|
| [Assumptions register](W2_assumptions_register.csv) | 21 assumptions with scenario evidence, validation action, owner, and status | Current |
| [Risk register](W2_risk_register.csv) | 16 analytical, benefit, execution, control, technology, and communication risks | Current |
| [Decision log](W2_decision_log.md) | Carried Week 1 decisions, nine Week 2 decisions, and checkpoint decisions | Current |
| [Source log](W2_source_log.csv) | Six external sources carried as context; no Week 2 finding depends on them | Current |
| [Findings log](W2_findings_log.md) | Five promoted findings and Week 1 disposition | Current |

## Generated analytical outputs

| Output | Grain | Diagnostic use |
|---|---|---|
| [`W2_reconciliation_metrics.csv`](../../../data/processed/W2_reconciliation_metrics.csv) | Metric | Controlled Week 2 baseline |
| [`W2_account_diagnostic.csv`](../../../data/processed/W2_account_diagnostic.csv) | Account | Footprint, candidate, and protection screen |
| [`W2_visibility_diagnostic.csv`](../../../data/processed/W2_visibility_diagnostic.csv) | Dimension/category | Timeliness and value-weighted visibility |
| [`W2_liquidity_daily.csv`](../../../data/processed/W2_liquidity_daily.csv) | Date | Daily liquidity layers and scenarios |
| [`W2_liquidity_account_scenarios.csv`](../../../data/processed/W2_liquidity_account_scenarios.csv) | Account | 30 June account-level buffer screen |
| [`W2_liquidity_scenarios.csv`](../../../data/processed/W2_liquidity_scenarios.csv) | Liquidity layer | 30 June interpretation ladder |
| [`W2_liquidity_thresholds.csv`](../../../data/processed/W2_liquidity_thresholds.csv) | Window/threshold | $21m/$35m/$46.2m stability tests |
| [`W2_simultaneous_positions_daily.csv`](../../../data/processed/W2_simultaneous_positions_daily.csv) | Date | Concurrent account/entity positions |
| [`W2_entity_positions.csv`](../../../data/processed/W2_entity_positions.csv) | Entity/date | Entity net and within-entity mismatch |
| [`W2_account_positions.csv`](../../../data/processed/W2_account_positions.csv) | Account | Persistent deficit screen |
| [`W2_payment_diagnostic.csv`](../../../data/processed/W2_payment_diagnostic.csv) | Dimension/category | Mutually exclusive cohorts, explicit overlap, deduplicated union, rates, amounts, and absolute contribution |
| [`W2_process_capacity.csv`](../../../data/processed/W2_process_capacity.csv) | Activity | Estimated capacity and control screen |
| [`W2_repair_baseline_reconciliation.csv`](../../../data/processed/W2_repair_baseline_reconciliation.csv) | Metric | Unreconciled payment/process baseline comparison |

## Reproduce the pack

From the repository root:

```bash
python3 src/generate_data.py
python3 src/starter_analysis.py
python3 src/week1_data_quality.py
python3 src/week2_diagnostic.py
python3 tests/test_data_quality.py
python3 tests/test_week2_diagnostic.py
```

## Quality and evidence status

- The report contains eight designed pages; the checkpoint contains exactly five core slides.
- Five findings are promoted; every one has fact, magnitude, implication, likely mechanism, confidence, counterevidence, action, and source.
- Every payment statement is limited to the supplied 7,600 records.
- Screening results are never described as movable cash; closure candidates are never approved closures; capacity is never called P&L or headcount.
- Receivables and FX remain P1/data-gated.
- Raw files remain unchanged; generated outputs reproduce from version-controlled code.

## Evidence-label convention

- `ACG-DATA` — supplied client material or project dataset
- `ANALYST-CALC` — reproducible calculation from supplied data
- `ANALYST-ASSUMPTION` — unverified scenario or input requiring validation
- `ANALYST-JUDGMENT` — interpretation or proposed action
- `JPM-PUBLIC` — official public JPMorgan context, never proof of ACG performance

All named client owners and recommendations remain proposed until confirmed at the diagnostic checkpoint.
