# Project Northstar — Week 2 Execution Brief

**Prepared by:** Baker

**Working period:** 10–16 August 2026

**Status:** Planned

**Classification:** Project Northstar simulated client material

## Executive direction — what matters in 90 seconds

Week 2 will not analyze every treasury topic equally. It will test three executive findings and produce only four to six conclusions that could change the Week 3 recommendation.

| Observed anchor entering Week 2 | Hypothesis and decision test | Week 3 evidence gate |
|---|---|---|
| Visibility evidence: 23/55 accounts are delayed and median positive estimated availability outside same-day visibility is $26.01m | Is the gap operationally real, does it create a greater-than-$5m funding/decision consequence, and can 50/55 accounts reach the target without ERP replacement? | Timestamped receipt/cutoff/reconciliation evidence for all 55 accounts |
| Liquidity boundary: $57.80m gross positive estimated availability is not validated movable cash | Does the evidence support the $21m stress / $35m base / $46.2m upside range after restrictions, buffers, timing, and entity rules? | Account-level transferability, buffers, funding events, facility use, and borrowing/transfer costs |
| Payment signal: within the **7,600 supplied records only**, manual touch is 31.51%, exceptions 6.30%, late release 5.00%, and repair is 20,080 minutes | Which cohorts matter, what service/control consequence follows, and which apparent causes survive validation? No result will be generalized to ACG's full population without source reconciliation. | Source population/value control, sampling logic, reason codes, approval/release timestamps, and criticality |

**Executive output:** the three findings above, plus one to three supporting findings on account rationalization, operating-model/control feasibility, or another issue that materially changes the decision. Receivables and FX remain P1 and data-gated.

## My Week 2 mission

In Week 2, I will turn the Week 1 evidence foundation into a reconciled current-state diagnostic. My goal is to determine which treasury problems are material enough to affect ACG's transformation choice, explain their likely causes, and distinguish clearly between what the supplied evidence proves and what still requires client validation.

I will not begin with a predetermined solution. I will build the diagnostic in small, reproducible modules, reconcile each module to the Week 1 control totals, record the result in the engagement logs, and commit each logical step separately before using it in the report or checkpoint deck.

## How I will prioritize the work

- **P0 — required:** Work that must be complete for a defensible Week 2 diagnostic and submission.
- **P1 — conditional enrichment:** Work that improves confidence or scope if additional client evidence becomes available, but will not delay the P0 diagnostic.
- A P1 evidence request in Week 2 may become a P0 dependency for the Week 3 recommendation and business case.

## Finding-promotion and depth rule

| Depth | Week 2 topics | Rule |
|---|---|---|
| **Full P0 diagnosis** | Cash visibility; liquidity and cash mobility; payment friction within the supplied 7,600-record extract | Complete reconciled analysis because these topics can directly change Wave 1 scope, value, or risk. |
| **P0 supporting screen** | Account rationalization; targeted operating-model and control feasibility | Analyze only far enough to determine whether each topic earns one of at most three supporting-finding slots or changes implementation sequencing. |
| **P1 and data-gated** | Receivables; FX transactions/exposure; broad maturity scoring; exhaustive process mapping | Do not develop a main-report section unless controlled evidence arrives and the result could change the recommendation. Record the gap instead. |

Only four to six findings may enter the main report. A finding is promoted only if it is material to the decision, reconciles to the baseline, has a clear consequence, survives a counterevidence test, and leads to a decision or action. Detailed methods, control results, and domain cuts will sit in appendices.

## My working rules

1. I will keep `data/raw/` unchanged and generate calculated outputs under `data/processed/`.
2. I will define each KPI, denominator, period, filter, exclusion, and sensitivity before interpreting it.
3. I will reconcile totals before segmenting them by region, entity, bank, currency, account, payment type, or month.
4. I will distinguish `ACG-DATA`, `ANALYST-CALC`, `ANALYST-ASSUMPTION`, and `ANALYST-JUDGMENT`.
5. I will keep observed balances, estimated availability, scenario surplus, and validated movable cash separate.
6. I will describe account records as closure-validation candidates, not approved closures.
7. I will treat manual hours as capacity unless a validated removal rate and financial baseline support cashable savings.
8. I will identify associations in the payment data without claiming root causes that the supplied fields cannot prove.
9. I will add code, generated outputs, tests, and the related analysis-log update to the same logical analytical commit.
10. I will stage explicit file paths, review the staged diff, commit locally, and avoid including `.DS_Store` files.

