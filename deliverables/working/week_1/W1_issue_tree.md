# Week 1 — Decision-Led Issue Tree

**Classification:** Confidential — Project Northstar simulated client material; statuses are analyst assessments pending client review

## Executive question

Should ACG authorize a 90-day treasury-transformation mobilization, at what ambition, and with which Wave 1 initiatives and control conditions?

## Prioritized issue tree

| ID | Branch | Decision question | Initial hypothesis | Evidence required | Analysis | Decision affected | Priority | Status |
|---|---|---|---|---|---|---|---|---|
| V1 | Value | How much cash is visible with sufficient timeliness and confidence? | Date-level delays are material, but start-of-day reliability cannot be determined | Timestamped balance receipt, balance type, source quality, reconciliation | Same-day coverage by region, method, and date | Visibility workstream and KPI | High | Unresolved |
| V2 | Value | How much positive cash is genuinely mobilizable? | **At least 50% of gross positive estimated availability—approximately $29m at the 30 June reference date—can ultimately be validated as movable within 24 hours after restrictions and operating buffers.** | Legal/tax transferability, operating buffers, settlement timing, entity rules, timestamped movement capability | Test the 50% / $29m threshold through conservative, base, and upside scenarios | Liquidity design and cash-release case | High | Unresolved |
| V3 | Value | Which accounts create avoidable cost and complexity? | A defined cohort can enter closure validation, but fewer than management's ten may close | Activity, purpose, local need, fees, dependencies, signatories | Candidate criteria and sensitivity | Account rationalization | High | Unresolved |
| V4 | Value | Where is avoidable payment and process effort concentrated? | Payment friction is material enough to justify root-cause segmentation | Exception reason, format, channel, entity, amount, repair time | Segment manual touch, exceptions, late release, and repair | Payment standardization and capacity | High | Supported |
| V5 | Value | Where does receivables reconciliation create delay, manual work, or trapped working capital? | ACG may have reconciliation friction, but the current package cannot test it | AR ledger, invoices, receipts, remittance, match status, reason codes, aging | Match-rate, aging, unapplied-cash, and root-cause diagnostic | Receivables priority and data design | Medium | Unresolved |
| R1 | Risk | Which visibility and funding gaps create liquidity or control exposure? | **Stale reporting leaves more than $15m of positive cash outside timely Group visibility on a typical day and creates more than $5m of liquidity decision exposure.** | Timestamped receipt, daily stale USD value, funding events and terms, transfer timing, restrictions | Test the $15m stale-cash and $5m decision-exposure thresholds; quantify surplus/deficit overlap and duration | Liquidity governance | High | Unresolved |
| R2 | Risk | Which payment failure modes threaten suppliers, customers, or controls? | Late and exception-prone payments cluster in specific workflows | Cutoff timestamps, reason codes, approvals, criticality | Root-cause tree and exposure pathways | Payment controls and service levels | High | Unresolved |
| R3 | Risk | Could centralization concentrate failure risk? | Greater standards improve control only if emergency access, resilience, and segregation are designed explicitly | Access model, BCP, cyber review, emergency process | Failure scenarios and control inventory | Operating-model choice | High | Untested |
| R4 | Risk | Which FX transaction and exposure patterns create avoidable cost or risk? | ACG may have fragmented FX activity, but project rates alone cannot test transactions or exposures | FX trades, exposures, hedge records, spreads/fees, settlement, entity/currency | Volume, offset, timing, cost, and policy diagnostic | FX governance and operating model | Medium | Unresolved |
| F1 | Feasibility | What can be delivered without replacing the three ERPs? | **Without replacing any of the three ERPs, staged connectivity and data ownership can raise same-calendar-day account coverage from 58% to at least 85%—47 of 55 accounts—and reduce estimated observations below 10% within 12 months.** | Account/source coverage, interface inventory, architecture, ERP retirement, data owners, delivery estimates | Build the dependency and coverage-uplift path to 85%; test the below-10% estimated-source target | Wave sequencing | High | Untested |
| F2 | Feasibility | Which legal and local constraints limit pooling or account closure? | A global policy with locally validated exceptions is feasible | Country/entity legal, tax, regulatory, collection, payroll, and resilience requirements | Constraint matrix | Global versus regional ambition | High | Unresolved |
| F3 | Feasibility | Can ACG demonstrate value within 12 months and limited funding? | Process and visibility foundations can show earlier value than full liquidity redesign | Cost baselines, resource capacity, implementation cost/timing | Scenario business case and ramp | Funding envelope | High | Untested |
| E1 | Execution | Which governance model preserves accountability and local responsiveness? | A federated model with global standards and bounded local autonomy may fit better than either extreme | Decision rights, service needs, role capacity, escalation paths | Options matrix and RACI | Target operating model | High | Untested |
| E2 | Execution | What sequence minimizes payment disruption? | Sequencing must protect peak-season service; whether pilot-first is best remains to be tested | Peak calendar, candidate entities, rollback, SLAs, dependencies | 30/60/90-day plan and stage gates | Mobilization approval | High | Unresolved |
| E3 | Execution | How will benefits and control improvements be validated? | Benefits will not be credible without named owners, formulas, baselines, and gates | Baseline owners, sources, KPI definitions, finance sign-off | Benefits-tracking design | Funding and accountability | Medium | Supported |

### Quantified-hypothesis convention

The bold V2, R1, and F1 thresholds are intentionally ambitious `ANALYST-ASSUMPTION` tests for Week 2, not confirmed findings, benefit baselines, or recommendations. V2 uses 50% of the $57.80m gross positive estimated availability on 30 June as its approximately $29m test; R1's greater-than-$5m figure is a decision-exposure threshold, not observed borrowing; and F1 measures same-calendar-day reporting, not start-of-day visibility.

## Hypothesis updates during Week 1

| Date | Hypothesis | Previous | Current | New evidence | Consequence |
|---|---|---|---|---|---|
| 2026-08-02 | V1 — start-of-day visibility is reliable | Untested | Unresolved | 58.18% of 9,955 observations were reported on the balance date and 25.45% were delayed by at least two days, but timestamps are absent | Define the KPI and obtain timestamped reporting logs in Week 2 |
| 2026-08-02 | V3 — ten or more accounts can close | Untested | Unresolved | Four accounts are marked dormant, while 21 are preliminarily restricted | Build validation criteria; do not use ten as a benefit baseline |
| 2026-08-02 | V4 — payment friction is material enough to diagnose | Untested | Supported | 31.51% manual touch, 6.30% exceptions, 20,080 repair minutes | Segment root causes; do not infer causation or headcount savings |
| 2026-08-02 | E1 — centralization is the preferred model | Untested | Untested | Public cases show possible benefits, but ACG has local constraints and resilience concerns | Evaluate genuinely different options; do not copy a case solution |
| 2026-08-02 | E2 — pilot-first sequencing is required | Untested | Unresolved | Peak-season protection is confirmed, but the best deployment pattern depends on readiness, dependencies, and service risk | Test pilot and non-pilot sequences; require blackout, rollback, and control gates |

## Evidence discipline

Statuses are limited to `Untested`, `Supported`, `Weakened`, `Rejected`, and `Unresolved`. External cases generate questions and design hypotheses; only ACG evidence can establish the ACG recommendation.
