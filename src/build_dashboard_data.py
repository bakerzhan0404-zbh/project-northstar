"""Build the fail-closed data contract for the interactive dashboard.

The dashboard reads only the reconciled Week 1 and Week 2 analytical outputs.
This adapter deliberately fails before producing JSON if a control total,
required evidence boundary, or cohort reconciliation changes.  In particular,
validated movable cash is represented as ``None``/``not_established``; the
separate zero-dollar value is the current *funded case*, not an observed cash
balance.
"""

from __future__ import annotations

import json
import math
import os
import tempfile
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Dict, Mapping

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUT = ROOT / "dashboard" / "dashboard_data.json"

INPUT_FILES = {
    "w1_checks": "W1_data_quality_checks.csv",
    "w1_metrics": "W1_data_quality_metrics.csv",
    "w2_reconciliation": "W2_reconciliation_metrics.csv",
    "visibility": "W2_visibility_diagnostic.csv",
    "liquidity_scenarios": "W2_liquidity_scenarios.csv",
    "liquidity_thresholds": "W2_liquidity_thresholds.csv",
    "payments": "W2_payment_diagnostic.csv",
    "process_capacity": "W2_process_capacity.csv",
    "repair_baseline": "W2_repair_baseline_reconciliation.csv",
    "accounts": "W2_account_diagnostic.csv",
}

VISIBILITY_BOUNDARY = (
    "Calendar-date proxy; not start-of-day or elapsed-24-hour visibility"
)
PAYMENT_BOUNDARY = (
    "Within supplied 7,600 records only; association does not establish cause "
    "or ACG-wide performance"
)
LIQUIDITY_THRESHOLD_BOUNDARY = (
    "Scenario screen only; no threshold is validated movable cash"
)
CAPACITY_BOUNDARY = (
    "Management-estimated capacity; not observed labor, headcount, or cashable "
    "savings"
)
REPAIR_BOUNDARY = (
    "Source scope and removability are unresolved; no combined capacity or P&L "
    "baseline"
)
CLOSURE_BOUNDARY = (
    "Local purpose, dependencies, signatories, service continuity, closure cost, "
    "and fee removal are not validated"
)


class DashboardDataError(ValueError):
    """Raised when the dashboard evidence contract cannot be certified."""


def load_dashboard_inputs(
    processed_dir: Path = PROCESSED,
) -> Dict[str, pd.DataFrame]:
    """Load the canonical processed CSVs without mutating or writing anything."""
    frames: Dict[str, pd.DataFrame] = {}
    missing = []
    for key, filename in INPUT_FILES.items():
        path = processed_dir / filename
        if not path.is_file():
            missing.append(str(path))
            continue
        frames[key] = pd.read_csv(path)
    if missing:
        raise DashboardDataError(
            "Missing canonical dashboard input(s): " + ", ".join(missing)
        )
    return frames


def _require_columns(
    frame: pd.DataFrame, required: set[str], source: str
) -> None:
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise DashboardDataError(
            f"{source} is missing required column(s): {', '.join(missing)}"
        )


def _one_row(frame: pd.DataFrame, source: str, **criteria: Any) -> pd.Series:
    mask = pd.Series(True, index=frame.index)
    for column, expected in criteria.items():
        if column not in frame.columns:
            raise DashboardDataError(f"{source} is missing required column: {column}")
        mask &= frame[column].eq(expected)
    matches = frame.loc[mask]
    if len(matches) != 1:
        label = ", ".join(f"{key}={value!r}" for key, value in criteria.items())
        raise DashboardDataError(
            f"Expected exactly one {source} row for {label}; found {len(matches)}"
        )
    return matches.iloc[0]


def _decimal(value: Any, label: str) -> Decimal:
    if pd.isna(value) or isinstance(value, bool):
        raise DashboardDataError(f"{label} must be numeric; found {value!r}")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise DashboardDataError(
            f"{label} must be numeric; found {value!r}"
        ) from exc
    if not result.is_finite():
        raise DashboardDataError(f"{label} must be finite; found {value!r}")
    return result


def _expect_number(actual: Any, expected: Any, label: str) -> None:
    if _decimal(actual, label) != Decimal(str(expected)):
        raise DashboardDataError(
            f"{label} changed: expected {expected!r}, found {actual!r}"
        )


def _expect_text(actual: Any, expected: str, label: str) -> None:
    if pd.isna(actual) or str(actual) != expected:
        raise DashboardDataError(
            f"{label} changed: expected {expected!r}, found {actual!r}"
        )


def _as_int(value: Any, label: str) -> int:
    number = _decimal(value, label)
    if number != number.to_integral_value():
        raise DashboardDataError(f"{label} must be an integer; found {value!r}")
    return int(number)


