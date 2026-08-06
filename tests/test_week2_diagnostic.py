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
    build_reconciliation_metrics,
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
    }
    failed = [name for name, passed in checks.items() if not passed]
    for name, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'} — {name}")
    if failed:
        raise SystemExit(f"Week 2 diagnostic test failures: {failed}")
    print(f"All {len(checks)} Week 2 diagnostic tests passed.")


if __name__ == "__main__":
    main()
