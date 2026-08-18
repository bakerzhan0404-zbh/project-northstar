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

PRIORITY_PAYMENT_CATEGORIES = [
    "Manual touch only",
    "Manual touch + cross-border wire",
    "Cross-border wire only",
    "Neither priority cohort",
]


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


def add_priority_payment_cohorts(payments: pd.DataFrame) -> pd.DataFrame:
    """Add the governed, mutually exclusive payment-priority cohorts."""
    working = payments.copy()
    working["cross_border_wire_flag"] = working["payment_type"].eq(
        "Wire"
    ) & working["cross_border_flag"]
    manual_touch = working["manual_touch_flag"]
    cross_border_wire = working["cross_border_wire_flag"]
    working["priority_payment_cohort"] = "Neither priority cohort"
    working.loc[manual_touch & ~cross_border_wire, "priority_payment_cohort"] = (
        "Manual touch only"
    )
    working.loc[manual_touch & cross_border_wire, "priority_payment_cohort"] = (
        "Manual touch + cross-border wire"
    )
    working.loc[~manual_touch & cross_border_wire, "priority_payment_cohort"] = (
        "Cross-border wire only"
    )
    working["priority_payment_cohort"] = pd.Categorical(
        working["priority_payment_cohort"],
        categories=PRIORITY_PAYMENT_CATEGORIES,
        ordered=True,
    )
    working["priority_union_cohort"] = pd.Categorical(
        (manual_touch | cross_border_wire).map(
            {
                True: "Manual touch or cross-border wire",
                False: "Outside priority union",
            }
        ),
        categories=[
            "Manual touch or cross-border wire",
            "Outside priority union",
        ],
        ordered=True,
    )
    return working


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
    total_hours = result["manual_hours_monthly"].sum()
    total_cost = result["loaded_capacity_usd_monthly"].sum()
    result["manual_hour_share_pct"] = (
        100 * result["manual_hours_monthly"] / total_hours
    ).round(2)
    result["loaded_capacity_share_pct"] = (
        100 * result["loaded_capacity_usd_monthly"] / total_cost
    ).round(2)
    result["high_control_criticality_flag"] = result["control_criticality"].eq(
        "High"
    )
    result["evidence_label"] = "ANALYST-CALC"
    result["decision_boundary"] = (
        "Management-estimated capacity; not observed labor, headcount, or cashable savings"
    )
    return result


