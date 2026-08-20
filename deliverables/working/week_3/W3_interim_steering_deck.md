# Week 3 — Interim Steering Deck Source

**Audience:** CFO, Group Treasurer, Steering Committee

**Format:** 16:9, maximum 10 slides

**Status:** Analyst proposal for decision alignment; design and evidence mobilization only

**Prepared date:** 18 August 2026

**Classification:** Confidential — Project Northstar simulated client material

## Slide 1 — Advance federated design—not execution

### On-slide copy

**Decision today**

- Advance federated coordination as the direction for detailed design and a 90-day evidence-mobilization plan.
- Retain local stabilization as the controlled fallback; hold global coordination until the critical gates close.
- Confirm that this decision authorizes no production change, cash movement, closure, labor action, benefit, or spend.

**Boundary strip:** The FY2026 `$1.0–$1.5m` initial-stage envelope is a ceiling only—not a cost estimate, approved budget, or permission to spend.

### Visual grammar

Dark board-ledger opener with one decision statement, a three-part direction strip (`advance / retain / hold`), and a visible authorization boundary. No hero image or logo.

### Speaker notes

Open with the decision, not the work completed. The recommendation is deliberately conditional: federated coordination best fits the evidence and preserves local rights, but every option remains design-only. “Advance” means assign owners and close evidence gaps; it does not mean launch either pilot. The initial funding envelope is a non-compensating affordability constraint. A bottom-up cost and a separate CFO/SteerCo approval are still required.

### Provenance

- `deliverables/working/week_3/W3_strategic_options.md` — decision requested, gates, scores, and switching conditions (`ANALYST-JUDGMENT`).
- `deliverables/working/week_3/W3_future_state_operating_model.md` — decision purpose and stage boundaries (`ANALYST-JUDGMENT`).
- `deliverables/working/week_3/W3_business_case.md` — envelope and no-spend boundary (`ACG-DATA` / `ANALYST-JUDGMENT`).

## Slide 2 — The evidence points to concentrated friction, not a proven cash or efficiency benefit

### On-slide copy

| Evidence readout | What it supports | What it does not support |
|---|---|---|
| `23 / 55` accounts delayed under the reporting-date proxy; all 23 use portal or spreadsheet | Target source ownership and timestamp controls | Start-of-day performance or causal attribution |
| `$38.13m` at 30 June under the 14-day screen | Test mobility certification and buffer governance | Cash, surplus, or transfer authority |
| `7,600` supplied payment records; priority union has `2,839` records | Define a bounded diagnostic population | A certified ACG-wide population |
| `356` priority-union exceptions and `14,939` repair minutes | Prioritize root-cause evidence | Cause, removability, P&L, or headcount action |

**Readout:** The next decision is how to close evidence gaps safely—not how much value to book.

### Visual grammar

Lab-results evidence table with four numeric readouts, a narrow interpretation column, and an explicit “does not prove” column. Keep `$38.13m` visually tagged as `SCREEN`.

### Speaker notes

The visibility analysis covers 55 accounts and 9,955 account-days from January through June 2026. The delay measure is a reporting-date proxy because receipt timestamps and approved cutoffs are absent. The `$38.13m` figure is the 30 June 14-day screen; the `$35m` threshold passes 138 of 168 complete windows, but no account-level mobility certification exists. The payment evidence is limited to the supplied extract. Manual touch and cross-border status are associated with friction; they are not established causes. Do not add the two repair-hour sources or translate them into labor value.

### Provenance

- `deliverables/working/week_2/W2_findings_log.md` — F07–F10 and stated limitations (`ANALYST-CALC`).
- `deliverables/working/week_2/W2_metric_contract.md` — denominators, proxy definitions, and boundaries.
- `data/processed/W2_visibility_diagnostic.csv`, `data/processed/W2_liquidity_scenarios.csv`, and `data/processed/W2_payment_diagnostic.csv` — reproduced Week 2 outputs.
- `deliverables/working/week_3/W3_design_principles.md` — evidence-to-design consequences.

## Slide 3 — Federated leads at 87—subject to seven open gates

### On-slide copy

| Direction | Weighted score / 100 | Steering posture |
|---|---:|---|
| Local stabilization | 72 | Retain as fallback |
| **Federated coordination** | **87** | **Advance detailed design** |
| Globally coordinated | 60 | Hold pending gates |

