# Consulting Standards and Ways of Working

## 1. Think in decisions, not topics

Weak work says, “I analyzed bank accounts.” Strong work says, “Management should validate closure of a defined account cohort because those accounts add cost and control complexity while contributing little operational value.”

Every analysis must connect to a client decision.

## 2. Maintain a single source of truth

Required working documents:

- `workplan.md`: tasks, owners, dates, dependencies, status
- `issue_tree.md`: questions and hypotheses
- `source_log.csv`: external evidence and limitations
- `analysis_log.md`: transformations, definitions, tests, and file versions
- `findings_log.md`: fact–implication–action chain
- `decision_log.md`: decisions, rationale, owner, and date
- `risk_register.csv`: delivery and recommendation risks
- `assumptions_register.csv`: assumptions, sensitivity, and validation owner

Templates are provided under `templates/`. Update them throughout the engagement, not retrospectively during the final week.

## 3. Apply the evidence ladder

Rank evidence from strongest to weakest:

1. Reconciled client data with reproducible calculation
2. Corroborated evidence from multiple client sources
3. Direct process observation or controlled test
4. Single stakeholder statement
5. External benchmark with relevant methodology
6. Analyst assumption or analogy

Recommendations can use weaker evidence, but uncertainty must be visible.

## 4. Use the fact–implication–action chain

- **Fact:** What the evidence directly supports.
- **Implication:** Why it matters to the executive question.
- **Action:** What management should do as a result.

Do not jump from an interesting chart to a recommendation without the implication.

## 5. Make analysis reproducible

- Keep raw data unchanged.
- Write processed outputs to `data/processed/`.
- Use explicit definitions for every KPI.
- Reconcile totals before segmentation.
- Record exclusions and missing values.
- Test at least one alternative definition for material metrics.
- Use versioned output names or version control.
- Never manually overwrite a calculated number in a presentation.

## 6. Distinguish four types of value

| Value type | Example | Minimum evidence |
|---|---|---|
| Cash release | Mobilizing demonstrably available surplus | Balance analysis plus legal/operational validation assumption |
| P&L benefit | Lower fees or interest expense | Baseline, rate/price assumption, timing, and owner |
| Capacity benefit | Fewer manual hours | Activity volume × time × realistic removal rate; do not automatically call this headcount reduction |
| Risk reduction | Fewer late or uncontrolled payments | Control gap, exposure pathway, mitigation, and leading indicator |

Never add cash release, annual P&L, and avoided risk into one “total benefit” number.

## 7. Communicate like a consultant

- Use answer-first slide titles that state the conclusion.
- One slide should have one governing message.
- Label axes, units, periods, filters, and sample size.
- Show sources and definitions in readable footnotes.
- Round consistently and avoid false precision.
- Use charts only when they improve the decision.
- Write recommendations with an owner, action, timing, and outcome.
- Prepare for the strongest counterargument, not only supportive questions.

## 8. Respect professional and ethical boundaries

- Never invent a JPMorgan quote, benchmark, client outcome, or product capability.
- Do not provide legal, tax, regulatory, investment, or accounting advice.
- Treat public case studies as marketing evidence with appropriate limitations.
- Do not recommend centralization without addressing resilience, local requirements, access control, and emergency procedures.
- Do not describe a balance as “available” solely because it is positive.

## 9. Minimum quality gate before any client review

- The question being answered is explicit.
- Numbers reconcile to the agreed baseline.
- Units and time periods are consistent.
- Material assumptions are visible.
- Source links work and claims match the source.
- The implication is stated.
- At least one alternative explanation was considered.
- Confidential, client, analyst, and public-source labels are correct.
- The reviewer can reproduce the calculation.
