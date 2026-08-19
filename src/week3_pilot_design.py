"""Deterministic Week 3 pilot-selection model for Project Northstar.

This module turns the two design-only pilot charters into reproducible review
frames.  It does not authorize a pilot, infer root causes, estimate prevalence,
or recognize cash, capacity, P&L, or risk benefits.  Every output is bounded to
the supplied Week 2 extracts and fails closed if their governed anchors drift.
"""

from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
from pandas.testing import assert_frame_equal

from starter_analysis import enrich_balances, load_data, validate_keys
from week2_diagnostic import add_priority_payment_cohorts, enrich_payments


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"

VISIBILITY_RULE_VERSION = "W3-VIS-PILOT-v2 · 2026-08-18"
PAYMENT_RULE_VERSION = "W3-PAY-PILOT-v3 · 2026-08-18"
EVIDENCE_BOUNDARY = (
    "ANALYST-JUDGMENT pilot design only; supplied extracts only; not a "
    "representative sample, root-cause conclusion, execution authorization, "
    "or funded-benefit estimate."
)

VISIBILITY_SELECTION: Dict[str, Tuple[str, ...]] = {
    "Spreadsheet": ("AC0021", "AC0010", "AC0017", "AC0001", "AC0040"),
    "Portal": ("AC0022", "AC0031", "AC0018", "AC0002", "AC0050"),
}

PAYMENT_COHORTS: Tuple[str, ...] = (
    "Manual touch only",
    "Manual touch + cross-border wire",
    "Cross-border wire only",
    "Neither priority cohort",
)

ISSUE_MODE_TARGETS: Dict[str, int] = {
    "Exception/status": 8,
    "Late-only": 7,
}

AMOUNT_BAND_LABELS: Tuple[str, ...] = (
    "≤$10k",
    ">$10k–$25k",
    ">$25k–$50k",
    ">$50k–$100k",
    ">$100k",
)

VISIBILITY_OUTPUT_COLUMNS: Tuple[str, ...] = (
    "selection_order",
    "account_id",
    "entity_id",
    "entity_name",
    "region",
    "country",
    "currency",
    "bank_name",
    "erp_system",
    "visibility_method",
    "purpose",
    "restricted_flag",
    "cash_restriction_level",
    "supplied_account_days",
    "minimum_reporting_delay_days",
    "maximum_reporting_delay_days",
    "average_positive_available_usd",
    "method_average_positive_rank",
    "region_method_average_positive_rank",
    "selection_rule",
    "cohort_treatment",
    "shadow_only_flag",
    "control_review_required",
    "enhanced_control_review_required",
    "readiness_status",
    "selection_rule_version",
    "evidence_label",
    "decision_boundary",
)

PAYMENT_OUTPUT_COLUMNS: Tuple[str, ...] = (
    "sample_order",
    "case_control_pair_id",
    "pair_sequence_within_cohort",
    "sample_role",
    "source_payment_id",
    "paired_source_payment_id",
    "priority_payment_cohort",
    "issue_case_flag",
    "issue_definition_hits",
    "issue_mode",
    "paired_issue_mode",
    "issue_selection_rank",
    "issue_mode_selection_rank",
    "payment_date",
    "month",
    "account_id",
    "entity_id",
    "entity_name",
    "region",
    "country",
    "bank_name",
    "erp_system",
    "purpose",
    "visibility_method",
    "payment_type",
    "currency",
    "amount_local",
    "usd_per_unit",
    "amount_usd",
    "amount_band_usd",
    "amount_band_order",
    "cross_border_flag",
    "cross_border_wire_flag",
    "manual_touch_flag",
    "exception_flag",
    "late_release_flag",
    "repair_minutes",
    "fee_usd",
    "status",
    "payment_type_match",
    "region_match",
    "month_match",
    "amount_band_match",
    "match_deviation_count",
    "match_deviation_detail",
    "amount_band_distance",
    "month_distance",
    "absolute_amount_gap_usd",
    "match_quality",
    "selection_rule_version",
    "sample_purpose",
    "evidence_label",
    "decision_boundary",
)


def _assert(condition: bool, message: str) -> None:
    """Raise a consistent fail-closed exception."""
    if not condition:
        raise AssertionError(message)


def _required_fields_are_nonblank(
    frame: pd.DataFrame, columns: List[str]
) -> bool:
    """Return False for null, empty, or whitespace-only required values."""
    if not set(columns).issubset(frame.columns):
        return False
    return bool(
        frame[columns]
        .notna()
        .all()
        .all()
        and frame[columns]
        .astype(str)
        .apply(lambda column: column.str.strip().ne(""))
        .all()
        .all()
    )


def load_governed_inputs() -> Tuple[Dict[str, pd.DataFrame], pd.DataFrame, pd.DataFrame]:
    """Load and enrich the supplied data using the governed Week 2 functions."""
    data = load_data()
    validate_keys(data)
    balances = enrich_balances(data)
    payments = add_priority_payment_cohorts(enrich_payments(data))
    validate_week2_anchors(data, balances, payments)
    return data, balances, payments


def _stored_metric(path: Path, dimension: str, category: str, column: str) -> float:
    """Read one governed Week 2 diagnostic value and fail on ambiguity."""
    _assert(path.exists(), f"Missing governed Week 2 output: {path}")
    stored = pd.read_csv(path, keep_default_na=False)
    required = {"dimension", "category", column}
    _assert(required.issubset(stored.columns), f"Missing columns in {path.name}")
    row = stored.loc[
        stored["dimension"].eq(dimension) & stored["category"].eq(category)
    ]
    _assert(len(row) == 1, f"Expected one {dimension}/{category} row in {path.name}")
    return float(row.iloc[0][column])


