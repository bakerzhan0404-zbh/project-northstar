# Week 2 — Analysis Log

**Prepared by:** Baker

**Working period:** 10–16 August 2026

**Status:** In progress

**Classification:** Confidential — Project Northstar simulated client material

## Reconciliation baseline carried from Week 1

| Dataset | Rows | Period | Control total | Week 2 use |
|---|---:|---|---:|---|
| Entities | 16 | FY2025 attributes | $3,900m supplied revenue | Entity and regional segmentation |
| Accounts | 55 | Opened 2010–2024 | $110,100 estimated fees/year | Footprint, protection, and candidate screen |
| Balances | 9,955 | 1 Jan–30 Jun 2026 | 55 accounts × 181 days | Visibility and liquidity diagnosis |
| Payments | 7,600 | 1 Jan–30 Jun 2026 | $198.14m gross supplied-record value | Extract-bounded payment friction diagnosis |
| FX rates | 1,810 | 1 Jan–30 Jun 2026 | 10 currencies × 181 days | USD translation only |
| Process activity | 9 | Monthly estimates | 617.72 manual hours/month | Capacity and control screen |

## Analytical work modules

| ID | Module | Decision question | Status | Reproducible outputs |
|---|---|---|---|---|
| A06 | Week 2 analytical contract and baseline | Do all later modules use one controlled population and definition set? | Complete | `W2_metric_contract.md`; `W2_reconciliation_metrics.csv` |
| A07 | Account rationalization screen | Which accounts merit local closure validation without weakening required services or controls? | Complete | `W2_account_diagnostic.csv` |
| A08 | Cash visibility diagnostic | Where is cash reporting insufficiently timely for Group Treasury decisions? | Complete | `W2_visibility_diagnostic.csv` |
| A09 | Liquidity and buffer scenarios | What is observed, apparently available, buffer-dependent, or still unvalidated? | Complete | `W2_liquidity_daily.csv`; `W2_liquidity_account_scenarios.csv`; `W2_liquidity_scenarios.csv`; `W2_liquidity_thresholds.csv` |
| A10 | Simultaneous surplus/deficit | How often do positive and negative positions coexist? | Complete | `W2_simultaneous_positions_daily.csv`; `W2_entity_positions.csv`; `W2_account_positions.csv` |
| A11 | Payment friction profile | Which supplied-record cohorts drive manual work, exceptions, delay, and repair? | Complete | `W2_payment_diagnostic.csv` |
| A12 | Process capacity and controls | Which estimated manual activities are material and which controls must be preserved? | Complete | `W2_process_capacity.csv`; `W2_repair_baseline_reconciliation.csv` |
| A13 | Targeted operating-model feasibility | Which ownership, handoff, data, and control gaps affect Wave 1 feasibility? | Complete | `W2_current_state_process_map_and_RACI.md`; `W2_maturity_heatmap.md` |
| A14 | Executive diagnostic synthesis | Which four to six findings materially change the Week 3 decision? | Complete | `W2_findings_log.md`; `W2_diagnostic_report.md`; `W2_checkpoint_deck.md` |

## A06 — Week 2 analytical contract and baseline

- **Decision question:** Can the diagnostic be built without changing definitions between analysis, report, and deck?
- **Owner/date:** Baker / 10 August 2026
- **Inputs:** Six supplied raw CSV files and the Week 1 processed controls.
- **Population:** All supplied records; domain-specific exclusions must be declared in the relevant module.
- **Definitions:** See `W2_metric_contract.md`.
- **Evidence boundary:** Date-level visibility is not start-of-day visibility; estimated availability is not movable cash; the payment file is not a certified ACG-wide population; process hours are capacity estimates.
- **Reconciliation result:** 16 entities, 55 accounts, 9,955 account-days, 7,600 supplied payment records, $198.14m gross translated supplied-record value, 20,080 repair minutes, and 617.72 estimated manual process hours/month all reproduce.
- **Code and test:** `src/week2_diagnostic.py`; `tests/test_week2_diagnostic.py`.
- **Output:** `data/processed/W2_reconciliation_metrics.csv`.
- **Executive use:** Only findings meeting the six-part promotion rule enter the main report.
- **Status:** Complete. All four Week 2 baseline assertions and all ten supplied data-quality tests pass.

## A07 — Account rationalization screen

