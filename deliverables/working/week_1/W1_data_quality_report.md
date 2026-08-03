# Week 1 — Data Quality and Readiness Report

## Executive conclusion

The six supplied datasets are **technically fit for Week 2 diagnostic analysis with controls, but not sufficient by themselves for a final liquidity or benefits decision**. All 10 supplied tests and all 33 expanded Week 1 checks pass. Keys are unique, required relationships resolve, the six-month balance and FX panels are complete, required fields are populated, and payment currencies match their debit accounts.

The principal risk is semantic rather than structural. “Available” balances are estimates, restriction flags are preliminary, reporting lacks timestamps, fees and effort are estimates, and the data does not establish legal transferability, required operating buffers, or exception root causes. These gaps can materially change the recommended ambition and value case.

## Reconciliation baseline

| Dataset | Coverage/control total | Reconciliation result |
|---|---:|---|
| Entities | 16 entities; 13 countries; 3 regions; 3 ERPs; $3.9bn revenue control total | Unique IDs; no missing fields; does not reconcile to the client brief's $3.8bn FY2025 revenue |
| Accounts | 55 accounts; 51 active; 4 dormant; 5 banks; 10 currencies | Unique account IDs; all entities resolve |
| Balances | 9,955 observations; 55 accounts × 181 days; 1 Jan–30 Jun 2026 | 100% row completeness; unique account/date; all account and FX joins resolve |
| FX | 1,810 observations; 10 currencies × 181 days | 100% panel completeness; unique currency/date |
| Payments | 7,600 payments; $198.14m translated value; $62,613 estimated fees | Unique payment IDs; all accounts and FX resolve; currency matches account |
| Process activity | 9 activities; 617.72 estimated manual hours/month | Structurally complete; inputs are management estimates |

**Point-in-time balance control (30 Jun. 2026):** $59.80m ledger closing balance and $55.66m estimated available balance. Neither figure proves legal or operational transferability.

## Quality tests

All expanded checks passed: primary keys; composite balance/FX keys; account/entity relationships; balance/payment account relationships; balance/payment FX joins; account/payment currency consistency; complete balance and FX panels; nonnegative reporting delay and repair minutes; positive-closing available balances not exceeding closing balances; zero repair minutes for nonexceptions; and required-field completeness.

The loader was corrected to preserve the valid sweep category `None`; pandas had initially interpreted this category as null. Raw data was not changed.

## Timeliness and source quality

| Measure | Result | Interpretation |
|---|---:|---|
| Same-day balance observations | 5,792 / 9,955 (58.18%) | Date-level proxy; not equivalent to start-of-day availability |
| One-day delayed | 1,629 (16.36%) | Could make the group position stale |
| Two-or-more-day delayed | 2,534 (25.45%) | Material visibility limitation |
| Maximum delay | 3 days | Requires operational validation |
| Automated observations | 5,792 (58.18%) | Mapped from API/host-to-host in supplied data |
| Manually reported | 1,629 (16.36%) | Mapped from portal reporting |
| Estimated | 2,534 (25.45%) | Mapped from spreadsheets |

Same-day visibility varies by region: APAC 63.64%, NA 56.25%, and EMEA 52.94%. This partly corroborates the Treasurer's 60–70% estimate but is not a like-for-like comparison because no start-of-day timestamp is supplied.

## Preliminary payment/process signals—not final diagnostic findings

- 2,395 payments (31.51%) have manual touch.
- 479 (6.30%) have exceptions; 380 (5.00%) are late; 54 are rejected.
- Recorded repair totals 20,080 minutes. This is a capacity indicator, not headcount or cashable cost reduction.
- Process activity implies 617.72 manual hours/month, based on management estimates rather than observation.

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

## What can and cannot be answered confidently

**Can be answered now:** dataset population and integrity; account/entity/bank/currency footprint; historical date-level reporting delay; supplied source-quality mix; descriptive manual/exception/late rates; preliminary restricted/dormant populations; reproducible control totals.

**Cannot yet be answered confidently:** cash movable within 24 hours; accounts that can actually close; avoidable borrowing; cashable fee or labor savings; payment-exception root causes; legal feasibility of pooling; reconciled revenue by entity; target platform; or the preferred operating model.

## Week 2 analysis conditions

Proceed with transparent definitions, scenario ranges, and flags for unvalidated restrictions. Keep raw files unchanged, write all calculated outputs to `data/processed/`, reconcile every segmentation to the baselines above, and do not promote apparent liquidity or estimated effort into benefits without client validation.

## Reproducibility

Run:

```bash
python3 src/week1_data_quality.py
python3 tests/test_data_quality.py
```

Outputs: `W1_data_quality_metrics.csv`, `W1_data_quality_checks.csv`, `W1_missingness_profile.csv`, and `W1_visibility_by_region.csv` in `data/processed/`.
