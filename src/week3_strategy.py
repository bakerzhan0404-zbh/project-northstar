"""Reproducible Week 3 strategic-option model for Project Northstar.

The model implements the decision rule established in the Week 3 design
principles: non-compensating gates first, weighted comparison second, and
alternative-weight sensitivity third.  It is deliberately not a business-case
model.  Scores express analyst judgment about option fit; they do not certify
benefits, execution readiness, cash mobility, account closure, or removable
capacity.
"""

from pathlib import Path
from typing import Dict, Mapping, Optional, Tuple

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"

OPTION_IDS = (
    "local_stabilization",
    "federated_coordination",
    "globally_coordinated",
)

# Contract W3-DP-v1: the weights were fixed from the committed design
# principles before the option scores below were reviewed.
WEIGHT_LOCK_VERSION = "W3-DP-v1 · 2026-08-18"
BASE_WEIGHTS: Dict[str, int] = {
    "evidence_fit": 20,
    "control_resilience": 20,
    "feasibility_speed": 20,
    "local_adaptability": 15,
    "data_technology_scalability": 10,
    "value_economics": 10,
    "reversibility_learning": 5,
}

CRITERIA: Dict[str, Dict[str, str]] = {
    "evidence_fit": {
        "criterion": "Evidence fit",
        "definition": (
            "How directly the option resolves the five Week 2 findings and "
            "creates controlled decision evidence without assuming a cause."
        ),
        "principles": "DP-01; DP-02; DP-04; DP-07",
    },
    "control_resilience": {
        "criterion": "Control, service, and resilience",
        "definition": (
            "Ability to preserve control integrity, service continuity, local "
            "emergency execution, resilience, and auditable rollback."
        ),
        "principles": "DP-03; DP-05; DP-06",
    },
    "feasibility_speed": {
        "criterion": "Feasibility, speed, and affordability",
        "definition": (
            "Practicality of demonstrating controlled progress within 12 months, "
            "working around current ERPs, and fitting the CFO's $1.0–$1.5m FY2026 "
            "initial transformation envelope."
        ),
        "principles": "DP-01; DP-04; DP-08",
    },
    "local_adaptability": {
        "criterion": "Local adaptability",
        "definition": (
            "Ability to preserve documented regulatory, tax, settlement, service, "
            "and emergency rights across regions."
        ),
        "principles": "DP-02; DP-03; DP-06",
    },
    "data_technology_scalability": {
        "criterion": "Scalability and integration",
        "definition": (
            "Ability to create reusable data/control interfaces across three ERP "
            "environments, acquisitions, and a retiring legacy platform."
        ),
        "principles": "DP-01; DP-07; DP-08",
    },
    "value_economics": {
        "criterion": "Future value",
        "definition": (
            "Potential to create and later validate cash, P&L, capacity, and risk "
            "value separately; not a current benefit, ROI, or funded-value amount."
        ),
        "principles": "DP-02; DP-04; DP-07",
    },
    "reversibility_learning": {
        "criterion": "Reversibility and learning",
        "definition": (
            "Ability to learn through bounded tests, retain exit paths, and reverse "
            "a later production change within the approved service standard."
        ),
        "principles": "DP-04; DP-06; DP-08",
    },
}

# Every sensitivity reweights the same seven locked criteria.  No new criterion
# or option score is introduced after seeing a result.
SENSITIVITY_WEIGHTS: Dict[str, Dict[str, object]] = {
    "balanced_base": {
        "scenario_name": "Balanced base",
        "scenario_purpose": "Committed Week 3 design-principle weights",
        "weights": BASE_WEIGHTS,
    },
    "controls_first": {
        "scenario_name": "Controls first",
        "scenario_purpose": (
            "Tests a stronger preference for control, resilience, and reversibility"
        ),
        "weights": {
            "evidence_fit": 15,
            "control_resilience": 30,
            "feasibility_speed": 15,
            "local_adaptability": 10,
            "data_technology_scalability": 10,
            "value_economics": 10,
            "reversibility_learning": 10,
        },
    },
    "speed_first": {
        "scenario_name": "Speed first",
        "scenario_purpose": (
            "Tests a stronger preference for delivery speed under current constraints"
        ),
        "weights": {
            "evidence_fit": 15,
            "control_resilience": 20,
            "feasibility_speed": 30,
            "local_adaptability": 10,
            "data_technology_scalability": 5,
            "value_economics": 10,
            "reversibility_learning": 10,
        },
    },
    "scale_value_first": {
        "scenario_name": "Scale and value first",
        "scenario_purpose": (
            "Tests a stronger preference for long-run scalability and value validation"
        ),
        "weights": {
            "evidence_fit": 15,
            "control_resilience": 15,
            "feasibility_speed": 10,
            "local_adaptability": 10,
            "data_technology_scalability": 25,
            "value_economics": 20,
            "reversibility_learning": 5,
        },
    },
    "local_autonomy_first": {
        "scenario_name": "Local autonomy first",
        "scenario_purpose": (
            "Tests a stronger preference for local service and decision rights"
        ),
        "weights": {
            "evidence_fit": 15,
            "control_resilience": 20,
            "feasibility_speed": 15,
            "local_adaptability": 30,
            "data_technology_scalability": 5,
            "value_economics": 10,
            "reversibility_learning": 5,
        },
    },
}

