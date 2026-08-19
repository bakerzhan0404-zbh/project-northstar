# Week 3 — Proposed Cash-Visibility Pilot Charter

**Prepared by:** Baker

**Prepared date:** 18 August 2026

**Working period:** 17–23 August 2026

**Status:** Design only; analyst proposal; no launch, production change, procurement, cash movement, or value approval

**Classification:** Confidential — Project Northstar simulated client material

## Charter decision

This charter asks the CFO, Group Treasurer, CIO, Regional Finance, BU Finance, and management control owner to review a **bounded, read-only validation design**. Week 3 may approve the design for further readiness work; it does not authorize the pilot to launch.

A separate go/no-go approval is required after the authoritative-source census, controlled baseline, named ownership, service and control design, specialist reviews, cost range, approved blackout/peak-period conditions, and rollback rehearsal are complete. Pilot completion would not itself authorize cash transfers, account closure, platform procurement, funded benefits, or enterprise scale.

## Objective and testable hypothesis

**Objective:** Determine whether a targeted data-ownership and connectivity intervention can make selected delayed balance sources reliably available by an approved business cutoff, fully reconciled or formally explained, and decision-useful without disrupting critical service or replacing ACG's ERP estate.

**Design hypothesis:** Because all 23 accounts delayed under the supplied reporting-date proxy use portal or spreadsheet reporting, a focused intervention on those source handoffs may improve controlled visibility. The hypothesis is not yet a causal finding: source method may proxy ownership, process, bank, local calendar, or other differences.

## Evidence baseline and limits

| Current evidence | Permitted use | Prohibited inference |
|---|---|---|
| 55 accounts and 9,955 account-days from 1 January–30 June 2026 | Define the supplied population and source-method pattern | Do not call this a controlled start-of-day baseline |
| 5,792 account-days are same-calendar-day; 23 accounts are delayed; all delayed accounts use portal or spreadsheet | Target readiness and source/owner validation on delayed methods | Do not infer elapsed-24-hour or approved-cutoff performance |
| The 23 delayed accounts are associated with substantial positive estimated availability in the six-month panel | Prioritize evidence collection and decision-usefulness testing | Do not call estimated availability movable, idle, or a benefit |
| Current data lacks receipt timestamp, approved cutoff, certified balance type, owner, and reconciliation result | Define the minimum data contract and baseline plan | Do not claim a launch-ready cohort or technical cause |

Validated movable cash remains `$0 established`. This pilot does not test, authorize, or value cash mobility.

## Scope, population, and selection

### Evidence-readiness population

Before any launch decision, perform a census of **all 55 accounts / 9,955 supplied account-days** to establish:

- authoritative source and source owner;
- receipt timestamp and timezone;
- approved business cutoff and applicable calendar;
- balance type and value date;
- entity/account identifiers and currency;
- reconciliation rule, tolerance, result, and exception owner;
- local restriction, critical-service, payroll, tax, collection, settlement, and continuity context relevant to safe inclusion.

Complete evidence for all 55 accounts is the controlled-baseline goal; it is not a Week 3 claim that every account is ready for pilot.

### Provisional later-pilot cohort

Subject to readiness and control review, the design carries forward ten delayed accounts:

| Source method | Provisional account IDs | Selection rule |
|---|---|---|
| Spreadsheet | `AC0021`, `AC0010`, `AC0017`, `AC0001`, `AC0040` | Top four delayed-source accounts with complete supplied selection fields by January–June average positive estimated-available USD, plus the highest APAC account under the same screen; account ID ascending breaks ties |
| Portal | `AC0022`, `AC0031`, `AC0018`, `AC0002`, `AC0050` | Top four delayed-source accounts with complete supplied selection fields by January–June average positive estimated-available USD, plus the highest APAC account under the same screen; account ID ascending breaks ties |

