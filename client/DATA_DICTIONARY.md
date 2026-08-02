# Data Dictionary

All files under `data/raw/` are generated project datasets.

## `entity_master.csv`

| Field | Meaning |
|---|---|
| `entity_id` | Unique legal-entity identifier |
| `entity_name` | Legal-entity name |
| `region` | NA, EMEA, or APAC |
| `country` | Operating country |
| `functional_currency` | Entity's primary operating currency |
| `revenue_usd_m` | Annual revenue in USD millions |
| `erp_system` | Current ERP environment |
| `acquisition_origin` | Organic or acquisition cohort |
| `cash_restriction_level` | Indicative restriction classification; requires validation |

## `bank_accounts.csv`

| Field | Meaning |
|---|---|
| `account_id` | Masked account identifier |
| `entity_id` | Owning legal entity |
| `bank_name` | Banking provider |
| `country` | Account domicile |
| `currency` | Account currency |
| `purpose` | Operating, collection, payroll, tax, or legacy |
| `open_date` | Account opening date |
| `status` | Active or dormant |
| `visibility_method` | API, host-to-host, portal, or spreadsheet |
| `sweep_structure` | None, domestic sweep, or regional pool |
| `annual_fee_usd` | Estimated annual account/service fee |
| `restricted_flag` | Whether the account is preliminarily identified as restricted |

## `daily_balances.csv`

| Field | Meaning |
|---|---|
| `date` | Calendar date |
| `account_id` | Account identifier |
| `closing_balance_local` | End-of-day ledger balance in account currency |
| `available_balance_local` | Estimated available balance in account currency |
| `reported_to_group_date` | Date on which balance became visible to Group Treasury |
| `source_quality` | Automated, manually reported, or estimated |

## `payments.csv`

| Field | Meaning |
|---|---|
| `payment_id` | Unique payment identifier |
| `payment_date` | Initiation date |
| `account_id` | Debit account |
| `payment_type` | ACH/local transfer, wire, payroll, tax, or internal transfer |
| `currency` | Payment currency |
| `amount_local` | Payment amount in local currency |
| `cross_border_flag` | Cross-border indicator |
| `manual_touch_flag` | Whether a person manually intervened |
| `exception_flag` | Whether processing generated an exception |
| `late_release_flag` | Whether released after internal cutoff |
| `repair_minutes` | Estimated operations time spent on repair |
| `fee_usd` | Transaction and exception-related fee estimate |
| `status` | Completed, repaired, rejected, or pending |

## `fx_rates.csv`

| Field | Meaning |
|---|---|
| `date` | Calendar date |
| `currency` | Currency code |
| `usd_per_unit` | Project USD value of one currency unit |

## `process_activity.csv`

| Field | Meaning |
|---|---|
| `team` | Team performing activity |
| `process` | Treasury activity |
| `frequency_per_month` | Approximate monthly volume |
| `minutes_per_instance` | Average handling time |
| `manual_percentage` | Estimated share performed manually |
| `loaded_hourly_cost_usd` | Illustrative fully loaded labor rate |
| `control_criticality` | Low, medium, or high |

## Data limitations you must address

- Ledger balances do not prove legal availability or transferability.
- `restricted_flag` is preliminary, not legal or tax advice.
- Payment fees are estimates and do not represent actual bank pricing.
- Missing or delayed reporting may bias liquidity calculations.
- FX rates are provided for the project analysis period.
- Process time estimates are management estimates, not time-and-motion observations.
- Historical patterns do not guarantee future benefits.
