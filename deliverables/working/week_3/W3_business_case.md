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
- Actual implementation and run costs, benefit start, ramp, persistence, attribution, discount rate, and approved horizon are unavailable. ROI, NPV, payback, and a funding case therefore cannot be calculated responsibly. A provisional `ANALYST-ASSUMPTION` cost range is stated separately — one-time `$755k / $1,155k / $1,715k` and recurring `$175k / $281k / $442k` per year — for planning only; the base case fits the FY2026 ceiling while the high case breaches it and would return for staged approval.
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
| Implementation and recurring costs | Not supplied; a provisional `ANALYST-ASSUMPTION` range is stated separately | Cost status is `NOT AVAILABLE`; no numeric cost is populated in the value model |
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

All ten requirements are open. Do not calculate returns or decide funding until they are populated. A provisional low/base/high range for these same ten categories is given in the next section; it is a planning aid, not evidence, and does not close any requirement. Their detailed source-document and timing requirements are in `data/processed/W3_cost_evidence_requirements.csv`.

## Provisional cost estimate — one-time and recurring

The ten cost requirements above remain **open**: no vendor quote, statement of work, or rate card has been supplied, and nothing in this section closes them. What follows is a **provisional planning range** so that "cost is unavailable" is not read as "cost is unknowable." Every figure is `ANALYST-ASSUMPTION` — an analyst allocation of the disclosed FY2026 ceiling by Wave-1 scope tier, with a stated basis per line. None is evidence, and none can be used to authorize spend.

One-time and recurring costs are kept separate because they are funded differently: the one-time case is what the FY2026 `$1.0–$1.5m` envelope is a ceiling for; the recurring run rate begins only after go-live and requires its own budget line that no one has yet approved.

| ID | Cost category | One-time low / base / high | Recurring per year low / base / high |
|---|---|---:|---:|
| CR01 | Software, licenses, subscriptions | `$40k / $75k / $120k` | `$60k / $95k / $150k` |
| CR02 | Integration and data engineering | `$220k / $320k / $470k` | `—` |
| CR03 | Cybersecurity, access, control assurance | `$70k / $110k / $165k` | `$25k / $40k / $60k` |
| CR04 | Pilot, testing, program delivery | `$150k / $215k / $300k` | `—` |
| CR05 | Change, training, local adoption | `$60k / $95k / $140k` | `$10k / $18k / $30k` |
| CR06 | Internal capacity and backfill | `$120k / $175k / $250k` | `—` |
| CR07 | Bank, account, transfer, tax, FX | `$15k / $30k / $55k` | `$5k / $10k / $20k` |
| CR08 | Run support, hosting, service management | `$20k / $35k / $55k` | `$70k / $110k / $170k` |
| CR09 | Decommissioning, exit, contingency | `$45k / $75k / $120k` | `—` |
| CR10 | Cost and benefit timing model | `$15k / $25k / $40k` | `$5k / $8k / $12k` |
| | **Total** | **`$755k / $1,155k / $1,715k`** | **`$175k / $281k / $442k`** |

### What the range tells the Steering Committee

1. **The base case fits the envelope.** A `$1,155k` one-time Wave 1 sits inside the `$1.0–$1.5m` ceiling. Affordability is plausible — not demonstrated.
2. **The high case breaches it.** At `$1,715k` the one-time cost exceeds the ceiling by `$215k`, which under the FY2026 constraint returns for staged CFO/SteerCo approval after demonstrated Wave 1 benefits rather than proceeding. The affordability question is therefore live, not settled.
3. **The recurring line is the one most often missed.** A `$281k` base run rate is roughly a quarter of the one-time cost *every year*, indefinitely, and it is not covered by the FY2026 envelope at all. It needs its own approved budget before go-live, not after.
4. **The spread is wide because the evidence is absent.** High is roughly `2.3×` low. That spread is the honest width of an unsourced estimate; it should narrow as CR01–CR10 close, and a narrower range should not be claimed before they do.

### What this does not do

- It does **not** close CR01–CR10. Their evidence status remains `OPEN` and their cost status remains `NOT AVAILABLE`.
- It does **not** create a return. ROI, NPV, and payback stay unavailable because the *benefit* side is still `$0` — a cost estimate alone cannot produce a return.
- It does **not** authorize spend, procurement, or commitment.
- It assumes the federated direction and the Wave-1 scope in the two pilot charters. A switch to local stabilization would require a different estimate.

The reproducible line-by-line model, including each estimate's stated basis, is in `data/processed/W3_provisional_cost_estimates.csv`, generated and validated by `src/week3_business_case.py`.

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

## Illustrative planning scenarios — analyst assumption, not a business case

Zero recognized cash, P&L, and capacity value is an appropriate **control boundary**: it stops an unvalidated number from being spent, booked, or reported as if it were certified. It is not a substitute for a working business case, and it should not be read as "no planning view exists." Finance and the Steering Committee still need a distinction between **validated value** (stays `$0` until VG01–VG12 close, no matter how this section reads) and **hypothetical opportunity** (a bounded, clearly labelled range useful for sequencing and affordability conversation while that evidence work proceeds).