# These deliberately extreme cases are not part of the plausible sensitivity
# output.  They are retained for executable switching-condition tests: the
# model must be capable of preferring another direction when priorities become
# extreme rather than mechanically forcing the base recommendation.
EXTREME_SWITCH_WEIGHTS: Dict[str, Dict[str, object]] = {
    "extreme_speed_reversibility": {
        "scenario_name": "Extreme speed and reversibility",
        "scenario_purpose": "Switch-condition test only; not a plausible base lens",
        "weights": {
            "evidence_fit": 5,
            "control_resilience": 5,
            "feasibility_speed": 50,
            "local_adaptability": 20,
            "data_technology_scalability": 0,
            "value_economics": 0,
            "reversibility_learning": 20,
        },
    },
    "extreme_scale_future_value": {
        "scenario_name": "Extreme scale and future value",
        "scenario_purpose": "Switch-condition test only; not a plausible base lens",
        "weights": {
            "evidence_fit": 5,
            "control_resilience": 5,
            "feasibility_speed": 0,
            "local_adaptability": 0,
            "data_technology_scalability": 50,
            "value_economics": 40,
            "reversibility_learning": 0,
        },
    },
}

OPTIONS: Dict[str, Dict[str, str]] = {
    "local_stabilization": {
        "option_name": "Local stabilization",
        "option_description": (
            "Common minimum definitions and reporting controls with locally owned "
            "source, payment, and account improvements."
        ),
        "deliberate_non_solution": (
            "Does not create coordinated enterprise liquidity or a common operating "
            "model beyond the controlled feed to Group Treasury."
        ),
        "switch_condition": (
            "Use as the interim direction if central ownership, integration readiness, "
            "or affordability cannot clear the mobilization gates; retain the controlled "
            "enterprise data feed as a minimum condition."
        ),
    },
    "federated_coordination": {
        "option_name": "Federated coordination",
        "option_description": (
            "Group-owned data, policy, control, and daily-position spine with regional "
            "and local execution, approved exceptions, and emergency rights."
        ),
        "deliberate_non_solution": (
            "Does not centralize every payment, replace the ERPs, select a platform, or "
            "treat screened liquidity as transferable cash."
        ),
        "switch_condition": (
            "Remain preferred only while global owners, regional decision rights, staged "
            "interfaces, controls, service gates, and rollback are confirmed."
        ),
    },
    "globally_coordinated": {
        "option_name": "Globally coordinated",
        "option_description": (
            "Centralized enterprise cash-position and payment coordination supported by "
            "standardized connectivity, data, workflow, and controls."
        ),
        "deliberate_non_solution": (
            "Does not eliminate legal, tax, settlement, local-service, or resilience "
            "constraints and is not currently an execution-ready platform mandate."
        ),
        "switch_condition": (
            "Consider only after legal/local, cyber/resilience, architecture, cost, "
            "service, and mobility evidence clears the hard gates and the Steering "
            "Committee explicitly prioritizes enterprise scale."
        ),
    },
}

# These 1–5 scores are analyst judgments, not observed performance.  Each score
# has an explicit rationale and evidence anchor in SCORE_DETAILS.
OPTION_SCORES: Dict[str, Dict[str, int]] = {
    "local_stabilization": {
        "evidence_fit": 3,
        "control_resilience": 3,
        "feasibility_speed": 5,
        "local_adaptability": 5,
        "data_technology_scalability": 2,
        "value_economics": 2,
        "reversibility_learning": 5,
    },
    "federated_coordination": {
        "evidence_fit": 5,
        "control_resilience": 4,
        "feasibility_speed": 4,
        "local_adaptability": 5,
        "data_technology_scalability": 4,
        "value_economics": 4,
        "reversibility_learning": 4,
    },
    "globally_coordinated": {
        "evidence_fit": 3,
        "control_resilience": 3,
        "feasibility_speed": 2,
        "local_adaptability": 2,
        "data_technology_scalability": 5,
        "value_economics": 5,
        "reversibility_learning": 2,
    },
}

