"""Reproducible Week 3 validation case for Project Northstar.

This module is deliberately a validation case, not an investment case.  It
translates the Week 2 diagnostic into three explicitly labelled hypotheses,
keeps cash release, annual P&L, capacity, and risk in separate ledgers, and
fails closed whenever unsupported value or cost is introduced.

The FY2026 $1.0-$1.5m management envelope is a ceiling for an initial stage.
It is not a cost estimate, budget approval, spend authority, or denominator
for ROI.  Costs, benefit ramp, ROI, NPV, and payback remain unavailable until
the evidence requirements in ``W3_cost_evidence_requirements.csv`` close.
"""

from pathlib import Path
from typing import Dict, Iterable, Mapping

import pandas as pd
from pandas.testing import assert_frame_equal


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
WEEK3 = ROOT / "deliverables" / "working" / "week_3"

MODEL_VERSION = "W3-VALIDATION-CASE-v1 · 2026-08-18"
INITIAL_ENVELOPE_LOW_USD = 1_000_000
INITIAL_ENVELOPE_HIGH_USD = 1_500_000
ENVELOPE_ROLE = (
    "FY2026 initial-stage ceiling only; not a cost estimate, budget approval, "
    "spend authority, committed funding, or ROI denominator"
)
COST_MODEL_USE = (
    "BLOCKED — do not calculate returns or decide funding until populated"
)
RECOMMENDATION_TEST = (
    "CONDITIONAL DESIGN DIRECTION — federated coordination only while global "
    "data/control ownership, minimum integration readiness, and affordability "
    "remain viable; otherwise use local stabilization; no execution, funding, "
    "or benefit approval"
)
TWO_ACCOUNT_FEE_RANGE_LOW_USD_ANNUAL = 1_800
TWO_ACCOUNT_FEE_RANGE_HIGH_USD_ANNUAL = 6_000
TWO_ACCOUNT_FEE_RANGE_ROLE = (
    "EVIDENCED RANGE — any two of the four candidate estimates total "
    "$1,800–$6,000; comparison context only, not a selected pair or benefit"
)
LIQUIDITY_EVIDENCE_STATUS = {
    "downside": (
        "DIAGNOSTIC 14-DAY SCREEN — $21m passes 168/168 complete windows; "
        "validated movable cash is not established"
    ),
    "base": (
        "DIAGNOSTIC 14-DAY SCREEN — $35m passes 138/168 complete windows; "
        "validated movable cash is not established"
    ),
    "upside": (
        "DIAGNOSTIC 14-DAY SCREEN — $46.2m passes 0/168 complete windows; "
        "validated movable cash is not established"
    ),
}
FEE_EVIDENCE_STATUS = (
    "ARITHMETIC PORTFOLIO SENSITIVITY — not selected-account fees or annual P&L"
)
CAPACITY_EVIDENCE_STATUS = (
    "PRODUCTIVE-CAPACITY HYPOTHESIS — not observed labor, headcount, cash, or P&L"
)
RISK_VALUE_STATUS = "RISK EXPOSURE AND VALUE NOT QUANTIFIED"
LEDGER_EVIDENCE_STATUS = "OPEN — diagnostic quantity is not a validated benefit"
AGGREGATION_RULE = "NON-ADDITIVE — do not sum across categories or scenarios"
COST_EVIDENCE_STATUS = "OPEN — actual cost not supplied"
COST_STATUS = "NOT AVAILABLE — no numeric cost populated"

MODEL_OUTPUT_KEYS = (
    "scenarios",
    "value_ledger",
    "cost_requirements",
    "assumptions",
)
SCENARIO_COLUMNS = (
    "scenario_id",
    "scenario_name",
    "scenario_purpose",
    "liquidity_screen_usd",
    "liquidity_evidence_status",
    "closure_validation_candidates",
    "candidate_fee_sensitivity_usd_annual",
    "candidate_fee_sensitivity_basis",
    "evidenced_two_account_fee_range_low_usd_annual",
    "evidenced_two_account_fee_range_high_usd_annual",
    "evidenced_two_account_fee_range_role",
    "fee_evidence_status",
    "capacity_hypothesis_hours_monthly",
    "capacity_hypothesis_hours_annual",
    "capacity_evidence_status",
    "risk_value_status",
    "validated_value_usd",
    "funded_value_usd",
    "recognized_value_usd",
    "actual_cost_status",
    "benefit_ramp_status",
    "roi_npv_payback_status",
    "initial_envelope_low_usd",
    "initial_envelope_high_usd",
    "initial_envelope_role",
    "recommendation_test",
    "model_version",
)
VALUE_LEDGER_COLUMNS = (
    "scenario_id",
    "scenario_name",
    "value_category",
    "value_category_name",
    "diagnostic_quantity",
    "diagnostic_unit",
    "evidence_status",
    "validated_value_usd",
    "funded_value_usd",
    "recognized_value_usd",
    "value_owner",
    "required_gate_ids",
    "decision_boundary",
    "aggregation_rule",
    "model_version",
)
COST_REQUIREMENT_COLUMNS = (
    "cost_requirement_id",
    "cost_category",
    "evidence_required",
    "source_document_required",
    "proposed_accountable_owner",
    "timing_or_ramp_required",
    "current_evidence_status",
    "current_cost_status",
    "model_use",
    "envelope_role",
    "model_version",
)
ASSUMPTION_COLUMNS = (
    "assumption_id",
    "assumption_or_evidence_gap",
    "used_in",
    "downside_value",
    "base_value",
    "upside_value",
    "unit",
    "evidence_class",
    "source_or_rationale",
    "current_recognized_value_usd",
    "sensitivity",
    "validation_action",
    "proposed_owner",
    "decision_gate",
    "status",
)
CONTROL_COLUMNS = (
    "control_id",
    "control_name",
    "control_rule",
    "observed_result",
    "control_status",
    "evidence_gate_status",
    "failure_action",
    "proposed_owner",
    "model_version",
)
CONTROL_IDS = tuple(f"BC{number:02d}" for number in range(1, 13))
CONTROL_EVIDENCE_GATE_STATUS = {
    "BC01": "OPEN",
    "BC02": "OPEN",
    "BC03": "BLOCKED",
    "BC04": "BLOCKED",
    "BC05": "BLOCKED",
    "BC06": "BLOCKED",
    "BC07": "BLOCKED",
    "BC08": "OPEN",
    "BC09": "BLOCKED",
    "BC10": "OPEN",
    "BC11": "OPEN",
    "BC12": "OPEN",
}

