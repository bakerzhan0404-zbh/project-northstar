# Week 3 — Proposed Future-State Treasury Operating Model

**Prepared by:** Baker

**Prepared date:** 18 August 2026

**Working period:** 17–23 August 2026

**Status:** Analyst proposal for CFO/Treasurer review; design only; not client-approved

**Classification:** Confidential — Project Northstar simulated client material

## Decision purpose

This document operationalizes **federated coordination**, the provisional analyst direction in `W3_strategic_options.md`, as a proposed future-state reference model. The option result is directional and conditional; it is **not client approval, an execution authorization, a costed implementation plan, or proof of performance/value**. The CFO checkpoint should align on the operating-model direction, the non-negotiable conditions, and the evidence required before any later pilot or investment decision. If its global ownership, staged integration, affordability, or control gates cannot close, the documented switching condition is local stabilization with a minimum governed Group Treasury data feed.

The proposal creates one governed daily decision chain while preserving explicit regional and local execution rights:

> **Global standards and evidence ownership → regional/local validation and service context → controlled enterprise cash and payment decisions → local or shared execution → confirmation, reconciliation, and corrective action.**

No part of this design authorizes a production change, cash transfer, account closure, platform purchase, labor removal, or benefit recognition. Validated movable cash remains `$0` in the funded case, and validated redeployable capacity remains `0 hours/month` under the current evidence.

The start-of-Week-3 CFO update limits the **initial FY2026 transformation stage to a $1.0–$1.5m envelope** unless a larger commitment receives staged approval after demonstrated Wave 1 benefits. The envelope is an authorization ceiling—not a cost estimate, pilot budget, or permission to spend. Every proposed initial stage must be costed and fit within the approved envelope or return for a separate decision.

## Evidence carried into the design

| Week 2 evidence | Operating-model response | Boundary retained |
|---|---|---|
| 23 of 55 accounts are delayed under the reporting-date proxy; every delayed account uses portal or spreadsheet reporting | Establish authoritative-source ownership, timestamp/cutoff control, and a targeted connectivity path rather than replace every ERP | Reporting date is not start-of-day performance; the operational cause remains unverified |
| The 30 June 14-day result is a $38.13m screen; the $35m threshold survives 138 of 168 complete windows | Separate the daily position from account-level mobility certification, approved buffers, and funding authorization | The screen is not transferable cash; funded mobility remains zero until certified and Finance-approved |
| Within the 7,600 supplied records, the deduplicated priority union contains 2,839 records, 356 exceptions, and 14,939 repair minutes | Standardize intake, reason coding, exception ownership, and feedback for defined cohorts before broad automation | The extract is not a certified ACG-wide population, and association does not prove cause |
| Process and payment repair estimates are 102.60 and 55.78 hours/month respectively | Preserve separate sources and validate scope, observed time, removability, and controls before any capacity claim | Neither baseline is validated labor removal or P&L |
| Four accounts pass a narrow closure-validation screen and carry $7,800 of estimated fees | Add a controlled account-certification workflow; treat closure as local validation, not a central instruction | Candidates are not approved closures and the fees are not realized savings |
| Start-of-Week-3 CFO update sets a $1.0–$1.5m FY2026 initial transformation envelope | Stage the operating model and require a costed approval gate before implementation | The ceiling supplies no implementation-cost estimate or spending authority |

## Proposed model at a glance

The proposed reference state is **federated coordination on a common data and control spine**. Group functions own policy, definitions, enterprise positioning, performance governance, and escalation. Regional and local teams retain the responsibility and authority needed to validate restrictions, operating needs, regulatory conditions, and urgent service execution. Shared Services operates standardized payment preparation and exception management. IT/Data enables authoritative interfaces, lineage, access, resilience, and rollback. Management owns controls; Internal Audit is consulted on design and evidence.

This model is **intended** to support staged implementation around ACG's three current ERP environments; architecture and integration feasibility remain unvalidated. It does not select a treasury platform, bank, vendor, or final architecture, and it requires any initial design to avoid deep investment in the ERP expected to retire.

