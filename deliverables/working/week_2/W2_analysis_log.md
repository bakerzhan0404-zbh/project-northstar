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
| A08 | Cash visibility diagnostic | Where is cash reporting insufficiently timely for Group Treasury decisions? | Planned | Pending |
| A09 | Liquidity and buffer scenarios | What is observed, apparently available, buffer-dependent, or still unvalidated? | Planned | Pending |
| A10 | Simultaneous surplus/deficit | How often do positive and negative positions coexist? | Planned | Pending |
| A11 | Payment friction profile | Which supplied-record cohorts drive manual work, exceptions, delay, and repair? | Planned | Pending |
| A12 | Process capacity and controls | Which estimated manual activities are material and which controls must be preserved? | Planned | Pending |
| A13 | Targeted operating-model feasibility | Which ownership, handoff, data, and control gaps affect Wave 1 feasibility? | Planned | Pending |

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
