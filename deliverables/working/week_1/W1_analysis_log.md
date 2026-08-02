# Week 1 — Analysis Log

## Reconciliation baseline

| Dataset | File/version | Rows | Date range | Control total | Issues |
|---|---|---:|---|---:|---|
| Entities | `data/raw/entity_master.csv` / commit bcd0481 | 16 | FY2025 attributes | $3,900m revenue | Brief states $3.8bn; supplied entity sum is $3.9bn and requires reconciliation |
| Accounts | `data/raw/bank_accounts.csv` / commit bcd0481 | 55 | Open dates 2010–2024 | $110,100 estimated annual fees | Fees are estimates; restriction flags preliminary |
| Balances | `data/raw/daily_balances.csv` / commit bcd0481 | 9,955 | 2026-01-01–2026-06-30 | $59.80m closing on 30 Jun. | Availability and reporting are estimated/date-level |
| Payments | `data/raw/payments.csv` / commit bcd0481 | 7,600 | 2026-01-01–2026-06-30 | $198.14m translated value | Fees/repair time estimated; no reason codes |
| FX | `data/raw/fx_rates.csv` / commit bcd0481 | 1,810 | 2026-01-01–2026-06-30 | 10 currencies × 181 days | Project rates only |
| Process | `data/raw/process_activity.csv` / commit bcd0481 | 9 | Monthly estimates | 617.72 manual hours/month | Management estimates, not observed |

## A01 — Week 1 structural completeness and integrity audit

- **Decision question:** Is the supplied data structurally fit for diagnostic analysis?
- **Owner/date:** Baker / 2026-08-02
- **Input files and versions:** Six raw CSV files generated deterministically from seed `20260730`.
- **Population and exclusions:** All records; no exclusions.
- **Definitions:** Complete panel = every account/currency has one record for each of 181 calendar days. Required field = every supplied schema column.
- **Transformation steps:** Load with `keep_default_na=False`; parse dates; validate keys; join account/entity/FX; translate using date/currency project rates.
- **Reconciliation performed:** Row counts, unique keys, expected panels, relationship joins, currency consistency, missingness, control totals.
- **Quality tests:** 18/18 expanded checks and 10/10 supplied tests pass.
- **Assumptions:** The categorical sweep label `None` is valid, not null.
- **Sensitivity:** Not applicable to structural tests.
- **Output files:** `data/processed/W1_data_quality_*.csv`, `W1_missingness_profile.csv`, `W1_visibility_by_region.csv`.
- **Finding supported:** Data is technically fit for controlled diagnostic work.
- **Known limitations:** Structural completeness does not establish semantic accuracy or legal transferability.

## A02 — Reporting timeliness and source-quality profile

- **Decision question:** How much historical balance reporting is same-day under the supplied proxy?
- **Owner/date:** Baker / 2026-08-02
- **Inputs:** Balances joined to accounts and entities.
- **Definition:** Same-day = `reported_to_group_date - date = 0`; delay measured in calendar days.
- **Population/exclusions:** 9,955 observations; none excluded.
- **Result:** 58.18% same-day, 16.36% one-day delayed, 25.45% delayed two or more days; maximum three days. Regional same-day rates: APAC 63.64%, NA 56.25%, EMEA 52.94%.
- **Reconciliation:** Regional observations sum to 9,955; quality categories sum to total.
- **Sensitivity:** Start-of-day cannot be tested because timestamps are absent.
- **Finding supported:** A reliable daily view is not demonstrated.
- **Known limitations:** Same-day is not start-of-day; dates may mask intraday staleness.

## A03 — Preliminary payment/process profile

- **Decision question:** Is there sufficient evidence to prioritize a Week 2 payment diagnostic?
- **Result:** 31.51% manual touch, 6.30% exceptions, 5.00% late release, 54 rejected payments, 20,080 repair minutes, and 617.72 estimated manual process hours/month.
- **Reconciliation:** Counts reconcile to 7,600 payments; nonexceptions have zero repair minutes.
- **Finding supported:** Payment/process friction is material enough to investigate.
- **Known limitations:** No reason codes, criticality, timestamps, observed labor, or fully loaded realization assumptions.

