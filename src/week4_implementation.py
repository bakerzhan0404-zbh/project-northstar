"""Reproducible Week 4 implementation controls for Project Northstar.

The model converts the conditional Week 3 recommendation into an executable
portfolio, stage-gate roadmap, KPI dictionary, and benefits ledger.  It does
not promote diagnostic quantities into benefits: validated, funded, and
recognized value remain zero until the named evidence gates close.
"""

from pathlib import Path
from typing import Dict, List

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
MODEL_VERSION = "W4-EXECUTION-PLAN-v1 · 2026-08-24"

EVIDENCE_BOUNDARY = (
    "ANALYST-JUDGMENT implementation design; no production change, cash "
    "movement, account closure, labor action, spend, or benefit recognition"
)

WEIGHTS = {
    "value": 0.30,
    "risk_reduction": 0.25,
    "feasibility": 0.20,
    "dependency": 0.15,
    "speed": 0.10,
}

INITIATIVES: List[Dict[str, object]] = [
    {
        "initiative_id": "I01",
        "initiative_name": "Cash data and visibility foundation",
        "outcome": "A governed daily position for all 55 supplied accounts with source, timestamp, balance type, owner, reconciliation, and exception lineage.",
        "accountable_owner": "Group Treasurer",
        "delivery_lead": "Treasury Data Lead / CIO delegate",
        "start": "Day 1",
        "target_finish": "Month 6",
        "wave": "Mobilization → Wave 1",
        "prerequisites": "G0 evidence-mobilization authority; named account, source, data, and CIO owners; access to the 55-account/source inventory",
        "value_score_1_to_5": 5,
        "risk_reduction_score_1_to_5": 5,
        "feasibility_score_1_to_5": 4,
        "dependency_score_1_to_5": 5,
        "speed_score_1_to_5": 4,
        "required_gates": "G0; G1; G2; G3; G4",
        "completion_evidence": "Approved metric contract; 55-account census; reconciled daily run; owned exception log; control and rollback approval",
        "value_boundary": "Enables later cash decisions; no cash benefit recognized from visibility alone",
    },
    {
        "initiative_id": "I02",
        "initiative_name": "Liquidity certification and funding discipline",
        "outcome": "Account-level mobility, buffer, legal/tax, service, and funding-action evidence supports controlled decisions without labeling positive cash as movable.",
        "accountable_owner": "Group Treasurer",
        "delivery_lead": "Regional Treasury Leads",
        "start": "Day 31",
        "target_finish": "Month 12",
        "wave": "Mobilization → Wave 2",
        "prerequisites": "I01 reconciled population and source contract; named regional, legal, tax, regulatory, service, and Finance validators; G1 approval",
        "value_score_1_to_5": 5,
        "risk_reduction_score_1_to_5": 5,
        "feasibility_score_1_to_5": 3,
        "dependency_score_1_to_5": 4,
        "speed_score_1_to_5": 2,
        "required_gates": "G1; G2; G3; G4; G5",
        "completion_evidence": "Current certification register; approved buffers; complete decision evidence; controlled transfer or documented no-action decisions; Finance validation",
        "value_boundary": "$21m/$35m/$46.2m remain screens until VG01–VG05 close",
    },
    {
        "initiative_id": "I03",
        "initiative_name": "Payment intake, controls, and exception reduction",
        "outcome": "A controlled payment population, standard intake fields, reason-coded exceptions, service protections, and a bounded production test reduce avoidable rework without weakening controls.",
        "accountable_owner": "Shared Services Lead",
        "delivery_lead": "Payment Operations Lead",
        "start": "Day 1",
        "target_finish": "Month 9",
        "wave": "Mobilization → Wave 1",
        "prerequisites": "Controlled payment denominator and event/source access; named process and control owners; critical-payment rules and exact North America freeze calendar",
        "value_score_1_to_5": 4,
        "risk_reduction_score_1_to_5": 5,
        "feasibility_score_1_to_5": 4,
        "dependency_score_1_to_5": 4,
        "speed_score_1_to_5": 4,
        "required_gates": "G0; G1; G2; G3; G4; G5",
        "completion_evidence": "Reconciled payment denominator; completed 120-record review; approved cause/intervention; SoD/access/service evidence; like-for-like pilot readout",
        "value_boundary": "7,600-record extract is not certified enterprise performance; capacity stays in hours until VG08–VG10 close",
    },
    {
        "initiative_id": "I04",
        "initiative_name": "Account rationalization validation",
        "outcome": "Every closure candidate has locally certified purpose, dependencies, controls, closure cost, continuity plan, and verified fee removal before closure.",
        "accountable_owner": "Group Treasurer",
        "delivery_lead": "Regional Finance",
        "start": "Day 1",
        "target_finish": "Month 6",
        "wave": "Mobilization → Wave 1",
        "prerequisites": "Authoritative account inventory; local account owners; legal, tax, regulatory, service, continuity, closure-cost, and fee evidence",
        "value_score_1_to_5": 2,
        "risk_reduction_score_1_to_5": 3,
        "feasibility_score_1_to_5": 5,
        "dependency_score_1_to_5": 2,
        "speed_score_1_to_5": 5,
        "required_gates": "G0; G1; G2; G4",
        "completion_evidence": "Local checklist and approvals; zero residual dependencies; completed closure; invoice evidence of fee removal; Finance recognition",
        "value_boundary": "Four candidates and $7,800/year are validation hypotheses, not approved closures or P&L",
    },
    {
        "initiative_id": "I05",
        "initiative_name": "Staged integration, access, and resilience",
        "outcome": "Existing ERPs and selected bank sources connect through a secure, supportable, reversible architecture with tested access, audit trail, continuity, and rollback.",
        "accountable_owner": "CIO",
        "delivery_lead": "Enterprise Architecture / Cybersecurity",
        "start": "Day 1",
        "target_finish": "Month 12",
        "wave": "Mobilization → Wave 2",
        "prerequisites": "I01 source map and I03 use cases; architecture, cyber, access, support, and control owners; safe test environment and approved rollback method",
        "value_score_1_to_5": 4,
        "risk_reduction_score_1_to_5": 5,
        "feasibility_score_1_to_5": 3,
        "dependency_score_1_to_5": 5,
        "speed_score_1_to_5": 2,
        "required_gates": "G0; G2; G3; G4; G5",
        "completion_evidence": "Approved architecture; authoritative-source map; SoD/access test; audit trail; recovery and ≤4-hour rollback rehearsal; support model",
        "value_boundary": "No platform or vendor is selected; no major ERP replacement is assumed",
    },
    {
        "initiative_id": "I06",
        "initiative_name": "Governance, service, and adoption",
        "outcome": "Global policy and performance ownership operate with explicit regional/local rights, service levels, change control, training, and emergency procedures.",
        "accountable_owner": "CFO / Group Treasurer",
        "delivery_lead": "Transformation Director",
        "start": "Day 1",
        "target_finish": "Month 18",
        "wave": "Mobilization → BAU",
        "prerequisites": "G0 sponsor mandate; named global, regional, and local decision owners; approved local/emergency rights; service and blackout calendars; change support",
        "value_score_1_to_5": 4,
        "risk_reduction_score_1_to_5": 5,
        "feasibility_score_1_to_5": 4,
        "dependency_score_1_to_5": 5,
        "speed_score_1_to_5": 3,
        "required_gates": "G0; G1; G2; G3; G4; G5; G6",
        "completion_evidence": "Approved decision rights and RACI; operating forums; service and emergency rules; training/adoption evidence; BAU ownership",
        "value_boundary": "Central policy does not remove governed local execution or emergency rights",
    },
    {
        "initiative_id": "I07",
        "initiative_name": "Benefits, cost, and KPI assurance",
        "outcome": "Finance admits value only from reconciled baselines, approved formulas, named owners, realized evidence, and controlled attribution while costs remain separated by one-time and recurring treatment.",
        "accountable_owner": "CFO / Finance Benefits Lead",
        "delivery_lead": "Finance Benefits Manager",
        "start": "Day 1",
        "target_finish": "Month 18",
        "wave": "Mobilization → BAU",
        "prerequisites": "Named initiative and Finance owners; KPI/source contracts; CR01–CR10 and VG01–VG12 evidence definitions; independent recognition approvers",
        "value_score_1_to_5": 5,
        "risk_reduction_score_1_to_5": 5,
        "feasibility_score_1_to_5": 4,
        "dependency_score_1_to_5": 5,
        "speed_score_1_to_5": 3,
        "required_gates": "G0; G1; G2; G3; G4; G5; G6",
        "completion_evidence": "Closed CR01–CR10 and VG01–VG12 packages; approved baselines/targets; monthly ledger; independent Finance sign-off; change-control history",
        "value_boundary": "Cash, P&L, capacity, and risk remain non-additive; recognized value starts at $0",
    },
]