def validate_week2_anchors(
    data: Dict[str, pd.DataFrame],
    balances: pd.DataFrame,
    payments: pd.DataFrame,
) -> Dict[str, float]:
    """Fail closed if the supplied or stored Week 2 control totals drift."""
    same_day = balances["reporting_delay_days"].eq(0)
    delayed_accounts = balances.loc[
        balances["reporting_delay_days"].gt(0), "account_id"
    ].unique()
    delayed_methods = set(
        data["accounts"].loc[
            data["accounts"]["account_id"].isin(delayed_accounts),
            "visibility_method",
        ]
    )
    priority_union = payments.loc[
        payments["priority_union_cohort"].eq(
            "Manual touch or cross-border wire"
        )
    ]

    anchors = {
        "accounts": float(len(data["accounts"])),
        "account_days": float(len(balances)),
        "balance_dates": float(balances["date"].nunique()),
        "same_day_account_days": float(same_day.sum()),
        "delayed_accounts": float(len(delayed_accounts)),
        "payment_records": float(len(payments)),
        "gross_payment_intent_usd": round(float(payments["amount_usd"].sum()), 2),
        "manual_touch_records": float(payments["manual_touch_flag"].sum()),
        "exception_records": float(payments["exception_flag"].sum()),
        "late_release_records": float(payments["late_release_flag"].sum()),
        "rejected_records": float(payments["status"].eq("Rejected").sum()),
        "repair_minutes": float(payments["repair_minutes"].sum()),
        "priority_union_records": float(len(priority_union)),
        "priority_union_exceptions": float(priority_union["exception_flag"].sum()),
        "priority_union_repair_minutes": float(priority_union["repair_minutes"].sum()),
        "priority_union_amount_usd": round(
            float(priority_union["amount_usd"].sum()), 2
        ),
    }
    expected = {
        "accounts": 55.0,
        "account_days": 9_955.0,
        "balance_dates": 181.0,
        "same_day_account_days": 5_792.0,
        "delayed_accounts": 23.0,
        "payment_records": 7_600.0,
        "gross_payment_intent_usd": 198_135_489.50,
        "manual_touch_records": 2_395.0,
        "exception_records": 479.0,
        "late_release_records": 380.0,
        "rejected_records": 54.0,
        "repair_minutes": 20_080.0,
        "priority_union_records": 2_839.0,
        "priority_union_exceptions": 356.0,
        "priority_union_repair_minutes": 14_939.0,
        "priority_union_amount_usd": 66_705_933.64,
    }
    for name, value in expected.items():
        _assert(abs(anchors[name] - value) < 0.01, f"Week 2 anchor drift: {name}")
    _assert(
        delayed_methods == {"Portal", "Spreadsheet"},
        "Delayed accounts are no longer confined to Portal and Spreadsheet",
    )

    reconciliation_path = PROCESSED / "W2_reconciliation_metrics.csv"
    _assert(reconciliation_path.exists(), "Missing W2 reconciliation metrics")
    reconciliation = pd.read_csv(reconciliation_path, keep_default_na=False)
    reconciliation_values = reconciliation.set_index("metric")["value"]
    for metric in [
        "accounts",
        "balance_observations",
        "payment_records",
        "gross_supplied_payment_value",
        "payment_repair_minutes",
    ]:
        _assert(metric in reconciliation_values.index, f"Missing W2 metric: {metric}")
    stored_expected = {
        "accounts": anchors["accounts"],
        "balance_observations": anchors["account_days"],
        "payment_records": anchors["payment_records"],
        "gross_supplied_payment_value": anchors["gross_payment_intent_usd"],
        "payment_repair_minutes": anchors["repair_minutes"],
    }
    for metric, expected_value in stored_expected.items():
        _assert(
            abs(float(reconciliation_values.loc[metric]) - expected_value) < 0.01,
            f"Stored W2 reconciliation drift: {metric}",
        )

    diagnostic_path = PROCESSED / "W2_payment_diagnostic.csv"
    stored_priority = {
        "records": _stored_metric(
            diagnostic_path, "priority_union", "Manual touch or cross-border wire", "records"
        ),
        "exception_records": _stored_metric(
            diagnostic_path,
            "priority_union",
            "Manual touch or cross-border wire",
            "exception_records",
        ),
        "repair_minutes": _stored_metric(
            diagnostic_path,
            "priority_union",
            "Manual touch or cross-border wire",
            "repair_minutes",
        ),
        "gross_supplied_record_value_usd": _stored_metric(
            diagnostic_path,
            "priority_union",
            "Manual touch or cross-border wire",
            "gross_supplied_record_value_usd",
        ),
    }
    _assert(
        stored_priority
        == {
            "records": anchors["priority_union_records"],
            "exception_records": anchors["priority_union_exceptions"],
            "repair_minutes": anchors["priority_union_repair_minutes"],
            "gross_supplied_record_value_usd": anchors[
                "priority_union_amount_usd"
            ],
        },
        "Stored W2 priority-union anchors drift",
    )
    return anchors