- **Decision question:** Which accounts should enter local closure validation, and what prevents a closure conclusion today?
- **Owner/date:** Baker / 10 August 2026
- **Inputs:** `bank_accounts.csv`, `entity_master.csv`, `daily_balances.csv`, `payments.csv`, and `fx_rates.csv`.
- **Population and exclusions:** All 55 accounts; no accounts excluded. Payment activity is limited to the supplied six-month extract.
- **Definition:** Primary candidate = dormant status + legacy purpose + zero supplied payment records. This narrow rule is defined before interpretation.
- **Protection screen:** Payroll, tax, collection, active operating, preliminary restriction, and sweep dependencies are flagged. Every candidate still requires local purpose, legal/tax, signatory, collection, service-continuity, closure-cost, and fee-removal validation.
- **Reconciliation:** The output contains 55 unique accounts. Four candidates have zero supplied payment records and $7,800 of gross estimated annual fees.
- **Result:** The supplied evidence supports four closure-validation candidates, not the management stretch of ten closures and not any approved closure.
- **Counterevidence:** The six-month payment extract may omit activity, and the four candidates retain small positive estimated balances; local dependencies are not supplied.
- **Code and test:** `build_account_diagnostic()` in `src/week2_diagnostic.py`; five domain assertions in `tests/test_week2_diagnostic.py`.
- **Output:** `data/processed/W2_account_diagnostic.csv`.
- **Finding implication:** Account rationalization can support Wave 1, but it does not provide a material standalone business case on current evidence.

## A08 — Cash visibility diagnostic

- **Decision question:** Where does Group Treasury lack a timely view of supplied cash balances, and which source methods drive the gap?
- **Owner/date:** Baker / 11 August 2026
- **Inputs:** Enriched `daily_balances.csv` joined to account, entity, and daily project FX attributes.
- **Population and exclusions:** All 9,955 account-days across 55 accounts and 181 calendar days; no exclusions.
- **Definitions:** Same-day means reporting date equals balance date. Within one day includes zero- and one-calendar-day delay. Positive-value weighting uses positive estimated available USD. None of these definitions proves start-of-day or elapsed-24-hour visibility.
- **Reconciliation:** Overall and regional/source/month cuts each reconcile to the applicable account-day population. The overall view contains 5,792 same-day observations (32 accounts × 181 days), 1,629 one-day observations, and 2,534 observations delayed at least two days.
- **Result:** Same-day coverage is 58.18% of account-days; the within-one-calendar-day sensitivity is 74.55%. All 12 API and 20 host-to-host accounts are same-day, all nine portal accounts are one day late, and all 14 spreadsheet accounts are at least two days late.
- **Implication:** The gap is structurally concentrated in portal/spreadsheet reporting, so a targeted connectivity and data-ownership intervention can be tested without assuming an ERP replacement.
- **Counterevidence:** Source method and delay move together in the supplied synthetic panel, but timestamps, receipt cutoffs, balance definitions, and funding-decision consequences are absent. The data does not prove a greater-than-$5m cost or decision consequence.
- **Code and test:** `build_visibility_diagnostic()` in `src/week2_diagnostic.py`; six visibility assertions in `tests/test_week2_diagnostic.py`.
- **Output:** `data/processed/W2_visibility_diagnostic.csv`.
- **Finding implication:** Visibility earns promotion as a current-state finding; its value case remains dependent on mobility and funding evidence.

## A09 — Liquidity and operating-buffer scenarios

- **Decision question:** What is observed, estimated, preliminarily unflagged, buffer-dependent, or genuinely validated for movement?
- **Owner/date:** Baker / 12 August 2026
- **Inputs:** All 9,955 enriched account-day balances and the 7,600 supplied payment records.
- **Population and exclusions:** Daily balance layers use the full six-month panel. The account scenario uses all 55 accounts on 30 June 2026. Preliminary restricted accounts remain visible but receive zero scenario surplus. No account is described as legally or operationally transferable.
- **Definitions:** Gross positive estimated availability floors negative account positions at zero. The seven-day window is a short-horizon payment-intent reference; the 14-day window extends the stability test across two weeks. Both conservatively use all supplied-record value by account in the trailing calendar window; Completed/Repaired-only value is shown as a status sensitivity. Gross scenario surplus equals positive estimated availability less that buffer, floored at zero, and then excludes preliminarily restricted accounts. Net scenario surplus also includes negative account positions.
- **Reconciliation:** On 30 June, $57.80m gross positive estimated availability less $(2.14)m negative positions equals $55.66m net estimated availability. Preliminary restriction flags cover $8.05m; $49.75m is preliminarily unflagged.
- **Sensitivity result:** On 30 June, the seven-day screening result is $44.98m gross and $42.84m net; the 14-day screening result is $40.27m gross and $38.13m net. Across complete windows, the $35m base threshold survives 175/175 seven-day observations and 138/168 14-day observations. The $21m stress survives all complete windows; the $46.2m upside survives none after netting. Excluding Rejected/Pending records raises the latest 14-day gross result by only $0.02m.
- **Counterevidence:** The screen does not separately model or validate complete payroll, tax, seasonal or peak expenditure, receipts, settlement-calendar effects, forecast error, or extraordinary funding events. The extract contains payroll and tax records, but population completeness is not certified. Completed/Repaired status is not settlement proof.
- **Code and test:** `build_liquidity_scenarios()` in `src/week2_diagnostic.py`; 13 liquidity assertions in `tests/test_week2_diagnostic.py`.
- **Outputs:** `data/processed/W2_liquidity_daily.csv`, `W2_liquidity_account_scenarios.csv`, `W2_liquidity_scenarios.csv`, and `W2_liquidity_thresholds.csv`.
- **Finding implication:** The screen supports continued liquidity option design, but the Week 3 business case must show zero validated movable cash until account-level transferability and operating-buffer evidence is supplied.

