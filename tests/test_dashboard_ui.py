"""Structural and integration checks for the interactive dashboard UI."""

import functools
import http.server
import json
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


DASHBOARD = ROOT / "dashboard"


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags = []
        self.ids = []
        self.html_attrs = {}
        self.details = []
        self.summaries = []
        self.summary_depth = 0
        self.ids_in_summaries = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        self.tags.append((tag, values))
        if tag == "html":
            self.html_attrs = values
        if tag == "details":
            self.details.append(values)
        if tag == "summary":
            self.summaries.append(values)
            self.summary_depth += 1
        if "id" in values:
            self.ids.append(values["id"])
            if self.summary_depth:
                self.ids_in_summaries.add(values["id"])

    def handle_endtag(self, tag):
        if tag == "summary":
            self.summary_depth -= 1


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
            "detail-decision",
            "detail-visibility",
            "detail-liquidity",
            "detail-payments",
            "detail-capacity",
            "detail-closures",
            "visibility-summary-boundary",
            "liquidity-summary-boundary",
            "liquidity-summary-screen",
            "payment-summary-boundary",
            "closure-summary-boundary",
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

    def test_body_uses_six_native_collapsed_operational_disclosures(self) -> None:
        expected_topics = {
            "decision",
            "visibility",
            "liquidity",
            "payments",
            "capacity",
            "closures",
        }
        self.assertEqual(len(self.parser.details), 6)
        self.assertEqual(len(self.parser.summaries), 6)
        self.assertEqual(
            {details.get("data-inline-detail") for details in self.parser.details},
            expected_topics,
        )
        self.assertTrue(
            all(details.get("name") == "dashboard-detail" for details in self.parser.details)
        )
        self.assertTrue(all("open" not in details for details in self.parser.details))
        self.assertEqual(
            {summary.get("data-detail-summary") for summary in self.parser.summaries},
            expected_topics,
        )
        self.assertTrue(all("role" not in summary for summary in self.parser.summaries))
        self.assertTrue(
            all("aria-expanded" not in summary for summary in self.parser.summaries)
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

        footer = self.index.split('<footer class="evidence-footer">', 1)[1].split(
            "</footer>", 1
        )[0]
        self.assertNotIn("<button", footer)

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

    def test_disclosure_keyboard_search_reset_and_failure_behaviors_are_explicit(self) -> None:
        required = (
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
            "detail.hidden = disabled",
        )
        for token in required:
            self.assertIn(token, self.script)
        self.assertNotIn('summary.setAttribute("aria-expanded"', self.script)
        self.assertNotIn('summary.addEventListener("click"', self.script)

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
const { formatUsdCompact } = require('./dashboard/app.js');
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
            'id: `inline:${topic}`',
            'id: `guide:${topic}`',
        )
        for token in required:
            self.assertIn(token, self.script)
        self.assertNotIn("new RegExp", self.script)

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
const model = require('./dashboard/filter_model.js');
const data = JSON.parse(fs.readFileSync('./dashboard/dashboard_data.json', 'utf8'));
const defaults = model.createDefaultState(data);
const fullPeriod = model.summarize(data, defaults);
const sameEndSingleDay = model.summarize(data, { ...defaults, dateFrom: defaults.dateTo });
process.stdout.write(JSON.stringify({
  sameLiquidity: JSON.stringify(fullPeriod.liquidity) === JSON.stringify(sameEndSingleDay.liquidity),
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
        self.assertTrue(result["sameLiquidity"])
        self.assertNotEqual(result["fullPayments"], result["singleDayPayments"])

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
