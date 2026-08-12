# Week 2 — Technical Appendix

**Prepared by:** Baker

**Status:** Reproducible analytical support for the current-state diagnostic

**Classification:** Confidential — Project Northstar simulated client material

## 1. Purpose and executive boundary

This appendix contains definitions, reconciliations, methods, sensitivities, detailed cuts, and unpromoted observations supporting the [Week 2 diagnostic report](W2_diagnostic_report.md). It does not expand the five-finding executive story. A result remains here when it is technically useful but does not change the Week 3 value, risk, feasibility, sequencing, or evidence decision.

The governing definitions and evidence labels are in the [Week 2 metric contract](W2_metric_contract.md). The transformation record is in the [analysis log](W2_analysis_log.md).

## 2. Reconciliation and test status

| Control | Reproduced result | Status | Decision boundary |
|---|---:|---|---|
| Entities | 16 | Pass | Supplied entity revenue totals $3.9bn vs $3.8bn in client brief |
| Accounts | 55 | Pass | $110,100 fees are estimated; restrictions preliminary |
| Account-day balances | 9,955 = 55 × 181 | Pass | Date-level reporting only |
| Supplied payments | 7,600 unique records | Pass | Source-population completeness and sampling unknown |
| Gross translated supplied-record value | $198,135,489.50 | Pass | Includes all statuses; not settled value or enterprise volume |
| Payment repair | 20,080 minutes | Pass | Management-estimated effort in supplied extract |
| FX panel | 1,810 = 10 × 181 | Pass | Project translation rates only |
| Process activities | 9 | Pass | Management estimates; population undefined |
| Estimated process capacity | 617.72 hours/month | Pass | Not observed time, headcount, or savings |
| Week 2 assertions | 69/69 | Pass | Tests arithmetic, joins, definitions, and selected outputs |
| Supplied data-quality tests | 10/10 | Pass | Tests structural properties only |
| Week 1 expanded controls | 52/52 | Pass | Structural/logic controls; not semantic source certification |

## 3. Account-screen method

### Primary rule

```text
closure_validation_candidate =
    status = Dormant
    AND purpose = Legacy
    AND supplied_payment_records = 0
```

All 55 accounts remain in the diagnostic. Protection/validation flags cover payroll, tax, collection, active operating purpose, preliminary restrictions, and sweep dependencies. The four candidates are `AC0004`, `AC0009`, `AC0024`, and `AC0037`, with $7,800 of gross estimated annual fees.

### Unsafe interpretations avoided

- Zero debit records is not proof of zero receipts, direct debits, or linked services.
- A multi-bank or multi-account relationship is not automatically redundant.
- An estimated fee is not removable P&L until closure and fee termination are certified.
- A candidate is not an approved closure.

Detailed output: `data/processed/W2_account_diagnostic.csv`.

## 4. Visibility method

```text
reporting_delay_days = reported_to_group_date - balance_date
same_day = reporting_delay_days = 0
within_one_day = reporting_delay_days <= 1
positive_value_weighted_same_day =
    same-day positive estimated available USD
    / all positive estimated available USD
```

### Delay reconciliation

| Delay | Account-days | Share |
|---|---:|---:|
| Same calendar day | 5,792 | 58.18% |
| One calendar day | 1,629 | 16.36% |
| Two or three calendar days | 2,534 | 25.45% |
| **Total** | **9,955** | **100.00%** |

All API/host-to-host observations are same-day, all portal observations are one day late, and all spreadsheet observations are two to three days late. This is a source association in the supplied panel—not timestamped proof of start-of-day performance or a quantified decision consequence.

Detailed output: `data/processed/W2_visibility_diagnostic.csv`.

## 5. Liquidity ladder and rolling-buffer method

### Daily layers

```text
gross_positive_available[d] = Σ max(available_usd[a,d], 0)
gross_negative_available[d] = Σ min(available_usd[a,d], 0)
net_available[d] = gross_positive_available + gross_negative_available
unflagged_positive[a,d] =
    max(available_usd[a,d], 0) when restricted_flag = False; otherwise 0
```

### Rolling buffer and scenario

For each account `a`, date `d`, and window `N` of seven or 14 calendar days:

