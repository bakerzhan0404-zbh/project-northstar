# Your One-Month Engagement Playbook

Welcome to Project Northstar. Over the next four weeks, you will operate as an analyst on a J.P. Morgan Payments Advisory engagement. Your job is not to produce the largest volume of analysis. Your job is to help the client make a defensible decision.

The project contains four consulting phases. You will submit **one integrated assignment at the end of each week**. Use the activities below to manage your work during the week, but organize your time according to your own schedule.

## Submission cadence

| Week | Consulting phase | Weekly submission | Client/manager checkpoint |
|---:|---|---|---|
| 1 | Frame the problem and establish the evidence base | Engagement foundation pack | Hypothesis and data-readiness review |
| 2 | Complete the current-state diagnostic | Diagnostic pack | Treasurer diagnostic review |
| 3 | Develop and quantify the recommendation | Strategy and business-case pack | CFO interim steering review |
| 4 | Convert the answer into an executable plan | Final executive pack | Final steering committee |

## Standard weekly update

At the end of each week, submit the required assignment and a one-page update using `templates/weekly_update_template.md`. Your update must state:

- What you completed
- What the evidence now suggests
- Which hypotheses changed
- Which decisions or support you need
- What remains uncertain
- Your priorities for the following week

Save weekly work in `deliverables/working/week_#/`. Submit final materials to `deliverables/final/`.

---

# Week 1 — Frame the problem and establish the evidence base

## Your objective

Translate the client mandate into a decision-led workplan, establish an authoritative external fact base, and determine whether the supplied data is fit for analysis.

## Recommended activity sequence

### Activity 1 — Understand the mandate

1. Read the README, engagement charter, client brief, stakeholder pack, and data dictionary.
2. Write the executive question in your own words.
3. Identify decision makers, stakeholders, objectives, constraints, and out-of-scope areas.
4. Create a stakeholder map using influence and impact as the dimensions.
5. Draft ten kickoff questions. At least three must challenge an assumption in the brief.
6. Initialize your workplan, decision log, source log, assumptions register, and risk register.

### Activity 2 — Build a decision-led issue tree

1. Draft an issue tree covering value, risk, feasibility, and execution.
2. Write one initial hypothesis for each major branch.
3. Identify the evidence required to prove or disprove each hypothesis.
4. Rank questions by decision importance and evidence availability.
5. Convert the issue tree into a four-week workplan with milestones and dependencies.

### Activity 3 — Establish your JPMorgan evidence base

1. Read `references/JPM_BENCHMARK_PACK.md` and sources S01–S05 in `references/JPM_PUBLIC_SOURCES.md`.
2. Review at least three JPMorgan client transformations from source S06.
3. Compare client context, problem, intervention, reported outcome, evidence strength, and relevance to ACG.
4. Record every useful claim in the source log, including its limitation.
5. Identify three themes that appear across multiple sources and two areas where external evidence is insufficient.
6. Revise your hypotheses based on what you learned.

### Activity 4 — Validate and profile the data

1. Run `python3 src/generate_data.py` and `python3 tests/test_data_quality.py`.
2. Read and run `src/starter_analysis.py`.
3. Reconcile record counts, date ranges, currencies, accounts, entities, and payment totals.
4. Test referential integrity between accounts, entities, balances, and payments.
5. Quantify missing, delayed, estimated, and manually reported observations.
6. Create a data-quality issue log with impact, proposed treatment, and owner.
7. Identify which business questions cannot yet be answered confidently.

## Week 1 assignment — Engagement Foundation Pack

Submit one organized folder containing:

1. `W1_engagement_alignment.md`
   - Executive question
   - Scope and non-scope
   - Stakeholder map
   - Kickoff questions
   - Definition of a successful final decision
2. `W1_issue_tree.md`
   - Prioritized questions
   - Initial hypotheses
   - Evidence requirements
3. `W1_external_evidence_brief.md` — maximum two pages
   - Relevant JPMorgan benchmarks and cases
   - Application to ACG
   - Limitations and unsafe generalizations
4. `W1_data_quality_report.md`
   - Reconciliation results
   - Data limitations
   - Proposed treatment
   - Decision impact
5. Updated workplan, source log, assumptions register, risk register, and analysis log
6. `W1_weekly_update.md`

## Expected outcome

You can explain the engagement in 60 seconds, defend the analyses you selected, cite the JPMorgan evidence accurately, and state which client questions the data can and cannot answer.

## Manager challenge

> If you could answer only three questions during this project, which three would determine the recommendation—and which data issue could reverse it?

---

# Week 2 — Complete the current-state diagnostic

## Your objective

Quantify the most important account, liquidity, payment, process, and operating-model problems; identify root causes; and synthesize them into a coherent diagnostic.

## Recommended activity sequence

### Activity 1 — Diagnose account fragmentation

