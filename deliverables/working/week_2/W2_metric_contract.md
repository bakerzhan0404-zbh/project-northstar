# Week 2 — Metric and Evidence Contract

**Prepared by:** Baker

**Working period:** 10–16 August 2026

**Status:** Active analytical contract

**Classification:** Confidential — Project Northstar simulated client material

## Executive purpose

I will use one reconciled analytical layer to decide which four to six current-state findings should shape the Week 3 transformation options. A result enters the executive story only when it changes value, risk, feasibility, sequencing, or the evidence required for a decision.

## Governing evidence labels

| Label | Meaning | Permitted executive use |
|---|---|---|
| `ACG-DATA` | Supplied client material or project dataset | State what the supplied record says, with its scope and period |
| `ANALYST-CALC` | Reproducible calculation from supplied data | State the result with denominator, definition, and limitation |
| `ANALYST-ASSUMPTION` | Unverified input or scenario | Use for sensitivity only; never present as observed value |
| `ANALYST-JUDGMENT` | Interpretation or proposed action | Link explicitly to supporting facts and counterevidence |
| `JPM-PUBLIC` | Official public JPMorgan material | Use as context, not as proof of ACG performance or value |

## Reconciliation baseline

| Dataset | Required control | Scope boundary |
|---|---:|---|
| Entities | 16 entities; $3,900m supplied revenue | The client brief states $3.8bn; the difference remains unresolved |
| Accounts | 55 accounts; $110,100 estimated annual fees | Fees and preliminary restriction flags require client validation |
| Balances | 9,955 account-days; 1 Jan–30 Jun 2026 | Date-level reporting only; no timestamps or certified balance type |
| Payments | 7,600 records; $198.14m gross translated value | Supplied extract only; not a certified ACG-wide population |
| FX rates | 10 currencies × 181 days | Project translation rates, not executed FX economics |
| Process activity | Nine activities; 617.72 estimated manual hours/month | Management estimates, not observed time-and-motion evidence |

Every segmented output must reconcile to its applicable control before interpretation.

## Metric definitions and decision boundaries

### Account rationalization

| Metric | Definition | Protection or limitation |
|---|---|---|
| Closure-validation candidate | Dormant status + legacy purpose + zero records in the supplied payment extract | Candidate only; local purpose, signatories, collections, payroll, tax, regulation, resilience, and closure cost remain untested |
| Low-activity screen | Active account with low supplied-record count, evaluated as a sensitivity | Extract completeness is unproven; low count cannot establish dormancy |
| Gross candidate fee | Sum of `annual_fee_usd` for candidates | Estimated fee, not validated removable P&L |

### Cash visibility

| Metric | Definition | Denominator and limitation |
|---|---|---|
| Same-calendar-day visibility | `reported_to_group_date - date = 0` | All 9,955 account-days; not start-of-day visibility |
| Within-one-calendar-day sensitivity | Reporting delay of zero or one calendar day | Sensitivity only; dates do not prove elapsed 24-hour performance |
| Positive-value-weighted same-day rate | Positive estimated-available USD on same-day observations / all positive estimated-available USD across the six-month account-day panel | Describes value associated with the proxy, not point-in-time cash or validated movable cash |
| Delayed positive availability | Daily positive estimated available USD on accounts with delay above zero | Decision-timeliness exposure, not a loss or funding consequence |

### Liquidity and mobility

I will preserve the following interpretation ladder without collapsing categories:

```text
Observed ledger balance
        ↓
Estimated available balance
        ↓
Apparently available after preliminary restriction flags
        ↓
Screening result after an illustrative payment-intent window
        ↓
Validated movable cash — not established by the supplied data
```