```text
buffer[a,d,N] = Σ gross supplied payment USD[a,t]
                where d-N+1 <= t <= d

scenario_surplus[a,d,N] = max(unflagged_positive[a,d] - buffer[a,d,N], 0)

gross_scenario_surplus[d,N] = Σ scenario_surplus[a,d,N]

netting_sensitivity[d,N] =
    gross_scenario_surplus[d,N] + gross_negative_available[d]
```

The first six seven-day rows and first 13 fourteen-day rows remain null because they lack complete windows. Seven days provides a short-horizon payment-intent reference; 14 days extends the stability test across two weeks. Neither is an approved operating-buffer policy or cash forecast. The primary screen conservatively includes all supplied statuses; Completed/Repaired-only treatment is shown as a status sensitivity and changes the 30 June 14-day gross result by only $0.02m.

The screen does not separately model or validate complete payroll, tax, seasonal or peak expenditure, receipts, settlement-calendar effects, forecast error, or extraordinary funding events. Payroll and tax records exist in the extract, but completeness is not certified. Every output remains a screening result—not surplus cash or transfer authorization.

### Rolling threshold results

| Buffer | Complete days | Minimum net | Median net | $21m days met | $35m days met | $46.2m days met |
|---|---:|---:|---:|---:|---:|---:|
| Seven days | 175 | $37.90m | $41.95m | 175 | 175 | 0 |
| 14 days | 168 | $31.28m | $36.67m | 168 | 138 | 0 |

Every value is an `ANALYST-CALC / ANALYST-ASSUMPTION` scenario. None is transferable or movable cash.

Detailed outputs: `W2_liquidity_daily.csv`, `W2_liquidity_account_scenarios.csv`, `W2_liquidity_scenarios.csv`, and `W2_liquidity_thresholds.csv`.

## 6. Simultaneous-position method

Account signs are evaluated daily. Entity net equals the daily sum of its account estimated availability. Entity totals reconcile to the daily group total.

| Observation | Result | Safe interpretation |
|---|---:|---|
| Dates with positive and negative accounts | 181/181 | Coordination opportunity; not avoidable borrowing |
| Negative accounts each day | 2 | Persistent mismatch to investigate |
| Persistent deficit accounts | `AC0025`, `AC0034` | Active operating, spreadsheet/estimated sources; no facility evidence |
| Dates with at least one negative-net entity | 45/181 | Entity-level mismatch is intermittent |
| Largest entity net deficit | $(0.24)m | Small relative to group positive estimates; no interest conclusion |

Detailed outputs: `W2_simultaneous_positions_daily.csv`, `W2_entity_positions.csv`, and `W2_account_positions.csv`.

## 7. Payment diagnostic method

All metrics are limited to the 7,600 supplied records.

```text
amount_usd = amount_local × supplied usd_per_unit on payment date
cohort rate = cohort flagged records / cohort records
exception contribution = cohort exceptions / 479
late contribution = cohort late releases / 380
repair contribution = cohort repair minutes / 20,080
fee contribution = cohort estimated fees / $62,613
```

Wire geography compares cross-border wires with domestic wires—not cross-border wires with every domestic payment. USD amount bands are `≤$10k`, `>$10k–$25k`, `>$25k–$50k`, `>$50k–$100k`, and `>$100k`.

### Mutually exclusive priority cohorts

| Cohort | Records | Exceptions | Exception rate | Repair minutes | Gross supplied-record amount |
|---|---:|---:|---:|---:|---:|
| Manual touch only | 2,053 | 246 | 11.98% | 10,018 | $51,983,738.28 |
| Manual touch + cross-border wire | 342 | 58 | 16.96% | 2,702 | $6,846,691.83 |
| Cross-border wire only | 444 | 52 | 11.71% | 2,219 | $7,875,503.53 |
| Neither priority cohort | 4,761 | 123 | 2.58% | 5,141 | $131,429,555.87 |

The overlap is 14.28% of manual-touch records and 43.51% of cross-border wires. The deduplicated priority union contains 2,839 records, 356 exceptions, 14,939 repair minutes, and $66,705,933.64 of gross supplied-record amount; it contributes 74.32% of all exceptions and 74.40% of all repair minutes. Gross amount includes all statuses and is payment intent, not confirmed settlement or cash outflow.