SCORE_DETAILS: Dict[Tuple[str, str], Dict[str, str]] = {
    ("local_stabilization", "evidence_fit"): {
        "rationale": "Addresses the evidenced local reporting and payment gaps, but only partly resolves enterprise coordination.",
        "anchor": "F07–F11: observable gaps require one controlled decision chain.",
        "confidence": "Medium",
    },
    ("local_stabilization", "control_resilience"): {
        "rationale": "Limits concentration risk, but locally variable controls and ownership remain difficult to govern consistently.",
        "anchor": "F10 and stakeholder evidence: required controls and access practices remain unvalidated.",
        "confidence": "Low",
    },
    ("local_stabilization", "feasibility_speed"): {
        "rationale": "Requires the least organizational and integration change and is the most plausible fit to the initial funding envelope.",
        "anchor": "Client constraint: no major ERP replacement in 18 months; Inject 3 caps initial FY2026 investment at $1.0–$1.5m.",
        "confidence": "Medium",
    },
    ("local_stabilization", "local_adaptability"): {
        "rationale": "Retains local execution and is most adaptable to market-specific service, tax, and regulatory constraints.",
        "anchor": "APAC, BU Finance, and Audit concerns favor explicit local service and emergency rights.",
        "confidence": "Medium",
    },
    ("local_stabilization", "data_technology_scalability"): {
        "rationale": "Can standardize extracts, but repeated local fixes do not create a reusable enterprise integration model.",
        "anchor": "F07 and DP-08: 23 delayed sources are concentrated, while three ERP environments must remain.",
        "confidence": "Medium",
    },
    ("local_stabilization", "value_economics"): {
        "rationale": "May produce bounded local improvements, but it provides a weak path to validate enterprise liquidity or capacity economics.",
        "anchor": "F08, F10, and F11: mobility, removable capacity, and fee savings remain unvalidated.",
        "confidence": "Low",
    },
    ("local_stabilization", "reversibility_learning"): {
        "rationale": "Small, locally bounded changes provide the strongest near-term reversibility, though learning may not transfer automatically.",
        "anchor": "DP-04 and DP-06 require bounded tests, shared evidence, and an approved rollback path.",
        "confidence": "Medium",
    },
    ("federated_coordination", "evidence_fit"): {
        "rationale": "Directly joins the source, ownership, control, regional-execution, and KPI gaps identified in Week 2.",
        "anchor": "F07–F11 and the Week 2 conclusion favor one data/control spine with defined local execution.",
        "confidence": "High",
    },
    ("federated_coordination", "control_resilience"): {
        "rationale": "Combines global minimum controls with local emergency rights, but control-owner validation is still required.",
        "anchor": "DP-03, DP-05, and DP-06 make controls, service, resilience, and rollback non-compensating.",
        "confidence": "Medium",
    },
    ("federated_coordination", "feasibility_speed"): {
        "rationale": "Supports staged interfaces and bounded pilots without ERP replacement; affordability remains conditional on a costed plan within the initial envelope.",
        "anchor": "F07 and CIO evidence support staged integration; Inject 3 limits initial FY2026 investment to $1.0–$1.5m.",
        "confidence": "Medium",
    },
    ("federated_coordination", "local_adaptability"): {
        "rationale": "Sets enterprise standards while preserving approved regional execution, exceptions, and emergency authority.",
        "anchor": "DP-03 resolves global consistency versus local regulatory, tax, and service requirements.",
        "confidence": "Medium",
    },
    ("federated_coordination", "data_technology_scalability"): {
        "rationale": "Creates reusable interfaces and lineage across current ERPs without deep investment in the retiring platform.",
        "anchor": "DP-07 and DP-08 require metric lineage, modular integration, and explicit exit paths.",
        "confidence": "Medium",
    },
    ("federated_coordination", "value_economics"): {
        "rationale": "Creates the strongest staged path to validate value owners and baselines without recognizing uncertified benefits.",
        "anchor": "F08, F10, and F11 keep funded mobility, capacity, and fee value at zero until certification.",
        "confidence": "Medium",
    },
    ("federated_coordination", "reversibility_learning"): {
        "rationale": "Bounded source and payment tests can generate shared learning before scale, with more coordination than local stabilization requires.",
        "anchor": "DP-04, DP-06, and DP-08 require bounded pilots, four compliant weeks, and rollback.",
        "confidence": "High",
    },
    ("globally_coordinated", "evidence_fit"): {
        "rationale": "Addresses enterprise coordination comprehensively, but goes beyond the ambition proven necessary by current evidence.",
        "anchor": "Week 2 supports targeted intervention and option design, not a broad technology or centralization mandate.",
        "confidence": "Medium",
    },
    ("globally_coordinated", "control_resilience"): {
        "rationale": "Could standardize controls but concentrates operational, cyber, access, and resilience failure risk.",
        "anchor": "Audit and CIO evidence requires explicit SoD, access, resilience, emergency procedures, and rollback.",
        "confidence": "Low",
    },
    ("globally_coordinated", "feasibility_speed"): {
        "rationale": "Requires the greatest governance, architecture, integration, and change effort and is least likely to fit the uncosted initial envelope.",
        "anchor": "No ERP replacement, a retiring legacy ERP, peak protection, and Inject 3's $1.0–$1.5m envelope constrain delivery.",
        "confidence": "Medium",
    },
    ("globally_coordinated", "local_adaptability"): {
        "rationale": "Creates the highest risk of applying global assumptions before local legal, tax, settlement, and service rules are certified.",
        "anchor": "APAC and BU Finance evidence rejects centralization that weakens local response or critical service.",
        "confidence": "Medium",
    },
    ("globally_coordinated", "data_technology_scalability"): {
        "rationale": "Offers the strongest long-run enterprise standardization and acquisition scalability if architecture gates clear.",
        "anchor": "DP-08 favors reusable integration, but does not authorize a platform or irreversible rollout.",
        "confidence": "Low",
    },
    ("globally_coordinated", "value_economics"): {
        "rationale": "Offers the highest future enterprise value reach, but current costs and benefit lines remain uncertified and cannot support funding now.",
        "anchor": "F08, F10, and F11 plus open implementation-cost evidence prevent a funded economics claim.",
        "confidence": "Low",
    },
    ("globally_coordinated", "reversibility_learning"): {
        "rationale": "Greater centralization and integration create higher switching cost and a less reversible learning path.",
        "anchor": "DP-06 and DP-08 require bounded change, legacy transition, scale gates, and exit paths.",
        "confidence": "Medium",
    },
}