def build_repair_baseline_reconciliation(
    payments: pd.DataFrame, process_capacity: pd.DataFrame
) -> pd.DataFrame:
    """Keep payment-file and process-file repair baselines visibly separate."""
    payment_exceptions_monthly = payments["exception_flag"].sum() / 6
    payment_repair_hours_monthly = payments["repair_minutes"].sum() / 60 / 6
    process_exception = process_capacity.loc[
        process_capacity["process"].eq("Payment exception repair")
    ].iloc[0]
    process_instances_monthly = process_exception["frequency_per_month"]
    process_repair_hours_monthly = process_exception["manual_hours_monthly"]
    rows = [
        (
            "payment_file_exception_records_monthly",
            payment_exceptions_monthly,
            "records/month",
            "Six-month supplied payment total divided by six",
        ),
        (
            "payment_file_repair_hours_monthly",
            payment_repair_hours_monthly,
            "hours/month",
            "Six-month supplied repair minutes divided by 60 and six",
        ),
        (
            "process_file_exception_instances_monthly",
            process_instances_monthly,
            "instances/month",
            "Management estimate in process_activity.csv",
        ),
        (
            "process_file_exception_manual_hours_monthly",
            process_repair_hours_monthly,
            "hours/month",
            "Frequency × minutes × manual percentage",
        ),
        (
            "unreconciled_exception_count_difference_monthly",
            process_instances_monthly - payment_exceptions_monthly,
            "mixed records/instances per month",
            "Unreconciled process instances less supplied payment records; directional comparison only",
        ),
        (
            "repair_hour_difference_monthly",
            process_repair_hours_monthly - payment_repair_hours_monthly,
            "hours/month",
            "Process estimate less payment-file average",
        ),
        (
            "process_to_payment_exception_volume_ratio",
            process_instances_monthly / payment_exceptions_monthly,
            "ratio",
            "Unreconciled populations; do not combine",
        ),
        (
            "process_to_payment_repair_hour_ratio",
            process_repair_hours_monthly / payment_repair_hours_monthly,
            "ratio",
            "Unreconciled populations; do not combine",
        ),
        (
            "week2_capacity_target_share",
            150 / process_capacity["manual_hours_monthly"].sum(),
            "share",
            "150 hours/month target is an analyst assumption",
        ),
        (
            "week2_capacity_stress_share",
            50 / process_capacity["manual_hours_monthly"].sum(),
            "share",
            "50 hours/month stress case is an analyst assumption",
        ),
    ]
    result = pd.DataFrame(rows, columns=["metric", "value", "unit", "definition"])
    result["value"] = result["value"].round(4)
    result["evidence_label"] = "ANALYST-CALC / ANALYST-ASSUMPTION"
    result["decision_boundary"] = (
        "Source scope and removability are unresolved; no combined capacity or P&L baseline"
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


def _account_date_payment_outflow(
    balances: pd.DataFrame, payments: pd.DataFrame
) -> pd.Series:
    """Return a complete account-date panel of supplied payment outflow."""
    account_date_index = pd.MultiIndex.from_product(
        [
            sorted(balances["account_id"].unique()),
            sorted(balances["date"].unique()),
        ],
        names=["account_id", "date"],
    )
    return (
        payments.groupby(["account_id", "payment_date"])["amount_usd"]
        .sum()
        .rename_axis(index=["account_id", "date"])
        .reindex(account_date_index, fill_value=0.0)
        .sort_index()
    )


def build_dashboard_account_day_facts(
    balances: pd.DataFrame, payments: pd.DataFrame
) -> pd.DataFrame:
    """Build the minimum governed account-day facts used by dashboard filters.

    Currency, region, entity, and bank filters all resolve to accounts. Date
    filters select account-days for visibility and use the selected end date as
    the liquidity as-of date. The 7/14-day fields remain null until a complete
    trailing calendar window exists, so an incomplete screen cannot be read as
    a zero-dollar result.
    """
    columns = [
        "date",
        "account_id",
        "entity_id",
        "entity_name",
        "region",
        "currency",
        "bank_name",
        "visibility_method",
        "reporting_delay_days",
        "positive_available_usd",
        "restricted_positive_available_usd",
        "negative_available_usd",
    ]
    facts = balances[
        [
            "date",
            "account_id",
            "entity_id",
            "entity_name",
            "region",
            "currency",
            "bank_name",
            "visibility_method",
            "reporting_delay_days",
            "restricted_flag",
            "available_balance_usd",
        ]
    ].copy()
    facts["positive_available_usd"] = facts["available_balance_usd"].clip(
        lower=0
    )
    facts["restricted_positive_available_usd"] = facts[
        "positive_available_usd"
    ].where(facts["restricted_flag"], 0.0)
    facts["negative_available_usd"] = facts["available_balance_usd"].clip(
        upper=0
    )

    payment_outflow = _account_date_payment_outflow(balances, payments)
    first_balance_date = facts["date"].min()
    for window_days in [7, 14]:
        raw_buffer_column = f"_supplied_payment_buffer_{window_days}d_usd"
        complete_column = f"complete_{window_days}d_window"
        unflagged_buffer_column = (
            f"unflagged_payment_buffer_{window_days}d_usd"
        )
        contribution_column = f"net_screen_contribution_{window_days}d_usd"
        rolling_buffer = (
            payment_outflow.groupby(level="account_id")
            .rolling(window_days, min_periods=window_days)
            .sum()
            .reset_index(level=0, drop=True)
            .rename(raw_buffer_column)
            .reset_index()
        )
        facts = facts.merge(
            rolling_buffer,
            on=["account_id", "date"],
            how="left",
            validate="one_to_one",
        )
        facts[complete_column] = facts["date"].ge(
            first_balance_date + pd.Timedelta(days=window_days - 1)
        )
        facts[unflagged_buffer_column] = facts[raw_buffer_column].where(
            ~facts["restricted_flag"], 0.0
        )
        screened_positive = (
            facts["positive_available_usd"] - facts[raw_buffer_column]
        ).clip(lower=0)
        screened_positive = screened_positive.where(
            ~facts["restricted_flag"], 0.0
        )
        facts[contribution_column] = (
            screened_positive + facts["negative_available_usd"]
        )
        incomplete = ~facts[complete_column]
        facts.loc[
            incomplete, [unflagged_buffer_column, contribution_column]
        ] = float("nan")
        facts = facts.drop(columns=[raw_buffer_column])
        columns.extend(
            [complete_column, unflagged_buffer_column, contribution_column]
        )

    money_columns = [
        "positive_available_usd",
        "restricted_positive_available_usd",
        "negative_available_usd",
        "unflagged_payment_buffer_7d_usd",
        "net_screen_contribution_7d_usd",
        "unflagged_payment_buffer_14d_usd",
        "net_screen_contribution_14d_usd",
    ]
    facts[money_columns] = facts[money_columns].round(6)
    return (
        facts[columns]
        .sort_values(["date", "account_id"])
        .reset_index(drop=True)
    )


def build_dashboard_payment_facts(payments: pd.DataFrame) -> pd.DataFrame:
    """Build the minimum governed payment facts used by dashboard filters."""
    working = add_priority_payment_cohorts(payments)
    result = working[
        [
            "payment_id",
            "payment_date",
            "account_id",
            "entity_id",
            "entity_name",
            "region",
            "currency",
            "bank_name",
            "priority_payment_cohort",
            "exception_flag",
            "repair_minutes",
        ]
    ].copy()
    result = result.rename(columns={"payment_date": "date"})
    result["priority_payment_cohort"] = result[
        "priority_payment_cohort"
    ].astype("object")
    return result.sort_values(["date", "payment_id"]).reset_index(drop=True)


def validate_dashboard_filter_facts(
    account_days: pd.DataFrame, payment_facts: pd.DataFrame
) -> None:
    """Fail closed unless filter facts reconcile to the Week 2 controls."""
    failures = []

    expected_account_columns = {
        "date",
        "account_id",
        "entity_id",
        "entity_name",
        "region",
        "currency",
        "bank_name",
        "visibility_method",
        "reporting_delay_days",
        "positive_available_usd",
        "restricted_positive_available_usd",
        "negative_available_usd",
        "complete_7d_window",
        "unflagged_payment_buffer_7d_usd",
        "net_screen_contribution_7d_usd",
        "complete_14d_window",
        "unflagged_payment_buffer_14d_usd",
        "net_screen_contribution_14d_usd",
    }
    expected_payment_columns = {
        "payment_id",
        "date",
        "account_id",
        "entity_id",
        "entity_name",
        "region",
        "currency",
        "bank_name",
        "priority_payment_cohort",
        "exception_flag",
        "repair_minutes",
    }
    if set(account_days.columns) != expected_account_columns:
        failures.append("account-day columns changed")
    if set(payment_facts.columns) != expected_payment_columns:
        failures.append("payment-fact columns changed")
    if failures:
        raise AssertionError(
            f"Dashboard filter fact reconciliation failures: {failures}"
        )

    account_dates = pd.to_datetime(account_days["date"], errors="coerce")
    payment_dates = pd.to_datetime(payment_facts["date"], errors="coerce")
    dimensions = [
        "entity_id",
        "entity_name",
        "region",
        "currency",
        "bank_name",
    ]
    if len(account_days) != 9_955:
        failures.append("account-day row count is not 9,955")
    if account_days.duplicated(["date", "account_id"]).any():
        failures.append("account-day keys are not unique")
    if account_days["account_id"].nunique() != 55:
        failures.append("account-day facts do not cover 55 accounts")
    if account_dates.nunique() != 181:
        failures.append("account-day facts do not cover 181 dates")
    if (
        account_dates.min() != pd.Timestamp("2026-01-01")
        or account_dates.max() != pd.Timestamp("2026-06-30")
    ):
        failures.append("account-day date range changed")
    if not account_days.groupby("account_id").size().eq(181).all():
        failures.append("account-day panel is not complete by account")
    if account_days[dimensions].isna().any().any():
        failures.append("account-day dimensions contain nulls")
    if set(account_days["region"].unique()) != {"APAC", "EMEA", "NA"}:
        failures.append("region values changed or literal NA was parsed as null")
    expected_dimension_counts = {
        "entity_id": 16,
        "entity_name": 16,
        "region": 3,
        "currency": 10,
        "bank_name": 5,
    }
    for dimension, expected in expected_dimension_counts.items():
        if account_days[dimension].nunique() != expected:
            failures.append(f"{dimension} option count changed")
    stable_dimensions = (
        account_days.groupby("account_id")[dimensions]
        .nunique()
        .le(1)
        .all()
        .all()
    )
    if not stable_dimensions:
        failures.append("account dimensions change across dates")
    if not account_days["reporting_delay_days"].between(0, 3).all():
        failures.append("reporting-delay domain changed")
    if not account_days["positive_available_usd"].ge(0).all():
        failures.append("positive availability contains negative values")
    if not account_days["restricted_positive_available_usd"].ge(0).all():
        failures.append("restricted positive availability contains negative values")
    if not account_days["restricted_positive_available_usd"].le(
        account_days["positive_available_usd"]
    ).all():
        failures.append("restricted availability exceeds positive availability")
    if not account_days["negative_available_usd"].le(0).all():
        failures.append("negative availability contains positive values")

    daily_visibility = pd.DataFrame(
        {
            "date": account_dates,
            "same_day": account_days["reporting_delay_days"].eq(0),
            "delayed": account_days["reporting_delay_days"].gt(0),
        }
    ).groupby("date")[["same_day", "delayed"]].sum()
    if not daily_visibility["same_day"].eq(32).all():
        failures.append("same-day account count is not 32 on every date")
    if not daily_visibility["delayed"].eq(23).all():
        failures.append("delayed account count is not 23 on every date")

    expected_complete_rows = {7: 9_625, 14: 9_240}
    for days in [7, 14]:
        complete_column = f"complete_{days}d_window"
        value_columns = [
            f"unflagged_payment_buffer_{days}d_usd",
            f"net_screen_contribution_{days}d_usd",
        ]
        expected_complete = account_dates.ge(
            pd.Timestamp("2026-01-01") + pd.Timedelta(days=days - 1)
        )
        if not account_days[complete_column].eq(expected_complete).all():
            failures.append(f"{days}-day completeness flags changed")
        if int(account_days[complete_column].sum()) != expected_complete_rows[days]:
            failures.append(f"{days}-day complete row count changed")
        complete = account_days[complete_column]
        if account_days.loc[complete, value_columns].isna().any().any():
            failures.append(f"{days}-day complete rows contain null results")
        if account_days.loc[~complete, value_columns].notna().any().any():
            failures.append(f"{days}-day incomplete rows publish numeric results")

    latest = account_days.loc[account_dates.eq(pd.Timestamp("2026-06-30"))]
    latest_expected = {
        "positive_available_usd": 57_801_215.46,
        "restricted_positive_available_usd": 8_053_700.97,
        "negative_available_usd": -2_138_293.10,
        "unflagged_payment_buffer_7d_usd": 5_485_896.33,
        "net_screen_contribution_7d_usd": 42_844_787.78,
        "unflagged_payment_buffer_14d_usd": 10_828_186.91,
        "net_screen_contribution_14d_usd": 38_127_490.73,
    }
    for column, expected in latest_expected.items():
        if round(latest[column].sum(), 2) != expected:
            failures.append(f"latest {column} changed")

    if len(payment_facts) != 7_600:
        failures.append("payment-fact row count is not 7,600")
    if payment_facts["payment_id"].duplicated().any():
        failures.append("payment-fact keys are not unique")
    if payment_facts[dimensions].isna().any().any():
        failures.append("payment-fact dimensions contain nulls")
    if set(payment_facts["region"].unique()) != {"APAC", "EMEA", "NA"}:
        failures.append("payment regions changed or literal NA was parsed as null")
    if payment_dates.isna().any() or payment_dates.min() < pd.Timestamp(
        "2026-01-01"
    ) or payment_dates.max() > pd.Timestamp("2026-06-30"):
        failures.append("payment dates fall outside the supplied period")
    if payment_facts["payment_id"].nunique() != 7_600:
        failures.append("payment facts do not contain 7,600 unique payments")
    if payment_facts["account_id"].nunique() != 51:
        failures.append("payment facts do not cover 51 represented accounts")
    if not payment_facts["exception_flag"].isin([True, False]).all():
        failures.append("payment exception flag is not boolean")
    if not payment_facts["repair_minutes"].ge(0).all():
        failures.append("payment repair minutes contain negative values")
    if int(payment_facts["exception_flag"].sum()) != 479:
        failures.append("payment exceptions do not reconcile to 479")
    if int(payment_facts["repair_minutes"].sum()) != 20_080:
        failures.append("payment repair minutes do not reconcile to 20,080")

    expected_cohorts = {
        "Manual touch only": (2_053, 246, 10_018),
        "Manual touch + cross-border wire": (342, 58, 2_702),
        "Cross-border wire only": (444, 52, 2_219),
        "Neither priority cohort": (4_761, 123, 5_141),
    }
    if set(payment_facts["priority_payment_cohort"].unique()) != set(
        expected_cohorts
    ):
        failures.append("priority payment cohort domain changed")
    else:
        cohort_totals = payment_facts.groupby(
            "priority_payment_cohort", observed=True
        ).agg(
            records=("payment_id", "size"),
            exceptions=("exception_flag", "sum"),
            repair_minutes=("repair_minutes", "sum"),
        )
        for cohort, expected in expected_cohorts.items():
            actual = tuple(int(value) for value in cohort_totals.loc[cohort])
            if actual != expected:
                failures.append(f"{cohort} facts changed")

    account_lookup = account_days.drop_duplicates("account_id").set_index(
        "account_id"
    )
    if not payment_facts["account_id"].isin(account_lookup.index).all():
        failures.append("payment facts contain unknown accounts")
    else:
        for dimension in dimensions:
            mapped = payment_facts["account_id"].map(account_lookup[dimension])
            if not payment_facts[dimension].eq(mapped).all():
                failures.append(f"payment {dimension} differs from account dimension")

    if failures:
        raise AssertionError(
            f"Dashboard filter fact reconciliation failures: {failures}"
        )


def build_liquidity_scenarios(
    balances: pd.DataFrame, payments: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Build daily liquidity layers and 7/14-day screening sensitivities.

    Seven days provides a near-term trailing payment-intent reference; 14 days
    extends the stability test across two weeks. Both use supplied payment
    records in the trailing calendar window ending on the latest balance date.
    Neither is a certified cash forecast or approved operating-cash policy.
    """
    working = balances.copy()
    buffer_payments = payments.copy()
    completed_repaired_payments = payments.loc[
        payments["status"].isin({"Completed", "Repaired"})
    ].copy()
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

    daily_payment_outflow = _account_date_payment_outflow(
        working, buffer_payments
    )
    first_balance_date = working["date"].min()
    for window_days in [7, 14]:
        buffer_column = f"supplied_payment_buffer_{window_days}d_usd"
        gross_column = f"gross_scenario_surplus_after_{window_days}d_buffer_usd"
        net_column = f"net_scenario_surplus_after_{window_days}d_buffer_usd"
        rolling_buffer = (
            daily_payment_outflow.groupby(level="account_id")
            .rolling(window_days, min_periods=window_days)
            .sum()
            .reset_index(level=0, drop=True)
            .rename(buffer_column)
            .reset_index()
        )
        scenario_accounts = working.merge(
            rolling_buffer,
            on=["account_id", "date"],
            how="left",
            validate="one_to_one",
        )
        scenario_accounts[gross_column] = (
            scenario_accounts["positive_available_usd"]
            - scenario_accounts[buffer_column]
        ).clip(lower=0)
        scenario_accounts[gross_column] = scenario_accounts[gross_column].where(
            ~scenario_accounts["restricted_flag"], 0.0
        )
        scenario_daily = scenario_accounts.groupby("date", as_index=False).agg(
            **{
                gross_column: (gross_column, "sum"),
                net_column: (
                    "negative_available_usd",
                    "sum",
                ),
            }
        )
        scenario_daily[net_column] = (
            scenario_daily[gross_column] + scenario_daily[net_column]
        )
        first_complete_date = first_balance_date + pd.Timedelta(
            days=window_days - 1
        )
        incomplete_window = scenario_daily["date"].lt(first_complete_date)
        scenario_daily.loc[incomplete_window, [gross_column, net_column]] = float(
            "nan"
        )
        daily = daily.merge(
            scenario_daily,
            on="date",
            how="left",
            validate="one_to_one",
        )

    latest_date = working["date"].max()
    account_scenarios = working.loc[working["date"].eq(latest_date)].copy()
    for window_days in [7, 14]:
        window_start = latest_date - pd.Timedelta(days=window_days - 1)
        buffer_by_account = (
            buffer_payments.loc[
                buffer_payments["payment_date"].between(window_start, latest_date)
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
        "Uncertified screening windows do not separately validate complete cash needs; result is not movable cash"
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
    completed_repaired_14d = (
        completed_repaired_payments.loc[
            completed_repaired_payments["payment_date"].between(
                latest_date - pd.Timedelta(days=13), latest_date
            )
        ]
        .groupby("account_id")["amount_usd"]
        .sum()
    )
    completed_repaired_14d_buffer = (
        account_scenarios["account_id"].map(completed_repaired_14d).fillna(0.0)
    )
    completed_repaired_14d_surplus = (
        account_scenarios["positive_available_usd"] - completed_repaired_14d_buffer
    ).clip(lower=0)
    completed_repaired_14d_surplus = completed_repaired_14d_surplus.where(
        ~account_scenarios["restricted_flag"], 0.0
    )
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
            "apparent_net_after_preliminary_restriction_before_buffer",
            latest_daily["preliminarily_unflagged_positive_available_usd"]
            + latest_daily["gross_negative_estimated_available_usd"],
            "Restriction screen after netting",
            "Before an operating buffer; not validated movable cash",
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
            "Seven-day screening result",
            "Short-horizon payment-intent sensitivity; not validated movable cash",
            "ANALYST-CALC / ANALYST-ASSUMPTION",
        ),
        (
            "net_scenario_surplus_after_7d_buffer",
            daily.loc[
                daily["date"].eq(latest_date),
                "net_scenario_surplus_after_7d_buffer_usd",
            ].iloc[0],
            "Seven-day screening result after netting",
            "Includes negative positions; not an approved buffer, forecast, or movable cash",
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
            "14-day screening result",
            "Two-week stability sensitivity; not validated movable cash",
            "ANALYST-CALC / ANALYST-ASSUMPTION",
        ),
        (
            "net_scenario_surplus_after_14d_buffer",
            daily.loc[
                daily["date"].eq(latest_date),
                "net_scenario_surplus_after_14d_buffer_usd",
            ].iloc[0],
            "14-day screening result after netting",
            "Includes negative positions; not an approved buffer, forecast, or movable cash",
            "ANALYST-CALC / ANALYST-ASSUMPTION",
        ),
        (
            "completed_repaired_status_sensitivity_14d_gross_surplus",
            completed_repaired_14d_surplus.sum(),
            "Payment-status sensitivity",
            "Excludes Rejected/Pending records; not validated movable cash",
            "ANALYST-CALC / ANALYST-ASSUMPTION",
        ),
        (
            "completed_repaired_status_sensitivity_14d_net_surplus",
            completed_repaired_14d_surplus.sum()
            + latest_daily["gross_negative_estimated_available_usd"],
            "Payment-status sensitivity after netting",
            "Excludes Rejected/Pending records; not validated movable cash",
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

    threshold_rows = []
    for window_days in [7, 14]:
        net_column = f"net_scenario_surplus_after_{window_days}d_buffer_usd"
        eligible = daily.loc[daily[net_column].notna()]
        for threshold_name, threshold_usd in [
            ("stress", 21_000_000),
            ("base", 35_000_000),
            ("upside", 46_200_000),
        ]:
            days_met = int(eligible[net_column].ge(threshold_usd).sum())
            threshold_rows.append(
                {
                    "buffer_window_days": window_days,
                    "threshold_name": threshold_name,
                    "threshold_usd": threshold_usd,
                    "complete_window_days": len(eligible),
                    "days_threshold_met": days_met,
                    "threshold_met_rate_pct": round(100 * days_met / len(eligible), 2),
                    "minimum_net_scenario_surplus_usd": round(
                        eligible[net_column].min(), 2
                    ),
                    "median_net_scenario_surplus_usd": round(
                        eligible[net_column].median(), 2
                    ),
                    "evidence_label": "ANALYST-CALC / ANALYST-ASSUMPTION",
                    "decision_boundary": (
                        "Scenario screen only; no threshold is validated movable cash"
                    ),
                }
            )
    thresholds = pd.DataFrame(threshold_rows)
    return daily, account_scenarios, summary, thresholds


def longest_true_run(values: pd.Series) -> int:
    """Return the longest consecutive run of truthy values."""
    longest = 0
    current = 0
    for value in values:
        if bool(value):
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest


def build_simultaneous_position_diagnostic(
    balances: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Identify persistent account deficits and concurrent surplus positions."""
    working = balances.copy().sort_values(["date", "account_id"])
    working["positive_available_usd"] = working["available_balance_usd"].clip(
        lower=0
    )
    working["negative_available_usd"] = working["available_balance_usd"].clip(
        upper=0
    )

    daily_accounts = working.groupby("date", as_index=False).agg(
        positive_account_count=(
            "available_balance_usd",
            lambda series: int(series.gt(0).sum()),
        ),
        zero_account_count=(
            "available_balance_usd",
            lambda series: int(series.eq(0).sum()),
        ),
        negative_account_count=(
            "available_balance_usd",
            lambda series: int(series.lt(0).sum()),
        ),
        gross_positive_available_usd=("positive_available_usd", "sum"),
        gross_negative_available_usd=("negative_available_usd", "sum"),
        net_estimated_available_usd=("available_balance_usd", "sum"),
    )
    daily_accounts["simultaneous_account_positions_flag"] = (
        daily_accounts["positive_account_count"].gt(0)
        & daily_accounts["negative_account_count"].gt(0)
    )
    daily_accounts["gross_positive_to_deficit_ratio"] = (
        daily_accounts["gross_positive_available_usd"]
        / daily_accounts["gross_negative_available_usd"].abs()
    )

    entity_date = working.groupby(
        ["date", "entity_id", "entity_name", "region"], as_index=False
    ).agg(
        account_count=("account_id", "nunique"),
        positive_account_count=(
            "available_balance_usd",
            lambda series: int(series.gt(0).sum()),
        ),
        negative_account_count=(
            "available_balance_usd",
            lambda series: int(series.lt(0).sum()),
        ),
        gross_account_positive_available_usd=("positive_available_usd", "sum"),
        gross_account_negative_available_usd=("negative_available_usd", "sum"),
        entity_net_estimated_available_usd=("available_balance_usd", "sum"),
    )
    entity_date["within_entity_mixed_sign_flag"] = (
        entity_date["positive_account_count"].gt(0)
        & entity_date["negative_account_count"].gt(0)
    )
    entity_date["entity_net_deficit_flag"] = entity_date[
        "entity_net_estimated_available_usd"
    ].lt(0)

    daily_entities = entity_date.groupby("date", as_index=False).agg(
        positive_entity_count=(
            "entity_net_estimated_available_usd",
            lambda series: int(series.gt(0).sum()),
        ),
        zero_entity_count=(
            "entity_net_estimated_available_usd",
            lambda series: int(series.eq(0).sum()),
        ),
        deficit_entity_count=(
            "entity_net_estimated_available_usd",
            lambda series: int(series.lt(0).sum()),
        ),
        gross_entity_surplus_usd=(
            "entity_net_estimated_available_usd",
            lambda series: series.clip(lower=0).sum(),
        ),
        gross_entity_deficit_usd=(
            "entity_net_estimated_available_usd",
            lambda series: series.clip(upper=0).sum(),
        ),
        entity_net_estimated_available_usd=(
            "entity_net_estimated_available_usd",
            "sum",
        ),
    )
    daily_entities["simultaneous_entity_positions_flag"] = (
        daily_entities["positive_entity_count"].gt(0)
        & daily_entities["deficit_entity_count"].gt(0)
    )
    daily = daily_accounts.merge(
        daily_entities, on="date", how="left", validate="one_to_one"
    )
    if not daily["net_estimated_available_usd"].round(2).eq(
        daily["entity_net_estimated_available_usd"].round(2)
    ).all():
        raise AssertionError("Entity positions do not reconcile to group net availability")
    daily["evidence_label"] = "ANALYST-CALC"
    daily["decision_boundary"] = (
        "Concurrent positions do not prove avoidable borrowing, transferability, or interest cost"
    )
    entity_date["evidence_label"] = "ANALYST-CALC"
    entity_date["decision_boundary"] = (
        "Entity deficit is an estimated position, not evidence of facility use or avoidable funding cost"
    )

    account_rows = []
    account_fields = [
        "account_id",
        "entity_id",
        "entity_name",
        "region",
        "country",
        "purpose",
        "status",
        "visibility_method",
        "restricted_flag",
        "sweep_structure",
    ]
    for account_id, frame in working.groupby("account_id", sort=True):
        frame = frame.sort_values("date")
        first = frame.iloc[0]
        negative = frame["available_balance_usd"].lt(0)
        account_rows.append(
            {
                **{field: first[field] for field in account_fields},
                "observed_days": len(frame),
                "negative_position_days": int(negative.sum()),
                "positive_position_days": int(
                    frame["available_balance_usd"].gt(0).sum()
                ),
                "longest_negative_run_days": longest_true_run(negative),
                "average_available_usd": round(
                    frame["available_balance_usd"].mean(), 2
                ),
                "minimum_available_usd": round(
                    frame["available_balance_usd"].min(), 2
                ),
                "maximum_available_usd": round(
                    frame["available_balance_usd"].max(), 2
                ),
                "persistent_deficit_flag": bool(negative.all()),
                "evidence_label": "ANALYST-CALC",
                "decision_boundary": (
                    "Negative estimate does not establish borrowing, overdraft, or avoidable interest"
                ),
            }
        )
    account_summary = pd.DataFrame(account_rows)
    return daily, entity_date, account_summary


def build_payment_diagnostic(payments: pd.DataFrame) -> pd.DataFrame:
    """Profile payment friction by rate and absolute contribution.

    All results remain bounded to the supplied 7,600-record extract. Cohort
    rates use cohort record counts; contribution shares use the full extract's
    issue or effort total so that small high-rate cohorts are not overstated.
    Manual touch and cross-border wire are also split into four mutually
    exclusive cohorts so their overlap can be shown without double counting.
    """
    working = add_priority_payment_cohorts(payments)
    working["amount_band_usd"] = pd.cut(
        working["amount_usd"],
        bins=[float("-inf"), 10_000, 25_000, 50_000, 100_000, float("inf")],
        labels=[
            "≤$10k",
            ">$10k–$25k",
            ">$25k–$50k",
            ">$50k–$100k",
            ">$100k",
        ],
        ordered=True,
    )
    working["manual_touch_cohort"] = working["manual_touch_flag"].map(
        {True: "Manual touch", False: "No manual touch"}
    )
    working["cross_border_cohort"] = working["cross_border_flag"].map(
        {True: "Cross-border", False: "Domestic"}
    )
    manual_touch = working["manual_touch_flag"]
    cross_border_wire = working["cross_border_wire_flag"]
    totals = {
        "records": len(working),
        "value_usd": working["amount_usd"].sum(),
        "exceptions": working["exception_flag"].sum(),
        "exception_value_usd": working.loc[
            working["exception_flag"], "amount_usd"
        ].sum(),
        "late": working["late_release_flag"].sum(),
        "repair_minutes": working["repair_minutes"].sum(),
        "fees": working["fee_usd"].sum(),
    }

    def summarize(
        frame: pd.DataFrame,
        dimension: str,
        category: str,
        dimension_population: str,
    ) -> dict:
        records = len(frame)
        return {
            "dimension": dimension,
            "category": str(category),
            "dimension_population": dimension_population,
            "records": records,
            "represented_accounts": frame["account_id"].nunique(),
            "record_share_of_extract_pct": round(
                100 * records / totals["records"], 2
            ),
            "gross_supplied_record_value_usd": round(frame["amount_usd"].sum(), 2),
            "value_share_of_extract_pct": round(
                100 * frame["amount_usd"].sum() / totals["value_usd"], 2
            ),
            "manual_touch_records": int(frame["manual_touch_flag"].sum()),
            "manual_touch_rate_pct": round(
                100 * frame["manual_touch_flag"].mean(), 2
            ),
            "exception_records": int(frame["exception_flag"].sum()),
            "exception_rate_pct": round(100 * frame["exception_flag"].mean(), 2),
            "exception_contribution_pct": round(
                100 * frame["exception_flag"].sum() / totals["exceptions"], 2
            ),
            "exception_record_value_usd": round(
                frame.loc[frame["exception_flag"], "amount_usd"].sum(), 2
            ),
            "exception_value_contribution_pct": round(
                100
                * frame.loc[frame["exception_flag"], "amount_usd"].sum()
                / totals["exception_value_usd"],
                2,
            ),
            "late_release_records": int(frame["late_release_flag"].sum()),
            "late_release_rate_pct": round(
                100 * frame["late_release_flag"].mean(), 2
            ),
            "late_release_contribution_pct": round(
                100 * frame["late_release_flag"].sum() / totals["late"], 2
            ),
            "rejected_records": int(frame["status"].eq("Rejected").sum()),
            "rejection_rate_pct": round(
                100 * frame["status"].eq("Rejected").mean(), 2
            ),
            "pending_records": int(frame["status"].eq("Pending").sum()),
            "pending_rate_pct": round(
                100 * frame["status"].eq("Pending").mean(), 2
            ),
            "repair_minutes": int(frame["repair_minutes"].sum()),
            "repair_contribution_pct": round(
                100 * frame["repair_minutes"].sum() / totals["repair_minutes"], 2
            ),
            "estimated_fees_usd": round(frame["fee_usd"].sum(), 2),
            "fee_contribution_pct": round(
                100 * frame["fee_usd"].sum() / totals["fees"], 2
            ),
            "cross_border_records": int(frame["cross_border_flag"].sum()),
            "cross_border_rate_pct": round(
                100 * frame["cross_border_flag"].mean(), 2
            ),
            "overlap_share_of_manual_touch_pct": float("nan"),
            "overlap_share_of_cross_border_wire_pct": float("nan"),
            "evidence_label": "ANALYST-CALC",
            "decision_boundary": (
                "Within supplied 7,600 records only; association does not establish cause or ACG-wide performance"
            ),
        }

    rows = [
        summarize(
            working,
            "overall",
            "All supplied payment records",
            "All 7,600 supplied records",
        )
    ]
    dimensions = [
        ("manual_touch", "manual_touch_cohort", "All 7,600 supplied records"),
        ("payment_type", "payment_type", "All 7,600 supplied records"),
        ("cross_border", "cross_border_cohort", "All 7,600 supplied records"),
        ("region", "region", "All 7,600 supplied records"),
        ("account_purpose", "purpose", "All 7,600 supplied records"),
        ("visibility_method", "visibility_method", "All 7,600 supplied records"),
        ("bank", "bank_name", "All 7,600 supplied records"),
        ("erp_system", "erp_system", "All 7,600 supplied records"),
        ("status", "status", "All 7,600 supplied records"),
        ("month", "month", "All 7,600 supplied records"),
        ("amount_band_usd", "amount_band_usd", "All 7,600 supplied records"),
    ]
    for dimension, column, population in dimensions:
        for category, frame in working.groupby(column, sort=False, observed=True):
            rows.append(summarize(frame, dimension, category, population))

    for category in PRIORITY_PAYMENT_CATEGORIES:
        frame = working.loc[working["priority_payment_cohort"].eq(category)]
        row = summarize(
            frame,
            "priority_payment_cohort",
            category,
            "All 7,600 supplied records; four mutually exclusive cohorts",
        )
        if category == "Manual touch + cross-border wire":
            row["overlap_share_of_manual_touch_pct"] = round(
                100 * len(frame) / int(manual_touch.sum()), 2
            )
            row["overlap_share_of_cross_border_wire_pct"] = round(
                100 * len(frame) / int(cross_border_wire.sum()), 2
            )
        rows.append(row)

    for category in [
        "Manual touch or cross-border wire",
        "Outside priority union",
    ]:
        frame = working.loc[working["priority_union_cohort"].eq(category)]
        rows.append(
            summarize(
                frame,
                "priority_union",
                category,
                "All 7,600 supplied records; priority cohorts deduplicated",
            )
        )

    wires = working.loc[working["payment_type"].eq("Wire")].copy()
    wires["wire_geography"] = wires["cross_border_flag"].map(
        {True: "Cross-border wire", False: "Domestic wire"}
    )
    for category in ["Cross-border wire", "Domestic wire"]:
        frame = wires.loc[wires["wire_geography"].eq(category)]
        rows.append(
            summarize(frame, "wire_geography", category, "1,398 supplied wire records")
        )
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
    repair_reconciliation = build_repair_baseline_reconciliation(
        payments, process_capacity
    )
    validate_reconciliations(data, balances, payments, process_capacity)

    reconciliation = build_reconciliation_metrics(
        data, balances, payments, process_capacity
    )
    account_diagnostic = build_account_diagnostic(data, balances, payments)
    visibility_diagnostic = build_visibility_diagnostic(balances)
    (
        liquidity_daily,
        liquidity_accounts,
        liquidity_summary,
        liquidity_thresholds,
    ) = build_liquidity_scenarios(balances, payments)
    dashboard_account_day_facts = build_dashboard_account_day_facts(
        balances, payments
    )
    dashboard_payment_facts = build_dashboard_payment_facts(payments)
    validate_dashboard_filter_facts(
        dashboard_account_day_facts, dashboard_payment_facts
    )
    (
        simultaneous_daily,
        entity_positions,
        account_positions,
    ) = build_simultaneous_position_diagnostic(balances)
    payment_diagnostic = build_payment_diagnostic(payments)
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
    liquidity_thresholds.to_csv(
        PROCESSED / "W2_liquidity_thresholds.csv", index=False
    )
    dashboard_account_day_facts.to_csv(
        PROCESSED / "W2_dashboard_account_day_facts.csv", index=False
    )
    dashboard_payment_facts.to_csv(
        PROCESSED / "W2_dashboard_payment_facts.csv", index=False
    )
    simultaneous_daily.to_csv(
        PROCESSED / "W2_simultaneous_positions_daily.csv", index=False
    )
    entity_positions.to_csv(PROCESSED / "W2_entity_positions.csv", index=False)
    account_positions.to_csv(PROCESSED / "W2_account_positions.csv", index=False)
    payment_diagnostic.to_csv(PROCESSED / "W2_payment_diagnostic.csv", index=False)
    process_capacity.to_csv(PROCESSED / "W2_process_capacity.csv", index=False)
    repair_reconciliation.to_csv(
        PROCESSED / "W2_repair_baseline_reconciliation.csv", index=False
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
    print("Wrote data/processed/W2_liquidity_daily.csv")
    print("Wrote data/processed/W2_liquidity_account_scenarios.csv")
    print("Wrote data/processed/W2_liquidity_scenarios.csv")
    print("Wrote data/processed/W2_liquidity_thresholds.csv")
    print("Wrote data/processed/W2_dashboard_account_day_facts.csv")
    print("Wrote data/processed/W2_dashboard_payment_facts.csv")
    print("Wrote data/processed/W2_simultaneous_positions_daily.csv")
    print("Wrote data/processed/W2_entity_positions.csv")
    print("Wrote data/processed/W2_account_positions.csv")
    print("Wrote data/processed/W2_payment_diagnostic.csv")
    print("Wrote data/processed/W2_process_capacity.csv")
    print("Wrote data/processed/W2_repair_baseline_reconciliation.csv")


if __name__ == "__main__":
    main()
