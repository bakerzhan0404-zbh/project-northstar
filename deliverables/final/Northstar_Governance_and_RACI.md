# Project Northstar — Governance Model and Final RACI

**Prepared by:** Baker · **Date:** 24 August 2026
**Status:** Proposed for G0 confirmation; no client approvals inferred

## Governance design

| Forum | Chair / accountable owner | Cadence | Core members | Decision rights | Required records |
|---|---|---|---|---|---|
| Steering Committee | Group CFO | Monthly and at G0–G6 | Treasurer, CIO, Regional/BU Finance, Shared Services, Finance Benefits, Control owner; Legal/Tax as needed | Direction, scope, funding, wave gates, switch/stop/scale, unresolved cross-functional risk | Decision, condition, change, risk, and funding records |
| Transformation Office | Transformation Director | Weekly | Workstream leads, PMO, Finance Benefits, Change, Risk/Control | Integrated plan within tolerance; issue escalation; gate-pack quality; no authority to waive a critical gate | Plan, dependency, issue, change, gate, risk, and benefit registers |
| Cash & Data Workstream | Group Treasurer | Weekly; daily in production | Treasury Data, Regional Finance, IT/Data, Finance | Data contract, daily position, exception ownership, mobility recommendations within delegated authority | Population, reconciliation, exception, certification, and action logs |
| Payments & Service Workstream | Shared Services Lead | Weekly; daily in production | BU/Regional Finance, Payment Ops, IT, Control, Change | Intake/reason taxonomy, service and emergency process, test recommendation; no unapproved release/control bypass | Payment population, exception, service, emergency, control, and test logs |
| Technology & Control Workstream | CIO | Weekly and per release | Architecture, Cyber, IT Ops, Control owner, process leads | Architecture, access, security, release, recovery, rollback, control remediation | Architecture, access, test, incident, release, and recovery evidence |
| Benefits & Performance Review | Finance Benefits Lead | Monthly | Benefit owners, Controller, PMO, Treasury, Shared Services, CIO | Admit/reject value, approve formula/baseline changes, refresh costs; cannot approve program scope alone | KPI dictionary, cost/benefit ledger, attribution, variance and change history |
| Treasury Operating Council | Group Treasurer | Monthly after G4; BAU at G6 | Regional Treasury/Finance, Shared Services, IT service, Finance, Control | BAU policy/KPI/exceptions within approved mandate; escalate structural changes | KPI pack, policy/exception decisions, service and control actions |

## Escalation and tolerance rules

- Any critical control, cybersecurity, service, local-right, data-authenticity, or rollback failure goes immediately to the accountable control/process owner and can stop the affected activity.
- A likely one-time cost above `$1.5m`, an unapproved recurring run cost, or a benefit-definition change goes to the CFO/Steering Committee.
- A missing or late source remains in the denominator; the workstream cannot improve a KPI by excluding it silently.
- Uncertified cash contributes zero movable value and is ineligible for funding action.
- Any North America production change to routing or approval workflow inside the confirmed freeze is prohibited; any such change outside it requires Rachel Kim's sign-off.
- Any material change to population, formula, baseline, target, attribution, or timing requires Finance Benefits approval and restatement of comparisons where necessary.

## Final RACI

**R = Responsible · A = Accountable · C = Consulted · I = Informed. One accountable owner is shown per activity.**

| Activity / decision | CFO / SteerCo | Group Treasury | Regional Finance | BU / Local Finance | Shared Services | CIO / IT / Cyber | Finance Benefits | Legal / Tax | Control owner | Internal Audit |
|---|---|---|---|---|---|---|---|---|---|---|
| Approve direction, scope, funding, and gates | A | R | C | C | C | C | R | C | C | I |
| Own integrated mobilization and gate packs | A | R | C | C | R | R | R | C | C | I |
| Define cash/account data contract and cutoff | I | A | R | C | I | R | C | I | C | I |
| Maintain account/entity/source master and lineage | I | A | R | C | I | R | I | C | C | I |
| Produce and reconcile daily enterprise position | I | A/R | C | I | I | R | I | I | C | I |
| Certify restrictions, purpose, buffers, and service context | I | C | A | R | I | I | C | R | C | I |
| Approve funding action within delegated authority | I | A/R | C | C | I | I | C | C | C | I |
| Approve account closure | A | R | R | C | I | C | C | R | C | I |
| Define controlled payment population and KPI | I | C | C | C | A | R | C | I | C | I |
| Create and authorize complete payment request | I | I | C | A/R | C | I | I | I | C | I |
| Validate intake, cutoff, criticality, and format | I | C | C | R | A/R | C | I | I | C | I |
| Approve and release payment with SoD | I | I | C | A | R | C | I | I | C | I |
| Classify/repair exception and own cause backlog | I | C | C | R | A/R | R | I | I | C | I |
| Operate emergency payment and post-event review | I | C | C | A/R | R | C | I | I | C | I |
| Approve architecture, access, cyber, resilience, rollback | I | C | C | I | C | A/R | I | I | C | C |
| Approve management control design and remediation | I | C | C | C | R | R | I | I | A | C |
| Approve service/blackout/change calendar | I | C | R | A | R | C | I | I | C | I |
| Admit cost and realized value to ledger | C | R | C | I | R | I | A/R | C | C | I |
| Approve KPI/baseline/formula change | I | R | C | C | R | C | A | I | C | I |
| Approve production pilot, scale, or rollback | A | R | C | R | R | R | C | C | C | I |
| Accept BAU handoff | A | R | C | C | R | R | R | I | C | I |

## RACI safeguards

- Internal Audit is consulted and independent; it does not own management controls.
- Finance validates cost and value evidence but cannot certify legal, tax, operational, cyber, or service feasibility.
- Group Treasury's policy ownership does not eliminate approved local-service and emergency rights.
- Legal/Tax input is specialist evidence, not delegated to the project team.
- A pilot charter and G3/G4 decision are separate from this RACI; no production authorization is embedded here.

## Benefits governance

1. Benefit owners submit source evidence and calculation.
2. Finance Benefits reconciles population, baseline, formula, timing, attribution, and costs.
3. The process/control owner confirms no service or control degradation.
4. Finance admits the value as validated, funded, or recognized; these statuses are distinct.
5. The Steering Committee uses the ledger for funding/scale decisions but does not merge unlike value categories.
6. Any restatement preserves the prior version and rationale.

## BAU handoff evidence at G6

- Approved operating procedures and decision rights.
- Named KPI, data, service, control, support, and benefit owners.
- Two stable operating cycles with reconciled metrics.
- Current access and SoD certifications.
- Completed recovery/rollback evidence and open-risk acceptance.
- Current cost forecast and non-additive benefit ledger.
- Closed transition actions or explicitly accepted owners/dates.