HARD_GATES: Dict[str, Dict[str, str]] = {
    "G01": {
        "gate_name": "Authoritative data and metric ownership",
        "gate_rule": "Named source/metric owners, definitions, lineage, reconciliation, and change control are explicit.",
        "principles": "DP-01; DP-07",
    },
    "G02": {
        "gate_name": "Local rights and critical-service continuity",
        "gate_rule": "Local legal, tax, settlement, service, peak-period, and emergency rights remain explicit.",
        "principles": "DP-03; DP-06",
    },
    "G03": {
        "gate_name": "Control integrity and accountable ownership",
        "gate_rule": "Required authorization, SoD, access, audit, duplicate, sanctions, and reconciliation controls remain designed and owned.",
        "principles": "DP-05",
    },
    "G04": {
        "gate_name": "Resilience and rollback",
        "gate_rule": "A rehearsable prior-process fallback and later restoration within four hours are part of the design.",
        "principles": "DP-06; DP-08",
    },
    "G05": {
        "gate_name": "ERP and architecture constraint",
        "gate_rule": "The option works around three current ERPs, avoids major replacement, and identifies the retiring-platform exit path.",
        "principles": "DP-08",
    },
    "G06": {
        "gate_name": "Affordability and accountable funding",
        "gate_rule": "The costed initial scope fits the CFO's $1.0–$1.5m FY2026 envelope; larger commitments require staged approval and demonstrated Wave 1 benefits.",
        "principles": "DP-02; DP-04; DP-08; CLIENT_INJECTS-03",
    },
    "G07": {
        "gate_name": "Evidence and funded-value discipline",
        "gate_rule": "No screened cash, estimated fee, capacity, cause, closure, or external benchmark becomes an approved benefit by scoring.",
        "principles": "DP-02; DP-04; DP-07",
    },
}

GATE_CONDITIONS: Dict[Tuple[str, str], str] = {
    ("local_stabilization", "G01"): "Local sources must still deliver the controlled enterprise feed and common KPI contract.",
    ("local_stabilization", "G02"): "Local execution and emergency authority remain intact under common minimum service standards.",
    ("local_stabilization", "G03"): "Every local change retains or replaces required controls and identifies the management owner.",
    ("local_stabilization", "G04"): "Each local intervention retains the approved prior process and four-hour restoration design.",
    ("local_stabilization", "G05"): "Changes use controlled interfaces around existing ERPs and avoid deep retiring-platform investment.",
    ("local_stabilization", "G06"): "A costed local scope must fit $1.0–$1.5m; costs remain unavailable, so execution readiness is open.",
    ("local_stabilization", "G07"): "Local improvements remain evidence tests; no unvalidated value is recognized.",
    ("federated_coordination", "G01"): "Group owns the data/KPI contract; regional owners reconcile authoritative local sources.",
    ("federated_coordination", "G02"): "Enterprise standards explicitly preserve approved regional exceptions and emergency execution.",
    ("federated_coordination", "G03"): "Global minimum controls and accountable local operation are explicit in the design.",
    ("federated_coordination", "G04"): "Staged interfaces and bounded pilots retain local fallback and four-hour restoration.",
    ("federated_coordination", "G05"): "A modular data/control spine works around current ERPs and supports legacy retirement.",
    ("federated_coordination", "G06"): "A staged, costed foundation scope must fit $1.0–$1.5m before any implementation approval.",
    ("federated_coordination", "G07"): "The option creates validation pathways while keeping uncertified value outside funding.",
    ("globally_coordinated", "G01"): "Central coordination depends on authoritative local sources, owners, lineage, and reconciliation.",
    ("globally_coordinated", "G02"): "Central workflows retain documented local legal, service, and emergency override rights.",
    ("globally_coordinated", "G03"): "Centralized access and workflow include explicit SoD, audit, cyber, and control ownership.",
    ("globally_coordinated", "G04"): "The design includes regional continuity and a rehearsable four-hour restoration path.",
    ("globally_coordinated", "G05"): "No platform or ERP replacement is assumed; architecture and legacy-exit approval stay gated.",
    ("globally_coordinated", "G06"): "The option is held unless a bounded initial scope fits $1.0–$1.5m; any larger commitment requires staged approval.",
    ("globally_coordinated", "G07"): "Theoretical reach does not convert screened liquidity, capacity, or fees into funded value.",
}

EVIDENCE_BOUNDARY = (
    "ANALYST-JUDGMENT for option comparison only; not client-approved, not an "
    "execution authorization, and not a business case or funded-benefit estimate."
)


