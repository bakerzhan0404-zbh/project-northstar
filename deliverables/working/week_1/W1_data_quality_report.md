# Week 1 — Data Quality and Readiness Report

**Classification:** Confidential — `ACG-DATA` and `ANALYST-CALC`; limitations and treatments are `ANALYST-JUDGMENT`

## Executive conclusion

The six supplied datasets are **technically fit for Week 2 diagnostic analysis with controls, but not sufficient by themselves for a final liquidity or benefits decision**. All 10 supplied tests and all 52 expanded Week 1 checks pass. Keys are unique, required relationships resolve, the six-month balance and FX-rate panels are complete, required fields are populated, and payment currencies match their debit accounts.

The principal risk is semantic rather than structural. “Available” balances are estimates, restriction flags are preliminary, reporting lacks timestamps, fees and effort are estimates, and the data does not establish legal transferability, required operating buffers, or exception root causes. These gaps can materially change the recommended ambition and value case.

## Reconciliation baseline

| Dataset | Coverage/control total | Reconciliation result |
|---|---:|---|
| Entities | 16 entities; 13 countries; 3 regions; 3 ERPs; $3.9bn revenue control total | Unique IDs; no missing fields; does not reconcile to the client brief's $3.8bn FY2025 revenue |
| Accounts | 55 accounts; 51 active; 4 dormant; 5 banks; 10 currencies | Unique account IDs; all entities resolve |
| Balances | 9,955 observations; 55 accounts × 181 days; 1 Jan–30 Jun 2026 | 100% row completeness; unique account/date; all account and FX joins resolve |
| FX | 1,810 observations; 10 currencies × 181 days | 100% panel completeness; unique currency/date |
| Payments | 7,600 supplied records; $198.14m gross translated value across all statuses; $62,613 estimated fees | Unique IDs and valid joins; extract-to-source control and sampling method not supplied |
| Process activity | 9 supplied activities; 617.72 estimated manual hours/month | All supplied rows populated; expected activity universe is not defined and inputs are management estimates |

**Point-in-time balance control (30 Jun. 2026):** $59.80m net ledger closing balance. Estimated available positions comprise $57.80m gross positive balances and two negative accounts totaling $(2.14)m, producing $55.66m net estimated availability. None proves legal or operational transferability.

## Quality tests

All expanded checks passed, including: exact schemas and project date bounds; primary and composite keys; relationship and FX joins; panel completeness and continuity; required fields; categorical domains and boolean types; source-quality/visibility mapping; payment-status/exception/repair consistency; positive rates and amounts; nonnegative fees and process inputs; and valid reporting delays. These tests establish internal consistency—not source-system completeness or economic availability.

The loader was corrected to preserve the valid sweep category `None`; pandas had initially interpreted this category as null. Raw data was not changed.

## Timeliness and source quality

| Measure | Result | Interpretation |
|---|---:|---|
| Same-day accounts/account-days | 32 / 55 accounts; 5,792 / 9,955 account-days (58.18%) | Count-weighted date proxy; not percent of cash or start-of-day availability |
| Within-one-calendar-day sensitivity | 7,421 / 9,955 account-days (74.55%) | Alternative definition only; not proof of visibility within 24 hours |
| Same-day positive-balance value sensitivity | 55.14% of positive closing USD across the period | Value-weighted proxy; still not start-of-day visibility |
| One-day delayed | 1,629 (16.36%) | Could make the group position stale |
| Two-or-more-day delayed | 2,534 (25.45%) | Material visibility limitation |
| Maximum delay | 3 days | Requires operational validation |
| Automated observations | 5,792 (58.18%) | Mapped from API/host-to-host in supplied data |
| Manually reported | 1,629 (16.36%) | Mapped from portal reporting |
| Estimated | 2,534 (25.45%) | Mapped from spreadsheets |

Count-weighted same-day rates vary by region: APAC 63.64%, NA 56.25%, and EMEA 52.94%. These measures cannot corroborate the Treasurer's 60–70% estimate of cash visible at the start of day: the project metric repeats accounts across dates, the value-weighted sensitivity is 55.14%, and no intraday timestamp is supplied.

## Preliminary payment/process signals—not final diagnostic findings

- Of 7,600 supplied payment records, 2,395 (31.51%) have manual touch, 479 (6.30%) have exceptions, and 380 (5.00%) are late. Representativeness cannot be established without an extract control total and sampling method.
- The $198.14m gross translated control includes every status, including 54 rejected records worth $2.18m and 17 pending records worth $1.55m; it is not confirmed settled value.
- Recorded repair totals 20,080 minutes, or 55.78 hours/month across the six-month file. This is a capacity indicator, not headcount or cashable cost reduction.
- The process file separately estimates 180 exception-repair instances and 102.60 manual hours/month, versus 79.83 exceptions and 55.78 repair hours/month implied by the payment file. The 84% hours difference requires a scope and period reconciliation.
- All nine supplied process rows imply 617.72 manual hours/month, based on management estimates rather than observation.

