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
    reconciliation.to_csv(PROCESSED / "W2_reconciliation_metrics.csv", index=False)
    print(reconciliation.to_string(index=False))
    print("\nWrote data/processed/W2_reconciliation_metrics.csv")


if __name__ == "__main__":
    main()
