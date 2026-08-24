# Project Northstar — Final Executive Deck

**Prepared by:** Baker
**Date:** 24 August 2026
**Audience:** CFO-led Steering Committee
**Format:** 18 slides total — 15 core slides (the rubric cap) plus a 3-slide appendix
**Decision boundary:** Direction and 90-day evidence mobilization only; no production, funding, cash, closure, labor, benefit, or scale approval

This file is the human-readable source and speaker-note companion to the editable PowerPoint and PDF. The shipped `.pptx` and `.pdf` are built by `src/week4_final_deck.py`, which reuses the Week 2/3 house-style design system in `src/week3_steering_deck.py`. Rebuild with `python3 src/week4_final_deck.py`, then export the PDF with LibreOffice. The `decks/northstar-final/` workspace records the superseded first build and is no longer the build path.

## Core deck

### 1. Authorize 90 days to make the next treasury decision

Authorize a federated coordination direction with a local-stabilization fallback. Do not authorize production or funding. The Day-90 return is a separate `stop / extend / bounded-pilot` decision.

### 2. ACG has enough evidence to choose a direction—not enough to approve value or production

- Same-day calendar proxy: **58.18%** across 9,955 account-days.
- Supplied payment-exception rate: **6.30%** across 7,600 records.
- Weighted option score: **87 federated / 72 local / 60 global**.
- Recognized cash, P&L, and capacity value today: **$0**.

Speaker note: model-control passes and supplied-data calculations are not execution evidence.

### 3. Four linked failures explain ACG's treasury problem

Daily visibility, liquidity decisions, payment operations, and the operating model all point to incomplete ownership, evidence, controls, and service design. The recommendation must address them together.

### 4. Portal and spreadsheet sources explain every delayed account-day in the supplied pattern

Automated API and host-to-host sources are same-day under the calendar proxy; 23 manual-source accounts explain the supplied delayed pattern. This is a reporting-date proxy, not a proof of intraday completeness or cause.

### 5. The liquidity analysis defines a certification agenda—not a cash-release claim

Across 168 complete 14-day windows, the `$21m` screen passes 168, the `$35m` screen passes 138, and the `$46.2m` screen passes none. Recognized movable cash remains `$0` until VG01–VG05 close.

### 6. Payment friction is material enough to diagnose—and too weakly evidenced to automate broadly

The supplied extract shows **31.51% manual touch**, **6.30% exceptions**, **5.00% late release**, and **10.34% cross-border**. These are associations; the 120-record source-linked sample must establish causes and controls.

### 7. The root causes sit upstream of the visible symptoms

Ownership is split; core data lineage is incomplete; process/service practices vary; and access, SoD, audit, reconciliation, resilience, and staged integration require explicit design and testing.

### 8. Eight design principles resolve enterprise control versus local responsiveness

Use an enterprise standards spine, certified local context, control by design, and staged/reversible change. Any failed critical gate blocks the affected decision value and cannot be averaged away.

### 9. Federated coordination offers the best balance with a local fallback

Federated coordination scores 87 and leads all five plausible weight sensitivities. Local stabilization remains the switch path if ownership, integration readiness, affordability, or any critical control/service/local-right/resilience condition fails.

### 10. The target model centralizes standards and evidence—not every operational decision

Global Treasury owns policy, data contracts, daily-position and mobility standards. CIO owns staged integration, access, auditability, cyber, and resilience. Finance owns cost and benefit governance. Regions and business units retain certified local, critical-payment, and emergency rights.

### 11. Seven initiatives start with data, governance, and value control—not platform procurement

Priority scores: cash data and visibility 94; benefits/cost/KPI assurance 92; governance/service/adoption 86; payment controls/exceptions 85; liquidity certification 83; integration/access/resilience 80; account rationalization 63.

### 12. The business case stays credible by keeping unlike value types separate

Cash release, annual P&L, productive capacity, and risk reduction use separate ledgers and recognition gates. Planning cost is `$755k / $1.155m / $1.715m` one-time and `$175k / $281k / $442k` recurring; these are analyst assumptions, not quotes or authority.

### 13. Use 90 days to earn a bounded test before scaling

- Day 0–30: own the facts.
- Day 31–60: prove conditions.
- Day 61–90: make ready and return for G3.
- Months 4–6: Wave 1 only after separate approval.
- Months 7–18: expand only while evidence holds.

### 14. Governance converts the roadmap into stop, switch, and scale decisions

Unowned data, uncertified cash, service/control/rollback failure, absent affordability evidence, or value-formula drift triggers narrowing, suspension, redesign, rollback, or the local fallback. Critical risk cannot be averaged away.

### 15. Approve the direction and owners; return at Day 90

Five commitments: confirm direction/fallback/boundary at Day 0; accept functional owners and contracts by Day 30; close exact North America freeze dates/sign-off path by Day 30; produce bottom-up cost evidence by Day 60; and take a separate G3 decision at Day 90.

## Appendix

### 16. Definitions, data quality, and methods bound every metric

Defines the visibility, liquidity, payment, account, and capacity methods alongside the supplied-population limitations that prevent proxy rates, positive balances, associations, candidates, or estimated hours from being overstated.

### 17. Detailed analyses, sensitivities, and rejected alternatives support the choice

Shows the option-weight sensitivities, liquidity thresholds, account and capacity cases, and cost range. It also records why immediate global coordination, indefinite local-only remediation, bulk closure, automatic payment automation, and premature labor/value claims were rejected.

### 18. Source and assumption controls keep claims auditable

Separates `PROGRAM-STANDARD`, `ACG-DATA`, `ANALYST-CALC`, `ANALYST-ASSUMPTION`, `ANALYST-JUDGMENT`, and `JPM-PUBLIC`; points to the final source and assumptions registers; and records the rebuild path through documented outputs and fail-closed tests.

## Provenance

Primary evidence: Week 1 data-quality outputs; Week 2 visibility, liquidity, payment, process, RACI, maturity, and dashboard outputs; Week 3 option, sensitivity, operating-model, business-case, and pilot-control outputs; Week 4 initiative, gate, roadmap, KPI, benefits, risk, decision, and evidence records. Full traceability is in `Northstar_Final_Evidence_Register.md`.