def build_visibility_candidates(
    data: Dict[str, pd.DataFrame], balances: pd.DataFrame
) -> pd.DataFrame:
    """Build the locked ten-account, coverage-constrained review cohort."""
    account_profile = balances.groupby("account_id", as_index=False).agg(
        supplied_account_days=("date", "size"),
        minimum_reporting_delay_days=("reporting_delay_days", "min"),
        maximum_reporting_delay_days=("reporting_delay_days", "max"),
        average_positive_available_usd=(
            "available_balance_usd",
            lambda series: series.clip(lower=0).mean(),
        ),
    )
    account_profile = account_profile.merge(
        data["accounts"], on="account_id", how="left", validate="one_to_one"
    ).merge(
        data["entities"][
            [
                "entity_id",
                "entity_name",
                "region",
                "erp_system",
                "cash_restriction_level",
            ]
        ],
        on="entity_id",
        how="left",
        validate="many_to_one",
    )
    _assert(
        account_profile[
            ["entity_name", "region", "erp_system", "cash_restriction_level"]
        ]
        .notna()
        .all()
        .all(),
        "Incomplete account/entity join",
    )
    # Account ID is the explicit stable tiebreak after the governed value rank.
    account_profile = account_profile.sort_values(
        ["visibility_method", "average_positive_available_usd", "account_id"],
        ascending=[True, False, True],
        kind="mergesort",
    )
    account_profile["method_average_positive_rank"] = (
        account_profile.groupby("visibility_method", sort=False).cumcount() + 1
    )
    account_profile = account_profile.sort_values(
        ["visibility_method", "region", "average_positive_available_usd", "account_id"],
        ascending=[True, True, False, True],
    )
    account_profile["region_method_average_positive_rank"] = (
        account_profile.groupby(
            ["visibility_method", "region"], sort=False
        ).cumcount()
        + 1
    )

    selected_ids = [
        account_id
        for method in VISIBILITY_SELECTION.values()
        for account_id in method
    ]
    _assert(len(selected_ids) == len(set(selected_ids)) == 10, "Invalid locked cohort")
    selected = account_profile.loc[
        account_profile["account_id"].isin(selected_ids)
    ].copy()
    _assert(len(selected) == 10, "One or more locked visibility accounts are missing")
    order = {account_id: index + 1 for index, account_id in enumerate(selected_ids)}
    selected["selection_order"] = selected["account_id"].map(order).astype(int)

    def selection_rule(row: pd.Series) -> str:
        if row["region"] == "APAC":
            return (
                "Highest APAC account by January–June average positive estimated "
                f"available USD within {row['visibility_method']} sources"
            )
        return (
            "Top four accounts by January–June average positive estimated available "
            f"USD within {row['visibility_method']} sources"
        )

    selected["selection_rule"] = selected.apply(selection_rule, axis=1)
    selected["shadow_only_flag"] = selected["account_id"].eq("AC0040")
    selected["control_review_required"] = True
    selected["enhanced_control_review_required"] = selected["account_id"].eq(
        "AC0040"
    )
    selected["cohort_treatment"] = selected["shadow_only_flag"].map(
        {
            True: (
                "Read-only shadow observation; substitution subject to enhanced "
                "control review"
            ),
            False: "Provisional read-only cohort; subject to readiness and control review",
        }
    )
    selected["readiness_status"] = (
        "NOT LAUNCH-READY — authoritative source, cutoff, owner, reconciliation, "
        "service, control, cost, and rollback evidence open"
    )
    selected["selection_rule_version"] = VISIBILITY_RULE_VERSION
    selected["evidence_label"] = "ANALYST-CALC / ANALYST-JUDGMENT"
    selected["decision_boundary"] = EVIDENCE_BOUNDARY
    selected["average_positive_available_usd"] = selected[
        "average_positive_available_usd"
    ].round(2)
    selected = selected.sort_values("selection_order").reset_index(drop=True)
    return selected[list(VISIBILITY_OUTPUT_COLUMNS)]


def add_payment_sampling_fields(payments: pd.DataFrame) -> pd.DataFrame:
    """Add the locked issue modes, overall definition, and Week 2 USD bands."""
    working = payments.copy()
    working["exception_status_case_flag"] = (
        working["exception_flag"]
        | working["status"].isin(["Repaired", "Rejected"])
    )
    working["late_only_case_flag"] = (
        working["late_release_flag"]
        & ~working["exception_status_case_flag"]
    )
    working["issue_case_flag"] = (
        working["exception_status_case_flag"]
        | working["late_only_case_flag"]
    )
    working["source_issue_mode"] = "Non-issue"
    working.loc[
        working["exception_status_case_flag"], "source_issue_mode"
    ] = "Exception/status"
    working.loc[working["late_only_case_flag"], "source_issue_mode"] = "Late-only"

    def issue_hits(row: pd.Series) -> str:
        hits: List[str] = []
        if row["exception_flag"]:
            hits.append("exception_flag")
        if row["late_release_flag"]:
            hits.append("late_release_flag")
        if row["status"] == "Repaired":
            hits.append("status_repaired")
        if row["status"] == "Rejected":
            hits.append("status_rejected")
        return "; ".join(hits) if hits else "none"

    working["issue_definition_hits"] = working.apply(issue_hits, axis=1)
    working["amount_band_usd"] = pd.cut(
        working["amount_usd"],
        bins=[float("-inf"), 10_000, 25_000, 50_000, 100_000, float("inf")],
        labels=list(AMOUNT_BAND_LABELS),
        ordered=True,
    )
    _assert(working["amount_band_usd"].notna().all(), "Unassigned USD amount band")
    working["amount_band_order"] = (
        working["amount_band_usd"].cat.codes.astype(int) + 1
    )
    working["month"] = working["payment_date"].dt.to_period("M").astype(str)
    return working