## 1. Governance and decision rights

| Layer | Proposed accountability | Decisions retained | Required evidence |
|---|---|---|---|
| CFO / Steering Committee | Transformation ambition, funding envelope, risk appetite, scale/stop decisions, and benefit approval | Approve or defer mobilization, production pilot, scale, and funded benefits | Option decision, specialist reviews, cost range, control sign-off, service evidence, Finance-validated benefit case |
| Group Treasury | Global cash policy, daily position, visibility and mobility definitions, funding decision, account policy, and treasury KPI ownership | Set enterprise standards; approve funding action within delegated authority; escalate policy exceptions | Reconciled position, local attestations, buffer/restriction certification, approval evidence, decision log |
| Regional Finance | Regional aggregation, local-context validation, operating-buffer input, restriction/tax/regulatory coordination, and exception resolution | Confirm or challenge local facts; approve documented local exceptions within delegated rights | Entity/account evidence, local calendar, settlement and service needs, owner attestation |
| Local / BU Finance | Request quality, critical-service identification, local approvals, urgent-payment execution, and outcome confirmation | Protect customer refunds, payroll, tax, critical suppliers, and other approved local emergency needs | Authorized request, criticality, supporting document, approval, execution and confirmation evidence |
| Shared Services | Standard payment intake, file preparation, bank submission, status monitoring, repair workflow, and reason-coded corrective action | Operate the standard process and escalate policy, service, or control exceptions | Controlled population, timestamps, acknowledgements, reason/action history, reconciliations |
| IT / Data / Cybersecurity | Authoritative interfaces, data lineage, access, integration, monitoring, resilience, and rollback capability | Approve technical change within architecture/cyber policy; stop unsafe deployment | Source-to-target reconciliation, access/change evidence, monitoring, recovery and rollback test |
| Finance / Benefits | Cost baseline, benefit definitions, validation method, and benefit-ledger evidence | Validate, defer, or reject evidence for admission to the benefit ledger; CFO/SteerCo separately decides funding and scale | Reconciled baseline, formula, owner, timing, cost, realization evidence, approval |
| Management control owners | Control design, operation, deficiency response, and remediation approval | Block launch or scale when a required control is absent or ineffective | Control inventory, test evidence, issue owner, remediation and retest |
| Internal Audit | Independent consultation on control design and evidence; no operating ownership | Advise and challenge; management remains accountable | Design documentation and management test evidence |

All owners and decision rights remain proposed until the named client leaders confirm them.

## 2. Data ownership and system-of-record expectations

The future state requires authoritative data and evidence before additional connectivity. It does not require a single application to perform every role.

| Data object / evidence | Proposed business owner | System-of-record expectation | Minimum quality and lineage requirement |
|---|---|---|---|
| Bank balance and receipt event | Group Treasury, with Regional Finance validation | Bank-authoritative feed or controlled retrieval record; enterprise position layer stores receipt time and source | Account ID, balance type, value date, receipt timestamp, approved cutoff, source, currency, reconciliation result, owner |
| Account, bank, entity, and purpose master | Group Treasury | Governed reference master linked to ERP and bank identifiers | Unique identifiers, local purpose, status, signatory/service links, restriction and review history |
| Restriction, operating buffer, and mobility certification | Group Treasury; Regional Finance responsible for local evidence | Controlled certification register; legal/tax opinions remain in approved source repositories | Account-level scope, effective date, approver, restriction/buffer basis, permitted action, expiry/review date |
| Funding decision and execution | Group Treasury | Approved treasury decision record linked to bank/ERP execution and accounting confirmation | Initiator, approver, rationale, amount, entity, timing, authority, confirmation and accounting reference |
| Payment request and approval | BU Finance / process owner | ERP or controlled intake record | Required invoice/beneficiary fields, criticality, requested date, approvals, cutoff, change history |
| Payment file, acknowledgement, status, and exception | Shared Services | Controlled payment workflow linked to bank acknowledgement and ERP outcome | Payment ID, timestamps, channel, status, reason code, repair action, resubmission approval, owner, outcome |
| KPI and benefit evidence | Named metric/benefit owner | Governed reporting layer and decision log | Source, grain, denominator, formula, period, evidence label, limitation, owner, refresh, definition version |

