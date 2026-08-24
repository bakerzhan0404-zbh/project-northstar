# Project Northstar — Benefits-Tracking Dashboard

**Prepared by:** Baker · **Reporting date:** 24 August 2026

**Status:** Proposed control dashboard; G0 authorization and all client evidence gates remain open

**Dashboard type:** Static closeout snapshot with a machine-readable monthly ledger

## Executive status

| Control | Current status | Decision meaning |
|---|---:|---|
| Recognized cash value | `$0` | No account-level mobility and action evidence has passed VG01–VG05 |
| Recognized annual P&L | `$0` | No approved closure and verified invoice reduction has passed VG06–VG07 |
| Recognized productive capacity | `0 hours/month` | No sustained removal and productive redeployment has passed VG08–VG10 |
| Recognized risk value | `$0` ledger entry; exposure not quantified | No approved exposure and intervention valuation has passed VG11–VG12 |
| Evidence and cost packages closed | `0 of 22` | VG01–VG12 and CR01–CR10 remain open; model tests do not close evidence gates |
| Funding / production authority | `None` | The requested G0 decision authorizes evidence mobilization only |

## Four-value benefit ledger

| ID | Category | Diagnostic quantity | Validated | Funded | Recognized | Next evidence gate | Accountable owner |
|---|---|---:|---:|---:|---:|---|---|
| B01 | Cash release | `$35m` base liquidity screen | `$0` | `$0` | `$0` | VG01–VG05 | Group Treasurer; Finance validates |
| B02 | Annual P&L | `$7,800/year` fee sensitivity | `$0` | `$0` | `$0` | VG06–VG07 | Finance; local account owners |
| B03 | Capacity | `150 hours/month` hypothesis | `$0` | `$0` | `$0` | VG08–VG10 | Shared Services Lead; Finance |
| B04 | Risk reduction | Exposure and value not quantified | `$0` | `$0` | `$0` ledger entry | VG11–VG12 | Control owner; Finance |

The four categories are **non-additive**. Cash is not annual P&L, capacity remains in hours until an approved treatment exists, and zero recognized risk value does not mean zero exposure.

## Cost and affordability control

| Cost line | Low | Base | High | Current control |
|---|---:|---:|---:|---|
| One-time implementation | `$755k` | `$1.155m` | `$1.715m` | Analyst assumptions; high case exceeds the `$1.5m` ceiling by `$215k` |
| Recurring annual run cost | `$175k` | `$281k` | `$442k` | Separate BAU budget and G4 approval required |

CR01–CR10 must replace these planning assumptions with sourced scope, quotes or internal estimates, capacity, timing, contingency, and recurring support costs. One-time and recurring costs remain separate.

## Benefit-protection indicators

| Indicator | Current baseline | Decision threshold | Benefit consequence |
|---|---:|---|---|
| Same-day visibility proxy | `58.18%` of 9,955 account-days | `≥90%` in an approved cohort at G4 | A proxy improvement alone creates no cash value |
| Cash-position reconciliation | Not available | `100%` before a funding decision | Any unexplained material break blocks cash admission |
| Payment exception rate | `6.30%` within 7,600 records | `≥20%` relative reduction by G5 | Like-for-like evidence and attribution required |
| Late-release rate | `5.00%` within 7,600 records | No deterioration at G4 | Service deterioration can suspend benefit recognition |
| Rollback rehearsal | Not tested | Pass within four hours before G3 and scale | Failure blocks release and benefit recognition |
| Critical control/service incidents | Not available | `0` attributable incidents | Any critical event triggers review and possible suspension |

## Monthly review fields

Each monthly update must record the benefit ID, initiative, owner, applicable gate, baseline, target, actual, unit, measurement period, source, formula version, validated/funded/recognized status, one-time and recurring costs, forecast-to-complete, variance, attribution, counterfactual, confidence, exclusions, service/control/adoption indicators, evidence link, reviewer, approval date, and change-history reference.

Finance Benefits owns the ledger version. Benefit owners prepare evidence but cannot approve their own recognition. Population, source, formula, baseline, target, attribution, or time-window changes require approval and either restatement or a visible series break.

## Reproducible sources

- `data/processed/W4_benefits_tracker.csv` — four-value machine-readable ledger.
- `data/processed/W4_kpi_dictionary.csv` — KPI definitions, baselines, target logic, sources, cadence, and owners.
- `data/processed/W3_provisional_cost_estimates.csv` — low/base/high one-time and recurring planning assumptions.
- `src/week4_implementation.py` and `tests/test_week4_implementation.py` — rebuild and fail-closed controls.