## Week 1 hypothesis thresholds I will carry forward

These are intentionally ambitious `ANALYST-ASSUMPTION` tests, not findings. I will retain them as the Week 2 base and stress cases unless new evidence supports a documented change.

| Theme | Base hypothesis | Stress, stretch, or acceptance test |
|---|---|---|
| Liquidity | Validate at least $35m as movable within 24 hours | $21m stress; $46.2m upside |
| Accounts | Close all four dormant candidates within 12 months | Two closures under stress; ten remains management's stretch |
| Visibility | Reach 50/55 same-day accounts and reduce median delayed positive availability below $5m | Upgrade 18/23 delayed accounts, including 12/14 spreadsheet accounts |
| Payment friction | Reach no more than 20% manual touch, 4% exceptions, 3.5% late release, and 12,000 repair minutes | Cross-border cohort at no more than 7% exceptions, 5% late release, 2,500 repair minutes, and zero critical failures |
| Capacity | Redeploy at least 150 hours/month; if controlled receivables data arrives, test 53.31 hours/month in receipt reconciliation | One-third realization stress equals 50 hours/month |
| Restrictions | Clear at least $2.01m of flagged positive availability | $4.03m restriction-clearance stretch; no amount becomes movable cash without account-level certification |
| FX evidence (P1) | If controlled transaction data arrives, test 25–50 basis points of cross-border cost | Reconcile at least 95% of transaction value before drawing a conclusion; otherwise retain an evidence gap |
| Execution | Pilot 10 delayed accounts before the remaining eight-account rollout | Four consecutive weeks meeting service gates; rollback within four hours |
| Benefits | Require complete evidence and Finance approval for every funded-base benefit | Recommendation survives $21m mobility, two closures, and 50 hours/month; realized value reaches 90% of target for three months |

## P0 mission 1 — Establish the analytical contract and baseline

### What I will do

- Carry forward the Week 1 questions, hypotheses, assumptions, risks, findings, and unresolved validation requests.
- Define the Week 2 metrics and evidence boundaries before calculating new findings.
- Build a reusable Week 2 analysis script that joins entities, accounts, balances, FX rates, payments, and process activity.
- Add automated checks for joins, totals, USD conversion, segmentation, and scenario consistency.

### Baselines I will reproduce

- 16 entities and 55 accounts
- 9,955 account-day balance observations
- 7,600 supplied payment records
- $198.14 million of gross translated supplied payment value across all statuses
- 20,080 repair minutes in the payment file
- 617.72 estimated manual process hours per month in the process file

### Completion gate

Every later Week 2 output uses the same reconciled analytical layer, and the original 10 data-quality tests plus the expanded Week 1 controls continue to pass.

### Planned commits

1. `Initialize Week 2 diagnostic workspace`
2. `Define Week 2 metrics and evidence boundaries`
3. `Build Week 2 reconciled analysis baseline`
4. `Test Week 2 diagnostic reconciliations`

## P0 supporting screen 2 — Test account-rationalization feasibility

### Question I will answer

> Which accounts should enter closure validation, what makes them candidates, and which protections could prevent closure?

### What I will do

- Run a bounded screen and deepen it only if candidate closures could materially change Wave 1 scope, value, risk, or sequencing.
- Profile the 55 accounts by region, entity, bank, currency, purpose, age, ERP, acquisition origin, visibility method, sweep structure, status, preliminary restriction, activity, balance, and estimated annual fee.
- Define transparent screening criteria for dormant, legacy, low-activity, low-value, high-fee, or operationally overlapping accounts.
- Protect payroll, tax, collection, restricted, regulatory, resilience, and locally required accounts from automatic closure conclusions.
- Test how candidate counts and estimated fees change when the criteria change.
- Produce a local-validation checklist covering legal purpose, signatories, collections, payroll, tax, service continuity, and closure cost.

### Interpretation boundary

Observed account fees may be reported, but fee savings will remain unvalidated until the account can actually close and the fee can actually be removed.

### Completion gate

All account segments reconcile to 55 accounts, every candidate has a recorded reason, and every exclusion or protection rule is traceable.

### Planned commits

5. `Profile ACG bank account footprint`
6. `Define account closure validation candidates`

## P0 mission 3 — Diagnose cash visibility

### Question I will answer

> Where and why does Group Treasury lack a timely and reliable view of global cash?

### What I will do