### Counterevidence retained

- 2,091/2,395 manual-touch records (87.31%) have no exception.
- 676/786 cross-border wires (86.01%) have no exception.
- ERP and region cuts do not identify a single platform or geography as the problem.
- Balance `visibility_method` is not a payment initiation/transmission field.
- `cross_border_flag` is not an FX transaction or exposure.
- Payment `status` does not prove settlement or service consequence.

Detailed output: `data/processed/W2_payment_diagnostic.csv`.

## 8. Process-capacity method and source mismatch

```text
manual_hours_monthly =
    frequency_per_month × minutes_per_instance × manual_percentage / 100 / 60

loaded_capacity_equivalent =
    manual_hours_monthly × illustrative loaded hourly cost
```

| Baseline | Volume/month | Repair hours/month | Boundary |
|---|---:|---:|---|
| Payment-file six-month average | 79.83 exception records | 55.78 | Supplied extract only |
| Process-file management estimate | 180 exception-repair instances | 102.60 | Undefined activity population |
| Difference | 100.17 | 46.82 | Do not combine until scope reconciles |

Four activities contribute 439.85 hours/month, or 71.2% of the process screen. Six High-criticality activities contribute 315.48 hours/month. Criticality requires control preservation; it does not require preserving the current manual method.

Detailed outputs: `W2_process_capacity.csv` and `W2_repair_baseline_reconciliation.csv`.

## 9. Unpromoted observations

| Observation | Why it remains in appendix |
|---|---|
| Monthly payment exception rates range from 4.84% to 7.13% | Six months does not establish seasonality or a sustained trend |
| SAP-S4 supplies 50% of records but has a below-baseline exception rate | Does not support an ERP-first explanation |
| Regional exception rates range from 5.55% to 6.98% | No region is uniquely responsible |
| `≤$10k` records contribute most volume/workload, while `>$100k` records carry much of value | Useful design distinction, but it does not change the two promoted payment cohorts |
| Cross-border wires contribute 57.24% of estimated fees | Fee values are mechanically associated with payment type/status and are not validated pricing |
| Persistent account deficits coexist with much larger positives | No facility use, rate, timing, or legal-mobility evidence supports an interest benefit |
| Four closure candidates carry only $7,800 of estimated fees | Supports housekeeping, not a strategic business case |
| Receivables and FX performance remain unassessed | No controlled receivables records or executed FX trade/exposure data supplied |

## 10. Reproducible output register

| Output | Grain | Purpose |
|---|---|---|
| `W2_reconciliation_metrics.csv` | Metric | Week 2 control totals |
| `W2_account_diagnostic.csv` | Account | Footprint, activity, candidate, and protection screen |
| `W2_visibility_diagnostic.csv` | Dimension/category | Date-level and positive-value-weighted reporting profile |
| `W2_liquidity_daily.csv` | Date | Liquidity layers and rolling scenarios |
| `W2_liquidity_account_scenarios.csv` | Account on 30 June | Account-level buffer sensitivity |
| `W2_liquidity_scenarios.csv` | Liquidity layer | 30 June interpretation ladder |
| `W2_liquidity_thresholds.csv` | Window/threshold | Complete-window stability tests |
| `W2_simultaneous_positions_daily.csv` | Date | Concurrent account/entity positions |
| `W2_entity_positions.csv` | Entity/date | Entity net and within-entity mismatch |
| `W2_account_positions.csv` | Account | Persistent deficit screen |
| `W2_payment_diagnostic.csv` | Dimension/category | Cohort rates and absolute contributions |
| `W2_process_capacity.csv` | Process activity | Manual-capacity and control screen |
| `W2_repair_baseline_reconciliation.csv` | Metric | Payment/process source mismatch |

All files are under `data/processed/` and are generated by `src/week2_diagnostic.py`.

## 11. Reproduce and test

From the repository root:

```bash
python3 src/generate_data.py
python3 src/starter_analysis.py
python3 src/week1_data_quality.py
python3 src/week2_diagnostic.py
python3 tests/test_data_quality.py
python3 tests/test_week2_diagnostic.py
```

Raw files under `data/raw/` must remain unchanged. Generated Week 2 numbers must not be manually overwritten in the report or checkpoint deck.
