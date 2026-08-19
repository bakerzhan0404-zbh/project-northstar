"""Executable structural controls for the Week 3 operating-model design pack."""

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
W3 = ROOT / "deliverables" / "working" / "week_3"
PROCESSED = ROOT / "data" / "processed"

OPERATING_MODEL = W3 / "W3_future_state_operating_model.md"
PROCESS_RACI = W3 / "W3_future_state_process_map_and_RACI.md"
CONTROL_INVENTORY = W3 / "W3_control_inventory.csv"
VISIBILITY_CHARTER = W3 / "W3_visibility_pilot_charter.md"
PAYMENT_CHARTER = W3 / "W3_payment_pilot_charter.md"
VISIBILITY_FRAME = PROCESSED / "W3_visibility_pilot_candidates.csv"
PAYMENT_FRAME = PROCESSED / "W3_payment_sample_frame.csv"
PILOT_MODEL_CONTROLS = PROCESSED / "W3_pilot_model_controls.csv"

VISIBILITY_RULE_VERSION = "W3-VIS-PILOT-v2 · 2026-08-18"
PAYMENT_RULE_VERSION = "W3-PAY-PILOT-v3 · 2026-08-18"

PAYMENT_COHORTS = (
    "Manual touch only",
    "Manual touch + cross-border wire",
    "Cross-border wire only",
    "Neither priority cohort",
)

ISSUE_MODE_TARGETS = {
    "Exception/status": 8,
    "Late-only": 7,
}

EXPECTED_CONTROL_COLUMNS = [
    "control_id",
    "process",
    "control_objective",
    "risk_addressed",
    "proposed_control_activity",
    "control_type",
    "frequency_or_trigger",
    "proposed_accountable_owner",
    "proposed_operator",
    "evidence_required",
    "design_status",
    "pilot_gate",
    "stop_or_rollback_trigger",
    "specialist_review",
    "source_basis",
]

EXPECTED_CONTROL_IDS = {
    *(f"CASH-{number:02d}" for number in range(1, 7)),
    *(f"PAY-{number:02d}" for number in range(1, 8)),
    *(f"TECH-{number:02d}" for number in range(1, 4)),
    *(f"GOV-{number:02d}" for number in range(1, 4)),
}

