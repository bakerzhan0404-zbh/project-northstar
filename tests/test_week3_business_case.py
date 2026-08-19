"""Executable controls for the Week 3 Project Northstar validation case."""

import sys
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from week3_business_case import (  # noqa: E402
    ASSUMPTION_COLUMNS,
    CONTROL_COLUMNS,
    CONTROL_EVIDENCE_GATE_STATUS,
    CONTROL_IDS,
    COST_MODEL_USE,
    COST_REQUIREMENT_COLUMNS,
    COST_REQUIREMENTS,
    COST_STATUS,
    ENVELOPE_ROLE,
    INITIAL_ENVELOPE_HIGH_USD,
    INITIAL_ENVELOPE_LOW_USD,
    MODEL_OUTPUT_KEYS,
    MODEL_VERSION,
    PROCESSED,
    RECOMMENDATION_TEST,
    SCENARIO_COLUMNS,
    SCENARIO_INPUTS,
    TWO_ACCOUNT_FEE_RANGE_HIGH_USD_ANNUAL,
    TWO_ACCOUNT_FEE_RANGE_LOW_USD_ANNUAL,
    VALUE_CATEGORIES,
    VALUE_CATEGORY_DETAILS,
    VALUE_GATES,
    VALUE_LEDGER_COLUMNS,
    WEEK3,
    build_business_case_model,
    build_controls,
    validate_control_contract,
    validate_model_contract,
    validate_week2_evidence,
    write_outputs,
)


def assertion_raises(callable_object) -> bool:
    try:
        callable_object()
    except AssertionError:
        return True
    return False


def clone_outputs(outputs):
    return {key: frame.copy() for key, frame in outputs.items()}


def model_cell_mutation(outputs, frame_key, column, value, row=0):
    changed = clone_outputs(outputs)
    changed[frame_key].loc[changed[frame_key].index[row], column] = value
    return changed


def model_drop_column(outputs, frame_key, column):
    changed = clone_outputs(outputs)
    changed[frame_key] = changed[frame_key].drop(columns=[column])
    return changed


def model_extra_column(outputs, frame_key):
    changed = clone_outputs(outputs)
    changed[frame_key]["unsafe_extra_column"] = "unsafe"
    return changed


def all_model_mutations_fail(mutations) -> bool:
    return all(
        assertion_raises(lambda changed=changed: validate_model_contract(changed))
        for changed in mutations
    )


def all_control_mutations_fail(mutations) -> bool:
    return all(
        assertion_raises(
            lambda changed=changed: validate_control_contract(changed)
        )
        for changed in mutations
    )