## A10 — Simultaneous positive and negative positions

- **Decision question:** Do positive and negative estimated positions coexist often enough to justify a coordinated cash-positioning intervention?
- **Owner/date:** Baker / 12 August 2026
- **Inputs:** All 9,955 enriched account-day balance observations.
- **Population and exclusions:** All 55 accounts and 16 entities across all 181 dates; no exclusions.
- **Definitions:** An account deficit is estimated available USD below zero. Entity net equals the sum of its accounts on a date. Simultaneous account positions require at least one positive and one negative account; simultaneous entity positions require at least one positive-net and one negative-net entity.
- **Reconciliation:** Positive, zero, and negative account counts sum to 55 each day. Entity net positions reconcile to group net estimated availability each day.
- **Result:** Positive and negative account positions coexist on 181/181 dates, with exactly two negative accounts every day. `AC0025` (E007) and `AC0034` (E010) are active operating accounts with 181-day negative runs. At entity level, at least one net deficit occurs on 45/181 days: E007 on 37 days and E010 on 14 days, including six overlapping dates.
- **Implication:** Persistent account-level mismatches support daily position coordination and targeted funding-policy validation; they do not establish a large cash-release or interest-saving case.
- **Counterevidence:** The maximum entity net deficit is small relative to group positive estimates, and the supplied data contains no facility usage, interest rate, transfer timing, legal mobility, or internal-funding evidence.
- **Code and test:** `build_simultaneous_position_diagnostic()` in `src/week2_diagnostic.py`; nine position assertions in `tests/test_week2_diagnostic.py`.
- **Outputs:** `data/processed/W2_simultaneous_positions_daily.csv`, `W2_entity_positions.csv`, and `W2_account_positions.csv`.
- **Finding implication:** Promote as supporting evidence for operating-model coordination, not as a quantified financial benefit.

## A11 — Payment friction profile

- **Decision question:** Within the supplied extract, which cohorts concentrate manual activity, exceptions, late release, repair effort, and estimated fees?
- **Owner/date:** Baker / 13 August 2026
- **Inputs:** All 7,600 enriched payment records joined to account, entity, and daily project FX attributes.
- **Population and exclusions:** No supplied records excluded. Gross value includes all statuses. All results are extract-bounded; wire geography compares only the 1,398 wire records.
- **Definitions:** Cohort rates use cohort record counts. Contribution shares use 479 total exceptions, 380 late releases, 20,080 repair minutes, or $62,613 estimated fees. Four mutually exclusive priority cohorts remove double counting: manual-touch only, manual-touch + cross-border wire, cross-border-wire only, and neither. Gross supplied-record amount is all-status translated payment intent, not settlement or cash outflow. USD amount bands prevent mixed-currency comparisons.
- **Reconciliation:** 7,600 records, $198.14m gross supplied-record value, 2,395 manual touches, 479 exceptions, 380 late releases, 54 rejected, 17 pending, 20,080 repair minutes, and $62,613 estimated fees reproduce.
- **Result:** Manual touch and cross-border wire overlap on 342 records—14.28% of manual-touch records and 43.51% of cross-border wires. The overlap contains 58 exceptions, 2,702 repair minutes, and $6.85m of gross supplied-record amount. The deduplicated priority union contains 2,839 records, 356 exceptions, 14,939 repair minutes, and $66.71m; it contributes 74.32% of all exceptions and 74.40% of repair minutes. Manual-touch only is the largest absolute workload (246 exceptions; 10,018 minutes), while the overlap has the highest exception rate (16.96%).
- **Implication:** Week 3 options should prioritize targeted payment-intake, cutoff, format, and control interventions for manual-touch and cross-border-wire cohorts rather than assume uniform automation value.
- **Counterevidence:** 87.31% of manual-touch records and 86.01% of cross-border wires have no exception. The data lacks event sequence, reason code, beneficiary/corridor, criticality, and approval/release timestamps, so it cannot prove manual work or cross-border status caused the friction.
- **Code and test:** `build_payment_diagnostic()` in `src/week2_diagnostic.py`; 23 payment assertions in `tests/test_week2_diagnostic.py`.
- **Output:** `data/processed/W2_payment_diagnostic.csv`.
- **Finding implication:** Promote one extract-bounded payment finding; keep causal and ACG-wide benefit claims gated.

