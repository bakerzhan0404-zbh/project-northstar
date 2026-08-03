# Week 1 — Analysis Log

## Reconciliation baseline

| Dataset | File/version | Rows | Date range | Control total | Issues |
|---|---|---:|---|---:|---|
| Entities | `data/raw/entity_master.csv` / commit bcd0481 | 16 | FY2025 attributes | $3,900m revenue | Brief states $3.8bn; supplied entity sum is $3.9bn and requires reconciliation |
| Accounts | `data/raw/bank_accounts.csv` / commit bcd0481 | 55 | Open dates 2010–2024 | $110,100 estimated annual fees | Fees are estimates; restriction flags preliminary |
| Balances | `data/raw/daily_balances.csv` / commit bcd0481 | 9,955 | 2026-01-01–2026-06-30 | $59.80m net closing on 30 Jun. | Net estimated available is $55.66m; gross positive is $57.80m; reporting is date-level |
| Payments | `data/raw/payments.csv` / commit bcd0481 | 7,600 | 2026-01-01–2026-06-30 | $198.14m gross supplied-record value | Includes rejected/pending; extract control, sampling method, fees, and repair scope unvalidated |
| FX | `data/raw/fx_rates.csv` / commit bcd0481 | 1,810 | 2026-01-01–2026-06-30 | 10 currencies × 181 days | Project rates only |
| Process | `data/raw/process_activity.csv` / commit bcd0481 | 9 supplied rows | Monthly estimates | 617.72 manual hours/month | Expected activity universe undefined; exception scope does not reconcile to payment file |

## A01 — Week 1 structural completeness and integrity audit

- **Decision question:** Is the supplied data structurally fit for diagnostic analysis?
- **Owner/date:** Baker / 2026-08-02
- **Input files and versions:** Six raw CSV files generated deterministically from seed `20260730`.
- **Population and exclusions:** All records; no exclusions.
- **Definitions:** Complete panel = every account/currency has one record for each of 181 calendar days. Required field = every supplied schema column.
- **Transformation steps:** Load with `keep_default_na=False`; parse dates; validate keys; join account/entity/FX; translate using date/currency project rates.
- **Reconciliation performed:** Row counts, unique keys, expected panels, relationship joins, currency consistency, missingness, control totals.
- **Quality tests:** 52/52 expanded checks and 10/10 supplied tests pass.
- **Assumptions:** The categorical sweep label `None` is valid, not null.
- **Sensitivity:** Not applicable to structural tests.
- **Output files:** `data/processed/W1_data_quality_*.csv`, `W1_missingness_profile.csv`, `W1_visibility_by_region.csv`.
- **Finding supported:** Data is technically fit for controlled diagnostic work.
- **Known limitations:** Structural completeness does not establish semantic accuracy or legal transferability.

## A02 — Reporting timeliness and source-quality profile

- **Decision question:** How much historical balance reporting is same-day under the supplied proxy?
- **Owner/date:** Baker / 2026-08-02
- **Input files and versions:** `daily_balances.csv`, `bank_accounts.csv`, `entity_master.csv`, and `fx_rates.csv` from initial commit `bcd0481`.
- **Population and exclusions:** All 9,955 account-days across 55 accounts and 181 calendar days; no exclusions.
- **Definitions:** Same-day = report date minus balance date equals zero calendar days. Within-one-day = delay of zero or one calendar day. Neither is start-of-day or elapsed-24-hour visibility.
- **Transformation steps:** Join accounts/entities/FX; calculate reporting delay; classify source quality; convert balances to USD; aggregate by account-day, region, and positive-balance value.
- **Reconciliation performed:** 55 × 181 = 9,955 account-days; regional and source-quality categories sum to total; 32 same-day accounts repeat across all 181 dates.
- **Quality tests:** Unique account/date keys, exact period, continuous daily panel, nonnegative delays, source-quality/visibility mapping, complete FX joins, and positive FX rates all pass.
- **Assumptions:** Report dates are accurate; date equality is an interim proxy; positive USD balance weighting is a sensitivity, not proof of availability.
- **Sensitivity:** 58.18% of account-days are same-day; 74.55% are within one calendar day; 55.14% of positive closing USD is on same-day accounts. None proves the Treasurer's start-of-day cash estimate.
- **Output files:** `data/processed/W1_data_quality_metrics.csv` and `W1_visibility_by_region.csv`.
- **Finding supported:** A reliable daily view is not demonstrated.
- **Known limitations:** Timestamps, cutoff, balance type, extract timing, and reconciled start-of-day cash totals are absent; account-day observations are repeated and not independent cash percentages.

## A03 — Preliminary payment/process profile

