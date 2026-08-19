#!/usr/bin/env python3
"""Validate the Week 3 interim steering deck's source-only contract."""

from __future__ import annotations

import csv
import importlib.util
import json
import re
from collections import Counter
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parent
REPO = WORKSPACE.parents[1]
MARKDOWN_SOURCE = REPO / "deliverables/working/week_3/W3_interim_steering_deck.md"

JSON_FILES = (
    "outline.json",
    "content_plan.json",
    "design_brief.json",
    "evidence_plan.json",
    "asset_plan.json",
    "style_contract.json",
)

REQUIRED_SOURCE_FILES = (
    "deliverables/working/week_2/W2_findings_log.md",
    "deliverables/working/week_2/W2_metric_contract.md",
    "data/processed/W2_visibility_diagnostic.csv",
    "data/processed/W2_liquidity_scenarios.csv",
    "data/processed/W2_payment_diagnostic.csv",
    "deliverables/working/week_3/W3_design_principles.md",
    "deliverables/working/week_3/W3_strategic_options.md",
    "deliverables/working/week_3/W3_future_state_operating_model.md",
    "deliverables/working/week_3/W3_future_state_process_map_and_RACI.md",
    "deliverables/working/week_3/W3_control_inventory.csv",
    "deliverables/working/week_3/W3_visibility_pilot_charter.md",
    "deliverables/working/week_3/W3_payment_pilot_charter.md",
    "deliverables/working/week_3/W3_business_case.md",
    "deliverables/working/week_3/W3_assumptions_register.csv",
    "data/processed/W3_option_summary.csv",
    "data/processed/W3_option_weighted_scores.csv",
    "data/processed/W3_option_sensitivity.csv",
    "data/processed/W3_visibility_pilot_candidates.csv",
    "data/processed/W3_payment_sample_frame.csv",
    "data/processed/W3_pilot_model_controls.csv",
    "data/processed/W3_business_case_scenarios.csv",
    "data/processed/W3_business_case_value_ledger.csv",
    "data/processed/W3_cost_evidence_requirements.csv",
    "data/processed/W3_business_case_controls.csv",
    "src/week3_strategy.py",
    "src/week3_pilot_design.py",
    "tests/test_week3_strategy.py",
    "tests/test_week3_pilot_design.py",
)

REQUIRED_BOUNDARIES = (
    "$38.13m",
    "$0",
    "7,600",
    "NOT QUANTIFIED",
    "ROI",
    "$1.0–$1.5m",
)


def load_json(name: str) -> dict:
    path = WORKSPACE / name
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    assert isinstance(payload, dict), f"{name}: root must be an object"
    return payload


