# Week 3 — Proposed Payment Root-Cause and Process Pilot Charter

**Prepared by:** Baker

**Prepared date:** 18 August 2026

**Working period:** 17–23 August 2026

**Status:** Design only; analyst proposal; no launch, production routing, automation, labor removal, or value approval

**Classification:** Confidential — Project Northstar simulated client material

## Charter decision

This charter asks the CFO, Group Treasurer, Shared Services Lead, CIO, BU/Regional Finance, and management control owner to review a bounded payment-evidence and process-test design. Week 3 may approve further readiness and diagnostic work; it does not authorize production execution.

A separate go/no-go approval is required after the source population and value reconcile, the selected records link to required evidence, the root-cause taxonomy and controlled baseline are approved, service/control owners sign off, costs are ranged, the pilot avoids the approved peak blackout, and rollback is rehearsed. Completion would not itself authorize ACG-wide extrapolation, automation scale, headcount action, capacity/P&L recognition, or a platform decision.

## Objective and testable hypothesis

**Objective:** Determine which intake, data, cutoff, format, policy, approval, system, or user-behavior conditions are associated with payment friction in defined cohorts, then test a small control-preserving process intervention against a like-for-like baseline without worsening critical service, late release, rejection, or controls.

**Design hypothesis:** Within the supplied 7,600 records, the deduplicated manual-touch or cross-border-wire priority union contains 2,839 records, 356 exceptions, and 14,939 repair minutes—74.32% of extract exceptions and 74.40% of extract repair minutes. Targeted diagnosis may identify actionable causes more efficiently than broad automation. This is not proof that manual touch or cross-border status caused the friction.

## Evidence baseline and limits

| Current evidence | Permitted use | Prohibited inference |
|---|---|---|
| 7,600 supplied records and $198.14m gross translated payment-intent value | Reproduce the supplied extract and define the current analytical boundary | Do not call this a certified ACG-wide population, settlement value, or cash outflow |
| 2,395 manual touches, 479 exceptions, 380 late-release flags, 54 rejected, 17 pending, and 20,080 repair minutes | Set within-extract reference rates and test sample construction | Do not annualize, generalize, or treat flags as approved operational definitions |
| Priority union: 2,839 records, 356 exceptions, 14,939 repair minutes, $66.71m gross payment-intent amount | Prioritize four mutually exclusive strata and preserve overlap control | Do not add manual-touch and cross-border totals or infer cause |
| Process repair estimate 102.60 hours/month versus payment-file estimate 55.78 hours/month | Define a reconciliation and observed-time gate | Do not blend the sources or call either removable capacity, P&L, or headcount |
| No reason codes, source documents, criticality, beneficiary/corridor detail, event sequence, or approval/release timestamps are supplied | Define required evidence and pause rules | Do not state a root cause or approve an intervention before evidence review |

The current design carries **zero validated redeployable capacity and zero payment P&L benefit**.

## Scope and populations

### Controlled baseline population

Before a later launch decision, Shared Services and IT/Data must reconcile the source payment population to the extract and prospective process:

- unique record count and gross payment-intent value;
- extraction period, statuses, entities, regions, payment types, currencies, and channels;
- inclusion, exclusion, duplicate, cancelled, resubmitted, and status-as-of logic;
- source-to-extract field mapping and transformation;
- approval, release, submission, acknowledgement, status, repair, and completion timestamps where available;
- source document, required intake fields, criticality, reason code, root-cause category, owner, and action;
- bank/ERP acknowledgement and accounting reconciliation where applicable.

Until that control completes, all numerical statements remain limited to the supplied 7,600 records.

### Root-cause review population

Review **120 supplied records**, 30 from each mutually exclusive stratum:

1. manual-touch only;
2. manual-touch plus cross-border wire;
3. cross-border-wire only; and
4. neither/control.

Within each stratum, select:

- **15 issue cases**, where issue means exception, late release, `Repaired`, or `Rejected`; rank by repair minutes and then USD amount; and
- **15 non-issue controls**, matched on payment type, region, month, and USD amount band where feasible.

Record every nearest-match deviation and any unavailable match. The review is purposive case-control diagnosis, not a powered prevalence estimate and not an enterprise benefit sample.

