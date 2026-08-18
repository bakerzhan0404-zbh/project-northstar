# Week 3 — Analysis Log

**Prepared by:** Baker  
**Working period:** 17–23 August 2026  
**Status:** In progress  
**Classification:** Confidential — Project Northstar simulated client material

## Reconciled evidence baseline

| Domain | Controlled Week 2 evidence entering Week 3 | Week 3 use | Decision boundary |
|---|---|---|---|
| Account footprint | 55 accounts; four closure-validation candidates; $7,800 estimated candidate fees | Option scope, account certification, closure-validation workstream | Candidates are not approved closures; fees are not realized P&L |
| Visibility | 9,955 account-days; 5,792 same-calendar-day; 23 delayed accounts, all portal/spreadsheet | Design principle and pilot cohort | Reporting-date proxy only; no approved cutoff or start-of-day baseline |
| Liquidity | $38.13m 14-day screen at 30 June; $35m survives 138/168 complete windows | Scenario and option design | Validated mobility remains `$0 established`; no funded cash value |
| Payments | 7,600 supplied records; priority union 2,839 records / 356 exceptions / 14,939 repair minutes | Root-cause review and targeted process design | Extract-bounded; overlap counted once; association is not cause |
| Capacity | 617.72 estimated manual hours/month; repair sources 102.60 versus 55.78 hours/month | Feasibility and validation scenario | Management estimates; sources are independent; zero validated redeployment |
| Funding constraint | $1.0–$1.5m FY2026 initial transformation envelope | Affordability/staging gate for every option | Ceiling only; implementation and recurring costs remain unavailable |

## Analytical work modules

| ID | Module | Decision question | Status | Reproducible output |
|---|---|---|---|---|
| A15 | Diagnostic narrative confirmation | Which Week 2 facts and open gates constrain the recommendation? | Complete | Baseline above; Week 2 findings retained without new client evidence |
| A16 | Design principles | What rules must every credible option satisfy? | Complete — analyst proposal | `W3_design_principles.md` |
| A17 | Strategic option comparison | Which ambition level is preferred under locked weights and alternative priorities? | Complete — conditional analyst direction | `W3_strategic_options.md`; four option-model CSVs |
| A18 | Future-state operating model | How should cash positioning and payments operate, and who owns each decision/control? | Complete — proposed design; client validation open | Future-state model, process maps, RACI, control inventory, pilot charters |
| A19 | Business case | What value remains defensible when cash, P&L, capacity, risk, and cost are separated? | Not started | `W3_business_case.md`; reproducible scenario model |
| A20 | Executive synthesis | What should the CFO align on now, and what remains conditional? | Not started | Interim steering deck, CFO Q&A, weekly update, findings/decision/risk logs |

## A15 — Confirm the diagnostic narrative

- **Decision question:** Is there enough evidence to select a design direction without overstating the value case?
- **Answer:** There is enough evidence to compare and design targeted options, but not to approve execution or fund mobility, capacity, fee, receivables, or FX benefits.
- **Contradictory evidence retained:** 87.31% of manual-touch and 86.01% of cross-border-wire supplied records have no exception; the $35m screen fails 30 of 168 complete 14-day windows; only four closure candidates survive the narrow screen; process and payment repair baselines differ by 84%.
- **Alternative explanations retained:** source method may proxy ownership/process differences; payment cohort membership may associate with rather than cause friction; process estimates may cover different instances or geography; positive balances may be required locally.
- **Decision consequence:** use a gate-then-score option model and two bounded validation designs; keep unvalidated benefit out of the funded case.
- **New constraint:** the start-of-Week-3 CFO update limits the initial FY2026 transformation envelope to $1.0–$1.5m. A larger commitment requires staged approval and demonstrated Wave 1 benefits; this does not supply an implementation-cost estimate.

## A16 — Define design principles before scoring

- **Decision question:** Which observable rules resolve the diagnosis while preserving service, controls, and local rights?
- **Method:** Translate the five findings and three evidence gates into eight principles spanning service, visibility, mobility, local autonomy, standardization, control, resilience, data ownership, integration, and scalability.
- **Result:** Eight principles were defined with an observable test, principal tension, proposed owner, finding traceability, and change-control rule.
- **Non-compensating rule:** A failed critical data/control/service/local-right/rollback gate cannot be averaged away by weighted value.
- **Evidence label:** `ANALYST-JUDGMENT`, grounded in `ACG-DATA` and `ANALYST-CALC` Week 2 findings.
- **Output:** `W3_design_principles.md`.
- **Status:** Complete for analyst comparison; client validation remains open.