def _month_number(month: str) -> int:
    period = pd.Period(month, freq="M")
    return period.year * 12 + period.month


def _match_control(issue: pd.Series, candidates: pd.DataFrame) -> pd.Series:
    """Choose the deterministic nearest unused non-issue control."""
    ranked = candidates.copy()
    ranked["payment_type_match"] = ranked["payment_type"].eq(issue["payment_type"])
    ranked["region_match"] = ranked["region"].eq(issue["region"])
    ranked["month_match"] = ranked["month"].eq(issue["month"])
    ranked["amount_band_match"] = ranked["amount_band_usd"].astype(str).eq(
        str(issue["amount_band_usd"])
    )
    match_columns = [
        "payment_type_match",
        "region_match",
        "month_match",
        "amount_band_match",
    ]
    ranked["match_deviation_count"] = 4 - ranked[match_columns].sum(axis=1)
    ranked["amount_band_distance"] = (
        ranked["amount_band_order"] - int(issue["amount_band_order"])
    ).abs()
    ranked["month_distance"] = ranked["month"].map(_month_number).sub(
        _month_number(str(issue["month"]))
    ).abs()
    ranked["absolute_amount_gap_usd"] = (
        ranked["amount_usd"] - float(issue["amount_usd"])
    ).abs()
    ranked = ranked.sort_values(
        [
            "match_deviation_count",
            "amount_band_distance",
            "month_distance",
            "absolute_amount_gap_usd",
            "payment_id",
        ],
        ascending=True,
        kind="mergesort",
    )
    _assert(not ranked.empty, "No unused non-issue control remains")
    return ranked.iloc[0]


def _deviation_detail(control: pd.Series) -> str:
    fields = [
        ("payment_type", bool(control["payment_type_match"])),
        ("region", bool(control["region_match"])),
        ("month", bool(control["month_match"])),
        ("amount_band", bool(control["amount_band_match"])),
    ]
    mismatches = [name for name, matched in fields if not matched]
    return "none" if not mismatches else "; ".join(mismatches)


def _sample_row(
    source: pd.Series,
    paired: pd.Series,
    cohort: str,
    pair_sequence: int,
    issue_mode: str,
    issue_mode_selection_rank: int,
    role: str,
    match: pd.Series,
) -> Dict[str, object]:
    """Format one issue/control row while retaining source identifiers."""
    role_order = 1 if role == "Issue case" else 2
    cohort_code = f"C{PAYMENT_COHORTS.index(cohort) + 1}"
    pair_id = f"{cohort_code}-{pair_sequence:02d}"
    sample_order = PAYMENT_COHORTS.index(cohort) * 30 + (pair_sequence - 1) * 2 + role_order
    deviations = int(match["match_deviation_count"])
    row_issue_mode = issue_mode if role == "Issue case" else "Non-issue control"
    row_issue_rank = pair_sequence if role == "Issue case" else 0
    row_mode_rank = issue_mode_selection_rank if role == "Issue case" else 0
    return {
        "sample_order": sample_order,
        "case_control_pair_id": pair_id,
        "pair_sequence_within_cohort": pair_sequence,
        "sample_role": role,
        "source_payment_id": source["payment_id"],
        "paired_source_payment_id": paired["payment_id"],
        "priority_payment_cohort": cohort,
        "issue_case_flag": bool(source["issue_case_flag"]),
        "issue_definition_hits": source["issue_definition_hits"],
        "issue_mode": row_issue_mode,
        "paired_issue_mode": issue_mode,
        "issue_selection_rank": row_issue_rank,
        "issue_mode_selection_rank": row_mode_rank,
        "payment_date": source["payment_date"].date().isoformat(),
        "month": source["month"],
        "account_id": source["account_id"],
        "entity_id": source["entity_id"],
        "entity_name": source["entity_name"],
        "region": source["region"],
        "country": source["country"],
        "bank_name": source["bank_name"],
        "erp_system": source["erp_system"],
        "purpose": source["purpose"],
        "visibility_method": source["visibility_method"],
        "payment_type": source["payment_type"],
        "currency": source["currency"],
        "amount_local": source["amount_local"],
        "usd_per_unit": source["usd_per_unit"],
        "amount_usd": round(float(source["amount_usd"]), 2),
        "amount_band_usd": str(source["amount_band_usd"]),
        "amount_band_order": int(source["amount_band_order"]),
        "cross_border_flag": bool(source["cross_border_flag"]),
        "cross_border_wire_flag": bool(source["cross_border_wire_flag"]),
        "manual_touch_flag": bool(source["manual_touch_flag"]),
        "exception_flag": bool(source["exception_flag"]),
        "late_release_flag": bool(source["late_release_flag"]),
        "repair_minutes": int(source["repair_minutes"]),
        "fee_usd": source["fee_usd"],
        "status": source["status"],
        "payment_type_match": bool(match["payment_type_match"]),
        "region_match": bool(match["region_match"]),
        "month_match": bool(match["month_match"]),
        "amount_band_match": bool(match["amount_band_match"]),
        "match_deviation_count": deviations,
        "match_deviation_detail": _deviation_detail(match),
        "amount_band_distance": int(match["amount_band_distance"]),
        "month_distance": int(match["month_distance"]),
        "absolute_amount_gap_usd": round(float(match["absolute_amount_gap_usd"]), 2),
        "match_quality": (
            "Exact four-field match"
            if deviations == 0
            else "Nearest available; deviations documented"
        ),
        "selection_rule_version": PAYMENT_RULE_VERSION,
        "sample_purpose": (
            "Purposive root-cause case-control review; not a prevalence or benefit sample"
        ),
        "evidence_label": "ACG-DATA / ANALYST-CALC / ANALYST-JUDGMENT",
        "decision_boundary": EVIDENCE_BOUNDARY,
    }