SCENARIO_INPUTS: Dict[str, Dict[str, object]] = {
    "downside": {
        "scenario_name": "Manager challenge / downside",
        "liquidity_screen_usd": 21_000_000,
        "closure_validation_candidates": 2,
        "candidate_fee_sensitivity_usd_annual": 3_900,
        "candidate_fee_sensitivity_basis": (
            "Independent 50% × $7,800 portfolio sensitivity; not the fee sum "
            "for the two candidate-count hypothesis"
        ),
        "capacity_hypothesis_hours_monthly": 50,
        "purpose": (
            "Tests the conditional design direction at the $21m screen, two "
            "candidate validations, an independent 50% fee sensitivity, and "
            "one-third of the 150-hour target"
        ),
    },
    "base": {
        "scenario_name": "Base diagnostic hypothesis",
        "liquidity_screen_usd": 35_000_000,
        "closure_validation_candidates": 4,
        "candidate_fee_sensitivity_usd_annual": 7_800,
        "candidate_fee_sensitivity_basis": (
            "Full four-candidate estimated-fee portfolio sensitivity; not "
            "approved or realized annual P&L"
        ),
        "capacity_hypothesis_hours_monthly": 150,
        "purpose": (
            "Preserves the Week 2 design hypotheses without treating them as "
            "validated, funded, recognized, or cashable value"
        ),
    },
    "upside": {
        "scenario_name": "Upper diagnostic hypothesis",
        "liquidity_screen_usd": 46_200_000,
        "closure_validation_candidates": 4,
        "candidate_fee_sensitivity_usd_annual": 7_800,
        "candidate_fee_sensitivity_basis": (
            "Full four-candidate estimated-fee portfolio sensitivity; not "
            "approved or realized annual P&L"
        ),
        "capacity_hypothesis_hours_monthly": 150,
        "purpose": (
            "Retains the prior upper liquidity hypothesis while refusing to "
            "invent unsupported account closures or capacity"
        ),
    },
}

VALUE_CATEGORIES = (
    "cash_release",
    "annual_p_and_l",
    "capacity",
    "risk",
)

VALUE_CATEGORY_DETAILS: Dict[str, Dict[str, str]] = {
    "cash_release": {
        "value_category_name": "Cash release",
        "diagnostic_unit": "USD liquidity screen",
        "value_owner": "Group Treasurer; Finance validates recognition",
        "required_gate_ids": "VG01; VG02; VG03; VG04; VG05",
        "boundary": (
            "Screening hypothesis only; not surplus, transferable cash, a "
            "funded case, or transfer authority"
        ),
    },
    "annual_p_and_l": {
        "value_category_name": "Annual P&L",
        "diagnostic_unit": "USD/year fee sensitivity",
        "value_owner": "Finance; local account owners validate closure",
        "required_gate_ids": "VG06; VG07",
        "boundary": (
            "Arithmetic portfolio sensitivity on estimated annual candidate "
            "fees; downside $3,900 is independently 50% × $7,800, not the fee "
            "sum for the two candidate-count hypothesis; no closure is approved "
            "and no fee removal is evidenced"
        ),
    },
    "capacity": {
        "value_category_name": "Capacity",
        "diagnostic_unit": "hours/month hypothesis",
        "value_owner": "Shared Services Lead; Finance approves value treatment",
        "required_gate_ids": "VG08; VG09; VG10",
        "boundary": (
            "Productive-capacity hypothesis only; not observed time, removed "
            "labor, headcount reduction, cash saving, or P&L"
        ),
    },
    "risk": {
        "value_category_name": "Risk",
        "diagnostic_unit": "unquantified exposure/value",
        "value_owner": "Management control owner; Finance validates valuation",
        "required_gate_ids": "VG11; VG12",
        "boundary": (
            "Risk exposure and value are not quantified; no incident baseline, "
            "exposure distribution, or Finance-approved valuation is supplied; "
            "$0 is only the current recognized-value ledger entry"
        ),
    },
}

VALUE_GATES: Dict[str, Dict[str, str]] = {
    "VG01": {
        "value_category": "cash_release",
        "evidence_required": (
            "Account-level authoritative balance type, source timestamp, "
            "reconciliation result, and accountable data owner"
        ),
        "proposed_owner": "Group Treasurer / CIO",
    },
    "VG02": {
        "value_category": "cash_release",
        "evidence_required": (
            "Legal, tax, regulatory, purpose, and local transferability "
            "certification by entity and account"
        ),
        "proposed_owner": "Legal / Tax / Regional Finance",
    },
    "VG03": {
        "value_category": "cash_release",
        "evidence_required": (
            "Approved operating buffers, complete forecast/payment population, "
            "receipts, seasonality, settlement calendar, and extraordinary events"
        ),
        "proposed_owner": "Group Treasurer / Regional Finance",
    },
    "VG04": {
        "value_category": "cash_release",
        "evidence_required": (
            "Transfer timing, facility use, borrowing rates, transfer charges, "
            "tax leakage, FX effects, and counterfactual funding action"
        ),
        "proposed_owner": "Group Treasurer / Finance",
    },
    "VG05": {
        "value_category": "cash_release",
        "evidence_required": (
            "Finance-approved cash-release definition, value owner, measurement "
            "window, attribution rule, and realization evidence"
        ),
        "proposed_owner": "CFO / Finance",
    },
    "VG06": {
        "value_category": "annual_p_and_l",
        "evidence_required": (
            "Local validation of purpose, receipts, direct debits, linked "
            "services, signatories, regulatory need, and continuity for each candidate"
        ),
        "proposed_owner": "Regional Finance / Treasury",
    },
    "VG07": {
        "value_category": "annual_p_and_l",
        "evidence_required": (
            "Actual bank invoice, closure cost, closure completion, fee removal, "
            "measurement period, and Finance recognition"
        ),
        "proposed_owner": "Treasury / Finance",
    },
    "VG08": {
        "value_category": "capacity",
        "evidence_required": (
            "Source-population reconciliation and comparable process/payment "
            "scope before any baselines are combined"
        ),
        "proposed_owner": "Shared Services / Data owner",
    },
    "VG09": {
        "value_category": "capacity",
        "evidence_required": (
            "Observed time sample separating required control work, avoidable "
            "rework, demand displacement, and implementation effort"
        ),
        "proposed_owner": "Shared Services / Controls",
    },
    "VG10": {
        "value_category": "capacity",
        "evidence_required": (
            "Sustained removal rate, named productive redeployment, no service or "
            "control degradation, and Finance-approved value treatment"
        ),
        "proposed_owner": "Shared Services Lead / Finance",
    },
    "VG11": {
        "value_category": "risk",
        "evidence_required": (
            "Defined risk event, exposure population, incident/control-failure "
            "baseline, likelihood, severity, and loss history"
        ),
        "proposed_owner": "Management control owner",
    },
    "VG12": {
        "value_category": "risk",
        "evidence_required": (
            "Finance-approved valuation method, attribution, confidence range, "
            "and evidence that the intervention changes exposure"
        ),
        "proposed_owner": "Risk / Finance",
    },
}

