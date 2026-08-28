"""Structural and integration checks for the interactive dashboard UI."""

import functools
import hashlib
import http.server
import json
import re
import struct
import subprocess
import sys
import threading
import unittest
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from build_dashboard_data import build_dashboard_data, load_dashboard_inputs  # noqa: E402


DASHBOARD = ROOT / "docs" / "dashboard"


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags = []
        self.ids = []
        self.html_attrs = {}
        self.details = []
        self.summaries = []
        self.inline_details = []
        self.inline_summaries = []
        self.detail_topic_stack = []
        self.ids_by_inline_detail = {}
        self.figures = []
        self.canvases = []
        self.summary_depth = 0
        self.ids_in_summaries = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        self.tags.append((tag, values))
        if tag == "html":
            self.html_attrs = values
        if tag == "details":
            self.details.append(values)
            topic = values.get("data-inline-detail")
            inherited_topic = self.detail_topic_stack[-1] if self.detail_topic_stack else None
            self.detail_topic_stack.append(topic or inherited_topic)
            if topic:
                self.inline_details.append(values)
                self.ids_by_inline_detail.setdefault(topic, set())
        if tag == "summary":
            self.summaries.append(values)
            if "data-detail-summary" in values:
                self.inline_summaries.append(values)
            self.summary_depth += 1
        if tag == "figure":
            self.figures.append(values)
        if tag == "canvas":
            self.canvases.append(values)
        if "id" in values:
            self.ids.append(values["id"])
            if self.summary_depth:
                self.ids_in_summaries.add(values["id"])
            if self.detail_topic_stack and self.detail_topic_stack[-1]:
                self.ids_by_inline_detail.setdefault(
                    self.detail_topic_stack[-1], set()
                ).add(values["id"])

    def handle_endtag(self, tag):
        if tag == "summary":
            self.summary_depth -= 1
        if tag == "details":
            self.detail_topic_stack.pop()


class DashboardUiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.index = (DASHBOARD / "index.html").read_text(encoding="utf-8")
        cls.styles = (DASHBOARD / "styles.css").read_text(encoding="utf-8")
        cls.script = (DASHBOARD / "app.js").read_text(encoding="utf-8")
        cls.payload = json.loads(
            (DASHBOARD / "dashboard_data.json").read_text(encoding="utf-8")
        )
        cls.parser = StructureParser()
        cls.parser.feed(cls.index)

    def test_generated_json_matches_governed_adapter(self) -> None:
        frames = load_dashboard_inputs(ROOT / "data" / "processed")
        self.assertEqual(self.payload, build_dashboard_data(frames))
        self.assertEqual(self.payload["schema_version"], "2.0")
        self.assertIsNone(
            self.payload["liquidity"]["validated_mobility"]["value_usd"]
        )
        self.assertEqual(
            self.payload["liquidity"]["validated_mobility"]["status"],
            "not_established",
        )

    def test_html_has_accessible_landmarks_and_unique_ids(self) -> None:
        self.assertEqual(self.parser.html_attrs.get("lang"), "en")
        self.assertEqual(sum(tag == "main" for tag, _ in self.parser.tags), 1)
        self.assertEqual(sum(tag == "h1" for tag, _ in self.parser.tags), 1)
        # Two modals: the metric-guide drawer and the guided-review wizard.
        self.assertEqual(sum(tag == "dialog" for tag, _ in self.parser.tags), 2)
        self.assertEqual(len(self.parser.ids), len(set(self.parser.ids)))
        required_ids = {
            "dashboard-menu-hub",
            "dashboard-menu-title",
            "selected-view-header",
            "selected-view-title",
            "selected-view-description",
            "all-views-button",
            "signals",
            "filter-toolbar",
            "visibility-kpi",
            "funded-case-value",
            "payment-kpi",
            "regional-kpi",
            "evidence-dialog",
            "drawer-close",
            "dashboard-announcer",
            "panel-overview",
            "panel-visibility",
            "panel-liquidity",
            "panel-payments",
            "panel-regions",
            "panel-gates",
            "panel-quality",
            "dashboard-search",
            "dashboard-search-results",
            "filter-trigger",
            "filter-panel",
            "filter-form",
            "filter-date-from",
            "filter-date-to",
            "filter-currency",
            "filter-region",
            "filter-entity",
            "filter-bank",
            "filter-validation",
            "filter-empty-state",
            "active-filter-chips",
            "capacity-filter-note",
            "detail-decision",
            "detail-visibility",
            "detail-liquidity",
            "detail-payments",
            "detail-regions",
            "detail-capacity",
            "detail-closures",
            "visibility-summary-boundary",
            "liquidity-summary-boundary",
            "liquidity-summary-screen",
            "payment-summary-boundary",
            "regional-summary-boundary",
            "closure-summary-boundary",
            "decision-evidence-chips",
            "decision-composite-note",
            "visibility-ring",
            "visibility-source-bars",
            "visibility-action-insight",
            "liquidity-waterfall",
            "liquidity-trend-canvas",
            "liquidity-trend-table",
            "liquidity-trend-table-body",
            "payment-ring",
            "payment-cohort-stack",
            "payment-cohort-legend",
            "regional-map-base",
            "regional-map-markers",
            "regional-map-empty",
            "regional-evidence-table",
            "regional-evidence-table-body",
            "regional-all-button",
            "capacity-comparison-bars",
            "closure-candidate-table",
            "closure-candidate-table-body",
            "quality-view",
            "quality-view-title",
            "quality-status",
            "quality-certification",
            "quality-w1-checks",
            "quality-w2-controls",
            "quality-source-artifacts",
            "quality-monitoring-title",
            "quality-monitoring-status",
            "quality-monitoring-period",
            "quality-monitoring-boundary",
            "quality-dimensions-note",
            "quality-dimension-list",
            "quality-population-disclosure",
            "quality-population-controls",
            "quality-issues-disclosure",
            "quality-issue-summary",
            "quality-issue-list",
            "quality-issue-source",
            "quality-boundary",
            "quality-next-action",
            "quality-methodology-disclosure",
        }
        self.assertTrue(required_ids.issubset(self.parser.ids))
        self.assertIn('name="viewport"', self.index)
        self.assertIn("<noscript>", self.index)
        self.assertIn('aria-live="polite"', self.index)

    def test_filter_and_search_controls_are_accessible_and_ordered(self) -> None:
        tags_by_id = {
            attrs["id"]: (tag, attrs)
            for tag, attrs in self.parser.tags
            if "id" in attrs
        }
        search_tag, search = tags_by_id["dashboard-search"]
        self.assertEqual(search_tag, "input")
        self.assertEqual(search.get("type"), "search")
        self.assertEqual(search.get("role"), "combobox")
        self.assertEqual(search.get("aria-autocomplete"), "list")
        self.assertEqual(search.get("aria-controls"), "dashboard-search-results")
        self.assertEqual(search.get("placeholder"), "Search metrics, entities, banks…")

        trigger_tag, trigger = tags_by_id["filter-trigger"]
        self.assertEqual(trigger_tag, "button")
        self.assertEqual(trigger.get("aria-expanded"), "false")
        self.assertEqual(trigger.get("aria-controls"), "filter-panel")
        self.assertIn("data-toggle-filters", trigger)

        self.assertEqual(tags_by_id["filter-date-from"][1].get("type"), "date")
        self.assertEqual(tags_by_id["filter-date-to"][1].get("type"), "date")
        for control_id in (
            "filter-currency",
            "filter-region",
            "filter-entity",
            "filter-bank",
        ):
            self.assertEqual(tags_by_id[control_id][0], "select")

        model_script = '<script src="filter_model.js" defer></script>'
        app_script = '<script src="app.js" defer></script>'
        self.assertIn(model_script, self.index)
        self.assertLess(self.index.index(model_script), self.index.index(app_script))

    def test_filters_remain_visible_and_navigation_does_not_recalculate_scope(self) -> None:
        sync = self.script.split("function syncDashboardViewVisibility", 1)[1].split(
            "function selectDashboardView", 1
        )[0]
        self.assertIn(
            "filterToolbar.hidden = !dashboardData;",
            sync,
        )
        apply_candidate = self.script.split("function applyFilterCandidate", 1)[1].split(
            "function removeAppliedFilter", 1
        )[0]
        self.assertNotIn("activeDashboardView =", apply_candidate)
        choose_search = self.script.split("function chooseSearchResult", 1)[1].split(
            "function updateResetState", 1
        )[0]
        dimension_branch = choose_search.split('if (entry.kind === "dimension")', 1)[1]
        self.assertNotIn("activeDashboardView =", dimension_branch)

    def test_menu_first_body_maps_seven_views_to_seven_native_disclosures(self) -> None:
        expected_mapping = {
            "decision": "executive",
            "visibility": "cash",
            "liquidity": "cash",
            "regions": "footprint",
            "closures": "footprint",
            "payments": "payments",
            "capacity": "workload",
        }
        expected_topics = set(expected_mapping)
        self.assertEqual(len(self.parser.inline_details), 7)
        self.assertEqual(len(self.parser.inline_summaries), 7)
        self.assertEqual(
            {details.get("data-inline-detail") for details in self.parser.inline_details},
            expected_topics,
        )
        self.assertTrue(
            all(details.get("name") == "dashboard-detail" for details in self.parser.inline_details)
        )
        self.assertTrue(all("open" not in details for details in self.parser.inline_details))
        self.assertTrue(all("hidden" in details for details in self.parser.inline_details))
        self.assertEqual(
            {
                details["data-inline-detail"]: details.get("data-dashboard-view")
                for details in self.parser.inline_details
            },
            expected_mapping,
        )
        self.assertEqual(
            {summary.get("data-detail-summary") for summary in self.parser.inline_summaries},
            expected_topics,
        )
        self.assertTrue(all("role" not in summary for summary in self.parser.inline_summaries))
        self.assertTrue(
            all("aria-expanded" not in summary for summary in self.parser.inline_summaries)
        )
        visible_qualifier_ids = {
            "decision-title",
            "visibility-kpi",
            "visibility-summary-boundary",
            "funded-case-value",
            "liquidity-summary-boundary",
            "liquidity-summary-screen",
            "mobility-status",
            "payment-kpi",
            "payment-summary-boundary",
            "regional-kpi",
            "regional-summary-boundary",
            "regional-summary-context",
            "regional-selection-status",
            "capacity-filter-note",
            "capacity-summary",
            "closure-summary",
            "closure-summary-boundary",
        }
        self.assertTrue(visible_qualifier_ids.issubset(self.parser.ids_in_summaries))
        self.assertNotIn("signal-grid", self.index)
        self.assertNotIn("signal-card", self.index)
        self.assertIn(".operation-list", self.styles)
        self.assertIn(".operation-row > summary", self.styles)

        menu_buttons = [
            (tag, attrs)
            for tag, attrs in self.parser.tags
            if "data-select-dashboard-view" in attrs
        ]
        expected_controls = {
            "executive": "detail-decision",
            "cash": "detail-visibility detail-liquidity",
            "footprint": "detail-regions detail-closures",
            "payments": "detail-payments",
            "workload": "detail-capacity",
            "evidence": "quality-view",
            "roadmap": "roadmap-view",
        }
        self.assertEqual(len(menu_buttons), 7)
        self.assertEqual(
            {attrs["data-select-dashboard-view"]: attrs.get("aria-controls") for _, attrs in menu_buttons},
            expected_controls,
        )
        self.assertTrue(all(tag == "button" for tag, _ in menu_buttons))
        self.assertTrue(all("aria-pressed" not in attrs for _, attrs in menu_buttons))
        self.assertTrue(all("aria-current" not in attrs for _, attrs in menu_buttons))
        self.assertTrue(all("disabled" in attrs for _, attrs in menu_buttons))
        self.assertTrue(all("role" not in attrs for _, attrs in menu_buttons))
        for label in (
            "Executive Overview",
            "Cash Visibility &amp; Liquidity",
            "Bank Account Footprint",
            "Payment Operations",
            "Process Workload",
            "Data Quality &amp; Evidence",
            "Decision &amp; Roadmap",
        ):
            self.assertIn(label, self.index)
        for description in (
            "Portfolio decision and the validation needed before funding or execution.",
            "Reporting delays and governed 7-day and 14-day screening sensitivities.",
            "Regional account coverage and closure-validation candidates.",
            "Deduplicated payment cohorts, exceptions, and repair time.",
            "Independent management and payment-file workload estimates.",
            "Structural checks, reconciliation controls, source artifacts, and open certification limits.",
        ):
            self.assertIn(description, self.index)
        tags_by_id = {
            attrs["id"]: attrs for _, attrs in self.parser.tags if "id" in attrs
        }
        self.assertNotIn("hidden", tags_by_id["dashboard-menu-hub"])
        self.assertIn("hidden", tags_by_id["signals"])
        self.assertIn("hidden", tags_by_id["selected-view-header"])
        self.assertIn("hidden", tags_by_id["quality-view"])
        self.assertIn("hidden", tags_by_id["filter-toolbar"])

        footer = self.index.split('id="evidence-footer"', 1)[1].split("</footer>", 1)[0]
        self.assertNotIn("<button", footer)

    def test_menu_page_pairs_governed_findings_with_the_menu_and_fails_closed(self) -> None:
        tags_by_id = {attrs["id"]: attrs for _, attrs in self.parser.tags if "id" in attrs}
        required_ids = {
            "menu-page",
            "menu-decision-headline",
            "menu-decision-next",
            "menu-decision-confidence",
            "menu-findings",
            "menu-actions-title",
            "menu-findings-scope",
            "menu-stat-visibility",
            "menu-stat-liquidity",
            "menu-stat-payments",
            "menu-next-actions",
            "start-guided-review",
        }
        self.assertTrue(required_ids.issubset(tags_by_id))

        # The simplified homepage carries exactly three KPIs. The former fourth
        # KPI and the four finding cards now live on the secondary detail pages,
        # so the homepage summarizes instead of presenting everything at once.
        self.assertEqual(self.index.count('class="menu-stat menu-stat-'), 3)
        for removed in (
            "menu-stat-quality",
            "menu-finding-grid",
            "menu-finding-payments-bars",
            "menu-finding-liquidity-bars",
            "menu-finding-visibility-bars",
            "menu-finding-value-gates",
        ):
            self.assertNotIn(removed, self.index)

        # Exactly three next actions, each derived from a governed definition.
        self.assertIn(
            'const NEXT_ACTION_TOPICS = Object.freeze(["visibility", "liquidity", "payments"]);',
            self.script,
        )

        # The menu stays the routing spine and is still the only view selector.
        self.assertNotIn("hidden", tags_by_id["dashboard-menu-hub"])
        self.assertNotIn("hidden", tags_by_id["menu-page"])
        self.assertEqual(
            sum("data-select-dashboard-view" in attrs for _, attrs in self.parser.tags), 7
        )

        # Findings are declared portfolio-wide and never imply a composite score.
        self.assertIn("portfolio-wide · filters do not apply", self.script)
        self.assertIn("Three separate signals—not a composite score.", self.index)

        # The three signals are shown once, as the KPI strip. Repeating them in
        # the band and again under each action made the page read as three
        # copies of the same evidence.
        self.assertNotIn("menu-decision-signals", self.index)
        self.assertNotIn("menu-action-context", self.script)

        # Each block states what it is, so the three groups are self-evident.
        for label in (
            "The three measures behind the recommendation",
            "Three next actions",
            "Primary recommendation",
        ):
            self.assertIn(label, self.index)
        self.assertNotIn("What the supplied data shows", self.index)

        # Evidence on the menu page is hidden until the governed contract validates.
        evidence_sections = [
            attrs for _, attrs in self.parser.tags if "data-menu-evidence" in attrs
        ]
        self.assertEqual(len(evidence_sections), 2)
        sync = self.script.split("function syncDashboardViewVisibility", 1)[1].split(
            "function selectDashboardView", 1
        )[0]
        self.assertIn("if (menuPage) menuPage.hidden = Boolean(activeConfig) || detailPageOpen;", sync)
        self.assertIn("node.hidden = !dashboardData;", sync)

        # Every headline number is read from the governed contract, never hard-coded.
        findings = self.script.split("function renderMenuFindings", 1)[1].split(
            "function renderHeader", 1
        )[0]
        for source in (
            "dashboardData.visibility",
            "dashboardData.payments",
            "dashboardData.decision",
            "liquidity.evidence_ladder",
            "dashboardData.guardrails",
            "quality.w1_checks",
            "quality.w2_controls",
        ):
            self.assertIn(source, findings)
        self.assertIn("replaceChildren", findings)
        # Threshold scenarios moved off the homepage with the findings cards,
        # but must still be read from the contract by the liquidity view.
        self.assertIn("liquidity.scenarios", self.script)

        # Next-action text comes from the contract, not from literals in the page.
        self.assertIn("definition.next_action", findings)

        for token in (
            ".menu-page",
            ".menu-decision-band",
            ".menu-stat-strip",
            ".menu-next-actions",
            ".menu-bar-fill",
            "grid-template-columns: repeat(3, minmax(0, 1fr));",
            "@media (max-width: 1180px)",
        ):
            self.assertIn(token, self.styles)

    def test_menu_hub_is_dark_row_based_and_mobile_safe(self) -> None:
        required_css = (
            ".dashboard-menu-hub",
            "background: var(--analytics-deep);",
            ".dashboard-view-menu li + li",
            ".dashboard-view-menu button",
            "grid-template-columns: 48px minmax(0, 1fr) 32px;",
            "@media (max-width: 440px)",
            "grid-template-columns: 32px minmax(0, 1fr) 20px;",
            ".selected-view-header",
            ".quality-control-grid",
            ".quality-guide-grid",
            ".quality-next-action",
        )
        for token in required_css:
            self.assertIn(token, self.styles)
        self.assertNotIn('role="menu"', self.index)

    def test_interactions_use_native_controls_and_explicit_state(self) -> None:
        openers = [
            (tag, attrs)
            for tag, attrs in self.parser.tags
            if "data-open-drawer" in attrs
        ]
        self.assertGreaterEqual(len(openers), 7)
        self.assertTrue(all(tag == "button" for tag, _ in openers))
        self.assertIn('name="liquidity-days"', self.index)
        self.assertIn('name="payment-measure"', self.index)
        self.assertIn('value="records"', self.index)
        self.assertIn('value="exceptions"', self.index)
        self.assertIn('value="repair_minutes"', self.index)
        self.assertIn("showModal()", self.script)
        self.assertIn("ArrowRight", self.script)
        self.assertIn("ArrowLeft", self.script)
        self.assertIn("lastDrawerOpener", self.script)
        self.assertIn("lastFilterOpener", self.script)
        self.assertIn("draftFilters", self.script)
        self.assertIn("appliedFilters", self.script)
        self.assertIn("FilterModel.validateState", self.script)
        self.assertIn("FilterModel.summarize", self.script)

    def test_quality_landing_uses_governed_dimensions_and_progressive_disclosure(self) -> None:
        quality = self.payload["quality"]
        self.assertEqual(quality["w1_checks"], {
            "label": "Week 1 structural checks",
            "passed": 52,
            "total": 52,
        })
        self.assertEqual(quality["w2_controls"], {
            "label": "Week 2 reconciliation controls",
            "reconciled": 13,
            "total": 13,
        })
        self.assertEqual(quality["source_artifacts"], 12)
        self.assertEqual(len(quality["population_controls"]), 6)
        self.assertEqual(len(quality["dimensions"]), 7)
        self.assertEqual(sum(row["measured_rules"] for row in quality["dimensions"]), 52)
        self.assertEqual(quality["monitoring"]["status"], "baseline_only")
        self.assertEqual(quality["monitoring"]["snapshots"], 1)
        self.assertEqual(len(quality["issue_queue"]), 15)
        self.assertEqual(
            {severity: sum(issue["severity"] == severity for issue in quality["issue_queue"])
             for severity in ("High", "Medium")},
            {"High": 11, "Medium": 4},
        )
        self.assertIn("does not certify source completeness", quality["decision_boundary"])
        self.assertIn(
            "Complete source-owner certification",
            self.payload["definitions"]["quality"]["next_action"],
        )

        quality_section = self.index.split('id="quality-view"', 1)[1].split(
            "</section>\n\n        <footer", 1
        )[0]
        self.assertIn("<details", quality_section)
        self.assertIn('id="quality-population-disclosure"', quality_section)
        self.assertIn('id="quality-issues-disclosure"', quality_section)
        self.assertIn('id="quality-methodology-disclosure"', quality_section)
        self.assertNotIn('id="quality-population-disclosure" open', quality_section)
        self.assertNotIn('id="quality-issues-disclosure" open', quality_section)
        self.assertNotIn('id="quality-methodology-disclosure" open', quality_section)
        self.assertIn(
            "Coverage labels describe available evidence—not performance, certification, or a composite data-quality score.",
            quality_section,
        )
        for topic in (
            "overview", "visibility", "liquidity", "payments", "regions", "gates", "quality"
        ):
            self.assertIn(f'data-open-drawer="{topic}"', quality_section)
        quality_openers = {
            attrs["data-open-drawer"]
            for tag, attrs in self.parser.tags
            if tag == "button" and "data-open-drawer" in attrs
            and attrs["data-open-drawer"] in {
                "overview", "visibility", "liquidity", "payments", "regions", "gates", "quality"
            }
        }
        self.assertEqual(
            quality_openers,
            {"overview", "visibility", "liquidity", "payments", "regions", "gates", "quality"},
        )
        self.assertIn("Open data-quality method", quality_section)
        required_runtime = (
            "function renderQualityLanding()",
            "dashboardData.quality",
            "quality.w1_checks.passed",
            "quality.w2_controls.reconciled",
            "quality.source_artifacts",
            "quality.population_controls.forEach",
            "function renderQualityDimensions(quality)",
            "function renderQualityIssueQueue(quality)",
            "function openQualityDimension",
            "function openQualityIssue",
            "quality.monitoring.label",
            "quality.issue_queue",
            "quality.decision_boundary",
            "dashboardData.definitions.quality.next_action",
            'renderQualityLanding();',
        )
        for token in required_runtime:
            self.assertIn(token, self.script)
        self.assertIn('data-tab="quality"', self.index)
        self.assertIn('id="panel-quality"', self.index)
        self.assertNotIn("quality scorecard", quality_section.lower())
        self.assertNotIn("pass rate", quality_section.lower())
        for selector in (
            ".quality-dimension > summary:focus-visible",
            ".quality-issue > summary:focus-visible",
            ".quality-support-disclosure > summary:focus-visible",
            ".quality-rule-disclosure > summary:focus-visible",
        ):
            self.assertIn(selector, self.styles)
        self.assertIn('chevron.setAttribute("aria-hidden", "true")', self.script)
        mobile_css = self.styles.split("@media (max-width: 760px)", 1)[1].split(
            "@media (max-width: 440px)", 1
        )[0]
        self.assertIn(
            ".quality-dimension > summary {\n    grid-template-columns: minmax(0, 1fr) auto 22px;",
            mobile_css,
        )

    def test_reference_visuals_live_only_in_expanded_sections(self) -> None:
        expected_hooks = {
            "decision": {
                "decision-evidence-chips",
                "decision-visibility-chip",
                "decision-liquidity-chip",
                "decision-payments-chip",
                "decision-composite-note",
            },
            "visibility": {
                "visibility-ring",
                "visibility-ring-value",
                "visibility-source-bars",
                "visibility-source-empty",
            },
            "liquidity": {
                "liquidity-waterfall",
                "liquidity-waterfall-empty",
                "liquidity-trend-canvas",
                "liquidity-trend-table",
                "liquidity-trend-table-body",
            },
            "payments": {
                "payment-ring",
                "payment-ring-value",
                "payment-cohort-stack",
                "payment-cohort-legend",
                "payment-cohort-empty",
            },
            "regions": {
                "regional-map-base",
                "regional-map-markers",
                "regional-map-empty",
                "regional-evidence-table",
                "regional-evidence-table-body",
                "regional-all-button",
            },
            "capacity": {"capacity-comparison-bars"},
            "closures": {
                "closure-candidate-table",
                "closure-candidate-table-body",
                "closure-candidate-empty",
            },
        }
        for topic, hooks in expected_hooks.items():
            self.assertTrue(hooks.issubset(self.parser.ids_by_inline_detail[topic]))
            self.assertTrue(hooks.isdisjoint(self.parser.ids_in_summaries))

        self.assertEqual(len(self.parser.canvases), 1)
        canvas = self.parser.canvases[0]
        self.assertEqual(canvas.get("id"), "liquidity-trend-canvas")
        self.assertEqual(canvas.get("role"), "img")
        self.assertTrue(canvas.get("aria-label"))
        self.assertIn("View trend data table", self.index)
        self.assertIn("<caption>", self.index)
        self.assertEqual(self.index.count("Definition, formula &amp; source"), 8)
        self.assertIn("Separate signals—not a composite score.", self.index)
        self.assertIn(".analytics-card", self.styles)
        self.assertIn("background: var(--analytics);", self.styles)
        self.assertIn(".composition-ring", self.styles)
        self.assertIn(".cohort-stack", self.styles)
        self.assertIn(".waterfall-list", self.styles)
        self.assertIn(".regional-map-stage", self.styles)

    def test_regional_map_uses_a_local_public_domain_asset_and_semantic_controls(self) -> None:
        tags_by_id = {
            attrs["id"]: (tag, attrs)
            for tag, attrs in self.parser.tags
            if "id" in attrs
        }
        image_tag, image = tags_by_id["regional-map-base"]
        self.assertEqual(image_tag, "img")
        self.assertEqual(image.get("src"), "assets/world-map.png")
        self.assertEqual(image.get("alt"), "")
        self.assertEqual(image.get("aria-hidden"), "true")
        self.assertEqual(image.get("width"), "1280")
        self.assertEqual(image.get("height"), "650")
        self.assertNotIn("http", image.get("src", ""))

        asset = DASHBOARD / "assets" / "world-map.png"
        contents = asset.read_bytes()
        self.assertEqual(contents[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(contents[12:16], b"IHDR")
        self.assertEqual(struct.unpack(">II", contents[16:24]), (1280, 650))
        self.assertEqual(
            hashlib.sha256(contents).hexdigest(),
            "7097dc120bc4c45f15e1a116e2fd4b5b72dd84e45bec10063edd5fa5439e2154",
        )

        marker_tag, marker_group = tags_by_id["regional-map-markers"]
        self.assertEqual(marker_tag, "div")
        self.assertEqual(marker_group.get("role"), "group")
        self.assertIn("Filter dashboard by region", marker_group.get("aria-label", ""))
        table_tag, _ = tags_by_id["regional-evidence-table"]
        self.assertEqual(table_tag, "table")
        self.assertIn(
            "Regional diagnostic comparison within the current non-region filters",
            self.index,
        )
        self.assertIn("Schematic account coverage · supplied diagnostics · not a live cash map", self.index)
        self.assertIn("Schematic region positions—not bank, account, cash, legal-domicile, or transfer-path locations", self.index)

    def test_disclosure_keyboard_search_reset_and_failure_behaviors_are_explicit(self) -> None:
        required = (
            "selectDashboardView",
            "showAllDashboardViews",
            "syncDashboardViewVisibility",
            "visibleDetailSummaries",
            'state.activeDashboardView = null',
            "filterToolbar.hidden = !dashboardData",
            'activeView === "evidence"',
            'detail.addEventListener("toggle"',
            "closeAllInlineDetails({ except: detail })",
            'event.key === "ArrowDown"',
            'event.key === "ArrowUp"',
            'event.key === "Home"',
            'event.key === "End"',
            'event.key === "Escape"',
            "detail.open = false",
            "closeAllInlineDetails();",
            'entry.id.startsWith("inline:")',
            "openInlineDetail",
            'entry.id.startsWith("guide:")',
            'entry.id.startsWith("view:")',
            "detail.hidden = !visible",
        )
        for token in required:
            self.assertIn(token, self.script)
        self.assertIn("const nestedDetailOpen", self.script)
        self.assertIn('getAll(".trend-data-disclosure")', self.script)
        self.assertIn("const detailSummaries = visibleDetailSummaries();", self.script)
        self.assertIn("state.activeDashboardView === DEFAULT_VIEW.activeDashboardView", self.script)
        self.assertIn(".trend-data-disclosure > summary:focus-visible", self.styles)
        self.assertNotIn('summary.setAttribute("aria-expanded"', self.script)
        self.assertNotIn('summary.addEventListener("click"', self.script)

    def test_menu_selection_focus_reset_and_failure_are_fail_closed(self) -> None:
        selector = self.script.split("function selectDashboardView", 1)[1].split(
            "function showAllDashboardViews", 1
        )[0]
        self.assertIn("closeAllInlineDetails();", selector)
        self.assertIn("collapseNestedDetails();", selector)
        self.assertIn("state.activeDashboardView = view;", selector)
        self.assertIn('get("#selected-view-title").focus()', selector)
        self.assertNotIn("detail.open = true", selector)
        self.assertIn('view === "evidence"', selector)

        inline_open = self.script.split("function openInlineDetail", 1)[1].split(
            "function setCompositionRing", 1
        )[0]
        self.assertIn("dashboardViewForTopic(topic)", inline_open)
        self.assertIn("selectDashboardView(owningView", inline_open)
        self.assertIn("detail.open = true", inline_open)

        reset = self.script.split("function resetView", 1)[1].split(
            "function metricSearchDefinitions", 1
        )[0]
        self.assertIn("state.activeDashboardView = DEFAULT_VIEW.activeDashboardView;", reset)
        self.assertIn("dialog.close();", reset)
        self.assertIn('get("[data-select-dashboard-view]")', reset)

        disabled = self.script.split("function setDataControlsDisabled", 1)[1].split(
            "function setKpiEmpty", 1
        )[0]
        self.assertIn("state.activeDashboardView = null;", disabled)
        self.assertIn("syncDashboardViewVisibility();", disabled)

        all_views = self.script.split("function showAllDashboardViews", 1)[1].split(
            "function setDataControlsDisabled", 1
        )[0]
        self.assertIn("const previousView = state.activeDashboardView;", all_views)
        self.assertIn('data-select-dashboard-view="${previousView}"', all_views)

        self.assertIn(
            'skipLink.href = activeConfig ? "#selected-view-title" : "#dashboard-menu-title";',
            self.script,
        )
        self.assertIn('id="dashboard-menu-title" tabindex="-1"', self.index)

    def test_markup_never_hardcodes_a_recommendation(self) -> None:
        """The decision is contract-driven; the markup must not assert one.

        Static placeholder text is what a reader sees before the JSON loads,
        with scripting disabled, and if the contract fails validation. A
        hard-coded conclusion there can contradict the published pack, which is
        exactly what happened when the dashboard advanced from Week 2 to Week 4.
        """
        # The superseded Week 2 stance must not survive anywhere in the shipped
        # page or script.
        self.assertNotIn("Design and test", self.index)
        self.assertNotIn("Design and test", self.script)

        # Neither headline element may ship with a sourced-looking claim.
        for element_id in ("menu-decision-headline", "decision-title"):
            match = re.search(
                rf'id="{element_id}"[^>]*>([^<]*)<', self.index
            )
            self.assertIsNotNone(match, f"{element_id} is missing from the markup")
            placeholder = match.group(1).strip()
            self.assertNotIn(placeholder, self.payload["decision"]["headline"])
            self.assertTrue(
                placeholder.startswith("Loading"),
                f"{element_id} placeholder must be neutral, found {placeholder!r}",
            )

        # Both are filled from the governed contract at render time.
        self.assertIn(
            'setText("#menu-decision-headline", dashboardData.decision.headline);',
            self.script,
        )
        self.assertIn(
            'setText("#decision-title", dashboardData.decision.headline);',
            self.script,
        )

    def test_failed_validation_withdraws_the_recommendation(self) -> None:
        """Fail-closed means the conclusion goes away, not just the numbers."""
        failure = self.script[
            self.script.index("function showDataFailure()"):
        ]
        failure = failure[: failure.index("\nfunction ")]

        # Every element that carries the recommendation must be cleared.
        for element_id in (
            "menu-decision-status",
            "menu-decision-headline",
            "menu-decision-next",
            "menu-decision-confidence",
            "decision-title",
            "decision-support",
        ):
            self.assertIn(f'setText("#{element_id}"', failure)

        self.assertIn("No recommendation published.", failure)
        # The failure path must not name a superseded scope.
        self.assertNotIn("Week 1–2 diagnostic snapshot", failure)

    def test_roadmap_view_publishes_the_decision_pack(self) -> None:
        pack = self.payload["decision_pack"]

        # The view is registered as a landing page, not an accordion of topics.
        self.assertIn('roadmap: Object.freeze({', self.script)
        self.assertIn('label: "Decision & Roadmap"', self.script)
        self.assertIn('applicability: "Analyst proposal · filters do not apply"', self.script)
        self.assertIn('data-select-dashboard-view="roadmap"', self.index)
        self.assertIn('id="roadmap-view"', self.index)

        # Every region the renderer fills must exist in the markup.
        for element_id in (
            "roadmap-decision-requested", "roadmap-authority", "roadmap-direction",
            "roadmap-fallback", "roadmap-gate-count", "roadmap-recognized",
            "roadmap-option-list", "roadmap-initiative-list", "roadmap-benefit-list",
            "roadmap-gate-list", "roadmap-milestone-list", "roadmap-kpi-list",
            "roadmap-boundary",
        ):
            self.assertIn(f'id="{element_id}"', self.index)

        # It is hidden until chosen, like every other view.
        tags_by_id = {
            attrs["id"]: attrs for _, attrs in self.parser.tags if "id" in attrs
        }
        self.assertIn("hidden", tags_by_id["roadmap-view"])

        # The landing states the boundary rather than implying authority.
        self.assertEqual(pack["status"], "direction_proposed_no_execution_authority")
        self.assertIn("no production change", pack["authority_boundary"])
        self.assertIn("roadmap", self.payload["definitions"])
        self.assertTrue(self.payload["definitions"]["roadmap"]["boundary"])

        # The decision headline is the Week 4 recommendation, not the Week 2 stance.
        self.assertIn("90-day evidence mobilization", self.payload["decision"]["headline"])
        self.assertNotIn("Design and test", self.payload["decision"]["headline"])

    def test_governed_sources_separate_measured_data_from_design_artifacts(self) -> None:
        sources = self.payload["sources"]
        stages = [source["stage"] for source in sources]

        self.assertEqual(len(sources), 18)
        self.assertEqual(stages.count("diagnostic"), 12)
        self.assertEqual(stages.count("decision"), 6)
        # The data-quality tile counts measured evidence only: Week 3/4 design
        # files never passed the Week 1 checks or Week 2 reconciliation, so
        # counting them there would overstate the evidence base.
        self.assertEqual(self.payload["quality"]["source_artifacts"], 12)
        self.assertEqual(self.payload["decision_pack"]["source_artifacts"], 6)
        self.assertTrue(all(
            source["stage"] == "decision"
            for source in sources
            if source["file"].startswith(("W3_", "W4_"))
        ))

    def test_decision_pack_validation_fails_closed(self) -> None:
        node_script = """
const fs = require('node:fs');
const { assertDashboardData } = require('./docs/dashboard/app.js');
const base = JSON.parse(fs.readFileSync('./docs/dashboard/dashboard_data.json', 'utf8'));
assertDashboardData(base);
const clone = () => JSON.parse(JSON.stringify(base));
const mutations = [
  data => { delete data.decision_pack; },
  data => { data.decision_pack.status = 'approved_for_execution'; },
  data => { data.decision_pack.benefits.rows[0].recognized_value_usd = 35000000; },
  data => { data.decision_pack.benefits.rows[1].validated_value_usd = 7800; },
  data => { data.decision_pack.benefits.rows[2].funded_value_usd = 1; },
  data => { data.decision_pack.benefits.recognized_value_usd = 1; },
  data => { data.decision_pack.benefits.aggregation_rule = 'Total benefit'; },
  data => { data.decision_pack.benefits.rows.pop(); },
  data => { data.decision_pack.gates.rows[0].status = 'PASSED'; },
  data => { data.decision_pack.gates.passed_count = 3; },
  data => { data.decision_pack.gates.rows.pop(); },
  data => { data.decision_pack.options.rows[0].preferred = true; },
  data => { data.decision_pack.options.rows.pop(); },
  data => { data.decision_pack.options.decision_boundary = ''; },
  data => { data.decision_pack.initiatives.rows.pop(); },
  data => { data.decision_pack.initiatives.rows[1].priority_rank = 1; },
  data => { data.decision_pack.roadmap.rows.pop(); },
  data => { data.decision_pack.kpis.rows.pop(); },
  data => { data.decision_pack.kpis.rows.find(row => row.baseline === null).baseline = 0; },
];
let rejected = 0;
for (const mutate of mutations) {
  const data = clone();
  mutate(data);
  try { assertDashboardData(data); } catch { rejected += 1; }
}
process.stdout.write(JSON.stringify({ rejected, total: mutations.length }));
"""
        completed = subprocess.run(
            ["node", "-e", node_script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(completed.stdout)
        self.assertEqual(result["rejected"], result["total"])
        self.assertEqual(result["total"], 19)

    def test_quality_contract_validation_fails_closed_on_incomplete_evidence(self) -> None:
        node_script = """
const fs = require('node:fs');
const { assertDashboardData } = require('./docs/dashboard/app.js');
const base = JSON.parse(fs.readFileSync('./docs/dashboard/dashboard_data.json', 'utf8'));
assertDashboardData(base);
const clone = () => JSON.parse(JSON.stringify(base));
const mutations = [
  data => { data.quality.decision_boundary = ''; },
  data => { data.quality.decision_boundary = 'Certified complete and decision-ready'; },
  data => { data.quality.population_controls = []; },
  data => { data.quality.population_controls[1].key = data.quality.population_controls[0].key; },
  data => { data.quality.population_controls.forEach(control => { control.value = 0; }); },
  data => { data.quality.population_controls[0].evidence_label = 'Externally audited'; },
  data => { data.quality.source_artifacts += 1; },
  data => { data.quality.source_artifacts = 0; data.sources = []; },
  data => { data.quality.w1_checks.passed = 1; data.quality.w1_checks.total = 1; },
  data => { data.quality.w2_controls.reconciled = 1; data.quality.w2_controls.total = 1; },
  data => { data.quality.status = 'quality_score_passed'; },
  data => { data.meta.status = 'certified_live'; },
  data => { data.quality.dimensions.pop(); },
  data => { data.quality.dimensions[0].rules[1].key = data.quality.dimensions[0].rules[0].key; },
  data => { const moved = data.quality.dimensions[0].rules[0]; data.quality.dimensions[0].rules[0] = data.quality.dimensions[2].rules[0]; data.quality.dimensions[2].rules[0] = moved; },
  data => { data.quality.dimensions[0].label = 'Duplicate freedom'; },
  data => { data.quality.dimensions[1].status = 'measured'; data.quality.dimensions[1].status_label = 'Measured'; },
  data => { data.quality.dimensions[1].result = '0 / 0 passed'; },
  data => { data.quality.monitoring.snapshots = 2; },
  data => { data.quality.monitoring.status = 'improving'; },
  data => { data.quality.issue_queue.pop(); },
  data => { data.quality.issue_queue[0].severity = 'Critical'; },
  data => { data.quality.issue_queue[0].dimension = 'accuracy'; },
];
let rejected = 0;
for (const mutate of mutations) {
  const data = clone();
  mutate(data);
  try { assertDashboardData(data); } catch { rejected += 1; }
}
process.stdout.write(JSON.stringify({ rejected, total: mutations.length }));
"""
        completed = subprocess.run(
            ["node", "-e", node_script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(json.loads(completed.stdout), {"rejected": 23, "total": 23})

    def test_exact_menu_labels_route_to_their_owning_views(self) -> None:
        node_script = """
const fs = require('node:fs');
const model = require('./docs/dashboard/filter_model.js');
const app = require('./docs/dashboard/app.js');
const data = JSON.parse(fs.readFileSync('./docs/dashboard/dashboard_data.json', 'utf8'));
const index = model.buildSearchIndex(data, app.metricSearchDefinitions(data));
const expected = {
  'Executive Overview': 'view:executive',
  'Cash Visibility & Liquidity': 'view:cash',
  'Bank Account Footprint': 'view:footprint',
  'Payment Operations': 'view:payments',
  'Process Workload': 'view:workload',
  'Data Quality & Evidence': 'view:evidence',
};
const routes = Object.fromEntries(Object.entries(expected).map(([label]) => [
  label,
  model.querySearchIndex(index, label, { limit: 8 })[0]?.id ?? null,
]));
process.stdout.write(JSON.stringify({ routes, expected }));
"""
        completed = subprocess.run(
            ["node", "-e", node_script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(completed.stdout)
        self.assertEqual(result["routes"], result["expected"])

    def test_quality_dimension_and_issue_search_routes_are_indexed(self) -> None:
        node_script = """
const fs = require('node:fs');
const model = require('./docs/dashboard/filter_model.js');
const app = require('./docs/dashboard/app.js');
const data = JSON.parse(fs.readFileSync('./docs/dashboard/dashboard_data.json', 'utf8'));
const index = model.buildSearchIndex(data, app.metricSearchDefinitions(data));
const firstId = query => model.querySearchIndex(index, query, { limit: 8 })[0]?.id ?? null;
process.stdout.write(JSON.stringify({
  accuracy: firstId('Accuracy'),
  timeliness: firstId('Timeliness'),
  issue: firstId('DQ-11'),
}));
"""
        completed = subprocess.run(
            ["node", "-e", node_script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            json.loads(completed.stdout),
            {
                "accuracy": "quality-dimension:accuracy",
                "timeliness": "quality-dimension:timeliness",
                "issue": "quality-issue:DQ-11",
            },
        )
        self.assertIn('entry.id.startsWith("quality-dimension:")', self.script)
        self.assertIn('entry.id.startsWith("quality-issue:")', self.script)

    def test_visual_renderers_update_with_existing_state_and_fail_closed(self) -> None:
        required = (
            "renderDecisionEvidence();",
            "renderVisibilityAnalytics(visibility, hasData);",
            "renderLiquidityWaterfall(liquidity);",
            "renderLiquidityTrend(liquidity);",
            "renderPaymentAnalytics({ config, unionValue, totalValue, share });",
            "renderCapacityComparison(capacity);",
            "renderClosureCandidateTable(closures);",
            "renderRegionalFootprint(regional);",
            "renderRegions();",
            "currentSummary.visibility",
            "visibility.by_method.forEach",
            "currentSummary.liquidity.trend",
            "payments.cohort_order",
            "closures.candidate_accounts",
            "currentSummary.regional",
            "clearVisualizationOutputs();",
            "replaceChildren()",
            'detail.dataset.inlineDetail === "liquidity"',
        )
        for token in required:
            self.assertIn(token, self.script)

        self.assertIn("drawing = false", self.script)
        self.assertIn("if (!isFiniteNumber(value))", self.script)
        self.assertIn("context.setLineDash(days === 14 ? [6, 4] : [])", self.script)
        self.assertIn("border-top-style: dashed", self.styles)
        self.assertNotIn("context.fill()", self.script)
        self.assertNotIn("target", self.index.lower())
        self.assertIn(
            "Dormant + legacy purpose + zero supplied payment records",
            self.script,
        )
        self.assertIn("Validation required · not approved", self.script)
        self.assertIn("Shared scale · never additive", self.index)
        self.assertIn("visibilityActionText(visibility, hasData)", self.script)
        self.assertIn("No visibility action is derived for an empty scope.", self.script)
        self.assertIn("No delayed reporting method is evidenced in the selected scope", self.script)
        self.assertIn("Priority-union share and cohort composition", self.index)
        self.assertIn("Share of all matching ${config.label}", self.script)
        self.assertIn("supplied payment-file monthly average", self.index)
        self.assertIn("Estimated annual fee (USD)", self.index)
        self.assertIn("applyRegionalSelection", self.script)
        self.assertIn('region_filter_mode: "facet_override"', (DASHBOARD / "filter_model.js").read_text(encoding="utf-8"))
        regional_renderer = self.script.split("function renderRegionalFootprint", 1)[1].split(
            "function renderClosureCandidateTable", 1
        )[0]
        self.assertNotIn("liquidity", regional_renderer)

    def test_filters_fail_closed_and_empty_scopes_do_not_fake_rates(self) -> None:
        required = (
            'data.schema_version !== "2.0"',
            "The last valid view is unchanged.",
            "No matching data",
            "no percentage is calculated",
            'totalValue > 0 && isFiniteNumber(share)',
            'return isFiniteNumber(value) ? `${formatNumber(value, 2)}%` : "—"',
            "liquidity.funded_case.display",
            "validated_mobility.value_usd !== null",
            "Validated mobility: not established by supplied data.",
        )
        for token in required:
            self.assertIn(token, self.script)
        self.assertNotIn("share || 0", self.script)
        self.assertNotIn("share ?? 0", self.script)

    def test_adaptive_usd_formatter_never_renders_nonzero_as_zero_millions(self) -> None:
        node_script = """
const { formatUsdCompact } = require('./docs/dashboard/app.js');
const values = [1568.19, 943.98, -943.98, 0.5, -0.5, 0, 38127490.73];
process.stdout.write(JSON.stringify(values.map(formatUsdCompact)));
"""
        completed = subprocess.run(
            ["node", "-e", node_script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        formatted = json.loads(completed.stdout)
        self.assertEqual(formatted, ["$1.6k", "$944", "−$944", "$0.5", "−$0.5", "$0", "$38.13m"])
        self.assertNotIn("$0.00m", formatted)

    def test_visual_runtime_helpers_use_filtered_summaries_and_preserve_nulls(self) -> None:
        node_script = """
const fs = require('node:fs');
const model = require('./docs/dashboard/filter_model.js');
const visual = require('./docs/dashboard/app.js');
const data = JSON.parse(fs.readFileSync('./docs/dashboard/dashboard_data.json', 'utf8'));
const defaults = model.createDefaultState(data);
const base = model.summarize(data, defaults);
const filtered = model.summarize(data, {
  ...defaults,
  region: 'EMEA',
  currency: 'EUR',
  bank: 'Pacific Crown',
});
const zeroPayments = model.summarize(data, {
  ...defaults,
  entity: 'E006',
  bank: 'Pacific Crown',
});
const empty = model.summarize(data, {
  ...defaults,
  region: 'EMEA',
  currency: 'JPY',
});
const jan7 = model.summarize(data, {
  ...defaults,
  dateFrom: '2026-01-07',
  dateTo: '2026-01-07',
});
const paymentRows = visual.paymentCohortVisualRows(base.payments, 'records');
const zeroPaymentRegion = zeroPayments.regional.rows.find(row => row.status === 'available');
process.stdout.write(JSON.stringify({
  visibilityOrder: filtered.visibility.by_method.map(row => row.method),
  visibilityAccounts: filtered.visibility.by_method.map(row => row.accounts_total),
  paymentValues: paymentRows.map(row => row.value),
  paymentShareTotal: paymentRows.reduce((sum, row) => sum + row.contribution, 0),
  zeroPaymentRows: visual.paymentCohortVisualRows(zeroPayments.payments, 'records').length,
  waterfallGeometry: visual.waterfallBarGeometry(filtered.liquidity.waterfalls['14'].steps),
  closureIds: filtered.closures.candidate_accounts.map(row => row.account_id),
  jan7Seven: visual.liquidityTrendValue(jan7.liquidity.trend[0], 7),
  jan7Fourteen: visual.liquidityTrendValue(jan7.liquidity.trend[0], 14),
  trendStart: filtered.liquidity.trend[0].date,
  trendEnd: filtered.liquidity.trend.at(-1).date,
  baseVisibilityAction: visual.visibilityActionText(base.visibility, true),
  filteredVisibilityAction: visual.visibilityActionText(filtered.visibility, true),
  emptyVisibilityAction: visual.visibilityActionText(empty.visibility, false),
  zeroRegionalPayment: visual.regionalPaymentText(zeroPaymentRegion),
  missingRegionalDelay: visual.regionalDelayedText({
    status: 'available',
    visibility: { delayed_account_share_pct: null },
  }),
  unavailableMarkerSize: visual.regionalMarkerSize(0, 22),
}));
"""
        completed = subprocess.run(
            ["node", "-e", node_script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(completed.stdout)
        self.assertEqual(
            result["visibilityOrder"],
            ["API", "Host-to-host", "Portal", "Spreadsheet"],
        )
        self.assertEqual(result["visibilityAccounts"], [1, 1, 0, 0])
        self.assertEqual(result["paymentValues"], [2053, 342, 444, 4761])
        self.assertAlmostEqual(result["paymentShareTotal"], 100, delta=0.02)
        self.assertEqual(result["zeroPaymentRows"], 0)
        self.assertEqual(len(result["waterfallGeometry"]), 6)
        self.assertTrue(
            all(
                geometry is not None
                and 0 <= geometry["bottom"] <= 100
                and 0 <= geometry["height"] <= 100
                for geometry in result["waterfallGeometry"]
            )
        )
        self.assertEqual(result["closureIds"], ["AC0024"])
        self.assertIsNotNone(result["jan7Seven"])
        self.assertIsNone(result["jan7Fourteen"])
        self.assertEqual(result["trendStart"], "2026-01-01")
        self.assertEqual(result["trendEnd"], "2026-06-30")
        self.assertIn("Portal and Spreadsheet", result["baseVisibilityAction"])
        self.assertIn("No delayed reporting method is evidenced", result["filteredVisibilityAction"])
        self.assertEqual(
            result["emptyVisibilityAction"],
            "No visibility action is derived for an empty scope.",
        )
        self.assertEqual(
            result["zeroRegionalPayment"],
            "0 supplied records · share unavailable",
        )
        self.assertEqual(
            result["missingRegionalDelay"],
            "No supplied account-day evidence",
        )
        self.assertEqual(result["unavailableMarkerSize"], 52)

    def test_search_uses_model_index_and_complete_keyboard_controls(self) -> None:
        required = (
            "FilterModel.buildSearchIndex",
            "FilterModel.querySearchIndex",
            'event.key === "ArrowDown"',
            'event.key === "ArrowUp"',
            'event.key === "Enter"',
            'event.key === "Escape"',
            "aria-activedescendant",
            'entry.kind === "metric"',
            'entry.kind === "dimension"',
            'entry.kind === "account"',
            "entry.values.entity_id",
            "window.requestAnimationFrame(() => searchInput.focus())",
            'document.addEventListener("pointerdown"',
            'id: `inline:${topic}`',
            'id: `guide:${topic}`',
        )
        for token in required:
            self.assertIn(token, self.script)
        self.assertNotIn("new RegExp", self.script)

        node_script = """
const {
  orderSearchResultsForDisplay,
  dashboardViewForTopic,
  dashboardTopicsForView,
} = require('./docs/dashboard/app.js');
const results = [
  { id: 'inline:regions', kind: 'metric', label: 'Regional footprint' },
  { id: 'region:EMEA', kind: 'dimension', label: 'EMEA' },
  { id: 'account:AC0024', kind: 'account', label: 'AC0024' },
];
process.stdout.write(JSON.stringify({
  exact: orderSearchResultsForDisplay(results, ' EMEA ').map((entry) => entry.id),
  metric: orderSearchResultsForDisplay(results, 'map').map((entry) => entry.id),
  topicViews: ['decision', 'visibility', 'liquidity', 'regions', 'closures', 'payments', 'capacity']
    .map((topic) => [topic, dashboardViewForTopic(topic)]),
  footprintTopics: dashboardTopicsForView('footprint'),
  evidenceTopics: dashboardTopicsForView('evidence'),
}));
"""
        completed = subprocess.run(
            ["node", "-e", node_script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        ordered = json.loads(completed.stdout)
        self.assertEqual(
            ordered["exact"],
            ["region:EMEA", "inline:regions", "account:AC0024"],
        )
        self.assertEqual(
            ordered["metric"],
            ["inline:regions", "region:EMEA", "account:AC0024"],
        )
        self.assertEqual(
            ordered["topicViews"],
            [
                ["decision", "executive"],
                ["visibility", "cash"],
                ["liquidity", "cash"],
                ["regions", "footprint"],
                ["closures", "footprint"],
                ["payments", "payments"],
                ["capacity", "workload"],
            ],
        )
        self.assertEqual(ordered["footprintTopics"], ["regions", "closures"])
        self.assertEqual(ordered["evidenceTopics"], [])
        self.assertIn('id: `view:${view}`', self.script)
        self.assertIn("Object.entries(DASHBOARD_VIEWS)", self.script)
        self.assertIn('applicability: "Portfolio-wide · filters do not apply"', self.script)
        self.assertIn("selectDashboardView(entry.id.slice(\"view:\".length))", self.script)

    def test_metric_guide_contains_stable_methodology_without_live_values(self) -> None:
        required_sections = (
            'evidenceSection("Definition"',
            'evidenceSection("Formula / calculation"',
            'evidenceSection("Data source"',
            'evidenceSection("Method limit"',
        )
        for token in required_sections:
            self.assertIn(token, self.script)
        self.assertIn(
            "Estimated monthly manual hours = frequency × minutes per instance × manual percentage ÷ 60.",
            self.script,
        )
        self.assertIn("definition.formula", self.script)
        self.assertNotIn("dashboardData.visibility.sources", self.script)
        self.assertNotIn('evidenceSection("Next action"', self.script)
        self.assertNotIn("topicValues(", self.script)
        self.assertNotIn("metric-context", self.script)
        self.assertEqual(self.script.count('section.append(make("h3", "", title))'), 1)
        self.assertIn(
            "Definitions, formulas, sources, and method limits do not change with dashboard filters.",
            self.index,
        )

        definitions = self.payload["definitions"]
        self.assertEqual(
            definitions["visibility"]["formula"],
            "Delayed-account share = delayed selected accounts ÷ selected accounts; same-day rate = delay-0 account-days ÷ selected account-days.",
        )
        self.assertEqual(
            definitions["liquidity"]["formula"],
            "Net screen = Σ max(positive availability − trailing buffer, 0) for unflagged accounts + Σ negative availability.",
        )
        self.assertEqual(
            definitions["payments"]["formula"],
            "Priority share = priority-union measure ÷ matching overall measure; the manual-touch/cross-border overlap is counted once.",
        )
        self.assertEqual(
            definitions["regions"]["formula"],
            "Regional measure = the governed measure recomputed for accounts whose region equals NA, EMEA, or APAC; regional rows reconcile to the facet scope.",
        )
        self.assertEqual(
            definitions["quality"]["formula"],
            "Status = all required internal checks pass and all declared control totals reconcile; no composite data-quality score is calculated.",
        )
        self.assertIn('"gates", "quality"', self.script)
        self.assertIn(
            "Enterprise-global management estimate · filters do not apply · not a combined capacity or P&amp;L baseline",
            self.index,
        )

    def test_collapsed_operational_qualifiers_match_filter_applicability(self) -> None:
        combined = "\n".join((self.index, self.script))
        required = (
            "Calendar-date proxy · not start-of-day or elapsed-24-hour visibility",
            "-day screen · as of ${formatIsoDate(liquidity.as_of_date)}",
            '${formatNumber(unionValue)} of ${formatNumber(totalValue)} ${config.label}',
            "Supplied records only · association, not causation",
            "Enterprise-global management estimate · filters do not apply · not a combined capacity or P&L baseline",
            "h/month vs ${capacity.payment_file_repair_hours_monthly.toFixed(1)} h/month",
            "30 Jun 2026 snapshot · date filter does not apply · currency/region/entity/bank filters apply",
            "dimensionFilterContext(appliedFilters)",
            "Schematic account coverage · supplied diagnostics · not a live cash map",
            "regionalFacetContext(appliedFilters)",
        )
        for phrase in required:
            self.assertIn(phrase, combined)
        self.assertNotIn("Global baseline · filters do not apply", combined)

    def test_liquidity_scope_uses_range_end_not_from_date(self) -> None:
        self.assertIn(
            "As of ${formatIsoDate(liquidity.as_of_date)} · trailing ${state.liquidityDays} calendar days · From date does not constrain this screen",
            self.script,
        )
        render_liquidity = self.script.split("function renderLiquidity", 1)[1].split(
            "function paymentMeasureData", 1
        )[0]
        liquidity_detail = render_liquidity.split(
            'renderInlineDetail("liquidity"', 1
        )[1]
        self.assertIn("dimensionFilterContext(appliedFilters)", liquidity_detail)
        self.assertNotIn("currentScopeText()", liquidity_detail)

        node_script = """
const fs = require('node:fs');
const model = require('./docs/dashboard/filter_model.js');
const data = JSON.parse(fs.readFileSync('./docs/dashboard/dashboard_data.json', 'utf8'));
const defaults = model.createDefaultState(data);
const fullPeriod = model.summarize(data, defaults);
const sameEndSingleDay = model.summarize(data, { ...defaults, dateFrom: defaults.dateTo });
const { trend: fullTrend, ...fullSnapshot } = fullPeriod.liquidity;
const { trend: singleDayTrend, ...singleDaySnapshot } = sameEndSingleDay.liquidity;
process.stdout.write(JSON.stringify({
  sameSnapshot: JSON.stringify(fullSnapshot) === JSON.stringify(singleDaySnapshot),
  fullTrendStart: fullTrend[0].date,
  singleDayTrendStart: singleDayTrend[0].date,
  singleDayTrendEnd: singleDayTrend.at(-1).date,
  fullTrendLength: fullTrend.length,
  singleDayTrendLength: singleDayTrend.length,
  fullPayments: fullPeriod.payments.overall.records,
  singleDayPayments: sameEndSingleDay.payments.overall.records,
}));
"""
        completed = subprocess.run(
            ["node", "-e", node_script],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(completed.stdout)
        self.assertTrue(result["sameSnapshot"])
        self.assertEqual(result["fullTrendStart"], "2026-01-01")
        self.assertEqual(result["singleDayTrendStart"], "2026-06-30")
        self.assertEqual(result["singleDayTrendEnd"], "2026-06-30")
        self.assertEqual(result["fullTrendLength"], 181)
        self.assertEqual(result["singleDayTrendLength"], 1)
        self.assertNotEqual(result["fullPayments"], result["singleDayPayments"])

    def test_claims_keep_evidence_boundaries_visible(self) -> None:
        combined = "\n".join((self.index, self.script))
        required = (
            "supplied data, not live operations",
            "Reporting-date proxy—not start-of-day or elapsed-24-hour performance.",
            "Validated mobility: not established by supplied data.",
            "screening sensitivity—not surplus cash or transfer authorization.",
            "supplied records only; association, not causation.",
            "overlap records are counted once.",
            "Capacity value not fundable",
            "Closure value not fundable",
            "no approved closures",
        )
        for phrase in required:
            self.assertIn(phrase, combined)

        # The recommendation itself is contract-driven, not markup, so its
        # caution is asserted against the published decision rather than the
        # static files. It must still refuse funding and execution.
        headline = self.payload["decision"]["headline"]
        self.assertIn("do not fund or execute yet", headline)
        self.assertEqual(
            self.payload["decision"]["status"],
            "direction_proposed_no_execution_authority",
        )

    def test_csv_derived_content_is_not_injected_as_html(self) -> None:
        prohibited = ("innerHTML", "outerHTML", "insertAdjacentHTML")
        for token in prohibited:
            self.assertNotIn(token, self.script)
        self.assertIn("textContent", self.script)
        self.assertIn("replaceChildren", self.script)
        self.assertIn("showDataFailure", self.script)
        self.assertIn("Data unavailable — validation did not complete.", self.index)

    def test_site_is_self_contained(self) -> None:
        combined = "\n".join((self.index, self.styles, self.script))
        self.assertNotIn("http://", combined)
        self.assertNotIn("https://", combined)
        self.assertIn('href="styles.css"', self.index)
        self.assertIn('src="filter_model.js"', self.index)
        self.assertIn('src="app.js"', self.index)
        self.assertIn('fetch("dashboard_data.json"', self.script)

    def test_guided_review_wizard_has_three_governed_steps_and_controls(self) -> None:
        tags_by_id = {attrs["id"]: attrs for _, attrs in self.parser.tags if "id" in attrs}
        for required in (
            "guided-review-dialog",
            "wizard-title",
            "wizard-progress",
            "wizard-step-1",
            "wizard-step-2",
            "wizard-step-3",
            "wizard-decision-options",
            "wizard-decision-error",
            "wizard-scope-form",
            "wizard-answer",
            "wizard-back",
            "wizard-next",
            "wizard-finish",
            "wizard-skip",
            "wizard-close",
        ):
            self.assertIn(required, tags_by_id)

        # Steps 2 and 3 start hidden; step 1 is the entry point.
        self.assertNotIn("hidden", tags_by_id["wizard-step-1"])
        self.assertIn("hidden", tags_by_id["wizard-step-2"])
        self.assertIn("hidden", tags_by_id["wizard-step-3"])

        # Back is hidden on step 1 and Finish only appears on the last step.
        self.assertIn("hidden", tags_by_id["wizard-back"])
        self.assertIn("hidden", tags_by_id["wizard-finish"])
        self.assertNotIn("hidden", tags_by_id["wizard-next"])

        # Skip to the full dashboard stays available on every step.
        self.assertNotIn("hidden", tags_by_id["wizard-skip"])
        self.assertIn("Skip to Full Dashboard", self.index)
        self.assertIn("View Full Dashboard", self.index)

        # Exactly the four required decision areas, and a blocked step 1.
        self.assertIn('const WIZARD_DECISION_KEYS = Object.freeze(Object.keys(WIZARD_DECISIONS));', self.script)
        for label in ("Cash Visibility", "Liquidity", "Payments", "Data Quality"):
            self.assertIn(f'label: "{label}"', self.script)
        advance = self.script.split("function advanceWizard", 1)[1].split(
            "function selectWizardDecision", 1
        )[0]
        self.assertIn("if (!wizardState.decision)", advance)
        self.assertIn("error.hidden = false", advance)

        # Progress indicator is a live "Step N of 3".
        self.assertIn('`Step ${step} of ${WIZARD_TOTAL_STEPS}`', self.script)
        self.assertIn('const WIZARD_TOTAL_STEPS = 3;', self.script)

        # Scope selections persist across Back/Next.
        self.assertIn("wizardState.scope = readWizardScope();", self.script)
        self.assertIn("select.value = scope[field]", self.script)

        # Accessible radiogroup semantics and keyboard support.
        self.assertIn('role="radiogroup"', self.index)
        self.assertIn('option.setAttribute("role", "radio");', self.script)
        self.assertIn('option.setAttribute("aria-checked", String(selected));', self.script)
        self.assertIn('"ArrowDown"', self.script)

        # The wizard reuses the governed filter pipeline rather than bypassing it.
        apply_block = self.script.split("function applyWizardScopeToDashboard", 1)[1].split(
            "\n}", 1
        )[0]
        self.assertIn("applyFilterCandidate(", apply_block)

        for token in (".wizard-steps", ".wizard-option", ".wizard-answer", ".wizard-footer"):
            self.assertIn(token, self.styles)

    def test_wizard_answer_shows_one_finding_limit_action_and_approver(self) -> None:
        answer = self.script.split("function renderWizardAnswer", 1)[1].split(
            "function describeWizardScope", 1
        )[0]
        for label in (
            '"Core finding"',
            '"What this evidence cannot show"',
            '"Recommended action"',
            '"Approval required from"',
        ):
            self.assertIn(label, answer)

        # Exactly one finding, one action, one approver — read from the contract.
        self.assertIn("wizardFinding(key)", answer)
        self.assertIn("definition.boundary", answer)
        self.assertIn("definition.next_action", answer)
        self.assertIn("config.approver", answer)

        # Every decision area names a required approver.
        decisions = self.script.split("const WIZARD_DECISIONS", 1)[1].split(
            "const WIZARD_DECISION_KEYS", 1
        )[0]
        self.assertEqual(decisions.count("approver:"), 4)

        # Depth is linked, not inlined, so the wizard stays a summary.
        self.assertIn('dataset.openDetailPage = page', answer)
        self.assertNotIn("definition.formula", answer)

    def test_secondary_detail_pages_cover_the_four_reference_topics(self) -> None:
        tags_by_id = {attrs["id"]: attrs for _, attrs in self.parser.tags if "id" in attrs}
        for required in ("detail-pages", "detail-page-title", "detail-page-body", "detail-page-back"):
            self.assertIn(required, tags_by_id)
        self.assertIn("hidden", tags_by_id["detail-pages"])

        self.assertIn(
            'const DETAIL_PAGE_KEYS = Object.freeze(Object.keys(DETAIL_PAGES));',
            self.script,
        )
        for page in ("formulas", "constraints", "methodology", "data"):
            self.assertIn(f'data-open-detail-page="{page}"', self.index)
            self.assertIn(f"  {page}: Object.freeze({{", self.script)

        # Reachable from the Metric guide drawer and from contextual links.
        drawer = self.index.split('<dialog id="evidence-dialog"', 1)[1]
        for page in ("formulas", "constraints", "methodology", "data"):
            self.assertIn(f'data-open-detail-page="{page}"', drawer)
        menu_page = self.index.split('<div id="menu-page"', 1)[1].split("</main>", 1)[0]
        self.assertIn("data-open-detail-page=", menu_page)

        # Technical depth is rendered from the governed contract.
        render = self.script.split("function renderDetailPage", 1)[1].split(
            "function openDetailPage", 1
        )[0]
        for source in ("definition.formula", "definition.boundary", "definition.next_action", "quality.w1_checks"):
            self.assertIn(source, render)
        self.assertIn("replaceChildren", render)

        # Opening a detail page takes over the main area and is fail-closed.
        self.assertIn("const detailPageOpen = Boolean(state.detailPage);", self.script)
        self.assertIn('if (!dashboardData || !DETAIL_PAGE_KEYS.includes(page)) return;', self.script)

        for token in (".detail-pages", ".detail-page-tabs", ".detail-page-card"):
            self.assertIn(token, self.styles)

    def test_wizard_and_detail_contracts_resolve_against_governed_data(self) -> None:
        node_script = """
const {
  WIZARD_DECISIONS,
  WIZARD_DECISION_KEYS,
  WIZARD_TOTAL_STEPS,
  DETAIL_PAGE_KEYS,
  NEXT_ACTION_TOPICS,
} = require('./docs/dashboard/app.js');
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('./docs/dashboard/dashboard_data.json', 'utf8'));
const unresolved = WIZARD_DECISION_KEYS.filter((key) => {
  const topic = WIZARD_DECISIONS[key].topic;
  const definition = data.definitions[topic];
  return !definition || !definition.boundary || !definition.next_action || !definition.title;
});
const actionsUnresolved = NEXT_ACTION_TOPICS.filter((topic) => {
  const definition = data.definitions[topic];
  return !definition || !definition.next_action;
});
process.stdout.write(JSON.stringify({
  decisions: WIZARD_DECISION_KEYS,
  steps: WIZARD_TOTAL_STEPS,
  detailPages: DETAIL_PAGE_KEYS,
  nextActions: NEXT_ACTION_TOPICS,
  unresolved,
  actionsUnresolved,
  approvers: WIZARD_DECISION_KEYS.map((key) => WIZARD_DECISIONS[key].approver),
}));
"""
        completed = subprocess.run(
            ["node", "-e", node_script],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        result = json.loads(completed.stdout)

        # The four required decision areas, in the order the wizard presents them.
        self.assertEqual(result["decisions"], ["visibility", "liquidity", "payments", "quality"])
        self.assertEqual(result["steps"], 3)
        self.assertEqual(
            result["detailPages"], ["formulas", "constraints", "methodology", "data"]
        )
        self.assertEqual(result["nextActions"], ["visibility", "liquidity", "payments"])

        # Every wizard decision and next action resolves to a governed definition,
        # so no step can render an invented finding, limit, or action.
        self.assertEqual(result["unresolved"], [])
        self.assertEqual(result["actionsUnresolved"], [])

        # Every decision area names a real approver.
        self.assertEqual(len(result["approvers"]), 4)
        for approver in result["approvers"]:
            self.assertTrue(approver.strip())

    def test_guided_review_tour_spotlights_real_elements(self) -> None:
        tags_by_id = {attrs["id"]: attrs for _, attrs in self.parser.tags if "id" in attrs}
        for required in (
            "tour-overlay",
            "tour-scrim",
            "tour-ring",
            "tour-popover",
            "tour-progress",
            "tour-step-title",
            "tour-step-body",
            "tour-dots",
            "tour-back",
            "tour-next",
            "tour-finish",
            "tour-skip",
            "tour-close",
        ):
            self.assertIn(required, tags_by_id)

        # The overlay starts hidden; Back and Finish start hidden (step 1 of N).
        self.assertIn("hidden", tags_by_id["tour-overlay"])
        self.assertIn("hidden", tags_by_id["tour-back"])
        self.assertIn("hidden", tags_by_id["tour-finish"])
        self.assertNotIn("hidden", tags_by_id["tour-next"])
        self.assertNotIn("hidden", tags_by_id["tour-skip"])

        # Each control does what its label says: "Take a tour" starts the tour
        # and "Start Guided Review" opens the three-step review.
        self.assertIn('data-start-tour', self.index)
        self.assertIn(
            'getAll("[data-start-tour]").forEach((button) => {\n'
            '    button.addEventListener("click", () => startTour(button));',
            self.script,
        )
        self.assertIn(
            'getAll("[data-start-guided-review]").forEach((button) => {\n'
            '    button.addEventListener("click", () => openGuidedReview(button));',
            self.script,
        )
        self.assertNotIn("Focused review", self.index)

        # The popover is a real modal dialog for assistive technology.
        popover = self.index.split('id="tour-popover"', 1)[1].split(">", 1)[0]
        self.assertIn('role="dialog"', popover)
        self.assertIn('aria-modal="true"', popover)

        # Positioning must not depend on an animation frame alone, or a step that
        # needs no scrolling would never move the spotlight off the previous one.
        render = self.script.split("function renderTourStep", 1)[1].split(
            "function goToTourStep", 1
        )[0]
        self.assertIn("positionTourStep();", render)

        # Escape closes, arrow keys navigate, and focus stays inside the popover.
        keys = self.script.split("function handleTourKeydown", 1)[1].split(
            "\n}\n", 1
        )[0]
        for key in ('"Escape"', '"ArrowRight"', '"ArrowLeft"', '"Tab"'):
            self.assertIn(key, keys)

        # Scroll is locked while the tour runs and released when it ends.
        self.assertIn('document.body.classList.add("tour-active");', self.script)
        self.assertIn('document.body.classList.remove("tour-active");', self.script)

        # Steps whose target is missing or collapsed are skipped, never pointed at.
        visible = self.script.split("function tourVisibleSteps", 1)[1].split(
            "\n}\n", 1
        )[0]
        self.assertIn("rect.width > 0 && rect.height > 0", visible)

        for token in (".tour-overlay", ".tour-ring", ".tour-popover", "body.tour-active"):
            self.assertIn(token, self.styles)
        # The spotlight is the ring's outer shadow.
        self.assertIn("box-shadow: 0 0 0 9999px", self.styles)

    def test_tour_steps_target_elements_that_exist_in_the_page(self) -> None:
        node_script = """
const { TOUR_STEPS } = require('./docs/dashboard/app.js');
process.stdout.write(JSON.stringify({
  count: TOUR_STEPS.length,
  targets: TOUR_STEPS.map((step) => step.target),
  complete: TOUR_STEPS.every((step) => step.target && step.title && step.body),
}));
"""
        completed = subprocess.run(
            ["node", "-e", node_script],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        result = json.loads(completed.stdout)
        self.assertTrue(result["complete"])
        self.assertGreaterEqual(result["count"], 5)

        # Every tour target must resolve to something in the shipped markup,
        # otherwise the step silently disappears from the tour.
        ids = set(self.parser.ids)
        classes = set()
        for _, attrs in self.parser.tags:
            for value in (attrs.get("class") or "").split():
                classes.add(value)
        for target in result["targets"]:
            if target.startswith("#"):
                self.assertIn(target[1:], ids, f"tour target {target} missing")
            else:
                self.assertIn(target.lstrip("."), classes, f"tour target {target} missing")

        # The primary CTA class must exist in the design system, or the button
        # renders with the default surface fill and disappears on a dark band.
        self.assertIn(".button-primary {", self.styles)

    def test_liquidity_headline_is_labelled_as_a_screen_not_available_cash(self) -> None:
        # "availability" reads as spendable money. The headline number is a
        # screening total, so the label has to say so where the figure is read.
        self.assertIn("Gross positive balance — screening only", self.index)
        self.assertNotIn("Gross positive availability", self.index)
        self.assertNotIn("Gross positive estimated availability", self.index)

        ladder = self.payload["liquidity"]["evidence_ladder"][0]
        self.assertEqual(ladder["label"], "Gross positive balance — screening only")
        # The contract key is an identifier and stays stable across the rename.
        self.assertEqual(ladder["key"], "gross_positive_estimated_availability")

        # The screen is still separated from validated movable cash.
        self.assertEqual(
            self.payload["liquidity"]["validated_mobility"]["status"], "not_established"
        )

    def test_provenance_stamp_is_visible_and_read_from_the_contract(self) -> None:
        tags_by_id = {attrs["id"]: attrs for _, attrs in self.parser.tags if "id" in attrs}
        for required in ("data-provenance", "data-last-updated", "data-version"):
            self.assertIn(required, tags_by_id)
        # Shown in the header, not hidden behind a disclosure.
        self.assertNotIn("hidden", tags_by_id["data-provenance"])
        # A real <time> element so the date is machine-readable.
        self.assertEqual(tags_by_id["data-last-updated"].get("datetime"), "")
        self.assertIn("<time id=\"data-last-updated\"", self.index)

        # Both values come from the governed contract, never hard-coded.
        render = self.script.split("function renderProvenance", 1)[1].split(
            "\n}\n", 1
        )[0]
        self.assertIn("meta.last_updated", render)
        self.assertIn("meta.data_version", render)

        self.assertIn("last_updated", self.payload["meta"])
        self.assertIn("data_version", self.payload["meta"])
        self.assertTrue(self.payload["meta"]["data_version"].startswith(
            f"{self.payload['schema_version']}+"
        ))
        self.assertRegex(self.payload["meta"]["last_updated"], r"^\d{4}-\d{2}-\d{2}$")
        self.assertIn(".data-provenance", self.styles)

    def test_filtered_export_carries_scope_and_boundaries(self) -> None:
        tags_by_id = {attrs["id"]: attrs for _, attrs in self.parser.tags if "id" in attrs}
        self.assertIn("export-filtered", tags_by_id)
        self.assertIn("data-requires-data", tags_by_id["export-filtered"])
        self.assertIn("Export filtered results", self.index)

        rows = self.script.split("function filteredExportRows", 1)[1].split(
            "const EXPORT_COLUMNS", 1
        )[0]
        # Export reads the filtered summary, not the unfiltered payload.
        self.assertIn("currentSummary", rows)
        self.assertIn("currentScopeText()", rows)

        # An empty scope must not export a zero result.
        self.assertIn("summary.scope.has_matches", rows)
        self.assertIn("an empty scope is not a zero result", rows)

        # Unestablished values stay unestablished in the file.
        self.assertIn('"not_established"', rows)
        self.assertIn("This is not a zero balance.", rows)

        # Every row carries its scope, its limit, and the dataset identity.
        for column in ("applied_scope", "evidence_boundary", "data_version", "last_updated"):
            self.assertIn(column, self.script.split("const EXPORT_COLUMNS", 1)[1][:400])

        self.assertIn(".export-button", self.styles)

    def test_csv_export_escapes_quotes_and_blocks_formula_injection(self) -> None:
        node_script = """
const { csvCell, csvFromRows, EXPORT_COLUMNS } = require('./docs/dashboard/app.js');
process.stdout.write(JSON.stringify({
  formula: ['=1+1', '+1', '-1', '@x'].map(csvCell),
  plain: csvCell('Design and test'),
  quoted: csvCell('say "hi"'),
  comma: csvFromRows([{ a: 'x,y', b: 'z' }], ['a', 'b']),
  columns: EXPORT_COLUMNS,
}));
"""
        completed = subprocess.run(
            ["node", "-e", node_script],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        result = json.loads(completed.stdout)
        # Leading =, +, -, @ are neutralised so a spreadsheet cannot execute them.
        for cell in result["formula"]:
            self.assertTrue(cell.startswith("\"'"), cell)
        self.assertEqual(result["plain"], '"Design and test"')
        self.assertEqual(result["quoted"], '"say ""hi"""')
        self.assertIn('"x,y"', result["comma"])
        self.assertEqual(result["columns"][0], "section")

    def test_local_http_assets_are_served(self) -> None:
        handler = functools.partial(
            http.server.SimpleHTTPRequestHandler,
            directory=str(ROOT),
        )
        try:
            server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        except PermissionError:
            self.skipTest("Local sockets are disabled in this execution sandbox")
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            base = f"http://127.0.0.1:{server.server_port}/docs/dashboard"
            for relative in (
                "/",
                "/styles.css",
                "/filter_model.js",
                "/app.js",
                "/dashboard_data.json",
                "/assets/world-map.png",
            ):
                with urllib.request.urlopen(base + relative, timeout=5) as response:
                    self.assertEqual(response.status, 200)
                    self.assertTrue(response.read())
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
