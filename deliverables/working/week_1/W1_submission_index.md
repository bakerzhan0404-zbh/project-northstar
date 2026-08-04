# Week 1 — Submission Index

**Pack:** Engagement Foundation Pack

**Prepared by:** Baker

**Reporting date:** 2 August 2026

**Status:** Ready for mentor/client review; not client-approved

**Classification:** Confidential — Project Northstar simulated client material

## Executive review path — start here

1. [Weekly update](W1_weekly_update.md) — the 90-second recommendation, three findings, three decisions, and three requests
2. [Decision-led issue tree](W1_issue_tree.md) — the diagnosis-to-consequence logic and the hypotheses Week 2 will test
3. [Findings log](W1_findings_log.md) — the traceable fact–implication–action chain behind the executive story

These three files are the main review path. Technical controls, methods, and detailed supporting records are deliberately separated below so the executive story remains focused on implications.

## Technical assurance and appendix

| File | Appendix role | Review status |
|---|---|---|
| [Technical assurance summary](W1_data_quality_report.md) | Reconciliations, evidence limitations, treatments, and decision impact | Ready; technical support, not the executive narrative |
| [Analysis log](W1_analysis_log.md) | Detailed inputs, definitions, transformations, sensitivities, and outputs | Current through A05 |
| [Full 52-control inventory](../../../data/processed/W1_data_quality_checks.csv) | Check name and pass/fail result for every expanded control | 52 of 52 pass |
| [Data-quality metrics](../../../data/processed/W1_data_quality_metrics.csv) | Reproducible control totals and qualified analytical measures | Current |
| [Missingness profile](../../../data/processed/W1_missingness_profile.csv) | Field-level completeness evidence | Current |
| [Visibility by region](../../../data/processed/W1_visibility_by_region.csv) | Supporting regional visibility cut | Current |

## Governance and supporting records

| File | Purpose | Review status |
|---|---|---|
| [Engagement alignment](W1_engagement_alignment.md) | Decision, scope, stakeholders, kickoff questions, and success definition | Draft complete; agreement pending |
| [Workplan](W1_workplan.md) | Four-week tasks, dependencies, milestones, and blockers | Draft complete; agreement pending |
| [External evidence brief](W1_external_evidence_brief.md) | Public-evidence context and three-case S06 sample | Ready; contextual evidence only |
| [Source log](W1_source_log.csv) | External claims, links, methods, limitations, and use | Current; reverify before final submission |
| [Assumptions register](W1_assumptions_register.csv) | Uncertainty, sensitivity, validation action, and proposed owner | Current; one assumption closed |
| [Risk register](W1_risk_register.csv) | Delivery, analytical, benefit, control, and evidence risks | Current; owners proposed |
| [Decision log](W1_decision_log.md) | Analyst decisions and open client decisions | Current; no client checkpoint yet |
| [Stakeholder evidence notes](W1_interview_notes.md) | Claims, evidence needs, bias, and follow-up | Based on supplied pack, not new interviews |

## Assurance status

All 10 supplied tests and all 52 expanded controls pass. Six raw files reproduce from deterministic seed `20260730`, and four processed Week 1 CSVs reproduce from version-controlled code. The controls establish internal consistency and reproducibility—not source-system completeness, legal transferability, or representativeness of the supplied payment extract. See the technical appendix above for check-level evidence.

## Reproduce the technical appendix

From the repository root, run:

```bash
python3 src/generate_data.py
python3 src/starter_analysis.py
python3 src/week1_data_quality.py
python3 tests/test_data_quality.py
```

Calculated outputs are stored under `data/processed/`. Do not edit `data/raw/` manually.

## Three Week 3-critical evidence packages

1. **Visibility:** Timestamped reporting logs, cutoff, balance type, source, and reconciliation for all 55 accounts.
2. **Liquidity transferability and economics:** Account-level certification, operating buffers, settlement constraints, funding events, facility use, and borrowing/transfer costs.
3. **Controlled payments:** Source population/value control, sampling logic, reason codes, approval/release timestamps, and criticality for the supplied 7,600-record extract.

## Secondary and option-dependent confirmations

- Confirm the executive question, checkpoint dates, proposed owners, and closure-validation criteria.
- Supply AR/remittance/matching and FX transaction/exposure records or keep those workstreams P1 and explicitly constrained.
- Reconcile the $3.9bn entity revenue sum to the $3.8bn client brief before using revenue denominators.

## Evidence-label convention

- `ACG-DATA` — supplied client materials or project datasets
- `ANALYST-CALC` — reproducible calculation from supplied data
- `ANALYST-ASSUMPTION` — unverified input requiring validation
- `ANALYST-JUDGMENT` — interpretation or proposed action
- `JPM-PUBLIC` — official public JPMorgan material

All named client owners in the pack are proposed until confirmed at a checkpoint.