These signals justify Week 2 segmentation but do not establish root cause because reason codes, beneficiary/invoice completeness, approval timestamps, and payment criticality are absent.

## Data-quality issue and treatment log

| ID | Issue | Decision impact | Proposed treatment | Validation owner | Severity |
|---|---|---|---|---|---|
| DQ-01 | Reporting dates lack timestamps and cutoff definitions | Cannot prove start-of-day or within-24-hour visibility | Obtain receipt timestamps and actual report-run logs; agree KPI definition | Group Treasury / IT | High |
| DQ-02 | `available_balance_local` is estimated | May overstate mobilizable cash | Reconcile to bank definitions; distinguish ledger, available, restricted, and required buffers | Treasury / Controllers | High |
| DQ-03 | Restriction flags are preliminary | Could reverse liquidity opportunity | Legal/tax/regulatory review by entity/account; document approval | Legal / Tax / Local Finance | High |
| DQ-04 | No operating-buffer or settlement-calendar data | Positive cash may be operationally required | Define buffer methodology and test sensitivity | Treasury / Regional Finance | High |
| DQ-05 | Payment exceptions lack root-cause fields | Cannot target the correct intervention | Obtain exception codes, beneficiary/invoice fields, and repaired-payment samples | Shared Services / AP | High |
| DQ-06 | Fees are estimates, not invoices | P&L benefit cannot be booked | Reconcile 12 months of bank invoices and internal cost allocation | Treasury / Finance | Medium |
| DQ-07 | Process time and manual percentages are estimates | Capacity benefit may be overstated | Time sample and validate volumes; protect control-critical effort | Process owners / Audit | Medium |
| DQ-08 | Only six months of history are supplied | Seasonality and peak behavior may be missed | Obtain at least 12–24 months or explicitly constrain conclusions | Data owner | Medium |
| DQ-09 | No borrowing rates, facility usage, or transfer costs | Cannot quantify avoidable external funding | Obtain facility statements, interest, FX, tax, and transfer cost data | Treasurer / FP&A | High |
| DQ-10 | No account dependency/signatory/closure-cost data | Dormant does not equal closable | Perform local account certification and closure checklist | Regional Controllers | High |
| DQ-11 | Entity revenue sums to $3.9bn versus $3.8bn in the client brief | Entity-level sizing and denominator-based metrics could be misstated | Reconcile scope, period, eliminations, and rounding with Group Finance | Group Finance | Medium |
| DQ-12 | No AR ledger, receipt, remittance, match-status, reason, or aging data | Receivables reconciliation cannot be diagnosed | Obtain reconciled receivables extracts and source-system controls | Group Finance / AR owner | High |
| DQ-13 | FX file contains rates only; no trades, exposures, hedges, spreads/fees, or settlements | FX transaction patterns, costs, and risks cannot be diagnosed | Obtain FX transaction/exposure extracts and policy context | Group Treasury / Finance | High |
| DQ-14 | Payment extract control total and sampling method are absent | Rates may not represent ACG's full payment population | Reconcile record/value totals to source and document extract logic | Shared Services / Data owner | High |
| DQ-15 | Payment file implies 79.83 exceptions and 55.78 repair hours/month versus process estimates of 180 and 102.60 | Process capacity and root-cause baselines may use different scope or periods | Reconcile definitions, populations, periods, and manual-percentage treatment | Shared Services / Process owner | High |

## What can and cannot be answered confidently

**Can be answered now:** supplied-dataset population and internal integrity; account/entity/bank/currency footprint; historical date-level reporting delay; supplied source-quality mix; descriptive rates within the 7,600-record payment file; preliminary restricted/dormant populations; reproducible control totals.

**Cannot yet be answered confidently:** cash movable within 24 hours; accounts that can actually close; avoidable borrowing; cashable fee or labor savings; payment-exception root causes or population rates; receivables-reconciliation performance; FX transaction/exposure patterns; legal feasibility of pooling; reconciled revenue by entity; target platform; or the preferred operating model.

## Week 2 analysis conditions

Proceed with transparent definitions, alternative metric sensitivities, scenario ranges, and flags for unvalidated restrictions. Keep raw files unchanged, write all calculated outputs to `data/processed/`, reconcile every segmentation to the baselines above, and do not promote apparent liquidity, sample rates, or estimated effort into benefits without client validation. Treat receivables and FX as explicit evidence gaps until the requested extracts arrive.

## Reproducibility

Run:

```bash
python3 src/week1_data_quality.py
python3 tests/test_data_quality.py
```

Outputs: `W1_data_quality_metrics.csv`, `W1_data_quality_checks.csv`, `W1_missingness_profile.csv`, and `W1_visibility_by_region.csv` in `data/processed/`.
