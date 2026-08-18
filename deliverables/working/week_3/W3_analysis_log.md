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

## Analytical work modules

| ID | Module | Decision question | Status | Reproducible output |
|---|---|---|---|---|
| A15 | Diagnostic narrative confirmation | Which Week 2 facts and open gates constrain the recommendation? | Complete | Baseline above; Week 2 findings retained without new client evidence |
| A16 | Design principles | What rules must every credible option satisfy? | Complete — analyst proposal | `W3_design_principles.md` |
| A17 | Strategic option comparison | Which ambition level is preferred under locked weights and alternative priorities? | In progress | `W3_strategic_options.md`; option-model CSVs |
| A18 | Future-state operating model | How should cash positioning and payments operate, and who owns each decision/control? | Not started | Future-state model, process maps, RACI, control inventory, pilot charters |
| A19 | Business case | What value remains defensible when cash, P&L, capacity, risk, and cost are separated? | Not started | `W3_business_case.md`; reproducible scenario model |
| A20 | Executive synthesis | What should the CFO align on now, and what remains conditional? | Not started | Interim steering deck, CFO Q&A, weekly update, findings/decision/risk logs |

## A15 — Confirm the diagnostic narrative

- **Decision question:** Is there enough evidence to select a design direction without overstating the value case?
- **Answer:** There is enough evidence to compare and design targeted options, but not to approve execution or fund mobility, capacity, fee, receivables, or FX benefits.
- **Contradictory evidence retained:** 87.31% of manual-touch and 86.01% of cross-border-wire supplied records have no exception; the $35m screen fails 30 of 168 complete 14-day windows; only four closure candidates survive the narrow screen; process and payment repair baselines differ by 84%.
- **Alternative explanations retained:** source method may proxy ownership/process differences; payment cohort membership may associate with rather than cause friction; process estimates may cover different instances or geography; positive balances may be required locally.
- **Decision consequence:** use a gate-then-score option model and two bounded validation designs; keep unvalidated benefit out of the funded case.

## A16 — Define design principles before scoring

- **Decision question:** Which observable rules resolve the diagnosis while preserving service, controls, and local rights?
- **Method:** Translate the five findings and three evidence gates into eight principles spanning service, visibility, mobility, local autonomy, standardization, control, resilience, data ownership, integration, and scalability.
- **Result:** Eight principles were defined with an observable test, principal tension, proposed owner, finding traceability, and change-control rule.
- **Non-compensating rule:** A failed critical data/control/service/local-right/rollback gate cannot be averaged away by weighted value.
- **Evidence label:** `ANALYST-JUDGMENT`, grounded in `ACG-DATA` and `ANALYST-CALC` Week 2 findings.
- **Output:** `W3_design_principles.md`.
- **Status:** Complete for analyst comparison; client validation remains open.