def _as_float(value: Any, label: str) -> float:
    result = float(_decimal(value, label))
    if not math.isfinite(result):
        raise DashboardDataError(f"{label} must be finite; found {value!r}")
    return result


def _metric_row(frame: pd.DataFrame, source: str, metric: str) -> pd.Series:
    return _one_row(frame, source, metric=metric)


def _validate_w1(frames: Mapping[str, pd.DataFrame]) -> None:
    checks = frames["w1_checks"]
    _require_columns(checks, {"check", "passed"}, INPUT_FILES["w1_checks"])
    if checks["check"].duplicated().any() or checks.empty:
        raise DashboardDataError("Week 1 data-quality checks must be non-empty and unique")
    passed = checks["passed"].astype(str).str.lower().map(
        {"true": True, "false": False}
    )
    if passed.isna().any() or not passed.all():
        failed = checks.loc[passed.ne(True), "check"].astype(str).tolist()
        raise DashboardDataError(
            "Week 1 data-quality checks are not all passing: " + ", ".join(failed)
        )

    metrics = frames["w1_metrics"]
    _require_columns(
        metrics, {"metric", "value", "unit", "source", "note"},
        INPUT_FILES["w1_metrics"],
    )
    if metrics["metric"].duplicated().any():
        raise DashboardDataError("Week 1 metrics contain duplicate metric names")
    expected = {
        "entity_rows": 16,
        "revenue_control_total": 3900,
        "account_rows": 55,
        "annual_account_fee_control_total": 110100,
        "dormant_zero_payment_legacy_candidates": 4,
        "dormant_zero_payment_legacy_candidate_fees": 7800,
        "balance_rows": 9955,
        "balance_dates": 181,
        "same_day_visibility_accounts": 32,
        "same_day_visibility_observations": 5792,
        "same_day_visibility_rate": 58.18,
        "within_one_day_visibility_rate": 74.55,
        "payment_rows": 7600,
        "gross_supplied_payment_value_control_total": 198135489.5,
        "repair_minutes": 20080,
        "process_rows": 9,
        "estimated_manual_process_hours_monthly": 617.72,
    }
    for metric, value in expected.items():
        row = _metric_row(metrics, INPUT_FILES["w1_metrics"], metric)
        _expect_number(row["value"], value, f"Week 1 metric {metric}")
    for metric, value in {
        "balance_start_date": "2026-01-01",
        "balance_end_date": "2026-06-30",
        "payment_start_date": "2026-01-01",
        "payment_end_date": "2026-06-30",
        "payment_extract_external_control_status": "Not provided",
    }.items():
        row = _metric_row(metrics, INPUT_FILES["w1_metrics"], metric)
        _expect_text(row["value"], value, f"Week 1 metric {metric}")


def _validate_reconciliation(frames: Mapping[str, pd.DataFrame]) -> None:
    frame = frames["w2_reconciliation"]
    _require_columns(
        frame, {"metric", "value", "unit", "evidence_label"},
        INPUT_FILES["w2_reconciliation"],
    )
    if frame["metric"].duplicated().any() or len(frame) != 13:
        raise DashboardDataError(
            "Week 2 reconciliation must contain exactly 13 unique controls"
        )
    expected = {
        "entities": 16,
        "supplied_revenue": 3900,
        "accounts": 55,
        "estimated_annual_account_fees": 110100,
        "balance_observations": 9955,
        "balance_dates": 181,
        "payment_records": 7600,
        "gross_supplied_payment_value": 198135489.5,
        "payment_repair_minutes": 20080,
        "fx_rows": 1810,
        "fx_currencies": 10,
        "process_activities": 9,
        "estimated_manual_process_hours_monthly": 617.72,
    }
    for metric, value in expected.items():
        row = _metric_row(frame, INPUT_FILES["w2_reconciliation"], metric)
        _expect_number(row["value"], value, f"Week 2 control {metric}")


