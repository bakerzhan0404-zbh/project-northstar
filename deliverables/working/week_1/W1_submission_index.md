# Week 1 — Submission Index

**Pack:** Engagement Foundation Pack

**Prepared by:** Baker

**Reporting date:** 2 August 2026

**Status:** Ready for mentor/client review; not client-approved

**Classification:** Confidential — Project Northstar simulated client material

## Recommended review order

1. [Engagement alignment](W1_engagement_alignment.md) — decision, scope, stakeholders, kickoff questions, and success definition
2. [Decision-led issue tree](W1_issue_tree.md) — priority questions, hypotheses, evidence requirements, and status
3. [External evidence brief](W1_external_evidence_brief.md) — two-page public-evidence context and three-case S06 sample
4. [Data quality and readiness report](W1_data_quality_report.md) — reconciliations, limitations, treatments, and decision impact
5. [Weekly update](W1_weekly_update.md) — one-page status, evidence changes, requests, uncertainty, and Week 2 priorities

## Required and supporting records

| File | Purpose | Review status |
|---|---|---|
| [Workplan](W1_workplan.md) | Four-week tasks, dependencies, milestones, and blockers | Draft complete; agreement pending |
| [Source log](W1_source_log.csv) | External claims, links, methods, limitations, and use | Current; reverify before final submission |
| [Analysis log](W1_analysis_log.md) | Inputs, definitions, transformations, tests, sensitivities, and outputs | Current through A03 |
| [Assumptions register](W1_assumptions_register.csv) | Uncertainty, sensitivity, validation action, and proposed owner | Current; one assumption closed |
| [Risk register](W1_risk_register.csv) | Delivery, analytical, benefit, control, and evidence risks | Current; owners proposed |
| [Decision log](W1_decision_log.md) | Analyst decisions and open client decisions | Current; no client checkpoint yet |
| [Findings log](W1_findings_log.md) | Fact–implication–action chain with confidence/counterevidence | Draft findings only |
| [Stakeholder evidence notes](W1_interview_notes.md) | Claims, evidence needs, bias, and follow-up | Based on supplied pack, not new interviews |

## Quality gate completed

- All 10 supplied data-quality tests pass.
- All 52 expanded controls pass, covering schema, keys, relationships, date panels, domains, flags, FX, status logic, missingness, and numeric ranges.
- Six raw files reproduce exactly from deterministic seed `20260730`; raw data remains unchanged.
- Four processed Week 1 CSVs are reproducible from version-controlled code.
- External claims S01–S05 were checked against official JPMorgan pages and logged with limitations.
- The 548-word external evidence brief render-checks at two content pages.
- The weekly update render-checks at one content page.
- Markdown local links resolve, CSV registers parse, and Git whitespace checks pass.

## Reproduce the evidence

From the repository root, run:

```bash
python3 src/generate_data.py
python3 src/starter_analysis.py
python3 src/week1_data_quality.py
python3 tests/test_data_quality.py
```

Calculated outputs are stored under `data/processed/`. Do not edit `data/raw/` manually.

## Items requiring client/mentor confirmation

1. Confirm the executive question, priority hypotheses, checkpoint dates, and proposed owners.
2. Define start-of-day visibility and supply timestamped reporting logs.
3. Validate restrictions, operating buffers, seasonality, and legal/tax transferability.
4. Reconcile payment extract coverage and payment/process exception scope.
5. Supply AR/remittance/matching and FX transaction/exposure records or formally constrain scope.
6. Reconcile the $3.9bn entity revenue sum to the $3.8bn client brief and obtain actual fee/borrowing baselines.

## Evidence-label convention

- `ACG-DATA` — supplied client materials or project datasets
- `ANALYST-CALC` — reproducible calculation from supplied data
- `ANALYST-ASSUMPTION` — unverified input requiring validation
- `ANALYST-JUDGMENT` — interpretation or proposed action
- `JPM-PUBLIC` — official public JPMorgan material

All named client owners in the pack are proposed until confirmed at a checkpoint.