### Candidate later process-test population

The final intervention cohort is **TBD after root-cause review**. It must:

- target one or more evidenced, remediable causes rather than cohort membership alone;
- have a controlled source population and like-for-like comparator;
- exclude or separately protect payroll, tax, customer refunds, critical suppliers, and other owner-defined critical flows unless their owner explicitly approves a safe observation/test design;
- fit outside the approved peak blackout;
- retain required approvals, segregation, access, sanctions/beneficiary, duplicate, audit-trail, reconciliation, emergency, and service controls; and
- remain small enough to stop and restore under the approved four-hour rollback standard.

## Explicit exclusions

This charter excludes:

- production change, automated release, bank/platform/vendor selection, or enterprise process rollout;
- broad inference from 120 purposively selected records to ACG prevalence or savings;
- combining overlapping cohorts or the two unreconciled repair baselines;
- removal of required approvals, segregation, access, sanctions/beneficiary, duplicate, audit, reconciliation, emergency, or resilience controls;
- headcount reduction, cashable labor saving, P&L, fee, working-capital, or risk-value recognition;
- altering a live critical payment, bank instruction, beneficiary, signatory, or approval authority in Week 3; and
- legal, regulatory, sanctions, accounting, cybersecurity, or architecture conclusions.

## Proposed design phases and duration

| Phase | Proposed activity | Exit condition | Duration status |
|---|---|---|---|
| 0. Source and owner readiness | Reconcile controlled population/count/value, fields, events, owners, source documents, calendars, criticality, and required controls | Shared Services, IT/Data, Finance and control owner approve the controlled baseline plan | Duration TBD; no root-cause conclusion or launch clock before completion |
| 1. Four-stratum review | Review 120 records under the locked selection/matching rule; assign evidence-based reasons and actions | All reviewed issues have evidence status, reason or explicit unknown, owner, action, and review QA | Duration TBD from evidence-linkage and reviewer capacity |
| 2. Intervention design and baseline | Select an evidenced cause; define the standard change, comparator, KPI, service/control tests, costs, contingency, and rollback | Process and control owners approve a like-for-like baseline and target-setting rule | Duration TBD; target locked before viewing result |
| 3. Technical/control rehearsal | Test workflow, access, change, failure modes, evidence capture, contingency and rollback in a safe environment | Architecture/cyber/control/service sign-off; verified restoration at or below four hours | Duration TBD from change plan |
| 4. Later bounded operation | If separately approved, operate the signed intervention outside peak | Minimum four consecutive comparable operating weeks with all service/control gates | Proposed minimum four consecutive weeks; extend after material definition/population change |
| 5. Evaluation | Compare baseline and intervention; assess causes, KPI, service, controls, adoption, cost, and evidence limits | Written stop/extend/redesign/scale recommendation and separate CFO/SteerCo decision | Evaluation window TBD |

The total calendar duration remains TBD because source linkage, baseline stability, intervention choice, reviewer capacity, and approved blackout dates are not supplied.

## Required record-level evidence

| Evidence group | Required fields / proof | Treatment if unavailable |
|---|---|---|
| Population and lineage | Source population ID/count/value, extraction logic, unique payment ID, status-as-of, source-to-extract mapping | Retain extract boundary; no enterprise rate, cause, or benefit claim |
| Request quality | Source document, invoice/reference, beneficiary, entity, amount/currency, payment type, due date, purpose, requestor, required-field check | Mark evidence unavailable; do not assume incomplete intake caused the issue |
| Criticality and service | Critical-flow definition, criticality, requested/required date, local calendar, approved cutoff, service outcome | Exclude from unsafe testing; critical-service conclusion remains unvalidated |
| Approval and control | Initiator, approver, delegated authority, SoD, access, duplicate, sanctions/beneficiary checks, changes and overrides | Control failure or missing critical evidence blocks intervention launch |
| Event sequence | Request, approval, release, file, bank acknowledgement, status, repair, resubmission and completion timestamps | Do not assign sequence-dependent cause or calculate a controlled late-release KPI |
| Exception and action | Bank/system status, reason code, root-cause category, repair action, owner, approval, final outcome | Record explicit unknown; assign evidence action; do not infer cause from cohort |
| Accounting / completion | Bank acknowledgement/status, ERP/accounting reference, reconciliation result | Do not call the payment settled or completed in the controlled baseline |

