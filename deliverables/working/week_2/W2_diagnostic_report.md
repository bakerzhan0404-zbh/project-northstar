# Project Northstar — Week 2 Current-State Diagnostic

**Prepared by:** Baker

**Reporting date:** 16 August 2026

**Status:** Ready for mentor/client review; not client-approved

**Classification:** Confidential — Project Northstar simulated client material

---

## Page 1 — ACG should advance to Week 3 option design, but only as a targeted and gated transformation

### Executive diagnosis in 90 seconds

The diagnostic supports action on **observable reporting and payment gaps**, but it does not yet support a broad platform program or a funded claim for movable cash, labor savings, or ten account closures.

| What the evidence says | Decision consequence now | Evidence required before value approval |
|---|---|---|
| All 23 delayed accounts use portal or spreadsheet reporting; median delayed positive estimated availability is $26.01m/day | Design a pilot for the highest-exposure delayed sources and define ownership before selecting a platform | Timestamp, cutoff, balance type, source, and reconciliation for all 55 accounts |
| The all-status 14-day payment-intent sensitivity leaves $38.13m net on 30 June, but the $35m threshold survives only 138/168 complete windows and validated movable cash remains unestablished | Continue liquidity option design; carry $0 validated movable cash in the funded case | Account-level mobility, operating buffers, funding events, facility use, transfer timing, and economics |
| Within 7,600 supplied records, manual-touch and cross-border-wire cohorts carry disproportionate exception and repair effort | Test targeted intake, cutoff, format, and control interventions—not uniform automation | Controlled population, reason codes, criticality, approval/release timestamps, and observed process time |

### Three decisions requested

1. **Authorize Week 3 option development and comparison:** local stabilization, federated coordination, and globally coordinated alternatives around one data/control foundation, using the $21m / two-closure / 50-hour downside tests.
2. **Approve design—not execution—of two bounded validation pilots:** delayed balance reporting and manual-touch/cross-border-wire payment cohorts, outside peak season with service, control, and four-hour rollback gates.
3. **Approve the evidence owners and proposed due dates:** visibility (Group Treasurer, 18 August), payment/process (Shared Services Lead, 19 August), and mobility/economics (Group Treasurer, 21 August); keep related value outside the funded case until certification and Finance approval.

### Evidence status

All 57 Week 2 diagnostic assertions and the 10 supplied data-quality tests pass. Arithmetic is reproducible; source completeness, causation, transferability, and benefit realization remain separate questions.

<div style="page-break-after: always;"></div>

## Page 2 — Five findings determine the Week 3 design; everything else is supporting detail

| Rank | Promoted finding | Why it changes the decision | Confidence |
|---:|---|---|---|
| 1 | **Reporting delay is source-concentrated:** 23/55 accounts are delayed, all through portal or spreadsheet | A targeted connectivity/data-owner intervention is testable without ERP replacement | High for pattern; low for decision cost |
| 2 | **Liquidity passes a screen, not a mobility proof:** $38.13m net after the all-status 14-day payment-intent sensitivity on 30 June; $35m fails on 30/168 complete windows | A liquidity-led option remains viable, but no cash value can be booked yet | High for arithmetic; low for mobility/economics |
| 3 | **Payment friction is concentrated within the supplied extract:** manual-touch and cross-border-wire cohorts over-index on exception/repair | Options should target defined cohorts and root causes, not automate every flow uniformly | High for extract arithmetic; medium for prioritization |
| 4 | **Capacity is material but unfundable:** 617.72 estimated hours/month, 315.48 on High-criticality work, and a process repair estimate 84% above the payment-file estimate | Process redesign must preserve controls and validate observed/removable time before benefits | Medium |
| 5 | **The ten-account stretch is unsupported:** four candidates and $7,800 of estimated annual fees survive the narrow screen | Rationalization is Wave 1 housekeeping, not a business-case anchor | High for screen; low for closability |

### Synthesis—not five separate workstreams

