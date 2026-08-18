# Week 3 — Future-State Design Principles

**Prepared by:** Baker  
**Prepared date:** 18 August 2026  
**Working period:** 17–23 August 2026  
**Status:** Analyst proposal for Treasurer/CFO review; not client-approved  
**Classification:** Confidential — Project Northstar simulated client material

## Decision purpose

These principles translate the five Week 2 findings into observable tests for the three Week 3 strategic options. I defined them before scoring the options so that the recommendation cannot be reverse-engineered around a preferred solution.

The design mandate is **targeted and gated**: improve the observable reporting and payment gaps, preserve local service and controls, and create the evidence needed for later value approval. The current evidence does not authorize cash movement, account closure, production change, labor removal, or funded benefits.

## Evidence carried into design

| Evidence anchor | Design consequence | Boundary retained |
|---|---|---|
| 23 of 55 accounts are delayed under the supplied reporting-date proxy; all 23 use portal or spreadsheet reporting | Target the affected sources and ownership handoffs rather than replace every ERP or bank connection | Reporting date is not start-of-day or elapsed-24-hour performance |
| The 30 June 14-day result is a $38.13m screening sensitivity; the $35m threshold survives 138 of 168 complete windows | Design daily positioning, mobility certification, and buffer governance before assigning value | Validated movable cash remains `$0 established`; the screen is not surplus or transfer authority |
| The deduplicated priority-payment union contains 2,839 of 7,600 records, 356 of 479 exceptions, and 14,939 of 20,080 repair minutes | Diagnose and redesign defined cohorts rather than automate the entire population by assumption | The supplied extract is not a certified enterprise population; association does not establish cause |
| The process file estimates 102.60 repair hours/month versus 55.78 hours/month from the payment file | Reconcile scope and observe work before using capacity in the business case | The sources are independent and non-additive; neither proves removable labor or P&L |
| Four accounts pass the narrow closure-validation screen with $7,800 of estimated annual fees | Treat account rationalization as a validation workstream, not the economic case | No candidate is an approved closure and no fee is realized or funded |
| Start-of-Week-3 client update: FY2026 initial transformation funding is limited to $1.0–$1.5m; a larger commitment requires staged approval and demonstrated Wave 1 benefits | Make affordability, staging, and evidence-based release of funding explicit in every option | The envelope is an authorization ceiling, not an implementation-cost estimate or permission to spend |

## Eight design principles

| ID | Principle | Design requirement | Observable Week 3 / pilot test | Primary tension | Proposed accountable owner |
|---|---|---|---|---|---|
| DP-01 | **Decision-useful visibility before connectivity scale** | Every in-scope balance must have an authoritative source, receipt timestamp, approved cutoff, balance definition, owner, and reconciliation result | Before any later pilot launch, 100% of selected accounts have the six required fields; the pilot hypothesis is at least 95% on-time and 100% reconciled or formally explained for four consecutive weeks | Faster connectivity versus reliable meaning | Group Treasurer; CIO enables data |
| DP-02 | **Certify mobility before recognizing cash value** | Separate estimated availability, restrictions, operating buffers, negative positions, legal/entity mobility, timing, and economics at account level | Every dollar entering funded value has account-level certification and Finance approval; uncertified accounts contribute zero | Opportunity speed versus legal, service, and funding protection | Group Treasurer; Finance approves value; Legal/Tax consulted |
| DP-03 | **Global minimum standards with explicit local rights** | Set one minimum data, control, KPI, and escalation contract while retaining documented local operating, regulatory, tax, and emergency-payment rights | Each process step names the global standard, permitted local exception, approving owner, expiry/review date, and evidence trail | Standardization versus local autonomy | Group Treasurer and Shared Services; Regional Finance responsible locally |
| DP-04 | **Target interventions to evidenced friction** | Prioritize portal/spreadsheet reporting and the four mutually exclusive payment cohorts; do not treat all accounts or payments as equally broken | Visibility cohort follows the declared coverage rule; payment review uses 30 records per stratum and records any matching deviation | Focus and learning speed versus broad coverage | Treasurer for visibility; Shared Services Lead for payments |
| DP-05 | **Controls are acceptance criteria, not later remediation** | Preserve or replace segregation of duties, authorization, access, audit trail, duplicate prevention, sanctions, and reconciliation controls in the design | A named management control owner signs the inventory and test evidence; any critical control failure blocks launch or scale and cannot be offset by value | Efficiency versus control integrity | Management control owner; Internal Audit consulted |
| DP-06 | **Resilience, service continuity, and reversibility by design** | Protect payroll, tax, critical suppliers, refunds, peak periods, and local emergency execution; maintain a rehearsed return to the approved prior process | Zero defined critical-service or control incidents; approved blackout calendar; rollback rehearsal and later restoration at or below four hours | Central coordination versus operational resilience | CIO and relevant BU Finance / process owner |
| DP-07 | **One accountable owner and lineage for every decision metric** | Every KPI must state source, grain, denominator, period, formula, owner, evidence label, limitation, refresh, and change history | 100% of decision KPIs pass the metric-contract checklist; changed definitions require a decision-log entry before comparison | Speed of reporting versus governance discipline | Data owner accountable; Finance/Treasury owns decision use |
| DP-08 | **Modular integration and staged scalability** | Use reusable data and control interfaces across the three current ERP environments without deep investment in a retiring platform or a single irreversible rollout | Each option identifies minimum interfaces, legacy transition, dependencies, bounded pilot, scale gate, and exit path; the initial FY2026 stage must fit the $1.0–$1.5m envelope or return for staged approval, and no scale occurs before four compliant weeks | Near-term affordability versus long-term architecture | CIO; CFO/Finance and architecture/cybersecurity review required |