- Calculate same-calendar-day visibility and a within-one-calendar-day sensitivity.
- Measure one-day, two-day, and longer reporting delays.
- Segment visibility by region, entity, bank, visibility method, source quality, account purpose, month, and date.
- Compare count-weighted and positive-value-weighted results.
- Test whether reporting performance is consistent over time or concentrated in particular sources or regions.

### Interpretation boundary

Because the data contains dates but no timestamps, I will not describe the result as start-of-day visibility or proof of visibility within 24 hours.

### Completion gate

All visibility observations reconcile to 9,955 account-days, alternative definitions are shown, and every chart states its denominator and limitation.

### Planned commit

7. `Analyze cash visibility by region and source`

## P0 mission 4 — Diagnose liquidity and apparent surplus

### Question I will answer

> How much cash is observed, apparently available, restricted, required under an illustrative buffer, or genuinely validated for movement?

### What I will do

- Convert ledger and estimated available balances to USD using the supplied project FX rates.
- Reconcile gross positive balances, negative balances, and net positions by date.
- Separate preliminarily restricted and unflagged accounts.
- Identify simultaneous positive and negative positions across accounts and entities, including their frequency and duration.
- Test at least two explicit operating-buffer sensitivities, provisionally based on 7-day and 14-day supplied payment activity.
- Show results by entity, region, currency, and date where the evidence supports the segmentation.

### Interpretation ladder

```text
Observed ledger balance
        ↓
Estimated available balance
        ↓
Apparently available after preliminary restriction flags
        ↓
Scenario surplus after an assumed operating buffer
        ↓
Validated movable cash — not established by the supplied data
```

### Interpretation boundary

The buffer scenarios will be labeled analyst sensitivities because the payment extract is not certified complete. No scenario output will be described as transferable cash.

### Completion gate

Each scenario reconciles back to the daily balance baseline, assumptions are visible, and no restricted or buffer-dependent amount is presented as validated value.

### Planned commits

8. `Build liquidity and operating buffer scenarios`
9. `Identify simultaneous surplus and deficit positions`

## P0 mission 5 — Diagnose payment and process friction

### Question I will answer

> Where are manual activity, exceptions, delays, rejection, repair effort, and estimated fees concentrated?

### What I will do

- Profile payment volume and value by type, region, entity, currency, bank, account purpose, cross-border status, status, month, and explicit amount band.
- Calculate manual-touch, exception, late-release, rejection, pending, repair-time, and estimated-fee metrics.
- Rank concentrations by both rate and absolute contribution so small cohorts with high percentages do not distort the priorities.
- Compare the data patterns with stakeholder claims while preserving contradictory evidence and possible bias.
- Reconcile 55.78 repair hours per month implied by the payment file with 102.60 exception-repair hours per month in the process file without forcing them into one baseline.
- Profile the 617.72 total estimated manual process hours by team, process, and control criticality.
- Separate potentially avoidable work from control-critical activity.

### Interpretation boundary

Missing reason codes, approval timestamps, invoice fields, beneficiary fields, and payment criticality prevent a proven root-cause conclusion. Estimated capacity will not be called headcount or cashable savings.

### Completion gate

All payment segments reconcile to the 7,600 supplied records, $198.14 million gross supplied-record value, and 20,080 repair minutes. No rate or concentration is generalized to ACG's full population, and the payment/process baselines remain separately labeled until both scope differences and source-population coverage are validated.

### Planned commits

10. `Profile ACG payment operations`
11. `Locate payment friction concentrations`
12. `Reconcile payment repair and process capacity`

## P0 supporting screen 6 — Test targeted operating-model and control feasibility

### Question I will answer

> Can ACG implement and control the interventions implied by the promoted findings, and which likely causes or ownership gaps could prevent delivery?

### What I will do

- Map only the cash-visibility, liquidity, and payment steps needed to explain or implement the promoted findings.
- Trace the relevant ERP, spreadsheet, bank, and manual handoffs; rework loops; control points; and unclear ownership.
- Draft a targeted RACI for the owners needed to validate evidence, approve interventions, protect controls, and deliver Wave 1.
- Test likely causes across data, process, policy, systems, organization, governance, controls, and user behavior without converting association into proof.
- Use observable maturity criteria only where a capability gap changes an intervention or its sequencing; do not create an equal-weight seven-dimension scorecard by default.

### Interpretation boundary

The targeted process views, RACI, cause hypotheses, and any capability assessments will remain draft until validated with process owners.

### Completion gate

