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
| A06 | Week 2 analytical contract and baseline | Do all later modules use one controlled population and definition set? | Defined | `W2_metric_contract.md` |
| A07 | Account rationalization screen | Which accounts merit local closure validation without weakening required services or controls? | Planned | Pending |
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
- **Reconciliation required:** 16 entities, 55 accounts, 9,955 account-days, 7,600 supplied payment records, $198.14m gross translated supplied-record value, 20,080 repair minutes, and 617.72 estimated manual process hours/month.
- **Executive use:** Only findings meeting the six-part promotion rule enter the main report.
- **Status:** Defined; executable controls pending A07–A12 code.