If an authoritative source, owner, identifier, or reconciliation rule is absent, the item remains an exception and cannot silently enter a decision metric or funded benefit.

## 3. Daily cash-positioning operating cycle

| Proposed control point | Global role | Regional/local role | Output and service expectation |
|---|---|---|---|
| 1. Receive balances | Set source contract and approved receipt cutoff | Confirm local bank/calendar exceptions and ownership | Timestamped, source-identified account-day record |
| 2. Validate and reconcile | Monitor completeness and consolidated reconciliation | Validate balance type, explain breaks, and attest local context | Every expected account-day is reconciled or has an approved owner/action |
| 3. Build enterprise position | Consolidate by account, entity, region, currency, restriction, and evidence status | Confirm local operating needs, settlement timing, and known funding events | Daily decision position that separates observed, estimated, restricted, buffer-dependent, and uncertified layers |
| 4. Certify mobility | Apply enterprise policy and maintain certification status | Provide account/entity legal, tax, regulatory, service, and buffer evidence | Account-level certification; uncertified value contributes zero to funded mobility |
| 5. Decide funding action | Make or escalate the funding decision within delegated authority | Challenge local infeasibility and execute an approved local action | Authorized action, rationale, approvals, expected outcome, and fallback |
| 6. Execute and confirm | Monitor enterprise completion and exception | Execute through the approved channel and confirm local outcome | Bank acknowledgement, accounting entry, settlement/status evidence, exception if unresolved |
| 7. Learn and govern | Review service, exceptions, controls, and decision outcomes | Own corrective action for local/source exceptions | KPI pack, issue/action log, policy exception review, benefit evidence where applicable |

The exact cutoff, materiality tolerances, approval limits, and escalation times are **TBD and owner-approved before execution**. The visibility pilot hypothesis is at least 95% on-time and 100% reconciled or formally explained for four consecutive weeks; it is not the current baseline.

## 4. Payment-execution operating cycle

| Proposed control point | Process design | Owner / executor | Required evidence or gate |
|---|---|---|---|
| 1. Controlled request intake | Require standard invoice, beneficiary, entity, payment type, currency, amount, due date, criticality, and supporting evidence | BU Finance / requestor; Shared Services validates | Authorized request and complete required fields; exception routed, not silently repaired |
| 2. Policy and cutoff validation | Apply payment calendar, standard cutoff, local exception, and emergency classification | Shared Services; BU Finance owns urgency/service need | Approved cutoff and local exception rule; emergency path used only with documented authority |
| 3. Approval and control | Apply delegated authority, segregation, access, duplicate, sanctions/beneficiary, and audit-trail controls | Entity approvers and management control owner | Independent approvals and machine/user evidence before release |
| 4. File creation and secure submission | Use governed format, channel, and file/control totals | Shared Services; IT enables secure channel | Source-to-file reconciliation, transmission evidence, acknowledgement, retry/contingency rule |
| 5. Status, repair, and escalation | Classify status and reason; preserve approval on repair/resubmission | Shared Services, with requestor/IT/Bank support as needed | Reason code, root-cause category, owner, action, timestamps, resubmission approval and outcome |
| 6. Completion and accounting reconciliation | Link bank status to ERP/accounting result; identify aged unresolved items | Shared Services / Finance | Confirmation, accounting reference, reconciliation result, exception ageing |
| 7. Performance feedback | Review mutually exclusive cohorts, trends, service failures, controls, and actions | Shared Services accountable; Group Treasury and BU Finance review | Controlled denominator and like-for-like KPIs; corrective-action log; no unsupported extrapolation |

The supplied 7,600-record extract remains the only measured population. Prospective process targets and any capacity effect require a reconciled source population, observed work, approved controls, and a separate Finance validation.

## 5. Local autonomy and emergency rights

