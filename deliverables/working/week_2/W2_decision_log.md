# Week 2 — Decision Log

*Named client owners remain proposed until confirmed at the diagnostic checkpoint. Analyst decisions control the working evidence pack; they do not substitute for client approval.*

## Decisions carried from Week 1

| ID | Decision carried forward | Week 2 disposition |
|---|---|---|
| DEC-01 | Keep raw data immutable and calculations reproducible | Retained; all Week 2 outputs generate from `src/week2_diagnostic.py` |
| DEC-02 / 06 | Use date equality only as a same-day proxy | Retained; source pattern quantified, timestamp KPI still unvalidated |
| DEC-03 | Do not equate positive/available balance with movable cash | Retained; liquidity ladder and $0 validated mobility made explicit |
| DEC-04 | Use JPMorgan public cases as context only | Retained; no promoted Week 2 finding depends on an external case |
| DEC-05 | Week 1 status Amber | Superseded by Week 2 Amber: action is supported, value approval remains gated |
| DEC-07 | Keep payment and process estimates separate | Retained; 84% repair-hour mismatch quantified |
| DEC-08 | Prioritize three evidence packages | Retained as the Week 3 recommendation gates |

## Week 2 analyst decisions

| ID | Date | Decision | Decision maker | Rationale | Conditions / limitation | Follow-up | Proposed owner | Due |
|---|---|---|---|---|---|---|---|---|
| DEC-09 | 2026-08-10 | Lock the Week 2 metric/evidence contract before segmentation | Analyst | Prevent definition drift and overstatement | Every segment reconciles; evidence labels remain visible | Maintain contract through report/deck | Baker | Complete |
| DEC-10 | 2026-08-12 | Use all supplied payment statuses for the primary 7/14-day buffer and show Completed/Repaired as a status sensitivity | Analyst | All-status treatment is conservative for payment intent; status is not settlement evidence | Complete rolling windows only; first 6/13 days remain null | Replace with approved operating-buffer policy | Treasury / FP&A | Before Week 3 value approval |
| DEC-11 | 2026-08-12 | Carry $0 validated movable cash in the funded base despite encouraging scenarios | Analyst | Transferability, legal/local rules, forecast events, facility use, and economics are absent | Scenario ranges may guide option design only | Build account-level mobility certification | Group Treasurer | Before business case |
| DEC-12 | 2026-08-13 | Promote one payment finding focused on manual-touch and cross-border-wire cohorts | Analyst | These cohorts over-index on both rate and absolute contribution | Every claim remains limited to 7,600 supplied records; cause unproven | Controlled root-cause diagnostic | Shared Services Lead | Week 3 |
| DEC-13 | 2026-08-13 | Keep payment-file and process-file repair baselines separate | Analyst | 55.78 versus 102.60 hours/month do not reconcile | No combined capacity or P&L baseline | Reconcile population and process instance | Shared Services / Data owner | Before business case |
| DEC-14 | 2026-08-14 | Promote five findings only; move detailed cuts to the appendix | Analyst | Sharp synthesis is more decision-useful than topic-by-topic reporting | Each finding meets the six-part promotion rule | Use same five-finding spine in report, update, and deck | Baker | Complete |
| DEC-15 | 2026-08-14 | Use a provisional, non-aggregated maturity heatmap | Analyst | Observable evidence is uneven and dimensions are not equally weighted | No overall average or external benchmark claim | Validate each dimension with process owners | Group Treasurer / CIO | Week 3 |
| DEC-16 | 2026-08-15 | Keep receivables and FX P1/data-gated | Analyst | No controlled receivables records or executed FX trades/exposures arrived | Do not use proxy or external benchmark as substitute evidence | Reconfirm scope at checkpoint | Finance / Treasury | Week 3 |
| DEC-17 | 2026-08-15 | Develop local-stabilization, federated, and globally coordinated options against common gates | Analyst recommendation pending checkpoint | Diagnosis supports staged action but not a predetermined ambition | All options face $21m / two-closure / 50-hour downside and control/service tests | Build weighted matrix and sensitivities | Baker / SteerCo | Week 3 |

## Client decisions required at the Week 2 checkpoint

| Decision required | Analyst recommendation | Evidence or condition | Decision owner |
|---|---|---|---|
| Accept the five promoted findings | Accept as the current diagnostic, with stated confidence and counterevidence | Confirm stakeholder/process-owner contradictions | Group Treasurer / Steering committee |
| Authorize Week 3 option design | Approve three coherent ambition levels around one data/control foundation | No selection of preferred option yet | Steering committee |
| Approve two targeted pilots for design | Delayed balance sources and manual-touch/cross-border-wire cohorts | Peak calendar, service levels, controls, rollback, and owners | Treasurer / CIO / BU Finance |
| Assign the three evidence packages | Confirm one accountable owner and deadline per package | Visibility, mobility/economics, payment/process control | CFO / Steering committee |
| Define funded-value rule | Carry $0 validated mobility and exclude unvalidated capacity/fees | Finance approval and evidence completeness required | CFO / Finance |
| Confirm P1 deferrals | Keep receivables and FX constrained unless controlled data arrives | No substitute benchmark or proxy | CFO / Treasurer |

## Decision-status convention

- **Analyst decision:** Controls how the evidence pack is calculated or communicated.
- **Analyst recommendation pending checkpoint:** Proposed client direction, not approved.
- **Client decision:** Effective only after the named decision owner confirms it.
