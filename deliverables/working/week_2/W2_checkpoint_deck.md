# Project Northstar — Week 2 Diagnostic Checkpoint

## Slide 1 — ACG should advance to option design, but only through two targeted pilots and three evidence gates

### Executive diagnosis

| **ACT NOW** | **DESIGN, DO NOT BOOK** | **CONSTRAIN THE CASE** |
|---|---|---|
| All 23 delayed accounts use portal or spreadsheet reporting; payment friction concentrates in two supplied-record cohorts | The 14-day screen leaves $38.13m net on 30 June, but validated movable cash is not established | 150 hours/month and ten closures are unsupported as funded benefits |
| Pilot delayed balance sources and manual-touch/cross-border-wire flows | Continue liquidity option design with $0 validated mobility until certification | Use 50 hours/month and two closures only as downside tests |

### Decisions requested today

1. Authorize three Week 3 operating-model options around one data/control foundation.
2. Approve two bounded pilots outside peak season, with service, control, and rollback gates.
3. Assign accountable owners and deadlines to visibility, mobility, and payment/process evidence packages.

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

## Slide 2 — Reporting sources are fixable; the liquidity screen is encouraging but validates no movable cash

### Visibility: every delayed account sits in two source methods

| API | Host-to-host | Portal | Spreadsheet |
|---:|---:|---:|---:|
| 12 accounts | 20 accounts | 9 accounts | 14 accounts |
| Same day | Same day | One day late | Two-to-three days late |

**58.18%** of account-days and **55.15%** of positive estimated availability are same-day under the date proxy. Median delayed positive estimated availability is **$26.01m/day**.

### 30 June liquidity ladder

```text
$57.80m  gross positive estimated availability
 −$8.05m  preliminary restriction flags
 −$2.14m  negative account positions
────────
$47.61m  apparent net before buffer
 −$9.48m  absorbed 14-day supplied-payment buffer
────────
$38.13m  14-day netting sensitivity
   N/E    validated movable cash — NOT ESTABLISHED
```

| Net threshold | Seven-day windows | 14-day windows |
|---|---:|---:|
| $21m stress | 175/175 | 168/168 |
| $35m base | 175/175 | 138/168 |
| $46.2m upside | 0/175 | 0/168 |

**Ask:** Validate timestamps for all 55 accounts and certify mobility, buffers, funding events, facility use, and economics before any liquidity value is funded.

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

## Slide 4 — Governance and evidence—not ERP replacement—constrain Wave 1 feasibility and benefits

### Supporting findings

| Finding | Reconciled evidence | Design consequence |
|---|---|---|
| Capacity is material but unvalidated | 617.72 estimated manual hours/month; four activities = 439.85 hours; High-criticality work = 315.48 hours | Preserve/replace controls; validate observed and removable time before funding 150 hours/month |
| Repair baselines disagree | Process file = 102.60 hours/month vs payment file = 55.78, an 84% gap | Reconcile scope before using a single baseline |
| Ten closures are unsupported | Four candidates; $7,800 estimated annual fees | Treat as controlled housekeeping, not a business-case pillar |
| Position coordination is persistent but small | Two negative accounts on 181/181 days; entity deficits on 45 days; maximum entity deficit $(0.24)m | Improve daily coordination without claiming avoidable borrowing cost |

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

### Evidence-to-decision gates

| Gate | Evidence due | Proposed accountable owner | Decision unlocked |
|---|---|---|---|
| **1 · Visibility** | Timestamp, cutoff, balance type, source, reconciliation, owner for 55 accounts | Group Treasurer | Pilot scope, architecture, 50/55 feasibility |
| **2 · Mobility** | Legal/local certification, buffers, funding events, facility use, interest and transfer costs | Group Treasurer | Validated liquidity range and funded value |
| **3 · Payment / capacity** | Source control, reason codes, criticality, release timestamps, observed time, removal/redeployment | Shared Services Lead | Targeted intervention and capacity case |

### Every option must survive the same tests

| Downside test | Stress | Current diagnostic position |
|---|---:|---|
| Liquidity | $21m | Survives every modeled complete window; still not validated mobility |
| Closures | 2 accounts | Four candidates evidenced; ten unsupported |
| Capacity | 50 hours/month | Screening baseline exists; removability unvalidated |
| Controls / service | Four consecutive weeks + four-hour rollback | Requirements proposed; owner approval pending |

### Week 3 direction

Develop and compare **local stabilization, federated coordination, and globally coordinated** options. The preferred option must create one enterprise data/control spine, preserve defined local autonomy, work around existing ERPs, avoid peak-season disruption, and keep unvalidated value outside the funded base.

**Decision requested:** Approve the option set, three evidence owners, and downside tests.

<details>
<summary>Speaker notes</summary>

Close the conclusion loop: act on the observable gaps, design liquidity without booking it, and constrain the value case. Record owners and deadlines at the checkpoint. Receivables and FX remain P1/data-gated; no external benchmark substitutes for missing ACG evidence.

[Sources]
- `deliverables/working/week_2/W2_findings_log.md`
- `deliverables/working/week_2/W2_diagnostic_report.md`
- `deliverables/working/week_2/W2_current_state_process_map_and_RACI.md`
[/Sources]

</details>