def _validate_visibility(frames: Mapping[str, pd.DataFrame]) -> None:
    frame = frames["visibility"]
    required = {
        "dimension", "category", "observations", "accounts",
        "same_day_observations", "same_day_rate_pct",
        "within_one_day_observations", "within_one_day_rate_pct",
        "one_day_delayed_observations", "two_plus_day_delayed_observations",
        "maximum_delay_days", "evidence_label", "decision_boundary",
    }
    _require_columns(frame, required, INPUT_FILES["visibility"])
    rows = {
        "overall": _one_row(
            frame, INPUT_FILES["visibility"],
            dimension="overall", category="All supplied account-days",
        ),
        **{
            method: _one_row(
                frame, INPUT_FILES["visibility"],
                dimension="visibility_method", category=method,
            )
            for method in ("API", "Host-to-host", "Portal", "Spreadsheet")
        },
    }
    expected = {
        "overall": (9955, 55, 5792, 58.18, 7421, 74.55, 1629, 2534, 3),
        "API": (2172, 12, 2172, 100, 2172, 100, 0, 0, 0),
        "Host-to-host": (3620, 20, 3620, 100, 3620, 100, 0, 0, 0),
        "Portal": (1629, 9, 0, 0, 1629, 100, 1629, 0, 1),
        "Spreadsheet": (2534, 14, 0, 0, 0, 0, 0, 2534, 3),
    }
    fields = (
        "observations", "accounts", "same_day_observations",
        "same_day_rate_pct", "within_one_day_observations",
        "within_one_day_rate_pct", "one_day_delayed_observations",
        "two_plus_day_delayed_observations", "maximum_delay_days",
    )
    for name, row in rows.items():
        for field, value in zip(fields, expected[name]):
            _expect_number(row[field], value, f"visibility {name} {field}")
        _expect_text(
            row["evidence_label"], "ANALYST-CALC",
            f"visibility {name} evidence label",
        )
        _expect_text(
            row["decision_boundary"], VISIBILITY_BOUNDARY,
            f"visibility {name} boundary",
        )


def _validate_liquidity(frames: Mapping[str, pd.DataFrame]) -> None:
    scenarios = frames["liquidity_scenarios"]
    _require_columns(
        scenarios,
        {"scenario_date", "metric", "value_usd", "liquidity_layer",
         "interpretation", "evidence_label"},
        INPUT_FILES["liquidity_scenarios"],
    )
    if scenarios["metric"].duplicated().any():
        raise DashboardDataError("Liquidity scenarios contain duplicate metrics")
    expected_values = {
        "net_estimated_available_balance": 55662922.37,
        "gross_positive_estimated_available_balance": 57801215.46,
        "preliminarily_restricted_positive_available_balance": 8053700.97,
        "preliminarily_unflagged_positive_available_balance": 49747514.49,
        "apparent_net_after_preliminary_restriction_before_buffer": 47609221.4,
        "unflagged_supplied_payment_buffer_7d": 5485896.33,
        "unflagged_scenario_surplus_after_7d_buffer": 44983080.88,
        "net_scenario_surplus_after_7d_buffer": 42844787.78,
        "unflagged_supplied_payment_buffer_14d": 10828186.91,
        "unflagged_scenario_surplus_after_14d_buffer": 40265783.82,
        "net_scenario_surplus_after_14d_buffer": 38127490.73,
    }
    for metric, value in expected_values.items():
        row = _metric_row(scenarios, INPUT_FILES["liquidity_scenarios"], metric)
        _expect_number(row["value_usd"], value, f"liquidity metric {metric}")
        _expect_text(row["scenario_date"], "2026-06-30", f"{metric} date")

    expected_layers = {
        "net_estimated_available_balance": (
            "Estimated layer",
            "Includes negative positions; not validated movable cash",
            "ANALYST-CALC",
        ),
        "gross_positive_estimated_available_balance": (
            "Estimated layer",
            "Before negative positions, restrictions, and buffers",
            "ANALYST-CALC",
        ),
        "preliminarily_restricted_positive_available_balance": (
            "Restriction screen",
            "Preliminary flag only; requires account-level certification",
            "ANALYST-CALC",
        ),
        "preliminarily_unflagged_positive_available_balance": (
            "Restriction screen",
            "Unflagged does not mean movable",
            "ANALYST-CALC",
        ),
        "apparent_net_after_preliminary_restriction_before_buffer": (
            "Restriction screen after netting",
            "Before an operating buffer; not validated movable cash",
            "ANALYST-CALC",
        ),
    }
    for metric, (layer, interpretation, evidence_label) in expected_layers.items():
        row = _metric_row(scenarios, INPUT_FILES["liquidity_scenarios"], metric)
        _expect_text(row["liquidity_layer"], layer, f"{metric} layer")
        _expect_text(
            row["interpretation"], interpretation, f"{metric} interpretation"
        )
        _expect_text(
            row["evidence_label"], evidence_label, f"{metric} evidence label"
        )

    layer_values = {
        metric: _decimal(
            _metric_row(scenarios, INPUT_FILES["liquidity_scenarios"], metric)[
                "value_usd"
            ],
            f"liquidity ladder {metric}",
        )
        for metric in expected_layers
    }
    gross = layer_values["gross_positive_estimated_available_balance"]
    restrictions = layer_values[
        "preliminarily_restricted_positive_available_balance"
    ]
    unflagged = layer_values[
        "preliminarily_unflagged_positive_available_balance"
    ]
    net_estimated = layer_values["net_estimated_available_balance"]
    apparent_net = layer_values[
        "apparent_net_after_preliminary_restriction_before_buffer"
    ]
    if gross - restrictions != unflagged:
        raise DashboardDataError("Liquidity restriction ladder does not reconcile")
    negative_from_estimated_layer = net_estimated - gross
    negative_from_restriction_layer = apparent_net - unflagged
    _expect_number(
        negative_from_estimated_layer, -2138293.09,
        "liquidity negative positions",
    )
    if negative_from_estimated_layer != negative_from_restriction_layer:
        raise DashboardDataError("Liquidity negative-position ladder does not reconcile")

    validated = _metric_row(
        scenarios, INPUT_FILES["liquidity_scenarios"], "validated_movable_cash"
    )
    if not pd.isna(validated["value_usd"]):
        raise DashboardDataError(
            "validated movable cash must be null/not established, never numeric"
        )
    _expect_text(validated["scenario_date"], "2026-06-30", "mobility date")
    _expect_text(validated["liquidity_layer"], "Validated value", "mobility layer")
    _expect_text(
        validated["interpretation"], "Not established by supplied data",
        "mobility interpretation",
    )
    _expect_text(
        validated["evidence_label"], "NOT ESTABLISHED", "mobility evidence label"
    )

    thresholds = frames["liquidity_thresholds"]
    _require_columns(
        thresholds,
        {"buffer_window_days", "threshold_name", "threshold_usd",
         "complete_window_days", "days_threshold_met",
         "threshold_met_rate_pct", "minimum_net_scenario_surplus_usd",
         "median_net_scenario_surplus_usd", "evidence_label",
         "decision_boundary"},
        INPUT_FILES["liquidity_thresholds"],
    )
    if len(thresholds) != 6 or thresholds.duplicated(
        ["buffer_window_days", "threshold_name"]
    ).any():
        raise DashboardDataError(
            "Liquidity thresholds must contain six unique 7/14-day scenario rows"
        )
    expected_thresholds = {
        (7, "stress"): (21000000, 175, 175, 100, 37901838.94, 41951646.43),
        (7, "base"): (35000000, 175, 175, 100, 37901838.94, 41951646.43),
        (7, "upside"): (46200000, 175, 0, 0, 37901838.94, 41951646.43),
        (14, "stress"): (21000000, 168, 168, 100, 31277959.18, 36667187.11),
        (14, "base"): (35000000, 168, 138, 82.14, 31277959.18, 36667187.11),
        (14, "upside"): (46200000, 168, 0, 0, 31277959.18, 36667187.11),
    }
    fields = (
        "threshold_usd", "complete_window_days", "days_threshold_met",
        "threshold_met_rate_pct", "minimum_net_scenario_surplus_usd",
        "median_net_scenario_surplus_usd",
    )
    for (days, name), values in expected_thresholds.items():
        row = _one_row(
            thresholds, INPUT_FILES["liquidity_thresholds"],
            buffer_window_days=days, threshold_name=name,
        )
        for field, value in zip(fields, values):
            _expect_number(row[field], value, f"{days}-day {name} {field}")
        _expect_text(
            row["evidence_label"], "ANALYST-CALC / ANALYST-ASSUMPTION",
            f"{days}-day {name} evidence label",
        )
        _expect_text(
            row["decision_boundary"], LIQUIDITY_THRESHOLD_BOUNDARY,
            f"{days}-day {name} boundary",
        )