COST_REQUIREMENTS: Dict[str, Dict[str, str]] = {
    "CR01": {
        "cost_category": "Software, licenses, and subscriptions",
        "evidence_required": "Vendor quote by module, user, volume, term, and currency",
        "source_document": "Executed quote or procurement-validated proposal",
        "proposed_owner": "CIO / Procurement",
        "timing_or_ramp_required": "One-time and recurring start dates; indexation and renewal",
    },
    "CR02": {
        "cost_category": "Integration and data engineering",
        "evidence_required": (
            "Effort and rate by bank interface, three ERP environments, data "
            "quality remediation, testing, and legacy transition"
        ),
        "source_document": "Architecture estimate and supplier statement of work",
        "proposed_owner": "CIO / Enterprise Architecture",
        "timing_or_ramp_required": "Build profile by month and dependency",
    },
    "CR03": {
        "cost_category": "Cybersecurity, access, and control assurance",
        "evidence_required": (
            "Design, segregation-of-duties, access, audit-trail, penetration, "
            "resilience, and control-testing effort"
        ),
        "source_document": "Cyber/control workplan and resourced estimate",
        "proposed_owner": "CISO / Management control owner",
        "timing_or_ramp_required": "Pre-launch, launch, and recurring assurance",
    },
    "CR04": {
        "cost_category": "Pilot, testing, and program delivery",
        "evidence_required": (
            "Internal and external team, environments, data preparation, PMO, "
            "quality assurance, and rollback rehearsal"
        ),
        "source_document": "Resource plan and approved rate card",
        "proposed_owner": "Program sponsor / PMO",
        "timing_or_ramp_required": "Pilot mobilization through exit decision",
    },
    "CR05": {
        "cost_category": "Change, training, and local adoption",
        "evidence_required": (
            "Role-by-region training, communications, procedure changes, local "
            "validation, travel, and hypercare"
        ),
        "source_document": "Adoption plan and bottom-up resource estimate",
        "proposed_owner": "Business change lead / Regional Finance",
        "timing_or_ramp_required": "Cohort schedule and hypercare duration",
    },
    "CR06": {
        "cost_category": "Internal capacity and backfill",
        "evidence_required": (
            "Named role effort, loaded rates, approved backfill, opportunity cost, "
            "and treatment of business-as-usual work"
        ),
        "source_document": "Approved staffing plan and Finance rate source",
        "proposed_owner": "Functional owners / Finance",
        "timing_or_ramp_required": "Monthly demand and release profile",
    },
    "CR07": {
        "cost_category": "Bank, account, transfer, tax, and FX costs",
        "evidence_required": (
            "Actual bank tariffs, closure charges, transfer costs, tax leakage, "
            "FX effects, and local-market costs"
        ),
        "source_document": "Bank invoices/contracts and Legal/Tax assessment",
        "proposed_owner": "Treasury / Tax / Procurement",
        "timing_or_ramp_required": "By transaction/account and implementation wave",
    },
    "CR08": {
        "cost_category": "Run support, hosting, and service management",
        "evidence_required": (
            "Support model, hosting, monitoring, incident response, service desk, "
            "data operations, and ongoing control operation"
        ),
        "source_document": "Target operating cost model and service agreements",
        "proposed_owner": "CIO / Service owners",
        "timing_or_ramp_required": "Steady-state annual run rate and ramp",
    },
    "CR09": {
        "cost_category": "Decommissioning, exit, and contingency",
        "evidence_required": (
            "Legacy exit, dual running, data retention, contract termination, "
            "rollback, contingency basis, and range methodology"
        ),
        "source_document": "Exit plan, contracts, and risk-based estimate",
        "proposed_owner": "CIO / Procurement / Finance",
        "timing_or_ramp_required": "Dual-run duration, exit date, and contingency release",
    },
    "CR10": {
        "cost_category": "Cost and benefit timing model",
        "evidence_required": (
            "Low/base/high cost range, cash-flow timing, benefit start, ramp, "
            "persistence, attribution, discount rate, and horizon"
        ),
        "source_document": "Finance-approved integrated cost/value model",
        "proposed_owner": "Finance",
        "timing_or_ramp_required": "Monthly cash flow over the approved horizon",
    },
}


def _load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise AssertionError(f"Required evidence file is missing: {path}")
    return pd.read_csv(path, keep_default_na=False)