def build_payment_sample(payments: pd.DataFrame) -> pd.DataFrame:
    """Select 8 exception/status and 7 late-only cases plus 15 controls."""
    working = add_payment_sampling_fields(payments)
    rows: List[Dict[str, object]] = []
    for cohort in PAYMENT_COHORTS:
        cohort_frame = working.loc[
            working["priority_payment_cohort"].eq(cohort)
        ].copy()
        # A comparator must be flag-negative and have a supplied Completed
        # outcome. Pending is not treated as a clean control because its
        # unresolved status-as-of could conceal later friction or failure.
        control_pool = cohort_frame.loc[
            ~cohort_frame["issue_case_flag"]
            & cohort_frame["status"].eq("Completed")
        ].copy()
        _assert(len(control_pool) >= 15, f"Fewer than 15 non-issue controls in {cohort}")
        selected_mode_frames: List[pd.DataFrame] = []
        for issue_mode, target in ISSUE_MODE_TARGETS.items():
            issue_pool = cohort_frame.loc[
                cohort_frame["source_issue_mode"].eq(issue_mode)
            ].sort_values(
                ["repair_minutes", "amount_usd", "payment_id"],
                ascending=[False, False, True],
                kind="mergesort",
            )
            _assert(
                len(issue_pool) >= target,
                f"Fewer than {target} {issue_mode} cases in {cohort}",
            )
            selected_mode = issue_pool.head(target).copy()
            selected_mode["issue_mode_selection_rank"] = range(1, target + 1)
            selected_mode_frames.append(selected_mode)
        selected_issues = pd.concat(selected_mode_frames, ignore_index=False)
        unused_controls = control_pool.copy()
        for pair_sequence, (_, issue) in enumerate(
            selected_issues.iterrows(), start=1
        ):
            issue_mode = str(issue["source_issue_mode"])
            issue_mode_selection_rank = int(issue["issue_mode_selection_rank"])
            match = _match_control(issue, unused_controls)
            control = unused_controls.loc[match.name]
            rows.append(
                _sample_row(
                    issue,
                    control,
                    cohort,
                    pair_sequence,
                    issue_mode,
                    issue_mode_selection_rank,
                    "Issue case",
                    match,
                )
            )
            rows.append(
                _sample_row(
                    control,
                    issue,
                    cohort,
                    pair_sequence,
                    issue_mode,
                    issue_mode_selection_rank,
                    "Non-issue control",
                    match,
                )
            )
            unused_controls = unused_controls.drop(index=match.name)

    result = pd.DataFrame(rows).sort_values("sample_order").reset_index(drop=True)
    return result[list(PAYMENT_OUTPUT_COLUMNS)]