def _validate_payments(frames: Mapping[str, pd.DataFrame]) -> None:
    frame = frames["payments"]
    required = {
        "dimension", "category", "records", "record_share_of_extract_pct",
        "exception_records", "exception_rate_pct", "exception_contribution_pct",
        "repair_minutes", "repair_contribution_pct", "evidence_label",
        "decision_boundary",
    }
    _require_columns(frame, required, INPUT_FILES["payments"])
    overall = _one_row(
        frame, INPUT_FILES["payments"],
        dimension="overall", category="All supplied payment records",
    )
    cohort_expected = {
        "Manual touch only": (2053, 27.01, 246, 11.98, 51.36, 10018, 49.89),
        "Manual touch + cross-border wire": (
            342, 4.50, 58, 16.96, 12.11, 2702, 13.46
        ),
        "Cross-border wire only": (444, 5.84, 52, 11.71, 10.86, 2219, 11.05),
        "Neither priority cohort": (4761, 62.64, 123, 2.58, 25.68, 5141, 25.60),
    }
    union = _one_row(
        frame, INPUT_FILES["payments"], dimension="priority_union",
        category="Manual touch or cross-border wire",
    )
    expected_rows = {"overall": (7600, 100, 479, 6.30, 100, 20080, 100)}
    expected_rows.update(cohort_expected)
    expected_rows["priority union"] = (2839, 37.36, 356, 12.54, 74.32, 14939, 74.40)
    rows = {"overall": overall, "priority union": union}
    rows.update(
        {
            name: _one_row(
                frame, INPUT_FILES["payments"],
                dimension="priority_payment_cohort", category=name,
            )
            for name in cohort_expected
        }
    )
    fields = (
        "records", "record_share_of_extract_pct", "exception_records",
        "exception_rate_pct", "exception_contribution_pct", "repair_minutes",
        "repair_contribution_pct",
    )
    for name, row in rows.items():
        for field, value in zip(fields, expected_rows[name]):
            _expect_number(row[field], value, f"payments {name} {field}")
        _expect_text(
            row["evidence_label"], "ANALYST-CALC",
            f"payments {name} evidence label",
        )
        _expect_text(
            row["decision_boundary"], PAYMENT_BOUNDARY,
            f"payments {name} boundary",
        )
    cohort_rows = [rows[name] for name in cohort_expected]
    for field, total in (
        ("records", 7600), ("exception_records", 479),
        ("repair_minutes", 20080),
    ):
        actual = sum(_decimal(row[field], f"cohort {field}") for row in cohort_rows)
        _expect_number(actual, total, f"deduplicated cohort {field} reconciliation")


