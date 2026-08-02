# Week 1 — External Evidence Brief

**Purpose:** use official JPMorgan public material to challenge and refine ACG hypotheses—not to select a product or copy another client's solution.  
**Access/verification date:** 2 August 2026

## Three observations that change the workplan

### 1. Automation presence is not end-to-end automation

J.P. Morgan Payments reports that 87% of surveyed organizations have some treasury/payments automation, while only 39% describe their systems as mostly or fully automated (ASUG/J.P. Morgan, n=107). This supports testing the full ACG workflow rather than counting API or host-to-host connections. ACG already shows the same structural warning: 58.18% of balance observations are same-day, while 41.82% arrive later; 31.51% of payments require manual touch.

**Evidence needed at ACG:** workflow steps from source creation through reconciliation, interface coverage, exception handling, reference-data ownership, and timestamps.  
**Limitation/alternative interpretation:** the survey is small and SAP-oriented; adoption levels are not performance targets and do not prove automation causes better outcomes.  
**Hypothesis effect:** strengthens the hypothesis that process/data standardization must precede or accompany connectivity.

### 2. Scale and acquisition can create fragmentation, but account count alone does not prove inefficiency

The Fortescue public story describes growth to more than 180 accounts across countries and currencies, followed by standardized connectivity and liquidity changes. Ansys describes acquisition-driven decentralization and reports rationalizing more than 80 accounts across 27 banks while improving visibility over $550 million. These cases make structural drivers—entities, markets, currencies, acquisitions, connectivity, and purpose—more relevant than a raw account-count benchmark.

**Evidence needed at ACG:** transaction activity, purpose, balance behavior, local requirements, signatories, service dependencies, fees, and closure costs for each account.  
**Limitation/alternative interpretation:** both are JPMorgan client-success stories and do not disclose counterfactuals, total program cost, full methodology, or unsuccessful elements.  
**Hypothesis effect:** weakens any claim that 55 accounts are inherently excessive; supports a rules-based closure-validation cohort.

### 3. Structured data and local-market design are prerequisites to useful automation

J.P. Morgan's ISO 20022 explainer states that structured, richer payment data can improve reconciliation, integration, screening, and automation; JPMorgan Chase states it went live with ISO 20022 in March 2023. The Mettler-Toledo China story links document-free cross-border processing, ERP integration, and local-market design to shorter processing and less manual work. For ACG, this reinforces Lucas Schneider's claim that incomplete invoice and beneficiary information—not only the bank platform—may drive repair.

**Evidence needed at ACG:** exception reason codes, mandatory-field completeness, payment-format map, beneficiary-master ownership, rejection detail, and local documentation requirements.  
**Limitation/alternative interpretation:** ISO 20022 does not repair poor source data by itself, and the China case may depend on market-specific programs unavailable elsewhere.  
**Hypothesis effect:** prioritizes data ownership and intake standards; does not turn Northstar into an ISO migration project.

## Transformation-case comparison

| Case | Context/problem | Intervention described publicly | Reported outcome | Evidence strength | Relevance and caution for ACG |
|---|---|---|---|---|---|
| Fortescue | Global growth; 180+ accounts; manual reconciliation; cross-border complexity | Standardized connectivity, liquidity, account, FX, and trade capabilities | Near-real-time visibility across 14 countries; less manual administration | Medium-low: named client, concrete footprint, but marketing case with limited methodology | Tests whether ACG needs scalable standards before another acquisition; does not establish product fit |
| Ansys | Acquisition-driven decentralization; small teams; local forecasting | EMEA liquidity centralization, multi-entity/multicurrency structure, host-to-host reporting | 80+ accounts rationalized across 27 banks; visibility over $550m | Medium-low: quantified outcome but no cost or counterfactual | Supports regional option design; ACG must validate restrictions and local service needs first |
| Mettler-Toledo China | Manual documentation, AR reconciliation, time-zone funding constraints | Local cross-border simplification, ERP integration, reference-based reconciliation, on-demand funding | Processing reduced from 3–4 days to one; one FTE reportedly freed; less paper | Medium-low: quantified but market-specific and sponsor-published | Demonstrates local tailoring and upstream data importance; outcomes cannot be transplanted to ACG |

## Repeated themes and evidence gaps

**Themes across sources:** (1) connectivity creates value only when processes and data are standardized; (2) visibility and liquidity design must follow entity and local-market constraints; (3) transformation combines operating-model change, governance, and technology rather than technology alone.

**External evidence remains insufficient on:** (1) the proportion of ACG balances legally and operationally movable within 24 hours; and (2) the cost, timing, control risk, and realized benefit of a comparable transformation under ACG's three-ERP and funding constraints.

## Why no public solution was copied

The cases differ in industry, scale, jurisdictions, systems, legal structure, and starting maturity. They are sponsor-published success stories, not controlled comparisons. Northstar therefore uses them to form questions and option criteria. ACG's recommendation must be derived from reconciled client data, locally validated constraints, explicit assumptions, credible alternatives, and quantified implementation conditions.

## Sources

- [J.P. Morgan Payments, “Payments Outlook: Five Trends Powering Payments in 2026,” 23 Apr. 2026](https://www.jpmorgan.com/insights/payments/trends-innovation/payments-outlook-trends-2026)
- [J.P. Morgan Payments, “Fortescue's Global Treasury Transformation,” 19 Jun. 2026](https://www.jpmorgan.com/insights/treasury/liquidity-management/fortescue-global-treasury-transformation)
- [J.P. Morgan Payments, “Ansys transforms treasury through centralized liquidity solution,” 20 Aug. 2024](https://www.jpmorgan.com/insights/treasury/liquidity-management/emea-treasury-transformation-ansys)
- [J.P. Morgan Payments, “Mettler-Toledo's Treasury Transformation in China,” 22 Jul. 2025](https://www.jpmorgan.com/insights/treasury/treasury-management/mettler-toledo-china-treasury-transformation)
- [J.P. Morgan, “ISO 20022 Migration: The journey to faster payments automation”](https://www.jpmorgan.com/insights/treasury/treasury-management/what-is-iso-20022)
- [J.P. Morgan Payments client stories](https://www.jpmorgan.com/payments/client-stories)