def validate_week2_evidence() -> Dict[str, float]:
    """Reconcile the governed Week 3 hypotheses to stored Week 2 outputs."""
    thresholds = _load_csv(PROCESSED / "W2_liquidity_thresholds.csv")
    accounts = _load_csv(PROCESSED / "W2_account_diagnostic.csv")
    process = _load_csv(PROCESSED / "W2_process_capacity.csv")
    metrics = _load_csv(PROCESSED / "W2_reconciliation_metrics.csv")
    repair = _load_csv(PROCESSED / "W2_repair_baseline_reconciliation.csv")

    required_threshold_columns = {
        "buffer_window_days",
        "threshold_name",
        "threshold_usd",
        "complete_window_days",
        "days_threshold_met",
        "decision_boundary",
    }
    required_account_columns = {
        "account_id",
        "annual_fee_usd",
        "closure_validation_candidate",
        "decision_boundary",
    }
    required_process_columns = {
        "process",
        "manual_hours_monthly",
        "decision_boundary",
    }
    if not required_threshold_columns.issubset(thresholds.columns):
        raise AssertionError("Week 2 liquidity-threshold schema changed")
    if not required_account_columns.issubset(accounts.columns):
        raise AssertionError("Week 2 account-diagnostic schema changed")
    if not required_process_columns.issubset(process.columns):
        raise AssertionError("Week 2 process-capacity schema changed")

    threshold_14d = thresholds.loc[
        thresholds["buffer_window_days"].eq(14)
    ].set_index("threshold_name")
    if set(threshold_14d.index) != {"stress", "base", "upside"}:
        raise AssertionError("Week 2 14-day threshold population changed")
    expected_thresholds = {
        "stress": (21_000_000, 168, 168),
        "base": (35_000_000, 168, 138),
        "upside": (46_200_000, 168, 0),
    }
    for name, (amount, complete, met) in expected_thresholds.items():
        row = threshold_14d.loc[name]
        if (
            float(row["threshold_usd"]) != amount
            or int(row["complete_window_days"]) != complete
            or int(row["days_threshold_met"]) != met
            or "no threshold is validated movable cash"
            not in str(row["decision_boundary"])
        ):
            raise AssertionError(f"Week 2 {name} liquidity evidence changed")

    candidate_flag = accounts["closure_validation_candidate"].astype(str).str.lower()
    candidates = accounts.loc[candidate_flag.eq("true")]
    if len(candidates) != 4 or float(candidates["annual_fee_usd"].sum()) != 7_800:
        raise AssertionError("Week 2 closure-candidate evidence changed")
    candidate_fees = sorted(candidates["annual_fee_usd"].astype(int).tolist())
    two_candidate_fee_range = (
        sum(candidate_fees[:2]),
        sum(candidate_fees[-2:]),
    )
    if two_candidate_fee_range != (
        TWO_ACCOUNT_FEE_RANGE_LOW_USD_ANNUAL,
        TWO_ACCOUNT_FEE_RANGE_HIGH_USD_ANNUAL,
    ):
        raise AssertionError("Week 2 two-candidate fee range changed")
    if not candidates["decision_boundary"].str.contains("not validated").all():
        raise AssertionError("Week 2 account-closure boundary changed")

    total_process_hours = round(float(process["manual_hours_monthly"].sum()), 2)
    if len(process) != 9 or total_process_hours != 617.72:
        raise AssertionError("Week 2 process-capacity evidence changed")
    if not process["decision_boundary"].str.contains("not observed labor").all():
        raise AssertionError("Week 2 capacity boundary changed")

    metric_lookup = metrics.set_index("metric")["value"].astype(float).to_dict()
    if metric_lookup.get("payment_records") != 7_600:
        raise AssertionError("Week 2 payment-record population changed")
    if metric_lookup.get("gross_supplied_payment_value") != 198_135_489.50:
        raise AssertionError("Week 2 supplied payment value changed")

    repair_lookup = repair.set_index("metric")["value"].astype(float).to_dict()
    if repair_lookup.get("payment_file_repair_hours_monthly") != 55.7778:
        raise AssertionError("Week 2 payment-file repair baseline changed")
    if repair_lookup.get("process_file_exception_manual_hours_monthly") != 102.6:
        raise AssertionError("Week 2 process-file repair baseline changed")

    return {
        "stress_liquidity_screen_usd": 21_000_000,
        "base_liquidity_screen_usd": 35_000_000,
        "upside_liquidity_screen_usd": 46_200_000,
        "closure_validation_candidates": 4,
        "candidate_fee_sensitivity_usd_annual": 7_800,
        "two_candidate_fee_range_low_usd_annual": 1_800,
        "two_candidate_fee_range_high_usd_annual": 6_000,
        "estimated_manual_process_hours_monthly": 617.72,
        "payment_file_repair_hours_monthly": 55.7778,
        "process_file_repair_hours_monthly": 102.6,
        "payment_records": 7_600,
        "gross_supplied_payment_value": 198_135_489.50,
    }


def build_scenario_table() -> pd.DataFrame:
    """Build the governed downside/base/upside diagnostic hypotheses."""
    rows = []
    for scenario_id, inputs in SCENARIO_INPUTS.items():
        monthly_hours = int(inputs["capacity_hypothesis_hours_monthly"])
        rows.append(
            {
                "scenario_id": scenario_id,
                "scenario_name": inputs["scenario_name"],
                "scenario_purpose": inputs["purpose"],
                "liquidity_screen_usd": int(inputs["liquidity_screen_usd"]),
                "liquidity_evidence_status": LIQUIDITY_EVIDENCE_STATUS[
                    scenario_id
                ],
                "closure_validation_candidates": int(
                    inputs["closure_validation_candidates"]
                ),
                "candidate_fee_sensitivity_usd_annual": int(
                    inputs["candidate_fee_sensitivity_usd_annual"]
                ),
                "candidate_fee_sensitivity_basis": inputs[
                    "candidate_fee_sensitivity_basis"
                ],
                "evidenced_two_account_fee_range_low_usd_annual": (
                    TWO_ACCOUNT_FEE_RANGE_LOW_USD_ANNUAL
                ),
                "evidenced_two_account_fee_range_high_usd_annual": (
                    TWO_ACCOUNT_FEE_RANGE_HIGH_USD_ANNUAL
                ),
                "evidenced_two_account_fee_range_role": TWO_ACCOUNT_FEE_RANGE_ROLE,
                "fee_evidence_status": FEE_EVIDENCE_STATUS,
                "capacity_hypothesis_hours_monthly": monthly_hours,
                "capacity_hypothesis_hours_annual": monthly_hours * 12,
                "capacity_evidence_status": CAPACITY_EVIDENCE_STATUS,
                "risk_value_status": RISK_VALUE_STATUS,
                "validated_value_usd": 0,
                "funded_value_usd": 0,
                "recognized_value_usd": 0,
                "actual_cost_status": "NOT AVAILABLE",
                "benefit_ramp_status": "NOT AVAILABLE",
                "roi_npv_payback_status": "NOT AVAILABLE",
                "initial_envelope_low_usd": INITIAL_ENVELOPE_LOW_USD,
                "initial_envelope_high_usd": INITIAL_ENVELOPE_HIGH_USD,
                "initial_envelope_role": ENVELOPE_ROLE,
                "recommendation_test": RECOMMENDATION_TEST,
                "model_version": MODEL_VERSION,
            }
        )
    return pd.DataFrame(rows, columns=SCENARIO_COLUMNS)


