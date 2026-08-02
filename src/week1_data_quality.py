"""Reproducible Week 1 data-quality assessment for Project Northstar.

The script does not alter raw data. It writes reconciled control totals and
quality summaries to ``data/processed`` for use in the Week 1 evidence pack.
"""

from pathlib import Path

import pandas as pd

from starter_analysis import enrich_balances, load_data, validate_keys


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def metric(name: str, value, unit: str, source: str, note: str = "") -> dict:
    return {"metric": name, "value": value, "unit": unit, "source": source, "note": note}


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    data = load_data()
    validate_keys(data)
    balances = enrich_balances(data)

    entities = data["entities"]
    accounts = data["accounts"]
    payments = data["payments"]
    fx = data["fx"]
    process = data["process"]

    payment_enriched = payments.merge(
        accounts[["account_id", "entity_id", "currency"]].rename(columns={"currency": "account_currency"}),
        on="account_id",
        how="left",
        validate="many_to_one",
    ).merge(
        fx.rename(columns={"date": "payment_date"}),
        on=["payment_date", "currency"],
        how="left",
        validate="many_to_one",
    ).merge(
        entities[["entity_id", "region"]],
        on="entity_id",
        how="left",
        validate="many_to_one",
    )
    payment_enriched["amount_usd"] = (
        payment_enriched["amount_local"] * payment_enriched["usd_per_unit"]
    )

    latest_date = balances["date"].max()
    latest_balances = balances[balances["date"] == latest_date]
    expected_balance_rows = accounts["account_id"].nunique() * balances["date"].nunique()
    expected_fx_rows = fx["currency"].nunique() * fx["date"].nunique()

    rows = [
        metric("entity_rows", len(entities), "rows", "entity_master.csv"),
        metric("unique_entities", entities["entity_id"].nunique(), "entities", "entity_master.csv"),
        metric("countries", accounts["country"].nunique(), "countries", "bank_accounts.csv"),
        metric("regions", entities["region"].nunique(), "regions", "entity_master.csv"),
        metric("erp_environments", entities["erp_system"].nunique(), "systems", "entity_master.csv"),
        metric("revenue_control_total", entities["revenue_usd_m"].sum(), "USD millions", "entity_master.csv"),
        metric("account_rows", len(accounts), "rows", "bank_accounts.csv"),
        metric("unique_accounts", accounts["account_id"].nunique(), "accounts", "bank_accounts.csv"),
        metric("active_accounts", accounts["status"].eq("Active").sum(), "accounts", "bank_accounts.csv"),
        metric("dormant_accounts", accounts["status"].eq("Dormant").sum(), "accounts", "bank_accounts.csv"),
        metric("restricted_accounts_preliminary", accounts["restricted_flag"].sum(), "accounts", "bank_accounts.csv", "Requires legal/tax validation"),
        metric("banks", accounts["bank_name"].nunique(), "banks", "bank_accounts.csv"),
        metric("account_currencies", accounts["currency"].nunique(), "currencies", "bank_accounts.csv"),
        metric("annual_account_fee_control_total", accounts["annual_fee_usd"].sum(), "USD/year", "bank_accounts.csv", "Estimated, not actual pricing"),
        metric("balance_rows", len(balances), "rows", "daily_balances.csv"),
        metric("balance_start_date", balances["date"].min().date().isoformat(), "date", "daily_balances.csv"),
        metric("balance_end_date", latest_date.date().isoformat(), "date", "daily_balances.csv"),
        metric("balance_dates", balances["date"].nunique(), "calendar days", "daily_balances.csv"),
        metric("expected_balance_rows", expected_balance_rows, "rows", "calculation"),
        metric("balance_row_completeness", round(100 * len(balances) / expected_balance_rows, 2), "%", "calculation"),
        metric("same_day_visibility_observations", balances["reporting_delay_days"].eq(0).sum(), "observations", "calculation"),
        metric("same_day_visibility_rate", round(100 * balances["reporting_delay_days"].eq(0).mean(), 2), "%", "calculation"),
        metric("one_day_delayed_observations", balances["reporting_delay_days"].eq(1).sum(), "observations", "calculation"),
        metric("two_or_more_day_delayed_observations", balances["reporting_delay_days"].ge(2).sum(), "observations", "calculation"),
        metric("maximum_reporting_delay", balances["reporting_delay_days"].max(), "days", "calculation"),
        metric("automated_balance_observations", balances["source_quality"].eq("Automated").sum(), "observations", "daily_balances.csv"),
        metric("manually_reported_balance_observations", balances["source_quality"].eq("Manually reported").sum(), "observations", "daily_balances.csv"),
        metric("estimated_balance_observations", balances["source_quality"].eq("Estimated").sum(), "observations", "daily_balances.csv"),
        metric("latest_closing_balance", round(latest_balances["closing_balance_usd"].sum(), 2), "USD", "calculation", "Ledger balance; not proof of transferability"),
        metric("latest_available_balance", round(latest_balances["available_balance_usd"].sum(), 2), "USD", "calculation", "Estimated availability; requires validation"),
        metric("fx_rows", len(fx), "rows", "fx_rates.csv"),
        metric("fx_currencies", fx["currency"].nunique(), "currencies", "fx_rates.csv"),
        metric("fx_dates", fx["date"].nunique(), "calendar days", "fx_rates.csv"),
        metric("expected_fx_rows", expected_fx_rows, "rows", "calculation"),
        metric("payment_rows", len(payments), "rows", "payments.csv"),
        metric("unique_payments", payments["payment_id"].nunique(), "payments", "payments.csv"),
        metric("payment_start_date", payments["payment_date"].min().date().isoformat(), "date", "payments.csv"),
        metric("payment_end_date", payments["payment_date"].max().date().isoformat(), "date", "payments.csv"),
        metric("payment_value_control_total", round(payment_enriched["amount_usd"].sum(), 2), "USD", "calculation"),
        metric("payment_fee_control_total", round(payments["fee_usd"].sum(), 2), "USD", "payments.csv", "Estimated fees, not actual bank pricing"),
        metric("manual_touch_payments", payments["manual_touch_flag"].sum(), "payments", "payments.csv"),
        metric("manual_touch_rate", round(100 * payments["manual_touch_flag"].mean(), 2), "%", "calculation"),
        metric("exception_payments", payments["exception_flag"].sum(), "payments", "payments.csv"),
        metric("exception_rate", round(100 * payments["exception_flag"].mean(), 2), "%", "calculation"),
        metric("late_release_payments", payments["late_release_flag"].sum(), "payments", "payments.csv"),
        metric("late_release_rate", round(100 * payments["late_release_flag"].mean(), 2), "%", "calculation"),
        metric("rejected_payments", payments["status"].eq("Rejected").sum(), "payments", "payments.csv"),
        metric("repair_minutes", payments["repair_minutes"].sum(), "minutes", "payments.csv", "Management-estimated effort"),
        metric("process_rows", len(process), "activities", "process_activity.csv"),
        metric("estimated_manual_process_hours_monthly", round((process["frequency_per_month"] * process["minutes_per_instance"] * process["manual_percentage"] / 100 / 60).sum(), 2), "hours/month", "calculation", "Management estimates; not time-and-motion evidence"),
    ]

    missing_rows = []
    for dataset_name, frame in data.items():
        for column in frame.columns:
            missing_rows.append({
                "dataset": dataset_name,
                "column": column,
                "missing_count": int(frame[column].isna().sum()),
                "missing_rate_pct": round(100 * frame[column].isna().mean(), 4),
            })

    checks = [
        ("entity_primary_key_unique", entities["entity_id"].is_unique),
        ("account_primary_key_unique", accounts["account_id"].is_unique),
        ("payment_primary_key_unique", payments["payment_id"].is_unique),
        ("balance_account_date_unique", not balances.duplicated(["account_id", "date"]).any()),
        ("fx_currency_date_unique", not fx.duplicated(["currency", "date"]).any()),
        ("account_entities_resolve", accounts["entity_id"].isin(entities["entity_id"]).all()),
        ("balance_accounts_resolve", balances["account_id"].isin(accounts["account_id"]).all()),
        ("payment_accounts_resolve", payments["account_id"].isin(accounts["account_id"]).all()),
        ("balance_fx_resolves", balances["usd_per_unit"].notna().all()),
        ("payment_fx_resolves", payment_enriched["usd_per_unit"].notna().all()),
        ("payment_currency_matches_account", payment_enriched["currency"].eq(payment_enriched["account_currency"]).all()),
        ("balance_panel_complete", len(balances) == expected_balance_rows),
        ("fx_panel_complete", len(fx) == expected_fx_rows),
        ("reporting_date_not_before_balance_date", balances["reporting_delay_days"].ge(0).all()),
        ("available_not_above_positive_closing", (balances.loc[balances["closing_balance_local"] > 0, "available_balance_local"] <= balances.loc[balances["closing_balance_local"] > 0, "closing_balance_local"]).all()),
        ("repair_minutes_nonnegative", payments["repair_minutes"].ge(0).all()),
        ("nonexception_repair_minutes_zero", payments.loc[~payments["exception_flag"], "repair_minutes"].eq(0).all()),
        ("all_required_fields_complete", all(frame.notna().all().all() for frame in data.values())),
    ]
    check_frame = pd.DataFrame(checks, columns=["check", "passed"])

    balance_region = balances.groupby("region", as_index=False).agg(
        observations=("account_id", "size"),
        accounts=("account_id", "nunique"),
        same_day_observations=("reporting_delay_days", lambda x: x.eq(0).sum()),
        delayed_observations=("reporting_delay_days", lambda x: x.gt(0).sum()),
        automated_observations=("source_quality", lambda x: x.eq("Automated").sum()),
        manually_reported_observations=("source_quality", lambda x: x.eq("Manually reported").sum()),
        estimated_observations=("source_quality", lambda x: x.eq("Estimated").sum()),
    )
    balance_region["same_day_rate_pct"] = (
        100 * balance_region["same_day_observations"] / balance_region["observations"]
    ).round(2)

    metrics = pd.DataFrame(rows)
    missing = pd.DataFrame(missing_rows)
    metrics.to_csv(PROCESSED / "W1_data_quality_metrics.csv", index=False)
    check_frame.to_csv(PROCESSED / "W1_data_quality_checks.csv", index=False)
    missing.to_csv(PROCESSED / "W1_missingness_profile.csv", index=False)
    balance_region.to_csv(PROCESSED / "W1_visibility_by_region.csv", index=False)

    failed = check_frame.loc[~check_frame["passed"], "check"].tolist()
    print(metrics.to_string(index=False))
    print(f"\nQuality checks passed: {check_frame['passed'].sum()}/{len(check_frame)}")
    if failed:
        raise SystemExit(f"Week 1 data-quality failures: {failed}")
    print("Wrote four reproducible Week 1 outputs to data/processed/.")


if __name__ == "__main__":
    main()