## Controlled baseline and comparison plan

1. Reconcile the source population, record count, gross payment-intent value, identifiers, statuses, and extract logic before segmentation.
2. Freeze the eligible population, period, strata, issue definition, criticality, cutoffs, event definitions, amount-band logic, exclusions, and KPI version.
3. Retain mutually exclusive cohorts or the deduplicated union; never add overlapping manual-touch and cross-border totals.
4. Include every eligible record in its applicable denominator. Missing fields, exceptions, rejections, and late/missing events do not disappear through exclusion.
5. Compare like-for-like payment type, region, calendar period, criticality, channel, amount band, and other material factors where feasible; document residual imbalance.
6. Observe time and classify required control activity separately before estimating removability. Do not combine process-file and payment-file repair hours.
7. Lock pilot targets or improvement rules through a decision-log entry before results are viewed.
8. Reset or segment the comparison after a material process, system, population, definition, policy, or peak-season change.

## KPI and acceptance contract

The Week 2 values are supplied-extract proxies. Directional hypotheses of 20% manual touch, 4% exceptions, 3.5% late release, and 157.89 repair minutes per 100 records are **not adopted as pilot acceptance targets**. The accountable owners must first approve a controlled like-for-like baseline and feasible target.

| KPI | Formula / denominator | Proposed pilot condition | Proposed accountable owner | Interpretation boundary |
|---|---|---|---|---|
| Population count reconciliation | Controlled records represented in the measurement layer / controlled source records | 100% before launch and reporting | Shared Services Lead | IT/Data operates extraction and lineage; requires approved inclusion/exclusion and duplicate logic |
| Population value reconciliation | Gross payment-intent value represented / controlled source gross payment-intent value | 100% within approved tolerance before launch and reporting | Shared Services Lead | Finance validates the value reconciliation; payment intent is not settlement or cash outflow |
| Manual-touch rate | Records with approved manual-touch definition / eligible controlled records | Report by mutually exclusive stratum; target locked after baseline | Shared Services Lead | Manual work may be required control, response, or cause |
| Exception rate | Records meeting the approved exception definition / eligible controlled records | Must improve against pre-agreed like-for-like baseline; magnitude locked before launch | Shared Services Lead | Reason and criticality context are required |
| Late-release rate | Records released after approved cutoff / eligible controlled records with valid event timestamps | Must not worsen; improvement target locked after timestamp baseline | Shared Services Lead | Supplied flag is not a controlled timestamp baseline |
| Rejection rate | Rejected records / eligible controlled records | Must not worsen | Shared Services Lead | Status-as-of and resubmission logic must be controlled |
| Repair effort | Validated repair minutes / eligible controlled records × 100 | Must improve against pre-agreed like-for-like baseline; magnitude locked after observed-time validation | Shared Services Lead | Not P&L, headcount, or removable capacity |
| Reviewed-issue evidence closure | Reviewed issue cases with reason or explicit unknown, owner, action, and evidence status / reviewed issue cases | 100% | Shared Services Lead | Explicit unknown is acceptable evidence status, not a proven cause |
| Defined critical-service failure | Count of attributable owner-defined critical payment failures | 0 | Relevant BU Finance / process owner | Definition and attribution require approval |
| Confirmed control breach | Count of attributable SoD, authorization, access, duplicate, sanctions/beneficiary, audit, cyber, resilience, or reconciliation breaches | 0 | Management control owner | Management owns the control conclusion |
| Rollback restoration time | Authorized rollback decision to verified restoration of the approved prior process | Rehearse at or below four hours before launch/scale | CIO / service owner | Four hours is a proposed gate, not current performance |

## Root-cause coding and intervention rule

Each reviewed issue should be coded only to the lowest defensible evidence level:

