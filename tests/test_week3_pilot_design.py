"""Executable controls for the Week 3 deterministic pilot-selection model."""

import sys
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from week3_pilot_design import (  # noqa: E402
    AMOUNT_BAND_LABELS,
    EVIDENCE_BOUNDARY,
    ISSUE_MODE_TARGETS,
    PAYMENT_COHORTS,
    PAYMENT_RULE_VERSION,
    PROCESSED,
    VISIBILITY_RULE_VERSION,
    VISIBILITY_SELECTION,
    add_payment_sampling_fields,
    build_pilot_model,
    load_governed_inputs,
    validate_pilot_contract,
    validate_week2_anchors,
    write_outputs,
)


def assertion_raises(callable_object) -> bool:
    try:
        callable_object()
    except AssertionError:
        return True
    return False


def main() -> None:
    data, balances, payments = load_governed_inputs()
    anchors = validate_week2_anchors(data, balances, payments)
    outputs = build_pilot_model()
    visibility = outputs["visibility_candidates"]
    sample = outputs["payment_sample"]
    controls = outputs["controls"].set_index("control_record_id")

    expected_visibility = [
        "AC0021",
        "AC0010",
        "AC0017",
        "AC0001",
        "AC0040",
        "AC0022",
        "AC0031",
        "AC0018",
        "AC0002",
        "AC0050",
    ]
    expected_pool_counts = {
        "Manual touch only": (2_053, 246, 166, 1_641, 1_638),
        "Manual touch + cross-border wire": (342, 58, 29, 255, 254),
        "Cross-border wire only": (444, 52, 27, 365, 365),
        "Neither priority cohort": (4_761, 123, 103, 4_535, 4_524),
    }
    expected_mismatch_pairs = {
        "C1-01": "payment_type",
        "C1-05": "payment_type",
        "C1-11": "payment_type",
        "C1-12": "region",
        "C2-09": "month",
        "C2-11": "region",
        "C2-12": "region",
        "C2-13": "region",
        "C3-07": "month",
        "C3-11": "region",
    }

    enriched = add_payment_sampling_fields(payments)
    actual_pool_counts = {}
    for cohort in PAYMENT_COHORTS:
        frame = enriched.loc[enriched["priority_payment_cohort"].eq(cohort)]
        actual_pool_counts[cohort] = (
            len(frame),
            int(frame["exception_status_case_flag"].sum()),
            int(frame["late_only_case_flag"].sum()),
            int((~frame["issue_case_flag"]).sum()),
            int(
                (
                    ~frame["issue_case_flag"]
                    & frame["status"].eq("Completed")
                ).sum()
            ),
        )

    visibility_by_method = visibility.groupby(
        "visibility_method", sort=False
    )["account_id"].apply(list).to_dict()
    ac0040 = visibility.set_index("account_id").loc["AC0040"]
    non_ac0040 = visibility.loc[~visibility["account_id"].eq("AC0040")]
    method_ranks = visibility.set_index("account_id")[
        "method_average_positive_rank"
    ].astype(int).to_dict()
    expected_method_ranks = {
        "AC0021": 1,
        "AC0010": 2,
        "AC0017": 3,
        "AC0001": 4,
        "AC0040": 6,
        "AC0022": 1,
        "AC0031": 2,
        "AC0018": 3,
        "AC0002": 4,
        "AC0050": 7,
    }

    issue_rows = sample.loc[sample["sample_role"].eq("Issue case")]
    control_rows = sample.loc[sample["sample_role"].eq("Non-issue control")]
    cohort_counts = sample.groupby("priority_payment_cohort", sort=False).size()
    role_counts = sample.groupby(
        ["priority_payment_cohort", "sample_role"], sort=False
    ).size()
    issue_mode_counts = issue_rows.groupby(
        ["priority_payment_cohort", "issue_mode"], sort=False
    ).size()
    mismatch_rows = issue_rows.loc[issue_rows["match_deviation_count"].gt(0)]
    mismatch_pairs = mismatch_rows.set_index("case_control_pair_id")[
        "match_deviation_detail"
    ].to_dict()

    payment_source = enriched.set_index("payment_id")
    source_lineage_matches = True
    for _, row in sample.iterrows():
        source = payment_source.loc[row["source_payment_id"]]
        source_lineage_matches = source_lineage_matches and (
            row["account_id"] == source["account_id"]
            and row["entity_id"] == source["entity_id"]
            and row["payment_type"] == source["payment_type"]
            and row["region"] == source["region"]
            and abs(row["amount_usd"] - round(float(source["amount_usd"]), 2)) < 0.01
            and row["status"] == source["status"]
            and (
                row["sample_role"] != "Issue case"
                or row["issue_mode"] == source["source_issue_mode"]
            )
        )

    pair_lineage_matches = True
    for _, pair in sample.groupby("case_control_pair_id", sort=False):
        issue = pair.loc[pair["sample_role"].eq("Issue case")].iloc[0]
        control = pair.loc[pair["sample_role"].eq("Non-issue control")].iloc[0]
        pair_lineage_matches = pair_lineage_matches and (
            issue["paired_source_payment_id"] == control["source_payment_id"]
            and control["paired_source_payment_id"] == issue["source_payment_id"]
            and issue["issue_mode"] == issue["paired_issue_mode"]
            and control["issue_mode"] == "Non-issue control"
            and control["paired_issue_mode"] == issue["issue_mode"]
            and int(control["issue_selection_rank"]) == 0
            and int(control["issue_mode_selection_rank"]) == 0
        )

    model_again = build_pilot_model()
    deterministic = all(
        assert_frame_equal(
            outputs[key].reset_index(drop=True),
            model_again[key].reset_index(drop=True),
            check_dtype=True,
        )
        is None
        for key in outputs
    )

    # Mutation tests exercise the fail-closed contract independently of the
    # happy-path controls written to the output manifest.
    missing_visibility = visibility.iloc[:-1].copy()
    unsafe_ac0040 = visibility.copy()
    unsafe_ac0040.loc[
        unsafe_ac0040["account_id"].eq("AC0040"), "shadow_only_flag"
    ] = False
    missing_standard_review = visibility.copy()
    missing_standard_review.loc[
        missing_standard_review["account_id"].eq("AC0021"),
        "control_review_required",
    ] = False
    missing_enhanced_review = visibility.copy()
    missing_enhanced_review.loc[
        missing_enhanced_review["account_id"].eq("AC0040"),
        "enhanced_control_review_required",
    ] = False
    unsafe_ac0040_attributes = visibility.copy()
    unsafe_ac0040_attributes.loc[
        unsafe_ac0040_attributes["account_id"].eq("AC0040"), "restricted_flag"
    ] = False
    blank_visibility = visibility.copy()
    blank_visibility.loc[blank_visibility.index[0], "selection_rule"] = "   "
    duplicate_sample = sample.copy()
    duplicate_sample.loc[duplicate_sample.index[-1], "source_payment_id"] = (
        duplicate_sample.iloc[0]["source_payment_id"]
    )
    false_issue = sample.copy()
    first_issue_index = false_issue.loc[
        false_issue["sample_role"].eq("Issue case")
    ].index[0]
    false_issue.loc[first_issue_index, "issue_case_flag"] = False
    changed_issue_mode = sample.copy()
    changed_issue_mode.loc[first_issue_index, "issue_mode"] = "Late-only"
    pending_control = sample.copy()
    first_control_index = pending_control.loc[
        pending_control["sample_role"].eq("Non-issue control")
    ].index[0]
    pending_control.loc[first_control_index, "status"] = "Pending"
    broken_pair = sample.copy()
    broken_pair.loc[broken_pair.index[0], "paired_source_payment_id"] = "P999999"
    blank_sample = sample.copy()
    blank_sample.loc[blank_sample.index[0], "match_quality"] = ""
    changed_payments = payments.iloc[:-1].copy()

    output_paths = {
        "visibility_candidates": PROCESSED / "W3_visibility_pilot_candidates.csv",
        "payment_sample": PROCESSED / "W3_payment_sample_frame.csv",
        "controls": PROCESSED / "W3_pilot_model_controls.csv",
    }
    stored_matches_before_write = True
    for key, path in output_paths.items():
        stored = pd.read_csv(path, keep_default_na=False)
        try:
            assert_frame_equal(
                stored,
                outputs[key],
                check_dtype=False,
                check_like=False,
            )
        except AssertionError:
            stored_matches_before_write = False
    write_outputs(outputs)
    round_trip_matches = True
    for key, path in output_paths.items():
        stored = pd.read_csv(path, keep_default_na=False)
        try:
            assert_frame_equal(
                stored,
                outputs[key],
                check_dtype=False,
                check_like=False,
            )
        except AssertionError:
            round_trip_matches = False

    w2_account_diagnostic = pd.read_csv(
        PROCESSED / "W2_account_diagnostic.csv", keep_default_na=False
    ).set_index("account_id")
    visibility_averages_reconcile = all(
        abs(
            float(row["average_positive_available_usd"])
            - round(
                float(
                    w2_account_diagnostic.loc[
                        row["account_id"], "average_positive_available_usd"
                    ]
                ),
                2,
            )
        )
        < 0.01
        for _, row in visibility.iterrows()
    )

    checks = {
        "Week 2 account and balance anchors reconcile": anchors["accounts"] == 55
        and anchors["account_days"] == 9_955
        and anchors["same_day_account_days"] == 5_792
        and anchors["delayed_accounts"] == 23,
        "Week 2 payment anchors reconcile": anchors["payment_records"] == 7_600
        and anchors["gross_payment_intent_usd"] == 198_135_489.50
        and anchors["repair_minutes"] == 20_080,
        "Week 2 priority-union anchors reconcile": anchors[
            "priority_union_records"
        ]
        == 2_839
        and anchors["priority_union_exceptions"] == 356
        and anchors["priority_union_repair_minutes"] == 14_939
        and anchors["priority_union_amount_usd"] == 66_705_933.64,
        "visibility cohort is the exact locked ten-account sequence": visibility[
            "account_id"
        ].tolist()
        == expected_visibility,
        "visibility split is exactly five Spreadsheet and five Portal": visibility_by_method
        == {method: list(ids) for method, ids in VISIBILITY_SELECTION.items()},
        "visibility cohort covers 3 regions, 3 ERPs, and 4 banks": visibility[
            "region"
        ].nunique()
        == 3
        and visibility["erp_system"].nunique() == 3
        and visibility["bank_name"].nunique() == 4,
        "visibility method rankings preserve four leaders plus top APAC": method_ranks
        == expected_method_ranks,
        "visibility averages reconcile to Week 2 account diagnostic": visibility_averages_reconcile,
        "all visibility accounts require review and AC0040 alone is enhanced/shadow-only": visibility[
            "control_review_required"
        ].all()
        and bool(
            ac0040["shadow_only_flag"]
        )
        and bool(ac0040["enhanced_control_review_required"])
        and ac0040["region"] == "APAC"
        and ac0040["purpose"] == "Payroll"
        and bool(ac0040["restricted_flag"])
        and "shadow" in ac0040["cohort_treatment"].lower()
        and not non_ac0040["shadow_only_flag"].any()
        and not non_ac0040["enhanced_control_review_required"].any(),
        "visibility outputs remain explicitly not launch-ready": visibility[
            "readiness_status"
        ].str.startswith("NOT LAUNCH-READY").all(),
        "four source payment cohorts reconcile before sampling": actual_pool_counts
        == expected_pool_counts,
        "payment sample contains exactly 120 unique source IDs": len(sample) == 120
        and sample["source_payment_id"].nunique() == 120,
        "each mutually exclusive cohort contributes exactly 30 rows": cohort_counts.to_dict()
        == {cohort: 30 for cohort in PAYMENT_COHORTS},
        "each cohort contributes exactly 15 issues and 15 controls": all(
            role_counts.loc[(cohort, "Issue case")] == 15
            and role_counts.loc[(cohort, "Non-issue control")] == 15
            for cohort in PAYMENT_COHORTS
        ),
        "each cohort contains exactly 8 exception/status and 7 late-only issues": all(
            issue_mode_counts.loc[(cohort, issue_mode)] == target
            for cohort in PAYMENT_COHORTS
            for issue_mode, target in ISSUE_MODE_TARGETS.items()
        ),
        "issue definition is exception OR late release OR repaired/rejected": issue_rows[
            "issue_case_flag"
        ].all()
        and not control_rows["issue_case_flag"].any()
        and issue_rows["issue_definition_hits"].ne("none").all()
        and control_rows["issue_definition_hits"].eq("none").all(),
        "issue modes obey exception/status and late-only definitions": (
            issue_rows.loc[
                issue_rows["issue_mode"].eq("Exception/status"),
                "exception_flag",
            ]
            | issue_rows.loc[
                issue_rows["issue_mode"].eq("Exception/status"), "status"
            ].isin(["Repaired", "Rejected"])
        ).all()
        and issue_rows.loc[
            issue_rows["issue_mode"].eq("Late-only"), "late_release_flag"
        ].all()
        and not (
            issue_rows.loc[
                issue_rows["issue_mode"].eq("Late-only"), "exception_flag"
            ]
            | issue_rows.loc[
                issue_rows["issue_mode"].eq("Late-only"), "status"
            ].isin(["Repaired", "Rejected"])
        ).any(),
        "each issue mode retains deterministic subgroup and overall ranks": all(
            issue_rows.loc[
                issue_rows["priority_payment_cohort"].eq(cohort)
                & issue_rows["issue_mode"].eq(issue_mode),
                "issue_mode_selection_rank",
            ].tolist()
            == list(range(1, target + 1))
            for cohort in PAYMENT_COHORTS
            for issue_mode, target in ISSUE_MODE_TARGETS.items()
        )
        and all(
            issue_rows.loc[
                issue_rows["priority_payment_cohort"].eq(cohort),
                "issue_selection_rank",
            ].tolist()
            == list(range(1, 16))
            for cohort in PAYMENT_COHORTS
        )
        and control_rows["issue_selection_rank"].eq(0).all()
        and control_rows["issue_mode_selection_rank"].eq(0).all(),
        "controls are explicitly non-issue and retain paired issue mode": control_rows[
            "issue_mode"
        ].eq("Non-issue control").all()
        and control_rows["paired_issue_mode"].isin(ISSUE_MODE_TARGETS).all()
        and control_rows["status"].eq("Completed").all(),
        "all 60 case-control pairs retain reciprocal source IDs": sample[
            "case_control_pair_id"
        ].nunique()
        == 60
        and sample.groupby("case_control_pair_id").size().eq(2).all()
        and pair_lineage_matches,
        "all matching fields and deviations are populated": sample[
            [
                "payment_type_match",
                "region_match",
                "month_match",
                "amount_band_match",
                "match_deviation_count",
                "match_deviation_detail",
                "match_quality",
            ]
        ]
        .notna()
        .all()
        .all(),
        "50 pairs are exact and ten nearest-match deviations are explicit": issue_rows[
            "match_deviation_count"
        ].eq(0).sum()
        == 50
        and mismatch_pairs == expected_mismatch_pairs,
        "amount bands reuse the governed Week 2 five-band contract": tuple(
            enriched["amount_band_usd"].cat.categories
        )
        == AMOUNT_BAND_LABELS,
        "sample fields reconcile to source records": source_lineage_matches,
        "rule versions are fixed on every selected row": visibility[
            "selection_rule_version"
        ].eq(VISIBILITY_RULE_VERSION).all()
        and sample["selection_rule_version"].eq(PAYMENT_RULE_VERSION).all(),
        "every selected row states the purposive non-prevalence boundary": sample[
            "sample_purpose"
        ].str.contains("not a prevalence", case=False, regex=False).all()
        and sample["decision_boundary"].eq(EVIDENCE_BOUNDARY).all()
        and visibility["decision_boundary"].eq(EVIDENCE_BOUNDARY).all(),
        "control manifest contains fourteen passing controls": len(controls) == 14
        and controls["test_result"].eq("PASS").all()
        and controls["evidence_boundary"].eq(EVIDENCE_BOUNDARY).all(),
        "model build is deterministic": deterministic,
        "stored artifacts matched the regenerated model before rewrite": stored_matches_before_write,
        "stored CSVs exactly match regenerated outputs": round_trip_matches,
        "only the three governed output paths are used": set(output_paths)
        == set(outputs)
        and all(path.exists() for path in output_paths.values()),
        "missing visibility account fails closed": assertion_raises(
            lambda: validate_pilot_contract(
                missing_visibility, sample, payments
            )
        ),
        "unsafe AC0040 treatment fails closed": assertion_raises(
            lambda: validate_pilot_contract(unsafe_ac0040, sample, payments)
        ),
        "missing standard visibility review fails closed": assertion_raises(
            lambda: validate_pilot_contract(
                missing_standard_review, sample, payments
            )
        ),
        "missing AC0040 enhanced review fails closed": assertion_raises(
            lambda: validate_pilot_contract(
                missing_enhanced_review, sample, payments
            )
        ),
        "changed AC0040 restricted semantics fail closed": assertion_raises(
            lambda: validate_pilot_contract(
                unsafe_ac0040_attributes, sample, payments
            )
        ),
        "blank visibility selection field fails closed": assertion_raises(
            lambda: validate_pilot_contract(blank_visibility, sample, payments)
        ),
        "duplicate sampled source payment fails closed": assertion_raises(
            lambda: validate_pilot_contract(visibility, duplicate_sample, payments)
        ),
        "false issue classification fails closed": assertion_raises(
            lambda: validate_pilot_contract(visibility, false_issue, payments)
        ),
        "changed issue mode allocation fails closed": assertion_raises(
            lambda: validate_pilot_contract(
                visibility, changed_issue_mode, payments
            )
        ),
        "Pending comparator status fails closed": assertion_raises(
            lambda: validate_pilot_contract(
                visibility, pending_control, payments
            )
        ),
        "broken pair lineage fails closed": assertion_raises(
            lambda: validate_pilot_contract(visibility, broken_pair, payments)
        ),
        "blank payment selection field fails closed": assertion_raises(
            lambda: validate_pilot_contract(visibility, blank_sample, payments)
        ),
        "changed payment population fails the Week 2 anchor": assertion_raises(
            lambda: validate_week2_anchors(data, balances, changed_payments)
        ),
    }

    failed = [name for name, passed in checks.items() if not passed]
    for name, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'} — {name}")
    if failed:
        raise SystemExit(f"Week 3 pilot-model test failures: {failed}")
    print(f"All {len(checks)} Week 3 pilot-model tests passed.")


if __name__ == "__main__":
    main()