STAGE_GATES = [
    ("G0", "Day 0", "Authorize evidence mobilization", "Federated direction, named owners, $1.0–$1.5m ceiling treatment, local fallback, and no-execution boundary recorded", "CFO / Steering Committee", "Proceed / revise / stop"),
    ("G1", "Day 30", "Baseline and ownership control", "55-account and 7,600-record populations reconciled; metric contracts, sources, owners, calendars, and gaps approved", "Group Treasurer / CIO / Shared Services", "Proceed / narrow / extend evidence"),
    ("G2", "Day 60", "Design and affordability control", "Local rights, control, architecture, resilience, CR01–CR10 cost ranges, and remediation owners evidenced", "CFO / CIO / Control owners", "Proceed / switch to local stabilization / stop"),
    ("G3", "Day 90", "Bounded pilot readiness", "Baselines and target rules locked; critical gates closed; cohort ready; rollback rehearsed; NA freeze dates and sign-off path confirmed", "CFO / Steering Committee", "Stop / extend / authorize separate bounded pilot"),
    ("G4", "Months 4–6", "Wave 1 production go/no-go", "Separate funding and production approvals; control/service tests pass; NA change is outside freeze and signed by NA BU CFO", "CFO / CIO / BU Finance", "Launch / delay / rollback"),
    ("G5", "Months 9–12", "Scale decision", "Like-for-like results sustained; benefits validated; service/control thresholds met; cost forecast refreshed", "Steering Committee", "Scale / hold / redesign"),
    ("G6", "Months 15–18", "BAU handoff", "Stable KPI ownership, procedures, support, control testing, open-risk acceptance, and benefit ledger handed to BAU", "CFO / Group Treasurer / CIO", "Accept BAU / extend program"),
]