def _diagnostic_quantity(scenario: Mapping[str, object], category: str) -> object:
    if category == "cash_release":
        return str(int(scenario["liquidity_screen_usd"]))
    if category == "annual_p_and_l":
        return str(int(scenario["candidate_fee_sensitivity_usd_annual"]))
    if category == "capacity":
        return str(int(scenario["capacity_hypothesis_hours_monthly"]))
    if category == "risk":
        return "NOT QUANTIFIED"
    raise AssertionError(f"Unknown value category: {category}")


def build_value_ledger(scenarios: pd.DataFrame) -> pd.DataFrame:
    """Build a non-additive ledger with a zero recognized-value floor."""
    rows = []
    for scenario in scenarios.to_dict("records"):
        for category in VALUE_CATEGORIES:
            details = VALUE_CATEGORY_DETAILS[category]
            rows.append(
                {
                    "scenario_id": scenario["scenario_id"],
                    "scenario_name": scenario["scenario_name"],
                    "value_category": category,
                    "value_category_name": details["value_category_name"],
                    "diagnostic_quantity": _diagnostic_quantity(scenario, category),
                    "diagnostic_unit": details["diagnostic_unit"],
                    "evidence_status": LEDGER_EVIDENCE_STATUS,
                    "validated_value_usd": 0,
                    "funded_value_usd": 0,
                    "recognized_value_usd": 0,
                    "value_owner": details["value_owner"],
                    "required_gate_ids": details["required_gate_ids"],
                    "decision_boundary": details["boundary"],
                    "aggregation_rule": AGGREGATION_RULE,
                    "model_version": MODEL_VERSION,
                }
            )
    return pd.DataFrame(rows, columns=VALUE_LEDGER_COLUMNS)


def build_cost_requirements() -> pd.DataFrame:
    """Enumerate evidence required before an investment case can be calculated."""
    rows = []
    for requirement_id, requirement in COST_REQUIREMENTS.items():
        rows.append(
            {
                "cost_requirement_id": requirement_id,
                "cost_category": requirement["cost_category"],
                "evidence_required": requirement["evidence_required"],
                "source_document_required": requirement["source_document"],
                "proposed_accountable_owner": requirement["proposed_owner"],
                "timing_or_ramp_required": requirement["timing_or_ramp_required"],
                "current_evidence_status": COST_EVIDENCE_STATUS,
                "current_cost_status": COST_STATUS,
                "model_use": COST_MODEL_USE,
                "envelope_role": ENVELOPE_ROLE,
                "model_version": MODEL_VERSION,
            }
        )
    return pd.DataFrame(rows, columns=COST_REQUIREMENT_COLUMNS)


