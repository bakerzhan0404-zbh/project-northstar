# Project Northstar — KPI Dictionary and Benefits-Tracking Framework

**Prepared by:** Baker · **Date:** 24 August 2026
**Status:** Proposed; owner, baseline, and target approval remains part of G1–G3

## Performance contract

Every KPI must have a controlled population, definition, formula, source, frequency, accountable owner, baseline boundary, target logic, and change history. Missing records remain in the denominator unless an approved definition says otherwise. Like-for-like comparisons must disclose any population, source, or formula change.

The machine-readable dictionary is `data/processed/W4_kpi_dictionary.csv`.

## Executive dashboard

| Dimension | KPI | Current baseline | Proposed decision threshold | Owner |
|---|---|---:|---|---|
| Data | Same-day cash visibility proxy | `58.18%` of 9,955 account-days | `≥90%` in approved cohort at G4; enterprise target after G1 | Group Treasurer |
| Data | Two-plus-day delayed account-days | `2,534` of 9,955 | `≥75%` reduction in approved cohort by G5 | Treasury Data Owner |
| Control | Reconciled cash positions | Not available | `100%` before a funding decision | Group Treasurer |
| Liquidity | Certified movable cash | `$0` recognized | Target only after VG01–VG05 | Group Treasurer; Finance validates |
| Operations | Manual-touch rate | `31.51%` of supplied 7,600 | Target after root-cause review; bounded first test | Shared Services Lead |
| Operations | Payment exception rate | `6.30%` | `≥20%` relative reduction in like-for-like cohort by G5 | Shared Services Lead |
| Service | Late-release rate | `5.00%` | No deterioration at G4; `≥20%` relative reduction by G5 | Shared Services / BU Finance |
| Control | Emergency-payment compliance | Not available | `100%` | BU Finance / Control owner |
| Adoption | Trained and access-certified roles | `0%` program start | `100%` before production access | Change Lead / CIO |
| Resilience | Rollback within four hours | Not tested | Pass before G3 and each material scale event | CIO / Process owner |
| P&L | Verified fee removal | `$0` recognized | Recognition only after VG06–VG07 | Finance / Group Treasurer |
| Capacity | Productively redeployed hours | `0` recognized | Recognition only after VG08–VG10 | Shared Services / Finance |
| Risk | Critical change-attributable incidents | Not available | `0`; any event triggers review | Control owner / CIO |
| Economics | Evidence-gate closure | `0%` | Relevant VG/CR packages closed for each decision | Finance Benefits Lead |

### Baseline cautions

- `58.18%` is a same-calendar-date proxy, not a start-of-day operational metric.
- Payment rates are within the supplied 7,600-record extract, not certified enterprise performance.
- `0 recognized` means evidence has not met the recognition rule; it does not mean zero opportunity or zero risk.
- Targets are proposed. ACG must approve denominator, cutoff, materiality, cohort, and measurement windows before use in incentives or external reporting.

## Four-value benefit ledger

| Category | Diagnostic quantity | Validated | Funded | Recognized | Gate | Owner |
|---|---:|---:|---:|---:|---|---|
| Cash release | `$35m` base liquidity screen | `$0` | `$0` | `$0` | VG01–VG05 | Group Treasurer; Finance validates |
| Annual P&L | `$7,800/year` estimated fee sensitivity | `$0` | `$0` | `$0` | VG06–VG07 | Finance; local account owners |
| Capacity | `150 hours/month` hypothesis | `$0` | `$0` | `$0` | VG08–VG10 | Shared Services Lead; Finance |
| Risk reduction | Exposure and value not quantified | `$0` | `$0` | `$0` ledger entry | VG11–VG12 | Control owner; Finance |

The categories are **non-additive**. Capacity is reported in hours until Finance approves a productive redeployment or other treatment. Cash is not annual P&L. Risk value cannot be inferred from a zero recognized entry.

The machine-readable tracker is `data/processed/W4_benefits_tracker.csv`.

## Cost tracking

| Cost treatment | Low | Base | High | Recognition boundary |
|---|---:|---:|---:|---|
| One-time implementation | `$755k` | `$1.155m` | `$1.715m` | Analyst assumption until CR01–CR10 evidence; no spend authority |
| Recurring annual run cost | `$175k` | `$281k` | `$442k` | Separate BAU budget required before go-live |

The program must forecast and report one-time and recurring cost separately. A likely one-time outcome above `$1.5m` returns to the Steering Committee; it is not silently absorbed through scope or contingency.

## Benefit recognition workflow

| Status | Meaning | Minimum evidence | Who approves |
|---|---|---|---|
| Diagnostic | Screen, estimate, or hypothesis used to direct validation | Reproducible calculation and disclosed boundary | Analysis owner |
| Validated | Evidence confirms the baseline and eligibility under the category rule | Reconciled source, definition, owner, specialist/control evidence | Finance Benefits and accountable process owner |
| Funded | The Steering Committee has approved the relevant intervention/cost and target | Validated case, approved funding, timing, owner, gate pass | CFO / Steering Committee |
| Recognized | Realized outcome is evidenced for the approved period and attribution | Actuals, counterfactual/attribution, cost netting where relevant, no service/control degradation | Finance |

No status is automatically inherited from the previous status. A model-control pass is not evidence validation.

## Monthly benefits dashboard fields

For each value line, report:

- benefit ID, category, owner, initiative, and applicable gate;
- baseline, target, actual, unit, measurement period, source, and formula version;
- validated, funded, and recognized amounts/statuses separately;
- one-time and recurring costs, forecast-to-complete, and variance;
- attribution method, counterfactual, confidence, and exclusions;
- service/control/adoption indicators and any disqualifying event;
- evidence link, reviewer, approval date, and change-history reference.

## Change control

- Finance Benefits owns the KPI dictionary and benefit-ledger version.
- Population, baseline, formula, target, source, attribution, or time-window changes require approval before comparison.
- Material changes require prior-period restatement or a visible break in series.
- Benefit owners prepare evidence; they do not self-approve recognition.
- Critical service/control incidents can suspend benefit recognition even when the operational metric improves.
- The Steering Committee receives both positive and negative variance; unvalidated pipeline is never shown as realized value.

## Reproducibility

Run:

```bash
python3 src/week4_implementation.py
python3 tests/test_week4_implementation.py
```

Outputs:

- `data/processed/W4_kpi_dictionary.csv`
- `data/processed/W4_benefits_tracker.csv`
- `data/processed/W4_stage_gates.csv`
- `data/processed/W4_initiative_portfolio.csv`
- `data/processed/W4_roadmap_milestones.csv`
