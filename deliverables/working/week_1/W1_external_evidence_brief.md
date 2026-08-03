# Week 1 — External Evidence Brief

**Classification:** Confidential — Project Northstar simulated client material

**Purpose:** use public evidence to refine ACG hypotheses, not select a product or copy a client solution

**Verified:** 2 August 2026; full claim records and limitations are in `W1_source_log.csv`

## Three observations that change the workplan

### 1. Automation presence is not end-to-end automation

**[JPM-PUBLIC — S01](https://www.jpmorgan.com/insights/payments/trends-innovation/payments-outlook-trends-2026).** J.P. Morgan Payments reports that 87% of surveyed organizations have some treasury/payments automation, while 39% describe their systems as mostly or fully automated (ASUG/J.P. Morgan, n=107). Test ACG's workflow from source through reconciliation—not whether an API exists.

**ACG test — ANALYST-CALC A02/A03.** Only 32 of 55 accounts are reported on the balance date; 31.51% of supplied payment records have manual touch. Obtain timestamps, interface coverage, exception handling, and data ownership. The small, SAP-oriented survey is neither a target nor causal proof; it supports testing process/data standards alongside connectivity.

### 2. Growth can create fragmentation, but account count alone proves little

**JPM-PUBLIC — [S02](https://www.jpmorgan.com/insights/treasury/liquidity-management/fortescue-global-treasury-transformation)/[S03](https://www.jpmorgan.com/insights/treasury/liquidity-management/emea-treasury-transformation-ansys).** Fortescue describes growth to 180+ accounts across countries/currencies. Ansys reports rationalizing 80+ accounts across 27 banks and visibility over $550m after acquisition-driven decentralization.

**ACG test — ACG-DATA/ANALYST-JUDGMENT.** Assess activity, purpose, balance behavior, local requirements, dependencies, fees, and closure costs. These sponsor-published stories omit full cost and counterfactuals; they do not support raw account count as a benchmark. Use rules-based closure validation.

### 3. Structured source data and local-market design precede useful automation

**JPM-PUBLIC — [S04](https://www.jpmorgan.com/insights/treasury/treasury-management/mettler-toledo-china-treasury-transformation)/[S05](https://www.jpmorgan.com/insights/treasury/treasury-management/what-is-iso-20022).** J.P. Morgan states structured payment data can support reconciliation and automation; its Mettler-Toledo China case links local design and ERP integration to less manual processing.

**ACG test — ACG-DATA/ANALYST-JUDGMENT.** Obtain exception reasons, field completeness, formats, beneficiary ownership, and local rules. ISO 20022 cannot repair poor source data; a China-specific program may not transfer. Prioritize ownership and intake standards, not an ISO migration.

## Required three-case sample from S06

The required [S06 client-story](https://www.jpmorgan.com/payments/client-stories) sample uses Fortescue, Ansys, and Mettler-Toledo; individual pages are logged as S02–S04.

| Case | Context and intervention | Reported outcome | Evidence strength and ACG relevance |
|---|---|---|---|
| Fortescue | Global growth, 180+ accounts, manual reconciliation; standardized connectivity and liquidity capabilities | Near-real-time visibility across 14 countries and less manual administration | Medium-low: named footprint but sponsor-published. Tests scalable standards; does not establish product fit. |
| Ansys | Acquisition-driven decentralization; EMEA liquidity centralization and host-to-host reporting | 80+ accounts rationalized across 27 banks; visibility over $550m | Medium-low: quantified but no full economics. Supports a regional option subject to ACG constraints. |
| Mettler-Toledo China | Manual documentation/AR reconciliation; local simplification and ERP integration | Processing reportedly fell from 3–4 days to one and one FTE was freed | Medium-low: quantified but market-specific. Reinforces local tailoring and upstream-data discipline. |

## Synthesis and boundaries

Three themes shape Week 2: connectivity depends on standardized data/processes; liquidity design must respect entity/local constraints; and transformation combines governance, controls, operating-model change, and technology. External evidence cannot establish ACG cash movable within 24 hours or ACG-specific economics and risk.

No public solution was copied: the cases differ in industry, scale, jurisdictions, systems, legal structure, and maturity. They are marketing evidence, not controlled comparisons. ACG's recommendation must come from reconciled client evidence, explicit assumptions, tested alternatives, and implementation conditions. Complete citations, publication/access dates, methods, and limitations are in `W1_source_log.csv`.
