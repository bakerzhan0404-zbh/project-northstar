# Project Northstar — Weekly Update

- **Week:** 1
- **Prepared by:** Baker
- **Reporting date:** 2 August 2026
- **Overall status:** Amber

## Executive summary

The engagement question, scope, stakeholder tensions, issue tree, and four-week workplan are established. All supplied and expanded structural data-quality checks pass, enabling Week 2 diagnostic work. However, the evidence cannot yet establish cash movable within 24 hours, actual account closures, cashable cost savings, or payment root causes. The immediate priority is to convert the structurally sound dataset into a decision-grade diagnostic while explicitly validating restrictions, operating buffers, timestamps, and root-cause evidence.

## Work completed

| Workstream | Completed output | Evidence/location | Quality status |
|---|---|---|---|
| Engagement framing | Executive question, scope, stakeholder map, kickoff questions | `W1_engagement_alignment.md` | Complete |
| Problem structure | Prioritized issue tree and hypothesis changes | `W1_issue_tree.md` | Complete; evolves with evidence |
| External evidence | Three observations and three-case comparison | `W1_external_evidence_brief.md`; source log | Official sources; limitations recorded |
| Data readiness | Reproducible 33-check audit and report | `src/week1_data_quality.py`; processed CSVs; DQ report | 33/33 and 10/10 pass |
| Engagement controls | Workplan, analysis, decision, assumption, risk, findings, and interview logs | Week 1 folder | Initialized and current |

## What the evidence now suggests

| Emerging finding | Supporting evidence | Implication | Confidence |
|---|---|---|---|
| Data is structurally fit but semantically incomplete | All checks pass; high-impact fields absent | Proceed with controlled analysis, not final benefits | High |
| Reliable daily visibility is not demonstrated | 58.18% same-day proxy; 25.45% delayed ≥2 days | Visibility and data ownership likely matter in Wave 1 | High |
| Apparent cash cannot be called mobilizable | $55.66m estimated available; 21 preliminarily restricted accounts | Liquidity case requires local/legal validation | High |
| Payment friction is material enough to diagnose | 31.51% manual; 6.30% exceptions; 20,080 repair minutes | Segment causes before selecting intervention | Medium |
| Ten account closures are not yet supported | Four dormant accounts | Use a candidate-validation process, not a booked benefit | High |

## Hypothesis changes

| Hypothesis | Previous status | Current status | What changed it |
|---|---|---|---|
| Visibility is materially below a reliable daily standard | Untested | Supported | Reconciled reporting-delay profile |
| Ten or more accounts can close | Untested | Unresolved | Only four marked dormant; restriction/dependency data absent |
| Manual payment processes create material repair | Untested | Supported | Manual, exception, late, and repair metrics |
| Centralization is the preferred model | Untested | Untested | External cases relevant but not transferable; local/control constraints remain |
| Pilot-first sequencing is required | Untested | Supported | Peak-season, ERP, resilience, and control constraints |

## Decisions, support, or escalation required

| Request | Why it matters | Decision owner | Required by |
|---|---|---|---|
| Agree visibility KPI and provide timestamps | Same-day proxy cannot prove start-of-day control | Treasurer / CIO | Week 2 |
| Validate restrictions and operating buffers | Can reverse liquidity opportunity | Treasury / Legal / Tax / Local Finance | Before Week 3 |
| Provide exception reasons and repaired samples | Needed to prove root causes | Shared Services | Week 2 |
| Provide fee invoices and facility statements | Needed for P&L/borrowing baseline | Treasury / Finance | Week 3 |

## Risks and uncertainties

| Risk or uncertainty | Decision impact | Mitigation or validation action | Owner |
|---|---|---|---|
| Apparent available cash is not transferable | Overstates value and favors wrong option | Scenario ranges plus local/legal validation | Daniel Wu |
| Manual effort includes required control | Overstates capacity benefit | Time sample and control classification | Martin Blake |
| Six-month period misses seasonality | Weakens peak-season inference | Obtain longer history or constrain claims | Data owner |
| External cases create solution bias | Predetermines design | Evaluate three genuine options against ACG evidence | Baker |
| $3.9bn entity revenue does not reconcile to $3.8bn brief | Can distort denominator-based metrics | Reconcile scope, period, eliminations, and rounding | Group Finance |

## Priorities for Week 2

1. Complete reconciled account, visibility/liquidity, payment, and process diagnostics.
2. Build root-cause and maturity views with confidence and counterevidence.
3. Select four to six CFO-relevant findings and agree what remains unresolved.