| Right or exception | Proposed local authority | Enterprise safeguard | Escalation / expiry |
|---|---|---|---|
| Protect payroll, tax, customer refunds, critical suppliers, and locally regulated obligations | Regional or BU Finance may invoke the approved emergency path within delegated authority | Named initiator/approver, SoD or documented compensating control, full audit trail, post-event reconciliation | Notify Group Treasury and control owner immediately; review by next business day or approved local timetable |
| Challenge a proposed cash movement or account action | Regional Finance may block pending evidence of restriction, buffer, settlement, tax, regulatory, or service feasibility | Document reason, evidence owner, consequence, and earliest review date | Group Treasury resolves or escalates; no movement while unresolved |
| Maintain a local account or process exception | Regional Finance proposes the exception | Named policy owner approval, purpose, control, review date, and exit condition | Time-bound review; expired exceptions cannot remain by default |
| Use a contingency channel during outage | Authorized local operator under the approved continuity plan | Tested access, dual control, limit, confirmation, recovery, and evidence preservation | Return to the standard route when restored; investigate and close the event |

Local autonomy is not an informal override. It is a governed right with explicit scope, authority, evidence, and review.

## 6. Control, service, and resilience contract

The detailed proposed controls are in `W3_control_inventory.csv`. The operating model applies these non-compensating gates:

1. **Data gate:** authoritative source, owner, identifier, timestamp, definition, and reconciliation rule exist for the in-scope record.
2. **Control gate:** authorization, segregation, access, audit trail, duplicate prevention, sanctions/beneficiary controls, and management sign-off are designed and testable.
3. **Service gate:** payroll, tax, customer refunds, critical suppliers, and other defined critical flows are protected; the change avoids the approved peak blackout.
4. **Resilience gate:** contingency access, recovery, monitoring, and rollback are rehearsed; the proposed rollback standard is at or below four hours.
5. **Evidence gate:** the population, denominator, formula, baseline, exception rule, and owner are approved before comparison.
6. **Value gate:** Finance approves the source, formula, costs, timing, realization, and owner before a benefit enters funded reporting.

A value or efficiency score cannot compensate for a failed gate.

## 7. Capability-to-root-cause traceability

| Proposed capability | Root cause / evidence gap addressed | Design principles | Observable design evidence |
|---|---|---|---|
| Authoritative cash-data contract | Delayed/manual sources and unclear ownership | DP-01, DP-07, DP-08 | Source, timestamp, cutoff, balance type, owner, and reconciliation rule for every selected account |
| Daily reconciled position and exception workflow | Weekly/stale consolidation and fragmented definitions | DP-01, DP-03, DP-07 | Expected account-day control total, break owner, resolution status, versioned metric |
| Mobility and buffer certification | Positive/estimated balances being mistaken for movable cash | DP-02, DP-03, DP-05 | Account-level certification with restriction, buffer, timing, approver, and review date |
| Standard payment intake and reason taxonomy | Manual repair concentration with unknown causes | DP-03, DP-04, DP-07 | Required fields, four mutually exclusive cohorts, reason/action/owner evidence |
| Controlled payment release and emergency route | Varied approvals, late release, local responsiveness concern | DP-03, DP-05, DP-06 | SoD, authority, cutoff, criticality, emergency approval, confirmation and review |
| Modular integration and evidence lineage | Three ERPs, retiring legacy instance, and unowned data | DP-07, DP-08 | Reusable interface contract, identifier mapping, source-to-target reconciliation, exit path |
| Service/control-led pilot governance | Peak-season, resilience, access, and centralization risk | DP-05, DP-06, DP-08 | Approved blackout, zero defined critical failures, rollback evidence, scale/stop decision |
| Benefits and change control | No certified value/capacity baseline or owner | DP-02, DP-07 | Separate value type, baseline, formula, cost, owner, validation and Finance approval |

## 8. Proposed sequencing and stage gates