The set spans three regions, three ERP environments, and four banks under the Week 2 design. Here, selection eligibility means only that the supplied delayed-source fields needed to reproduce the screen are complete; it does **not** mean launch readiness. All ten accounts require the same base readiness/control review before any later use. `AC0040` remains APAC, Payroll, and restricted; it alone is marked for enhanced control review and retained only as a read-only shadow-observation candidate subject to documented substitution. In `data/processed/W3_visibility_pilot_candidates.csv`, this distinction is explicit: `control_review_required = true` for 10/10 accounts, while `enhanced_control_review_required = true` only for `AC0040`. The set is coverage-constrained and purposive, not statistically representative. Account readiness must be rechecked against the reproduced output before approval.

### Cohort substitution rule

If an account contains an unresolved restriction, payroll, tax, collection, regulatory, service-continuity, access, or readiness concern, the accountable owners may:

1. retain it in read-only shadow observation without changing the source or process;
2. substitute the next eligible account under the same method and documented selection rule; or
3. remove it and record the resulting coverage limitation.

Every substitution or exclusion requires reason, approving owner, effect on region/ERP/bank coverage, and analysis-log/decision-log traceability before comparison.

## Explicit exclusions

This charter excludes:

- cash transfer, sweep, pooling, investment, borrowing, account closure, or signatory change;
- production routing of payments or funding decisions through a new platform;
- ERP replacement, bank/vendor selection, or enterprise architecture commitment;
- use of estimated balances as movable or idle cash;
- value, interest, fee, capacity, headcount, or P&L recognition;
- representative inference from the ten-account cohort to all 55 accounts;
- any legal, tax, regulatory, accounting, sanctions, or cybersecurity conclusion.

## Proposed design phases and duration

| Phase | Proposed activity | Exit condition | Duration status |
|---|---|---|---|
| 0. Owner and data readiness | Complete the 55-account census; confirm source, cutoff, calendar, balance, owner, reconciliation, local context, and exception rules | Controlled denominator and readiness status are owner-approved | Duration TBD; no launch clock begins until complete |
| 1. Baseline | Observe the approved cohort using the current approved process; capture all KPI fields and failures without changing production | Baseline period and comparability are approved by Group Treasury and data/control owners | Length TBD from reporting calendar and data stability; must be approved before launch |
| 2. Technical/control rehearsal | Test the proposed read-only source path, monitoring, access, failure modes, contingency, evidence capture, and rollback in a non-production or approved safe environment | Cyber/architecture/control/service sign-off; restoration rehearsal at or below four hours | Duration TBD from architecture and test plan |
| 3. Later bounded operation | If separately approved, observe the ten-account process outside approved blackout/peak periods under the signed charter | Minimum four consecutive compliant operating weeks | Proposed minimum four consecutive weeks; extend after material population, control, or service change |
| 4. Evaluation | Compare like-for-like baseline and pilot periods; assess data, service, control, cost, adoption, and learning | Written scale/extend/stop recommendation and separate CFO/SteerCo decision | Evaluation window TBD |

The total calendar duration and launch window remain TBD. Any blackout or peak-period exclusion must be defined and approved by affected BU/Regional Finance and the Steering Committee before launch.

## Controlled baseline and denominator plan

1. Freeze the approved account list, expected operating calendar, timezones, cutoffs, balance type, source, and owners before baseline measurement.
2. Define one expected account-day for every in-scope account on each applicable reporting day. Late, missing, invalid, or unexplained records remain in the denominator.
3. Reconcile the account-day population and identifiers to the source system and governed account master.
4. Capture receipt event time, cutoff result, balance definition, reconciliation result, explanation/approval, service event, control event, and process version.
5. Predefine allowable exclusions—such as an owner-approved market holiday—and record each with reason and approver. Technical failures and missing data are not exclusions.
6. Compare only like-for-like accounts, calendars, definitions, and periods. A materially changed population resets or segments the comparison.
7. Lock the baseline, tolerance, and targets through a decision-log entry before any intervention result is viewed.

## KPI and acceptance contract

All targets are proposed design hypotheses until the named owner approves the definition, baseline, tolerance, and reporting process.

