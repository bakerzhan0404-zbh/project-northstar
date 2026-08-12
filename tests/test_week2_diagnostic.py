"""Executable reconciliation tests for the Week 2 diagnostic layer."""

import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from starter_analysis import enrich_balances, load_data, validate_keys  # noqa: E402
from week2_diagnostic import (  # noqa: E402
    build_account_diagnostic,
    build_visibility_diagnostic,
    build_liquidity_scenarios,
    build_simultaneous_position_diagnostic,
    build_payment_diagnostic,
    build_reconciliation_metrics,
    build_repair_baseline_reconciliation,
    calculate_process_capacity,
    enrich_payments,
    validate_reconciliations,
)


def main() -> None:
    data = load_data()
    validate_keys(data)
    balances = enrich_balances(data)
    payments = enrich_payments(data)
    process_capacity = calculate_process_capacity(data["process"])
    repair_reconciliation = build_repair_baseline_reconciliation(
        payments, process_capacity
    ).set_index("metric")
    validate_reconciliations(data, balances, payments, process_capacity)
    metrics = build_reconciliation_metrics(
        data, balances, payments, process_capacity
    ).set_index("metric")
    accounts = build_account_diagnostic(data, balances, payments)
    candidates = accounts.loc[accounts["closure_validation_candidate"]]
    visibility = build_visibility_diagnostic(balances)
    visibility_overall = visibility.loc[
        visibility["dimension"].eq("overall")
    ].iloc[0]
    visibility_source = visibility.loc[
        visibility["dimension"].eq("visibility_method")
    ].set_index("category")
    liquidity_daily, liquidity_accounts, liquidity_summary, liquidity_thresholds = (
        build_liquidity_scenarios(balances, payments)
    )
    liquidity_metrics = liquidity_summary.set_index("metric")["value_usd"]
    simultaneous_daily, entity_positions, account_positions = (
        build_simultaneous_position_diagnostic(balances)
    )
    persistent_deficits = account_positions.loc[
        account_positions["persistent_deficit_flag"]
    ].set_index("account_id")
    payment_diagnostic = build_payment_diagnostic(payments)
    payment_overall = payment_diagnostic.loc[
        payment_diagnostic["dimension"].eq("overall")
    ].iloc[0]
    payment_manual = payment_diagnostic.loc[
        payment_diagnostic["dimension"].eq("manual_touch")
    ].set_index("category")
    payment_wires = payment_diagnostic.loc[
        payment_diagnostic["dimension"].eq("wire_geography")
    ].set_index("category")
    payment_priority = payment_diagnostic.loc[
        payment_diagnostic["dimension"].eq("priority_payment_cohort")
    ].set_index("category")
    payment_priority_union = payment_diagnostic.loc[
        payment_diagnostic["dimension"].eq("priority_union")
    ].set_index("category")

    checks = {
        "revenue control remains $3.9bn": metrics.loc[
            "supplied_revenue", "value"
        ]
        == 3_900,
        "account fees reconcile": metrics.loc[
            "estimated_annual_account_fees", "value"
        ]
        == 110_100,
        "payment value reconciles": metrics.loc[
            "gross_supplied_payment_value", "value"
        ]
        == 198_135_489.50,
        "process capacity reconciles": metrics.loc[
            "estimated_manual_process_hours_monthly", "value"
        ]
        == 617.72,
        "account diagnostic reconciles to 55": len(accounts) == 55,
        "four narrow closure-validation candidates": len(candidates) == 4,
        "candidate fees reconcile to $7,800": candidates["annual_fee_usd"].sum()
        == 7_800,
        "all primary candidates have zero supplied payments": candidates[
            "supplied_payment_records"
        ].eq(0).all(),
        "all primary candidates remain locally gated": candidates[
            "decision_boundary"
        ].str.contains("not validated").all(),
        "visibility overall reconciles to 9,955": visibility_overall[
            "observations"
        ]
        == 9_955,
        "32 accounts have same-day date proxy": visibility_overall[
            "same_day_observations"
        ]
        == 32 * 181,
        "same-day account-day rate is 58.18%": visibility_overall[
            "same_day_rate_pct"
        ]
        == 58.18,
        "within-one-day sensitivity is 74.55%": visibility_overall[
            "within_one_day_rate_pct"
        ]
        == 74.55,
        "all portal observations are one day delayed": visibility_source.loc[
            "Portal", "one_day_delayed_observations"
        ]
        == 9 * 181,
        "all spreadsheet observations are two-plus days delayed": visibility_source.loc[
            "Spreadsheet", "two_plus_day_delayed_observations"
        ]
        == 14 * 181,
        "liquidity daily output covers 181 dates": len(liquidity_daily) == 181,
        "liquidity account scenario covers 55 accounts": len(liquidity_accounts)
        == 55,
        "latest net estimated availability reconciles": liquidity_metrics[
            "net_estimated_available_balance"
        ]
        == 55_662_922.37,
        "latest gross positive estimate reconciles": liquidity_metrics[
            "gross_positive_estimated_available_balance"
        ]
        == 57_801_215.46,
        "preliminary restriction layer reconciles": liquidity_metrics[
            "preliminarily_restricted_positive_available_balance"
        ]
        == 8_053_700.97,
        "seven-day scenario surplus reconciles": liquidity_metrics[
            "unflagged_scenario_surplus_after_7d_buffer"
        ]
        == 44_983_080.88,
        "14-day scenario surplus reconciles": liquidity_metrics[
            "unflagged_scenario_surplus_after_14d_buffer"
        ]
        == 40_265_783.82,
        "seven-day net scenario reconciles": liquidity_metrics[
            "net_scenario_surplus_after_7d_buffer"
        ]
        == 42_844_787.78,
        "14-day net scenario reconciles": liquidity_metrics[
            "net_scenario_surplus_after_14d_buffer"
        ]
        == 38_127_490.73,
        "seven-day base threshold survives all complete windows": liquidity_thresholds.loc[
            (liquidity_thresholds["buffer_window_days"].eq(7))
            & (liquidity_thresholds["threshold_name"].eq("base")),
            "days_threshold_met",
        ].iloc[0]
        == 175,
        "14-day base threshold survives 138 complete windows": liquidity_thresholds.loc[
            (liquidity_thresholds["buffer_window_days"].eq(14))
            & (liquidity_thresholds["threshold_name"].eq("base")),
            "days_threshold_met",
        ].iloc[0]
        == 138,
        "completed/repaired status sensitivity is immaterial": liquidity_metrics[
            "completed_repaired_status_sensitivity_14d_gross_surplus"
        ]
        == 40_286_213.98,
        "upside threshold survives no net scenario window": liquidity_thresholds.loc[
            liquidity_thresholds["threshold_name"].eq("upside"),
            "days_threshold_met",
        ].eq(0).all(),
        "validated movable cash remains unestablished": pd.isna(
            liquidity_metrics["validated_movable_cash"]
        ),
        "simultaneous daily output covers 181 dates": len(simultaneous_daily)
        == 181,
        "positive and negative accounts coexist every day": simultaneous_daily[
            "simultaneous_account_positions_flag"
        ].all(),
        "exactly two accounts are negative every day": simultaneous_daily[
            "negative_account_count"
        ].eq(2).all(),
        "two accounts have persistent estimated deficits": set(
            persistent_deficits.index
        )
        == {"AC0025", "AC0034"},
        "persistent deficit run covers all 181 days": persistent_deficits[
            "longest_negative_run_days"
        ].eq(181).all(),
        "entity net deficits occur on 45 days": simultaneous_daily[
            "deficit_entity_count"
        ].gt(0).sum()
        == 45,
        "E007 has 37 entity deficit days": entity_positions.loc[
            entity_positions["entity_id"].eq("E007"), "entity_net_deficit_flag"
        ].sum()
        == 37,
        "E010 has 14 entity deficit days": entity_positions.loc[
            entity_positions["entity_id"].eq("E010"), "entity_net_deficit_flag"
        ].sum()
        == 14,
        "entity net reconciles to account net": simultaneous_daily[
            "net_estimated_available_usd"
        ].round(2).eq(
            simultaneous_daily["entity_net_estimated_available_usd"].round(2)
        ).all(),
        "payment diagnostic reconciles to 7,600": payment_overall["records"]
        == 7_600,
        "payment exceptions reconcile to 479": payment_overall[
            "exception_records"
        ]
        == 479,
        "payment late releases reconcile to 380": payment_overall[
            "late_release_records"
        ]
        == 380,
        "payment fees reconcile to $62,613": payment_overall[
            "estimated_fees_usd"
        ]
        == 62_613,
        "manual records contribute 63.47% of exceptions": payment_manual.loc[
            "Manual touch", "exception_contribution_pct"
        ]
        == 63.47,
        "manual records have 12.69% exception rate": payment_manual.loc[
            "Manual touch", "exception_rate_pct"
        ]
        == 12.69,
        "cross-border wires reconcile to 786": payment_wires.loc[
            "Cross-border wire", "records"
        ]
        == 786,
        "cross-border wire exception rate is 13.99%": payment_wires.loc[
            "Cross-border wire", "exception_rate_pct"
        ]
        == 13.99,
        "cross-border wires contribute 24.51% of repair": payment_wires.loc[
            "Cross-border wire", "repair_contribution_pct"
        ]
        == 24.51,
        "domestic wire exception rate is 4.41%": payment_wires.loc[
            "Domestic wire", "exception_rate_pct"
        ]
        == 4.41,
        "mutually exclusive payment cohorts reconcile to 7,600": payment_priority[
            "records"
        ].sum()
        == 7_600,
        "manual-touch-only cohort reconciles": (
            payment_priority.loc["Manual touch only", "records"] == 2_053
            and payment_priority.loc[
                "Manual touch only", "exception_records"
            ]
            == 246
            and payment_priority.loc["Manual touch only", "repair_minutes"]
            == 10_018
            and payment_priority.loc[
                "Manual touch only", "gross_supplied_record_value_usd"
            ]
            == 51_983_738.28
        ),
        "manual/cross-border overlap reconciles": (
            payment_priority.loc[
                "Manual touch + cross-border wire", "records"
            ]
            == 342
            and payment_priority.loc[
                "Manual touch + cross-border wire", "exception_records"
            ]
            == 58
            and payment_priority.loc[
                "Manual touch + cross-border wire", "repair_minutes"
            ]
            == 2_702
            and payment_priority.loc[
                "Manual touch + cross-border wire",
                "gross_supplied_record_value_usd",
            ]
            == 6_846_691.83
        ),
        "cross-border-wire-only cohort reconciles": (
            payment_priority.loc["Cross-border wire only", "records"] == 444
            and payment_priority.loc[
                "Cross-border wire only", "exception_records"
            ]
            == 52
            and payment_priority.loc[
                "Cross-border wire only", "repair_minutes"
            ]
            == 2_219
            and payment_priority.loc[
                "Cross-border wire only", "gross_supplied_record_value_usd"
            ]
            == 7_875_503.53
        ),
        "neither-priority cohort reconciles": (
            payment_priority.loc["Neither priority cohort", "records"] == 4_761
            and payment_priority.loc[
                "Neither priority cohort", "exception_records"
            ]
            == 123
            and payment_priority.loc[
                "Neither priority cohort", "repair_minutes"
            ]
            == 5_141
            and payment_priority.loc[
                "Neither priority cohort", "gross_supplied_record_value_usd"
            ]
            == 131_429_555.87
        ),
        "deduplicated priority union reconciles": (
            payment_priority_union.loc[
                "Manual touch or cross-border wire", "records"
            ]
            == 2_839
            and payment_priority_union.loc[
                "Manual touch or cross-border wire", "exception_records"
            ]
            == 356
            and payment_priority_union.loc[
                "Manual touch or cross-border wire", "repair_minutes"
            ]
            == 14_939
            and payment_priority_union.loc[
                "Manual touch or cross-border wire",
                "gross_supplied_record_value_usd",
            ]
            == 66_705_933.64
        ),
        "overlap magnitude is explicit": (
            round(
                100
                * payment_priority.loc[
                    "Manual touch + cross-border wire", "records"
                ]
                / payment_manual.loc["Manual touch", "records"],
                2,
            )
            == 14.28
            and round(
                100
                * payment_priority.loc[
                    "Manual touch + cross-border wire", "records"
                ]
                / payment_wires.loc["Cross-border wire", "records"],
                2,
            )
            == 43.51
        ),
        "every payment row carries extract boundary": payment_diagnostic[
            "decision_boundary"
        ].str.contains("7,600").all(),
        "process capacity has nine activities": len(process_capacity) == 9,
        "process capacity sums to 617.72 hours": round(
            process_capacity["manual_hours_monthly"].sum(), 2
        )
        == 617.72,
        "high-criticality work is 315.48 hours": round(
            process_capacity.loc[
                process_capacity["high_control_criticality_flag"],
                "manual_hours_monthly",
            ].sum(),
            2,
        )
        == 315.48
        and process_capacity["high_control_criticality_flag"].equals(
            process_capacity["control_criticality"].eq("High")
        ),
        "loaded capacity equivalent is $426,618.90 annual": round(
            process_capacity["loaded_capacity_usd_annual"].sum(), 2
        )
        == 426_618.90,
        "payment file implies 55.78 repair hours monthly": round(
            repair_reconciliation.loc[
                "payment_file_repair_hours_monthly", "value"
            ],
            2,
        )
        == 55.78,
        "process file implies 102.60 repair hours monthly": round(
            repair_reconciliation.loc[
                "process_file_exception_manual_hours_monthly", "value"
            ],
            2,
        )
        == 102.60,
        "process repair hours are 1.84x payment baseline": round(
            repair_reconciliation.loc[
                "process_to_payment_repair_hour_ratio", "value"
            ],
            2,
        )
        == 1.84
        and repair_reconciliation.loc[
            "unreconciled_exception_count_difference_monthly", "unit"
        ]
        == "mixed records/instances per month",
        "150-hour target is 24.28% of screening baseline": round(
            100
            * repair_reconciliation.loc["week2_capacity_target_share", "value"],
            2,
        )
        == 24.28,
    }
    failed = [name for name, passed in checks.items() if not passed]
    for name, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'} — {name}")
    if failed:
        raise SystemExit(f"Week 2 diagnostic test failures: {failed}")
    print(f"All {len(checks)} Week 2 diagnostic tests passed.")


if __name__ == "__main__":
    main()
