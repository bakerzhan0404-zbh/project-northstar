# Week 1 — Decision-Led Issue Tree

**Classification:** Confidential — Project Northstar simulated client material; statuses are analyst assessments pending client review

**Reviewer cross-reference:** The [findings log](W1_findings_log.md) maps evidence-backed findings to the nodes below; assumptions A012–A019 in the [assumptions register](W1_assumptions_register.csv) preserve the base, stress, and stretch targets for Weeks 2–4.

## Executive question

Should ACG authorize a 90-day treasury-transformation mobilization, at what ambition, and with which Wave 1 initiatives and control conditions?

## Decision logic at a glance

The tree follows one direction: **diagnose the problem → assess its consequence or value → test feasibility and downside protection → decide and execute**. This assigns one owner to each question instead of repeating the same metric under both value and risk.

- Visibility path: `V1 → R1 → F1 → E2`
- Liquidity path: `F2 → V2 → F3 → E3`
- Payment path: `V4 → R2 → E2`
- Account path: `V3 → F2 → F3`
- Receivables and FX: `V5 / R4` remain data-gated and do not receive equal Week 2 depth without controlled subject data.

### 1. Diagnose the problem or opportunity

| ID | Decision question | Current evidence anchor | Week 2 test/target | Depends on / feeds | Priority | Status |
|---|---|---|---|---|---|---|
| <a id="v1"></a>V1 | Where and why is cash reporting late, estimated, or unreliable? | The date-only proxy identifies 32/55 same-day accounts, 23 delayed accounts, and 4,163 delayed account-days; timestamps are absent. | **Establish the timestamped KPI and isolate causes by source, region, method, and account.** | Feeds R1 and F1 | High | Unresolved |
| <a id="v3"></a>V3 | Which accounts create avoidable cost and complexity? | Four dormant, zero-payment legacy accounts average $37.46k of aggregate positive availability and carry $7.8k of estimated annual fees. | **Validate all four closures within 12 months; use two closures as the downside and management's ten as a stretch requiring six additional candidates.** | Feeds F2 and F3 | High | Unresolved |
| <a id="v4"></a>V4 | Within the supplied 7,600 records, where is payment friction concentrated and which process conditions are associated with it? | Manual-touch records are 31.51% of the supplied extract but represent 63.47% of exceptions and 63.35% of repair minutes. | **Reconcile the extract and test no more than 20% manual touch and 12,000 repair minutes over a comparable 7,600-record scope; do not infer causation.** | Feeds R2 | High | Unresolved |
| <a id="v5"></a>V5 | Where does receivables reconciliation create delay, manual work, or trapped working capital? | The process estimate implies 133.28 manual hours/month, but no AR, remittance, or match-status transactions are supplied. | **If controlled subject data arrives, test 40% / 53.31 hours per month of redeployment; otherwise defer the conclusion.** | Data-gated; may feed F3 | P1 | Unresolved |

### 2. Assess the consequence or value

| ID | Decision question | Current evidence anchor | Week 2 test/target | Depends on / feeds | Priority | Status |
|---|---|---|---|---|---|---|
| <a id="r1"></a>R1 | What funding, decision, or control consequences arise from stale or incomplete visibility? | Delayed accounts carry a median $26.01m—and no less than $24.02m—of positive estimated availability; this is an exposure proxy, not movable cash. | **Determine whether at least one funding or decision mismatch above $5m occurred and test reduction of median stale positive availability below $5m.** | Depends on V1; feeds F3 | High | Unresolved |
| <a id="v2"></a>V2 | After constraints, buffers, and settlement requirements are certified, how much cash can genuinely move within 24 hours? | $57.80m gross positive and $49.75m preliminarily unflagged availability are estimates, not movable cash. | **Validate the $21m stress / $35m base / $46.2m upside cases using F2-certified evidence. V2 alone owns aggregate movable-cash sizing.** | Depends on F2; feeds F3 | High | Unresolved |
| <a id="r2"></a>R2 | Within the supplied 7,600 records, which payment failures create supplier, customer, service, or control consequences? | The 786-record cross-border-wire cohort totals $14.72m, with 13.99% exceptions, 8.78% late release, and 4,921 repair minutes; criticality is unknown. | **Test overall-extract gates of no more than 4% exceptions and 3.5% late release; cross-border gates of 7%, 5%, and 2,500 minutes; and zero critical failures. Do not generalize beyond the supplied records.** | Depends on V4; feeds E2 | High | Unresolved |
| <a id="r4"></a>R4 | Which FX transaction and exposure patterns create avoidable cost or risk? | The 786 cross-border records and $14.72m value come only from the supplied payment extract; no trades, exposures, hedges, spreads, or settlements are supplied. | **If controlled FX data arrives, test the $73.61k–$147.22k annualized screen and reconcile at least 95% of value; otherwise book no benefit.** | Data-gated; may feed F3 | P1 | Unresolved |