def build_assumptions_register() -> pd.DataFrame:
    """Build the Week 3 assumptions and evidence-gate register."""
    rows = []
    for gate_id, gate in VALUE_GATES.items():
        rows.append(
            {
                "assumption_id": gate_id,
                "assumption_or_evidence_gap": gate["evidence_required"],
                "used_in": VALUE_CATEGORY_DETAILS[gate["value_category"]][
                    "value_category_name"
                ],
                "downside_value": "N/A",
                "base_value": "N/A",
                "upside_value": "N/A",
                "unit": "Evidence gate",
                "evidence_class": "CLIENT / CONTROL EVIDENCE REQUIRED",
                "source_or_rationale": "Week 2 evidence gap retained into Week 3",
                "current_recognized_value_usd": 0,
                "sensitivity": "High",
                "validation_action": gate["evidence_required"],
                "proposed_owner": gate["proposed_owner"],
                "decision_gate": "Required before benefit recognition",
                "status": "Open",
            }
        )

    scenario_rows = [
        {
            "assumption_id": "SA01",
            "assumption_or_evidence_gap": (
                "The $21m/$35m/$46.2m amounts are 14-day liquidity screens, "
                "not validated movable cash"
            ),
            "used_in": "Cash release diagnostic scenarios",
            "downside_value": "21000000",
            "base_value": "35000000",
            "upside_value": "46200000",
            "unit": "USD screening hypothesis",
            "evidence_class": "ANALYST-ASSUMPTION",
            "source_or_rationale": (
                "W2_liquidity_thresholds.csv; 14-day thresholds pass "
                "168/168, 138/168, and 0/168 complete windows"
            ),
            "current_recognized_value_usd": 0,
            "sensitivity": "High",
            "validation_action": (
                "Close VG01-VG05 at account level and obtain Finance approval"
            ),
            "proposed_owner": "Group Treasurer / Finance",
            "decision_gate": "No cash value or movement before certification",
            "status": "Open — screen reconciled; value unvalidated",
        },
        {
            "assumption_id": "SA02",
            "assumption_or_evidence_gap": (
                "Only 2/4/4 of the four closure-validation candidates are used "
                "in downside/base/upside; ten closures remain unsupported"
            ),
            "used_in": "Annual P&L diagnostic scenarios",
            "downside_value": "2",
            "base_value": "4",
            "upside_value": "4",
            "unit": "validation candidates",
            "evidence_class": "ANALYST-ASSUMPTION",
            "source_or_rationale": (
                "W2_account_diagnostic.csv; four narrow-screen candidates"
            ),
            "current_recognized_value_usd": 0,
            "sensitivity": "High",
            "validation_action": "Close VG06-VG07 for each account",
            "proposed_owner": "Treasury / Regional Finance / Finance",
            "decision_gate": "No closure or P&L until local and invoice validation",
            "status": "Open — candidates only",
        },
        {
            "assumption_id": "SA03",
            "assumption_or_evidence_gap": (
                "$3,900 is an independent 50% × $7,800 portfolio sensitivity, "
                "not the fee sum for whichever two candidates validate; the "
                "base/upside $7,800 is the full four-candidate estimate"
            ),
            "used_in": "Annual P&L diagnostic scenarios",
            "downside_value": "3900",
            "base_value": "7800",
            "upside_value": "7800",
            "unit": "USD/year fee sensitivity",
            "evidence_class": "ANALYST-CALC / ANALYST-ASSUMPTION",
            "source_or_rationale": (
                "Independent 50%/100%/100% sensitivities on the Week 2 $7,800 "
                "portfolio; actual fees for any two evidenced candidates range "
                "from $1,800 to $6,000"
            ),
            "current_recognized_value_usd": 0,
            "sensitivity": "High",
            "validation_action": "Validate invoices, closure cost, and actual fee removal",
            "proposed_owner": "Treasury / Finance",
            "decision_gate": "Finance recognition after evidenced removal",
            "status": "Open — arithmetic only",
        },
        {
            "assumption_id": "SA04",
            "assumption_or_evidence_gap": (
                "50/150/150 hours per month represent productive-capacity "
                "hypotheses, not labor removal or monetary savings"
            ),
            "used_in": "Capacity diagnostic scenarios",
            "downside_value": "50",
            "base_value": "150",
            "upside_value": "150",
            "unit": "hours/month hypothesis",
            "evidence_class": "ANALYST-ASSUMPTION",
            "source_or_rationale": (
                "Manager downside and Week 2 target against a 617.72-hour "
                "management-estimated process screen"
            ),
            "current_recognized_value_usd": 0,
            "sensitivity": "High",
            "validation_action": "Close VG08-VG10 through observation and redeployment evidence",
            "proposed_owner": "Shared Services Lead / Finance",
            "decision_gate": "No P&L or headcount claim before Finance approval",
            "status": "Open — hypothesis only",
        },
        {
            "assumption_id": "SA05",
            "assumption_or_evidence_gap": (
                "The FY2026 $1.0-$1.5m envelope is only an initial-stage ceiling"
            ),
            "used_in": "Affordability and staging",
            "downside_value": "N/A",
            "base_value": "N/A",
            "upside_value": "N/A",
            "unit": "USD ceiling range",
            "evidence_class": "CLIENT-PROVIDED CONSTRAINT",
            "source_or_rationale": (
                "Start-of-Week-3 CFO constraint: FY2026 initial-stage ceiling "
                "$1.0–$1.5m; not a scenario value"
            ),
            "current_recognized_value_usd": 0,
            "sensitivity": "High",
            "validation_action": (
                "Obtain bottom-up cost range; stage or return for approval if above ceiling"
            ),
            "proposed_owner": "CFO / Finance / CIO",
            "decision_gate": "Not cost, budget approval, or spend authority",
            "status": "Constraint confirmed; cost evidence open",
        },
        {
            "assumption_id": "SA06",
            "assumption_or_evidence_gap": (
                "Actual implementation/run cost and benefit ramp are unavailable"
            ),
            "used_in": "ROI / NPV / payback",
            "downside_value": "NOT AVAILABLE",
            "base_value": "NOT AVAILABLE",
            "upside_value": "NOT AVAILABLE",
            "unit": "Model status",
            "evidence_class": "NOT ESTABLISHED",
            "source_or_rationale": "No validated cost, timing, or ramp evidence supplied",
            "current_recognized_value_usd": 0,
            "sensitivity": "High",
            "validation_action": "Close CR01-CR10 and the relevant value gates",
            "proposed_owner": "Finance / CIO / value owners",
            "decision_gate": "ROI, NPV, payback, and funding case unavailable",
            "status": "Open — calculation blocked",
        },
        {
            "assumption_id": "SA07",
            "assumption_or_evidence_gap": (
                "Risk exposure and value remain unquantified until evidence and "
                "an approved valuation method exist"
            ),
            "used_in": "Risk value",
            "downside_value": "NOT QUANTIFIED",
            "base_value": "NOT QUANTIFIED",
            "upside_value": "NOT QUANTIFIED",
            "unit": "Qualitative category",
            "evidence_class": "NOT ESTABLISHED",
            "source_or_rationale": "No incident/exposure distribution or approved valuation supplied",
            "current_recognized_value_usd": 0,
            "sensitivity": "High",
            "validation_action": "Close VG11-VG12",
            "proposed_owner": "Management control owner / Risk / Finance",
            "decision_gate": "No aggregation with cash, P&L, or capacity",
            "status": "Open — exposure and value not quantified",
        },
    ]
    rows.extend(scenario_rows)
    return pd.DataFrame(rows, columns=ASSUMPTION_COLUMNS)


def _exact_frame_failures(
    name: str,
    actual: object,
    expected: pd.DataFrame,
    expected_columns: tuple,
) -> list:
    """Return contract failures without trusting the incoming frame schema."""
    if not isinstance(actual, pd.DataFrame):
        return [f"{name} is not a DataFrame"]
    failures = []
    if tuple(actual.columns) != expected_columns:
        failures.append(f"{name} schema or column order changed")
        return failures
    try:
        assert_frame_equal(
            actual.reset_index(drop=True),
            expected.reset_index(drop=True),
            check_dtype=False,
            check_exact=True,
        )
    except AssertionError:
        failures.append(f"{name} content, row order, or governed value changed")
    return failures


