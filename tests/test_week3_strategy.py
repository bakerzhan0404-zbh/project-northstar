"""Executable controls for the Week 3 gate-then-score option model."""

import copy
import sys
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from week3_strategy import (  # noqa: E402
    BASE_WEIGHTS,
    CRITERIA,
    EVIDENCE_BOUNDARY,
    EXTREME_SWITCH_WEIGHTS,
    HARD_GATES,
    OPTION_IDS,
    OPTION_SCORES,
    PROCESSED,
    SENSITIVITY_WEIGHTS,
    WEIGHT_LOCK_VERSION,
    build_gate_assessments,
    build_score_inputs,
    build_sensitivity_results,
    build_strategy_model,
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


def main() -> None:
    evidence = validate_week2_evidence()
    score_inputs = build_score_inputs()
    gates = build_gate_assessments()
    outputs = build_strategy_model()
    weighted = outputs["weighted_scores"]
    summary = outputs["summary"].set_index("option_id")
    sensitivity = outputs["sensitivity"]
    controls = outputs["controls"].set_index("control_record_id")

    expected_weights = {
        "evidence_fit": 20,
        "control_resilience": 20,
        "feasibility_speed": 20,
        "local_adaptability": 15,
        "data_technology_scalability": 10,
        "value_economics": 10,
        "reversibility_learning": 5,
    }
    expected_scores = {
        "local_stabilization": [3, 3, 5, 5, 2, 2, 5],
        "federated_coordination": [5, 4, 4, 5, 4, 4, 4],
        "globally_coordinated": [3, 3, 2, 2, 5, 5, 2],
    }
    expected_base = {
        "local_stabilization": 72.0,
        "federated_coordination": 87.0,
        "globally_coordinated": 60.0,
    }
    expected_ranks = {
        "local_stabilization": 2,
        "federated_coordination": 1,
        "globally_coordinated": 3,
    }
    expected_sensitivity = {
        ("balanced_base", "local_stabilization"): 72.0,
        ("balanced_base", "federated_coordination"): 87.0,
        ("balanced_base", "globally_coordinated"): 60.0,
        ("controls_first", "local_stabilization"): 70.0,
        ("controls_first", "federated_coordination"): 85.0,
        ("controls_first", "globally_coordinated"): 61.0,
        ("speed_first", "local_stabilization"): 77.0,
        ("speed_first", "federated_coordination"): 85.0,
        ("speed_first", "globally_coordinated"): 56.0,
        ("scale_value_first", "local_stabilization"): 61.0,
        ("scale_value_first", "federated_coordination"): 85.0,
        ("scale_value_first", "globally_coordinated"): 73.0,
        ("local_autonomy_first", "local_stabilization"): 77.0,
        ("local_autonomy_first", "federated_coordination"): 89.0,
        ("local_autonomy_first", "globally_coordinated"): 56.0,
    }

    actual_scores = {
        option_id: [
            OPTION_SCORES[option_id][criterion_id]
            for criterion_id in BASE_WEIGHTS
        ]
        for option_id in OPTION_IDS
    }
    actual_base = summary["base_weighted_score_0_to_100"].to_dict()
    actual_ranks = summary["base_rank"].astype(int).to_dict()
    sensitivity_lookup = sensitivity.set_index(["scenario_id", "option_id"])[
        "total_weighted_score_0_to_100"
    ].to_dict()
    extreme_results = build_sensitivity_results(
        score_inputs, gates, EXTREME_SWITCH_WEIGHTS
    )
    extreme_winners = extreme_results.loc[
        extreme_results["scenario_winner"]
    ].set_index("scenario_id")["option_id"].to_dict()
    weighted_formula = (
        weighted["score_1_to_5"] * weighted["locked_weight_pct"] / 5
    ).round(4)

    invalid_score_inputs = score_inputs.copy()
    invalid_score_inputs.loc[invalid_score_inputs.index[0], "score_1_to_5"] = 6
    invalid_sensitivity = copy.deepcopy(SENSITIVITY_WEIGHTS)
    invalid_sensitivity["controls_first"]["weights"]["evidence_fit"] += 1

    failed_gate_outputs = build_strategy_model(
        {("federated_coordination", "G03"): False}
    )
    failed_gate_summary = failed_gate_outputs["summary"].set_index("option_id")
    failed_gate_weighted = failed_gate_outputs["weighted_scores"]
    failed_federated_rows = failed_gate_weighted.loc[
        failed_gate_weighted["option_id"].eq("federated_coordination")
    ]
    failed_gate_control = failed_gate_outputs["controls"].loc[
        failed_gate_outputs["controls"]["control_record_id"].eq(
            "G03-federated_coordination"
        )
    ].iloc[0]

    model_again = build_strategy_model()
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
        "weighted_scores": PROCESSED / "W3_option_weighted_scores.csv",
        "summary": PROCESSED / "W3_option_summary.csv",
        "sensitivity": PROCESSED / "W3_option_sensitivity.csv",
        "controls": PROCESSED / "W3_model_controls.csv",
    }
    write_outputs(outputs)
    round_trip_matches = True
    for key, path in output_paths.items():
        stored = pd.read_csv(path, keep_default_na=False)
        regenerated = outputs[key].copy()
        # No current governed option fails a design gate, so the generated
        # production outputs contain no intentional null cells.
        try:
            assert_frame_equal(
                stored,
                regenerated,
                check_dtype=False,
                check_like=False,
            )
        except AssertionError:
            round_trip_matches = False

    forbidden_business_case_columns = {
        "benefit_usd",
        "cost_usd",
        "roi",
        "npv",
        "payback",
        "cash_release_usd",
        "capacity_savings_usd",
    }
    all_output_columns = set().union(*(set(frame.columns) for frame in outputs.values()))

    checks = {
        "Week 2 evidence controls cover F07–F11": set(evidence)
        == {"F07", "F08", "F09", "F10", "F11"},
        "criteria match the seven committed decision dimensions": list(
            CRITERIA
        )
        == list(expected_weights),
        "base weights are locked exactly at 20/20/20/15/10/10/5": BASE_WEIGHTS
        == expected_weights,
        "base weights sum to 100": sum(BASE_WEIGHTS.values()) == 100,
        "weight lock is dated and present on every score row": (
            WEIGHT_LOCK_VERSION == "W3-DP-v1 · 2026-08-18"
            and weighted["weight_lock_version"].eq(WEIGHT_LOCK_VERSION).all()
        ),
        "three options use exactly the directed 1–5 scores": actual_scores
        == expected_scores,
        "score matrix is complete at 3 options x 7 criteria": len(weighted) == 21
        and not weighted.duplicated(["option_id", "criterion_id"]).any(),
        "every score has explicit rationale, evidence, and confidence": (
            weighted[
                ["score_rationale", "evidence_anchor", "evidence_confidence"]
            ]
            .replace("", pd.NA)
            .notna()
            .all()
            .all()
        ),
        "weighted points use weight x score / 5": weighted[
            "weighted_points_0_to_100"
        ].equals(weighted_formula),
        "base results are exactly 72 / 87 / 60": actual_base == expected_base,
        "base ranking is federated then local then global": actual_ranks
        == expected_ranks,
        "federated is the sole provisional base preference": (
            summary["provisional_preferred_option"].sum() == 1
            and bool(
                summary.loc[
                    "federated_coordination", "provisional_preferred_option"
                ]
            )
        ),
        "all current options pass design gates only": (
            len(gates) == len(OPTION_IDS) * len(HARD_GATES)
            and gates["design_compliant"].all()
            and gates["execution_evidence_status"].str.contains("Open").all()
        ),
        "all options remain explicitly non-execution-ready": summary[
            "execution_gate_status"
        ].str.startswith("OPEN").all()
        and summary["execution_readiness"].str.startswith("NOT AUTHORIZED").all(),
        "affordability gate uses the CFO $1.0–$1.5m constraint": (
            "$1.0–$1.5m"
            in HARD_GATES["G06"]["gate_rule"]
            and summary["initial_funding_constraint"]
            .str.contains(r"\$1\.0–\$1\.5m", regex=True)
            .all()
        ),
        "all five plausible sensitivity cases retain the same seven criteria": (
            len(SENSITIVITY_WEIGHTS) == 5
            and all(
                set(case["weights"]) == set(BASE_WEIGHTS)
                and sum(case["weights"].values()) == 100
                for case in SENSITIVITY_WEIGHTS.values()
            )
        ),
        "sensitivity scores reproduce the governed cases": sensitivity_lookup
        == expected_sensitivity,
        "federated leads all five plausible sensitivity cases": (
            sensitivity.loc[sensitivity["scenario_winner"], "option_id"]
            .eq("federated_coordination")
            .all()
            and summary.loc["federated_coordination", "sensitivity_wins"] == 5
        ),
        "extreme priorities exercise both documented switch directions": (
            extreme_winners
            == {
                "extreme_speed_reversibility": "local_stabilization",
                "extreme_scale_future_value": "globally_coordinated",
            }
        ),
        "a failed gate removes an option before scoring": (
            pd.isna(
                failed_gate_summary.loc[
                    "federated_coordination", "base_weighted_score_0_to_100"
                ]
            )
            and failed_federated_rows["weighted_points_0_to_100"].isna().all()
            and str(failed_gate_control["test_result"]).startswith("FAIL")
            and not bool(
                failed_gate_summary.loc[
                    "federated_coordination", "provisional_preferred_option"
                ]
            )
        ),
        "out-of-range scores fail closed": assertion_raises(
            lambda: validate_model_contract(invalid_score_inputs, gates)
        ),
        "sensitivity weights that do not sum to 100 fail closed": assertion_raises(
            lambda: validate_model_contract(
                score_inputs, gates, invalid_sensitivity
            )
        ),
        "model controls record gate-then-score": controls.loc[
            "MC03", "test_result"
        ]
        == "PASS"
        and "cannot compensate" in controls.loc["MC03", "control_rule"],
        "model outputs contain no business-case result columns": not (
            all_output_columns & forbidden_business_case_columns
        ),
        "every output retains the no-business-case boundary": all(
            frame["evidence_boundary"].eq(EVIDENCE_BOUNDARY).all()
            for frame in outputs.values()
        ),
        "model build is deterministic": deterministic,
        "stored CSVs exactly match regenerated outputs": round_trip_matches,
        "only the four governed output paths are used": set(output_paths)
        == {
            "weighted_scores",
            "summary",
            "sensitivity",
            "controls",
        }
        and all(path.exists() for path in output_paths.values()),
    }

    failed = [name for name, passed in checks.items() if not passed]
    for name, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'} — {name}")
    if failed:
        raise SystemExit(f"Week 3 strategy test failures: {failed}")
    print(f"All {len(checks)} Week 3 strategy tests passed.")


if __name__ == "__main__":
    main()
