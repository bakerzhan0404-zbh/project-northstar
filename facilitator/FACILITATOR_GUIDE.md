# Facilitator Guide — Keep Separate from the Learner Pack

## Purpose

This guide helps the mentor run Project Northstar as an apprenticeship rather than a take-home assignment. The facilitator should challenge Baker's reasoning, introduce realistic client developments, and avoid giving away a single “correct” solution.

## Recommended package release

Give Baker access initially to:

- `WELCOME_BAKER.md`
- `README.md`
- `program/`
- `client/`
- `references/`
- `src/`
- `templates/`
- `data/` after Baker runs the generator

Keep `facilitator/` private until the program is complete.

## Coaching cadence

| Session | Timing | Length | Facilitator role |
|---|---|---:|---|
| Kickoff | Start of Week 1 | 30 min | Role-play CFO/Treasurer; clarify scope without solving it |
| Week 1 review | End of Week 1 | 40 min | Challenge hypotheses, sources, and data readiness |
| Week 2 diagnostic review | End of Week 2 | 45 min | Test reconciliation, root causes, and implications |
| Week 3 interim steering | End of Week 3 | 45 min | Challenge choices, operating model, and business case |
| Final rehearsal | During Week 4 | 40 min | Challenge narrative and Q&A; do not rewrite the deck |
| Steering committee | End of Week 4 | 45 min | Make and document the executive decision |

## Indicative planted signals

These are quality-control anchors, not answer keys. Baker may define metrics differently if the definition is defensible.

- The generated footprint contains 16 entities, 55 accounts, 13 countries, 10 currencies, and five banking providers.
- Four legacy accounts are dormant, with approximately $7,800 in directly observable annual fees. Account closure still requires local validation.
- Approximately 58% of balance observations arrive on the same date; because of account mix, the positive-balance-weighted same-day visibility level is around 55% under a simple definition.
- Spreadsheet balances arrive roughly 2.2 days late on average; portal balances arrive one day late in the generated data.
- Positive and negative account positions coexist throughout the period. The average gross positive position is approximately $62 million and the average negative position approximately $2.1 million, but neither figure is automatically mobilizable or avoidable.
- Approximately 31.5% of payments have a manual touch, 6.3% generate an exception, and 5.0% are released late.
- Exception incidence is materially higher for manual-touch payments than non-manual payments, and for cross-border payments than domestic payments. Baker should avoid claiming causality from this descriptive relationship.
- Recorded payment repair effort totals approximately 335 hours over six months.
- The process-activity file implies approximately 618 manual hours per month and about $427,000 in annual modeled labor capacity. This is not automatically a cashable headcount benefit.

## What a strong recommendation may look like

A defensible answer will often favor a **federated transformation**: centralized visibility, policy, data standards, and selected liquidity decisions; standardized payment intake and controls; regional/local execution retained where justified; staged integration around existing ERPs; and account rationalization after regulatory and operational validation.

This is not mandatory. A different choice can score highly if Baker:

- Uses explicit criteria
- Addresses the CFO's 12-month benefit requirement
- Respects local and resilience constraints
- Separates foundational work from later technology decisions
- Shows how the recommendation remains valuable under downside sensitivities

## Red flags to challenge

- Calling all positive cash “idle” or “releasable”
- Recommending global pooling without legal, tax, currency, and market validation
- Treating a public JPMorgan case study as proof of ACG benefit
- Converting all process capacity into headcount savings
- Starting with a product or platform rather than the operating problem
- Scoring maturity without observable criteria or evidence
- Using weighted option scores to disguise subjective assumptions
- Hiding low-confidence numbers in appendix footnotes
- Proposing centralization without outage, emergency-payment, access, and segregation-of-duties design
- Reporting correlations as causes

## How to give feedback

Use questions before answers:

1. “What evidence supports that statement?”
2. “What else could explain the pattern?”
3. “Which decision changes because of this?”
4. “What assumption drives the range?”
5. “Who must validate this before implementation?”
6. “What is the strongest argument against your recommendation?”
7. “How would you know within 90 days that the plan is failing?”

## Final steering-committee roles

- **CFO:** Focus on value, pace, funding, and confidence.
- **Treasurer:** Focus on visibility, liquidity, and operating practicality.
- **Regional Controller:** Challenge centralization and assumptions about locally available cash.
- **CIO:** Challenge data ownership, integration sequence, security, and resilience.
- **Internal Audit:** Challenge controls, access, emergency processes, and concentration risk.

The committee should provide a conditional decision, such as approval of a 90-day mobilization subject to validation of legal account requirements, liquidity availability, technical architecture, and the benefit baseline.

## Scoring

Use `program/EVALUATION_RUBRIC.md`. Score the submitted work before the final presentation, then adjust only the communication component and any evidence corrected during Q&A. Provide written feedback with:

- Two demonstrated strengths
- Two decision-relevant gaps
- One technical skill to develop
- One consulting behavior to practice
- One specific next assignment