def validate_pilot_contract(
    visibility: pd.DataFrame,
    payment_sample: pd.DataFrame,
    payments: pd.DataFrame,
) -> None:
    """Enforce cohort, pairing, lineage, and evidence-boundary controls."""
    expected_visibility_ids = [
        account_id
        for method in VISIBILITY_SELECTION.values()
        for account_id in method
    ]
    _assert(len(visibility) == 10, "Visibility cohort must contain 10 accounts")
    _assert(visibility["account_id"].is_unique, "Visibility accounts must be unique")
    _assert(
        visibility.sort_values("selection_order")["account_id"].tolist()
        == expected_visibility_ids,
        "Visibility cohort or order differs from the locked charter",
    )
    for method, account_ids in VISIBILITY_SELECTION.items():
        method_frame = visibility.loc[
            visibility["visibility_method"].eq(method)
        ]
        actual = method_frame["account_id"].tolist()
        _assert(actual == list(account_ids), f"{method} cohort drift")
        _assert(
            set(
                method_frame.loc[
                    ~method_frame["region"].eq("APAC"),
                    "method_average_positive_rank",
                ].astype(int)
            )
            == {1, 2, 3, 4},
            f"{method} leaders no longer satisfy the locked top-four rule",
        )
        apac = method_frame.loc[method_frame["region"].eq("APAC")]
        _assert(
            len(apac) == 1
            and int(apac.iloc[0]["region_method_average_positive_rank"]) == 1,
            f"{method} APAC account no longer satisfies the locked regional rule",
        )
    _assert(visibility["region"].nunique() == 3, "Visibility coverage must span 3 regions")
    _assert(visibility["erp_system"].nunique() == 3, "Visibility coverage must span 3 ERPs")
    _assert(visibility["bank_name"].nunique() == 4, "Visibility coverage must span 4 banks")
    _assert(
        visibility["minimum_reporting_delay_days"].gt(0).all()
        and visibility["supplied_account_days"].eq(181).all(),
        "Visibility cohort must remain delayed across the complete supplied panel",
    )
    visibility_required_fields = [
        "account_id",
        "entity_id",
        "entity_name",
        "region",
        "country",
        "currency",
        "bank_name",
        "erp_system",
        "visibility_method",
        "purpose",
        "cash_restriction_level",
        "selection_rule",
        "cohort_treatment",
        "readiness_status",
        "selection_rule_version",
        "evidence_label",
        "decision_boundary",
    ]
    _assert(
        _required_fields_are_nonblank(visibility, visibility_required_fields),
        "Visibility selection contains a blank required field",
    )
    _assert(
        visibility["control_review_required"].all(),
        "Every visibility account must remain subject to readiness/control review",
    )
    ac0040 = visibility.loc[visibility["account_id"].eq("AC0040")]
    _assert(len(ac0040) == 1, "AC0040 missing from visibility cohort")
    _assert(
        bool(ac0040.iloc[0]["shadow_only_flag"])
        and bool(ac0040.iloc[0]["control_review_required"])
        and bool(ac0040.iloc[0]["enhanced_control_review_required"])
        and ac0040.iloc[0]["region"] == "APAC"
        and ac0040.iloc[0]["purpose"] == "Payroll"
        and bool(ac0040.iloc[0]["restricted_flag"])
        and "shadow" in ac0040.iloc[0]["cohort_treatment"].lower(),
        "AC0040 must remain APAC, Payroll, restricted, shadow-only, and enhanced-review gated",
    )
    _assert(
        not visibility.loc[~visibility["account_id"].eq("AC0040"), "shadow_only_flag"].any(),
        "Only AC0040 may be flagged shadow-only in the locked cohort",
    )
    _assert(
        not visibility.loc[
            ~visibility["account_id"].eq("AC0040"),
            "enhanced_control_review_required",
        ].any(),
        "Only AC0040 may be flagged for enhanced control review",
    )

    _assert(len(payment_sample) == 120, "Payment sample must contain 120 rows")
    _assert(payment_sample["source_payment_id"].is_unique, "Payment IDs must be unique")
    payment_required_fields = [
        "case_control_pair_id",
        "sample_role",
        "source_payment_id",
        "paired_source_payment_id",
        "priority_payment_cohort",
        "issue_definition_hits",
        "issue_mode",
        "paired_issue_mode",
        "payment_date",
        "month",
        "account_id",
        "entity_id",
        "entity_name",
        "region",
        "country",
        "bank_name",
        "erp_system",
        "purpose",
        "visibility_method",
        "payment_type",
        "currency",
        "status",
        "match_deviation_detail",
        "match_quality",
        "selection_rule_version",
        "sample_purpose",
        "evidence_label",
        "decision_boundary",
    ]
    _assert(
        _required_fields_are_nonblank(payment_sample, payment_required_fields),
        "Payment selection contains a blank required field",
    )
    _assert(
        payment_sample["priority_payment_cohort"].tolist()
        == sorted(
            payment_sample["priority_payment_cohort"].tolist(),
            key=lambda value: PAYMENT_COHORTS.index(value),
        ),
        "Payment cohorts must retain governed order",
    )
    cohort_counts = payment_sample.groupby("priority_payment_cohort", sort=False).size()
    _assert(
        cohort_counts.to_dict() == {cohort: 30 for cohort in PAYMENT_COHORTS},
        "Every payment cohort must contain 30 rows",
    )
    role_counts = payment_sample.groupby(
        ["priority_payment_cohort", "sample_role"], sort=False
    ).size()
    for cohort in PAYMENT_COHORTS:
        _assert(role_counts.loc[(cohort, "Issue case")] == 15, f"Issue count drift: {cohort}")
        _assert(
            role_counts.loc[(cohort, "Non-issue control")] == 15,
            f"Control count drift: {cohort}",
        )
    issue_rows = payment_sample.loc[
        payment_sample["sample_role"].eq("Issue case")
    ]
    control_rows = payment_sample.loc[
        payment_sample["sample_role"].eq("Non-issue control")
    ]
    mode_counts = issue_rows.groupby(
        ["priority_payment_cohort", "issue_mode"], sort=False
    ).size()
    for cohort in PAYMENT_COHORTS:
        for issue_mode, target in ISSUE_MODE_TARGETS.items():
            _assert(
                mode_counts.loc[(cohort, issue_mode)] == target,
                f"{issue_mode} allocation drift: {cohort}",
            )
    _assert(
        issue_rows["issue_case_flag"].all(),
        "Every issue row must meet the locked issue definition",
    )
    _assert(
        not control_rows["issue_case_flag"].any(),
        "Every control row must be non-issue",
    )
    _assert(
        control_rows["status"].eq("Completed").all(),
        "Every control row must have supplied status Completed",
    )
    _assert(
        (
            issue_rows.loc[
                issue_rows["issue_mode"].eq("Exception/status"),
                "exception_flag",
            ]
            | issue_rows.loc[
                issue_rows["issue_mode"].eq("Exception/status"), "status"
            ].isin(["Repaired", "Rejected"])
        ).all(),
        "Exception/status sample contains a case outside its locked mode",
    )
    late_only_rows = issue_rows.loc[issue_rows["issue_mode"].eq("Late-only")]
    _assert(
        late_only_rows["late_release_flag"].all()
        and not (
            late_only_rows["exception_flag"]
            | late_only_rows["status"].isin(["Repaired", "Rejected"])
        ).any(),
        "Late-only sample contains an exception/status case",
    )
    pair_counts = payment_sample.groupby("case_control_pair_id").size()
    _assert(len(pair_counts) == 60 and pair_counts.eq(2).all(), "Every pair must have two rows")

    source = add_payment_sampling_fields(payments).set_index("payment_id")
    _assert(
        set(payment_sample["source_payment_id"]).issubset(source.index),
        "Sample contains an unknown source payment ID",
    )
    for _, row in payment_sample.iterrows():
        source_row = source.loc[row["source_payment_id"]]
        _assert(
            row["priority_payment_cohort"] == str(source_row["priority_payment_cohort"]),
            f"Cohort lineage failure: {row['source_payment_id']}",
        )
        expected_issue = bool(
            source_row["exception_flag"]
            or source_row["late_release_flag"]
            or source_row["status"] in {"Repaired", "Rejected"}
        )
        _assert(
            bool(row["issue_case_flag"]) == expected_issue,
            f"Issue-definition lineage failure: {row['source_payment_id']}",
        )
        if row["sample_role"] == "Issue case":
            _assert(
                row["issue_mode"] == source_row["source_issue_mode"],
                f"Issue-mode lineage failure: {row['source_payment_id']}",
            )

    for pair_id, pair in payment_sample.groupby("case_control_pair_id", sort=False):
        issue = pair.loc[pair["sample_role"].eq("Issue case")].iloc[0]
        control = pair.loc[pair["sample_role"].eq("Non-issue control")].iloc[0]
        _assert(
            issue["paired_source_payment_id"] == control["source_payment_id"]
            and control["paired_source_payment_id"] == issue["source_payment_id"],
            f"Broken pairing lineage: {pair_id}",
        )
        _assert(
            issue["issue_mode"] == issue["paired_issue_mode"]
            and control["issue_mode"] == "Non-issue control"
            and control["paired_issue_mode"] == issue["paired_issue_mode"]
            and int(issue["issue_selection_rank"])
            == int(issue["pair_sequence_within_cohort"])
            and int(issue["issue_mode_selection_rank"]) > 0
            and int(control["issue_selection_rank"]) == 0
            and int(control["issue_mode_selection_rank"]) == 0,
            f"Broken issue-mode pairing: {pair_id}",
        )
        expected_matches = {
            "payment_type_match": issue["payment_type"] == control["payment_type"],
            "region_match": issue["region"] == control["region"],
            "month_match": issue["month"] == control["month"],
            "amount_band_match": issue["amount_band_usd"] == control["amount_band_usd"],
        }
        for field, expected_match in expected_matches.items():
            _assert(
                bool(issue[field]) == bool(control[field]) == expected_match,
                f"Incorrect {field}: {pair_id}",
            )
        _assert(
            int(issue["match_deviation_count"])
            == int(control["match_deviation_count"])
            == 4 - sum(expected_matches.values()),
            f"Incorrect deviation count: {pair_id}",
        )

    working = add_payment_sampling_fields(payments)
    for cohort in PAYMENT_COHORTS:
        for issue_mode, target in ISSUE_MODE_TARGETS.items():
            expected_top = (
                working.loc[
                    working["priority_payment_cohort"].eq(cohort)
                    & working["source_issue_mode"].eq(issue_mode)
                ]
                .sort_values(
                    ["repair_minutes", "amount_usd", "payment_id"],
                    ascending=[False, False, True],
                    kind="mergesort",
                )
                .head(target)["payment_id"]
                .tolist()
            )
            actual_mode = issue_rows.loc[
                issue_rows["priority_payment_cohort"].eq(cohort)
                & issue_rows["issue_mode"].eq(issue_mode)
            ].sort_values("issue_mode_selection_rank")
            _assert(
                actual_mode["source_payment_id"].tolist() == expected_top
                and actual_mode["issue_mode_selection_rank"].astype(int).tolist()
                == list(range(1, target + 1)),
                f"{issue_mode} ranking drift: {cohort}",
            )

    regenerated_sample = build_payment_sample(payments)
    assert_frame_equal(
        payment_sample.reset_index(drop=True),
        regenerated_sample.reset_index(drop=True),
        check_dtype=True,
        obj="deterministic payment sample",
    )

    _assert(
        payment_sample["sample_purpose"].str.contains(
            "not a prevalence", case=False, regex=False
        ).all(),
        "Every payment row must retain the purposive-sample boundary",
    )
    _assert(
        visibility["decision_boundary"].eq(EVIDENCE_BOUNDARY).all()
        and payment_sample["decision_boundary"].eq(EVIDENCE_BOUNDARY).all(),
        "Pilot outputs lost their evidence boundary",
    )