ROADMAP = [
    ("M01", "Mobilization", "Days 1–30", "Confirm owners and decision rights; reconcile populations; lock definitions and baselines; start account validation", "G1", "I01; I03; I04; I05; I06; I07"),
    ("M02", "Evidence and design", "Days 31–60", "Complete local/control/architecture reviews; source costs; define service, emergency, and rollback rules", "G2", "I01; I02; I03; I04; I05; I06; I07"),
    ("M03", "Decision readiness", "Days 61–90", "Lock target rules; assess cohorts; rehearse rollback; prepare stop/extend/pilot recommendation", "G3", "I01; I02; I03; I05; I06; I07"),
    ("M04", "Wave 1", "Months 4–6", "Launch approved read-only visibility and bounded process changes; complete validated low-risk account closures; begin controlled daily governance", "G4", "I01; I03; I04; I05; I06; I07"),
    ("M05", "Wave 2", "Months 7–12", "Expand certified visibility and funding discipline; standardize priority payment flows; scale interfaces only where evidence supports", "G5", "I02; I03; I05; I06; I07"),
    ("M06", "Scale and BAU", "Months 13–18", "Embed operating model, retire redundant manual work only after evidence, complete training/support, and transfer KPI/control ownership", "G6", "I01; I02; I03; I05; I06; I07"),
]


