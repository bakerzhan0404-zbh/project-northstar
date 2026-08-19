# Week 3 — Validation Case and Business-Case Evidence Plan

**Prepared by:** Baker

**Prepared date:** 18 August 2026

**Status:** Analyst validation case for Steering Committee review; not an investment case or funding request

**Classification:** Confidential — Project Northstar simulated client material

## Decision requested

Retain **federated coordination** as the direction for detailed design and bounded evidence mobilization, subject to the existing non-compensating gates. Do **not** approve production change, cash movement, account closure, labor removal, funded benefits, or implementation spend from this document.

Authorize Finance, Treasury, Shared Services, IT, Legal/Tax, Regional Finance, Procurement, and control owners to complete the value and cost evidence packages required for a later investment decision. The FY2026 `$1.0–$1.5m` initial transformation envelope is a **ceiling only**—not an implementation-cost estimate, approved budget, spend authority, committed funding, or ROI denominator.

## Executive conclusion

The supplied evidence supports a **validation case**, not a bankable business case:

- Three diagnostic cases test `$21m / $35m / $46.2m` liquidity screens, `2 / 4 / 4` closure-validation candidates, `$3,900 / $7,800 / $7,800` arithmetic portfolio-fee sensitivities, and `50 / 150 / 150` productive-capacity hours per month. The downside `$3,900` is independently `50% × $7,800`; it is not the fee total for the two-candidate hypothesis.
- None of those quantities is a validated benefit. Cash, P&L, and capacity validated/funded/recognized fields remain `$0`; risk exposure and value are not quantified, with `$0` appearing only as the current recognized-value ledger entry.
- Cash release, annual P&L, capacity, and risk remain separate and non-additive. Capacity remains in hours and is not converted to labor or P&L.
- Actual implementation and run costs, benefit start, ramp, persistence, attribution, discount rate, and approved horizon are unavailable. ROI, NPV, payback, and a funding case therefore cannot be calculated responsibly.
- The manager downside does not change the **design-direction** recommendation because federated coordination was selected for evidence fit, controls, local rights, staged integration, and reversibility—not because a particular value number was assumed. It does not prove that the recommendation is affordable or investable.

## Scenario view — diagnostic quantities, not benefits

| Scenario | 14-day liquidity screen | Closure-validation candidates | Arithmetic fee sensitivity | Productive-capacity hypothesis | Current validated / funded / recognized value |
|---|---:|---:|---:|---:|---:|
| Manager challenge / downside | `$21.0m` | 2 | `$3,900/year` independent portfolio sensitivity | 50 hours/month | `$0 / $0 / $0` |
| Base diagnostic hypothesis | `$35.0m` | 4 | `$7,800/year` | 150 hours/month | `$0 / $0 / $0` |
| Upper diagnostic hypothesis | `$46.2m` | 4 | `$7,800/year` | 150 hours/month | `$0 / $0 / $0` |

### Evidence retained from Week 2

- The 14-day `$21m` threshold passes `168/168` complete windows; `$35m` passes `138/168`; `$46.2m` passes `0/168`. These are screen results, not a cash forecast or mobility proof.
- Four accounts meet the narrow dormant + legacy + zero-supplied-payments screen. Their `$7,800` total is estimated annual fees, not approved closures or realized P&L. Ten closures remain unsupported.
- Among those four evidenced candidates, any two candidate fee estimates total between `$1,800` and `$6,000`. The `$3,900` downside is a separate 50% portfolio sensitivity and does not identify which two accounts validate.
- The management-estimated process baseline is `617.72` hours/month. The process-file payment-repair estimate is `102.60` hours/month and the supplied-payment-file estimate is `55.78` hours/month; the sources are independent and cannot be added or substituted without reconciliation.
- The supplied payment extract covers 7,600 records and `$198.14m` of translated payment intent, not a certified enterprise population or confirmed settlement.

The full governed cases are in `data/processed/W3_business_case_scenarios.csv`.

## Four-value ledger — keep unlike value types separate

| Value category | Diagnostic quantity used | What it is not | Current recognized value | Gate owner |
|---|---|---|---:|---|
| Cash release | `$21m / $35m / $46.2m` liquidity screens | Surplus cash, transferable cash, funding action, interest saving, or transfer authority | `$0` | Group Treasurer; Finance validates recognition |
| Annual P&L | `$3,900 / $7,800 / $7,800` portfolio sensitivities; any two evidenced candidates span `$1,800–$6,000` | Selected-account fee total, approved closure, invoice proof, fee removal, or net saving | `$0` | Finance; local account owners validate closure |
| Capacity | `50 / 150 / 150` hours/month hypotheses | Observed removable work, headcount reduction, cash saving, or P&L | `$0` | Shared Services Lead; Finance approves value treatment |
| Risk | Exposure and value are `NOT QUANTIFIED` | Zero exposure, monetized loss avoidance, or probability-adjusted benefit | `$0` recognized-value ledger entry only | Management control owner; Finance validates valuation |