| Metric | Definition | Boundary |
|---|---|---|
| Gross positive estimated availability | Sum of positive `available_balance_usd` | Before negative positions, restrictions, and buffers |
| Net estimated availability | Sum of positive and negative `available_balance_usd` | Not proof of transferability |
| Preliminarily unflagged positive availability | Positive estimate on accounts where `restricted_flag = False` | Unflagged does not mean legally or operationally movable |
| 7-day / 14-day screening window | Seven days provides a short-horizon payment-intent reference; 14 days extends the stability test across two weeks. Each uses account-level gross supplied-record value over the trailing calendar window; Completed/Repaired is shown as a status sensitivity. | `ANALYST-ASSUMPTION`; neither is an approved buffer or forecast. The screen does not separately model or validate complete payroll, tax, seasonal/peak expenditure, receipts, settlement calendars, forecast error, or extraordinary funding events. |
| Scenario surplus | Positive estimated availability less the illustrative buffer, floored at zero, then excluding preliminary restricted accounts | Sensitivity only; never labeled movable cash |
| Simultaneous surplus and deficit | Same date contains at least one positive and one negative estimated available account position | Shows coordination opportunity, not avoidable interest cost |

### Payment operations

All rates below use the 7,600 supplied records as the denominator unless the cohort is named explicitly.

| Metric | Definition | Boundary |
|---|---|---|
| Manual-touch rate | Mean of `manual_touch_flag` | Association only; no causal inference |
| Exception rate | Mean of `exception_flag` | Reason codes are absent |
| Late-release rate | Mean of `late_release_flag` | Approval/release timestamps and cutoff are absent |
| Rejection / pending rate | Status count divided by supplied records | Status-as-of timing and settlement are unknown |
| Repair effort | Sum of `repair_minutes`; monthly equivalent divides the six-month extract by six | Management-estimated capacity, not headcount or cashable savings |
| Concentration contribution | Cohort issue count or repair minutes / total issue count or repair minutes | Must be shown with cohort size to prevent small-denominator distortion |
| Gross supplied-record amount | Sum of payment-date FX-translated `amount_local` for all statuses in the named cohort | Payment intent/initiation value; not confirmed settlement or cash outflow |
| Priority payment cohort | Four mutually exclusive categories: manual touch only; manual touch + cross-border wire; cross-border wire only; neither | The explicit overlap prevents double counting; association does not establish cause |
| Priority union | Manual touch OR cross-border wire, deduplicated | Report records, exceptions, repair minutes, and gross amount together; retain the 7,600-record boundary |
| Exception-linked gross payment-intent amount | Sum of payment-date FX-translated amount where `exception_flag = True` | $12.48m across the extract; not settlement, loss, or confirmed outflow |
| Repair minutes per 100 records | `repair_minutes / eligible records × 100` | Use a reconciled, like-for-like population; current extract proxy is 264.21 |

### Process capacity and controls

| Metric | Definition | Boundary |
|---|---|---|
| Estimated manual hours/month | Frequency × minutes per instance × manual percentage / 60 | Management estimate; no realization rate |
| Loaded capacity equivalent | Manual hours × loaded hourly cost | Capacity-equivalent value, not booked P&L |
| Control-critical manual hours | Manual hours on High-criticality activities | Control must be preserved or replaced; manual does not automatically mean waste |

The payment-file repair baseline and process-file exception-repair baseline will remain separate until their populations and periods are reconciled.

## Finding-promotion rule

A finding reaches the main report only when it meets all six tests:

1. It reconciles to the applicable control total.
2. It is material to the CFO's Week 3 choice.
3. It states fact, magnitude, implication, likely cause, and action.
4. It distinguishes evidence from assumption and judgment.
5. It survives an explicit counterevidence or alternative-explanation test.
6. It points to a decision, owner, or evidence gate.

Detailed cuts that fail the promotion rule remain in the technical appendix. Receivables and FX remain data-gated because the supplied package contains neither controlled receivables records nor executed FX trades/exposures.

## Executive communication rule

The report, work brief, weekly update, and checkpoint deck will use the same answer-first spine:

1. Three executive conclusions.
2. The decision consequence of each conclusion.
3. The evidence and counterevidence.
4. Three actions or evidence requests required before Week 3.

No executive section will reproduce the sequence in which I performed the analysis.
