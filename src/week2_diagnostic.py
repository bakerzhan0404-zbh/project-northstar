"""Reproducible Week 2 current-state diagnostic for Project Northstar.

Raw files remain unchanged. This module enriches the supplied datasets,
reconciles every analytical population, and writes decision-support outputs to
``data/processed``. The calculations deliberately preserve the evidence
boundaries defined in ``W2_metric_contract.md``: estimated availability is not
validated movable cash, the payment extract is not an ACG-wide population, and
process hours are capacity estimates rather than cashable savings.
"""

from pathlib import Path
from typing import Dict

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
    reconciliation.to_csv(PROCESSED / "W2_reconciliation_metrics.csv", index=False)
    account_diagnostic.to_csv(PROCESSED / "W2_account_diagnostic.csv", index=False)
    visibility_diagnostic.to_csv(
        PROCESSED / "W2_visibility_diagnostic.csv", index=False
    )
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


if __name__ == "__main__":
    main()