Do not add these categories. A cash balance that becomes movable is a balance-sheet or funding decision, not automatically annual earnings. Productive capacity is an operating quantity, not automatically a cash or P&L saving. Risk can be described before it can be priced, but it cannot enter return calculations without an approved exposure and valuation method.

The row-level ledger and required gate IDs are in `data/processed/W3_business_case_value_ledger.csv`.

## Why a return calculation is blocked

| Required input | Current evidence | Model treatment |
|---|---|---|
| Validated cash mobility and actual funding action | Not established | Cash-release value fixed at `$0` |
| Account closure and actual fee removal | Four candidates only; fees estimated | Annual P&L fixed at `$0` |
| Observed/removable work and productive redeployment | Management estimates; source mismatch unresolved | Capacity retained in hours; monetary value fixed at `$0` |
| Risk baseline and approved valuation | Not supplied | Exposure/value `NOT QUANTIFIED`; only the current recognized-value ledger entry is `$0` |
| Implementation and recurring costs | Not supplied | Cost status is `NOT AVAILABLE`; no numeric cost is populated |
| Benefit start, ramp, persistence, and attribution | Not supplied | No benefit cash-flow schedule |
| Discount rate and investment horizon | Not approved | No NPV |
| Cost and benefit timing | Not available | No payback |

As a result:

- **ROI:** not available.
- **NPV:** not available.
- **Payback:** not available.
- **Funding recommendation:** not available.

The model intentionally contains no calculated ROI, NPV, payback, total-benefit, net-benefit, or benefit-cost-ratio fields.

## Cost evidence required before investment review

| ID | Cost category | Minimum evidence | Proposed owner |
|---|---|---|---|
| CR01 | Software, licenses, and subscriptions | Vendor quote by module, user, volume, term, currency, renewal, and indexation | CIO / Procurement |
| CR02 | Integration and data engineering | Estimate by bank interface, three ERP environments, data remediation, test, and legacy transition | CIO / Enterprise Architecture |
| CR03 | Cybersecurity, access, and control assurance | Resourced design and test estimate for SoD, access, audit, resilience, and cybersecurity | CISO / management control owner |
| CR04 | Pilot, testing, and program delivery | Internal/external resource plan, environments, QA, PMO, and rollback rehearsal | Program sponsor / PMO |
| CR05 | Change, training, and local adoption | Bottom-up role/region training, procedure, validation, travel, and hypercare estimate | Business change lead / Regional Finance |
| CR06 | Internal capacity and backfill | Named role effort, loaded rates, approved backfill, and treatment of business-as-usual work | Functional owners / Finance |
| CR07 | Bank, account, transfer, tax, and FX costs | Actual tariffs, closure charges, transfer costs, leakage, FX, and local-market costs | Treasury / Tax / Procurement |
| CR08 | Run support, hosting, and service management | Steady-state service, hosting, monitoring, data operations, incident, and control costs | CIO / service owners |
| CR09 | Decommissioning, exit, and contingency | Dual-run, retention, termination, rollback, legacy exit, and risk-based contingency | CIO / Procurement / Finance |
| CR10 | Cost and benefit timing model | Finance-approved low/base/high ranges, monthly timing, ramp, persistence, attribution, rate, and horizon | Finance |

All ten requirements are open. Do not calculate returns or decide funding until they are populated. Their detailed source-document and timing requirements are in `data/processed/W3_cost_evidence_requirements.csv`.

## Value evidence gates

### Cash release · VG01–VG05

Before any cash value is recognized, the evidence package must establish:

1. Authoritative balance type, source timestamp, reconciliation, lineage, and owner by account.
2. Legal, tax, regulatory, operating-purpose, and local transferability certification.
3. Approved operating buffers; complete payments, receipts, forecasts, seasonality, settlement calendars, and extraordinary funding events.
4. Transfer timing, facility use, borrowing rates, transfer charges, tax leakage, FX effects, and the counterfactual funding action.
5. A Finance-approved cash-release definition, value owner, measurement window, attribution rule, and realization evidence.

### Annual P&L · VG06–VG07

Each account candidate requires local validation of receipts, direct debits, linked services, signatories, regulatory purpose, tax requirements, and continuity. P&L recognition additionally requires the actual invoice baseline, closure cost, completed closure, verified fee removal, measurement period, and Finance approval.

### Productive capacity · VG08–VG10

The process and payment populations must first reconcile. A time study must distinguish required control work, avoidable rework, displaced demand, and implementation effort. A capacity claim then requires sustained removal, named productive redeployment, no service/control degradation, and Finance-approved treatment. Until then, report hours only.

### Risk · VG11–VG12

