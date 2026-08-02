"""Starter analytical workflow for Project Northstar.

This module loads, validates, joins, and profiles the project datasets. It
intentionally does not calculate the core engagement answers. Extend it with
documented functions rather than editing raw CSV files.
"""

from pathlib import Path
from typing import Dict

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"


def load_data() -> Dict[str, pd.DataFrame]:
    """Load all case datasets and parse date columns."""
    required = {
        "entities": "entity_master.csv",
        "accounts": "bank_accounts.csv",
        "balances": "daily_balances.csv",
        "payments": "payments.csv",
        "fx": "fx_rates.csv",
        "process": "process_activity.csv",
    }
    missing = [filename for filename in required.values() if not (RAW / filename).exists()]
    if missing:
        raise FileNotFoundError(
            f"Missing {missing}. Run `python3 src/generate_data.py` first."
        )
    data = {name: pd.read_csv(RAW / filename) for name, filename in required.items()}
    data["accounts"]["open_date"] = pd.to_datetime(data["accounts"]["open_date"])
    for column in ["date", "reported_to_group_date"]:
        data["balances"][column] = pd.to_datetime(data["balances"][column])
    data["payments"]["payment_date"] = pd.to_datetime(data["payments"]["payment_date"])
    data["fx"]["date"] = pd.to_datetime(data["fx"]["date"])
    return data


def validate_keys(data: Dict[str, pd.DataFrame]) -> None:
    """Fail fast on duplicate primary keys and broken relationships."""
    assert data["entities"]["entity_id"].is_unique, "Duplicate entity_id"
    assert data["accounts"]["account_id"].is_unique, "Duplicate account_id"
    assert data["payments"]["payment_id"].is_unique, "Duplicate payment_id"
    assert not data["accounts"]["entity_id"].isin(data["entities"]["entity_id"]).eq(False).any(), "Unknown entity"
    assert not data["balances"]["account_id"].isin(data["accounts"]["account_id"]).eq(False).any(), "Unknown balance account"
    assert not data["payments"]["account_id"].isin(data["accounts"]["account_id"]).eq(False).any(), "Unknown payment account"


def enrich_balances(data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Join balance, account, entity, and FX attributes and calculate USD values."""
    balances = data["balances"].merge(data["accounts"], on="account_id", how="left", validate="many_to_one")
    balances = balances.merge(
        data["entities"][["entity_id", "entity_name", "region", "cash_restriction_level"]],
        on="entity_id", how="left", validate="many_to_one",
    )
    balances = balances.merge(
        data["fx"], on=["date", "currency"], how="left", validate="many_to_one",
    )
    if balances["usd_per_unit"].isna().any():
        raise ValueError("Missing FX rate after balance enrichment")
    balances["closing_balance_usd"] = balances["closing_balance_local"] * balances["usd_per_unit"]
    balances["available_balance_usd"] = balances["available_balance_local"] * balances["usd_per_unit"]
    balances["reporting_delay_days"] = (
        balances["reported_to_group_date"] - balances["date"]
    ).dt.days
    return balances


def build_portfolio_profile(data: Dict[str, pd.DataFrame], balances: pd.DataFrame) -> pd.DataFrame:
    """Provide a neutral starting profile; this is not the diagnostic answer."""
    rows = [
        ("entities", data["entities"]["entity_id"].nunique()),
        ("countries", data["accounts"]["country"].nunique()),
        ("accounts", data["accounts"]["account_id"].nunique()),
        ("banks", data["accounts"]["bank_name"].nunique()),
        ("currencies", data["accounts"]["currency"].nunique()),
        ("balance_observations", len(balances)),
        ("payments", len(data["payments"])),
    ]
    return pd.DataFrame(rows, columns=["metric", "value"])


# Your Week 2 work should implement functions such as:
# - classify_account_review_candidates(...)
# - calculate_same_day_visibility(...)
# - calculate_liquidity_scenarios(...)
# - analyze_simultaneous_surplus_and_deficit(...)
# - calculate_payment_operations_kpis(...)
# - quantify_process_capacity(...)
#
# For every function, document definitions, exclusions, assumptions, reconciliation,
# and the client decision supported. Do not use unexplained thresholds.


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    data = load_data()
    validate_keys(data)
    balances = enrich_balances(data)
    profile = build_portfolio_profile(data, balances)
    profile.to_csv(PROCESSED / "starter_portfolio_profile.csv", index=False)
    print(profile.to_string(index=False))
    print("\nStarter profile written to data/processed/starter_portfolio_profile.csv")
    print("Next: complete the Week 1 data-quality report before diagnostic analysis.")


if __name__ == "__main__":
    main()