| Category | Evidence needed before coding as supported | Possible design response; not preselected |
|---|---|---|
| Intake / master data | Source document and required-field evidence show missing, invalid, or late input preceded the issue | Required fields, validation, owner feedback, controlled master-data correction |
| Cutoff / timing | Approved cutoff and event timestamps show an actionable timing failure | Calendar/cutoff clarification, earlier workflow, escalation, capacity timing review |
| Format / channel | Technical validation, acknowledgement, or rejection evidence identifies format/channel failure | Controlled format rule, mapping correction, pre-validation, channel resilience |
| Policy / approval | Policy, authority, approval sequence, or local exception evidence identifies the condition | Clarify decision rights, standardize rule, preserve local exception and control |
| System / integration | Logs and reconciliation show interface or mapping failure | Bounded interface/data fix with architecture, cyber, and rollback review |
| User / training | Complete process/system evidence plus observed behavior supports a knowledge or execution gap | Targeted training, job aid, workflow feedback; avoid blame without evidence |
| Required control work | Evidence shows manual activity is necessary for authorization, review, or risk treatment | Preserve or replace control before any efficiency claim |
| Unknown / mixed | Evidence is missing, contradictory, or multiple causes remain plausible | Assign evidence owner; do not force a cause or fund a response |

An intervention may enter a later pilot only when the cause is sufficiently evidenced, the change directly addresses it, required controls remain, and a comparable baseline can test the result.

## Proposed ownership and governance

| Role | Proposed responsibility |
|---|---|
| CFO / Steering Committee | Approve later go/no-go and scale decision; accept cost/risk envelope and explicit deferrals |
| Shared Services Lead | Accountable for population reconciliation, review quality, process design, KPI, reason/action ownership, and operating result |
| Group Treasury | Own global policy and performance direction; review critical implications and service/control conditions |
| BU / Regional Finance | Own request quality, criticality, local calendar/service, approvals, emergency rights, and business outcome |
| CIO / IT / Data / Cyber | Own extraction, lineage, event data, integration, access, technical testing, resilience, and rollback |
| Management control owner | Approve authorization, SoD, access, duplicate, sanctions/beneficiary, audit, reconciliation, deficiency and stop/restart design |
| Internal Audit | Consulted on design and evidence; management remains control owner |
| Finance / Benefits | Reconcile costs; validate any later P&L/capacity formula and realized evidence; reject unsupported value |
| Baker | Maintain analytical selection and evidence traceability; no client approval authority |

## Required controls and service gates

The relevant proposed controls are `PAY-01` through `PAY-07`, `TECH-01` through `TECH-03`, and `GOV-01` through `GOV-03` in `W3_control_inventory.csv`.

No later launch may occur without:

1. a reconciled source population and gross payment-intent value, controlled extraction logic, and complete measurement denominator;
2. linkable source documents, criticality, reason/action, and event evidence sufficient for the selected intervention;
3. named business, process, data, technology, control, service, exception, and benefit/cost owners;
4. approved intake, approval, SoD, access, duplicate, sanctions/beneficiary, audit, submission, reconciliation, emergency, and evidence-retention controls;
5. a like-for-like baseline and target-setting rule locked before results;
6. peak-blackout and critical-service definitions approved by affected BU/Regional Finance;
7. architecture, cyber, change, resilience, contingency, and rollback approval with restoration rehearsed at or below four hours;
8. one-time and recurring low/base/high cost ranges with source and Finance review; and
9. a recorded CFO/SteerCo go/no-go decision.

## Cost range and benefit treatment

**Current cost range:** `TBD — not estimated from the supplied evidence.`

Before a later launch decision, Shared Services, IT, control owners, BU Finance, and Finance must document low/base/high one-time and recurring ranges for process design, data extraction, reviewer/SME time, configuration/integration, testing, controls, training, support, bank/vendor charges if any, and contingency. Each estimate requires source, unit, timing, owner, dependency, and approval.

The start-of-Week-3 `$1.0–$1.5m` FY2026 initial transformation envelope is a **ceiling for the combined initial stage**, not a payment-pilot cost estimate or allocation. The costed pilot and other initial-stage commitments must fit within the approved envelope, or a larger commitment must return for staged CFO/SteerCo approval after demonstrated Wave 1 benefits. No amount is authorized by this charter.

This charter approves no capacity or financial benefit. The 20,080 supplied repair minutes, 55.78 payment-file hours/month, and 102.60 process-file hours/month are separate management-data references. Capacity can be considered only after comparable scope, observed time, required-control classification, removal rate, redeployment evidence, cost, owner, and Finance approval. It must remain separate from P&L and headcount.

