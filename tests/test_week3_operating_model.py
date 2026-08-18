"""Executable structural controls for the Week 3 operating-model design pack."""

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
W3 = ROOT / "deliverables" / "working" / "week_3"

OPERATING_MODEL = W3 / "W3_future_state_operating_model.md"
PROCESS_RACI = W3 / "W3_future_state_process_map_and_RACI.md"
CONTROL_INVENTORY = W3 / "W3_control_inventory.csv"
VISIBILITY_CHARTER = W3 / "W3_visibility_pilot_charter.md"
PAYMENT_CHARTER = W3 / "W3_payment_pilot_charter.md"

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


def main() -> None:
    required_paths = [
        OPERATING_MODEL,
        PROCESS_RACI,
        CONTROL_INVENTORY,
        VISIBILITY_CHARTER,
        PAYMENT_CHARTER,
    ]
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

    checks = {
        "all five Week 3 design artifacts exist": len(texts) == 5,
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
        "payment charter fixes a 120-record four-stratum diagnostic": (
            "Review **120 supplied records**, 30 from each mutually exclusive stratum"
            in payment_text
            and "**15 issue cases**" in payment_text
            and "**15 non-issue controls**" in payment_text
        ),
        "payment issue definition is explicit and reproducible": (
            "exception, late release, `Repaired`, or `Rejected`" in payment_text
            and "rank by repair minutes and then USD amount" in payment_text
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