KPI_ROWS = [
    ("K01", "Data", "Same-day cash visibility proxy", "Account-days reported on the supplied reporting date ÷ expected account-days", "%", "58.18", "Calendar-date proxy only; approve an operational cutoff at G1", "≥90% for pilot cohort at G4; enterprise target set after G1", "Daily / monthly", "Group Treasurer", "Bank/source receipt log + account master", "Leading"),
    ("K02", "Data", "Two-plus-day delayed account-days", "Expected account-days delayed two or more calendar days", "count", "2534 of 9955", "Supplied six-month population", "Reduce ≥75% in approved pilot cohort by G5", "Daily / monthly", "Treasury Data Owner", "Source receipt log", "Lagging"),
    ("K03", "Control", "Cash-position reconciliation completion", "Positions completed with approved control total and no unexplained material break ÷ expected positions", "%", "Not available", "Baseline at G1; materiality approved at G2", "100% before funding decision", "Daily", "Group Treasurer", "Position control log", "Leading"),
    ("K04", "Liquidity", "Certified movable cash", "USD balances with current source, buffer, legal/tax/local/service certification and approved action eligibility", "USD", "0 recognized", "$21m/$35m/$46.2m are screens, not baseline value", "Target set only after VG01–VG05", "Daily / monthly", "Group Treasurer; Finance validates", "Mobility register + benefit ledger", "Lagging"),
    ("K05", "Operations", "Payment manual-touch rate", "Manual-touch records ÷ controlled payment population", "%", "31.51", "Within supplied 7,600 records only", "Target set after root-cause review; no more than 20% relative reduction at first pilot without reapproval", "Weekly / monthly", "Shared Services Lead", "Payment event log", "Lagging"),
    ("K06", "Operations", "Payment exception rate", "Exception records ÷ controlled payment population", "%", "6.30", "Within supplied 7,600 records only", "≥20% relative reduction in like-for-like approved cohort by G5", "Weekly / monthly", "Shared Services Lead", "Payment status and reason log", "Lagging"),
    ("K07", "Client service", "Late-release rate", "Late-release records ÷ controlled payment population", "%", "5.00", "Within supplied 7,600 records only", "No deterioration at G4; ≥20% relative reduction by G5", "Weekly / monthly", "Shared Services Lead / BU Finance", "Payment event log", "Lagging"),
    ("K08", "Control", "Emergency-payment control compliance", "Emergency payments with approved authority, rationale, compensating control, confirmation, and review ÷ emergency payments", "%", "Not available", "Baseline at G1", "100%", "Per event / monthly", "BU Finance / Control owner", "Emergency-payment register", "Leading"),
    ("K09", "Adoption", "In-scope role certification", "In-scope users completing role training and access certification ÷ in-scope users", "%", "0", "Program starts at mobilization", "100% before production access", "Weekly", "Change Lead / CIO", "Learning + access systems", "Leading"),
    ("K10", "Resilience", "Rollback rehearsal success", "Approved rehearsal restores prior process and reconciles affected items within four hours", "pass/fail", "Not tested", "Proposed threshold", "Pass before G3 and each material scale event", "Per release", "CIO / Process owner", "Test evidence", "Leading"),
    ("K11", "P&L", "Verified annual account-fee removal", "Annualized invoiced fees demonstrably removed after approved closure, net of closure/run costs", "USD/year", "0 recognized", "Four candidates total $7,800 estimated, not validated", "Recognize only after VG06–VG07", "Monthly / quarterly", "Finance / Group Treasurer", "Invoices + closure evidence", "Lagging"),
    ("K12", "Capacity", "Productively redeployed hours", "Observed sustained hours removed from avoidable work and assigned to named productive activity without service/control degradation", "hours/month", "0 recognized", "50/150 are hypotheses; 617.72 hours/month is management-estimated total manual capacity", "Recognize only after VG08–VG10", "Monthly", "Shared Services / Finance", "Time study + resource plan", "Lagging"),
    ("K13", "Risk", "Critical control or service incidents", "Count of critical control breaches or material service failures attributable to changed processes", "count", "Not available", "Define severity and attribution at G2", "0; any event triggers review", "Per event / monthly", "Control owner / CIO", "Incident system", "Lagging"),
    ("K14", "Economics", "Evidence-gate closure", "Closed and approved VG01–VG12 plus CR01–CR10 packages ÷ 22 total packages", "%", "0", "Model controls do not count as evidence closure", "100% of gates required for the relevant decision; not necessarily all for every bounded test", "Weekly", "Finance Benefits Lead", "Gate register", "Leading"),
]