| KPI | Formula / denominator | Proposed pilot condition | Proposed accountable owner | Interpretation boundary |
|---|---|---|---|---|
| Data-contract readiness | Selected accounts with approved source, timestamp, cutoff, balance type, owner, reconciliation rule, calendar, and exception owner / selected accounts | 100% before launch | Group Treasurer; CIO enables | Readiness only; not performance |
| On-time cash visibility | In-scope account-days received by the approved cutoff / expected in-scope account-days | At least 95% for four consecutive operating weeks | Group Treasurer | Replaces the date proxy only after controlled baseline approval |
| Reconciliation / exception-disposition coverage | In-scope account-days reconciled or formally explained and owner-approved / expected in-scope account-days | 100% for four consecutive operating weeks | Group Treasurer | An approved explanation remains visible; it is not a silent pass or proof that cash was observed |
| Daily position ready for decision | Scheduled pilot days with an approved pilot position by the approved decision cutoff / scheduled pilot days | Target and cutoff TBD before launch | Group Treasurer | Must test decision usefulness, not connectivity alone |
| Data exceptions aged beyond tolerance | Open data exceptions older than the approved tolerance / open data exceptions | Tolerance and target TBD from baseline; no critical aged break | Named data owner | Materiality and ageing are not yet defined |
| Defined critical-service failure | Count of attributable payroll, tax, refund, critical-supplier, regulated, or other owner-approved critical failures | 0 | Relevant BU Finance / process owner | Criticality definition and attribution require approval |
| Confirmed control breach | Count of attributable SoD, unauthorized access, audit-trail, reconciliation, cyber, or resilience breaches | 0 | Management control owner | Management determines and owns control conclusion |
| Rollback restoration time | Authorized rollback decision to verified restoration of the approved prior process | Rehearse at or below four hours before launch/scale | CIO / service owner | Four hours is a proposed standard, not current performance |

No liquidity, borrowing, cash-release, fee, or capacity KPI is an acceptance measure for this pilot.

## Proposed ownership and governance

| Role | Proposed responsibility |
|---|---|
| CFO / Steering Committee | Approve later go/no-go and any scale decision; accept cost/risk envelope and conditions |
| Group Treasurer | Accountable for objective, data contract, cutoffs, position usefulness, KPI, cohort, and operating decision |
| Regional Finance | Responsible for source ownership, calendar, local context, restriction/service evidence, and local exception resolution |
| Local / BU Finance | Confirm critical services, operational readiness, emergency rights, and local outcome; operate approved local step |
| CIO / IT / Data / Cyber | Accountable for technical design, authoritative interface, identity/access, monitoring, resilience, and rollback |
| Management control owner | Approve control design, test evidence, deficiency treatment, and stop/restart conditions |
| Internal Audit | Consulted on design and evidence; management retains control accountability |
| Finance / Benefits | Validate costs and reject unsupported benefits; no value is expected or approved by this charter |
| Baker | Maintain design traceability and record evidence boundaries; no client approval authority |

## Required controls and service gates

The relevant proposed controls are `CASH-01`, `CASH-02`, `CASH-06`, `TECH-01`, `TECH-02`, `TECH-03`, `GOV-01`, `GOV-02`, and `GOV-03` in `W3_control_inventory.csv`.

No later launch may occur without:

1. named business, data, technology, control, service, and exception owners;
2. an approved account population, source, calendar, cutoff, balance type, denominator, baseline, tolerance, and KPI version;
3. architecture, cybersecurity, access, source authentication, lineage, and source-to-target reconciliation approval;
4. blackout/peak-period and critical-service definitions approved by affected BU/Regional Finance leaders;
5. tested contingency and a rollback rehearsal at or below four hours;
6. a complete issue, incident, evidence-retention, and escalation plan;
7. one-time and recurring cost ranges with source and Finance review; and
8. a recorded CFO/SteerCo go/no-go decision.

## Cost range and benefit treatment

**Current cost range:** `TBD — not estimated from the supplied evidence.`

Before a launch decision, IT, Treasury, Regional Finance, control owners, and Finance must provide low/base/high one-time and recurring ranges for interface/configuration work, internal effort, testing, controls, support, bank/vendor charges if any, and contingency. Each range requires source, unit, timing, owner, dependency, and approval.

