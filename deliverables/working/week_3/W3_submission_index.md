# Week 3 — Submission Index

**Pack:** Strategy and Business-Case Pack
**Prepared by:** Baker
**Reporting date:** 18 August 2026
**Status:** Working index; steering deck rendered and visually reviewed in the Week 2 checkpoint house style, from one reproducible source
**Classification:** Confidential — Project Northstar simulated client material

## Executive review path — start here

1. [Weekly update](W3_weekly_update.md) — the 90-second recommendation, current status, decisions required, uncertainties, and Week 4 priorities
2. [Five hardest CFO questions](W3_CFO_QA.md) — direction, liquidity screen, affordability, pilot safety/usefulness, and downside switching conditions
3. [Strategic options](W3_strategic_options.md) — gate-then-score comparison, `87 / 72 / 60` result, five plausible sensitivities, and switching conditions
4. [Validation case](W3_business_case.md) — non-additive value ledgers, zero recognized value, open costs, and manager challenge
5. [Interim steering deck](W3_interim_steering_deck.pdf) — the ten rendered slides; the same deck is supplied as an editable [PPTX](W3_interim_steering_deck.pptx), and the [Markdown source](W3_interim_steering_deck.md) carries the speaker notes and file-level provenance

The executive spine is consistent: **federated coordination is the provisional design direction; local stabilization is the fallback if global ownership, minimum integration readiness, or affordability fails; all execution-evidence gates remain open; and the present case authorizes no execution or value.**

## Strategy and future-state design

| File | Purpose | Review status |
|---|---|---|
| [Design principles](W3_design_principles.md) | Eight observable principles and non-compensating gate rule | Analyst proposal; client validation open |
| [Strategic options](W3_strategic_options.md) | Three coherent options, locked weighted matrix, five plausible sensitivities, and switching cases | Conditional analyst direction |
| [Future-state operating model](W3_future_state_operating_model.md) | Federated organization, governance, cash/payment processes, data, technology, controls, service, and capability map | Proposed design; no client approval |
| [Future-state process maps and RACI](W3_future_state_process_map_and_RACI.md) | Cash/payment flows, global/regional/local accountability, exceptions, and escalation | Proposed; owner and specialist validation open |
| [Control inventory](W3_control_inventory.csv) | 19 proposed cash, payment, technology/resilience, and governance controls | Design inventory; no operating effectiveness claim |

## Bounded evidence designs

| File | Purpose | Review status |
|---|---|---|
| [Visibility pilot charter](W3_visibility_pilot_charter.md) | All-55 readiness census and ten-account read-only design | Design only; separate later go/no-go required |
| [Payment pilot charter](W3_payment_pilot_charter.md) | Four-cohort root-cause and control-preserving process-test design | Design only; no production intervention defined or approved |
| [`W3_visibility_pilot_candidates.csv`](../../../data/processed/W3_visibility_pilot_candidates.csv) | Deterministic visibility v2 candidate frame | 10 accounts; all base review; `AC0040` enhanced/shadow-only |
| [`W3_payment_sample_frame.csv`](../../../data/processed/W3_payment_sample_frame.csv) | Deterministic payment v3 case-control frame | 120 unique records; 50 exact / 10 documented match deviations |
| [`W3_pilot_model_controls.csv`](../../../data/processed/W3_pilot_model_controls.csv) | Reconciliation, selection, eligibility, lineage, and boundary controls | Model controls only; no client-evidence closure |

## Validation case and economics

| File | Purpose | Review status |
|---|---|---|
| [Business-case validation narrative](W3_business_case.md) | Three diagnostic cases, four separate value types, cost gaps, downside, and stage gates | Validation case; not an investment or funding request |
| [Assumptions register](W3_assumptions_register.csv) | VG01–VG12 and SA01–SA07 evidence/assumption ownership | Open or blocked pending evidence |
| [`W3_business_case_scenarios.csv`](../../../data/processed/W3_business_case_scenarios.csv) | Downside/base/upper diagnostic quantities and zero-value boundaries | Reproducible; not benefits |
| [`W3_business_case_scenario_planning.csv`](../../../data/processed/W3_business_case_scenario_planning.csv) | Illustrative Wave-1 cost range, benefit-realization month, ramp-up, steady state, and sensitivities per scenario | Reproducible; `ANALYST-ASSUMPTION` planning range, excluded from recognized value |
| [`W3_business_case_value_ledger.csv`](../../../data/processed/W3_business_case_value_ledger.csv) | Cash, P&L, capacity, and risk kept non-additive | Cash/P&L/capacity recognized `$0`; risk `NOT QUANTIFIED` |
| [`W3_cost_evidence_requirements.csv`](../../../data/processed/W3_cost_evidence_requirements.csv) | Ten cost and timing evidence packages | All open; actual cost unavailable |
| [`W3_business_case_controls.csv`](../../../data/processed/W3_business_case_controls.csv) | Model-contract and fail-closed checks | Model-control pass does not close evidence gates |