def build_control_records(
    anchors: Dict[str, float],
    visibility: pd.DataFrame,
    payment_sample: pd.DataFrame,
) -> pd.DataFrame:
    """Create an auditable manifest of model controls and outcomes."""
    cohort_counts = payment_sample.groupby("priority_payment_cohort", sort=False).size()
    role_counts = payment_sample.groupby(
        ["priority_payment_cohort", "sample_role"], sort=False
    ).size()
    issue_mode_counts = payment_sample.loc[
        payment_sample["sample_role"].eq("Issue case")
    ].groupby(["priority_payment_cohort", "issue_mode"], sort=False).size()
    rows: List[Tuple[str, str, str, str, str]] = [
        ("PC01", "Week 2 population", "55 accounts / 9,955 account-days", "55 / 9,955", "PASS"),
        ("PC02", "Week 2 visibility", "5,792 same-day proxy account-days / 23 delayed accounts", "5,792 / 23", "PASS"),
        ("PC03", "Visibility cohort", "10 unique locked accounts; 5 Spreadsheet and 5 Portal", f"{len(visibility)} unique; 5 / 5", "PASS"),
        ("PC04", "Visibility coverage", "3 regions / 3 ERPs / 4 banks", f"{visibility['region'].nunique()} / {visibility['erp_system'].nunique()} / {visibility['bank_name'].nunique()}", "PASS"),
        ("PC05", "Visibility review treatment", "All 10 require readiness/control review; AC0040 alone is APAC, Payroll, restricted, shadow-only, and enhanced-review gated", "All 10 reviewed; AC0040 also enhanced-review and shadow-only", "PASS"),
        ("PC06", "Week 2 payments", "7,600 records / $198,135,489.50 intent / 20,080 repair minutes", f"{int(anchors['payment_records']):,} / ${anchors['gross_payment_intent_usd']:,.2f} / {int(anchors['repair_minutes']):,}", "PASS"),
        ("PC07", "Week 2 priority union", "2,839 records / 356 exceptions / 14,939 repair minutes", f"{int(anchors['priority_union_records']):,} / {int(anchors['priority_union_exceptions']):,} / {int(anchors['priority_union_repair_minutes']):,}", "PASS"),
        ("PC08", "Payment sample", "120 unique source records", f"{len(payment_sample)} rows / {payment_sample['source_payment_id'].nunique()} unique", "PASS"),
        ("PC09", "Cohort allocation", "30 rows in each of four mutually exclusive cohorts", "; ".join(f"{cohort}: {int(cohort_counts.loc[cohort])}" for cohort in PAYMENT_COHORTS), "PASS"),
        ("PC10", "Case-control allocation", "15 issues and 15 controls per cohort", "; ".join(f"{cohort}: {int(role_counts.loc[(cohort, 'Issue case')])}/{int(role_counts.loc[(cohort, 'Non-issue control')])}" for cohort in PAYMENT_COHORTS), "PASS"),
        ("PC11", "Issue-mode allocation", "Per cohort: 8 exception/status cases and 7 late-only cases", "; ".join(f"{cohort}: {int(issue_mode_counts.loc[(cohort, 'Exception/status')])}/{int(issue_mode_counts.loc[(cohort, 'Late-only')])}" for cohort in PAYMENT_COHORTS), "PASS"),
        ("PC12", "Issue and control eligibility", "exception/status means exception OR Repaired/Rejected; late-only means late release without exception/status; controls are issue-flag-negative and supplied status Completed", "32 exception/status; 28 late-only; all 60 controls flag-negative and Completed", "PASS"),
        ("PC13", "Matching disclosure", "Every pair records four match fields and all deviations", f"{payment_sample['case_control_pair_id'].nunique()} pairs; {(payment_sample['match_deviation_count'].eq(0).sum() // 2)} exact", "PASS"),
        ("PC14", "Evidence use", "Purposive root-cause review; not prevalence, causality, or benefit", "Boundary present on every row", "PASS"),
    ]
    result = pd.DataFrame(
        rows,
        columns=[
            "control_record_id",
            "control_name",
            "control_rule",
            "actual_result",
            "test_result",
        ],
    )
    result["visibility_rule_version"] = VISIBILITY_RULE_VERSION
    result["payment_rule_version"] = PAYMENT_RULE_VERSION
    result["evidence_boundary"] = EVIDENCE_BOUNDARY
    return result