**Robustness:** Federated remains the numerical leader in all five declared stakeholder-weight cases.

**Seven non-compensating gates:** authoritative data and ownership; legal/local rights; controls/cyber; service/peak continuity; resilience/rollback; affordability/staging; benefit recognition.

### Visual grammar

Editable horizontal bar chart for `72 / 87 / 60`, with a right-side gate ledger showing all seven as `OPEN`. The 87 score is accented; the gate ledger, not the chart, carries the decision-status color.

### Speaker notes

The scores are ordinal analyst judgments, not confidence scores, value estimates, or approval readiness. The weights were locked before scoring and sum to 100%. Federated leads the base case and controls-first, speed-first, scale/value-first, and local-autonomy-first sensitivities. That robustness supports choosing a direction for learning; it cannot compensate for a failed gate. Global coordination is held because it depends most heavily on unresolved architecture, local-right, resilience, cost, and mobility evidence.

### Provenance

- `deliverables/working/week_3/W3_strategic_options.md` — criteria, scores, five sensitivities, seven gates, and switching conditions.
- `data/processed/W3_option_summary.csv`, `data/processed/W3_option_weighted_scores.csv`, and `data/processed/W3_option_sensitivity.csv` — reproducible option outputs.
- `src/week3_strategy.py` and `tests/test_week3_strategy.py` — model and controls.

## Slide 4 — One global spine can preserve local rights while tightening the decision chain

### On-slide copy

| Decision-chain layer | Enterprise responsibility | Regional / local right | Required proof |
|---|---|---|---|
| 1. Standards and evidence | Group Treasury owns policy, definitions, KPI, and escalation | Validate calendar, restrictions, purpose, and service context | Source, owner, definition, lineage |
| 2. Position and intake | Governed cash position and controlled payment request | Challenge invalid facts; protect critical needs | Reconciliation, approvals, exceptions |
| 3. Decision | Funding or policy decision within delegated authority | Block infeasible action; invoke governed emergency path | Authority, rationale, local attestation |
| 4. Execution | Shared Services or approved enterprise route | Execute approved local action where required | Acknowledgement, status, audit trail |
| 5. Learn and correct | Enterprise KPI, control, and benefit governance | Own local/source corrective action | Outcome, reconciliation, decision log |

**Design rule:** Global standards and evidence ownership; regional/local validation and service context; controlled decisions; confirmed outcomes.

### Visual grammar

Five-row operating ledger with a continuous vertical spine. Blue denotes enterprise standard; teal denotes local right; amber denotes required proof. Avoid a decorative org chart.

### Speaker notes

This is a decision-rights model, not an application architecture. It does not select a platform, bank, vendor, or ERP end state. Group Treasury owns the common data/control spine and enterprise decisions. Regional and local teams retain explicit rights to validate restrictions and operating needs, protect payroll/tax/refunds/critical suppliers, challenge unsafe actions, and use an approved contingency route. Shared Services operates standardized payment steps. IT/Data/Cyber enables source integrity, access, resilience, and rollback. Management owns controls; Internal Audit is consulted.

### Provenance

- `deliverables/working/week_3/W3_future_state_operating_model.md` — governance, data ownership, cash and payment cycles, and local rights.
- `deliverables/working/week_3/W3_future_state_process_map_and_RACI.md` — process map, decision rights, and one-accountable-owner RACI.
- `deliverables/working/week_3/W3_control_inventory.csv` — proposed control gates.

## Slide 5 — Visibility readiness starts with 55-account control, then a 10-account read-only test

### On-slide copy

| Design element | Locked proposal | Acceptance / stop boundary |
|---|---|---|
| Readiness census | All `55` accounts / `9,955` supplied account-days | 100% source, timestamp, cutoff, balance, owner, calendar, and reconciliation contract before launch |
| Provisional cohort | `10` delayed accounts: 5 spreadsheet + 5 portal | Covers 3 regions, 3 ERPs, and 4 banks; purposive, not representative |
| Protected case | `AC0040`: APAC, Payroll, restricted | Read-only shadow observation only; enhanced review or documented substitution |
| Later operating test | Minimum 4 comparable weeks | `≥95%` on-time; `100%` reconciled or formally explained; `0` defined critical-service failures; `0` confirmed control breaches |
| Recovery | Approved prior process | Rollback rehearsed at or below `4 hours` before launch or scale |

