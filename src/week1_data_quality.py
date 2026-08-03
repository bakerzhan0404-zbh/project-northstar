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


def missing_mask(series: pd.Series) -> pd.Series:
    """Treat nulls and blank text as missing while preserving valid labels."""
    blank = series.astype("string").str.strip().eq("").fillna(False)
    return series.isna() | blank


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
    same_day = balances["reporting_delay_days"].eq(0)
    balances["positive_closing_usd"] = balances["closing_balance_usd"].clip(lower=0)
    latest_balances = balances[balances["date"] == latest_date]
    latest_balances_same_day = latest_balances["reporting_delay_days"].eq(0)
    latest_positive_available = latest_balances["available_balance_usd"].clip(lower=0)
    payment_exception_process = process[process["process"].eq("Payment exception repair")].iloc[0]

    payment_count_by_account = payments.groupby("account_id").size().reindex(
        accounts["account_id"], fill_value=0
    )
    dormant_validation_candidates = accounts.loc[
        accounts["status"].eq("Dormant")
        & accounts["purpose"].eq("Legacy")
        & accounts["account_id"].map(payment_count_by_account).eq(0)
    ]
    restricted_account_context = accounts.loc[accounts["restricted_flag"]].merge(
        entities[["entity_id"]], on="entity_id", how="left", validate="many_to_one"
    )
    two_plus_day_stale_positive_daily = (
        balances.loc[balances["reporting_delay_days"].ge(2)]
        .groupby("date")["positive_closing_usd"]
        .sum()
    )
    manual_payments = payments["manual_touch_flag"]
    manual_core_payment_types = payments["payment_type"].isin({"Local transfer", "Wire", "ACH"})
    cross_border_wires = payments["payment_type"].eq("Wire") & payments["cross_border_flag"]
    process_manual_hours_monthly = (
        process["frequency_per_month"]
        * process["minutes_per_instance"]
        * process["manual_percentage"]
        / 100
        / 60
    )
    high_control_processes = process["control_criticality"].eq("High")

    expected_schemas = {
        "entities": ["entity_id", "entity_name", "region", "country", "functional_currency", "revenue_usd_m", "erp_system", "acquisition_origin", "cash_restriction_level"],
        "accounts": ["account_id", "entity_id", "bank_name", "country", "currency", "purpose", "open_date", "status", "visibility_method", "sweep_structure", "annual_fee_usd", "restricted_flag"],
        "balances": ["date", "account_id", "closing_balance_local", "available_balance_local", "reported_to_group_date", "source_quality"],
        "payments": ["payment_id", "payment_date", "account_id", "payment_type", "currency", "amount_local", "cross_border_flag", "manual_touch_flag", "exception_flag", "late_release_flag", "repair_minutes", "fee_usd", "status"],
        "fx": ["date", "currency", "usd_per_unit"],
        "process": ["team", "process", "frequency_per_month", "minutes_per_instance", "manual_percentage", "loaded_hourly_cost_usd", "control_criticality"],
    }

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
        metric("restricted_account_rate", round(100 * accounts["restricted_flag"].mean(), 2), "% of accounts", "calculation", "Preliminary flags; not legal/tax conclusions"),
        metric("entities_with_preliminary_restricted_accounts", restricted_account_context["entity_id"].nunique(), "entities", "calculation", "Requires local validation"),
        metric("countries_with_preliminary_restricted_accounts", restricted_account_context["country"].nunique(), "countries", "calculation", "Requires local validation"),
        metric("banks", accounts["bank_name"].nunique(), "banks", "bank_accounts.csv"),
        metric("account_currencies", accounts["currency"].nunique(), "currencies", "bank_accounts.csv"),
        metric("annual_account_fee_control_total", accounts["annual_fee_usd"].sum(), "USD/year", "bank_accounts.csv", "Estimated, not actual pricing"),
        metric("dormant_zero_payment_legacy_candidates", len(dormant_validation_candidates), "accounts", "calculation", "Closure-validation candidates only; local dependencies unknown"),
        metric("dormant_zero_payment_legacy_candidate_fees", dormant_validation_candidates["annual_fee_usd"].sum(), "USD/year", "calculation", "Gross estimated fees before closure cost or feasibility validation"),
        metric("balance_rows", len(balances), "rows", "daily_balances.csv"),
        metric("balance_start_date", balances["date"].min().date().isoformat(), "date", "daily_balances.csv"),
        metric("balance_end_date", latest_date.date().isoformat(), "date", "daily_balances.csv"),
        metric("balance_dates", balances["date"].nunique(), "calendar days", "daily_balances.csv"),
        metric("expected_balance_rows", expected_balance_rows, "rows", "calculation"),
        metric("balance_row_completeness", round(100 * len(balances) / expected_balance_rows, 2), "%", "calculation"),
        metric("same_day_visibility_accounts", balances.loc[same_day, "account_id"].nunique(), "accounts", "calculation", "Count-weighted proxy; not percent of cash"),
        metric("same_day_visibility_observations", same_day.sum(), "account-days", "calculation", "32 of 55 accounts repeat for each of 181 days"),
        metric("same_day_visibility_rate", round(100 * same_day.mean(), 2), "% of account-days", "calculation", "Not start-of-day or percent of cash"),
        metric("within_one_day_visibility_rate", round(100 * balances["reporting_delay_days"].le(1).mean(), 2), "% of account-days", "calculation", "Sensitivity only; not proof of within 24 hours"),
        metric("positive_closing_value_weighted_same_day_rate", round(100 * balances.loc[same_day, "positive_closing_usd"].sum() / balances["positive_closing_usd"].sum(), 2), "% of positive closing USD", "calculation", "Value-weighted sensitivity; not start-of-day"),
        metric("one_day_delayed_observations", balances["reporting_delay_days"].eq(1).sum(), "observations", "calculation"),
        metric("two_or_more_day_delayed_observations", balances["reporting_delay_days"].ge(2).sum(), "observations", "calculation"),
        metric("median_two_plus_day_stale_positive_balance", round(two_plus_day_stale_positive_daily.median(), 2), "USD/day", "calculation", "Positive closing value reported at least two calendar days late; not a loss estimate"),
        metric("minimum_two_plus_day_stale_positive_balance", round(two_plus_day_stale_positive_daily.min(), 2), "USD/day", "calculation", "Positive closing value reported at least two calendar days late; not a loss estimate"),
        metric("maximum_reporting_delay", balances["reporting_delay_days"].max(), "days", "calculation"),
        metric("automated_balance_observations", balances["source_quality"].eq("Automated").sum(), "observations", "daily_balances.csv"),
        metric("manually_reported_balance_observations", balances["source_quality"].eq("Manually reported").sum(), "observations", "daily_balances.csv"),
        metric("estimated_balance_observations", balances["source_quality"].eq("Estimated").sum(), "observations", "daily_balances.csv"),
        metric("latest_closing_balance", round(latest_balances["closing_balance_usd"].sum(), 2), "USD", "calculation", "Ledger balance; not proof of transferability"),
        metric("latest_available_balance", round(latest_balances["available_balance_usd"].sum(), 2), "USD", "calculation", "Net estimated availability after negative positions; requires validation"),
        metric("latest_gross_positive_available_balance", round(latest_positive_available.sum(), 2), "USD", "calculation", "Gross positive estimate before negative positions; requires validation"),
        metric("latest_negative_available_balance", round(latest_balances.loc[latest_balances["available_balance_usd"] < 0, "available_balance_usd"].sum(), 2), "USD", "calculation", "Two negative account positions"),
        metric("latest_positive_available_value_weighted_same_day_rate", round(100 * latest_positive_available[latest_balances_same_day].sum() / latest_positive_available.sum(), 2), "% of positive available USD", "calculation", "30 Jun. sensitivity; not start-of-day"),
        metric("fx_rows", len(fx), "rows", "fx_rates.csv"),
        metric("fx_currencies", fx["currency"].nunique(), "currencies", "fx_rates.csv"),
        metric("fx_dates", fx["date"].nunique(), "calendar days", "fx_rates.csv"),
        metric("expected_fx_rows", expected_fx_rows, "rows", "calculation"),
        metric("payment_rows", len(payments), "rows", "payments.csv"),
        metric("unique_payments", payments["payment_id"].nunique(), "payments", "payments.csv"),
        metric("payment_start_date", payments["payment_date"].min().date().isoformat(), "date", "payments.csv"),
        metric("payment_end_date", payments["payment_date"].max().date().isoformat(), "date", "payments.csv"),
        metric("gross_supplied_payment_value_control_total", round(payment_enriched["amount_usd"].sum(), 2), "USD", "calculation", "Includes every supplied status; not settled value"),
        metric("payment_fee_control_total", round(payments["fee_usd"].sum(), 2), "USD", "payments.csv", "Estimated fees, not actual bank pricing"),
        metric("manual_touch_payments", payments["manual_touch_flag"].sum(), "payments", "payments.csv"),
        metric("manual_touch_rate", round(100 * payments["manual_touch_flag"].mean(), 2), "%", "calculation"),
        metric("exception_payments", payments["exception_flag"].sum(), "payments", "payments.csv"),
        metric("exception_rate", round(100 * payments["exception_flag"].mean(), 2), "%", "calculation"),
        metric("late_release_payments", payments["late_release_flag"].sum(), "payments", "payments.csv"),
        metric("late_release_rate", round(100 * payments["late_release_flag"].mean(), 2), "%", "calculation"),
        metric("rejected_payments", payments["status"].eq("Rejected").sum(), "payments", "payments.csv"),
        metric("pending_payments", payments["status"].eq("Pending").sum(), "payments", "payments.csv", "Status as of extract is not supplied"),
        metric("rejected_payment_value", round(payment_enriched.loc[payment_enriched["status"].eq("Rejected"), "amount_usd"].sum(), 2), "USD", "calculation", "Included in gross supplied value; not settled"),
        metric("pending_payment_value", round(payment_enriched.loc[payment_enriched["status"].eq("Pending"), "amount_usd"].sum(), 2), "USD", "calculation", "Included in gross supplied value; settlement unknown"),
        metric("repair_minutes", payments["repair_minutes"].sum(), "minutes", "payments.csv", "Management-estimated effort"),
        metric("manual_payment_exception_share", round(100 * payments.loc[manual_payments, "exception_flag"].sum() / payments["exception_flag"].sum(), 2), "% of exceptions", "calculation", "Association within supplied records; not causal attribution"),
        metric("manual_payment_repair_share", round(100 * payments.loc[manual_payments, "repair_minutes"].sum() / payments["repair_minutes"].sum(), 2), "% of repair minutes", "calculation", "Association within supplied records; not causal attribution"),
        metric("manual_local_wire_ach_repair_share", round(100 * payments.loc[manual_payments & manual_core_payment_types, "repair_minutes"].sum() / payments["repair_minutes"].sum(), 2), "% of repair minutes", "calculation", "Manual local transfer, wire, and ACH cohorts combined"),
        metric("cross_border_wire_payment_share", round(100 * cross_border_wires.mean(), 2), "% of payments", "calculation", "Within supplied records; population representativeness unproven"),
        metric("cross_border_wire_exception_rate", round(100 * payments.loc[cross_border_wires, "exception_flag"].mean(), 2), "%", "calculation", "Within supplied records; reason codes absent"),
        metric("cross_border_wire_late_release_rate", round(100 * payments.loc[cross_border_wires, "late_release_flag"].mean(), 2), "%", "calculation", "Within supplied records; cutoff timestamps absent"),
        metric("cross_border_wire_repair_share", round(100 * payments.loc[cross_border_wires, "repair_minutes"].sum() / payments["repair_minutes"].sum(), 2), "% of repair minutes", "calculation", "Within supplied records; repair time is management-estimated"),
        metric("payment_file_exception_volume_monthly", round(payments["exception_flag"].sum() / 6, 2), "payments/month", "calculation", "Six-month supplied payment file"),
        metric("payment_file_repair_hours_monthly", round(payments["repair_minutes"].sum() / 60 / 6, 2), "hours/month", "calculation", "Six-month supplied payment file"),
        metric("process_file_exception_volume_monthly", payment_exception_process["frequency_per_month"], "instances/month", "process_activity.csv", "Management estimate; scope differs from payment file"),
        metric("process_file_exception_manual_hours_monthly", round(payment_exception_process["frequency_per_month"] * payment_exception_process["minutes_per_instance"] * payment_exception_process["manual_percentage"] / 100 / 60, 2), "hours/month", "calculation", "Management estimate; scope differs from payment file"),
        metric("payment_extract_external_control_status", "Not provided", "status", "project package", "Representativeness cannot be established"),
        metric("process_rows", len(process), "activities", "process_activity.csv"),
        metric("estimated_manual_process_hours_monthly", round(process_manual_hours_monthly.sum(), 2), "hours/month", "calculation", "Management estimates; not time-and-motion evidence"),
        metric("high_control_criticality_processes", high_control_processes.sum(), "activities", "process_activity.csv", "Control-critical does not mean the current manual method must remain"),
        metric("high_control_manual_hours_monthly", round(process_manual_hours_monthly.loc[high_control_processes].sum(), 2), "hours/month", "calculation", "Management estimates; controls must be preserved or replaced"),
        metric("illustrative_15pct_capacity_redeployment", round(process_manual_hours_monthly.sum() * 12 * 0.15, 2), "hours/year", "calculation", "Sensitivity only; not headcount or cashable savings"),
        metric("illustrative_20pct_capacity_redeployment", round(process_manual_hours_monthly.sum() * 12 * 0.20, 2), "hours/year", "calculation", "Sensitivity only; not headcount or cashable savings"),
    ]

    missing_rows = []
    for dataset_name, frame in data.items():
        for column in frame.columns:
            missing = missing_mask(frame[column])
            missing_rows.append({
                "dataset": dataset_name,
                "column": column,
                "missing_count": int(missing.sum()),
                "missing_rate_pct": round(100 * missing.mean(), 4),
            })

    balance_dates = pd.DatetimeIndex(sorted(balances["date"].unique()))
    expected_dates = pd.date_range(balance_dates.min(), balance_dates.max(), freq="D")
    payment_flag_columns = [
        "cross_border_flag",
        "manual_touch_flag",
        "exception_flag",
        "late_release_flag",
    ]
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
        ("all_required_fields_complete", all(not missing_mask(frame[column]).any() for frame in data.values() for column in frame.columns)),
        ("entity_region_domain_valid", entities["region"].isin({"NA", "EMEA", "APAC"}).all()),
        ("account_status_domain_valid", accounts["status"].isin({"Active", "Dormant"}).all()),
        ("visibility_method_domain_valid", accounts["visibility_method"].isin({"API", "Host-to-host", "Portal", "Spreadsheet"}).all()),
        ("balance_source_quality_domain_valid", balances["source_quality"].isin({"Automated", "Manually reported", "Estimated"}).all()),
        ("payment_status_domain_valid", payments["status"].isin({"Completed", "Repaired", "Rejected", "Pending"}).all()),
        ("restricted_flag_is_boolean", pd.api.types.is_bool_dtype(accounts["restricted_flag"])),
        ("payment_flags_are_boolean", all(pd.api.types.is_bool_dtype(payments[column]) for column in payment_flag_columns)),
        ("fx_rates_positive", fx["usd_per_unit"].gt(0).all()),
        ("payment_amounts_positive", payments["amount_local"].gt(0).all()),
        ("payment_fees_nonnegative", payments["fee_usd"].ge(0).all()),
        ("account_fees_nonnegative", accounts["annual_fee_usd"].ge(0).all()),
        ("balance_date_range_contiguous", balance_dates.equals(expected_dates)),
        ("fx_dates_match_balance_dates", pd.DatetimeIndex(sorted(fx["date"].unique())).equals(balance_dates)),
        ("process_numeric_inputs_nonnegative", process[["frequency_per_month", "minutes_per_instance", "loaded_hourly_cost_usd"]].ge(0).all().all()),
        ("process_manual_percentage_in_range", process["manual_percentage"].between(0, 100).all()),
        ("entity_schema_exact", list(entities.columns) == expected_schemas["entities"]),
        ("account_schema_exact", list(accounts.columns) == expected_schemas["accounts"]),
        ("balance_schema_exact", list(data["balances"].columns) == expected_schemas["balances"]),
        ("payment_schema_exact", list(payments.columns) == expected_schemas["payments"]),
        ("fx_schema_exact", list(fx.columns) == expected_schemas["fx"]),
        ("process_schema_exact", list(process.columns) == expected_schemas["process"]),
        ("balance_period_matches_project", balances["date"].min() == pd.Timestamp("2026-01-01") and balances["date"].max() == pd.Timestamp("2026-06-30")),
        ("fx_period_matches_project", fx["date"].min() == pd.Timestamp("2026-01-01") and fx["date"].max() == pd.Timestamp("2026-06-30")),
        ("visibility_source_quality_mapping_valid", balances["source_quality"].eq(balances["visibility_method"].map({"API": "Automated", "Host-to-host": "Automated", "Portal": "Manually reported", "Spreadsheet": "Estimated"})).all()),
        ("repaired_payments_are_exceptions", payments.loc[payments["status"].eq("Repaired"), "exception_flag"].all()),
        ("rejected_payments_are_exceptions", payments.loc[payments["status"].eq("Rejected"), "exception_flag"].all()),
        ("completed_payments_are_not_exceptions", (~payments.loc[payments["status"].eq("Completed"), "exception_flag"]).all()),
        ("exception_payments_have_repair_minutes", payments.loc[payments["exception_flag"], "repair_minutes"].gt(0).all()),
        ("account_purpose_domain_valid", accounts["purpose"].isin({"Operating", "Collection", "Payroll", "Tax", "Legacy"}).all()),
        ("sweep_structure_domain_valid", accounts["sweep_structure"].isin({"None", "Domestic sweep", "Regional pool"}).all()),
        ("entity_restriction_domain_valid", entities["cash_restriction_level"].isin({"Low", "Medium", "High"}).all()),
        ("payment_type_domain_valid", payments["payment_type"].isin({"Local transfer", "ACH", "Wire", "Payroll", "Tax", "Internal transfer"}).all()),
        ("process_control_criticality_domain_valid", process["control_criticality"].isin({"Low", "Medium", "High"}).all()),
        ("payment_dates_have_fx_coverage", payment_enriched["payment_date"].between(fx["date"].min(), fx["date"].max()).all()),
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
