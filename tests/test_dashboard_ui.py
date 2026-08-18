"""Structural and integration checks for the interactive dashboard UI."""

import functools
import http.server
import json
import sys
import threading
import unittest
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from build_dashboard_data import build_dashboard_data, load_dashboard_inputs  # noqa: E402


DASHBOARD = ROOT / "dashboard"


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags = []
        self.ids = []
        self.html_attrs = {}

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        self.tags.append((tag, values))
        if tag == "html":
            self.html_attrs = values
        if "id" in values:
            self.ids.append(values["id"])


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
        self.assertEqual(sum(tag == "dialog" for tag, _ in self.parser.tags), 1)
        self.assertEqual(len(self.parser.ids), len(set(self.parser.ids)))
        required_ids = {
            "signals",
            "visibility-kpi",
            "funded-case-value",
            "payment-kpi",
            "evidence-dialog",
            "drawer-close",
            "dashboard-announcer",
            "panel-overview",
            "panel-visibility",
            "panel-liquidity",
            "panel-payments",
            "panel-gates",
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
            'document.addEventListener("pointerdown"',
        )
        for token in required:
            self.assertIn(token, self.script)
        self.assertNotIn("new RegExp", self.script)

    def test_metric_guide_has_formulas_sources_and_filtered_context(self) -> None:
        required_sections = (
            'evidenceSection("Definition"',
            'evidenceSection("Calculation"',
            'evidenceSection("Data source"',
            'evidenceSection("Interpretation limit"',
            'evidenceSection("Next action"',
        )
        for token in required_sections:
            self.assertIn(token, self.script)
        self.assertIn(
            "Estimated monthly manual hours = frequency × minutes per instance × manual percentage ÷ 60.",
            self.script,
        )
        self.assertIn("definition.formula", self.script)
        self.assertIn("currentSummary.visibility", self.script)
        self.assertNotIn("dashboardData.visibility.sources", self.script)

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
        self.assertIn("Global baseline · filters do not apply", self.index)

    def test_claims_keep_evidence_boundaries_visible(self) -> None:
        combined = "\n".join((self.index, self.script))
        required = (
            "supplied data, not live operations",
            "Design and test; do not fund or execute yet.",
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
            base = f"http://127.0.0.1:{server.server_port}/dashboard"
            for relative in (
                "/",
                "/styles.css",
                "/filter_model.js",
                "/app.js",
                "/dashboard_data.json",
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