def validate_model_contract(outputs: Mapping[str, pd.DataFrame]) -> None:
    """Fail closed against the complete Week 3 validation-case contract."""
    if tuple(outputs) != MODEL_OUTPUT_KEYS:
        raise AssertionError(
            "Week 3 validation-case failures: output keys or order changed"
        )

    expected_scenarios = build_scenario_table()
    expected_ledger = build_value_ledger(expected_scenarios)
    expected_costs = build_cost_requirements()
    expected_assumptions = build_assumptions_register()
    failures = []
    failures.extend(
        _exact_frame_failures(
            "scenarios", outputs["scenarios"], expected_scenarios, SCENARIO_COLUMNS
        )
    )
    failures.extend(
        _exact_frame_failures(
            "value_ledger",
            outputs["value_ledger"],
            expected_ledger,
            VALUE_LEDGER_COLUMNS,
        )
    )
    failures.extend(
        _exact_frame_failures(
            "cost_requirements",
            outputs["cost_requirements"],
            expected_costs,
            COST_REQUIREMENT_COLUMNS,
        )
    )
    failures.extend(
        _exact_frame_failures(
            "assumptions",
            outputs["assumptions"],
            expected_assumptions,
            ASSUMPTION_COLUMNS,
        )
    )

    scenarios = outputs["scenarios"]
    ledger = outputs["value_ledger"]
    costs = outputs["cost_requirements"]
    assumptions = outputs["assumptions"]
    if tuple(scenarios.columns) == SCENARIO_COLUMNS:
        if scenarios["scenario_id"].duplicated().any():
            failures.append("scenario IDs are duplicated")
    if tuple(ledger.columns) == VALUE_LEDGER_COLUMNS:
        expected_pairs = [
            (scenario_id, category)
            for scenario_id in SCENARIO_INPUTS
            for category in VALUE_CATEGORIES
        ]
        actual_pairs = list(
            ledger[["scenario_id", "value_category"]].itertuples(
                index=False, name=None
            )
        )
        if actual_pairs != expected_pairs:
            failures.append("value ledger is not the exact ordered 3x4 cartesian set")
        if ledger.duplicated(["scenario_id", "value_category"]).any():
            failures.append("scenario/value-category keys are duplicated")
    if tuple(costs.columns) == COST_REQUIREMENT_COLUMNS:
        if list(costs["cost_requirement_id"]) != list(COST_REQUIREMENTS):
            failures.append("cost requirement IDs or order changed")
        if costs["cost_requirement_id"].duplicated().any():
            failures.append("cost requirement IDs are duplicated")
    if tuple(assumptions.columns) == ASSUMPTION_COLUMNS:
        required_assumption_ids = list(VALUE_GATES) + [
            f"SA{number:02d}" for number in range(1, 8)
        ]
        if list(assumptions["assumption_id"]) != required_assumption_ids:
            failures.append("assumption IDs, population, or order changed")
        if assumptions["assumption_id"].duplicated().any():
            failures.append("assumption IDs are duplicated")
        if assumptions["decision_gate"].replace("", pd.NA).isna().any():
            failures.append("an assumption decision gate is missing")

    if failures:
        raise AssertionError(f"Week 3 validation-case failures: {failures}")


def build_business_case_model() -> Dict[str, pd.DataFrame]:
    """Build, validate, and return every governed validation-case output."""
    validate_week2_evidence()
    scenarios = build_scenario_table()
    outputs = {
        "scenarios": scenarios,
        "value_ledger": build_value_ledger(scenarios),
        "cost_requirements": build_cost_requirements(),
        "assumptions": build_assumptions_register(),
    }
    validate_model_contract(outputs)
    return outputs


def _control_rows() -> Iterable[dict]:
    """Yield the canonical control definitions; never derive control text ad hoc."""
    yield {
        "control_id": "BC01",
        "control_name": "Week 2 evidence reconciliation",
        "control_rule": (
            "Reconcile $21m/$35m/$46.2m screens, 4 candidates/$7,800, "
            "617.72 hours/month, and independent repair baselines"
        ),
        "observed_result": "All governed Week 2 anchors reconcile exactly",
        "failure_action": "Stop generation and investigate source change",
        "proposed_owner": "Baker / data owners",
    }
    yield {
        "control_id": "BC02",
        "control_name": "Diagnostic scenario boundary",
        "control_rule": "Scenario quantities must be labelled hypotheses, not benefits",
        "observed_result": "Three scenario rows retain screen/sensitivity/hypothesis labels",
        "failure_action": "Reject scenario output",
        "proposed_owner": "Finance / value owners",
    }
    for control_id, category, name in [
        ("BC03", "cash_release", "Cash-release recognition gate"),
        ("BC04", "annual_p_and_l", "Annual P&L recognition gate"),
        ("BC05", "capacity", "Capacity recognition gate"),
        ("BC06", "risk", "Risk-valuation gate"),
    ]:
        if category == "risk":
            control_rule = (
                "Risk exposure and value remain NOT QUANTIFIED; $0 appears only "
                "as the current recognized-value ledger entry"
            )
            observed_result = (
                "Three risk rows retain NOT QUANTIFIED diagnostic quantities "
                "and $0 recognized-value entries"
            )
        else:
            control_rule = (
                "Validated, funded, and recognized USD remain zero until all "
                "category evidence gates close"
            )
            observed_result = (
                "3 scenario rows remain open with all value fields at $0"
            )
        yield {
            "control_id": control_id,
            "control_name": name,
            "control_rule": control_rule,
            "observed_result": observed_result,
            "failure_action": "Block value and return to named evidence gates",
            "proposed_owner": VALUE_CATEGORY_DETAILS[category]["value_owner"],
        }
    yield {
        "control_id": "BC07",
        "control_name": "Cost completeness gate",
        "control_rule": "All ten cost categories require sourced amount and timing evidence",
        "observed_result": "10/10 requirements are open; actual cost unavailable",
        "failure_action": "Do not calculate returns or decide funding until populated",
        "proposed_owner": "Finance / CIO / Procurement",
    }
    yield {
        "control_id": "BC08",
        "control_name": "Funding-envelope interpretation",
        "control_rule": "$1.0-$1.5m is a ceiling only and never an estimated cost",
        "observed_result": "Envelope role is explicit on every scenario and cost row",
        "failure_action": "Remove any inferred spend or return calculation",
        "proposed_owner": "CFO / Finance",
    }
    yield {
        "control_id": "BC09",
        "control_name": "Return-metric gate",
        "control_rule": "ROI, NPV, and payback remain unavailable without cost and ramp",
        "observed_result": "Return metric status is NOT AVAILABLE for all scenarios",
        "failure_action": "Block investment-case calculation",
        "proposed_owner": "Finance",
    }
    yield {
        "control_id": "BC10",
        "control_name": "Non-additive value ledger",
        "control_rule": "Never add cash release, P&L, capacity, and risk categories",
        "observed_result": "12/12 ledger rows carry the non-additive rule",
        "failure_action": "Reject aggregate value total",
        "proposed_owner": "Finance",
    }
    yield {
        "control_id": "BC11",
        "control_name": "Conditional downside-boundary control",
        "control_rule": (
            "At $21m, two candidate validations, independent 50% × $7,800 fee "
            "sensitivity, and 50 hours/month, retain federated coordination only "
            "while global data/control ownership, minimum integration readiness, "
            "and affordability remain viable; otherwise use local stabilization"
        ),
        "observed_result": (
            "Conditional direction and fallback are explicit; no robustness, "
            "execution, funding, or benefit conclusion is authorized"
        ),
        "failure_action": (
            "Keep evidence gates open and use local stabilization if any named "
            "condition fails"
        ),
        "proposed_owner": "Steering Committee",
    }
    yield {
        "control_id": "BC12",
        "control_name": "Assumption/evidence ownership",
        "control_rule": "Every value gate names evidence, action, owner, and status",
        "observed_result": "19 governed assumption/evidence rows present",
        "failure_action": "Keep value gate open",
        "proposed_owner": "Value owners / PMO",
    }