**Boundary:** No liquidity, borrowing, cash-release, fee, or capacity KPI is an acceptance measure.

### Visual grammar

Lab-run-results table: three evidence blocks (`census / cohort / safeguards`) plus a bottom acceptance strip. Treat AC0040 as an amber exception, not a failed account.

### Speaker notes

The ten accounts are a reproducible coverage-constrained design, not a launch-ready sample. All ten require base readiness/control review. AC0040 alone requires enhanced review and can remain only in read-only shadow observation subject to owner approval. The goal is to replace the reporting-date proxy with governed receipt timestamps, cutoffs, and reconciliation. Four compliant weeks would complete the technical test, but completion would not authorize movement, value, procurement, or scale. Any missing owner, cost range, control sign-off, service definition, blackout decision, or rollback rehearsal is a no-go.

### Provenance

- `deliverables/working/week_3/W3_visibility_pilot_charter.md` — scope, sample rule, KPIs, gates, and no-scale conditions.
- `data/processed/W3_visibility_pilot_candidates.csv` — deterministic cohort and control-review flags.
- `src/week3_pilot_design.py` and `tests/test_week3_pilot_design.py` — selection logic and validation.

## Slide 6 — Payment v3 uses 120 paired reviews to diagnose causes

### On-slide copy

| Per mutually exclusive stratum | Selection | Purpose |
|---|---:|---|
| Exception / status issues | 8 | Diagnose exception, Repaired, or Rejected cases |
| Late-only issues | 7 | Preserve timing evidence without double-counting issue modes |
| Completed, flag-negative controls | 15 | Create a within-stratum comparator |
| **Per stratum / four strata** | **30 / 120** | Manual-only; overlap; cross-border-wire-only; neither |

**Matching result:** `50` exact four-field pairs + `10` visible nearest-match deviations; no replacement.

**Go-forward rule:** Select an intervention only after source linkage and evidence-based root-cause coding; preserve controls, critical flows, comparability, blackout rules, and four-hour rollback.

### Visual grammar

Compact root-cause sampling table with a `8 + 7 + 15 = 30` equation band and a four-stratum footer. A small matching-quality strip shows `50 exact / 10 deviations` without implying statistical power.

### Speaker notes

The four strata are mutually exclusive, so overlapping manual-touch and cross-border totals are never added. Within each stratum, rank exception/status and late-only modes separately, then match without replacement on payment type, region, month, and amount band where feasible. This is purposive case-control diagnosis. It is not a powered prevalence sample, an ACG-wide extrapolation, or a benefit sample. No root cause is established today because source documents, criticality, reason codes, and event sequences are missing. A later process test remains TBD until an evidenced, remediable cause and like-for-like baseline exist.

### Provenance

- `deliverables/working/week_3/W3_payment_pilot_charter.md` — v3 sampling, evidence, intervention, control, and stop rules.
- `data/processed/W3_payment_sample_frame.csv` and `data/processed/W3_pilot_model_controls.csv` — deterministic sample and controls.
- `src/week3_pilot_design.py` and `tests/test_week3_pilot_design.py` — reproducible selection and fail-closed checks.

## Slide 7 — Four value ledgers stay separate; recognized value remains zero

### On-slide copy

| Value ledger | Diagnostic quantity | Recognized today | Evidence gate |
|---|---|---:|---|
| Cash release | `$21m / $35m / $46.2m` liquidity screens | `$0` | VG01–VG05: source, mobility, buffers, economics, Finance recognition |
| Annual P&L | `$3,900 / $7,800 / $7,800` fee sensitivities | `$0` | VG06–VG07: closure proof, actual fee removal, costs, Finance approval |
| Productive capacity | `50 / 150 / 150` hours per month | `$0` | VG08–VG10: reconciled scope, observed removal, productive redeployment |
| Risk | Exposure and value `NOT QUANTIFIED` | `$0` recognized-ledger entry only | VG11–VG12: event, exposure, likelihood/severity, intervention effect, valuation |

**Do not add the rows.** Actual cost, ROI, NPV, payback, and funding recommendation are unavailable.