EXPECTED_VISIBILITY_ACCOUNTS = {
    "AC0021",
    "AC0010",
    "AC0017",
    "AC0001",
    "AC0040",
    "AC0022",
    "AC0031",
    "AC0018",
    "AC0002",
    "AC0050",
}


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def main() -> None:
    required_paths = [
        OPERATING_MODEL,
        PROCESS_RACI,
        CONTROL_INVENTORY,
        VISIBILITY_CHARTER,
        PAYMENT_CHARTER,
    ]
    model_paths = [VISIBILITY_FRAME, PAYMENT_FRAME, PILOT_MODEL_CONTROLS]
    texts = {path.name: load_text(path) for path in required_paths if path.exists()}

    with CONTROL_INVENTORY.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        controls = list(reader)
        columns = reader.fieldnames

    control_ids = [row["control_id"] for row in controls]
    referenced_controls = set()
    for text in texts.values():
        referenced_controls.update(
            re.findall(r"\b(?:CASH|PAY|TECH|GOV)-\d{2}\b", text)
        )

    process_text = texts.get(PROCESS_RACI.name, "")
    visibility_text = texts.get(VISIBILITY_CHARTER.name, "")
    payment_text = texts.get(PAYMENT_CHARTER.name, "")
    operating_text = texts.get(OPERATING_MODEL.name, "")
    visibility_accounts = set(re.findall(r"\bAC\d{4}\b", visibility_text))

    visibility_rows, visibility_columns = load_csv(VISIBILITY_FRAME)
    payment_rows, payment_columns = load_csv(PAYMENT_FRAME)
    pilot_control_rows, _ = load_csv(PILOT_MODEL_CONTROLS)

    payment_ids = [row["source_payment_id"] for row in payment_rows]
    issue_rows = [row for row in payment_rows if row["sample_role"] == "Issue case"]
    nonissue_rows = [
        row for row in payment_rows if row["sample_role"] == "Non-issue control"
    ]
    cohort_role_counts = Counter(
        (row["priority_payment_cohort"], row["sample_role"])
        for row in payment_rows
    )
    issue_mode_counts = Counter(
        (row["priority_payment_cohort"], row["issue_mode"])
        for row in issue_rows
    )
    pair_counts = Counter(row["case_control_pair_id"] for row in payment_rows)
    exact_pairs = sum(
        int(row["match_deviation_count"]) == 0 for row in issue_rows
    )
    deviation_rows = [
        row for row in issue_rows if int(row["match_deviation_count"]) > 0
    ]
    ac0040_rows = [row for row in visibility_rows if row["account_id"] == "AC0040"]
    ac0040 = ac0040_rows[0] if len(ac0040_rows) == 1 else {}

    checks = {
        "all five Week 3 design artifacts exist": len(texts) == 5,
        "all three governed pilot-model outputs exist": all(
            path.exists() for path in model_paths
        ),
        "control inventory uses the governed 15-column schema": columns
        == EXPECTED_CONTROL_COLUMNS,
        "control inventory contains 19 unique controls": len(controls) == 19
        and len(control_ids) == len(set(control_ids)),
        "control IDs cover cash, payment, technology, and governance": set(
            control_ids
        )
        == EXPECTED_CONTROL_IDS,
        "every control has an evidence requirement and stop trigger": all(
            row["evidence_required"].strip()
            and row["stop_or_rollback_trigger"].strip()
            for row in controls
        ),
        "every control remains proposed and acts as a pilot gate": all(
            row["design_status"].startswith("Proposed")
            and row["pilot_gate"] == "Yes"
            for row in controls
        ),
        "all control references resolve to the inventory": referenced_controls
        <= set(control_ids),
        "cash and payment future-state maps are closed Mermaid blocks": (
            process_text.count("```mermaid") == 2
            and process_text.count("```") == 4
        ),
        "future-state direction is conditional federated coordination": (
            "federated coordination" in operating_text.lower()
            and "local stabilization" in operating_text.lower()
            and "not client approval" in operating_text.lower()
        ),
        "future-state design preserves zero established mobility and capacity": (
            "Validated movable cash remains `$0` in the funded case" in operating_text
            and "validated redeployable capacity remains `0 hours/month`"
            in operating_text
        ),
        "funding envelope is a ceiling rather than a cost estimate": all(
            "$1.0–$1.5m" in text
            and "ceiling" in text.lower()
            and "cost estimate" in text.lower()
            for text in (operating_text, visibility_text, payment_text)
        ),
        "visibility charter carries exactly the ten provisional accounts": (
            visibility_accounts == EXPECTED_VISIBILITY_ACCOUNTS
        ),
        "visibility charter requires the 55-account readiness census": (
            "all 55 accounts / 9,955 supplied account-days" in visibility_text
            and "purposive, not statistically representative" in visibility_text
        ),
        "visibility charter keeps mobility outside the test": (
            "This pilot does not test, authorize, or value cash mobility."
            in visibility_text
        ),
        "visibility charter states base and enhanced review semantics": (
            "All ten accounts require the same base readiness/control review"
            in visibility_text
            and "enhanced control review" in visibility_text
            and "`control_review_required = true` for 10/10 accounts"
            in visibility_text
            and "`enhanced_control_review_required = true` only for `AC0040`"
            in visibility_text
        ),
        "visibility charter uses generic approved peak-period language": (
            "outside approved blackout/peak periods" in visibility_text
            and "launch window remain TBD" in visibility_text
            and "fourth-quarter" not in visibility_text.lower()
            and "q4" not in visibility_text.lower()
        ),
        "visibility frame uses the v2 review fields": (
            {
                "control_review_required",
                "enhanced_control_review_required",
                "shadow_only_flag",
            }
            <= set(visibility_columns)
            and len(visibility_rows) == 10
            and {row["account_id"] for row in visibility_rows}
            == EXPECTED_VISIBILITY_ACCOUNTS
            and all(
                row["control_review_required"] == "True"
                for row in visibility_rows
            )
            and {
                row["account_id"]
                for row in visibility_rows
                if row["enhanced_control_review_required"] == "True"
            }
            == {"AC0040"}
            and {
                row["account_id"]
                for row in visibility_rows
                if row["shadow_only_flag"] == "True"
            }
            == {"AC0040"}
            and all(
                row["selection_rule_version"] == VISIBILITY_RULE_VERSION
                for row in visibility_rows
            )
        ),
        "AC0040 retains the enhanced-review source semantics": (
            len(ac0040_rows) == 1
            and ac0040.get("region") == "APAC"
            and ac0040.get("purpose") == "Payroll"
            and ac0040.get("restricted_flag") == "True"
            and ac0040.get("control_review_required") == "True"
            and ac0040.get("enhanced_control_review_required") == "True"
            and ac0040.get("shadow_only_flag") == "True"
        ),
        "payment charter fixes a 120-record four-stratum diagnostic": (
            "Review **120 supplied records**, 30 from each mutually exclusive stratum"
            in payment_text
            and "**8 exception/status issue cases**" in payment_text
            and "**7 late-only issue cases**" in payment_text
            and "**15 non-issue controls**" in payment_text
        ),
        "payment issue modes and ranking are explicit and reproducible": (
            "`exception_flag = true` or status is `Repaired`/`Rejected`"
            in payment_text
            and "`late_release_flag = true`" in payment_text
            and "Rank each issue-mode subgroup separately" in payment_text
            and "repair minutes descending, USD amount descending"
            in payment_text
            and "source payment ID ascending" in payment_text
        ),
        "payment 8/7 split is coverage judgment rather than prevalence weighting": (
            "balances diagnostic coverage" in payment_text
            and "larger source pool in every cohort" in payment_text
            and "not prevalence weighting" in payment_text
        ),
        "payment charter fixes combined issue-mode matching order": (
            "exception/status ranks 1–8 first" in payment_text
            and "late-only ranks 1–7 second" in payment_text
            and "overall ranks 9–15" in payment_text
        ),
        "payment charter reports the current v3 matching result": (
            "50 exact four-field pairs" in payment_text
            and "ten documented nearest-match deviations" in payment_text
            and "row-level `issue_mode`" in payment_text
            and "pair-level `paired_issue_mode`" in payment_text
        ),
        "payment charter excludes Pending from the control pool": (
            "supplied status `Completed`" in payment_text
            and "`Pending` records remain inside the supplied source population"
            in payment_text
            and "excluded from the non-issue control pool" in payment_text
            and "not certify a `Completed` record as settled" in payment_text
        ),
        "payment charter rejects stale issue and match wording": (
            "**15 issue cases**" not in payment_text
            and "55 exact four-field pairs" not in payment_text
            and "five documented nearest-match deviations" not in payment_text
            and "51 exact four-field pairs" not in payment_text
            and "nine documented nearest-match deviations" not in payment_text
        ),
        "payment frame uses v3 issue-mode lineage fields": (
            {
                "issue_mode",
                "paired_issue_mode",
                "issue_selection_rank",
                "issue_mode_selection_rank",
            }
            <= set(payment_columns)
            and len(payment_rows) == 120
            and len(payment_ids) == len(set(payment_ids)) == 120
            and all(
                row["selection_rule_version"] == PAYMENT_RULE_VERSION
                for row in payment_rows
            )
        ),
        "payment frame allocates 15 issues and controls in every cohort": all(
            cohort_role_counts[(cohort, "Issue case")] == 15
            and cohort_role_counts[(cohort, "Non-issue control")] == 15
            for cohort in PAYMENT_COHORTS
        ),
        "payment frame allocates 8 exception/status and 7 late-only cases": all(
            issue_mode_counts[(cohort, issue_mode)] == target
            for cohort in PAYMENT_COHORTS
            for issue_mode, target in ISSUE_MODE_TARGETS.items()
        ),
        "payment frame keeps issue ranks deterministic and controls non-issue": (
            all(
                sorted(
                    int(row["issue_mode_selection_rank"])
                    for row in issue_rows
                    if row["priority_payment_cohort"] == cohort
                    and row["issue_mode"] == issue_mode
                )
                == list(range(1, target + 1))
                for cohort in PAYMENT_COHORTS
                for issue_mode, target in ISSUE_MODE_TARGETS.items()
            )
            and all(
                sorted(
                    int(row["issue_selection_rank"])
                    for row in issue_rows
                    if row["priority_payment_cohort"] == cohort
                )
                == list(range(1, 16))
                for cohort in PAYMENT_COHORTS
            )
            and all(
                row["issue_mode"] == "Non-issue control"
                and row["paired_issue_mode"] in ISSUE_MODE_TARGETS
                and int(row["issue_selection_rank"]) == 0
                and int(row["issue_mode_selection_rank"]) == 0
                and row["status"] == "Completed"
                for row in nonissue_rows
            )
        ),
        "payment frame excludes Pending and other unresolved control statuses": (
            len(nonissue_rows) == 60
            and all(row["status"] == "Completed" for row in nonissue_rows)
            and all(row["source_payment_id"] != "P004510" for row in nonissue_rows)
        ),
        "payment frame preserves combined matching order": all(
            [
                row["issue_mode"]
                for row in issue_rows
                if row["priority_payment_cohort"] == cohort
            ]
            == ["Exception/status"] * 8 + ["Late-only"] * 7
            and [
                int(row["issue_selection_rank"])
                for row in issue_rows
                if row["priority_payment_cohort"] == cohort
            ]
            == list(range(1, 16))
            for cohort in PAYMENT_COHORTS
        ),
        "payment frame contains 60 complete pairs and current 50/10 result": (
            len(pair_counts) == 60
            and all(count == 2 for count in pair_counts.values())
            and exact_pairs == 50
            and len(deviation_rows) == 10
            and all(
                row["match_deviation_detail"].strip()
                and row["match_deviation_detail"] != "none"
                for row in deviation_rows
            )
        ),
        "pilot control output records v3 and fourteen passing controls": (
            len(pilot_control_rows) == 14
            and all(row["test_result"] == "PASS" for row in pilot_control_rows)
            and all(
                row["visibility_rule_version"] == VISIBILITY_RULE_VERSION
                and row["payment_rule_version"] == PAYMENT_RULE_VERSION
                for row in pilot_control_rows
            )
        ),
        "payment review is not a prevalence or benefit sample": (
            "purposive case-control diagnosis" in payment_text
            and "not an enterprise benefit sample" in payment_text
        ),
        "both pilots require a separate later go or no-go": all(
            "separate go/no-go approval" in text
            for text in (visibility_text, payment_text)
        ),
        "both pilot cost ranges remain explicitly unavailable": all(
            "**Current cost range:** `TBD — not estimated from the supplied evidence.`"
            in text
            for text in (visibility_text, payment_text)
        ),
        "both pilots retain four-week and four-hour gates": all(
            "four consecutive" in text and "four hours" in text
            for text in (visibility_text, payment_text)
        ),
    }

    failed = []
    for name, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'} — {name}")
        if not passed:
            failed.append(name)

    if failed:
        raise SystemExit(f"{len(failed)} Week 3 operating-model checks failed")
    print(f"All {len(checks)} Week 3 operating-model checks passed.")


if __name__ == "__main__":
    main()