def _validate_guardrails(frames: Mapping[str, pd.DataFrame]) -> None:
    capacity = frames["process_capacity"]
    _require_columns(
        capacity,
        {"process", "manual_hours_monthly", "evidence_label", "decision_boundary"},
        INPUT_FILES["process_capacity"],
    )
    if len(capacity) != 9 or capacity["process"].duplicated().any():
        raise DashboardDataError("Process capacity must contain nine unique activities")
    for _, row in capacity.iterrows():
        _expect_text(row["evidence_label"], "ANALYST-CALC", "capacity evidence label")
        _expect_text(row["decision_boundary"], CAPACITY_BOUNDARY, "capacity boundary")
    exception_process = _one_row(
        capacity, INPUT_FILES["process_capacity"], process="Payment exception repair"
    )
    _expect_number(
        exception_process["manual_hours_monthly"], 102.6,
        "process-file exception repair hours",
    )

    repair = frames["repair_baseline"]
    _require_columns(
        repair,
        {"metric", "value", "unit", "definition", "evidence_label",
         "decision_boundary"},
        INPUT_FILES["repair_baseline"],
    )
    if repair["metric"].duplicated().any() or len(repair) != 10:
        raise DashboardDataError("Repair baseline must contain ten unique metrics")
    repair_expected = {
        "payment_file_repair_hours_monthly": 55.7778,
        "process_file_exception_manual_hours_monthly": 102.6,
        "repair_hour_difference_monthly": 46.8222,
        "process_to_payment_repair_hour_ratio": 1.8394,
    }
    for metric, value in repair_expected.items():
        row = _metric_row(repair, INPUT_FILES["repair_baseline"], metric)
        _expect_number(row["value"], value, f"repair baseline {metric}")
        _expect_text(
            row["evidence_label"], "ANALYST-CALC / ANALYST-ASSUMPTION",
            f"repair baseline {metric} evidence label",
        )
        _expect_text(
            row["decision_boundary"], REPAIR_BOUNDARY,
            f"repair baseline {metric} boundary",
        )

    accounts = frames["accounts"]
    _require_columns(
        accounts,
        {"account_id", "annual_fee_usd", "supplied_payment_records",
         "closure_validation_candidate", "candidate_reason", "evidence_label",
         "decision_boundary"},
        INPUT_FILES["accounts"],
    )
    if len(accounts) != 55 or accounts["account_id"].duplicated().any():
        raise DashboardDataError("Account diagnostic must contain 55 unique accounts")
    candidate_flag = accounts["closure_validation_candidate"]
    if candidate_flag.dtype != bool:
        candidate_flag = candidate_flag.astype(str).str.lower().map(
            {"true": True, "false": False}
        )
    if candidate_flag.isna().any():
        raise DashboardDataError("Closure candidate flag must be boolean")
    candidates = accounts.loc[candidate_flag]
    if len(candidates) != 4:
        raise DashboardDataError(
            f"Closure-validation candidate count changed: expected 4, found {len(candidates)}"
        )
    _expect_number(
        candidates["annual_fee_usd"].sum(), 7800,
        "closure-validation candidate fees",
    )
    if not candidates["supplied_payment_records"].eq(0).all():
        raise DashboardDataError(
            "Every closure-validation candidate must have zero supplied payment records"
        )
    for _, row in candidates.iterrows():
        _expect_text(
            row["candidate_reason"],
            "Dormant + legacy purpose + zero supplied payment records",
            f"candidate {row['account_id']} reason",
        )
        _expect_text(
            row["evidence_label"], "ANALYST-CALC",
            f"candidate {row['account_id']} evidence label",
        )
        _expect_text(
            row["decision_boundary"], CLOSURE_BOUNDARY,
            f"candidate {row['account_id']} boundary",
        )