### Visual grammar

Four-row compact ledger with diagnostic quantities in neutral gray and recognized values in a strict zero column. Use no “total benefit” box. Put `NOT QUANTIFIED` in amber, not green or red.

### Speaker notes

The scenarios are diagnostic cases, not benefits. The downside `$3,900` is independently 50% of the `$7,800` portfolio sensitivity; it is not the fee total of a selected two-account cohort. Any two evidenced closure candidates could total `$1,800–$6,000`. Capacity stays in hours and is not converted to headcount or P&L. Risk exposure is unknown; the zero is only the present recognized-value ledger entry, not zero risk. CR01–CR10 are all open, so there is no responsible return calculation or funding case.

### Provenance

- `deliverables/working/week_3/W3_business_case.md` — scenario treatment, separate ledgers, and return block.
- `data/processed/W3_business_case_scenarios.csv`, `data/processed/W3_business_case_value_ledger.csv`, and `data/processed/W3_cost_evidence_requirements.csv` — governed model outputs.
- `deliverables/working/week_3/W3_assumptions_register.csv` — VG01–VG12 and scenario assumptions.

## Slide 8 — The downside preserves the design direction, while ownership and affordability can still force a switch

### On-slide copy

**What survives under the manager challenge**

- `$21m` screen, `2` closure candidates, independent `$3,900` fee sensitivity, and `50` hours/month.
- Federated remains a direction for common ownership, controls, local rights, and reversible learning.
- The same evidence work is required even when the diagnostic quantities fall.

**What changes the direction**

- Switch to local stabilization if global data/control ownership, minimum integration readiness, or an affordable 90-day mobilization cannot be established.
- Reconsider global coordination only after legal/local, architecture, cyber/resilience, cost, mobility, and rollback evidence close and scale/value priorities materially dominate.
- Remove or redesign any option that fails a critical gate.

**Boundary:** The downside does not produce an investment case; every current scenario has zero validated value and unavailable cost.

### Visual grammar

Open two-column comparison: `direction survives` versus `switch condition`. Use a center hinge labelled `gates`, not a decorative arrow.

### Speaker notes

This is the deck’s falsification test. The recommendation survives smaller hypotheses because the option score does not include the scenario values. It does not survive failure of the common ownership, integration-readiness, affordability, or critical-control conditions. Local stabilization is the immediate fallback and must preserve a minimum governed group feed. Global coordination is not the next automatic phase; it must earn reconsideration through materially stronger evidence and a separate decision.

### Provenance

- `deliverables/working/week_3/W3_business_case.md` — manager challenge and evidence boundary.
- `deliverables/working/week_3/W3_strategic_options.md` — switching conditions and extreme-weight sensitivities.
- `data/processed/W3_business_case_scenarios.csv` and `data/processed/W3_option_sensitivity.csv` — model inputs and sensitivity outputs.

## Slide 9 — Five owner-led evidence packages now gate launch and funding

### On-slide copy

| Open package | Accountable owner(s) | Evidence required before a later decision |
|---|---|---|
| Data and metric contract | Group Treasurer; CIO enables | Reconciled population, source, timestamp, cutoff, definition, lineage, denominator, owner |
| Local rights and mobility | Group Treasurer; Regional Finance; Legal/Tax consulted | Restrictions, purpose, buffers, transferability, service, approval, review date |
| Controls and cybersecurity | Management control owner; CIO/Cyber | Authorization, SoD, access, audit, duplicate, sanctions, reconciliation, test evidence |
| Service and resilience | BU/Regional Finance; Shared Services; CIO | Critical-flow definition, blackout, monitoring, contingency, `≤4h` rollback rehearsal |
| Cost and value recognition | Finance; Procurement and functional owners | CR01–CR10 cost ranges; VG01–VG12 evidence; timing, attribution, realization, approval |

**Status:** All packages remain open or blocked. A `MODEL CONTROL PASS` confirms model behavior—not client evidence closure.

### Visual grammar

Board risk ledger with owner, evidence, and status columns. Every status is `OPEN` or `BLOCKED`; no averaged readiness score.

### Speaker notes