def _assert_close(actual: float, expected: float, label: str) -> None:
    if round(float(actual), 2) != round(float(expected), 2):
        raise AssertionError(f"{label}: expected {expected}, found {actual}")


def validate_week2_evidence() -> Dict[str, str]:
    """Fail closed if the Week 2 anchors used by the score rationales drift."""
    metrics = pd.read_csv(PROCESSED / "W2_reconciliation_metrics.csv").set_index(
        "metric"
    )
    expected_metrics = {
        "accounts": 55,
        "balance_observations": 9_955,
        "payment_records": 7_600,
        "gross_supplied_payment_value": 198_135_489.50,
        "payment_repair_minutes": 20_080,
        "estimated_manual_process_hours_monthly": 617.72,
    }
    for metric, expected in expected_metrics.items():
        _assert_close(metrics.loc[metric, "value"], expected, metric)

    visibility = pd.read_csv(PROCESSED / "W2_visibility_diagnostic.csv")
    overall_visibility = visibility.loc[visibility["dimension"].eq("overall")].iloc[0]
    _assert_close(overall_visibility["accounts"], 55, "visibility accounts")
    _assert_close(
        overall_visibility["same_day_rate_pct"], 58.18, "same-day date proxy"
    )
    source_visibility = visibility.loc[
        visibility["dimension"].eq("visibility_method")
    ].set_index("category")
    _assert_close(source_visibility.loc["Portal", "accounts"], 9, "portal accounts")
    _assert_close(
        source_visibility.loc["Spreadsheet", "accounts"],
        14,
        "spreadsheet accounts",
    )

    thresholds = pd.read_csv(PROCESSED / "W2_liquidity_thresholds.csv")
    threshold_14 = thresholds.loc[thresholds["buffer_window_days"].eq(14)].set_index(
        "threshold_name"
    )
    for name, expected in {"stress": 168, "base": 138, "upside": 0}.items():
        _assert_close(
            threshold_14.loc[name, "days_threshold_met"],
            expected,
            f"14-day {name} threshold",
        )
    if not threshold_14["decision_boundary"].str.contains(
        "no threshold is validated movable cash", case=False
    ).all():
        raise AssertionError("Liquidity screen lost the movable-cash boundary")

    accounts = pd.read_csv(
        PROCESSED / "W2_account_diagnostic.csv", keep_default_na=False
    )
    candidates = accounts.loc[
        accounts["closure_validation_candidate"].astype(str).str.lower().eq("true")
    ]
    _assert_close(len(candidates), 4, "closure-validation candidates")
    _assert_close(candidates["annual_fee_usd"].sum(), 7_800, "candidate fees")

    payments = pd.read_csv(PROCESSED / "W2_payment_diagnostic.csv")
    priority = payments.loc[
        payments["dimension"].eq("priority_union")
        & payments["category"].eq("Manual touch or cross-border wire")
    ].iloc[0]
    _assert_close(priority["records"], 2_839, "priority-union records")
    _assert_close(priority["exception_records"], 356, "priority-union exceptions")
    _assert_close(priority["repair_minutes"], 14_939, "priority-union repair minutes")

    repair = pd.read_csv(
        PROCESSED / "W2_repair_baseline_reconciliation.csv"
    ).set_index("metric")
    _assert_close(
        repair.loc["payment_file_repair_hours_monthly", "value"],
        55.78,
        "payment-file repair hours",
    )
    _assert_close(
        repair.loc["process_file_exception_manual_hours_monthly", "value"],
        102.60,
        "process-file repair hours",
    )

    return {
        "F07": "23/55 delayed accounts are portal/spreadsheet; 58.18% is a same-calendar-day proxy.",
        "F08": "Liquidity thresholds are screening sensitivities; validated movable cash remains unestablished.",
        "F09": "Priority union is 2,839/7,600 records with 356 exceptions and 14,939 repair minutes.",
        "F10": "617.72 estimated hours/month; payment/process repair baselines remain unreconciled.",
        "F11": "Four closure-validation candidates and estimated fees remain locally gated.",
    }


def build_gate_assessments(
    gate_overrides: Optional[Mapping[Tuple[str, str], bool]] = None,
) -> pd.DataFrame:
    """Build option-specific, non-compensating design-gate assessments.

    A ``True`` result means the option definition contains the required design
    condition.  It does not mean execution evidence or client approval exists.
    ``gate_overrides`` supports fail-closed testing and future reviewed changes.
    """
    overrides = dict(gate_overrides or {})
    rows = []
    for option_order, option_id in enumerate(OPTION_IDS, start=1):
        for gate_order, (gate_id, gate) in enumerate(HARD_GATES.items(), start=1):
            design_compliant = overrides.get((option_id, gate_id), True)
            rows.append(
                {
                    "option_order": option_order,
                    "option_id": option_id,
                    "option_name": OPTIONS[option_id]["option_name"],
                    "gate_order": gate_order,
                    "gate_id": gate_id,
                    "gate_name": gate["gate_name"],
                    "principles": gate["principles"],
                    "gate_rule": gate["gate_rule"],
                    "option_design_condition": GATE_CONDITIONS[(option_id, gate_id)],
                    "design_compliant": bool(design_compliant),
                    "design_gate_status": (
                        "PASS — condition explicit; execution evidence open"
                        if design_compliant
                        else "FAIL — option is not eligible for weighted scoring"
                    ),
                    "execution_evidence_status": (
                        "Open — named client/control owner validation required"
                    ),
                    "non_compensating": True,
                    "evidence_boundary": EVIDENCE_BOUNDARY,
                }
            )
    return pd.DataFrame(rows)