def build_pilot_model() -> Dict[str, pd.DataFrame]:
    """Build and validate all three governed Week 3 pilot outputs."""
    data, balances, payments = load_governed_inputs()
    anchors = validate_week2_anchors(data, balances, payments)
    visibility = build_visibility_candidates(data, balances)
    payment_sample = build_payment_sample(payments)
    validate_pilot_contract(visibility, payment_sample, payments)

    # Determinism is an execution control: the same governed inputs must yield
    # byte-equivalent frames before any file is written.
    visibility_again = build_visibility_candidates(data, balances)
    payment_again = build_payment_sample(payments)
    assert_frame_equal(visibility, visibility_again, check_dtype=True)
    assert_frame_equal(payment_sample, payment_again, check_dtype=True)

    controls = build_control_records(anchors, visibility, payment_sample)
    return {
        "visibility_candidates": visibility,
        "payment_sample": payment_sample,
        "controls": controls,
    }


def write_outputs(outputs: Dict[str, pd.DataFrame]) -> None:
    """Write only the three governed Week 3 pilot-model CSVs."""
    output_paths = {
        "visibility_candidates": PROCESSED / "W3_visibility_pilot_candidates.csv",
        "payment_sample": PROCESSED / "W3_payment_sample_frame.csv",
        "controls": PROCESSED / "W3_pilot_model_controls.csv",
    }
    _assert(set(outputs) == set(output_paths), "Unexpected pilot output key")
    PROCESSED.mkdir(parents=True, exist_ok=True)
    for key, path in output_paths.items():
        outputs[key].to_csv(path, index=False)


def main() -> None:
    outputs = build_pilot_model()
    write_outputs(outputs)
    visibility = outputs["visibility_candidates"]
    sample = outputs["payment_sample"]
    exact_pairs = sample.loc[sample["sample_role"].eq("Issue case"), "match_deviation_count"].eq(0).sum()
    print(
        "Visibility pilot frame: "
        f"{len(visibility)} accounts; {visibility['region'].nunique()} regions; "
        f"{visibility['erp_system'].nunique()} ERPs; {visibility['bank_name'].nunique()} banks"
    )
    print(
        "Payment root-cause frame: "
        f"{len(sample)} unique records; 60 issue/control pairs; "
        f"{exact_pairs} exact four-field matches"
    )
    print("Wrote data/processed/W3_visibility_pilot_candidates.csv")
    print("Wrote data/processed/W3_payment_sample_frame.csv")
    print("Wrote data/processed/W3_pilot_model_controls.csv")


if __name__ == "__main__":
    main()
