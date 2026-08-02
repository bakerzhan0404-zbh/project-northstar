# Project Northstar

## Global Treasury Transformation — One-Month JPM PTA Project

Welcome to Project Northstar, your one-month JPM PTA consulting project. You will join a J.P. Morgan Payments Advisory engagement and advise **Aurelius Consumer Group (ACG)**, a multinational consumer-products company whose treasury infrastructure has not kept pace with its growth.

The assignment is to diagnose ACG's fragmented cash-management environment, quantify the opportunity, design a future-state treasury operating model, and defend a phased transformation roadmap before the client steering committee.

## What you will learn

- Structure an ambiguous executive problem using hypotheses and an issue tree.
- Convert transaction and account data into decision-relevant insights.
- Assess treasury maturity across people, process, technology, data, and controls.
- Size liquidity, efficiency, and risk opportunities without overstating precision.
- Evaluate strategic options using explicit criteria and traceable evidence.
- Build a recommendation, business case, implementation roadmap, and KPI framework.
- Produce consulting-grade documentation and communicate with senior stakeholders.

## Start here

1. Follow [`GETTING_STARTED.md`](GETTING_STARTED.md) to set up your repository.
2. Read [`WELCOME_BAKER.md`](WELCOME_BAKER.md).
3. Read [`program/ENGAGEMENT_CHARTER.md`](program/ENGAGEMENT_CHARTER.md).
4. Read [`client/CLIENT_BRIEF.md`](client/CLIENT_BRIEF.md) and [`client/STAKEHOLDER_PACK.md`](client/STAKEHOLDER_PACK.md).
5. Follow [`program/ONE_MONTH_PLAYBOOK.md`](program/ONE_MONTH_PLAYBOOK.md) and submit one integrated assignment each week.
6. Use [`program/CONSULTING_STANDARDS.md`](program/CONSULTING_STANDARDS.md) for quality expectations.

## Repository map

```text
client/        Client brief, stakeholder evidence, and data dictionary
data/          Generated client case data and starter outputs
deliverables/  Your working and final deliverables
facilitator/   Mentor-only guidance and indicative findings
program/       Charter, daily plan, standards, and evaluation rubric
references/    JPMorgan public-source register and evidence rules
src/           Reproducible data generator and starter analysis
templates/     Consulting documentation templates
tests/         Lightweight data-quality checks
```

## Required final submission

You must submit:

1. An executive presentation of no more than 15 core slides, plus appendix.
2. A concise written recommendation of no more than six pages.
3. A reproducible analytical workbook or Python analysis.
4. A 12–18 month implementation roadmap.
5. A KPI and benefits-tracking framework.
6. A complete evidence pack: workplan, interview notes, source log, analysis log, decision log, and risk register.
7. Four weekly progress updates and a five-minute personal reflection covering what changed in your thinking and what you would do next with additional client access.

## Technology

The seed code requires Python 3.9+ and `pandas`. It deliberately performs setup, validation, and a few descriptive calculations without completing the consulting analysis. You are expected to extend it.

```bash
python3 src/generate_data.py
python3 src/starter_analysis.py
python3 tests/test_data_quality.py
```