1. Analyze accounts by region, entity, bank, currency, purpose, age, visibility method, and status.
2. Define transparent criteria for a closure-validation candidate.
3. Identify overlapping accounts and low-activity or dormant patterns.
4. Estimate directly observable annual fees associated with candidate accounts.
5. Build a rationalization decision tree that protects regulatory, tax, collection, payroll, and resilience needs.

### Activity 2 — Assess cash visibility and liquidity

1. Convert local balances to USD using the supplied project FX rates.
2. Define same-day visibility and calculate it by region, source method, and date.
3. Distinguish ledger, available, restricted, operationally required, and preliminarily mobilizable balances.
4. Identify simultaneous positive and negative positions across accounts and entities.
5. Develop at least two liquidity thresholds and test sensitivity.
6. Document the legal, tax, regulatory, operational, and timing validation needed before moving cash.

### Activity 3 — Diagnose payment operations

1. Profile payment volume and value by type, region, currency, and cross-border status.
2. Calculate manual-touch, exception, rejection, and late-release rates.
3. Segment exceptions to locate material concentrations.
4. Estimate repair capacity using repair minutes; keep capacity separate from cashable cost reduction.
5. Compare results with stakeholder statements.
6. Build a root-cause tree across upstream data, process, policy, system, and user behavior.

### Activity 4 — Map the current operating model

1. Map cash-positioning and payment processes from trigger to completion.
2. Show roles across Group Treasury, regional finance, shared services, IT, business units, and controls.
3. Identify handoffs, rework loops, control points, system boundaries, and unclear ownership.
4. Estimate monthly manual effort using `process_activity.csv`.
5. Separate required control activity from avoidable process waste.

### Activity 5 — Complete the maturity assessment and synthesis

1. Define a 1–5 maturity scale with observable criteria.
2. Score strategy and governance, organization, process, technology, data, controls, and performance management.
3. Attach evidence and confidence to every score.
4. Define a realistic 18-month target state.
5. Select the four to six findings most material to the CFO's decision.
6. State each finding as fact, magnitude, implication, root cause, confidence, and potential action.

## Week 2 assignment — Current-State Diagnostic Pack

Submit:

1. `W2_diagnostic_report.md` — maximum eight pages
   - Executive diagnostic summary
   - Account-footprint analysis
   - Liquidity and visibility analysis
   - Payment-operations analysis
   - Process and operating-model analysis
   - Maturity assessment
   - Root causes and management implications
2. Reproducible processed datasets and analysis code
3. Current-state process map and draft RACI
4. Treasury maturity heatmap
5. Five-slide diagnostic checkpoint deck
6. Updated findings, assumptions, risk, source, and analysis logs
7. `W2_weekly_update.md`

## Expected outcome

You can distinguish symptoms from root causes, reconcile every material number, explain uncertainty, and tell the Treasurer which problems matter most to the transformation decision.

## Client checkpoint

Present what you know, what you believe, and what remains unresolved. Seek agreement on the diagnosis—not approval for a predetermined solution.

## Manager challenge

> What portion of the liquidity opportunity is observed, what portion is apparently available, and what portion has actually been validated for movement?

---

# Week 3 — Develop and quantify the recommendation

## Your objective

Translate the diagnosis into design principles, genuinely different strategic options, a future-state operating model, and a business case that remains credible under challenge.

## Recommended activity sequence

### Activity 1 — Confirm the diagnostic narrative

1. Update the findings log using fact–implication–action logic.
2. Test each priority finding for contradictory evidence and alternative explanations.
3. Create an executive narrative: situation, complication, findings, and decisions required.
4. Define unresolved questions that affect solution design.

### Activity 2 — Define future-state design principles

1. Draft six to eight principles covering client service, visibility, local autonomy, standardization, control, resilience, data ownership, integration, and scalability.
2. Identify tensions between principles and define how tradeoffs will be resolved.
3. Validate each principle against stakeholder concerns.
4. Define an observable measure for each principle.

### Activity 3 — Develop and evaluate strategic options

1. Define at least three coherent options, such as local stabilization, a federated regional model, and a globally coordinated model.
2. Specify organization, governance, process, data, technology, control, and service implications for each.
3. Define evaluation criteria and weights before scoring.
4. Score options with evidence and test sensitivity to alternative weights.
5. State what each option deliberately does not solve.

### Activity 4 — Design the future-state operating model

1. Design future-state daily cash positioning and payment execution.
2. Allocate global, regional, and local responsibilities.
3. Define data ownership, system-of-record expectations, controls, emergency procedures, and service levels.
4. Draft the future-state RACI.
5. Map capabilities to root causes and design principles.
6. Identify decisions requiring legal, tax, regulatory, cybersecurity, or architecture review.

### Activity 5 — Build and challenge the business case

