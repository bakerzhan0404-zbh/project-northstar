# Project Northstar — Week 2 Diagnostic Checkpoint

## Slide 1 — ACG should advance to option design, but only through two targeted pilot designs and three evidence gates

### Executive diagnosis

| **ACT NOW** | **DESIGN, DO NOT BOOK** | **CONSTRAIN THE CASE** |
|---|---|---|
| All 23 delayed accounts use portal or spreadsheet reporting; payment friction concentrates in two supplied-record cohorts | The all-status 14-day payment-intent sensitivity leaves $38.13m net on 30 June, but validated movable cash is not established | 150 hours/month and ten closures are unsupported as funded benefits |
| Design pilots for delayed balance sources and manual-touch/cross-border-wire flows | Continue liquidity option design; book $0 in the funded case until certification | Use 50 hours/month and two closures only as downside tests |

### Decisions requested today

1. **Authorize Week 3 option development and comparison:** local stabilization, federated coordination, and globally coordinated alternatives around one data/control foundation, using the $21m / two-closure / 50-hour downside tests.
2. **Approve design—not execution—of two bounded validation pilots:** delayed balance reporting and manual-touch/cross-border-wire payment cohorts, outside peak season with service, control, and four-hour rollback gates.
3. **Approve the evidence owners and proposed due dates:** visibility (Group Treasurer, 18 August), payment/process (Shared Services Lead, 19 August), and mobility/economics (Group Treasurer, 21 August); keep related value outside the funded case until certification and Finance approval.

**Governing message:** ACG has enough evidence to design and test the transformation—not enough to fund the full value claim.

**Source:** Week 2 findings F07–F11; 57/57 Week 2 diagnostic assertions and 10/10 supplied data-quality tests pass.

<details>
<summary>Speaker notes</summary>

Open with the distinction between action and value approval. The observable gaps justify targeted pilots. The liquidity, capacity, and fee outcomes remain conditional. Ask the committee to approve the Week 3 decision process, not a predetermined technology or ambition.

[Sources]
- `deliverables/working/week_2/W2_findings_log.md`
- `data/processed/W2_reconciliation_metrics.csv`
- `tests/test_week2_diagnostic.py`
[/Sources]

</details>

---

## Slide 2 — Reporting delay is source-concentrated and testable; the analysis does not yet validate a movable-cash amount

### Visibility: every delayed account sits in two source methods

| API | Host-to-host | Portal | Spreadsheet |
|---:|---:|---:|---:|
| 12 accounts | 20 accounts | 9 accounts | 14 accounts |
| Same day | Same day | One day late | Two-to-three days late |

**58.18%** of account-days are same-day under the date proxy. Across the six-month panel, same-day accounts represent **55.15%** of summed positive estimated-available USD across account-days. Median delayed positive estimated availability is **$26.01m/day**. **The reporting-date proxy is not proof of start-of-day or within-24-hour visibility.**

### 30 June liquidity ladder

```text
$57.80m  gross positive estimated availability
 −$8.05m  preliminary restriction flags
 −$2.14m  negative account positions
────────
$47.61m  apparent net before buffer
 −$9.48m  effective reduction after account floors (all statuses)
────────
$38.13m  all-status 14-day payment-intent sensitivity
   N/E    validated movable cash — NOT ESTABLISHED
```

| Net threshold | Seven-day windows | 14-day windows |
|---|---:|---:|
| $21m stress | 175/175 | 168/168 |
| $35m base | 175/175 | 138/168 |
| $46.2m upside | 0/175 | 0/168 |

The all-status 14-day payment-intent window is $12.65m; $10.83m sits on preliminarily unflagged accounts, and account-level floors cap the effective reduction at $9.48m. **Ask:** Validate timestamps for all 55 accounts and certify mobility, buffers, funding events, facility use, and economics before any liquidity value is funded.

<details>
<summary>Speaker notes</summary>

Do not call date equality start-of-day or within 24 hours. Do not call the scenario surplus transferable. The message is that option design remains warranted, while the base case needs account-level proof. The upside is not supported after netting.

[Sources]
- `data/processed/W2_visibility_diagnostic.csv`
- `data/processed/W2_liquidity_scenarios.csv`
- `data/processed/W2_liquidity_thresholds.csv`
[/Sources]

</details>

---

## Slide 3 — Within 7,600 supplied records, two cohorts—not the whole payment estate—should anchor root-cause testing

### Manual-touch records

| Metric | Manual touch | No manual touch | Difference |
|---|---:|---:|---:|
| Record share | 31.51% | 68.49% | — |
| Exception rate | **12.69%** | 3.36% | **+9.33 pts / 3.78×** |
| Late-release rate | **9.48%** | 2.94% | **+6.54 pts / 3.22×** |
| Repair contribution | **63.35%** | 36.65% | — |

### Wire geography

| Metric | Cross-border wire | Domestic wire | Difference |
|---|---:|---:|---:|
| Records | 786 | 612 | — |
| Exception rate | **13.99%** | 4.41% | **+9.58 pts / 3.17×** |
| Late-release rate | **8.78%** | 4.90% | **+3.88 pts** |
| Repair contribution | **24.51%** | 5.74% | — |

Repair contribution is each cohort's share of all repair minutes in the extract. The two cohorts overlap and must not be added; findings are descriptive within the supplied records, not causal or ACG-wide.

### Counterevidence keeps the recommendation targeted

- **87.31%** of manual-touch records have no exception.
- **86.01%** of cross-border wires have no exception.
- Reason codes, event sequence, criticality, corridor, and approval/release timestamps are absent.

**Ask:** Reconcile the source population, then test intake completeness, cutoff discipline, format, and required controls in these two cohorts before sizing automation value.

<details>
<summary>Speaker notes</summary>

Keep the qualifier “within the supplied 7,600 records” in the spoken conclusion. Manual work may cause an error, respond to it, or perform a required control. Cross-border is not proof of FX activity. The evidence earns cohort priority, not a causal conclusion.

[Sources]
- `data/processed/W2_payment_diagnostic.csv`
- `deliverables/working/week_2/W2_analysis_log.md` (A11)
[/Sources]

</details>

---

## Slide 4 — A controlled data-to-decision spine—not ERP replacement—constrains Wave 1 sequencing

### Supporting findings

| Finding | Reconciled evidence | Design consequence |
|---|---|---|
| Capacity is material but unvalidated | 617.72 estimated manual hours/month; the process repair estimate is 84% above the payment-file estimate; High-criticality work = 315.48 hours | Reconcile scope, preserve/replace controls, and validate observed/removable time before funding 150 hours/month |
| Ten closures are unsupported | Four candidates; $7,800 estimated annual fees | Treat as controlled housekeeping, not a business-case pillar |

### Targeted maturity readout

```text
Emerging today                                18-month observable target
Fragmented ownership ───────────────────────► Confirmed global/local RACI
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