BENEFIT_ROWS = [
    ("B01", "Cash release", "Liquidity screen", "35000000", "USD screen", "0", "0", "0", "VG01–VG05", "Group Treasurer; Finance validates", "Non-additive; no transferability or funding action established"),
    ("B02", "Annual P&L", "Account-fee sensitivity", "7800", "USD/year estimate", "0", "0", "0", "VG06–VG07", "Finance; local account owners", "Non-additive; four candidates are not approved closures"),
    ("B03", "Capacity", "Productive-capacity hypothesis", "150", "hours/month", "0", "0", "0", "VG08–VG10", "Shared Services Lead; Finance", "Non-additive; hours are not headcount, cash, or P&L"),
    ("B04", "Risk reduction", "Exposure and value", "NOT QUANTIFIED", "unquantified", "0", "0", "0", "VG11–VG12", "Management control owner; Finance", "$0 is only the current recognized-ledger entry, not zero exposure"),
]


def _weighted_score(row: pd.Series) -> float:
    score = sum(
        float(row[f"{criterion}_score_1_to_5"]) * weight
        for criterion, weight in WEIGHTS.items()
    )
    return round(score * 20, 1)


def build_outputs() -> Dict[str, pd.DataFrame]:
    initiatives = pd.DataFrame(INITIATIVES)
    initiatives["weighted_priority_score_0_to_100"] = initiatives.apply(_weighted_score, axis=1)
    initiatives["priority_rank"] = initiatives["weighted_priority_score_0_to_100"].rank(method="dense", ascending=False).astype(int)
    initiatives["evidence_label"] = "ANALYST-JUDGMENT"
    initiatives["evidence_boundary"] = EVIDENCE_BOUNDARY
    initiatives["model_version"] = MODEL_VERSION

    gates = pd.DataFrame(STAGE_GATES, columns=[
        "gate_id", "timing", "gate_name", "minimum_exit_evidence",
        "decision_owner", "allowed_decision",
    ])
    gates["current_status"] = "OPEN"
    gates["evidence_label"] = "ANALYST-JUDGMENT"
    gates["model_version"] = MODEL_VERSION

    roadmap = pd.DataFrame(ROADMAP, columns=[
        "milestone_id", "phase", "timing", "scope_and_outcome",
        "exit_gate", "linked_initiatives",
    ])
    roadmap["status"] = "PLANNED — pending G0 authorization"
    roadmap["evidence_label"] = "ANALYST-JUDGMENT"
    roadmap["model_version"] = MODEL_VERSION

    kpis = pd.DataFrame(KPI_ROWS, columns=[
        "kpi_id", "dimension", "kpi_name", "definition_and_formula", "unit",
        "current_baseline", "baseline_boundary", "target_logic", "frequency",
        "accountable_owner", "source_system_or_evidence", "indicator_type",
    ])
    kpis["status"] = "PROPOSED — owner and target approval open"
    kpis["evidence_label"] = "MIXED — ACG-DATA / ANALYST-CALC / ANALYST-JUDGMENT"
    kpis["model_version"] = MODEL_VERSION

    benefits = pd.DataFrame(BENEFIT_ROWS, columns=[
        "benefit_id", "value_category", "diagnostic_quantity_name",
        "diagnostic_quantity", "diagnostic_unit", "validated_value_usd",
        "funded_value_usd", "recognized_value_usd", "required_gates",
        "accountable_owner", "recognition_boundary",
    ])
    benefits["aggregation_rule"] = "NON-ADDITIVE — do not sum categories"
    benefits["status"] = "OPEN — no current benefit recognized"
    benefits["model_version"] = MODEL_VERSION

    return {
        "initiatives": initiatives,
        "stage_gates": gates,
        "roadmap": roadmap,
        "kpis": kpis,
        "benefits": benefits,
    }