def validate_dashboard_inputs(frames: Mapping[str, pd.DataFrame]) -> None:
    """Certify controls and boundaries; raise before any dashboard is built."""
    missing = sorted(set(INPUT_FILES).difference(frames))
    if missing:
        raise DashboardDataError(
            "Missing loaded dashboard input(s): " + ", ".join(missing)
        )
    _validate_w1(frames)
    _validate_reconciliation(frames)
    _validate_visibility(frames)
    _validate_liquidity(frames)
    _validate_payments(frames)
    _validate_guardrails(frames)


def _payment_values(row: pd.Series, label: str) -> Dict[str, Any]:
    return {
        "records": _as_int(row["records"], f"{label} records"),
        "record_contribution_pct": _as_float(
            row["record_share_of_extract_pct"], f"{label} record share"
        ),
        "exceptions": _as_int(row["exception_records"], f"{label} exceptions"),
        "exception_rate_pct": _as_float(
            row["exception_rate_pct"], f"{label} exception rate"
        ),
        "exception_contribution_pct": _as_float(
            row["exception_contribution_pct"], f"{label} exception share"
        ),
        "repair_minutes": _as_int(
            row["repair_minutes"], f"{label} repair minutes"
        ),
        "repair_contribution_pct": _as_float(
            row["repair_contribution_pct"], f"{label} repair share"
        ),
    }