## A12 — Process capacity and control screen

- **Decision question:** Which estimated manual activities are material enough to shape intervention design, and what prevents them from becoming a funded benefit?
- **Owner/date:** Baker / 13 August 2026
- **Inputs:** All nine rows in `process_activity.csv` and the supplied payment-file repair fields.
- **Population and exclusions:** No process activities or payment exceptions excluded. The sources remain separate because there is no process-to-payment key or common population definition.
- **Definitions:** Manual hours/month = frequency × minutes per instance × manual percentage / 100 / 60. Loaded capacity is hours × illustrative loaded rate. Neither is observed time, removable work, headcount, or P&L savings.
- **Reconciliation:** The process file yields 617.72 estimated manual hours/month and $426,618.90 loaded capacity equivalent/year. Six High-criticality activities contribute 315.48 hours/month.
- **Result:** Receipt reconciliation, payment exception repair, cash forecast preparation, and payment file preparation contribute 439.85 hours/month (71.2% of the screening baseline). The process file implies 102.60 repair hours/month, 84% above the 55.78-hour payment-file estimate. The 150-hour target equals 24.28% of the screening baseline; the 50-hour stress equals 8.09%.
- **Implication:** Process simplification should focus on four material activities, but controls must be preserved and Week 3 cannot fund a 150-hour benefit until scope, observed time, removal rate, and redeployment are validated.
- **Counterevidence:** High criticality does not require the current manual method, while manual percentage does not prove waste. The repair mismatch may reflect broader scope or multiple process instances per payment.
- **Code and test:** `calculate_process_capacity()` and `build_repair_baseline_reconciliation()` in `src/week2_diagnostic.py`; eight capacity/reconciliation assertions in `tests/test_week2_diagnostic.py`.
- **Outputs:** `data/processed/W2_process_capacity.csv` and `W2_repair_baseline_reconciliation.csv`.
- **Finding implication:** Use capacity as a supporting feasibility finding and evidence gate, not a booked benefit.

## A13 — Targeted operating-model feasibility

- **Decision question:** Which handoffs, ownership gaps, data conditions, and controls determine whether ACG can deliver the promoted interventions safely?
- **Owner/date:** Baker / 14 August 2026
- **Inputs:** A07–A12 results, client brief, stakeholder evidence, and nine process-activity estimates.
- **Method:** Map only the cash and payment handoffs needed to explain or implement the promoted findings; draft responsibility at the relevant validation and control decisions; score maturity only against observable 1–5 criteria.
- **Result:** Data ownership, global/local decision rights, process standards, controls, and performance evidence are all emerging constraints. Connectivity can be staged around existing ERPs only if those capabilities move together.
- **Boundary:** Maps are analytical, not observed BPMN. Maturity scores are provisional, non-aggregated, and not external benchmarks. Internal Audit is consulted; management owns controls.
- **Outputs:** `W2_current_state_process_map_and_RACI.md` and `W2_maturity_heatmap.md`.

## A14 — Executive diagnostic synthesis

- **Decision question:** What must the Treasurer believe, decide, and request after Week 2?
- **Owner/date:** Baker / 15 August 2026
- **Promotion rule:** Material to Week 3; reconciled; fact–magnitude–implication–mechanism–action; evidence labels visible; counterevidence retained; named decision/evidence gate.
- **Result:** Five findings promoted. Three drive option design—visibility, liquidity evidence, and payment cohorts. Two constrain value/sequencing—capacity/control and account rationalization.
- **Executive conclusion:** Proceed to three-option design and two bounded pilot designs; carry $0 validated mobility and exclude unvalidated capacity/fee value from the funded base.
- **Consistency check:** The findings log, eight-page report, weekly update, and five-slide checkpoint use the same conclusion loop and three evidence requests.
- **Outputs:** `W2_findings_log.md`, `W2_diagnostic_report.md`, `W2_checkpoint_deck.md`, and `W2_weekly_update.md`.