## A17 — Compare strategic options under locked weights and gates

- **Decision question:** Which ambition level best fits the diagnosis, constraints, and principles, and when would that direction change?
- **Options:** Local stabilization, federated coordination, and globally coordinated design.
- **Method:** Lock seven criteria at 20/20/20/15/10/10/5 before scoring; score every option 1–5 with rationale; calculate `Σ(weight × score) ÷ 5`; apply non-compensating design and execution gates; rerun five plausible stakeholder weight cases and two extreme switching cases.
- **Base result:** Federated coordination 87/100; local stabilization 72; globally coordinated 60. Federated leads all five plausible sensitivities, with scores from 85 to 89.
- **Gate result:** All three option architectures explicitly contain the required gate conditions and may be scored for design. None is execution-ready because client ownership, source readiness, controls, service, rollback, costs, and value approval remain open.
- **New client constraint:** Every initial stage must fit the $1.0–$1.5m FY2026 envelope; a larger commitment requires staged approval and demonstrated Wave 1 benefits. The envelope is not an implementation-cost estimate.
- **Switching conditions:** Local becomes the interim direction if federated ownership, integration readiness, or affordability fails. Global becomes numerically preferred only under extreme scale/value weights and still requires all non-compensating gates.
- **Counterevidence:** The model is analyst judgment, not observed performance; no option cost exists; the mandate and owners remain unconfirmed; weighted robustness does not validate value or execution feasibility.
- **Code/test:** `src/week3_strategy.py`; `tests/test_week3_strategy.py` (28 controls).
- **Outputs:** `W3_option_weighted_scores.csv`, `W3_option_summary.csv`, `W3_option_sensitivity.csv`, and `W3_model_controls.csv`.
- **Status:** Complete as a conditional analyst recommendation for detailed design; not client approval or execution authorization.

## A18 — Design the future-state operating model and bounded validation tests

- **Design question:** How can federated coordination create a governed cash/payment decision chain while preserving explicit regional and local service, exception, and emergency rights?
- **Operating-model result:** One common data, policy, KPI, control, and escalation spine; regional/local validation and governed execution rights; standardized payment intake and exception learning; authoritative-source, mobility, control, service, resilience, evidence, and value gates.
- **Process/control result:** Two proposed future-state process maps, detailed cash and payment RACIs, an exception taxonomy, and 19 proposed controls across cash, payment, technology/resilience, and governance. All owners, service levels, approval limits, and specialist conclusions remain proposed.
- **Visibility design:** A 55-account evidence-readiness census precedes any later launch; the provisional ten-account, three-region, three-ERP, four-bank cohort is purposive and read-only. The proposed 95% cutoff and 100% reconciled/formally explained conditions require four comparable weeks and owner approval; they are not the current baseline.
- **Payment design:** Phase A is a 120-record, four-stratum root-cause review with 15 issue cases and 15 non-issue controls per stratum. It is purposive case-control diagnosis, not prevalence, causation, or benefit evidence. A production intervention remains undefined until a cause, comparator, control design, cost, and baseline are approved.
- **Affordability/value boundary:** Both charters keep cost ranges `TBD`; the `$1.0–$1.5m` FY2026 envelope is a combined-stage ceiling, not a pilot budget or spend authority. Mobility, capacity, account fees, P&L, and risk value remain unfunded.
- **Code/test:** `tests/test_week3_operating_model.py` validates artifact presence, the 19-control contract, control references, process-map blocks, provisional populations, and evidence boundaries.
- **Outputs:** `W3_future_state_operating_model.md`, `W3_future_state_process_map_and_RACI.md`, `W3_control_inventory.csv`, `W3_visibility_pilot_charter.md`, and `W3_payment_pilot_charter.md`.
- **Status:** Complete for Week 3 design review only; no launch, production change, cash movement, closure, labor action, benefit recognition, or scale is authorized.