## Executive controls and traceability

| File | Control role | Status |
|---|---|---|
| [Analysis log](W3_analysis_log.md) | A15–A20 methods, results, counterevidence, and outputs | Current through the validation case; executive synthesis integration in progress |
| [Workplan](W3_workplan.md) | Week 3 modules, dependencies, owners, and status | Current; client mandate/ownership remains proposed |
| [Findings log](W3_findings_log.md) | F12–F17 fact–implication–action chain and Week 2 disposition | Promoted for CFO review; not approved |
| [Decision log](W3_decision_log.md) | Analyst decisions, open CFO decisions, conditions, and status convention | Current; no client decision recorded |
| [Recommendation risk register](W3_risk_register.csv) | R017–R030 likelihood, impact, score, trigger, mitigation, contingency, owner, and evidence label | Open/monitoring; risk exposure not monetized |
| [Risk register narrative](W3_risk_register.md) | Same register with priority control actions and Week 2 relationship | Companion to the CSV; the CSV governs |
| [Source and evidence log](W3_source_log.csv) | 11 internal and 7 public-context sources with label, method, limitation, and status | Current for working pack |
| [Source log narrative](W3_source_log.md) | Same sources with the evidence-label convention and approval boundary | Companion to the CSV; the CSV governs |

## Reproducible model and assurance paths

| Model / test | Purpose |
|---|---|
| [`src/week3_strategy.py`](../../../src/week3_strategy.py) / [`tests/test_week3_strategy.py`](../../../tests/test_week3_strategy.py) | Reproduce option scores, gate results, sensitivities, and switch cases |
| [`src/week3_pilot_design.py`](../../../src/week3_pilot_design.py) / [`tests/test_week3_pilot_design.py`](../../../tests/test_week3_pilot_design.py) | Reproduce ten-account and 120-payment frames |
| [`tests/test_week3_operating_model.py`](../../../tests/test_week3_operating_model.py) | Validate process, RACI, controls, charter, and frame semantics |
| [`src/week3_business_case.py`](../../../src/week3_business_case.py) / [`tests/test_week3_business_case.py`](../../../tests/test_week3_business_case.py) | Reproduce scenarios, ledgers, cost requirements, evidence gates, and fail-closed treatment |
| [`src/week3_steering_deck.py`](../../../src/week3_steering_deck.py) | Rebuild the ten-slide PPTX in the Week 2 checkpoint house style; the PDF is exported from it |
| [`tests/test_week3_executive_pack.py`](../../../tests/test_week3_executive_pack.py) | Check executive-pack files, exact figures, evidence labels, decision boundaries, and forbidden overclaims |

Run from the repository root:

```bash
python3 src/week3_strategy.py
python3 src/week3_pilot_design.py
python3 src/week3_business_case.py
python3 src/week3_steering_deck.py
python3 tests/test_week3_strategy.py
python3 tests/test_week3_pilot_design.py
python3 tests/test_week3_operating_model.py
python3 tests/test_week3_business_case.py
python3 tests/test_week3_executive_pack.py
```

## Evidence-label convention

- `ACG-DATA` — supplied client material or project dataset.
- `ANALYST-CALC` — reproducible calculation from supplied data.
- `ANALYST-ASSUMPTION` — unverified scenario or input requiring validation.
- `ANALYST-JUDGMENT` — interpretation, score, threshold, or proposed action.
- `JPM-PUBLIC` — official public J.P. Morgan context; never proof of ACG performance.

## Current quality and approval boundary

- The provisional option result is federated `87`, local `72`, and global `60`; federated leads all five plausible sensitivities.
- The visibility frame contains 10 purposive accounts. The payment frame contains 120 records with per-cohort `8 + 7 + 15` allocation, `Completed`-only controls, and 50 exact / 10 documented pair deviations.
- The validation case contains no current recognized cash, P&L, or capacity benefit; risk exposure/value is `NOT QUANTIFIED`; actual costs and ROI/NPV/payback are unavailable.
- A separate, clearly labelled illustrative Wave-1 planning range (conservative/base/upside cost, benefit-realization timing, ramp-up, and duration) supports sequencing and affordability conversation; it is `ANALYST-ASSUMPTION` only and does not change the zero recognized-value boundary above.
- The FY2026 `$1.0–$1.5m` amount is a ceiling only—not an implementation-cost estimate, approved budget, spend authority, committed funding, or ROI denominator.
- No client approval for pilot launch, production change, cash movement, account closure, labor action, benefit recognition, implementation spend, procurement, or scale is recorded in this pack.