def validate_source_baselines() -> None:
    visibility = pd.read_csv(PROCESSED / "W2_visibility_diagnostic.csv", keep_default_na=False)
    overall_visibility = visibility.loc[visibility["dimension"] == "overall"].iloc[0]
    assert float(overall_visibility["same_day_rate_pct"]) == 58.18
    assert int(overall_visibility["observations"]) == 9955
    assert int(overall_visibility["two_plus_day_delayed_observations"]) == 2534

    payments = pd.read_csv(PROCESSED / "W2_payment_diagnostic.csv", keep_default_na=False)
    overall_payments = payments.loc[payments["dimension"] == "overall"].iloc[0]
    assert int(overall_payments["records"]) == 7600
    assert float(overall_payments["manual_touch_rate_pct"]) == 31.51
    assert float(overall_payments["exception_rate_pct"]) == 6.30
    assert float(overall_payments["late_release_rate_pct"]) == 5.00

    accounts = pd.read_csv(PROCESSED / "W2_account_diagnostic.csv", keep_default_na=False)
    candidates = accounts.loc[accounts["closure_validation_candidate"].astype(str).str.lower() == "true"]
    assert len(accounts) == 55
    assert len(candidates) == 4
    assert int(candidates["annual_fee_usd"].sum()) == 7800

    costs = pd.read_csv(PROCESSED / "W3_provisional_cost_estimates.csv", keep_default_na=False)
    assert int(costs["one_time_base_usd"].sum()) == 1_155_000
    assert int(costs["recurring_annual_base_usd"].sum()) == 281_000


def validate_outputs(outputs: Dict[str, pd.DataFrame]) -> None:
    assert tuple(outputs) == ("initiatives", "stage_gates", "roadmap", "kpis", "benefits")
    assert len(outputs["initiatives"]) == 7
    assert len(outputs["stage_gates"]) == 7
    assert len(outputs["roadmap"]) == 6
    assert len(outputs["kpis"]) == 14
    assert len(outputs["benefits"]) == 4
    assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9
    assert outputs["initiatives"]["initiative_id"].is_unique
    assert outputs["initiatives"]["prerequisites"].str.strip().ne("").all()
    assert outputs["stage_gates"]["gate_id"].is_unique
    assert outputs["kpis"]["kpi_id"].is_unique
    assert set(outputs["benefits"]["validated_value_usd"]) == {"0"}
    assert set(outputs["benefits"]["funded_value_usd"]) == {"0"}
    assert set(outputs["benefits"]["recognized_value_usd"]) == {"0"}
    assert outputs["initiatives"]["weighted_priority_score_0_to_100"].between(0, 100).all()
    assert set(outputs["stage_gates"]["current_status"]) == {"OPEN"}
    assert not outputs["kpis"].astype(str).apply(lambda c: c.str.contains("TBD|TODO|XXX", case=False)).any().any()


def write_outputs(outputs: Dict[str, pd.DataFrame]) -> None:
    paths = {
        "initiatives": PROCESSED / "W4_initiative_portfolio.csv",
        "stage_gates": PROCESSED / "W4_stage_gates.csv",
        "roadmap": PROCESSED / "W4_roadmap_milestones.csv",
        "kpis": PROCESSED / "W4_kpi_dictionary.csv",
        "benefits": PROCESSED / "W4_benefits_tracker.csv",
    }
    for name, path in paths.items():
        outputs[name].to_csv(path, index=False)


def main() -> None:
    validate_source_baselines()
    outputs = build_outputs()
    validate_outputs(outputs)
    write_outputs(outputs)
    print("Week 4 implementation model: PASS")
    for name, frame in outputs.items():
        print(f"- {name}: {len(frame)} rows")


if __name__ == "__main__":
    main()
