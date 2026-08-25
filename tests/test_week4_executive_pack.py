#!/usr/bin/env python3
"""Fail-closed completeness and approval-boundary checks for the final pack."""

import csv
import json
import re
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "deliverables" / "final"
W4 = ROOT / "deliverables" / "working" / "week_4"


def require(path: Path) -> str:
    assert path.exists(), f"missing required deliverable: {path.relative_to(ROOT)}"
    assert path.stat().st_size > 0, f"empty required deliverable: {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8") if path.suffix in {".md", ".csv"} else ""


def pptx_slide_count(path: Path) -> int:
    """Count slides from the presentation manifest without PowerPoint dependencies."""
    with ZipFile(path) as archive:
        presentation = ElementTree.fromstring(archive.read("ppt/presentation.xml"))
    namespace = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
    return len(presentation.findall(".//p:sldId", namespace))


def pdf_page_count(path: Path) -> int:
    """Count page objects without requiring a third-party PDF package."""
    return len(re.findall(rb"/Type\s*/Page\b", path.read_bytes()))


def main() -> None:
    final_files = [
        "FINAL_SUBMISSION_INDEX.md",
        "Northstar_Final_Executive_Deck.md",
        "Northstar_Final_Executive_Deck.pdf",
        "Northstar_Final_Executive_Deck.pptx",
        "Northstar_Final_Recommendation_Memo.md",
        "Northstar_Final_Recommendation_Memo.pdf",
        "Northstar_Implementation_Roadmap.md",
        "Northstar_Initiative_Charters.md",
        "Northstar_Governance_and_RACI.md",
        "Northstar_KPI_and_Benefits_Framework.md",
        "Northstar_Benefits_Tracking_Dashboard.md",
        "Northstar_Final_QA_Log.md",
        "Northstar_Personal_Reflection.md",
        "Northstar_Final_Evidence_Register.md",
        "Northstar_Final_Completeness_Checklist.md",
    ]
    working_files = [
        "W4_workplan.md",
        "W4_weekly_update.md",
        "W4_findings_log.md",
        "W4_decision_log.md",
        "W4_analysis_log.md",
        "W4_assumptions_register.csv",
        "W4_risk_register.csv",
        "W4_risk_register.md",
        "W4_source_log.csv",
        "W4_submission_index.md",
    ]
    corpus = "\n".join(require(FINAL / name) for name in final_files)
    deck_pptx = FINAL / "Northstar_Final_Executive_Deck.pptx"
    deck_pdf = FINAL / "Northstar_Final_Executive_Deck.pdf"
    memo_pdf = FINAL / "Northstar_Final_Recommendation_Memo.pdf"
    outline = json.loads((ROOT / "deliverables" / "final" / "Northstar_Final_Executive_Deck_outline.json").read_text(encoding="utf-8"))
    slide_ids = [slide["slide_id"] for slide in outline["slides"]]
    assert slide_ids == [f"s{i:02d}" for i in range(1, 16)] + [f"a{i:02d}" for i in range(1, 5)]
    assert pptx_slide_count(deck_pptx) == len(slide_ids) == 19, "final deck must contain 15 core plus 4 appendix slides"
    assert pdf_page_count(deck_pdf) == 19, "final deck PDF must match the 19-slide PPTX"
    memo_pages = pdf_page_count(memo_pdf)
    assert 1 <= memo_pages <= 6, "final recommendation memo must not exceed six pages"
    assert f"{memo_pages} A4 pages" in corpus, "memo page-count evidence must match the PDF"
    assert "19 slides total — 15 core slides (the rubric cap) plus a 4-slide appendix" in corpus
    for name in working_files:
        require(W4 / name)

    appendix = "\n".join(
        json.dumps(slide, ensure_ascii=False) for slide in outline["slides"] if slide["slide_id"].startswith("a")
    ).lower()
    for phrase in (
        "definitions",
        "data quality",
        "method",
        "detailed analys",
        "source",
        "assumption",
        "sensitiv",
        "rejected alternative",
        "program-standard",
    ):
        assert phrase in appendix, f"missing required appendix category: {phrase}"

    dashboard = require(FINAL / "Northstar_Benefits_Tracking_Dashboard.md")
    for phrase in ("B01", "B02", "B03", "B04", "0 of 22", "non-additive"):
        assert phrase.lower() in dashboard.lower(), f"missing benefits-dashboard control: {phrase}"

    charters = require(FINAL / "Northstar_Initiative_Charters.md")
    assert charters.count("**Prerequisites / dependencies:**") == 7

    with (W4 / "W4_source_log.csv").open(encoding="utf-8", newline="") as handle:
        source_rows = list(csv.DictReader(handle))
    assert all(row["evidence_label"] == "PROGRAM-STANDARD" for row in source_rows if row["source_type"] == "Program")
    allowed_labels = {
        "PROGRAM-STANDARD",
        "ACG-DATA",
        "ANALYST-CALC",
        "ANALYST-ASSUMPTION",
        "ANALYST-JUDGMENT",
        "JPM-PUBLIC",
    }
    assert all(
        set(row["evidence_label"].split(" / ")) <= allowed_labels for row in source_rows
    ), "Week 4 source log contains an undefined evidence label"
    logged_paths = {row["source_path_or_title"] for row in source_rows}
    assert {
        "data/processed/W4_initiative_portfolio.csv",
        "data/processed/W4_stage_gates.csv",
        "data/processed/W4_roadmap_milestones.csv",
        "data/processed/W4_kpi_dictionary.csv",
        "data/processed/W4_benefits_tracker.csv",
    } <= logged_paths

    for week in range(1, 5):
        require(ROOT / "deliverables" / "working" / f"week_{week}" / f"W{week}_weekly_update.md")

    for phrase in (
        "90-day evidence mobilization",
        "local stabilization",
        "recognized cash, annual P&L, and capacity value is `$0`",
        "no production",
    ):
        assert phrase.lower() in corpus.lower(), f"missing final-pack boundary: {phrase}"

    for forbidden in ("[insert", "lorem ipsum", "xxxx"):
        assert forbidden not in corpus.lower(), f"placeholder text detected: {forbidden}"

    print("Week 4 executive pack completeness: PASS")


if __name__ == "__main__":
    main()
