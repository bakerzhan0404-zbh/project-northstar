# Project Northstar — Week 2 Diagnostic Checkpoint

## Slide 1 — ACG should advance to option design, but only through two targeted pilot designs and three evidence gates

### Three findings management needs today

| **REPORTING** | **LIQUIDITY** | **PAYMENTS** |
|---|---|---|
| **23/55 delayed**; every delayed account uses portal or spreadsheet | **$38.13m 14-day screening result**; validated movable cash remains $0 established | **2,839-record priority union** contains 356 exceptions and 14,939 repair minutes |

### Decisions requested today

1. **Authorize the Week 3 three-option comparison.**
2. **Approve design—not execution—of two bounded validation pilots.**
3. **Confirm evidence owners and the 18 / 19 / 21 August deadlines.**

**Governing message:** ACG has enough evidence to design and test the transformation—not enough to fund the full value claim.

**Source:** Week 2 findings F07–F11.

<details>
<summary>Speaker notes</summary>

Open with the distinction between action and value approval. The three options are local stabilization, federated coordination, and a globally coordinated model around one data/control spine. Score them against the same $21m mobility, two-closure, and 50-hour downside tests; do not pre-select an ambition or technology.

The two charters are for delayed-balance reporting and the deduplicated priority-payment population. They are design approvals only. Execution remains gated by named owners, authoritative sources, service/control criteria, peak-season protection, and a tested four-hour rollback.

Evidence packages: visibility—Group Treasurer, 18 August; payment/process—Shared Services Lead, 19 August; mobility/economics—Group Treasurer, 21 August. Keep mobility, capacity, and fee value outside the funded case until certification and Finance approval.

[Sources]
- `deliverables/working/week_2/W2_findings_log.md`
- `data/processed/W2_reconciliation_metrics.csv`
- `tests/test_week2_diagnostic.py`
[/Sources]

</details>

---

## Slide 2 — Reporting delay is source-concentrated and testable; the analysis does not yet validate a movable-cash amount

### Visibility distribution — 55 accounts

| Same-day date proxy | Delayed date proxy |
|---|---|
| API **12** + host-to-host **20** = **32** | Portal **9** + spreadsheet **14** = **23** |

Use one 100% stacked distribution bar in the presentation: `API 12 | H2H 20 | Portal 9 | Spreadsheet 14`, with a visual bracket for `32 same-day | 23 delayed`.

### 30 June liquidity waterfall

```text
$57.80m  gross positive estimated availability
 −$8.05m  preliminary restriction screen
 −$2.14m  negative account positions
────────
$47.61m  apparent net before screening window
 −$9.48m  effective 14-day reduction after account floors
────────
$38.13m  14-day screening result — NOT MOVABLE CASH
$0       validated movable cash established by current evidence
```

**Stability callout:** The $35m base passes **138/168 complete 14-day windows (82%)**; the minimum is **$31.28m**. The seven-day reference is **$42.84m** on 30 June; it is an alternative sensitivity, not another waterfall step.

**Ask:** Validate timestamps for all 55 accounts and certify every dollar entering funded mobility. The screen does not separately validate complete cash needs.

<details>
<summary>Speaker notes</summary>

Build the visibility visual as one horizontal 100% stacked bar. API and host-to-host are same-calendar-day in the supplied panel; portal is one day late; spreadsheet is two to three days late. The 58.18% account-day rate is a date proxy—not proof of start-of-day or elapsed-24-hour performance. Across the six-month panel, same-day accounts represent 55.15% of summed positive estimated-available USD; median delayed positive availability is $26.01m/day.

Build the liquidity visual as a true waterfall with only one window: $57.80m → −$8.05m → −$2.14m → $47.61m → −$9.48m → $38.13m. Seven and 14 days are alternatives, so do not deduct both. Seven days is a short-horizon payment-intent reference; 14 days extends the stability test across two weeks. Neither is an approved buffer or forecast.

Full threshold context: $21m passes 175/175 seven-day and 168/168 14-day windows; $35m passes 175/175 and 138/168; $46.2m passes none. The raw 14-day all-status window is $12.65m, of which $10.83m sits on preliminarily unflagged accounts; account floors limit the effective reduction to $9.48m.

The screen does not separately model or validate complete payroll, tax, seasonal or peak expenditure, receipts, settlement-calendar effects, forecast error, or extraordinary funding events. Payroll and tax records exist in the extract, but completeness is not certified. Do not call $38.13m surplus, available, transferable, or movable cash.

[Sources]
- `data/processed/W2_visibility_diagnostic.csv`
- `data/processed/W2_liquidity_scenarios.csv`
- `data/processed/W2_liquidity_thresholds.csv`
[/Sources]

</details>

---

## Slide 3 — A deduplicated 2,839-record priority union drives about 74% of exceptions and repair effort

### Within the supplied 7,600 records only

| Mutually exclusive cohort | Records | Exceptions (rate) | Repair minutes | Gross payment-intent amount |
|---|---:|---:|---:|---:|
| Manual touch only | 2,053 | 246 (11.98%) | 10,018 | $51.98m |
| **Manual touch + cross-border wire** | **342** | **58 (16.96%)** | **2,702** | **$6.85m** |
| Cross-border wire only | 444 | 52 (11.71%) | 2,219 | $7.88m |
| Neither priority cohort | 4,761 | 123 (2.58%) | 5,141 | $131.43m |

