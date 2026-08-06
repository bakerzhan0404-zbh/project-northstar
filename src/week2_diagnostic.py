"""Reproducible Week 2 current-state diagnostic for Project Northstar.

Raw files remain unchanged. This module enriches the supplied datasets,
reconciles every analytical population, and writes decision-support outputs to
``data/processed``. The calculations deliberately preserve the evidence
boundaries defined in ``W2_metric_contract.md``: estimated availability is not
validated movable cash, the payment extract is not an ACG-wide population, and
process hours are capacity estimates rather than cashable savings.
"""

from pathlib import Path
from typing import Dict, Tuple

import pandas as pd

from starter_analysis import enrich_balances, load_data, validate_keys


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def enrich_payments(data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Join payment records to account, entity, and daily project FX data."""
    payments = data["payments"].merge(
        data["accounts"][
            [
                "account_id",
                "entity_id",
                "bank_name",
                "country",
                "purpose",
                "visibility_method",
                "currency",
            ]
        ].rename(columns={"currency": "account_currency"}),
        on="account_id",
        how="left",
        validate="many_to_one",
    )
    payments = payments.merge(
        data["entities"][
            ["entity_id", "entity_name", "region", "erp_system"]
        ],
        on="entity_id",
        how="left",
        validate="many_to_one",
    )
    payments = payments.merge(
        data["fx"].rename(columns={"date": "payment_date"}),
        on=["payment_date", "currency"],
        how="left",
        validate="many_to_one",
    )
    if payments["usd_per_unit"].isna().any():
        raise ValueError("Missing FX rate after payment enrichment")
    if not payments["currency"].eq(payments["account_currency"]).all():
        raise ValueError("Payment currency differs from account currency")
    payments["amount_usd"] = payments["amount_local"] * payments["usd_per_unit"]
    payments["month"] = payments["payment_date"].dt.to_period("M").astype(str)
    return payments


def calculate_process_capacity(process: pd.DataFrame) -> pd.DataFrame:
    """Calculate management-estimated manual capacity without implying savings."""
    result = process.copy()
    result["manual_hours_monthly"] = (
        result["frequency_per_month"]
        * result["minutes_per_instance"]
        * result["manual_percentage"]
        / 100
        / 60
    )
    result["loaded_capacity_usd_monthly"] = (
        result["manual_hours_monthly"] * result["loaded_hourly_cost_usd"]
    )
    result["loaded_capacity_usd_annual"] = (
        result["loaded_capacity_usd_monthly"] * 12
    )
    return result


def build_account_diagnostic(
    data: Dict[str, pd.DataFrame],
    balances: pd.DataFrame,
    payments: pd.DataFrame,
) -> pd.DataFrame:
    """Screen all accounts for local closure validation and protection needs.

    The primary screen is intentionally narrow: dormant status, legacy purpose,
    and zero supplied payment records. Every result remains a validation
    candidate because local legal purpose, service dependencies, and closure
    economics are not supplied.
    """
    accounts = data["accounts"].merge(
        data["entities"][
            [
                "entity_id",
                "entity_name",
                "region",
                "erp_system",
                "acquisition_origin",
                "cash_restriction_level",
            ]
        ],
        on="entity_id",
        how="left",
        validate="many_to_one",
    )
    payment_profile = payments.groupby("account_id", as_index=False).agg(
        supplied_payment_records=("payment_id", "size"),
        supplied_payment_value_usd=("amount_usd", "sum"),
        last_supplied_payment_date=("payment_date", "max"),
    )
    balance_profile = balances.groupby("account_id", as_index=False).agg(
        average_positive_available_usd=(
            "available_balance_usd",
            lambda series: series.clip(lower=0).mean(),
        ),
        average_absolute_available_usd=(
            "available_balance_usd",
            lambda series: series.abs().mean(),
        ),
    )
    latest_date = balances["date"].max()
    latest_profile = balances.loc[
        balances["date"].eq(latest_date),
        ["account_id", "available_balance_usd"],
    ].rename(columns={"available_balance_usd": "latest_available_usd"})

    result = (
        accounts.merge(
            payment_profile, on="account_id", how="left", validate="one_to_one"
        )
        .merge(balance_profile, on="account_id", how="left", validate="one_to_one")
        .merge(latest_profile, on="account_id", how="left", validate="one_to_one")
    )
    result["supplied_payment_records"] = result[
        "supplied_payment_records"
    ].fillna(0).astype(int)
    result["supplied_payment_value_usd"] = result[
        "supplied_payment_value_usd"
    ].fillna(0.0)
    result["account_age_years"] = (
        (latest_date - result["open_date"]).dt.days / 365.25
    ).round(1)
    result["closure_validation_candidate"] = (
        result["status"].eq("Dormant")
        & result["purpose"].eq("Legacy")
        & result["supplied_payment_records"].eq(0)
    )

    def protection_reason(row: pd.Series) -> str:
        reasons = []
        if row["purpose"] in {"Payroll", "Tax", "Collection"}:
            reasons.append(f"{row['purpose'].lower()} purpose")
        if bool(row["restricted_flag"]):
            reasons.append("preliminary restriction flag")
        if row["sweep_structure"] != "None":
            reasons.append(f"{row['sweep_structure'].lower()} dependency")
        if row["status"] == "Active" and row["purpose"] == "Operating":
            reasons.append("active operating purpose")
        return "; ".join(reasons) if reasons else "local validation required"

    result["protection_or_validation_reason"] = result.apply(
        protection_reason, axis=1
    )
    result["candidate_reason"] = result["closure_validation_candidate"].map(
        {
            True: "Dormant + legacy purpose + zero supplied payment records",
            False: "Does not meet the narrow primary screen",
        }
    )
    result["evidence_label"] = "ANALYST-CALC"
    result["decision_boundary"] = (
        "Local purpose, dependencies, signatories, service continuity, closure "
        "cost, and fee removal are not validated"
    )
    output_columns = [
        "account_id",
        "entity_id",
        "entity_name",
        "region",
        "country",
        "bank_name",
        "currency",
        "purpose",
        "status",
        "account_age_years",
        "visibility_method",
        "sweep_structure",
        "erp_system",
        "acquisition_origin",
        "cash_restriction_level",
        "restricted_flag",
        "annual_fee_usd",
        "supplied_payment_records",
        "supplied_payment_value_usd",
        "last_supplied_payment_date",
        "average_positive_available_usd",
        "average_absolute_available_usd",
        "latest_available_usd",
        "closure_validation_candidate",
        "candidate_reason",
        "protection_or_validation_reason",
        "evidence_label",
        "decision_boundary",
    ]
    return result[output_columns].sort_values(
        ["closure_validation_candidate", "annual_fee_usd", "account_id"],
        ascending=[False, False, True],
    )


def build_visibility_diagnostic(balances: pd.DataFrame) -> pd.DataFrame:
    """Profile date-level reporting timeliness across decision-relevant cuts."""
    working = balances.copy()
    working["positive_available_usd"] = working["available_balance_usd"].clip(
        lower=0
    )
    working["same_calendar_day"] = working["reporting_delay_days"].eq(0)
    working["within_one_calendar_day"] = working["reporting_delay_days"].le(1)
    working["month"] = working["date"].dt.to_period("M").astype(str)

    def summarize(frame: pd.DataFrame, dimension: str, category: str) -> dict:
        delayed_daily = (
            frame.loc[frame["reporting_delay_days"].gt(0)]
            .groupby("date")["positive_available_usd"]
            .sum()
        )
        two_plus_daily = (
            frame.loc[frame["reporting_delay_days"].ge(2)]
            .groupby("date")["positive_available_usd"]
            .sum()
        )
        total_positive = frame["positive_available_usd"].sum()
        same_day_positive = frame.loc[
            frame["same_calendar_day"], "positive_available_usd"
        ].sum()
        return {
            "dimension": dimension,
            "category": str(category),
            "observations": len(frame),
            "accounts": frame["account_id"].nunique(),
            "same_day_observations": int(frame["same_calendar_day"].sum()),
            "same_day_rate_pct": round(100 * frame["same_calendar_day"].mean(), 2),
            "within_one_day_observations": int(
                frame["within_one_calendar_day"].sum()
            ),
            "within_one_day_rate_pct": round(
                100 * frame["within_one_calendar_day"].mean(), 2
            ),
            "one_day_delayed_observations": int(
                frame["reporting_delay_days"].eq(1).sum()
            ),
            "two_plus_day_delayed_observations": int(
                frame["reporting_delay_days"].ge(2).sum()
            ),
            "maximum_delay_days": int(frame["reporting_delay_days"].max()),
            "positive_available_usd": round(total_positive, 2),
            "same_day_positive_available_usd": round(same_day_positive, 2),
            "positive_value_weighted_same_day_rate_pct": round(
                100 * same_day_positive / total_positive, 2
            )
            if total_positive
            else 0.0,
            "median_daily_delayed_positive_available_usd": round(
                delayed_daily.median(), 2
            )
            if not delayed_daily.empty
            else 0.0,
            "median_daily_two_plus_day_positive_available_usd": round(
                two_plus_daily.median(), 2
            )
            if not two_plus_daily.empty
            else 0.0,
            "evidence_label": "ANALYST-CALC",
            "decision_boundary": (
                "Calendar-date proxy; not start-of-day or elapsed-24-hour visibility"
            ),
        }

    rows = [summarize(working, "overall", "All supplied account-days")]
    for dimension in ["region", "visibility_method", "source_quality", "month"]:
        for category, frame in working.groupby(dimension, sort=True):
            rows.append(summarize(frame, dimension, category))
    return pd.DataFrame(rows)


def build_liquidity_scenarios(
    balances: pd.DataFrame, payments: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Build daily liquidity layers and 7/14-day operating-buffer sensitivities.

    The buffers use supplied payment records in the trailing calendar window
    ending on the latest balance date. They are screening sensitivities, not a
    certified cash forecast or minimum operating-cash policy.
    """
    working = balances.copy()
    working["positive_closing_usd"] = working["closing_balance_usd"].clip(lower=0)
    working["negative_closing_usd"] = working["closing_balance_usd"].clip(upper=0)
    working["positive_available_usd"] = working["available_balance_usd"].clip(
        lower=0
    )
    working["negative_available_usd"] = working["available_balance_usd"].clip(
        upper=0
    )
    working["restricted_positive_available_usd"] = working[
        "positive_available_usd"
    ].where(working["restricted_flag"], 0)
    working["unflagged_positive_available_usd"] = working[
        "positive_available_usd"
    ].where(~working["restricted_flag"], 0)
    working["delayed_positive_available_usd"] = working[
        "positive_available_usd"
    ].where(working["reporting_delay_days"].gt(0), 0)

    daily = working.groupby("date", as_index=False).agg(
        net_closing_usd=("closing_balance_usd", "sum"),
        gross_positive_closing_usd=("positive_closing_usd", "sum"),
        gross_negative_closing_usd=("negative_closing_usd", "sum"),
        net_estimated_available_usd=("available_balance_usd", "sum"),
        gross_positive_estimated_available_usd=("positive_available_usd", "sum"),
        gross_negative_estimated_available_usd=("negative_available_usd", "sum"),
        preliminarily_restricted_positive_available_usd=(
            "restricted_positive_available_usd",
            "sum",
        ),
        preliminarily_unflagged_positive_available_usd=(
            "unflagged_positive_available_usd",
            "sum",
        ),
        delayed_positive_available_usd=("delayed_positive_available_usd", "sum"),
    )
    daily["evidence_label"] = "ANALYST-CALC"
    daily["decision_boundary"] = (
        "Estimated availability and preliminary flags do not establish transferability"
    )

    latest_date = working["date"].max()
    account_scenarios = working.loc[working["date"].eq(latest_date)].copy()
    for window_days in [7, 14]:
        window_start = latest_date - pd.Timedelta(days=window_days - 1)
        buffer_by_account = (
            payments.loc[
                payments["payment_date"].between(window_start, latest_date)
            ]
            .groupby("account_id")["amount_usd"]
            .sum()
        )
        buffer_column = f"supplied_payment_buffer_{window_days}d_usd"
        surplus_column = f"scenario_surplus_after_{window_days}d_buffer_usd"
        account_scenarios[buffer_column] = (
            account_scenarios["account_id"].map(buffer_by_account).fillna(0.0)
        )
        account_scenarios[surplus_column] = (
            account_scenarios["positive_available_usd"]
            - account_scenarios[buffer_column]
        ).clip(lower=0)
        account_scenarios[surplus_column] = account_scenarios[surplus_column].where(
            ~account_scenarios["restricted_flag"], 0.0
        )
    account_scenarios["scenario_date"] = latest_date
    account_scenarios["evidence_label"] = "ANALYST-CALC / ANALYST-ASSUMPTION"
    account_scenarios["decision_boundary"] = (
        "Buffers use an uncertified supplied-payment extract; surplus is not movable cash"
    )
    account_columns = [
        "scenario_date",
        "account_id",
        "entity_id",
        "entity_name",
        "region",
        "country",
        "currency",
        "purpose",
        "restricted_flag",
        "reporting_delay_days",
        "closing_balance_usd",
        "available_balance_usd",
        "positive_available_usd",
        "supplied_payment_buffer_7d_usd",
        "scenario_surplus_after_7d_buffer_usd",
        "supplied_payment_buffer_14d_usd",
        "scenario_surplus_after_14d_buffer_usd",
        "evidence_label",
        "decision_boundary",
    ]
    account_scenarios = account_scenarios[account_columns].sort_values("account_id")

    latest_daily = daily.loc[daily["date"].eq(latest_date)].iloc[0]
    unflagged = account_scenarios.loc[~account_scenarios["restricted_flag"]]
    summary_rows = [
        (
            "observed_net_ledger_balance",
            latest_daily["net_closing_usd"],
            "Observed layer",
            "Ledger position; not a transferability measure",
            "ANALYST-CALC",
        ),
        (
            "net_estimated_available_balance",
            latest_daily["net_estimated_available_usd"],
            "Estimated layer",
            "Includes negative positions; not validated movable cash",
            "ANALYST-CALC",
        ),
        (
            "gross_positive_estimated_available_balance",
            latest_daily["gross_positive_estimated_available_usd"],
            "Estimated layer",
            "Before negative positions, restrictions, and buffers",
            "ANALYST-CALC",
        ),
        (
            "preliminarily_restricted_positive_available_balance",
            latest_daily["preliminarily_restricted_positive_available_usd"],
            "Restriction screen",
            "Preliminary flag only; requires account-level certification",
            "ANALYST-CALC",
        ),
        (
            "preliminarily_unflagged_positive_available_balance",
            latest_daily["preliminarily_unflagged_positive_available_usd"],
            "Restriction screen",
            "Unflagged does not mean movable",
            "ANALYST-CALC",
        ),
        (
            "unflagged_supplied_payment_buffer_7d",
            unflagged["supplied_payment_buffer_7d_usd"].sum(),
            "Illustrative buffer",
            "Trailing seven calendar days in uncertified supplied-payment extract",
            "ANALYST-ASSUMPTION",
        ),
        (
            "unflagged_scenario_surplus_after_7d_buffer",
            account_scenarios[
                "scenario_surplus_after_7d_buffer_usd"
            ].sum(),
            "Scenario surplus",
            "Not validated movable cash",
            "ANALYST-CALC / ANALYST-ASSUMPTION",
        ),
        (
            "unflagged_supplied_payment_buffer_14d",
            unflagged["supplied_payment_buffer_14d_usd"].sum(),
            "Illustrative buffer",
            "Trailing 14 calendar days in uncertified supplied-payment extract",
            "ANALYST-ASSUMPTION",
        ),
        (
            "unflagged_scenario_surplus_after_14d_buffer",
            account_scenarios[
                "scenario_surplus_after_14d_buffer_usd"
            ].sum(),
            "Scenario surplus",
            "Not validated movable cash",
            "ANALYST-CALC / ANALYST-ASSUMPTION",
        ),
        (
            "validated_movable_cash",
            float("nan"),
            "Validated value",
            "Not established by supplied data",
            "NOT ESTABLISHED",
        ),
    ]
    summary = pd.DataFrame(
        summary_rows,
        columns=[
            "metric",
            "value_usd",
            "liquidity_layer",
            "interpretation",
            "evidence_label",
        ],
    )
    summary.insert(0, "scenario_date", latest_date)
    summary["value_usd"] = summary["value_usd"].round(2)
    return daily, account_scenarios, summary


def build_reconciliation_metrics(
    data: Dict[str, pd.DataFrame],
    balances: pd.DataFrame,
    payments: pd.DataFrame,
    process_capacity: pd.DataFrame,
) -> pd.DataFrame:
    """Return the control totals that every Week 2 module must preserve."""
    metrics = [
        ("entities", len(data["entities"]), "rows", "ACG-DATA"),
        (
            "supplied_revenue",
            data["entities"]["revenue_usd_m"].sum(),
            "USD millions",
            "ACG-DATA",
        ),
        ("accounts", len(data["accounts"]), "accounts", "ACG-DATA"),
        (
            "estimated_annual_account_fees",
            data["accounts"]["annual_fee_usd"].sum(),
            "USD/year",
            "ACG-DATA",
        ),
        ("balance_observations", len(balances), "account-days", "ACG-DATA"),
        ("balance_dates", balances["date"].nunique(), "calendar days", "ACG-DATA"),
        ("payment_records", len(payments), "records", "ACG-DATA"),
        (
            "gross_supplied_payment_value",
            payments["amount_usd"].sum(),
            "USD",
            "ANALYST-CALC",
        ),
        (
            "payment_repair_minutes",
            payments["repair_minutes"].sum(),
            "minutes",
            "ACG-DATA",
        ),
        ("fx_rows", len(data["fx"]), "rows", "ACG-DATA"),
        ("fx_currencies", data["fx"]["currency"].nunique(), "currencies", "ACG-DATA"),
        ("process_activities", len(data["process"]), "activities", "ACG-DATA"),
        (
            "estimated_manual_process_hours_monthly",
            process_capacity["manual_hours_monthly"].sum(),
            "hours/month",
            "ANALYST-CALC",
        ),
    ]
    result = pd.DataFrame(
        metrics, columns=["metric", "value", "unit", "evidence_label"]
    )
    result["value"] = result["value"].map(
        lambda value: round(float(value), 2) if isinstance(value, (float, int)) else value
    )
    return result


def validate_reconciliations(
    data: Dict[str, pd.DataFrame],
    balances: pd.DataFrame,
    payments: pd.DataFrame,
    process_capacity: pd.DataFrame,
) -> None:
    """Fail fast when the supplied Week 2 population changes unexpectedly."""
    checks = {
        "16 entities": len(data["entities"]) == 16,
        "55 accounts": len(data["accounts"]) == 55,
        "55 x 181 balance panel": len(balances) == 55 * 181,
        "7,600 supplied payments": len(payments) == 7_600,
        "$198.14m translated payment control": abs(
            payments["amount_usd"].sum() - 198_135_489.50
        )
        < 0.01,
        "20,080 repair minutes": payments["repair_minutes"].sum() == 20_080,
        "617.72 manual process hours": abs(
            process_capacity["manual_hours_monthly"].sum() - 617.7163333333333
        )
        < 0.001,
        "payment joins complete": payments[
            ["entity_id", "region", "bank_name", "usd_per_unit"]
        ]
        .notna()
        .all()
        .all(),
        "balance joins complete": balances[
            ["entity_id", "region", "usd_per_unit"]
        ]
        .notna()
        .all()
        .all(),
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError(f"Week 2 reconciliation failures: {failed}")


def main() -> None:
    """Build all implemented Week 2 diagnostic outputs."""
    PROCESSED.mkdir(parents=True, exist_ok=True)
    data = load_data()
    validate_keys(data)
    balances = enrich_balances(data)
    payments = enrich_payments(data)
    process_capacity = calculate_process_capacity(data["process"])
    validate_reconciliations(data, balances, payments, process_capacity)

    reconciliation = build_reconciliation_metrics(
        data, balances, payments, process_capacity
    )
    account_diagnostic = build_account_diagnostic(data, balances, payments)
    visibility_diagnostic = build_visibility_diagnostic(balances)
    liquidity_daily, liquidity_accounts, liquidity_summary = build_liquidity_scenarios(
        balances, payments
    )
    reconciliation.to_csv(PROCESSED / "W2_reconciliation_metrics.csv", index=False)
    account_diagnostic.to_csv(PROCESSED / "W2_account_diagnostic.csv", index=False)
    visibility_diagnostic.to_csv(
        PROCESSED / "W2_visibility_diagnostic.csv", index=False
    )
    liquidity_daily.to_csv(PROCESSED / "W2_liquidity_daily.csv", index=False)
    liquidity_accounts.to_csv(
        PROCESSED / "W2_liquidity_account_scenarios.csv", index=False
    )
    liquidity_summary.to_csv(PROCESSED / "W2_liquidity_scenarios.csv", index=False)
    print(reconciliation.to_string(index=False))
    candidates = account_diagnostic.loc[
        account_diagnostic["closure_validation_candidate"]
    ]
    print(
        "\nAccount screen: "
        f"{len(candidates)} closure-validation candidates; "
        f"${candidates['annual_fee_usd'].sum():,.0f} gross estimated annual fees"
    )
    print("Wrote data/processed/W2_reconciliation_metrics.csv")
    print("Wrote data/processed/W2_account_diagnostic.csv")
    print("Wrote data/processed/W2_visibility_diagnostic.csv")
    print("Wrote data/processed/W2_liquidity_daily.csv")
    print("Wrote data/processed/W2_liquidity_account_scenarios.csv")
    print("Wrote data/processed/W2_liquidity_scenarios.csv")


if __name__ == "__main__":
    main()