def main() -> None:
    evidence = validate_week2_evidence()
    outputs = build_business_case_model()
    scenarios_frame = outputs["scenarios"]
    ledger = outputs["value_ledger"]
    costs = outputs["cost_requirements"]
    assumptions_frame = outputs["assumptions"]
    controls_frame = build_controls(outputs)
    scenarios = scenarios_frame.set_index("scenario_id")
    assumptions = assumptions_frame.set_index("assumption_id")
    controls = controls_frame.set_index("control_id")

    expected_scenarios = {
        "downside": {
            "liquidity_screen_usd": 21_000_000,
            "closure_validation_candidates": 2,
            "candidate_fee_sensitivity_usd_annual": 3_900,
            "capacity_hypothesis_hours_monthly": 50,
            "capacity_hypothesis_hours_annual": 600,
        },
        "base": {
            "liquidity_screen_usd": 35_000_000,
            "closure_validation_candidates": 4,
            "candidate_fee_sensitivity_usd_annual": 7_800,
            "capacity_hypothesis_hours_monthly": 150,
            "capacity_hypothesis_hours_annual": 1_800,
        },
        "upside": {
            "liquidity_screen_usd": 46_200_000,
            "closure_validation_candidates": 4,
            "candidate_fee_sensitivity_usd_annual": 7_800,
            "capacity_hypothesis_hours_monthly": 150,
            "capacity_hypothesis_hours_annual": 1_800,
        },
    }
    expected_quantities = {
        ("downside", "cash_release"): "21000000",
        ("downside", "annual_p_and_l"): "3900",
        ("downside", "capacity"): "50",
        ("downside", "risk"): "NOT QUANTIFIED",
        ("base", "cash_release"): "35000000",
        ("base", "annual_p_and_l"): "7800",
        ("base", "capacity"): "150",
        ("base", "risk"): "NOT QUANTIFIED",
        ("upside", "cash_release"): "46200000",
        ("upside", "annual_p_and_l"): "7800",
        ("upside", "capacity"): "150",
        ("upside", "risk"): "NOT QUANTIFIED",
    }
    expected_units = {
        "cash_release": "USD liquidity screen",
        "annual_p_and_l": "USD/year fee sensitivity",
        "capacity": "hours/month hypothesis",
        "risk": "unquantified exposure/value",
    }
    expected_gate_refs = {
        "cash_release": "VG01; VG02; VG03; VG04; VG05",
        "annual_p_and_l": "VG06; VG07",
        "capacity": "VG08; VG09; VG10",
        "risk": "VG11; VG12",
    }
    expected_owners = {
        "cash_release": "Group Treasurer; Finance validates recognition",
        "annual_p_and_l": "Finance; local account owners validate closure",
        "capacity": "Shared Services Lead; Finance approves value treatment",
        "risk": "Management control owner; Finance validates valuation",
    }

    output_key_mutations = []
    missing_key = clone_outputs(outputs)
    missing_key.pop("assumptions")
    output_key_mutations.append(missing_key)
    extra_key = clone_outputs(outputs)
    extra_key["unsafe_extra_output"] = pd.DataFrame()
    output_key_mutations.append(extra_key)
    reordered_keys = {
        "value_ledger": outputs["value_ledger"].copy(),
        "scenarios": outputs["scenarios"].copy(),
        "cost_requirements": outputs["cost_requirements"].copy(),
        "assumptions": outputs["assumptions"].copy(),
    }
    output_key_mutations.append(reordered_keys)

    scenario_mutations = [
        model_drop_column(outputs, "scenarios", "scenario_name"),
        model_extra_column(outputs, "scenarios"),
        model_cell_mutation(
            outputs, "scenarios", "liquidity_screen_usd", 22_000_000
        ),
        model_cell_mutation(
            outputs, "scenarios", "liquidity_evidence_status", "Validated benefit"
        ),
        model_cell_mutation(
            outputs, "scenarios", "capacity_hypothesis_hours_annual", 601
        ),
        model_cell_mutation(
            outputs, "scenarios", "candidate_fee_sensitivity_basis", "Selected pair"
        ),
        model_cell_mutation(
            outputs,
            "scenarios",
            "evidenced_two_account_fee_range_low_usd_annual",
            3_900,
        ),
        model_cell_mutation(
            outputs, "scenarios", "risk_value_status", "Risk value $0"
        ),
        model_cell_mutation(
            outputs, "scenarios", "recommendation_test", "Federated is robust"
        ),
        model_cell_mutation(
            outputs, "scenarios", "initial_envelope_role", "Cost estimate"
        ),
        model_cell_mutation(outputs, "scenarios", "recognized_value_usd", 1),
        model_cell_mutation(outputs, "scenarios", "actual_cost_status", "$1m"),
        model_cell_mutation(
            outputs, "scenarios", "model_version", "unsafe-version"
        ),
    ]
    missing_scenario = clone_outputs(outputs)
    missing_scenario["scenarios"] = missing_scenario["scenarios"].iloc[:-1]
    scenario_mutations.append(missing_scenario)
    duplicate_scenario = clone_outputs(outputs)
    duplicate_scenario["scenarios"] = pd.concat(
        [duplicate_scenario["scenarios"], duplicate_scenario["scenarios"].iloc[[0]]],
        ignore_index=True,
    )
    scenario_mutations.append(duplicate_scenario)

    ledger_mutations = [
        model_drop_column(outputs, "value_ledger", "diagnostic_unit"),
        model_extra_column(outputs, "value_ledger"),
        model_cell_mutation(
            outputs, "value_ledger", "diagnostic_quantity", "0", row=3
        ),
        model_cell_mutation(
            outputs, "value_ledger", "diagnostic_unit", "USD benefit"
        ),
        model_cell_mutation(
            outputs, "value_ledger", "required_gate_ids", "VG01"
        ),
        model_cell_mutation(outputs, "value_ledger", "value_owner", "Unowned"),
        model_cell_mutation(
            outputs, "value_ledger", "decision_boundary", "Validated"
        ),
        model_cell_mutation(outputs, "value_ledger", "evidence_status", "CLOSED"),
        model_cell_mutation(
            outputs, "value_ledger", "aggregation_rule", "Add to total"
        ),
        model_cell_mutation(outputs, "value_ledger", "funded_value_usd", 1),
        model_cell_mutation(
            outputs, "value_ledger", "model_version", "unsafe-version"
        ),
    ]
    missing_ledger_row = clone_outputs(outputs)
    missing_ledger_row["value_ledger"] = missing_ledger_row["value_ledger"].iloc[:-1]
    ledger_mutations.append(missing_ledger_row)
    duplicate_ledger_row = clone_outputs(outputs)
    duplicate_ledger_row["value_ledger"] = pd.concat(
        [
            duplicate_ledger_row["value_ledger"],
            duplicate_ledger_row["value_ledger"].iloc[[0]],
        ],
        ignore_index=True,
    )
    ledger_mutations.append(duplicate_ledger_row)
    reordered_ledger = clone_outputs(outputs)
    reordered_ledger["value_ledger"] = reordered_ledger["value_ledger"].iloc[::-1]
    ledger_mutations.append(reordered_ledger)

    cost_mutations = [
        model_drop_column(outputs, "cost_requirements", "model_use"),
        model_extra_column(outputs, "cost_requirements"),
        model_cell_mutation(
            outputs, "cost_requirements", "current_evidence_status", "CLOSED"
        ),
        model_cell_mutation(
            outputs, "cost_requirements", "current_cost_status", "$1,000,000"
        ),
        model_cell_mutation(
            outputs, "cost_requirements", "model_use", "Use for ROI"
        ),
        model_cell_mutation(
            outputs, "cost_requirements", "envelope_role", "Budget approved"
        ),
        model_cell_mutation(
            outputs, "cost_requirements", "proposed_accountable_owner", "Unowned"
        ),
        model_cell_mutation(
            outputs, "cost_requirements", "model_version", "unsafe-version"
        ),
    ]
    missing_cost = clone_outputs(outputs)
    missing_cost["cost_requirements"] = missing_cost["cost_requirements"].iloc[:-1]
    cost_mutations.append(missing_cost)
    duplicate_cost = clone_outputs(outputs)
    duplicate_cost["cost_requirements"] = pd.concat(
        [duplicate_cost["cost_requirements"], duplicate_cost["cost_requirements"].iloc[[0]]],
        ignore_index=True,
    )
    cost_mutations.append(duplicate_cost)

    assumption_mutations = [
        model_drop_column(outputs, "assumptions", "decision_gate"),
        model_extra_column(outputs, "assumptions"),
        model_cell_mutation(outputs, "assumptions", "decision_gate", ""),
        model_cell_mutation(
            outputs, "assumptions", "current_recognized_value_usd", 1
        ),
        model_cell_mutation(
            outputs, "assumptions", "downside_value", "1000000", row=16
        ),
        model_cell_mutation(
            outputs,
            "assumptions",
            "source_or_rationale",
            "Funding constraint",
            row=16,
        ),
        model_cell_mutation(outputs, "assumptions", "proposed_owner", "Unowned"),
        model_cell_mutation(outputs, "assumptions", "status", "Closed"),
    ]
    missing_assumption = clone_outputs(outputs)
    missing_assumption["assumptions"] = missing_assumption["assumptions"].iloc[:-1]
    assumption_mutations.append(missing_assumption)
    duplicate_assumption = clone_outputs(outputs)
    duplicate_assumption["assumptions"] = pd.concat(
        [duplicate_assumption["assumptions"], duplicate_assumption["assumptions"].iloc[[0]]],
        ignore_index=True,
    )
    assumption_mutations.append(duplicate_assumption)
    extra_assumption_id = clone_outputs(outputs)
    extra_row = extra_assumption_id["assumptions"].iloc[[0]].copy()
    extra_row["assumption_id"] = "SA08"
    extra_assumption_id["assumptions"] = pd.concat(
        [extra_assumption_id["assumptions"], extra_row], ignore_index=True
    )
    assumption_mutations.append(extra_assumption_id)

    control_mutations = [controls_frame.drop(columns=["evidence_gate_status"])]
    extra_control_column = controls_frame.copy()
    extra_control_column["unsafe_extra_column"] = "unsafe"
    control_mutations.append(extra_control_column)
    for column, value in [
        ("control_status", "PASS"),
        ("evidence_gate_status", "CLOSED"),
        ("model_version", "unsafe-version"),
    ]:
        changed = controls_frame.copy()
        changed.loc[changed.index[0], column] = value
        control_mutations.append(changed)
    changed_bc11 = controls_frame.copy()
    changed_bc11.loc[
        changed_bc11["control_id"].eq("BC11"), "control_rule"
    ] = "Federated is robust"
    control_mutations.append(changed_bc11)
    contradictory_controls = [
        ("BC06", "control_rule", "Risk value is zero"),
        ("BC07", "failure_action", "Approve funding"),
        ("BC08", "control_rule", "$1.5m approved cost"),
        ("BC09", "control_rule", "ROI is available"),
        ("BC12", "proposed_owner", "Unowned"),
    ]
    contradictory_control_mutations = []
    for control_id, column, value in contradictory_controls:
        changed = controls_frame.copy()
        changed.loc[changed["control_id"].eq(control_id), column] = value
        contradictory_control_mutations.append(changed)
    control_mutations.append(controls_frame.iloc[:-1].copy())
    control_mutations.append(
        pd.concat([controls_frame, controls_frame.iloc[[0]]], ignore_index=True)
    )

    model_again = build_business_case_model()
    deterministic = all(
        (
            assert_frame_equal(
                outputs[key].reset_index(drop=True),
                model_again[key].reset_index(drop=True),
                check_dtype=True,
            )
            is None
        )
        for key in outputs
    )
    output_paths = {
        "scenarios": PROCESSED / "W3_business_case_scenarios.csv",
        "value_ledger": PROCESSED / "W3_business_case_value_ledger.csv",
        "cost_requirements": PROCESSED / "W3_cost_evidence_requirements.csv",
        "controls": PROCESSED / "W3_business_case_controls.csv",
        "assumptions": WEEK3 / "W3_assumptions_register.csv",
    }
    write_outputs(outputs)
    round_trip_matches = True
    expected_frames = {**outputs, "controls": build_controls(outputs)}
    for key, path in output_paths.items():
        stored = pd.read_csv(path, keep_default_na=False)
        try:
            assert_frame_equal(stored, expected_frames[key], check_dtype=False)
        except AssertionError:
            round_trip_matches = False

    forbidden_columns = {
        "roi",
        "npv",
        "payback",
        "total_benefit_usd",
        "net_benefit_usd",
        "benefit_cost_ratio",
    }
    all_output_columns = set().union(
        *(set(frame.columns) for frame in expected_frames.values())
    )
    ledger_lookup = ledger.set_index(["scenario_id", "value_category"])
    category_first = ledger.drop_duplicates("value_category").set_index(
        "value_category"
    )
    required_assumption_ids = list(VALUE_GATES) + [
        f"SA{number:02d}" for number in range(1, 8)
    ]

    checks = {
        "Week 2 liquidity screens reconcile exactly": (
            evidence["stress_liquidity_screen_usd"] == 21_000_000
            and evidence["base_liquidity_screen_usd"] == 35_000_000
            and evidence["upside_liquidity_screen_usd"] == 46_200_000
        ),
        "Week 2 candidates and portfolio fee estimate reconcile": (
            evidence["closure_validation_candidates"] == 4
            and evidence["candidate_fee_sensitivity_usd_annual"] == 7_800
        ),
        "evidenced any-two candidate fee range is $1,800-$6,000": (
            evidence["two_candidate_fee_range_low_usd_annual"] == 1_800
            and evidence["two_candidate_fee_range_high_usd_annual"] == 6_000
            and TWO_ACCOUNT_FEE_RANGE_LOW_USD_ANNUAL == 1_800
            and TWO_ACCOUNT_FEE_RANGE_HIGH_USD_ANNUAL == 6_000
        ),
        "Week 2 management-estimated capacity reconciles": (
            evidence["estimated_manual_process_hours_monthly"] == 617.72
        ),
        "independent Week 2 repair baselines remain separate": (
            evidence["payment_file_repair_hours_monthly"] == 55.7778
            and evidence["process_file_repair_hours_monthly"] == 102.6
        ),
        "Week 2 payment extract boundary reconciles": (
            evidence["payment_records"] == 7_600
            and evidence["gross_supplied_payment_value"] == 198_135_489.50
        ),
        "three governed scenario definitions are exact": (
            list(SCENARIO_INPUTS) == ["downside", "base", "upside"]
            and list(scenarios.index) == ["downside", "base", "upside"]
        ),
        "downside base and upside hypotheses reproduce exactly": all(
            all(
                scenarios.loc[scenario_id, column] == value
                for column, value in values.items()
            )
            for scenario_id, values in expected_scenarios.items()
        ),
        "14-day screen labels preserve 168/168 138/168 and 0/168": (
            "168/168" in scenarios.loc["downside", "liquidity_evidence_status"]
            and "138/168" in scenarios.loc["base", "liquidity_evidence_status"]
            and "$46.2m passes 0/168"
            in scenarios.loc["upside", "liquidity_evidence_status"]
            and scenarios["liquidity_evidence_status"]
            .str.startswith("DIAGNOSTIC 14-DAY SCREEN")
            .all()
        ),
        "$3,900 is independent 50% portfolio sensitivity not selected two fees": (
            "Independent 50% × $7,800 portfolio sensitivity"
            in scenarios.loc["downside", "candidate_fee_sensitivity_basis"]
            and "not the fee sum"
            in scenarios.loc["downside", "candidate_fee_sensitivity_basis"]
            and scenarios["evidenced_two_account_fee_range_low_usd_annual"]
            .eq(1_800)
            .all()
            and scenarios["evidenced_two_account_fee_range_high_usd_annual"]
            .eq(6_000)
            .all()
        ),
        "upper scenario does not invent ten closures": (
            scenarios.loc["upside", "closure_validation_candidates"] == 4
        ),
        "capacity annualization is exact": scenarios[
            "capacity_hypothesis_hours_annual"
        ].eq(scenarios["capacity_hypothesis_hours_monthly"] * 12).all(),
        "scenario availability and risk statuses are exact": (
            scenarios["actual_cost_status"].eq("NOT AVAILABLE").all()
            and scenarios["benefit_ramp_status"].eq("NOT AVAILABLE").all()
            and scenarios["roi_npv_payback_status"].eq("NOT AVAILABLE").all()
            and scenarios["risk_value_status"]
            .eq("RISK EXPOSURE AND VALUE NOT QUANTIFIED")
            .all()
        ),
        "recommendation is conditional on ownership readiness and affordability": (
            scenarios["recommendation_test"].eq(RECOMMENDATION_TEST).all()
            and all(
                term in RECOMMENDATION_TEST
                for term in [
                    "global data/control ownership",
                    "minimum integration readiness",
                    "affordability",
                    "local stabilization",
                ]
            )
        ),
        "all scenario value fields remain zero": scenarios[
            ["validated_value_usd", "funded_value_usd", "recognized_value_usd"]
        ].eq(0).all().all(),
        "value ledger is the exact ordered 3x4 cartesian set": (
            list(
                ledger[["scenario_id", "value_category"]].itertuples(
                    index=False, name=None
                )
            )
            == [
                (scenario_id, category)
                for scenario_id in ["downside", "base", "upside"]
                for category in ["cash_release", "annual_p_and_l", "capacity", "risk"]
            ]
        ),
        "cash P&L capacity and risk categories remain separate": (
            list(VALUE_CATEGORIES)
            == ["cash_release", "annual_p_and_l", "capacity", "risk"]
            and ledger.groupby("scenario_id")["value_category"].nunique().eq(4).all()
        ),
        "all category quantities and units are exact": (
            ledger_lookup["diagnostic_quantity"].to_dict() == expected_quantities
            and category_first["diagnostic_unit"].to_dict() == expected_units
        ),
        "all category gates owners and boundaries are governed": (
            category_first["required_gate_ids"].to_dict() == expected_gate_refs
            and category_first["value_owner"].to_dict() == expected_owners
            and all(
                category_first.loc[category, "decision_boundary"]
                == VALUE_CATEGORY_DETAILS[category]["boundary"]
                for category in VALUE_CATEGORIES
            )
        ),
        "risk exposure and value are not quantified": (
            ledger.loc[ledger["value_category"].eq("risk"), "diagnostic_quantity"]
            .eq("NOT QUANTIFIED")
            .all()
            and ledger.loc[ledger["value_category"].eq("risk"), "decision_boundary"]
            .str.contains("$0 is only", regex=False)
            .all()
        ),
        "ledger value remains unvalidated unfunded and unrecognized": ledger[
            ["validated_value_usd", "funded_value_usd", "recognized_value_usd"]
        ].eq(0).all().all(),
        "ledger is explicitly non-additive": ledger["aggregation_rule"].eq(
            "NON-ADDITIVE — do not sum across categories or scenarios"
        ).all(),
        "cost requirement set is exact complete and open": (
            list(costs["cost_requirement_id"]) == list(COST_REQUIREMENTS)
            and costs["current_evidence_status"]
            .eq("OPEN — actual cost not supplied")
            .all()
        ),
        "costs block return calculation and funding decision": (
            costs["current_cost_status"].eq(COST_STATUS).all()
            and costs["model_use"].eq(COST_MODEL_USE).all()
            and "do not calculate returns or decide funding until populated"
            in COST_MODEL_USE
        ),
        "funding constraint is an exact ceiling not cost or authority": (
            INITIAL_ENVELOPE_LOW_USD == 1_000_000
            and INITIAL_ENVELOPE_HIGH_USD == 1_500_000
            and scenarios["initial_envelope_low_usd"].eq(1_000_000).all()
            and scenarios["initial_envelope_high_usd"].eq(1_500_000).all()
            and scenarios["initial_envelope_role"].eq(ENVELOPE_ROLE).all()
            and costs["envelope_role"].eq(ENVELOPE_ROLE).all()
        ),
        "assumption IDs are exactly VG01-VG12 plus SA01-SA07": (
            list(assumptions_frame["assumption_id"]) == required_assumption_ids
            and not assumptions_frame["assumption_id"].duplicated().any()
        ),
        "SA05 is one non-scenario $1.0-$1.5m constraint": (
            assumptions.loc[
                "SA05", ["downside_value", "base_value", "upside_value"]
            ].eq("N/A").all()
            and "$1.0–$1.5m" in assumptions.loc["SA05", "source_or_rationale"]
            and "not a scenario value"
            in assumptions.loc["SA05", "source_or_rationale"]
        ),
        "all assumptions have required decision gates": assumptions[
            "decision_gate"
        ].replace("", pd.NA).notna().all(),
        "assumption ledger recognizes no current value": assumptions[
            "current_recognized_value_usd"
        ].eq(0).all(),
        "twelve model-control records pass while evidence stays open or blocked": (
            list(controls_frame["control_id"]) == list(CONTROL_IDS)
            and controls["control_status"].eq("MODEL CONTROL PASS").all()
            and controls["evidence_gate_status"].isin({"OPEN", "BLOCKED"}).all()
        ),
        "control evidence-gate statuses match the governed map": (
            controls["evidence_gate_status"].to_dict()
            == CONTROL_EVIDENCE_GATE_STATUS
        ),
        "BC11 carries the conditional downside switching boundary": all(
            term in controls.loc["BC11", "control_rule"]
            for term in [
                "$21m",
                "independent 50% × $7,800",
                "50 hours/month",
                "global data/control ownership",
                "minimum integration readiness",
                "affordability",
                "local stabilization",
            ]
        ),
        "all governed schemas and model versions are exact": (
            tuple(outputs) == MODEL_OUTPUT_KEYS
            and tuple(scenarios_frame.columns) == SCENARIO_COLUMNS
            and tuple(ledger.columns) == VALUE_LEDGER_COLUMNS
            and tuple(costs.columns) == COST_REQUIREMENT_COLUMNS
            and tuple(assumptions_frame.columns) == ASSUMPTION_COLUMNS
            and tuple(controls_frame.columns) == CONTROL_COLUMNS
            and all(
                frame["model_version"].eq(MODEL_VERSION).all()
                for frame in [scenarios_frame, ledger, costs, controls_frame]
            )
            and not (forbidden_columns & all_output_columns)
        ),
        "unsafe output-key and scenario mutations fail closed": (
            all_model_mutations_fail(output_key_mutations)
            and all_model_mutations_fail(scenario_mutations)
        ),
        "unsafe ledger mutations fail closed": all_model_mutations_fail(
            ledger_mutations
        ),
        "unsafe cost assumption and control structure mutations fail closed": (
            all_model_mutations_fail(cost_mutations)
            and all_model_mutations_fail(assumption_mutations)
            and all_control_mutations_fail(control_mutations)
        ),
        "BC06 BC07 BC08 BC09 and BC12 contradictions fail closed": (
            all_control_mutations_fail(contradictory_control_mutations)
        ),
        "model generation and stored outputs are deterministic": (
            deterministic and round_trip_matches
        ),
    }

    if len(checks) != 38:
        raise AssertionError(f"Expected 38 automated checks, found {len(checks)}")
    failed = [name for name, passed in checks.items() if not passed]
    for name, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'}: {name}")
    if failed:
        raise AssertionError(f"Week 3 business-case test failures: {failed}")
    print("All 38 Week 3 business-case automated checks passed.")
    print("12 model-control records remain separately labelled MODEL CONTROL PASS.")


if __name__ == "__main__":
    main()