def build_dashboard_data(frames: Mapping[str, pd.DataFrame]) -> Dict[str, Any]:
    """Return a deterministic JSON-ready dashboard contract without writing."""
    validate_dashboard_inputs(frames)

    visibility = frames["visibility"]
    visibility_overall = _one_row(
        visibility, INPUT_FILES["visibility"],
        dimension="overall", category="All supplied account-days",
    )
    visibility_sources = []
    for method in ("API", "Host-to-host", "Portal", "Spreadsheet"):
        row = _one_row(
            visibility, INPUT_FILES["visibility"],
            dimension="visibility_method", category=method,
        )
        visibility_sources.append(
            {
                "method": method,
                "accounts": _as_int(row["accounts"], f"{method} accounts"),
                "observations": _as_int(
                    row["observations"], f"{method} observations"
                ),
                "same_day_observations": _as_int(
                    row["same_day_observations"], f"{method} same-day observations"
                ),
                "same_day_rate_pct": _as_float(
                    row["same_day_rate_pct"], f"{method} same-day rate"
                ),
                "within_one_day_observations": _as_int(
                    row["within_one_day_observations"],
                    f"{method} within-one-day observations",
                ),
                "one_day_delayed_observations": _as_int(
                    row["one_day_delayed_observations"],
                    f"{method} one-day observations",
                ),
                "two_plus_day_delayed_observations": _as_int(
                    row["two_plus_day_delayed_observations"],
                    f"{method} two-plus-day observations",
                ),
                "maximum_delay_days": _as_int(
                    row["maximum_delay_days"], f"{method} maximum delay"
                ),
            }
        )

    scenarios = frames["liquidity_scenarios"]
    thresholds = frames["liquidity_thresholds"]
    gross_positive = _metric_row(
        scenarios, INPUT_FILES["liquidity_scenarios"],
        "gross_positive_estimated_available_balance",
    )
    preliminary_restrictions = _metric_row(
        scenarios, INPUT_FILES["liquidity_scenarios"],
        "preliminarily_restricted_positive_available_balance",
    )
    preliminarily_unflagged = _metric_row(
        scenarios, INPUT_FILES["liquidity_scenarios"],
        "preliminarily_unflagged_positive_available_balance",
    )
    apparent_net = _metric_row(
        scenarios, INPUT_FILES["liquidity_scenarios"],
        "apparent_net_after_preliminary_restriction_before_buffer",
    )
    negative_positions_usd = float(
        _decimal(apparent_net["value_usd"], "apparent net before buffer")
        - _decimal(
            preliminarily_unflagged["value_usd"],
            "preliminarily unflagged positive availability",
        )
    )
    liquidity_evidence_ladder = [
        {
            "key": "gross_positive_estimated_availability",
            "label": "Gross positive estimated availability",
            "value_usd": _as_float(
                gross_positive["value_usd"], "gross positive estimated availability"
            ),
            "waterfall_delta_usd": _as_float(
                gross_positive["value_usd"], "gross positive waterfall value"
            ),
            "role": "starting_total",
            "evidence_label": str(gross_positive["evidence_label"]),
            "decision_boundary": str(gross_positive["interpretation"]),
        },
        {
            "key": "preliminary_restrictions",
            "label": "Preliminary restrictions",
            "value_usd": _as_float(
                preliminary_restrictions["value_usd"],
                "preliminary restriction value",
            ),
            "waterfall_delta_usd": -_as_float(
                preliminary_restrictions["value_usd"],
                "preliminary restriction deduction",
            ),
            "role": "deduction",
            "evidence_label": str(preliminary_restrictions["evidence_label"]),
            "decision_boundary": str(preliminary_restrictions["interpretation"]),
        },
        {
            "key": "negative_positions",
            "label": "Negative positions",
            "value_usd": negative_positions_usd,
            "waterfall_delta_usd": negative_positions_usd,
            "role": "deduction",
            "evidence_label": "ANALYST-CALC",
            "decision_boundary": (
                "Derived within the adapter from the reconciled scenario layers; "
                "not proof of transferability"
            ),
        },
        {
            "key": "apparent_net_before_buffer",
            "label": "Apparent net before illustrative buffer",
            "value_usd": _as_float(
                apparent_net["value_usd"], "apparent net before buffer"
            ),
            "waterfall_delta_usd": None,
            "role": "resulting_total",
            "evidence_label": str(apparent_net["evidence_label"]),
            "decision_boundary": str(apparent_net["interpretation"]),
        },
    ]
    liquidity_by_window: Dict[str, Dict[str, Any]] = {}
    for days in (7, 14):
        net_screen = _metric_row(
            scenarios, INPUT_FILES["liquidity_scenarios"],
            f"net_scenario_surplus_after_{days}d_buffer",
        )
        gross_screen = _metric_row(
            scenarios, INPUT_FILES["liquidity_scenarios"],
            f"unflagged_scenario_surplus_after_{days}d_buffer",
        )
        buffer = _metric_row(
            scenarios, INPUT_FILES["liquidity_scenarios"],
            f"unflagged_supplied_payment_buffer_{days}d",
        )
        threshold_rows: Dict[str, Dict[str, Any]] = {}
        for threshold_name in ("stress", "base", "upside"):
            threshold = _one_row(
                thresholds, INPUT_FILES["liquidity_thresholds"],
                buffer_window_days=days, threshold_name=threshold_name,
            )
            threshold_rows[threshold_name] = {
                "threshold_usd": _as_float(
                    threshold["threshold_usd"],
                    f"{days}-day {threshold_name} threshold",
                ),
                "complete_windows": _as_int(
                    threshold["complete_window_days"],
                    f"{days}-day {threshold_name} complete windows",
                ),
                "windows_met": _as_int(
                    threshold["days_threshold_met"],
                    f"{days}-day {threshold_name} windows met",
                ),
                "met_rate_pct": _as_float(
                    threshold["threshold_met_rate_pct"],
                    f"{days}-day {threshold_name} threshold rate",
                ),
                "minimum_screen_usd": _as_float(
                    threshold["minimum_net_scenario_surplus_usd"],
                    f"{days}-day {threshold_name} minimum screen",
                ),
                "median_screen_usd": _as_float(
                    threshold["median_net_scenario_surplus_usd"],
                    f"{days}-day {threshold_name} median screen",
                ),
                "evidence_label": str(threshold["evidence_label"]),
                "decision_boundary": str(threshold["decision_boundary"]),
            }
        liquidity_by_window[str(days)] = {
            "screen_usd": _as_float(
                net_screen["value_usd"], f"{days}-day net screen"
            ),
            "unflagged_screen_usd": _as_float(
                gross_screen["value_usd"], f"{days}-day unflagged screen"
            ),
            "buffer_usd": _as_float(buffer["value_usd"], f"{days}-day buffer"),
            "thresholds": threshold_rows,
        }

    payments = frames["payments"]
    payment_overall = _one_row(
        payments, INPUT_FILES["payments"],
        dimension="overall", category="All supplied payment records",
    )
    union = _one_row(
        payments, INPUT_FILES["payments"], dimension="priority_union",
        category="Manual touch or cross-border wire",
    )
    cohort_names = (
        ("manual_touch_only", "Manual touch only"),
        ("manual_touch_and_cross_border_wire", "Manual touch + cross-border wire"),
        ("cross_border_wire_only", "Cross-border wire only"),
        ("neither_priority_cohort", "Neither priority cohort"),
    )
    cohorts = {}
    for key, category in cohort_names:
        row = _one_row(
            payments, INPUT_FILES["payments"],
            dimension="priority_payment_cohort", category=category,
        )
        cohorts[key] = {"label": category, **_payment_values(row, category)}

    repair = frames["repair_baseline"]
    accounts = frames["accounts"]
    candidate_flag = accounts["closure_validation_candidate"]
    if candidate_flag.dtype != bool:
        candidate_flag = candidate_flag.astype(str).str.lower().map(
            {"true": True, "false": False}
        )
    candidates = accounts.loc[candidate_flag].sort_values("account_id")

    payload: Dict[str, Any] = {
        "schema_version": "1.0",
        "meta": {
            "title": "Project Northstar — Treasury decision dashboard",
            "period_start": "2026-01-01",
            "period_end": "2026-06-30",
            "scope": "Week 1–2 diagnostic snapshot; supplied data, not live operations",
            "status": "reconciled_to_supplied_controls_source_certification_open",
        },
        "decision": {
            "status": "validation_required",
            "headline": "Design and test; do not fund or execute yet.",
            "next_step": (
                "Prioritize delayed reporting sources and payment root causes; "
                "certify mobility before booking value."
            ),
        },
        "visibility": {
            "accounts_total": _as_int(
                visibility_overall["accounts"], "visibility accounts"
            ),
            "same_day_accounts": 32,
            "delayed_accounts": 23,
            "observations": _as_int(
                visibility_overall["observations"], "visibility observations"
            ),
            "same_day_rate_pct": _as_float(
                visibility_overall["same_day_rate_pct"], "visibility same-day rate"
            ),
            "within_one_day_rate_pct": _as_float(
                visibility_overall["within_one_day_rate_pct"],
                "visibility within-one-day rate",
            ),
            "sources": visibility_sources,
            "evidence_label": "ANALYST-CALC",
            "decision_boundary": VISIBILITY_BOUNDARY,
        },
        "liquidity": {
            "default_window_days": 14,
            "evidence_ladder": liquidity_evidence_ladder,
            "validated_mobility": {
                "value_usd": None,
                "status": "not_established",
                "evidence_label": "NOT ESTABLISHED",
                "decision_boundary": "Not established by supplied data",
            },
            "funded_case": {
                "value_usd": 0,
                "display": "$0",
                "status": "not_fundable",
                "reason": "Validated mobility has not been established",
            },
            "scenarios": liquidity_by_window,
            "evidence_label": "ANALYST-CALC / ANALYST-ASSUMPTION",
            "decision_boundary": LIQUIDITY_THRESHOLD_BOUNDARY,
        },
        "payments": {
            "overall": _payment_values(payment_overall, "all supplied payments"),
            "priority_union": {
                "label": "Manual touch or cross-border wire (deduplicated)",
                **_payment_values(union, "priority union"),
            },
            "cohorts": cohorts,
            "evidence_label": "ANALYST-CALC",
            "decision_boundary": PAYMENT_BOUNDARY,
        },
        "guardrails": {
            "capacity": {
                "status": "not_fundable",
                "total_estimated_manual_hours_monthly": 617.72,
                "process_file_exception_repair_hours_monthly": _as_float(
                    _metric_row(
                        repair, INPUT_FILES["repair_baseline"],
                        "process_file_exception_manual_hours_monthly",
                    )["value"],
                    "process exception repair hours",
                ),
                "payment_file_repair_hours_monthly": _as_float(
                    _metric_row(
                        repair, INPUT_FILES["repair_baseline"],
                        "payment_file_repair_hours_monthly",
                    )["value"],
                    "payment-file repair hours",
                ),
                "difference_hours_monthly": _as_float(
                    _metric_row(
                        repair, INPUT_FILES["repair_baseline"],
                        "repair_hour_difference_monthly",
                    )["value"],
                    "repair-hour difference",
                ),
                "process_to_payment_ratio": _as_float(
                    _metric_row(
                        repair, INPUT_FILES["repair_baseline"],
                        "process_to_payment_repair_hour_ratio",
                    )["value"],
                    "repair-hour ratio",
                ),
                "evidence_label": "ANALYST-CALC / ANALYST-ASSUMPTION",
                "decision_boundary": REPAIR_BOUNDARY,
            },
            "closures": {
                "status": "not_fundable",
                "validation_candidates": len(candidates),
                "candidate_account_ids": candidates["account_id"].tolist(),
                "estimated_annual_fees_usd": _as_float(
                    candidates["annual_fee_usd"].sum(), "candidate fees"
                ),
                "approved_closures": 0,
                "funded_case_value_usd": 0,
                "evidence_label": "ANALYST-CALC",
                "decision_boundary": CLOSURE_BOUNDARY,
            },
        },
        "sources": [
            {"file": filename, "role": key}
            for key, filename in INPUT_FILES.items()
        ],
    }
    return payload


def write_dashboard_data(
    payload: Mapping[str, Any], output_path: Path = OUTPUT
) -> Path:
    """Atomically write validated JSON, leaving the previous file on failure."""
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(
        payload, indent=2, sort_keys=True, allow_nan=False
    ) + "\n"
    temporary_name = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_name = temporary.name
            temporary.write(serialized)
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_name, destination)
        temporary_name = None
    finally:
        if temporary_name is not None:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass
    return destination


def main() -> None:
    frames = load_dashboard_inputs()
    payload = build_dashboard_data(frames)
    output = write_dashboard_data(payload)
    print(f"Wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