1. Establish baselines for fees, repair effort, manual capacity, deficit positions, and apparent idle liquidity.
2. Separate cash release, annual P&L, capacity, and risk benefits.
3. Build conservative, base, and upside scenarios.
4. Add implementation timing, ramp, one-time cost, recurring cost, and dependencies.
5. Run sensitivities on the most material assumptions.
6. Assign a client owner and validation action to every benefit line.
7. Document benefits you chose not to quantify.

## Week 3 assignment — Strategy and Business-Case Pack

Submit:

1. `W3_interim_steering_deck` — maximum ten slides
2. `W3_design_principles.md`
3. `W3_strategic_options.md` with weighted matrix and sensitivity analysis
4. `W3_future_state_operating_model.md`
5. Future-state process map, RACI, and control inventory
6. `W3_business_case.md` and reproducible model
7. Assumptions and sensitivity table
8. Updated decision, findings, risk, and analysis logs
9. Written answers to the five hardest anticipated CFO questions
10. `W3_weekly_update.md`

## Expected outcome

The recommendation emerges from transparent choices, is specific enough to operate, and remains defensible when key benefit assumptions are reduced.

## CFO checkpoint

Seek alignment on the preferred strategic direction and the conditions required for final approval. Be prepared to explain when your preferred option would no longer be preferred.

## Manager challenge

> Assume only half the account candidates can close, only one-third of identified capacity is realized, and mobilizable cash is 40% below the base case. Does your recommendation still stand?

---

# Week 4 — Convert the answer into an executable plan

## Your objective

Translate the recommendation into a prioritized roadmap, governance model, KPI framework, executive decision package, and professional project handoff.

## Recommended activity sequence

### Activity 1 — Prioritize initiatives and build the roadmap

1. Define initiatives with a measurable outcome, owner, scope, prerequisites, and completion evidence.
2. Prioritize using value, feasibility, risk reduction, dependency, and speed to impact.
3. Sequence mobilization, Wave 1, Wave 2, and later decisions.
4. Identify quick wins without labeling unfinished foundational work as a quick win.
5. Define stage gates and exit criteria.
6. Draft a 30/60/90-day mobilization plan and a 12–18 month roadmap.

### Activity 2 — Design governance, risk, and performance management

1. Design steering, program, workstream, and business-as-usual governance.
2. Complete the recommendation risk register with likelihood, impact, mitigation, trigger, and owner.
3. Define leading and lagging KPIs across value, operations, adoption, data, control, and client service.
4. Write each KPI's definition, formula, source, frequency, owner, baseline, and target logic.
5. Define benefit validation and change control.

### Activity 3 — Produce and rehearse the executive answer

1. Build the final deck using the storyboard template.
2. Write the six-page maximum recommendation memo.
3. Move supporting analysis into a disciplined appendix.
4. Run the quality gate in `CONSULTING_STANDARDS.md` on every core slide.
5. Rehearse a 15-minute presentation and 15-minute Q&A.
6. Ask a reviewer to challenge the weakest assumption, strongest counterargument, and most difficult implementation risk.
7. Finalize all project documentation.

### Activity 4 — Defend the recommendation and close

1. Deliver the steering-committee presentation.
2. Answer questions directly and distinguish facts, assumptions, and judgments.
3. Record decisions, conditions, unresolved items, owners, and deadlines.
4. Update the recommendation and roadmap where the committee decision requires it.
5. Deliver the final evidence pack and personal reflection.

## Week 4 assignment — Final Executive Pack

Submit:

1. Final executive deck — no more than 15 core slides plus appendix
2. Final recommendation memo — no more than six pages
3. Final analytical files and documented code
4. 12–18 month implementation roadmap and 30/60/90-day plan
5. Initiative charters, future-state RACI, and governance model
6. KPI dictionary and benefits-tracking dashboard
7. Final risk, assumption, decision, findings, source, and analysis logs
8. Q&A preparation log
9. Personal reflection
10. `W4_weekly_update.md`

## Expected outcome

The steering committee can state the decision, rationale, conditions, first 90-day actions, ownership, and measures of success. Your work remains understandable, reproducible, and usable after project close.

## Reflection questions

1. Which initial hypothesis changed most, and why?
2. Which analysis most influenced the recommendation?
3. Where did you have to balance value, risk, feasibility, and control?
4. Which claim remains least certain?
5. What would you do next with additional client access?
6. What consulting behavior will you carry into your next project?

---

## Recommended final deck storyline

1. Decision required and executive recommendation
2. Why ACG must act now
3. Diagnostic summary
4. Account-footprint finding
5. Liquidity and visibility finding
6. Payment-operations finding
7. Root causes and maturity gaps
8. Future-state design principles
9. Options considered and decision logic
10. Recommended operating model
11. Initiative portfolio
12. Business case and sensitivities
13. 12–18 month roadmap
14. Risks, controls, and governance
15. Decisions and next 90 days

Your appendix should contain definitions, data quality, methodology, detailed analyses, source register, assumptions, sensitivities, and rejected alternatives.

