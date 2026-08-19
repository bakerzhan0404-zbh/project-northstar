"""Executable content controls for the Week 3 executive control pack."""

import re
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
W3 = ROOT / "deliverables" / "working" / "week_3"

REQUIRED_FILES = {
    "decision": W3 / "W3_decision_log.md",
    "findings": W3 / "W3_findings_log.md",
    "risk": W3 / "W3_risk_register.md",
    "source": W3 / "W3_source_log.md",
    "cfo_qa": W3 / "W3_CFO_QA.md",
    "weekly": W3 / "W3_weekly_update.md",
    "index": W3 / "W3_submission_index.md",
}

GOVERNED_LABELS = {
    "`ACG-DATA`",
    "`ANALYST-CALC`",
    "`ANALYST-ASSUMPTION`",
    "`ANALYST-JUDGMENT`",
}


def csv_scores_consistent(path: Path) -> bool:
    """Risk CSV parses rectangularly and every score is likelihood x impact."""
    if not path.exists():
        return False
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return False
    for row in rows:
        try:
            likelihood = int(row["likelihood_1_to_5"])
            impact = int(row["impact_1_to_5"])
            score = int(row["score"])
        except (KeyError, TypeError, ValueError):
            return False
        if likelihood * impact != score:
            return False
    return True


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def markdown_rows(text: str, identifier_pattern: str):
    return [
        line
        for line in text.splitlines()
        if re.match(rf"^\| {identifier_pattern} \|", line)
    ]


