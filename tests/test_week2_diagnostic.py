"""Executable reconciliation tests for the Week 2 diagnostic layer."""

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from starter_analysis import enrich_balances, load_data, validate_keys  # noqa: E402
from week2_diagnostic import (  # noqa: E402
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
    }
    failed = [name for name, passed in checks.items() if not passed]
    for name, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'} — {name}")
    if failed:
        raise SystemExit(f"Week 2 diagnostic test failures: {failed}")
    print(f"All {len(checks)} Week 2 diagnostic tests passed.")


if __name__ == "__main__":
    main()
