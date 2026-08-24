# Week 4 — Analysis and Build Log

**Prepared by:** Baker · **Date:** 24 August 2026

| ID | Analysis / build | Inputs | Method | Key result | Limitation | Output |
|---|---|---|---|---|---|---|
| A21 | Initiative portfolio | W2 findings; W3 principles/options/controls/charters | Seven initiatives scored 1–5 on locked value 30%, risk 25%, feasibility 20%, dependency 15%, speed 10%; score ×20 | I01 94; I07 92; I06 86; I03 85; I02 83; I05 80; I04 63 | Scores are analyst judgment, not readiness or value | `W4_initiative_portfolio.csv` |
| A22 | Stage-gate design | Client constraints; W3 open gates and fallback | Defined G0–G6 with minimum exit evidence, owner, and allowed decision | Day 90 is stop/extend/bounded-pilot; G4 is separate production/funding gate | Thresholds and owners require client approval | `W4_stage_gates.csv` |
| A23 | Roadmap sequencing | A21, A22, NA freeze, ERP constraint | Dependency sequence from mobilization through BAU | Six phases: 0–30, 31–60, 61–90, M4–6, M7–12, M13–18 | Dates move with gate closure; Month 5 NA floor is planning assumption | `W4_roadmap_milestones.csv` |
| A24 | KPI dictionary | W2 baselines; W3 controls/value gates | Defined 14 KPIs with formula, unit, baseline, boundary, target logic, frequency, source, owner, leading/lagging | Covers data, liquidity, operations, service, adoption, control, resilience, economics | Several baselines/targets require G1–G3 evidence | `W4_kpi_dictionary.csv` |
| A25 | Benefits tracker | W3 scenarios/value ledger/VG gates | Preserved four non-additive categories and zero validated/funded/recognized status | Cash screen 35m, fees 7,800/year, capacity 150h/month remain diagnostic; risk not quantified | No ROI/NPV/payback | `W4_benefits_tracker.csv` |
| A26 | Source-baseline control | W2 visibility/payment/account outputs; W3 costs | Python assertions for material baselines | 58.18%; 2,534 delayed; 31.51%; 6.30%; 5.00%; 4 candidates/$7,800; base costs 1.155m/281k | Validates supplied/project outputs, not client operational evidence | `src/week4_implementation.py` |
| A27 | Fail-closed Week 4 model | A21–A26 | Contract tests; unsafe recognized-value and closed-gate mutations must fail | Implementation tests pass | Test pass does not close client evidence | `tests/test_week4_implementation.py` |
| A28 | Final narrative integration | Weeks 1–4 evidence | Decision → evidence → choice → economics → execution loop | 90-day mobilization is exact final ask | Client has not approved recommendation | Final memo/deck/roadmap |
| A29 | Executive deck build and visual QA | Final evidence register; Week 2/3 house-style design system | Rebuilt all 18 slides from `src/week4_final_deck.py`, importing the tokens and components of `src/week3_steering_deck.py`; panel heights sized to row counts; overflow checked analytically across every panel and confirmed by rendered inspection | 18/18 slides rendered; 0 of 14 panels overflow; house style matches the Week 2 checkpoint and Week 3 interim decks | Visual consistency does not validate client evidence or approve execution | `src/week4_final_deck.py` and final PPTX/PDF |
| A30 | Final-pack completeness | Final and Week 4 indexes, executive files, working controls | Fail-closed required-file, decision-boundary, and placeholder checks plus full regression run | Final pack test passes; all 12 executable Python/JavaScript control suites pass (one UI test intentionally skipped) | Repository checks do not replace client acceptance | `tests/test_week4_executive_pack.py` |

## Rebuild

```bash
python3 src/week4_implementation.py
python3 tests/test_week4_implementation.py
python3 tests/test_week4_executive_pack.py
```

## Evidence boundary

The Week 4 model validates calculation and documentation contracts. It does not authorize production, spend, cash movement, closure, labor action, benefit recognition, or scale, and it does not close VG01–VG12 or CR01–CR10.