- **Decision question:** Is there sufficient evidence to prioritize a Week 2 payment diagnostic?
- **Owner/date:** Baker / 2026-08-02
- **Input files and versions:** `payments.csv`, `bank_accounts.csv`, `entity_master.csv`, `fx_rates.csv`, and `process_activity.csv` from initial commit `bcd0481`.
- **Population and exclusions:** All 7,600 supplied payment records and all nine supplied process rows; no exclusions. The payment extract's completeness and sampling method are unknown.
- **Definitions:** Rates use supplied payment records as denominator. Gross payment value includes Completed, Repaired, Rejected, and Pending. Repair capacity is time, not P&L or headcount reduction.
- **Transformation steps:** Join payment/account/entity/FX; translate each record at project date/currency rates; aggregate flags, status, value, and repair minutes; calculate six-month monthly averages; compare with process-file estimates.
- **Reconciliation performed:** Status counts sum to 7,600; all payment account/FX joins resolve; nonexceptions have zero repair minutes; gross value includes 54 rejected records/$2.18m and 17 pending/$1.55m.
- **Quality tests:** Primary key, schema, domains, boolean flags, positive amounts, nonnegative fees/minutes, currency consistency, status/exception logic, and FX coverage pass.
- **Assumptions:** The supplied file is analytically usable but not proven representative; repair minutes and process activity are management estimates; six months do not establish seasonality.
- **Sensitivity:** Payment file implies 79.83 exceptions and 55.78 repair hours/month, versus process estimates of 180 instances and 102.60 manual hours/month. Do not combine them until scope and period reconcile.
- **Output files:** `data/processed/W1_data_quality_metrics.csv` and `W1_data_quality_checks.csv`.
- **Result:** Within supplied records, 31.51% have manual touch, 6.30% exceptions, 5.00% late release, and 20,080 repair minutes; nine process rows imply 617.72 estimated manual hours/month.
- **Finding supported:** Payment/process friction is material enough to investigate.
- **Known limitations:** No source extract control, sampling method, reason codes, beneficiary/invoice completeness, criticality, cutoff/approval timestamps, observed labor, or realization assumptions; process and payment files have unresolved scope differences.

## A04 — Quantified issue-tree hypothesis anchors

- **Decision question:** Which additional Week 1 hypotheses can be quantified without converting assumptions into findings?
- **Owner/date:** Baker / 2026-08-03
- **Input files and versions:** All six raw project datasets from initial commit `bcd0481`; definitions inherit A01–A03.
- **Population and exclusions:** All 55 accounts, 9,955 account-days, 7,600 supplied payments, and nine supplied process rows; no records excluded.
- **Definitions:** Immediate account candidate = dormant, legacy-purpose, and zero supplied payments. Stale positive value = positive closing USD on accounts reported at least two calendar days late, summarized daily. Manual/cross-border shares use the supplied payment population. Capacity sensitivities apply 15% and 20% to estimated annual manual process hours.
- **Reconciliation performed:** Candidate accounts reconcile to the account file; payment cohort counts and repair minutes reconcile to 7,600 and 20,080; process hours reconcile to 617.72 per month.
- **Results:** Four immediate account candidates carry $7,800 of gross estimated annual fees. The median two-plus-day stale positive balance is $18.32m and never falls below $16.39m. Manual-touch records contribute 63.47% of exceptions and 63.35% of repair minutes; manual local transfer, wire, and ACH cohorts contribute 49.60% of repair minutes. Cross-border wires are 10.34% of records, with a 13.99% exception rate, 8.78% late rate, and 24.51% of repair minutes. Preliminary restrictions cover 21/55 accounts across all 16 entities and 13 countries. Six high-control activities represent 315.48 manual hours/month; 15–20% total-capacity sensitivities equal 1,111.89–1,482.52 hours/year.
- **Interpretation:** These values support falsifiable Week 2 thresholds; they do not prove closability, causation, transferability, control removability, headcount reduction, or cashable benefits.
- **Output file:** `data/processed/W1_data_quality_metrics.csv` generated by `src/week1_data_quality.py`.
- **Known limitations:** Account dependencies, payment population controls and reason codes, timestamped visibility, observed labor, legal/tax conclusions, and realization assumptions remain absent.

## A05 — Issue-tree ambition and stress test

- **Decision question:** Are the issue-tree hypotheses ambitious enough to change the mobilization decision while remaining numerically traceable?
- **Owner/date:** Baker / 2026-08-03
- **Input files and versions:** All six raw project datasets from initial commit `bcd0481`; calculations inherit A01–A04.
- **Population and exclusions:** All 55 accounts, 9,955 account-days, 7,600 supplied payments, and nine supplied process rows; no records excluded.
- **Observed anchors:** Delayed accounts carry a median $26.01m of positive estimated availability; the four dormant candidates average $37.46k in aggregate positive availability; 786 cross-border records total $14.72m and 4,921 repair minutes; preliminarily restricted accounts hold $8.05m of 30 June gross positive estimated availability; receipt reconciliation represents 133.28 manual hours/month. Concentration exceeds 25% for SAP-S4 payment records (50.00%), host-to-host accounts (36.36%), and Union Atlantic payment records (28.33%).
- **Base hypotheses:** Validate $35m as movable; close all four dormant candidates; reduce manual touch to 20%, exceptions to 4%, late release to 3.5%, and repair effort to 12,000 minutes over a comparable supplied-record period; redeploy 40% of receipt-reconciliation effort; reduce median delayed positive availability below $5m; halve cross-border friction; reach 50/55 same-day accounts with no more than two estimated-source accounts; and redeploy at least 150 manual hours/month.
- **Linked stress and stretch cases:** Stress movable cash at $21m, closures at two, and realized capacity at one-third of the identified target. Test $46.24m liquidity upside, $2.01m clearance of preliminarily restricted positive availability, and a 25–50 basis-point cross-border cost screen equal to approximately $73.61k–$147.22k annualized.
- **Classification:** Observed anchors are `ANALYST-CALC`; every target, stress case, stretch case, basis-point screen, and delivery gate is `ANALYST-ASSUMPTION` until Week 2 evidence supports or rejects it.
- **Output file:** `data/processed/W1_data_quality_metrics.csv` generated by `src/week1_data_quality.py`.
- **Known limitations:** These targets are intentionally ambitious and falsifiable. They are not booked cash release, P&L savings, headcount reduction, legal clearance, causal findings, or approved implementation commitments.