## How trade-offs are resolved

The principles are not equally substitutable. I will use a **gate-then-score** decision rule:

1. **Non-compensating gates first:** data ownership, controls, service/peak continuity, local rights, resilience, accountable ownership, and four-hour rollback must be satisfied or remain explicit pre-execution conditions. A high value or scalability score cannot offset a failed critical gate.
2. **Weighted comparison second:** only then compare evidence fit, control/resilience, feasibility/speed, local adaptability, scalability, value potential, and reversibility using weights fixed before option scores are reviewed.
3. **Sensitivity and switching conditions third:** test controls-first, speed-first, scale/value-first, and local-autonomy-first weights. State what evidence or priority change would alter the recommendation.
4. **Human approval last:** the model supports a Steering Committee decision; it does not authorize execution, funding, cash movement, closure, or labor removal.

## Principle-to-finding traceability

| Week 2 finding | Principles that answer it | Evidence still required |
|---|---|---|
| F07 · Reporting delay is source-concentrated | DP-01, DP-04, DP-07, DP-08 | Receipt timestamps, approved cutoffs, balance types, owners, reconciliation results, and pilot readiness for all 55 accounts |
| F08 · Liquidity screen validates no movable cash | DP-02, DP-03, DP-05, DP-06, DP-07 | Restrictions, operating buffers, receipts/forecast events, transferability, facility use, timing, and economics by account |
| F09 · Priority payment union concentrates supplied-record friction | DP-03, DP-04, DP-05, DP-07, DP-08 | Source-population reconciliation, reason codes, event timestamps, criticality, source documents, and matched-control review |
| F10 · Capacity target is not fundable | DP-04, DP-05, DP-07 | Comparable scope, observed time, required-control classification, removal rate, redeployment evidence, and Finance approval |
| F11 · Four closure candidates require validation | DP-02, DP-03, DP-05, DP-06 | Local purpose, receipts/direct debits, linked services, signatories, regulatory/tax needs, closure cost, continuity, and actual fee removal |

## Validation and change control

- The Group Treasurer, CIO, Shared Services Lead, Regional Finance, Finance, and management control owner must confirm or record disagreement with the principles relevant to their accountability.
- A principle changes only through the Week 3 decision log, with the reason, owner, affected option scores, and rerun sensitivity recorded.
- Proposed KPI thresholds are design hypotheses until the named owner approves the definition, baseline, and tolerance.
- New evidence enters the option or business-case model only after population/source reconciliation and an analysis-log update.

## Current conclusion

The principles favor a staged model that combines global standards and evidence governance with regional/local execution rights. That is a design hypothesis—not yet the preferred-option decision. The three options must now be scored transparently, tested under alternative priorities, and filtered through the non-compensating control and evidence gates.