Risk monetization requires a defined event and exposed population; incident/control-failure baseline; likelihood, severity, and loss history; evidence that the intervention changes exposure; and a Finance-approved valuation and attribution method. Until then, report control performance and incidents without a dollar value.

The detailed register is in `W3_assumptions_register.csv`.

## Manager challenge — does the recommendation survive?

**Challenge:** assume only `$21m` remains in the liquidity screen, only two of four account candidates validate, an independent 50% portfolio-fee sensitivity equals `$3,900`, and only 50 hours/month becomes productive capacity. The actual estimated fee total for any two evidenced candidates can range from `$1,800` to `$6,000`.

**Answer:** yes, the recommendation survives **as a conditional design direction**. It does not survive as an investment or value claim because no scenario currently has validated value or cost.

Why the direction remains:

1. The Week 2 problem is an ownership, data, control, and decision-chain gap, not merely a value-quantum opportunity. Federated coordination directly addresses that gap while retaining local operating and emergency rights.
2. The same no-regret evidence work is necessary under the downside: authoritative balance data, mobility certification, four-account local validation, reconciled payment/process baselines, reason coding, controls, and benefit ownership.
3. The option leads the current five plausible weighted sensitivities because of evidence fit and balanced feasibility—not because the `$35m`, four-account, or 150-hour hypotheses were added into its score.
4. Bounded tests and explicit exit paths make the evidence work reversible. A failed hypothesis should stop or narrow the intervention rather than create a sunk-cost argument for scale.

What the downside changes:

- It reduces the quantities available for validation and reinforces that account closure is secondary.
- It increases the importance of designing the initial stage around evidence acquisition and no-regret controls.
- It prevents any claim that the current analysis funds the program.
- If global data/control ownership is not confirmed, minimum integration readiness is absent, or a bottom-up initial-stage cost cannot fit the `$1.0–$1.5m` ceiling, the decision switches to **local stabilization** while preserving the common data/control minimum.

## Later formulas — inactive until gates close

These formulas define what Finance may calculate later; they are **not active in the current model**:

- `Certified movable cash = Σ account-level amount passing VG01–VG05`.
- `Realized funding P&L = evidenced change in net external funding/interest/fees attributable to certified action − incremental transfer/tax/FX cost`.
- `Realized account-fee P&L = actual removed recurring fees − closure and replacement-service costs`.
- `Productive capacity = observed avoidable hours sustainably removed × validated redeployment rate`; keep in hours unless a Finance-approved monetary consequence exists.
- `Risk value = approved change in expected loss or another approved risk measure`; do not use qualitative control improvement as dollars.
- `ROI, NPV, and payback` may be calculated only after CR01–CR10 and the relevant value gates provide approved, time-phased cash flows without double counting.

## Stage-gate path to an investable case

| Gate | Minimum output | Decision enabled | Current status |
|---|---|---|---|
| 1 · Evidence baseline | Reconciled sources/populations, approved metric contracts, value owners | Confirm what can be tested | Open |
| 2 · Local and control certification | Mobility/closure evidence, control design, service/rollback criteria | Approve bounded validation activity | Open |
| 3 · Observed pilot evidence | Four compliant weeks, observed time, incident/service record, actual fee/cost evidence | Validate benefit quantities and confidence | Not started |
| 4 · Costed initial stage | CR01–CR10, low/base/high range, cash-flow timing, contingency | Compare initial stage to the ceiling | Blocked pending evidence |
| 5 · Finance investment review | Recognized benefit cash flows, cost cash flows, attribution, rate, horizon | Calculate ROI/NPV/payback and request funding | Not available |
| 6 · Scale decision | Demonstrated Wave 1 benefits and control/service performance | Consider larger staged approval | Not available |

Passing a later gate does not retroactively convert a Week 2 screen into a benefit. Each value must enter the ledger through its own evidence owner and Finance recognition decision.

## Model controls and reproducibility

`src/week3_business_case.py` regenerates the scenario table, non-additive value ledger, cost-evidence requirements, model controls, and assumptions register. `tests/test_week3_business_case.py` checks Week 2 reconciliation, exact scenario inputs, zero-value boundaries, cost completeness, envelope interpretation, non-additivity, deterministic output, and fail-closed mutations.

Current executable result: all **38 automated checks** pass. Separately, the model writes **12 model-control records** labelled `MODEL CONTROL PASS`; each also carries an `OPEN` or `BLOCKED` evidence-gate status so a passing model control cannot be read as closed client evidence. The control evidence is in `data/processed/W3_business_case_controls.csv`.

## Final boundary

Project Northstar currently has enough evidence to select a **direction for controlled learning** and to specify what an investable case would require. It does not have enough evidence to claim movable cash, recognized savings, monetized capacity, monetized risk, implementation cost, return, payback, or spend authority. Those fields remain closed by design.