The findings resolve into one operating-model problem: **ACG lacks a controlled daily decision chain from authoritative balance/payment data to enterprise action and benefit validation**. Connectivity, policy, ownership, controls, and KPIs therefore need to move together. A technology-only response would digitize unresolved definitions; a purely local response would preserve the coordination gap.

Source: [Week 2 findings log](W2_findings_log.md).

<div style="page-break-after: always;"></div>

## Page 3 — The visibility gap is source-concentrated and selectively testable; account closures are secondary

### Visibility: 23 delayed sources explain the gap

| Source method | Accounts | Date-level result | Decision interpretation |
|---|---:|---|---|
| API | 12 | 100% same-calendar-day | Preserve and validate timestamp/cutoff performance |
| Host-to-host | 20 | 100% same-calendar-day | Preserve; assess resilience and ownership |
| Portal | 9 | 100% one-calendar-day delayed | Candidate for retrieval automation or controlled earlier cutoff |
| Spreadsheet | 14 | 100% two-to-three days delayed | Highest-priority source and data-ownership remediation |

Overall, 5,792/9,955 account-days (58.18%) are same-day and 7,421 (74.55%) fall within one calendar day. Across the six-month panel, same-day accounts represent 55.15% of summed positive estimated-available USD across account-days. These are reporting-date proxies—not start-of-day, elapsed-24-hour, or 30 June cash KPIs.

**Implication:** Design a risk/value pilot across the highest-exposure portal/spreadsheet accounts, establish the authoritative source and owner, then scale only after four consecutive weeks of service and control performance.

### Account footprint: validate four, do not promise ten

The pre-defined primary screen—dormant + legacy + zero supplied payment records—identifies four accounts with $7,800 of gross estimated annual fees. No account is approved for closure. Debit-payment absence does not exclude receipts, direct debits, linked services, signatories, regulatory purpose, resilience, or closure costs.

**Implication:** Put four accounts through local validation. Do not expand the commitment or book fee savings until dependencies and actual fee removal are certified.

Sources: `W2_visibility_diagnostic.csv`; `W2_account_diagnostic.csv`.

<div style="page-break-after: always;"></div>

## Page 4 — The downside screen is encouraging, but mobility and economics remain the decisive missing evidence

### 30 June liquidity ladder

| Layer | USD | What it means |
|---|---:|---|
| Gross positive estimated availability | $57.80m | Positive account estimates before deficits, restrictions, and buffers |
| Less preliminary restriction flags | $(8.05)m | Screen only; requires legal/local certification |
| Preliminarily unflagged positive estimate | $49.75m | Unflagged does not mean movable |
| Add negative account positions | $(2.14)m | Two persistent negative accounts |
| Apparent net before buffer | $47.61m | Still not movable cash |
| Net after seven-day all-status payment-intent sensitivity | $42.84m | Account-level floors cap the effective reduction |
| Net after 14-day all-status payment-intent sensitivity | $38.13m | More conservative scenario; still not a forecast |
| **Validated movable cash** | **Not established** | Account-level transferability and operating need are absent |

### Threshold test across complete rolling windows

| Hypothesis | Seven-day all-status screen | 14-day all-status screen | Diagnostic conclusion |
|---|---:|---:|---|
| $21m stress | 175/175 days | 168/168 days | Survives modeled downside, not validation |
| $35m base | 175/175 days | 138/168 days | Viable for option design; not stable enough to book |
| $46.2m upside | 0/175 days | 0/168 days | Not supported after netting |

Both screens use every supplied payment status as a conservative payment-intent sensitivity; status is not settlement. On 30 June, the raw 14-day window is $12.65m, $10.83m sits on preliminarily unflagged accounts, and $9.48m is absorbed after account-level floors. Restricting the sensitivity to Completed/Repaired records changes the final result only from $38.13m to $38.15m.