## Stop, pause, rollback, and no-scale rules

| Trigger | Required response | Proposed decision owner |
|---|---|---|
| Source population/count/value does not reconcile or extraction logic is unapproved | Pause; retain the 7,600-record boundary; no enterprise inference or launch | Shared Services Lead / IT-Data |
| Source documents, criticality, reason/action, required timestamps, or reviewer capacity cannot support the selected review/intervention | Pause diagnostic or redesign scope; record evidence gaps | Shared Services Lead |
| Material definition, process, system, or population change breaks comparability | Segment or rebuild baseline; do not claim improvement | Shared Services Lead / data owner |
| Late release or rejection worsens beyond approved tolerance | Pause intervention; investigate and restore approved process if service/control risk exists | Shared Services Lead / BU Finance |
| Defined critical-service failure or confirmed control/access/cyber breach attributable to the pilot | Stop; preserve evidence; invoke contingency/rollback and incident response | Pilot accountable owner / control owner / CIO |
| Restoration cannot be verified within four hours | Stop and do not restart without remediation, retest, and reapproval | CIO / CFO-SteerCo delegate |
| Four-week evidence is incomplete, non-comparable, target is missed, or issue causes remain unsupported | Extend, redesign, or stop; do not scale or assign benefit | Shared Services Lead / CFO-SteerCo |

## Evaluation and separate scale decision

A later pilot is technically complete only after four consecutive comparable operating weeks in which the controlled population/count/value reconcile, the pre-agreed exception and repair measures improve, late release and rejection do not worsen, every reviewed issue has reason or explicit unknown plus owner/action evidence, defined critical-service failures remain zero, confirmed control breaches remain zero, and rollback evidence remains valid.

Completion is not approval to scale. The CFO/SteerCo must separately decide to stop, extend, redesign, or scale after reviewing:

- whether the evidenced causes, not just cohort labels, changed;
- like-for-like KPI stability and residual differences;
- critical-service, control, access, cyber, resilience, and rollback evidence;
- local/BU and Shared Services operating feedback;
- data completeness and measurement comparability;
- one-time and recurring cost evidence; and
- any proposed capacity or P&L line under Finance's separate validation rule.

## Open decisions before any launch

1. What source population, value, period, status, and duplicate/resubmission logic is authoritative?
2. Can the 120 records link to source documents, criticality, reason codes, event timestamps, control evidence, and outcomes?
3. Which causes are evidenced strongly enough to select a bounded intervention and comparator?
4. Which payment types are critical, what blackout calendar applies, and what service tolerance triggers pause?
5. Which process targets are reasonable after the controlled baseline, and who approves them?
6. What low/base/high implementation and run-cost range is acceptable?
7. Who has pause, rollback, restart, and later scale authority?

Until those decisions are evidenced and recorded, this remains a design-only charter.

## Evidence provenance

- Pilot charter completeness, controlled-baseline, population, service/control, cost, rollback, and scale/stop expectations: `W2_workplan.md`, Week 3 readiness and success sections.
- Payment definitions, mutually exclusive cohorts, extract boundary, and KPI limitations: `W2_metric_contract.md` and `W2_analysis_log.md` A11–A12.
- Reconciled priority-union evidence and counterevidence: `W2_findings_log.md` F09–F10.
- Current-state payment handoffs and control gaps: `W2_current_state_process_map_and_RACI.md`.
- Future-state principles: `W3_design_principles.md`, especially DP-03 through DP-08.
- Initial FY2026 affordability ceiling: start-of-Week-3 CFO update recorded in `W3_workplan.md` and `W3_analysis_log.md`; it is not a pilot cost estimate.
- Client and stakeholder constraints: `client/CLIENT_BRIEF.md` and `client/STAKEHOLDER_PACK.md`.

The supplied population and reproduced measures are `ACG-DATA` / `ANALYST-CALC`. The diagnostic selection, intervention, targets, timing, ownership, cost requirements, and gates are `ANALYST-JUDGMENT` / `ANALYST-ASSUMPTION` and do not authorize execution or value.
