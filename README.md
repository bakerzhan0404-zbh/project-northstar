# Project Northstar

## My Four-Week Global Treasury Transformation Project

Project Northstar is my four-week J.P. Morgan Payments Advisory consulting project for **Aurelius Consumer Group (ACG)**, a multinational consumer-products company whose treasury infrastructure has not kept pace with its growth.

I am diagnosing ACG's fragmented cash-management environment, quantifying the opportunity, designing a future-state treasury operating model, and preparing a phased transformation roadmap for the client steering committee. Because the evidence is imperfect, I must separate facts from assumptions and make my recommendation traceable.

## What I am doing over four weeks

- **Week 1 — Frame and validate:** I define the executive question, build my issue tree and workplan, establish the evidence base, and test the supplied data.
- **Week 2 — Diagnose:** I assess accounts, liquidity, cash visibility, payments, processes, controls, and treasury maturity to identify the most important root causes.
- **Week 3 — Design and quantify:** I evaluate strategic options, design the future-state operating model, and build a business case with scenarios and sensitivities.
- **Week 4 — Make it executable:** I convert my recommendation into a 12–18 month roadmap, 30/60/90-day plan, governance model, KPIs, and executive decision package.

## What I am building toward

By the end, I will have a decision-ready recommendation that balances value, risk, feasibility, and control. I will be able to explain what the data supports, what still requires client validation, why my chosen model is preferable, and what ACG should do first.

My final submission will include:

1. An executive presentation of no more than 15 core slides, plus appendix.
2. A concise recommendation memo of no more than six pages.
3. A reproducible analytical workbook or Python analysis.
4. A 12–18 month implementation roadmap and 30/60/90-day plan.
5. A KPI and benefits-tracking framework.
6. A complete evidence pack covering my workplan, sources, assumptions, analysis, decisions, findings, and risks.
7. Four weekly updates and a reflection on how my thinking changed.

## Live diagnostic dashboard

**https://bakerzhan0404-zbh.github.io/project-northstar/dashboard/**

An interactive Week 1–2 diagnostic dashboard covering cash visibility, liquidity screening, bank-account footprint, payment operations, process workload, and data-quality evidence. Published by GitHub Pages from [`docs/dashboard/`](docs/dashboard/); see its [README](docs/dashboard/README.md) for the interaction model, evidence boundaries, and refresh steps. It is a governed snapshot of supplied data for 1 January–30 June 2026, not a live operational system.

## How I use this repository

I begin with [`GETTING_STARTED.md`](GETTING_STARTED.md), [`WELCOME_BAKER.md`](WELCOME_BAKER.md), and the [`program/ONE_MONTH_PLAYBOOK.md`](program/ONE_MONTH_PLAYBOOK.md). The client materials define the case, while the program and templates guide my work.

```text
client/        Client brief, stakeholder evidence, and data dictionary
data/          Generated client case data and my processed outputs
deliverables/  My working files and final deliverables
docs/          The published GitHub Pages site (interactive dashboard)
facilitator/   Mentor guidance and indicative findings
program/       Charter, four-week playbook, standards, and evaluation rubric
references/    JPMorgan public sources and evidence rules
src/           Reproducible data generation and analysis code
templates/     Consulting documentation templates I use throughout the project
tests/         Lightweight data-quality checks
```

## Technology

I use Python 3.9+ and `pandas` to validate and analyze the case data, extending the starter code as my work develops.

```bash
python3 src/generate_data.py
python3 src/starter_analysis.py
python3 tests/test_data_quality.py
```