These packages combine the most decision-relevant risks into named closure work. Data and controls are preconditions, not cleanup after launch. Legal, tax, accounting, cyber, architecture, and service specialists must answer their own questions. Finance owns admission to the value ledger; the CFO/SteerCo separately owns funding and scale. Ten cost requirements and twelve value-gate requirements are defined, but they are not complete. Automated model checks prevent unsafe calculations; they do not transform assumptions into evidence.

### Provenance

- `deliverables/working/week_3/W3_control_inventory.csv` — proposed controls and evidence owners.
- `deliverables/working/week_3/W3_assumptions_register.csv` — VG01–VG12.
- `data/processed/W3_cost_evidence_requirements.csv` and `data/processed/W3_business_case_controls.csv` — CR01–CR10 and model-control status.
- `deliverables/working/week_3/W3_future_state_operating_model.md` — specialist decisions and ownership.

## Slide 10 — Use 90 days to make the next decision evidence-ready, then return for a separate go/no-go

### On-slide copy

| Timebox | Evidence mobilization | Exit readout |
|---|---|---|
| Decision day | Confirm federated direction, accountable owners, local fallback, and no-execution boundary | Recorded agreement/disagreement and named package owners |
| Days 1–30 | Reconcile the 55-account and 7,600-record populations; lock definitions, source owners, calendars, and evidence gaps | Controlled population and metric-contract readout |
| Days 31–60 | Complete local/control/architecture review; develop CR01–CR10 cost ranges; rehearse rollback only in an approved safe environment | Gate register, cost evidence, deficiencies, and remediation owners |
| Days 61–90 | Lock pilot baselines and target rules; assess cohort readiness and evidence completeness | CFO/SteerCo pack recommending `stop / extend evidence work / approve a later bounded pilot`, subject to the confirmed NA Q4 freeze below |

**Confirmed constraint:** North America will not accept payment-routing or approval-workflow production changes during the eight weeks surrounding peak holiday operations (exact dates TBD from NA BU Finance), and any North America production change requires NA BU CFO (Rachel Kim) sign-off. Days 1–90 (data cleanup, design, testing, and low-risk validation) are unaffected, but Day 90 falls near the start of a typical Q4 freeze window — so even a clean evidence-readiness result at Day 90 does not guarantee an immediate North America launch. Treat Month 5 as the earliest realistic North America production start, not Day 90.

**Decisions requested now:** endorse the direction; assign evidence owners; approve the 90-day mobilization timebox; agree that any pilot launch, spend, value, or scale requires a later decision; and confirm that any North America production change also waits for the freeze window to lift and for NA BU CFO sign-off, regardless of evidence-readiness date.

### Visual grammar

Four-band report timeline with a persistent `EVIDENCE ONLY` rail and a confirmed NA Q4 freeze marker. The last band ends at a decision gate, not a launch arrow.

### Speaker notes

Close the loop by repeating the opening decision with the evidence attached. The 90 days are an analyst-proposed mobilization timebox, not a promise that every gate will close. Time does not override evidence: unfinished packages remain open and force an extension, redesign, or switch to local stabilization. No production pilot begins within this plan unless a separate go/no-go is granted after the relevant data, control, service, specialist, cost, and rollback gates are evidenced. Separately, the confirmed NA Q4 change freeze means Day 90 evidence-readiness does not equal a Day 90 North America launch: any wave touching North America payment routing or approval workflows needs the freeze to lift and Rachel Kim's sign-off first, which the illustrative planning range treats as pushing the earliest funded North America production start to Month 5.

### Provenance

- `deliverables/working/week_3/W3_future_state_operating_model.md` — evidence-readiness, pilot, and separate-scale stage gates.
- `deliverables/working/week_3/W3_visibility_pilot_charter.md` and `deliverables/working/week_3/W3_payment_pilot_charter.md` — pre-launch evidence, rollback, stop, and no-scale rules.
- `deliverables/working/week_3/W3_business_case.md` — investability stage gates, cost/value closure requirements, and the illustrative Wave-1 planning range.
- `deliverables/working/week_3/W3_strategic_options.md` — decision, fallback, and no-execution boundary.
- `deliverables/working/week_3/W3_decision_log.md` and `W3_risk_register.csv`/`W3_risk_register.md` (R031) — the confirmed NA Q4 change-freeze constraint and its sequencing effect.