### 3. Test feasibility and downside protection

| ID | Decision question | Current evidence anchor | Week 2 test/target | Depends on / feeds | Priority | Status |
|---|---|---|---|---|---|---|
| <a id="f1"></a>F1 | Can the visibility gap be closed without replacing the three ERPs? | Twenty-three accounts are delayed and 14 use spreadsheet/estimated reporting. | **Upgrade 18/23 delayed accounts, including 12/14 spreadsheet accounts, to reach at least 50/55 same-day accounts and fewer than 5% on estimated sources within 12 months.** | Depends on V1; feeds E2 | High | Untested |
| <a id="f2"></a>F2 | Which legal, tax, regulatory, buffer, and local-service constraints apply to each account, and which can be mitigated? | Twenty-one preliminarily restricted accounts hold $8.05m of positive estimated availability; the flags are not certification. | **Certify all 21 within 90 days, own 100% of exceptions, and test 25% / $2.01m base and 50% / $4.03m stretch clearance. F2 books no cash benefit.** | Feeds V2 and V3 | High | Unresolved |
| <a id="r3"></a>R3 | Could centralization concentrate control or resilience risk? | Six high-criticality activities represent 315.48 of 617.72 manual hours/month; SAP-S4, host-to-host, and Union Atlantic each exceed 25% concentration. | **Map or replace 100% of control purpose and test fallback for every component above 25% concentration.** | Feeds E1 and E2 | High | Untested |

### 4. Decide and execute

| ID | Decision question | Current evidence anchor | Week 2 test/target | Depends on / feeds | Priority | Status |
|---|---|---|---|---|---|---|
| <a id="f3"></a>F3 | Can the integrated foundation wave demonstrate value within 12 months and limited funding? | The component baselines are calculable, but implementation cost, timing, and realized benefits are not validated. | **Test $35m movable cash, 50/55 same-day accounts, four closures, and 150 of 617.72 manual hours/month redeployed; require the $21m / two-closure / 50-hour downside to hold.** | Depends on V2, V3, R1, and any data-gated value | High | Untested |
| <a id="e1"></a>E1 | Which governance model preserves accountability and local responsiveness? | ACG spans 16 entities and 55 accounts; current decision rights and exception ownership are not validated. | **Test a federated model with global standards over 100% of scope, one local certifier per entity, named ownership of all decisions/exceptions, and two-business-day escalation.** | Depends on R3 | High | Untested |
| <a id="e2"></a>E2 | What sequence minimizes disruption while delivering the visibility and payment targets? | Twenty-three accounts are delayed; readiness, peak calendar, criticality, and rollback evidence are absent. | **Pilot 10 delayed accounts covering at least 25% of the supplied records; scale only after four compliant weeks, zero critical disruptions, and rollback within four hours.** | Depends on F1, R2, and R3 | High | Unresolved |
| <a id="e3"></a>E3 | How will benefits and control improvements be validated? | No benefit line is yet Finance-approved or demonstrated as realized. | **Require 100% evidence completeness and Finance approval for the funded base case; recognize realized value only after at least 90% of target for three consecutive months.** | Depends on F3 | Medium | Untested |

## Quantified-hypothesis convention

The `Current evidence anchor` column contains `ACG-DATA` or reproducible `ANALYST-CALC`; bold cells are intentionally ambitious, falsifiable `ANALYST-ASSUMPTION` targets or gates. The fixed cross-branch stress case is $21m movable cash, two closures, and 50 hours/month of realized capacity. Week 2 must retain these thresholds or record any change in the decision and analysis logs. No hypothesis is a finding or booked benefit.