Two active operating accounts remain negative on every observed day; entity deficits occur on 45/181 days, but the largest entity net deficit is only $(0.24)m. This is evidence for better daily coordination, not proof of avoidable borrowing cost.

**Week 3 gate:** certify restriction, buffer, settlement, legal/tax, transfer timing, facility use, and borrowing/transfer economics at account level. Until then, the funded mobility line remains zero.

Sources: `W2_liquidity_scenarios.csv`; `W2_liquidity_thresholds.csv`; `W2_simultaneous_positions_daily.csv`.

<div style="page-break-after: always;"></div>

## Page 5 — Payment options should target two cohorts, while the cause and enterprise benefit remain unproven

### Within the supplied 7,600 records only

| Cohort | Share of records | Exception rate | Share of exceptions | Late rate | Share of repair |
|---|---:|---:|---:|---:|---:|
| Manual touch | 31.51% | 12.69% | 63.47% | 9.48% | 63.35% |
| No manual touch | 68.49% | 3.36% | 36.53% | 2.94% | 36.65% |
| Cross-border wire | 10.34% | 13.99% | 22.96% | 8.78% | 24.51% |
| Domestic wire | 8.05% | 4.41% | 5.64% | 4.90% | 5.74% |

Manual-touch records show a 9.33-point exception-rate uplift versus records without manual touch. Cross-border wires show a 9.58-point uplift versus domestic wires. The correct conclusion is **priority for root-cause testing**, not causation: 87.31% of manual-touch records and 86.01% of cross-border wires have no exception.

The file does not contain invoice/beneficiary completeness, reason codes, event sequence, approval/release timestamps, urgency, criticality, beneficiary corridor, or source-population controls. Manual work may cause an error, respond to it, or perform a required control.

**Week 3 implication:** Compare options on their ability to standardize required intake, enforce cutoffs, manage formats, preserve authorization/segregation, and generate reason-coded feedback. Do not annualize or generalize the supplied extract until it reconciles to the source population.

Source: `W2_payment_diagnostic.csv`.

<div style="page-break-after: always;"></div>

## Page 6 — Governance, data, process, and controls must advance together; Week 3 remains option-neutral

### Targeted maturity readout

| Capability | Current evidence | 18-month observable target |
|---|---|---|
| Governance / organization | Fragmented local practices and unconfirmed end-to-end accountability | Enterprise policy, confirmed RACI, local-autonomy rules, stage gates, and benefit owners |
| Cash / payment process | Delayed/manual handoffs, reactive funding, varied formats and approvals | Daily reconciled position, buffer/mobility policy, standard intake/cutoff, reason-coded exceptions |
| Technology / data | 32 automated same-day accounts; 23 portal/spreadsheet accounts; three ERPs | Staged integration around existing ERPs, named data owners, timestamp/source controls, retirement-aware architecture |
| Controls / performance | 315.48 High-criticality hours; access/emergency concerns; no certified KPI or benefit baselines | Tested SoD/access/emergency/resilience/rollback and owned KPI/benefit governance |

No overall maturity average is used: the dimensions are not equally important to the decision.

### Process-capacity boundary

Four activities—receipt reconciliation, payment exception repair, cash forecasting, and payment file preparation—contribute 439.85 of 617.72 estimated manual hours/month. Yet the process-file repair estimate is 102.60 hours/month, 84% above the 55.78-hour payment-file estimate. The 150-hour target equals 24.28% of the screening baseline and is not validated as removable.

### Design test for Week 3

Every option must be tested against the same requirement: one enterprise control/data spine with defined local execution and emergency authority. The comparison remains neutral across local stabilization, federated coordination, and a globally coordinated model; each must work around existing ERPs, avoid peak-season disruption, prove rollback, and sequence platform choices after—not before—data ownership and control requirements.

Sources: [maturity heatmap](W2_maturity_heatmap.md); [process map and RACI](W2_current_state_process_map_and_RACI.md); `W2_process_capacity.csv`.

<div style="page-break-after: always;"></div>

