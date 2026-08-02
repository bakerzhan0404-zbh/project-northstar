"""Generate deterministic case data for Project Northstar.

The generator produces a coherent analytical case without encoding a recommended
solution.
"""

from pathlib import Path

import numpy as np
import pandas as pd


SEED = 20260730
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"


def build_entities() -> pd.DataFrame:
    rows = [
        ("E001", "Aurelius Group Holdings", "NA", "United States", "USD", 420, "Oracle-E1", "Organic", "Low"),
        ("E002", "Aurelius Home US", "NA", "United States", "USD", 930, "Oracle-E1", "Organic", "Low"),
        ("E003", "Aurelius Wellness US", "NA", "United States", "USD", 510, "Oracle-E1", "Summit-2021", "Low"),
        ("E004", "Aurelius Canada", "NA", "Canada", "CAD", 215, "Oracle-E1", "Organic", "Low"),
        ("E005", "Aurelius UK", "EMEA", "United Kingdom", "GBP", 280, "SAP-S4", "Harbor-2020", "Low"),
        ("E006", "Aurelius Germany", "EMEA", "Germany", "EUR", 315, "SAP-S4", "Organic", "Low"),
        ("E007", "Aurelius France", "EMEA", "France", "EUR", 190, "SAP-S4", "Harbor-2020", "Low"),
        ("E008", "Aurelius Netherlands", "EMEA", "Netherlands", "EUR", 145, "SAP-S4", "Organic", "Low"),
        ("E009", "Aurelius Spain", "EMEA", "Spain", "EUR", 125, "Legacy-D365", "Verde-2023", "Low"),
        ("E010", "Aurelius Singapore", "APAC", "Singapore", "SGD", 155, "SAP-S4", "Organic", "Medium"),
        ("E011", "Aurelius Australia", "APAC", "Australia", "AUD", 195, "SAP-S4", "Organic", "Low"),
        ("E012", "Aurelius Japan", "APAC", "Japan", "JPY", 130, "Legacy-D365", "Kanso-2022", "Medium"),
        ("E013", "Aurelius Korea", "APAC", "South Korea", "KRW", 85, "Legacy-D365", "Kanso-2022", "Medium"),
        ("E014", "Aurelius India", "APAC", "India", "INR", 70, "Legacy-D365", "Organic", "High"),
        ("E015", "Aurelius Hong Kong", "APAC", "Hong Kong", "HKD", 65, "SAP-S4", "Organic", "Medium"),
        ("E016", "Aurelius Global Sourcing", "APAC", "Singapore", "USD", 70, "SAP-S4", "Organic", "Medium"),
    ]
    return pd.DataFrame(rows, columns=[
        "entity_id", "entity_name", "region", "country", "functional_currency",
        "revenue_usd_m", "erp_system", "acquisition_origin", "cash_restriction_level",
    ])