The table below is that range. Every figure is `ANALYST-ASSUMPTION`, reproducible from `src/week3_business_case.py`, and excluded from `validated_value_usd`, `funded_value_usd`, `recognized_value_usd`, the four-value ledger, and any ROI/NPV/payback calculation. It does not relax BC01–BC12, and it is not a funding request.

| Dimension | Conservative (downside-anchored) | Base | Upside |
|---|---|---|---|
| Anchored diagnostic case | `$21m` screen, 2 candidates, 50 hours/month | `$35m` screen, 4 candidates, 150 hours/month | `$46.2m` screen, 4 candidates, 150 hours/month |
| Illustrative Wave-1 cost range | `$1.0m` (bottom of the disclosed ceiling; narrowest scope: visibility census plus one bounded payment cohort) | `$1.15m–$1.35m` (mid ceiling; both pilot charters at standard scope) | `$1.35m–$1.5m` (top of the disclosed ceiling; full Wave-1 scope) |
| Cost basis | Illustrative allocation of the already-disclosed `$1.0–$1.5m` FY2026 ceiling by Wave-1 scope tier — **not** a vendor-sourced or bottom-up estimate; CR01–CR10 evidence still governs any real cost | Same basis | Same basis; any cost above `$1.5m` returns for staged CFO/SteerCo approval after demonstrated Wave 1 benefits |
| Earliest possible benefit-realization start | Month 5 | Month 5 | Month 5 |
| Ramp-up period (start to steady state) | 6–9 months | 4–6 months | 3–4 months |
| Illustrative steady-state month | Month 11–14 | Month 9–11 | Month 8–9 |
| Illustrative program duration (decision day through steady state) | 11–14 months | 9–11 months | 8–9 months |

**Why every tier shares a Month 5 floor:** the earliest possible go/no-go follows the existing 90-day evidence-mobilization timebox (~Month 3 from the 18 August 2026 decision day). Any wave that changes North America payment-routing or approval-workflow production cannot execute inside the confirmed eight-week NA Q4 change-freeze and requires separate NA BU CFO sign-off (see `W3_payment_pilot_charter.md`), which pushes the earliest funded North America production start to Month 5 regardless of scenario tier or how quickly evidence closes. Data cleanup, design, testing, and low-risk account validation are not subject to this floor and can continue inside the freeze window. Optimism narrows the ramp-up and steady-state range; it cannot move the freeze-driven floor.

**Key sensitivities:**

1. **Evidence-gate closure rate** (VG01–VG12, CR01–CR10) — late closure shifts every month in the table to the right by the same margin.
2. **NA Q4 freeze calendar** — exact dates remain TBD from NA BU Finance; a freeze that starts before Day 90 pushes the Month 5 floor later still.
3. **Closure-validation and capacity-conversion rates** (2 vs. 4 candidates; 50 vs. 150 hours/month) — move eventual benefit magnitude, not this timeline.
4. **Bottom-up CR01–CR10 cost outcome versus the disclosed ceiling** — a cost above `$1.5m` returns for staged CFO/SteerCo approval rather than proceeding within this Wave-1 range.
5. **Global data/control ownership, minimum integration readiness, and affordability** — failing any one switches the direction to local stabilization, which this federated-only range does not model.

The reproducible detail is in `data/processed/W3_business_case_scenario_planning.csv`, generated and validated alongside the other four governed outputs by `src/week3_business_case.py`.

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

`src/week3_business_case.py` regenerates the scenario table, non-additive value ledger, cost-evidence requirements, model controls, assumptions register, the illustrative Wave-1 planning range, and the provisional one-time/recurring cost estimate. `tests/test_week3_business_case.py` checks Week 2 reconciliation, exact scenario inputs, zero-value boundaries, cost completeness, envelope interpretation, non-additivity, the illustrative planning-range schema and NA Q4 floor reconciliation, deterministic output, and fail-closed mutations.

Current executable result: all **51 automated checks** pass. Separately, the model writes **12 model-control records** labelled `MODEL CONTROL PASS`; each also carries an `OPEN` or `BLOCKED` evidence-gate status so a passing model control cannot be read as closed client evidence. The control evidence is in `data/processed/W3_business_case_controls.csv`. The illustrative planning range writes **3 rows**, each labelled `ANALYST-ASSUMPTION` and explicitly excluded from recognized value, in `data/processed/W3_business_case_scenario_planning.csv`. The provisional cost estimate writes **10 rows**, one per cost requirement, in `data/processed/W3_provisional_cost_estimates.csv`; a passing model control there confirms the range is ordered, labelled, and inside the disclosed ceiling — not that any cost has been evidenced.

## Final boundary

Project Northstar currently has enough evidence to select a **direction for controlled learning** and to specify what an investable case would require. It does not have enough evidence to claim movable cash, recognized savings, monetized capacity, monetized risk, implementation cost, return, payback, or spend authority. Those fields remain closed by design.