## Page 7 — Week 3 should compare ambition levels against the same downside and control tests

| Option direction to develop | Diagnostic strength | Diagnostic weakness | Minimum condition to remain viable |
|---|---|---|---|
| Local stabilization | Lowest execution risk; can improve definitions, cutoff discipline, and local controls | Does not resolve enterprise visibility, liquidity coordination, or common ownership | Must deliver controlled account/payment data to Group Treasury |
| Federated coordination | Fits source-concentrated gaps, local-autonomy constraints, and staged integration | Requires disciplined global policy and local adoption; benefits remain gated | Confirm RACI, data owners, pilot service levels, mobility rules, and control sign-off |
| Globally coordinated model | Highest potential consistency and enterprise control | Mobility, resilience, local-market feasibility, and funding evidence are not ready | Must survive legal/tax, cyber/resilience, local-service, and $21m downside tests |

### Non-negotiable downside cases

- **Liquidity:** $21m remains the stress case; $35m is a design hypothesis, not funded cash; $46.2m is not supported.
- **Accounts:** Two closures under stress; four currently evidenced; ten unsupported.
- **Capacity:** 50 hours/month under stress; 150 hours/month remains an unvalidated target.
- **Controls:** No efficiency benefit assumes removal of required authorization, segregation, access, emergency, audit-trail, resilience, or service controls.
- **Timing:** Pilot outside peak season with four consecutive weeks of service/control gates and a four-hour rollback standard.

### No-regret components across all options

1. Global metric/data definitions and named owners.
2. Timestamped visibility control for all 55 accounts.
3. Four-account closure validation.
4. Reason-coded manual-touch/cross-border-wire diagnostic.
5. Certified liquidity layers and operating-buffer policy.
6. KPI, decision, risk, and benefit governance.

<div style="page-break-after: always;"></div>

## Page 8 — Three evidence packages now determine the recommendation and funded value range

| Evidence package | Required evidence | Proposed accountable owner | Proposed due | Earliest decision unlocked |
|---|---|---|---:|---|
| Visibility and authoritative cash data | Receipt timestamp, cutoff, balance type, source, reconciliation, owner, and service result for all 55 accounts | Group Treasurer, supported by Regional Finance and IT/Data | 18 Aug | Pilot scope, target architecture, and 50/55 feasibility |
| Mobility and funding economics | Legal/local certification, operating buffers, settlement constraints, forecast/funding events, facility use, interest and transfer costs | Group Treasurer, supported by Regional Finance and Legal/Tax | 21 Aug | Validated movable-cash range and liquidity business case |
| Payment/process control | Source population/value totals, sample logic, reason codes, criticality, approval/release timestamps, observed time, removal and redeployment rates | Shared Services Lead, supported by IT/Data and control owners | 19 Aug | Targeted intervention, capacity range, and payment benefit case |

### Decisions to record at the diagnostic checkpoint

1. **Authorize Week 3 option development and comparison:** local stabilization, federated coordination, and globally coordinated alternatives around one data/control foundation, using the $21m / two-closure / 50-hour downside tests.
2. **Approve design—not execution—of two bounded validation pilots:** delayed balance reporting and manual-touch/cross-border-wire payment cohorts, outside peak season with service, control, and four-hour rollback gates.
3. **Approve the evidence owners and proposed due dates:** visibility (Group Treasurer, 18 August), payment/process (Shared Services Lead, 19 August), and mobility/economics (Group Treasurer, 21 August); keep related value outside the funded case until certification and Finance approval.

### Final diagnostic statement

ACG has enough evidence to **design and test a transformation**, but not enough to **fund the full value claim**. Week 3 should therefore choose the operating model that best closes the observable visibility, payment, ownership, and control gaps while making liquidity and capacity benefits conditional on named evidence gates.

Technical methods and detailed cuts: [Week 2 technical appendix](W2_technical_appendix.md) · [analysis log](W2_analysis_log.md) · [findings log](W2_findings_log.md).