def split_markdown_row(line: str):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def main() -> None:
    existing = {
        name: path for name, path in REQUIRED_FILES.items() if path.exists()
    }
    texts = {name: load_text(path) for name, path in existing.items()}
    combined = "\n".join(texts.values())

    decision = texts.get("decision", "")
    findings = texts.get("findings", "")
    risk = texts.get("risk", "")
    source = texts.get("source", "")
    cfo = texts.get("cfo_qa", "")
    weekly = texts.get("weekly", "")
    index = texts.get("index", "")

    decision_rows = markdown_rows(decision, r"DEC-\d{2}")
    finding_rows = markdown_rows(findings, r"F\d{2}")
    risk_rows = markdown_rows(risk, r"R\d{3}")
    primary_source_rows = markdown_rows(source, r"W3-S\d{2}")
    public_source_rows = markdown_rows(source, r"S0[1-7]")
    cfo_questions = re.findall(r"(?m)^## ([1-5])\. ", cfo)

    risk_scores_reconcile = len(risk_rows) >= 10
    for row in risk_rows:
        cells = split_markdown_row(row)
        try:
            likelihood = int(cells[3])
            impact = int(cells[4])
            score = int(cells[5])
        except (IndexError, ValueError):
            risk_scores_reconcile = False
            continue
        risk_scores_reconcile &= (
            1 <= likelihood <= 5
            and 1 <= impact <= 5
            and score == likelihood * impact
        )

    local_links_resolve = True
    for name in ("source", "index"):
        path = REQUIRED_FILES[name]
        text = texts.get(name, "")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if "://" in target or target.startswith("#"):
                continue
            clean_target = target.split("#", 1)[0]
            if not (path.parent / clean_target).resolve().exists():
                print(f"BROKEN LINK — {path.name}: {target}")
                local_links_resolve = False

    forbidden_overclaims = {
        "screen presented as movable cash": re.compile(
            r"\$38\.13m\s+(?:is|equals)\s+(?:validated |certified )?"
            r"(?:movable|idle|surplus) cash",
            re.IGNORECASE,
        ),
        "federated presented as approved or execution ready": re.compile(
            r"federated coordination\s+(?:is|remains)\s+"
            r"(?:client-approved|approved|funded|execution-ready)",
            re.IGNORECASE,
        ),
        "pilot presented as approved": re.compile(
            r"(?:visibility|payment|production) pilot\s+(?:is|has been)\s+approved",
            re.IGNORECASE,
        ),
        "nonzero recognized cash P&L or capacity": re.compile(
            r"recognized (?:cash|P&L|capacity)(?: value)?\s+(?:is|equals)\s+"
            r"\$(?!0(?:\D|$))\d",
            re.IGNORECASE,
        ),
        "numeric ROI NPV or payback claim": re.compile(
            r"(?:ROI|NPV|payback)\s+(?:is|equals|=)\s+[-+]?\d",
            re.IGNORECASE,
        ),
        "funding ceiling asserted as cost": re.compile(
            r"\$1\.0[–-]\$1\.5m\s+(?:is|equals)\s+(?:the )?"
            r"(?:implementation )?(?:cost|budget|spend authority)",
            re.IGNORECASE,
        ),
        "risk asserted as zero exposure": re.compile(
            r"risk (?:exposure|value)\s+(?:is|equals)\s+\$0",
            re.IGNORECASE,
        ),
    }

    overclaim_hits = {
        name: pattern.search(combined)
        for name, pattern in forbidden_overclaims.items()
    }

    checks = {
        "all seven executive-control Markdown files exist": len(existing)
        == len(REQUIRED_FILES),
        "all executive-control files are substantive": all(
            len(text.splitlines()) >= 20 for text in texts.values()
        ),
        "decision log records eight Week 3 analyst decisions": len(decision_rows)
        == 8
        and all(f"DEC-{number}" in decision for number in range(18, 26)),
        "decision log separates analyst recommendation from client decision and execution approval": (
            "Analyst recommendation pending CFO alignment" in decision
            and "Client decision" in decision
            and "Execution approval" in decision
            and "none is recorded here" in decision
        ),
        "findings log promotes exactly F12 through F17": (
            len(finding_rows) == 6
            and all(f"F{number}" in findings for number in range(12, 18))
        ),
        "findings retain confidence counterevidence action label and source fields": (
            "| Confidence | Counterevidence / limitation | Decision or action | Evidence label | Reproducible source |"
            in findings
        ),
        "risk register is a semantic Markdown table": (
            "| ID | Risk description | Type | Likelihood | Impact | Score | Early-warning indicator / trigger | Mitigation | Contingency / decision consequence | Proposed owner | Status | Evidence label |"
            in risk
            and len(risk_rows) >= 14
        ),
        "risk scores equal likelihood times impact": risk_scores_reconcile,
        "risk register states scores are not quantified exposure or value": (
            "They are not quantified risk exposure or risk value." in risk
        ),
        "source log contains all four governed internal labels": GOVERNED_LABELS
        <= set(re.findall(r"`[^`]+`", source)),
        "source log uses semantic primary and public-context tables": (
            "| ID | Source / location | Evidence label | Week 3 claim or use | Method / provenance | Material limitation | Current status |"
            in source
            and len(primary_source_rows) == 11
            and len(public_source_rows) == 7
            and "`PUBLIC-CONTEXT`" in source
        ),
        "source and submission-index local links resolve": local_links_resolve,
        "CFO guide contains exactly five numbered questions": cfo_questions
        == ["1", "2", "3", "4", "5"],
        "CFO answer one explains direction without funded value": (
            "scores federated coordination `87`, local stabilization `72`, and globally coordinated `60`"
            in cfo
            and "all five plausible alternative-weight cases" in cfo
            and "every current recognized cash/P&L/capacity value is `$0`"
            in cfo
        ),
        "CFO answer two separates the $38.13m screen from $0 mobility": (
            "`$38.13m` is the 30 June result of a 14-day diagnostic screen"
            in cfo
            and "`$21m` threshold passes `168/168`" in cfo
            and "`$35m` passes `138/168`" in cfo
            and "`$46.2m` passes `0/168`" in cfo
            and "recognized cash value remains `$0`" in cfo
        ),
        "CFO answer three keeps ceiling and returns unavailable": (
            "Ten cost-evidence packages remain open" in cfo
            and "`$1.0–$1.5m` initial transformation envelope" in cfo
            and "ROI, NPV, payback, and a funding recommendation are therefore `NOT AVAILABLE`"
            in cfo
        ),
        "CFO answer four explains both deterministic pilot frames": (
            "all-55-account / 9,955-account-day readiness census" in cfo
            and "120 unique records" in cfo
            and "eight exception/status cases" in cfo
            and "seven late-only cases" in cfo
            and "15 issue-flag-negative controls" in cfo
            and "50 are exact" in cfo
            and "10 nearest-match deviations" in cfo
            and "four hours" in cfo
        ),
        "CFO answer five states downside and all three base switch conditions": (
            "`$21m` liquidity screen" in cfo
            and "independent `$3,900` fee sensitivity" in cfo
            and "50 hours/month" in cfo
            and "global data/control ownership" in cfo
            and "minimum integration readiness" in cfo
            and "affordable initial stage" in cfo
            and "local stabilization" in cfo
        ),
        "weekly update contains the required six update sections": all(
            heading in weekly
            for heading in (
                "## Executive summary",
                "## Work completed",
                "## What the evidence now suggests",
                "## Hypothesis changes",
                "## Decisions, support, or escalation required",
                "## Risks and uncertainties",
                "## Priorities for Week 4",
            )
        ),
        "weekly update is Amber for explicit unresolved gates": (
            "**Overall status:** Amber" in weekly
            and "all execution-evidence gates remain `OPEN`" in weekly
        ),
        "submission index reports the render without claiming polish-gate closure": (
            "steering deck rendered and visually reviewed" in index
            and "strict polish gate still open" in index
            and "W3_interim_steering_deck.pdf" in index
            and "W3_interim_steering_deck.pptx" in index
        ),
        "submission index lists all executive-control artifacts": all(
            path.name in index
            for name, path in REQUIRED_FILES.items()
            if name != "index"
        ),
        "submission index contains all four Week 3 model/test chains": all(
            item in index
            for item in (
                "src/week3_strategy.py",
                "src/week3_pilot_design.py",
                "tests/test_week3_operating_model.py",
                "src/week3_business_case.py",
                "tests/test_week3_executive_pack.py",
            )
        ),
        "direction spine is consistent across executive files": all(
            term in combined
            for term in (
                "federated coordination",
                "local stabilization",
                "globally coordinated",
                "all five plausible",
            )
        ),
        "current value and cost boundary is explicit across the pack": all(
            term in combined
            for term in (
                "risk exposure and value are `NOT QUANTIFIED`",
                "ROI, NPV, payback",
                "ceiling is not a cost estimate",
            )
        ),
        "no forbidden executive overclaim is present": not any(
            overclaim_hits.values()
        ),
        "registers are supplied as CSV per the consulting standards": all(
            (W3 / name).exists()
            for name in ("W3_risk_register.csv", "W3_source_log.csv", "W3_assumptions_register.csv")
        ),
        "risk register CSV is well formed and scores equal likelihood times impact": (
            csv_scores_consistent(W3 / "W3_risk_register.csv")
        ),
        "the rendered deck ships with the pack in both formats": all(
            (W3 / name).exists()
            for name in ("W3_interim_steering_deck.pdf", "W3_interim_steering_deck.pptx")
        ),
    }

    failed = []
    for name, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'} — {name}")
        if not passed:
            failed.append(name)

    for name, match in overclaim_hits.items():
        if match:
            print(f"OVERCLAIM — {name}: {match.group(0)!r}")

    if failed:
        raise SystemExit(f"{len(failed)} Week 3 executive-pack checks failed")
    print(f"All {len(checks)} Week 3 executive-pack checks passed.")


if __name__ == "__main__":
    main()