The start-of-Week-3 `$1.0–$1.5m` FY2026 initial transformation envelope is a **ceiling for the combined initial stage**, not a visibility-pilot cost estimate or allocation. The costed pilot and other initial-stage commitments must fit within the approved envelope, or a larger commitment must return for staged CFO/SteerCo approval after demonstrated Wave 1 benefits. No amount is authorized by this charter.

This charter approves no benefit. Visibility improvement may create decision evidence, but no cash release, borrowing reduction, fee savings, capacity, risk value, or P&L is recognized without a separate reconciled model, named owner, realized-value formula, cost, and Finance approval.

## Stop, pause, rollback, and no-scale rules

| Trigger | Required response | Proposed decision owner |
|---|---|---|
| Missing owner, source, controlled baseline, cutoff, service definition, control sign-off, cost range, approved blackout/peak-period decision, or rollback rehearsal | No-go; return design for remediation | Group Treasurer / CIO / BU Finance |
| Account/source population materially changes or cannot reconcile | Pause comparison; segment or rebuild baseline; do not claim improvement | Group Treasurer / data owner |
| Defined material unexplained position break | Pause the affected process; preserve evidence and escalate | Group Treasurer |
| Critical-service failure or confirmed control/cyber/access breach attributable to the pilot | Stop; preserve evidence; invoke the approved prior process and incident response | Pilot accountable owner / control owner / CIO |
| Restoration cannot be verified within four hours | Stop and do not restart without root-cause remediation and reapproval | CIO / Steering Committee delegate |
| Four-week evidence is incomplete, non-comparable, or target is missed | Extend or stop; do not scale or assign value | Group Treasurer / CFO-SteerCo |

## Evaluation and separate scale decision

A later pilot can be considered technically complete only if it produces four consecutive comparable operating weeks with at least 95% on-time visibility, 100% reconciled or formally explained records, zero defined critical-service failures, zero confirmed control breaches, and verified rollback evidence. Completion does not equal success or scale approval.

The CFO/SteerCo must separately decide to stop, extend, redesign, or scale after reviewing:

- result stability and explanation of every miss;
- decision usefulness and local-service feedback;
- control, cyber, access, resilience, and rollback evidence;
- population and definition comparability;
- adoption and operating ownership;
- one-time and recurring cost evidence; and
- any proposed benefit under Finance's separate validation rule.

## Open decisions before any launch

1. Who owns the authoritative source, cutoff, balance definition, and reconciliation for every selected account?
2. Which calendar, timezone, cutoff, materiality, explanation, and ageing rules are approved?
3. Which provisional accounts remain safe and ready, and which require shadow observation or substitution?
4. What constitutes a decision-ready daily position and a defined critical-service failure?
5. What architecture and access approach is acceptable around the three ERPs and the retiring legacy instance?
6. What low/base/high implementation and run-cost range is acceptable?
7. Who has pause, rollback, restart, and later scale authority?

Until those decisions are evidenced and recorded, this remains a design-only charter.

## Evidence provenance

- Pilot charter completeness, population, KPI, cost, service, rollback, and scale/stop expectations: `W2_workplan.md`, Week 3 readiness and success sections.
- Visibility population, same-calendar-day definition, source pattern, and limitations: `W2_metric_contract.md`, `W2_findings_log.md` F07, and `W2_analysis_log.md` A08.
- Current-state handoffs and data/control gates: `W2_current_state_process_map_and_RACI.md`.
- Future-state principles: `W3_design_principles.md`, especially DP-01, DP-04, DP-05, DP-06, DP-07, and DP-08.
- Initial FY2026 affordability ceiling: start-of-Week-3 CFO update recorded in `W3_workplan.md` and `W3_analysis_log.md`; it is not a pilot cost estimate.
- Client and stakeholder constraints: `client/CLIENT_BRIEF.md` and `client/STAKEHOLDER_PACK.md`.

The supplied population and reproduced measures are `ACG-DATA` / `ANALYST-CALC`. The cohort, target, timing, ownership, cost requirements, and gates are `ANALYST-JUDGMENT` / `ANALYST-ASSUMPTION` and do not become client commitments without recorded approval.