| Stage | Authorized work | Exit evidence | Explicitly not authorized |
|---|---|---|---|
| Week 3 design | Confirm owners, reference model, data/control contract, pilot charters, and specialist-review questions | Recorded agreement/disagreement; complete design artifacts; open gates named | Production change, procurement, cash movement, closure, labor removal, funded value |
| Evidence readiness | Reconcile source populations, define approved cutoffs/baselines, complete control and service design, estimate costs, rehearse rollback | Named owners and approvals; controlled baseline; specialist reviews; costed initial stage within $1.0–$1.5m or separate staged approval; no-go issues closed | Pilot launch without CFO/SteerCo and operating-owner approval |
| Later bounded pilot | Operate only the approved cohort/process outside peak under the signed charter | Four consecutive compliant weeks, zero defined critical service/control failures, comparable evidence, cost and learning review | Enterprise scale, value recognition, account closure, or operating-model rollout |
| Separate scale decision | Evaluate service, control, data, architecture, cost, adoption, and benefit evidence | CFO/SteerCo decision with conditions, scope, funding, and owners | Automatic scale because a pilot completed |

## 9. Specialist decisions required before execution

| Decision area | Required review | Question that must be answered |
|---|---|---|
| Legal / tax / regulatory | Legal, Tax, Regional Finance | Which balances, transfers, accounts, signatories, and entity relationships are permitted, restricted, or conditional? |
| Accounting / Finance | Finance / Controller | How are transfers, fees, costs, capacity, and realized benefits recognized and reconciled? |
| Cybersecurity / access | CIO, Cybersecurity, control owner | Are source connections, identities, privileges, transmission, monitoring, and contingency access acceptable? |
| Architecture / data | CIO, enterprise/data architecture | Which sources are authoritative, how are identifiers and lineage controlled, and how does the retiring ERP affect sequence and exit? |
| Service / continuity | BU Finance, Regional Finance, Shared Services | Which flows are critical, what blackout calendar applies, and what constitutes pause or rollback? |
| Controls | Management control owner; Internal Audit consulted | Are preventive, detective, emergency, evidence-retention, and deficiency-response controls explicit and testable? |
| Benefits / funding | CFO and Finance | Which cost and benefit lines have approved baselines, owners, timing, dependencies, and realization evidence? |

These reviews provide conditions and evidence; this document does not provide legal, tax, regulatory, accounting, cybersecurity, or architecture advice.

## Current conclusion

ACG can define a future-state decision chain now, but it cannot yet approve execution or value. The proposed federated reference model addresses the observed source, ownership, payment, control, and resilience gaps while retaining explicit local rights. It should advance only as a design hypothesis through the option decision and the two bounded validation charters. Any later pilot or scale decision requires a separate approval after the named data, control, service, specialist, cost, and rollback gates are satisfied.

## Evidence provenance

- Week 3 objective and operating-model requirements: `program/ONE_MONTH_PLAYBOOK.md`, Week 3 Activity 4 and assignment items 4–5.
- Governing design rules: `W3_design_principles.md`, DP-01 through DP-08.
- Provisional strategic direction and switching conditions: `W3_strategic_options.md`; the weighted scores are `ANALYST-JUDGMENT`, not execution readiness or value.
- Initial FY2026 affordability ceiling: start-of-Week-3 CFO update recorded in `W3_workplan.md` and `W3_analysis_log.md`; it is not a cost estimate.
- Reconciled facts and limitations: `W2_findings_log.md`, `W2_metric_contract.md`, and `W2_analysis_log.md`.
- Process, ownership, and control starting point: `W2_current_state_process_map_and_RACI.md` and `W2_maturity_heatmap.md`.
- Pilot populations, KPIs, gates, rollback, and no-scale rules: `W2_workplan.md`, Week 3 readiness sections.
- Client constraints and stakeholder concerns: `client/CLIENT_BRIEF.md` and `client/STAKEHOLDER_PACK.md`.

Evidence labels: supplied client/project facts are `ACG-DATA`; reproduced Week 2 measures are `ANALYST-CALC`; proposed roles, processes, targets, and gates are `ANALYST-JUDGMENT` or `ANALYST-ASSUMPTION` until the named client owner approves them.