def build_score_inputs() -> pd.DataFrame:
    """Return the complete option/criterion score matrix with rationales."""
    rows = []
    for option_order, option_id in enumerate(OPTION_IDS, start=1):
        for criterion_order, criterion_id in enumerate(BASE_WEIGHTS, start=1):
            detail = SCORE_DETAILS[(option_id, criterion_id)]
            rows.append(
                {
                    "option_order": option_order,
                    "option_id": option_id,
                    "option_name": OPTIONS[option_id]["option_name"],
                    "criterion_order": criterion_order,
                    "criterion_id": criterion_id,
                    "criterion": CRITERIA[criterion_id]["criterion"],
                    "criterion_definition": CRITERIA[criterion_id]["definition"],
                    "principles": CRITERIA[criterion_id]["principles"],
                    "locked_weight_pct": BASE_WEIGHTS[criterion_id],
                    "score_1_to_5": OPTION_SCORES[option_id][criterion_id],
                    "score_rationale": detail["rationale"],
                    "evidence_anchor": detail["anchor"],
                    "evidence_confidence": detail["confidence"],
                    "evidence_label": "ANALYST-JUDGMENT",
                    "weight_lock_version": WEIGHT_LOCK_VERSION,
                    "evidence_boundary": EVIDENCE_BOUNDARY,
                }
            )
    return pd.DataFrame(rows)


def validate_model_contract(
    score_inputs: pd.DataFrame,
    gate_assessments: pd.DataFrame,
    sensitivity_weights: Mapping[str, Mapping[str, object]] = SENSITIVITY_WEIGHTS,
) -> None:
    """Validate locked weights, common score rubric, gates, and sensitivities."""
    criterion_ids = tuple(BASE_WEIGHTS)
    if tuple(CRITERIA) != criterion_ids:
        raise AssertionError("Criterion definitions differ from the locked weights")
    if sum(BASE_WEIGHTS.values()) != 100:
        raise AssertionError("Base weights must sum to 100")
    if set(score_inputs["option_id"]) != set(OPTION_IDS):
        raise AssertionError("Score matrix must contain exactly the three governed options")
    expected_pairs = {
        (option_id, criterion_id)
        for option_id in OPTION_IDS
        for criterion_id in criterion_ids
    }
    actual_pairs = set(zip(score_inputs["option_id"], score_inputs["criterion_id"]))
    if actual_pairs != expected_pairs or len(score_inputs) != len(expected_pairs):
        raise AssertionError("Every option must have exactly one score per criterion")
    if not score_inputs["score_1_to_5"].between(1, 5, inclusive="both").all():
        raise AssertionError("All option scores must be in the 1–5 rubric")
    if score_inputs[
        ["score_rationale", "evidence_anchor", "evidence_confidence"]
    ].replace("", pd.NA).isna().any().any():
        raise AssertionError("Every score requires rationale, evidence, and confidence")

    expected_gates = {
        (option_id, gate_id) for option_id in OPTION_IDS for gate_id in HARD_GATES
    }
    actual_gates = set(
        zip(gate_assessments["option_id"], gate_assessments["gate_id"])
    )
    if actual_gates != expected_gates or len(gate_assessments) != len(expected_gates):
        raise AssertionError("Every option must be assessed once against every hard gate")
    if not gate_assessments["non_compensating"].eq(True).all():  # noqa: E712
        raise AssertionError("Hard gates must remain non-compensating")

    for scenario_id, scenario in sensitivity_weights.items():
        weights = scenario["weights"]
        if set(weights) != set(criterion_ids):
            raise AssertionError(
                f"Sensitivity {scenario_id} must reweight the same seven criteria"
            )
        if sum(weights.values()) != 100:
            raise AssertionError(f"Sensitivity {scenario_id} must sum to 100")
        if any(weight < 0 for weight in weights.values()):
            raise AssertionError(f"Sensitivity {scenario_id} has a negative weight")


def _option_eligibility(gate_assessments: pd.DataFrame) -> pd.Series:
    return gate_assessments.groupby("option_id")["design_compliant"].all()