**Deduplicated priority union:** **2,839 records · 356 exceptions · 14,939 repair minutes · $66.71m gross payment-intent amount**. It contains 74.32% of all exceptions and 74.40% of repair minutes.

**Overlap:** 342 records = **14.28% of manual-touch records** and **43.51% of cross-border wires**. Do not add the original two cohort totals.

**Ask:** Reconcile the source population, then test intake completeness, cutoff discipline, format, and required controls across the four mutually exclusive strata before sizing automation value.

<details>
<summary>Speaker notes</summary>

Use a four-quadrant cohort visual or one compact table, with the overlap visually emphasized and the union as the dominant headline. Manual-touch only is the largest absolute workload; the overlap has the highest exception rate. The union is the correct additive population.

Keep “within the supplied 7,600 records” in the spoken conclusion. Gross amount uses payment-date project FX and every status; it is payment initiation/intent value, not confirmed settlement, cash outflow, or loss. The full extract has $198.14m gross amount, 479 exceptions, and 20,080 repair minutes.

Counterevidence: 87.31% of manual-touch records and 86.01% of cross-border wires have no exception. Reason codes, event sequence, criticality, beneficiary/corridor, and approval/release timestamps are absent. Manual work may cause an error, respond to it, or perform a required control; cross-border is not proof of FX activity. The evidence earns priority, not causation.

[Sources]
- `data/processed/W2_payment_diagnostic.csv`
- `deliverables/working/week_2/W2_analysis_log.md` (A11)
[/Sources]

</details>

---

## Slide 4 — A controlled data-to-decision spine—not ERP replacement—constrains Wave 1 sequencing

### Supporting findings

| Finding | Current evidence | Design consequence |
|---|---|---|
| Capacity is material but unvalidated | 617.72 estimated manual hours/month; the process repair estimate is 84% above the payment-file estimate (unreconciled source estimates); High-criticality work = 315.48 hours | Reconcile scope, preserve/replace controls, and validate observed/removable time before funding 150 hours/month |
| Ten closures are unsupported | Four candidates; $7,800 estimated annual fees | Treat as controlled housekeeping, not a business-case pillar |

### Targeted maturity readout

```text
Emerging today                                18-month observable target
End-to-end ownership unconfirmed ──────────► Confirmed global/local RACI
Manual source and process handoffs ─────────► Owned data, standard intake/cutoff
Unvalidated controls and KPIs ──────────────► Tested SoD, resilience, rollback, KPI
Three ERPs + 23 delayed sources ────────────► Staged integration around existing ERPs
```

**Ask:** Confirm the draft RACI and require data, control, service, and rollback gates before platform or pilot scale decisions.

<details>
<summary>Speaker notes</summary>

Avoid a composite maturity score. The dimensions move together: connectivity without ownership creates unreliable data; centralization without controls creates concentration risk; labor estimates without removability create a weak business case. Internal Audit is consulted; management owns the controls.

[Sources]
- `data/processed/W2_process_capacity.csv`
- `data/processed/W2_repair_baseline_reconciliation.csv`
- `data/processed/W2_account_diagnostic.csv`
- `deliverables/working/week_2/W2_maturity_heatmap.md`
- `deliverables/working/week_2/W2_current_state_process_map_and_RACI.md`
[/Sources]

</details>

---

## Slide 5 — Three validations will determine which Week 3 option survives the downside

**Decision flow:** Evidence gates → common downside tests → three-option comparison.

### Evidence-to-decision gates

| Gate | Proposed due | Proposed accountable owner | Decision unlocked |
|---|---:|---|---|
| **1 · Visibility** | 18 Aug | Group Treasurer | Pilot scope, architecture, 50/55 feasibility |
| **2 · Payment / process** | 19 Aug | Shared Services Lead | Targeted intervention and capacity case |
| **3 · Mobility / economics** | 21 Aug | Group Treasurer | Validated liquidity range and funded value |

### Every option must survive the same tests

| Downside test | Stress | Current diagnostic position |
|---|---:|---|
| Liquidity | $21m | Survives every modeled complete window; still not validated mobility |
| Closures | 2 accounts | Four candidates evidenced; ten unsupported |
| Capacity | 50 hours/month | Screening baseline exists; removability unvalidated |
| Controls / service | Four consecutive weeks + four-hour rollback | Requirements proposed; owner approval pending |

### Week 3 direction

Develop and compare **local stabilization, federated coordination, and globally coordinated** options. The preferred option must create one enterprise data/control spine, preserve defined local autonomy, work around existing ERPs, avoid peak-season disruption, and keep unvalidated value outside the funded base.

**Decision requested:** Authorize the Week 3 three-option comparison; approve design—not execution—of the two validation pilots; approve the dated evidence owners and due dates, with unvalidated value outside the funded case until certification.

<details>
<summary>Speaker notes</summary>

Close the conclusion loop: act on the observable gaps, design liquidity without booking it, and constrain the value case. Record owners and deadlines at the checkpoint. Receivables and FX remain P1/data-gated; no external benchmark substitutes for missing ACG evidence.

[Sources]
- `deliverables/working/week_2/W2_findings_log.md`
- `deliverables/working/week_2/W2_diagnostic_report.md`
- `deliverables/working/week_2/W2_current_state_process_map_and_RACI.md`
[/Sources]

</details>