def load_csv(relative: str) -> list[dict[str, str]]:
    with (REPO / relative).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    payloads = {name: load_json(name) for name in JSON_FILES}
    outline = payloads["outline.json"]
    content = payloads["content_plan.json"]
    evidence = payloads["evidence_plan.json"]
    assets = payloads["asset_plan.json"]
    style = payloads["style_contract.json"]

    slides = outline.get("slides")
    assert isinstance(slides, list) and len(slides) == 10, "outline must contain exactly 10 slides"
    slide_ids = [str(slide.get("slide_id") or "") for slide in slides]
    assert slide_ids == [f"s{index:02d}" for index in range(1, 11)], "slide IDs must be s01 through s10"
    assert len(set(slide_ids)) == 10, "slide IDs must be unique"

    for slide in slides:
        slide_id = slide["slide_id"]
        assert str(slide.get("title") or "").strip(), f"{slide_id}: missing claim-led title"
        assert slide.get("sources"), f"{slide_id}: missing compact sources"
        assert len(str(slide.get("notes") or "").split()) >= 35, f"{slide_id}: speaker notes are not detailed"

    planned = content.get("slide_plan")
    assert isinstance(planned, list) and len(planned) == 10, "content plan must contain exactly 10 slides"
    assert [item.get("slide_id") for item in planned] == slide_ids, "content plan and outline IDs differ"

    evidence_items = evidence.get("items")
    assert isinstance(evidence_items, list) and len(evidence_items) == 10, "evidence plan must contain 10 items"
    covered = {slide_id for item in evidence_items for slide_id in item.get("used_on_slides", [])}
    assert covered == set(slide_ids), "every slide must be covered exactly by the evidence plan"
    assert all(item.get("source_note") and item.get("boundary") for item in evidence_items), "evidence needs provenance and boundary"

    markdown = MARKDOWN_SOURCE.read_text(encoding="utf-8")
    markdown_slides = re.findall(r"^## Slide (\d+) — ", markdown, flags=re.MULTILINE)
    assert markdown_slides == [str(index) for index in range(1, 11)], "Markdown must contain exactly Slides 1–10"
    assert markdown.count("### Speaker notes") == 10, "each Markdown slide needs speaker notes"
    assert markdown.count("### Provenance") == 10, "each Markdown slide needs provenance"

    combined_source = markdown + json.dumps(outline, ensure_ascii=False)
    for boundary in REQUIRED_BOUNDARIES:
        assert boundary in combined_source, f"required boundary missing: {boundary}"

    for relative in REQUIRED_SOURCE_FILES:
        assert (REPO / relative).is_file(), f"required source file missing: {relative}"

    option_rows = load_csv("data/processed/W3_option_summary.csv")
    option_scores = {row["option_name"]: float(row["base_weighted_score_0_to_100"]) for row in option_rows}
    assert option_scores == {
        "Local stabilization": 72.0,
        "Federated coordination": 87.0,
        "Globally coordinated": 60.0,
    }, "option scores drifted from the deck"

    visibility_rows = load_csv("data/processed/W3_visibility_pilot_candidates.csv")
    assert len(visibility_rows) == 10, "visibility cohort must contain 10 accounts"
    assert all(row["control_review_required"] == "True" for row in visibility_rows), "all visibility accounts need base review"
    enhanced_ids = {row["account_id"] for row in visibility_rows if row["enhanced_control_review_required"] == "True"}
    assert enhanced_ids == {"AC0040"}, "AC0040 must be the sole enhanced-review visibility account"

    payment_rows = load_csv("data/processed/W3_payment_sample_frame.csv")
    assert len(payment_rows) == 120, "payment frame must contain 120 rows"
    assert Counter(row["priority_payment_cohort"] for row in payment_rows) == {
        "Manual touch only": 30,
        "Manual touch + cross-border wire": 30,
        "Cross-border wire only": 30,
        "Neither priority cohort": 30,
    }, "payment strata must contain 30 records each"
    assert Counter(row["sample_role"] for row in payment_rows) == {
        "Issue case": 60,
        "Non-issue control": 60,
    }, "payment frame must contain 60 cases and 60 controls"
    pairs: dict[str, int] = {}
    for row in payment_rows:
        pairs[row["case_control_pair_id"]] = int(row["match_deviation_count"])
    assert len(pairs) == 60, "payment frame must contain 60 unique matched pairs"
    assert Counter(pairs.values()) == {0: 50, 1: 10}, "payment matching must remain 50 exact / 10 deviations"

    value_rows = load_csv("data/processed/W3_business_case_value_ledger.csv")
    assert len(value_rows) == 12, "business-case ledger must contain 3 scenarios x 4 categories"
    assert all(
        row["validated_value_usd"] == row["funded_value_usd"] == row["recognized_value_usd"] == "0"
        for row in value_rows
    ), "all current validated, funded, and recognized value must remain zero"
    assert all(
        row["diagnostic_quantity"] == "NOT QUANTIFIED"
        for row in value_rows
        if row["value_category"] == "risk"
    ), "risk exposure and value must remain NOT QUANTIFIED"

    cost_rows = load_csv("data/processed/W3_cost_evidence_requirements.csv")
    assert {row["cost_requirement_id"] for row in cost_rows} == {f"CR{index:02d}" for index in range(1, 11)}, "CR01–CR10 must remain complete"

    assert style.get("format", {}).get("aspect_ratio") == "16:9", "style contract must be 16:9"
    assert style.get("format", {}).get("slide_count") == 10, "style contract must lock 10 slides"
    assert style.get("composition", {}).get("page_system") == "board-ledger", "page system must be board-ledger"

    remote_text = json.dumps(assets, ensure_ascii=False)
    assert "http://" not in remote_text and "https://" not in remote_text, "external asset URLs are prohibited"
    assert not assets.get("images") and not assets.get("generated_images"), "external/generated imagery is prohibited"

    renderer_status = "available" if importlib.util.find_spec("pptx") else "blocked: python-pptx unavailable"
    print("PASS: 6 JSON files parsed")
    print("PASS: exactly 10 sourced slides with detailed notes")
    print("PASS: content, evidence, Markdown, style, and source-file contracts align")
    print("PASS: option, pilot, value-ledger, and cost evidence reconcile to deck claims")
    print("PASS: no external or generated imagery")
    print(f"INFO: renderer dependency {renderer_status}")


if __name__ == "__main__":
    main()