def score_base_options(
    score_inputs: pd.DataFrame, gate_assessments: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Apply hard gates, then calculate base weighted scores and summary."""
    validate_model_contract(score_inputs, gate_assessments)
    eligibility = _option_eligibility(gate_assessments)
    result = score_inputs.copy()
    result["hard_gate_result"] = result["option_id"].map(eligibility).map(
        {
            True: "PASS — eligible for design scoring; execution gates open",
            False: "FAIL — not scored",
        }
    )
    result["weighted_points_0_to_100"] = (
        result["score_1_to_5"] * result["locked_weight_pct"] / 5
    ).round(4)
    result.loc[
        ~result["option_id"].map(eligibility), "weighted_points_0_to_100"
    ] = pd.NA

    totals = (
        result.groupby(["option_order", "option_id", "option_name"], sort=False)[
            "weighted_points_0_to_100"
        ]
        .sum(min_count=1)
        .rename("base_weighted_score_0_to_100")
        .reset_index()
    )
    totals["base_weighted_score_0_to_100"] = totals[
        "base_weighted_score_0_to_100"
    ].round(4)
    totals["base_rank"] = totals["base_weighted_score_0_to_100"].rank(
        method="min", ascending=False, na_option="bottom"
    ).astype("Int64")
    totals.loc[
        totals["base_weighted_score_0_to_100"].isna(), "base_rank"
    ] = pd.NA
    totals["hard_gate_result"] = totals["option_id"].map(eligibility).map(
        {
            True: "PASS — eligible for design scoring; execution gates open",
            False: "FAIL — not scored",
        }
    )
    return result, totals


def build_sensitivity_results(
    score_inputs: pd.DataFrame,
    gate_assessments: pd.DataFrame,
    sensitivity_weights: Mapping[str, Mapping[str, object]] = SENSITIVITY_WEIGHTS,
) -> pd.DataFrame:
    """Reweight the same option scores under each governed priority lens."""
    validate_model_contract(score_inputs, gate_assessments, sensitivity_weights)
    eligibility = _option_eligibility(gate_assessments)
    score_lookup = score_inputs.pivot(
        index="option_id", columns="criterion_id", values="score_1_to_5"
    )
    rows = []
    for scenario_order, (scenario_id, scenario) in enumerate(
        sensitivity_weights.items(), start=1
    ):
        weights = scenario["weights"]
        scenario_rows = []
        for option_order, option_id in enumerate(OPTION_IDS, start=1):
            eligible = bool(eligibility.loc[option_id])
            total = (
                sum(
                    float(score_lookup.loc[option_id, criterion_id])
                    * weights[criterion_id]
                    / 5
                    for criterion_id in BASE_WEIGHTS
                )
                if eligible
                else pd.NA
            )
            row = {
                "scenario_order": scenario_order,
                "scenario_id": scenario_id,
                "scenario_name": scenario["scenario_name"],
                "scenario_purpose": scenario["scenario_purpose"],
                "option_order": option_order,
                "option_id": option_id,
                "option_name": OPTIONS[option_id]["option_name"],
            }
            for criterion_id in BASE_WEIGHTS:
                row[f"weight_{criterion_id}_pct"] = weights[criterion_id]
            row.update(
                {
                    "hard_gate_result": (
                        "PASS — eligible for design scoring; execution gates open"
                        if eligible
                        else "FAIL — not scored"
                    ),
                    "total_weighted_score_0_to_100": (
                        round(float(total), 4) if eligible else pd.NA
                    ),
                    "weight_lock_version": WEIGHT_LOCK_VERSION,
                    "evidence_boundary": EVIDENCE_BOUNDARY,
                }
            )
            scenario_rows.append(row)
        scenario_frame = pd.DataFrame(scenario_rows)
        scenario_frame["rank"] = scenario_frame[
            "total_weighted_score_0_to_100"
        ].rank(
            method="min", ascending=False, na_option="bottom"
        ).astype("Int64")
        scenario_frame.loc[
            scenario_frame["total_weighted_score_0_to_100"].isna(), "rank"
        ] = pd.NA
        scenario_frame["scenario_winner"] = scenario_frame["rank"].eq(1)
        rows.extend(scenario_frame.to_dict("records"))
    return pd.DataFrame(rows)


def build_option_summary(
    base_totals: pd.DataFrame, sensitivity: pd.DataFrame
) -> pd.DataFrame:
    """Create one decision-readable record per option without benefit claims."""
    wins = sensitivity.groupby("option_id")["scenario_winner"].sum()
    scenario_count = sensitivity["scenario_id"].nunique()
    rows = []
    for option_order, option_id in enumerate(OPTION_IDS, start=1):
        total = base_totals.loc[base_totals["option_id"].eq(option_id)].iloc[0]
        is_preferred = (
            not pd.isna(total["base_rank"]) and int(total["base_rank"]) == 1
        )
        rows.append(
            {
                "option_order": option_order,
                "option_id": option_id,
                "option_name": OPTIONS[option_id]["option_name"],
                "option_description": OPTIONS[option_id]["option_description"],
                "deliberate_non_solution": OPTIONS[option_id][
                    "deliberate_non_solution"
                ],
                "hard_gate_result": total["hard_gate_result"],
                "execution_gate_status": (
                    "OPEN — no option is execution-ready; all client/data/control/service/cost gates require approval"
                ),
                "execution_readiness": (
                    "NOT AUTHORIZED — client, data, control, service, cost, and owner evidence remains open"
                ),
                "initial_funding_constraint": (
                    "$1.0–$1.5m FY2026 initial envelope; larger commitment requires staged approval and demonstrated Wave 1 benefits"
                ),
                "base_weighted_score_0_to_100": total[
                    "base_weighted_score_0_to_100"
                ],
                "base_rank": total["base_rank"],
                "provisional_preferred_option": is_preferred,
                "sensitivity_wins": int(wins.loc[option_id]),
                "sensitivity_scenarios": scenario_count,
                "switch_condition": OPTIONS[option_id]["switch_condition"],
                "recommendation_status": (
                    "Provisional analyst direction for Steering Committee review"
                    if is_preferred
                    else "Alternative retained with explicit switching condition"
                ),
                "evidence_label": "ANALYST-JUDGMENT",
                "weight_lock_version": WEIGHT_LOCK_VERSION,
                "evidence_boundary": EVIDENCE_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def build_model_controls(gate_assessments: pd.DataFrame) -> pd.DataFrame:
    """Combine hard-gate results and model-governance controls for auditability."""
    rows = []
    for gate in gate_assessments.itertuples(index=False):
        rows.append(
            {
                "control_record_id": f"{gate.gate_id}-{gate.option_id}",
                "control_type": "NON_COMPENSATING_HARD_GATE",
                "option_id": gate.option_id,
                "option_name": gate.option_name,
                "control_name": gate.gate_name,
                "control_rule": gate.gate_rule,
                "test_result": gate.design_gate_status,
                "execution_evidence_status": gate.execution_evidence_status,
                "model_effect": (
                    "Eligible for scoring; execution still gated"
                    if gate.design_compliant
                    else "Option excluded from weighted scoring"
                ),
                "evidence_boundary": gate.evidence_boundary,
            }
        )

    governance_controls = [
        (
            "MC01",
            "Weights locked before scores",
            f"The seven base weights are fixed at {WEIGHT_LOCK_VERSION} and sum to 100%.",
        ),
        (
            "MC02",
            "Common scoring rubric",
            "Every option is scored once on the same seven 1–5 criteria with rationale and confidence.",
        ),
        (
            "MC03",
            "Gate then score",
            "A failed hard gate excludes an option; weighted value cannot compensate for failure.",
        ),
        (
            "MC04",
            "Sensitivity contract",
            "Alternative lenses reweight only the same seven criteria and each sums to 100%.",
        ),
        (
            "MC05",
            "Week 2 evidence reconciliation",
            "The model fails closed if the governed Week 2 finding anchors drift.",
        ),
        (
            "MC06",
            "No business-case inference",
            "Option scores do not calculate benefits, costs, ROI, NPV, payback, cash movement, closure, or labor removal.",
        ),
        (
            "MC07",
            "Human decision retained",
            "The result is an analyst proposal and cannot authorize execution, funding, or scale.",
        ),
    ]
    for control_id, control_name, rule in governance_controls:
        rows.append(
            {
                "control_record_id": control_id,
                "control_type": "MODEL_GOVERNANCE",
                "option_id": "ALL_OPTIONS",
                "option_name": "All options",
                "control_name": control_name,
                "control_rule": rule,
                "test_result": "PASS",
                "execution_evidence_status": "Not applicable — analytical control",
                "model_effect": "Required for valid model output",
                "evidence_boundary": EVIDENCE_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def build_strategy_model(
    gate_overrides: Optional[Mapping[Tuple[str, str], bool]] = None,
    sensitivity_weights: Mapping[str, Mapping[str, object]] = SENSITIVITY_WEIGHTS,
) -> Dict[str, pd.DataFrame]:
    """Build all four governed Week 3 option-model outputs in memory."""
    validate_week2_evidence()
    gates = build_gate_assessments(gate_overrides)
    score_inputs = build_score_inputs()
    validate_model_contract(score_inputs, gates, sensitivity_weights)
    weighted_scores, base_totals = score_base_options(score_inputs, gates)
    sensitivity = build_sensitivity_results(
        score_inputs, gates, sensitivity_weights
    )
    summary = build_option_summary(base_totals, sensitivity)
    controls = build_model_controls(gates)
    return {
        "weighted_scores": weighted_scores,
        "summary": summary,
        "sensitivity": sensitivity,
        "controls": controls,
    }


def write_outputs(outputs: Mapping[str, pd.DataFrame]) -> None:
    """Write only the governed Week 3 option-model CSV outputs."""
    PROCESSED.mkdir(parents=True, exist_ok=True)
    output_paths = {
        "weighted_scores": "W3_option_weighted_scores.csv",
        "summary": "W3_option_summary.csv",
        "sensitivity": "W3_option_sensitivity.csv",
        "controls": "W3_model_controls.csv",
    }
    if set(outputs) != set(output_paths):
        raise AssertionError("Unexpected Week 3 output set")
    for key, filename in output_paths.items():
        outputs[key].to_csv(PROCESSED / filename, index=False)


def main() -> None:
    outputs = build_strategy_model()
    write_outputs(outputs)
    summary = outputs["summary"][
        [
            "option_name",
            "hard_gate_result",
            "base_weighted_score_0_to_100",
            "base_rank",
        ]
    ]
    print(summary.to_string(index=False))
    print("\nWrote governed Week 3 option-model outputs to data/processed/.")
    print(f"Decision boundary: {EVIDENCE_BOUNDARY}")


if __name__ == "__main__":
    main()