def build_accounts(entities: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    banks = ["Northbridge Bank", "Continental Trust", "Meridian Commercial", "Union Atlantic", "Pacific Crown"]
    purposes = ["Operating", "Collection", "Payroll", "Tax", "Legacy"]
    account_counts = [4, 5, 4, 3, 4, 4, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3]
    rows = []
    account_number = 1
    for entity, count in zip(entities.itertuples(index=False), account_counts):
        for local_index in range(count):
            purpose = purposes[local_index] if local_index < len(purposes) else "Operating"
            if local_index >= 3 and count < 5:
                purpose = rng.choice(["Tax", "Legacy"])
            visibility = rng.choice(
                ["API", "Host-to-host", "Portal", "Spreadsheet"],
                p=[0.16, 0.25, 0.29, 0.30],
            )
            if entity.region == "NA" and rng.random() < 0.45:
                visibility = rng.choice(["API", "Host-to-host"])
            status = "Dormant" if purpose == "Legacy" and rng.random() < 0.65 else "Active"
            sweep = "None"
            if entity.region == "NA" and local_index == 0:
                sweep = "Domestic sweep"
            elif entity.region == "EMEA" and entity.entity_id in {"E005", "E006", "E008"} and local_index == 0:
                sweep = "Regional pool"
            restricted = entity.cash_restriction_level == "High" or purpose in {"Payroll", "Tax"}
            open_year = int(rng.integers(2010, 2025))
            if entity.acquisition_origin != "Organic" and purpose == "Legacy":
                open_year = int(entity.acquisition_origin.split("-")[-1])
            rows.append({
                "account_id": f"AC{account_number:04d}",
                "entity_id": entity.entity_id,
                "bank_name": rng.choice(banks),
                "country": entity.country,
                "currency": entity.functional_currency if rng.random() < 0.82 else "USD",
                "purpose": purpose,
                "open_date": f"{open_year}-{int(rng.integers(1, 13)):02d}-{int(rng.integers(1, 28)):02d}",
                "status": status,
                "visibility_method": visibility,
                "sweep_structure": sweep,
                "annual_fee_usd": int(rng.choice([900, 1200, 1800, 2400, 3600])),
                "restricted_flag": bool(restricted),
            })
            account_number += 1
    return pd.DataFrame(rows)


def build_fx_rates(dates: pd.DatetimeIndex, rng: np.random.Generator) -> pd.DataFrame:
    bases = {"USD": 1.0, "CAD": 0.74, "GBP": 1.27, "EUR": 1.09, "SGD": 0.75,
             "AUD": 0.66, "JPY": 0.0068, "KRW": 0.00074, "INR": 0.012, "HKD": 0.128}
    rows = []
    for currency, base in bases.items():
        shocks = rng.normal(0, 0.0025, len(dates))
        path = base * np.exp(np.cumsum(shocks))
        if currency == "USD":
            path = np.ones(len(dates))
        for date, rate in zip(dates, path):
            rows.append({"date": date.date(), "currency": currency, "usd_per_unit": round(float(rate), 8)})
    return pd.DataFrame(rows)


def build_balances(accounts: pd.DataFrame, dates: pd.DatetimeIndex, rng: np.random.Generator) -> pd.DataFrame:
    purpose_scale = {"Operating": 1_900_000, "Collection": 1_050_000, "Payroll": 420_000,
                     "Tax": 280_000, "Legacy": 55_000}
    deficit_entities = {"E007", "E010"}
    surplus_entities = {"E002", "E003", "E006", "E008", "E011"}
    rows = []
    for account in accounts.itertuples(index=False):
        base = purpose_scale[account.purpose] * float(rng.uniform(0.55, 1.55))
        if account.entity_id in surplus_entities:
            base *= 2.1
        if account.entity_id in deficit_entities and account.purpose == "Operating":
            base = -base * 0.45
        if account.status == "Dormant":
            base = float(rng.uniform(1_000, 28_000))
        phase = float(rng.uniform(0, 2 * np.pi))
        for day_index, date in enumerate(dates):
            weekly = 0.10 * max(abs(base), 50_000) * np.sin((2 * np.pi * day_index / 7) + phase)
            noise = rng.normal(0, 0.08 * max(abs(base), 60_000))
            closing = base + weekly + noise
            if account.status == "Dormant":
                closing = max(0, base + rng.normal(0, 600))
            available = closing
            if closing > 0:
                available = closing * float(rng.uniform(0.88, 0.99))
            delay_base = {"API": 0, "Host-to-host": 0, "Portal": 1, "Spreadsheet": 2}[account.visibility_method]
            delay = delay_base + (1 if account.visibility_method == "Spreadsheet" and rng.random() < 0.22 else 0)
            quality = {
                "API": "Automated", "Host-to-host": "Automated",
                "Portal": "Manually reported", "Spreadsheet": "Estimated",
            }[account.visibility_method]
            rows.append({
                "date": date.date(),
                "account_id": account.account_id,
                "closing_balance_local": round(float(closing), 2),
                "available_balance_local": round(float(available), 2),
                "reported_to_group_date": (date + pd.Timedelta(days=delay)).date(),
                "source_quality": quality,
            })
    return pd.DataFrame(rows)


def build_payments(accounts: pd.DataFrame, dates: pd.DatetimeIndex, rng: np.random.Generator) -> pd.DataFrame:
    active = accounts[accounts["status"] == "Active"].copy()
    weights = active["purpose"].map({"Operating": 5.0, "Collection": 0.7, "Payroll": 1.1, "Tax": 0.35, "Legacy": 0.15}).to_numpy()
    weights = weights / weights.sum()
    business_dates = dates[dates.dayofweek < 5]
    payment_types = ["Local transfer", "ACH", "Wire", "Payroll", "Tax", "Internal transfer"]
    rows = []
    for number in range(1, 7601):
        account = active.iloc[int(rng.choice(len(active), p=weights))]
        payment_date = pd.Timestamp(rng.choice(business_dates))
        payment_type = str(rng.choice(payment_types, p=[0.34, 0.25, 0.18, 0.10, 0.05, 0.08]))
        cross_border = bool(payment_type == "Wire" and rng.random() < 0.58)
        manual_prob = 0.18
        if account["visibility_method"] in {"Portal", "Spreadsheet"}:
            manual_prob += 0.24
        if cross_border:
            manual_prob += 0.13
        manual = bool(rng.random() < manual_prob)
        late_prob = 0.025 + (0.07 if manual else 0) + (0.025 if cross_border else 0)
        late = bool(rng.random() < late_prob)
        exception_prob = 0.018 + (0.10 if manual else 0) + (0.075 if cross_border else 0) + (0.08 if late else 0)
        exception = bool(rng.random() < exception_prob)
        rejected = bool(exception and rng.random() < 0.08)
        pending = bool(not rejected and rng.random() < 0.002)
        status = "Rejected" if rejected else ("Pending" if pending else ("Repaired" if exception else "Completed"))
        amount = float(np.exp(rng.normal(9.35, 1.15)))
        if payment_type in {"Payroll", "Tax"}:
            amount *= 4.2
        repair_minutes = int(rng.integers(12, 75)) if exception else 0
        fee = 1.50 + (18 if payment_type == "Wire" else 0) + (24 if cross_border else 0)
        fee += 15 if exception else 0
        rows.append({
            "payment_id": f"P{number:06d}",
            "payment_date": payment_date.date(),
            "account_id": account["account_id"],
            "payment_type": payment_type,
            "currency": account["currency"],
            "amount_local": round(amount, 2),
            "cross_border_flag": cross_border,
            "manual_touch_flag": manual,
            "exception_flag": exception,
            "late_release_flag": late,
            "repair_minutes": repair_minutes,
            "fee_usd": round(float(fee), 2),
            "status": status,
        })
    return pd.DataFrame(rows).sort_values(["payment_date", "payment_id"])


def build_process_activity() -> pd.DataFrame:
    rows = [
        ("Group Treasury", "Consolidated cash positioning", 22, 190, 82, 78, "High"),
        ("Regional Finance", "Local cash reporting", 220, 24, 76, 61, "Medium"),
        ("Shared Services", "Payment file preparation", 340, 31, 58, 49, "High"),
        ("Shared Services", "Payment exception repair", 180, 36, 95, 49, "High"),
        ("Accounts Receivable", "Receipt reconciliation", 420, 28, 68, 47, "Medium"),
        ("Group Treasury", "Intercompany funding decision", 38, 52, 71, 78, "High"),
        ("Regional Finance", "Cash forecast preparation", 48, 145, 88, 61, "Medium"),
        ("IT Operations", "Bank file support", 32, 64, 45, 84, "High"),
        ("Controllers", "Bank access review", 16, 105, 54, 92, "High"),
    ]
    return pd.DataFrame(rows, columns=[
        "team", "process", "frequency_per_month", "minutes_per_instance",
        "manual_percentage", "loaded_hourly_cost_usd", "control_criticality",
    ])


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    dates = pd.date_range("2026-01-01", "2026-06-30", freq="D")
    entities = build_entities()
    accounts = build_accounts(entities, rng)
    fx_rates = build_fx_rates(dates, rng)
    balances = build_balances(accounts, dates, rng)
    payments = build_payments(accounts, dates, rng)
    process_activity = build_process_activity()

    outputs = {
        "entity_master.csv": entities,
        "bank_accounts.csv": accounts,
        "fx_rates.csv": fx_rates,
        "daily_balances.csv": balances,
        "payments.csv": payments,
        "process_activity.csv": process_activity,
    }
    for filename, frame in outputs.items():
        frame.to_csv(RAW / filename, index=False)
        print(f"Wrote {filename}: {len(frame):,} rows")
    print("All project records were generated successfully and are deterministic.")


if __name__ == "__main__":
    main()