Every supporting point traces to a promoted finding, cites evidence, states confidence, and distinguishes a symptom from a likely cause. Week 2 will not produce a broad maturity profile unless it earns a decision-relevant finding.

### Planned commits

13. `Map causes and responsibilities behind promoted findings`
14. `Assess targeted operating-model feasibility`

## P0 mission 7 — Synthesize and communicate the diagnostic

### What I will do

- Promote only four to six findings that materially affect the CFO's transformation decision.
- Require each promoted finding to contain a fact, magnitude, implication, likely root cause, confidence, counterevidence, potential action, and reproducible source.
- Update the issue-tree hypotheses based on the diagnostic rather than preserving the Week 1 position automatically.
- Draft the diagnostic report before building the checkpoint deck.
- Use the report evidence to create five answer-first slides.
- Update all cumulative engagement-control logs and prepare the one-page weekly update.
- Run reproducibility, source, link, page-limit, slide-count, and Git quality checks before marking the pack ready for review.

### Planned report sequence

1. Three findings, three decisions, and three requests
2. Ranked four to six decision-relevant findings
3. Consequences and likely causes
4. Week 3 option implications and decision thresholds
5. Unresolved validations and next decisions

### Planned technical appendices

1. Definitions, evidence boundaries, and methods
2. Week 2 reconciliations and the Week 1 52-control inventory
3. Detailed domain cuts, sensitivities, and unpromoted observations
4. Analysis log, assumptions, risks, decisions, findings, and source notes

### Planned five-slide checkpoint sequence

1. Executive diagnosis: three findings, decisions, and requests
2. Cash visibility and mobility
3. Payment friction—explicitly limited to the supplied 7,600 records
4. Supporting feasibility findings that earned promotion
5. Decisions, Week 3 implications, and the three evidence gates

### Completion gate

The main report is no more than eight pages, the deck contains five core slides, every material number traces to a processed output, and all limitations that could change the recommendation are visible. Technical methods, control results, and detailed domain cuts appear only in the appendices.

### Planned commits

15. `Synthesize Week 2 root causes and findings`
16. `Draft the Week 2 diagnostic report`
17. `Build the Week 2 diagnostic checkpoint deck`
18. `Finalize the Week 2 diagnostic pack`

## Evidence requests and P1 missions

### Three gates to the Week 3 recommendation

1. **Timestamped visibility evidence:** Receipt timestamps, cutoff, balance type, source, and reconciliation for all 55 accounts.
2. **Liquidity transferability and economics:** Account-level legal/local certification, operating buffers, settlement constraints, funding events, facility use, and borrowing/transfer costs.
3. **Controlled payment evidence:** Source population/value totals, sampling logic, reason codes, approval/release timestamps, and criticality for the supplied 7,600-record extract.

### Secondary and option-dependent backlog

- Account dependencies, signatories, local purposes, and closure costs
- Twelve to twenty-four months of history for seasonality analysis
- AR, receipt, remittance, match-status, reason, and aging records
- FX trades, exposures, hedges, spreads, fees, and settlement records
- Stakeholder validation of targeted process, responsibility, root-cause, and maturity work
- Reconciliation of the $3.9bn entity sum to the $3.8bn brief

If evidence arrives, I will add it through a separate commit with its own reconciliation and analysis-log entry. If it does not, I will record the affected decision, owner, and earliest safe decision point. I will not substitute an external benchmark or analyst assumption for missing ACG evidence.

## Commit and review routine

Before each analytical commit, I will:

1. Run the relevant analysis and automated tests.
2. Reconcile the new output to the approved baseline.
3. Review the working-tree diff and stage only the intended files.
4. Review the staged diff for accidental files or unsupported claims.
5. Commit one logical analytical result with the planned message.
6. Confirm the remaining working-tree changes belong to later work.

I will keep these commits local during active development unless a mentor checkpoint requires the updated public repository. I will not push automatically.

## What I should be able to explain at the Week 2 checkpoint

By the end of Week 2, I should be able to explain:

- Which four to six findings matter most and exactly how each changes ACG's transformation decision
- Which statements are observed facts, calculations, assumptions, or judgments—including the 7,600-record boundary on every payment conclusion
- The difference between observed cash, apparent availability, scenario surplus, and validated movable cash, and which threshold the evidence supports
- Which likely causes, account candidates, and implementation constraints are supported versus still hypotheses
- Which three evidence packages remain critical, who should supply them, and what Week 3 decision each package unlocks
