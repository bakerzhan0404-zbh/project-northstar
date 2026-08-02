"""Lightweight executable checks for the generated Northstar datasets."""

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from starter_analysis import enrich_balances, load_data, validate_keys  # noqa: E402


def main() -> None:
    data = load_data()
    validate_keys(data)
    balances = enrich_balances(data)

    checks = {
        "16 entities supplied": len(data["entities"]) == 16,
        "account footprint is sufficiently complex": 45 <= len(data["accounts"]) <= 60,
        "six months of daily balances": balances["date"].nunique() == 181,
        "payment sample is substantive": len(data["payments"]) >= 7_000,
        "all FX joins succeeded": balances["usd_per_unit"].notna().all(),
        "reporting is never earlier than balance date": (balances["reporting_delay_days"] >= 0).all(),
        "payment repair minutes are nonnegative": (data["payments"]["repair_minutes"] >= 0).all(),
        "exceptions exist for analysis": data["payments"]["exception_flag"].sum() > 0,
        "dormant accounts exist for review": (data["accounts"]["status"] == "Dormant").sum() > 0,
        "restricted accounts exist for review": data["accounts"]["restricted_flag"].sum() > 0,
    }
    failed = [name for name, passed in checks.items() if not passed]
    for name, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'} — {name}")
    if failed:
        raise SystemExit(f"Data-quality test failures: {failed}")
    print(f"All {len(checks)} checks passed.")


if __name__ == "__main__":
    main()