Unless explicitly stated otherwise, every payment percentage, concentration, value, and repair measure refers only to the supplied 7,600-record file. None represents ACG's full payment population until source totals and extraction logic reconcile.

## Appendix A — Evidence and analysis detail

| ID | Evidence required | Detailed analysis |
|---|---|---|
| V1 | Timestamped receipt, cutoff, balance type, source quality, reconciliation | Define the timestamp KPI; segment delay by source, region, method, account, and date |
| V2 | F2-certified transferability, buffers, settlement timing, entity rules, movement capability | Build the certified $21m / $35m / $46.2m liquidity waterfall |
| V3 | Activity, purpose, local need, fees, dependencies, signatories, closure cost | Test the four-account base, two-account downside, and additional candidate screen |
| V4 | Source population/value control, sampling logic, reason codes, payment type, repair time | Reconcile the supplied extract; diagnose concentrations and associations only |
| V5 | AR ledger, invoices, receipts, remittance, match status, reason codes, aging | Validate scope and the 133.28-hour baseline before testing removal |
| R1 | Funding events/terms, decision records, timestamps, transfer timing | Match visibility gaps to actual funding or decision consequences and the greater-than-$5m test |
| R2 | Payment criticality, service consequence, cutoffs, approvals, reason codes | Test supplier/control impact and service gates within the reconciled supplied extract |
| R3 | Access model, BCP, cyber review, emergency process, control inventory | Test control-purpose coverage, fallback, segregation, and emergency access |
| R4 | FX exposures, trades, hedges, spreads/fees, funding, settlement | Reconcile exposure-to-trade evidence before screening cost or offset opportunity |
| F1 | Interface inventory, architecture, source owners, delivery estimates | Build the 18-account uplift path and 12-spreadsheet conversion plan |
| F2 | Country/entity legal, tax, regulatory, payroll, collection, buffer, resilience requirements | Create the account-level certification matrix and clearance scenarios |
| F3 | Validated component baselines, implementation cost/timing, benefit ownership | Integrate value types and test the fixed downside without double counting |
| E1 | Decision rights, service needs, role capacity, escalation paths | Compare genuinely different models and draft the RACI |
| E2 | Peak calendar, readiness, candidate accounts, rollback, SLAs, dependencies | Build the pilot selection and stage-gate plan |
| E3 | Owners, sources, formulas, baselines, timing/ramp, validation evidence, Finance sign-off | Apply evidence, downside-survival, approval, and realization gates |

## Appendix B — Hypothesis updates during Week 1

| Date | Hypothesis | Previous | Current | New evidence | Consequence |
|---|---|---|---|---|---|
| 2026-08-02 | V1 — start-of-day visibility is reliable | Untested | Unresolved | 58.18% of 9,955 observations were reported on the balance date and 25.45% were delayed by at least two days, but timestamps are absent | Define the KPI and obtain timestamped reporting logs in Week 2 |
| 2026-08-02 | V3 — ten or more accounts can close | Untested | Unresolved | Four accounts are marked dormant, while 21 are preliminarily restricted | Build validation criteria; do not use ten as a benefit baseline |
| 2026-08-02 | V4 — payment friction is material enough to diagnose | Untested | Supported | 31.51% manual touch, 6.30% exceptions, 20,080 repair minutes | Segment root causes; do not infer causation or headcount savings |
| 2026-08-02 | E1 — centralization is the preferred model | Untested | Untested | Public cases show possible benefits, but ACG has local constraints and resilience concerns | Evaluate genuinely different options; do not copy a case solution |
| 2026-08-02 | E2 — pilot-first sequencing is required | Untested | Unresolved | Peak-season protection is confirmed, but the best deployment pattern depends on readiness, dependencies, and service risk | Test pilot and non-pilot sequences; require blackout, rollback, and control gates |

## Evidence discipline

Statuses are limited to `Untested`, `Supported`, `Weakened`, `Rejected`, and `Unresolved`. External cases generate questions and design hypotheses; only ACG evidence can establish the ACG recommendation.