def _canonical_controls_frame() -> pd.DataFrame:
    """Return the sole governed 12-row model-control contract."""
    controls = pd.DataFrame(list(_control_rows()))
    controls["control_status"] = "MODEL CONTROL PASS"
    controls["evidence_gate_status"] = controls["control_id"].map(
        CONTROL_EVIDENCE_GATE_STATUS
    )
    controls["model_version"] = MODEL_VERSION
    return controls[list(CONTROL_COLUMNS)]


def build_controls(outputs: Mapping[str, pd.DataFrame]) -> pd.DataFrame:
    """Build an auditable summary of executable model controls."""
    validate_model_contract(outputs)
    controls = _canonical_controls_frame()
    validate_control_contract(controls)
    return controls


def validate_control_contract(controls: pd.DataFrame) -> None:
    """Fail closed on model-control status and evidence-gate semantics."""
    if not isinstance(controls, pd.DataFrame):
        raise AssertionError("Business-case controls are not a DataFrame")
    failures = _exact_frame_failures(
        "controls",
        controls,
        _canonical_controls_frame(),
        CONTROL_COLUMNS,
    )
    if tuple(controls.columns) == CONTROL_COLUMNS:
        if list(controls["control_id"]) != list(CONTROL_IDS):
            failures.append("control IDs, population, or order changed")
        if controls["control_id"].duplicated().any():
            failures.append("control IDs are duplicated")
        if not controls["control_status"].eq("MODEL CONTROL PASS").all():
            failures.append("model-control status changed")
        expected_gate_status = controls["control_id"].map(
            CONTROL_EVIDENCE_GATE_STATUS
        )
        if not controls["evidence_gate_status"].equals(expected_gate_status):
            failures.append("evidence-gate status changed")
        if not controls["evidence_gate_status"].isin({"OPEN", "BLOCKED"}).all():
            failures.append("evidence-gate status implies closure")
        if not controls["model_version"].eq(MODEL_VERSION).all():
            failures.append("control model version changed")
        bc11 = controls.loc[controls["control_id"].eq("BC11")]
        if len(bc11) != 1:
            failures.append("BC11 is missing or duplicated")
        else:
            rule = bc11.iloc[0]["control_rule"]
            required_terms = [
                "global data/control ownership",
                "minimum integration readiness",
                "affordability",
                "local stabilization",
            ]
            if not all(term in rule for term in required_terms):
                failures.append("BC11 conditional switching boundary changed")
    if failures:
        raise AssertionError(f"Week 3 control-contract failures: {failures}")


def write_outputs(outputs: Mapping[str, pd.DataFrame]) -> Dict[str, Path]:
    """Write governed CSVs and verify exact deterministic round trips."""
    validate_model_contract(outputs)
    controls = build_controls(outputs)
    paths = {
        "scenarios": PROCESSED / "W3_business_case_scenarios.csv",
        "value_ledger": PROCESSED / "W3_business_case_value_ledger.csv",
        "cost_requirements": PROCESSED / "W3_cost_evidence_requirements.csv",
        "controls": PROCESSED / "W3_business_case_controls.csv",
        "assumptions": WEEK3 / "W3_assumptions_register.csv",
    }
    frames = {**outputs, "controls": controls}
    for key, path in paths.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        frames[key].to_csv(path, index=False)
        stored = pd.read_csv(path, keep_default_na=False)
        assert_frame_equal(stored, frames[key], check_dtype=False)
    return paths


def main() -> None:
    outputs = build_business_case_model()
    paths = write_outputs(outputs)
    scenario_summary = outputs["scenarios"][[
        "scenario_id",
        "liquidity_screen_usd",
        "closure_validation_candidates",
        "candidate_fee_sensitivity_usd_annual",
        "capacity_hypothesis_hours_monthly",
        "recognized_value_usd",
    ]]
    print("Week 3 validation case generated; no investment case is available.")
    print(scenario_summary.to_string(index=False))
    print("Outputs:")
    for path in paths.values():
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
