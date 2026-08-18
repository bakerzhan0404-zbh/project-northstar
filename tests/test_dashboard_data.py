"""Tests for the fail-closed interactive-dashboard data adapter."""

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from build_dashboard_data import (  # noqa: E402
    DashboardDataError,
    INPUT_FILES,
    build_dashboard_data,
    load_dashboard_inputs,
    write_dashboard_data,
)


def decode_compact_table(table):
    return [dict(zip(table["columns"], row)) for row in table["rows"]]


class DashboardDataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.frames = load_dashboard_inputs(ROOT / "data" / "processed")

    def test_build_exposes_interactive_evidence_without_inventing_mobility(self) -> None:
        payload = build_dashboard_data(self.frames)

        self.assertEqual(payload["schema_version"], "2.0")
        self.assertEqual(payload["visibility"]["delayed_accounts"], 23)
        self.assertEqual(len(payload["visibility"]["sources"]), 4)
        self.assertEqual(payload["liquidity"]["scenarios"]["7"]["screen_usd"], 42844787.78)
        self.assertEqual(payload["liquidity"]["scenarios"]["14"]["screen_usd"], 38127490.73)
        self.assertEqual(
            payload["liquidity"]["scenarios"]["14"]["thresholds"]["base"],
            {
                "threshold_usd": 35000000.0,
                "complete_windows": 168,
                "windows_met": 138,
                "met_rate_pct": 82.14,
                "minimum_screen_usd": 31277959.18,
                "median_screen_usd": 36667187.11,
                "evidence_label": "ANALYST-CALC / ANALYST-ASSUMPTION",
                "decision_boundary": (
                    "Scenario screen only; no threshold is validated movable cash"
                ),
            },
        )
        self.assertEqual(
            set(payload["liquidity"]["scenarios"]["7"]["thresholds"]),
            {"stress", "base", "upside"},
        )
        self.assertEqual(
            set(payload["liquidity"]["scenarios"]["14"]["thresholds"]),
            {"stress", "base", "upside"},
        )
        self.assertEqual(
            [row["key"] for row in payload["liquidity"]["evidence_ladder"]],
            [
                "gross_positive_estimated_availability",
                "preliminary_restrictions",
                "negative_positions",
                "apparent_net_before_buffer",
            ],
        )
        self.assertEqual(
            [row["value_usd"] for row in payload["liquidity"]["evidence_ladder"]],
            [57801215.46, 8053700.97, -2138293.09, 47609221.4],
        )
        self.assertEqual(
            [
                row["waterfall_delta_usd"]
                for row in payload["liquidity"]["evidence_ladder"]
            ],
            [57801215.46, -8053700.97, -2138293.09, None],
        )
        self.assertIsNone(payload["liquidity"]["validated_mobility"]["value_usd"])
        self.assertEqual(
            payload["liquidity"]["validated_mobility"]["status"],
            "not_established",
        )
        self.assertEqual(payload["liquidity"]["funded_case"]["display"], "$0")
        self.assertEqual(payload["payments"]["priority_union"]["records"], 2839)
        self.assertEqual(payload["payments"]["priority_union"]["exceptions"], 356)
        self.assertEqual(
            payload["payments"]["priority_union"]["repair_contribution_pct"],
            74.4,
        )
        self.assertEqual(len(payload["payments"]["cohorts"]), 4)
        self.assertEqual(
            payload["guardrails"]["capacity"]["process_to_payment_ratio"],
            1.8394,
        )
        self.assertEqual(
            payload["guardrails"]["closures"]["estimated_annual_fees_usd"],
            7800.0,
        )

    def test_quality_summary_uses_governed_checks_and_controls(self) -> None:
        quality = build_dashboard_data(self.frames)["quality"]
        self.assertEqual(
            quality["status"],
            "reconciled_to_supplied_controls_source_certification_open",
        )
        self.assertEqual(
            quality["w1_checks"],
            {
                "passed": 52,
                "total": 52,
                "label": "Week 1 structural checks",
            },
        )
        self.assertEqual(
            quality["w2_controls"],
            {
                "reconciled": 13,
                "total": 13,
                "label": "Week 2 reconciliation controls",
            },
        )
        self.assertEqual(quality["source_artifacts"], len(INPUT_FILES))
        self.assertEqual(
            [(row["key"], row["value"]) for row in quality["population_controls"]],
            [
                ("entities", 16),
                ("accounts", 55),
                ("balance_observations", 9955),
                ("payment_records", 7600),
                ("fx_rows", 1810),
                ("process_activities", 9),
            ],
        )
        self.assertIn(
            "does not certify source completeness", quality["decision_boundary"]
        )

        dimensions = quality["dimensions"]
        self.assertEqual(
            [dimension["key"] for dimension in dimensions],
            [
                "uniqueness",
                "accuracy",
                "consistency",
                "completeness",
                "timeliness",
                "currency",
                "conformance",
            ],
        )
        self.assertEqual(
            {dimension["key"]: dimension["status"] for dimension in dimensions},
            {
                "uniqueness": "measured",
                "accuracy": "not_certified",
                "consistency": "partial_proxy",
                "completeness": "partial_proxy",
                "timeliness": "partial_proxy",
                "currency": "not_certified",
                "conformance": "measured",
            },
        )
        self.assertEqual(
            {dimension["key"]: dimension["measured_rules"] for dimension in dimensions},
            {
                "uniqueness": 5,
                "accuracy": 0,
                "consistency": 15,
                "completeness": 4,
                "timeliness": 1,
                "currency": 2,
                "conformance": 25,
            },
        )
        mapped_rules = [
            rule["key"]
            for dimension in dimensions
            for rule in dimension["rules"]
        ]
        self.assertEqual(len(mapped_rules), 52)
        self.assertEqual(len(set(mapped_rules)), 52)
        self.assertTrue(all(rule["result"] == "pass" for dimension in dimensions for rule in dimension["rules"]))
        self.assertEqual(
            quality["monitoring"],
            {
                "status": "baseline_only",
                "label": "Baseline only · monitoring history not yet available",
                "period_start": "2026-01-01",
                "period_end": "2026-06-30",
                "snapshots": 1,
                "boundary": (
                    "One supplied diagnostic snapshot cannot establish a quality trend, "
                    "control range, or improvement trajectory."
                ),
            },
        )
        self.assertEqual(len(quality["issue_queue"]), 15)
        self.assertEqual(
            [issue["id"] for issue in quality["issue_queue"]],
            [f"DQ-{index:02d}" for index in range(1, 16)],
        )
        self.assertEqual(quality["issue_source"], "W1_data_quality_report.md · Appendix A")

    def test_quality_dimensions_fail_closed_when_check_inventory_changes(self) -> None:
        frames = copy.deepcopy(self.frames)
        frames["w1_checks"].loc[0, "check"] = "unexpected_replacement_check"
        with self.assertRaisesRegex(DashboardDataError, "quality-dimension mapping changed"):
            build_dashboard_data(frames)

    def test_filter_catalog_preserves_na_and_control_counts(self) -> None:
        self.assertIn("NA", set(self.frames["accounts"]["region"]))
        self.assertFalse(self.frames["accounts"]["region"].isna().any())
        self.assertIn("NA", set(self.frames["account_day_facts"]["region"]))
        payload = build_dashboard_data(self.frames)
        filtering = payload["filtering"]
        accounts = filtering["dimensions"]["accounts"]
        catalog = filtering["catalog"]

        self.assertEqual(len(accounts), 55)
        self.assertEqual(
            list(accounts[0]),
            [
                "account_id",
                "entity_id",
                "entity_name",
                "region",
                "currency",
                "bank_name",
                "visibility_method",
                "closure_validation_candidate",
                "annual_fee_usd",
            ],
        )
        self.assertEqual({row["region"] for row in accounts}, {"APAC", "EMEA", "NA"})
        self.assertEqual(
            catalog["dates"],
            {
                "min": "2026-01-01",
                "max": "2026-06-30",
                "default_from": "2026-01-01",
                "default_to": "2026-06-30",
                "count": 181,
                "selection": "inclusive_range",
            },
        )
        self.assertEqual(catalog["currencies"]["count"], 10)
        self.assertEqual(catalog["regions"]["count"], 3)
        self.assertEqual(catalog["entities"]["count"], 16)
        self.assertEqual(catalog["banks"]["count"], 5)
        self.assertEqual(
            {row["value"] for row in catalog["regions"]["options"]},
            {"APAC", "EMEA", "NA"},
        )
        self.assertEqual(
            sum(row["account_count"] for row in catalog["currencies"]["options"]),
            55,
        )
        self.assertEqual(
            catalog["applicability"]["liquidity"]["date_mode"],
            "as_of_range_end",
        )
        self.assertEqual(
            catalog["applicability"]["capacity"]["dimensions"], []
        )

    def test_compact_filter_facts_reconcile_to_baseline(self) -> None:
        payload = build_dashboard_data(self.frames)
        facts = payload["filtering"]["facts"]
        self.assertEqual(
            facts["account_days"]["columns"],
            [
                "date",
                "account_id",
                "reporting_delay_days",
                "positive_available_usd",
                "restricted_positive_available_usd",
                "negative_available_usd",
                "unflagged_payment_buffer_7d_usd",
                "net_screen_contribution_7d_usd",
                "unflagged_payment_buffer_14d_usd",
                "net_screen_contribution_14d_usd",
            ],
        )
        self.assertEqual(
            facts["payments"]["columns"],
            [
                "date",
                "account_id",
                "priority_cohort",
                "exception_flag",
                "repair_minutes",
            ],
        )
        account_days = decode_compact_table(facts["account_days"])
        payment_facts = decode_compact_table(facts["payments"])
        self.assertEqual(len(account_days), 9955)
        self.assertEqual(len(payment_facts), 7600)
        self.assertIsNone(account_days[0]["net_screen_contribution_7d_usd"])
        self.assertIsNone(account_days[0]["net_screen_contribution_14d_usd"])

        latest = [row for row in account_days if row["date"] == "2026-06-30"]
        self.assertEqual(len(latest), 55)
        self.assertEqual(
            round(sum(row["net_screen_contribution_7d_usd"] for row in latest), 2),
            42844787.78,
        )
        self.assertEqual(
            round(sum(row["net_screen_contribution_14d_usd"] for row in latest), 2),
            38127490.73,
        )
        self.assertEqual(
            sum(row["exception_flag"] for row in payment_facts), 479
        )
        self.assertEqual(
            sum(row["repair_minutes"] for row in payment_facts), 20080
        )

    def test_definitions_have_user_facing_evidence_fields(self) -> None:
        definitions = build_dashboard_data(self.frames)["definitions"]
        self.assertEqual(
            set(definitions),
            {
                "overview",
                "quality",
                "visibility",
                "liquidity",
                "payments",
                "regions",
                "gates",
            },
        )
        required = {
            "title",
            "meaning",
            "calculation",
            "formula",
            "sources",
            "boundary",
            "next_action",
            "search_aliases",
        }
        for definition in definitions.values():
            self.assertEqual(set(definition), required)
            self.assertTrue(definition["sources"])
            self.assertTrue(definition["search_aliases"])

    def test_build_is_deterministic_and_does_not_write(self) -> None:
        output = ROOT / "dashboard" / "dashboard_data.json"
        existed_before = output.exists()
        first = build_dashboard_data(self.frames)
        second = build_dashboard_data(self.frames)
        self.assertEqual(first, second)
        self.assertEqual(output.exists(), existed_before)

    def test_changed_control_total_fails_closed(self) -> None:
        frames = copy.deepcopy(self.frames)
        mask = frames["w2_reconciliation"]["metric"].eq("payment_records")
        frames["w2_reconciliation"].loc[mask, "value"] = 7599
        with self.assertRaisesRegex(DashboardDataError, "payment_records changed"):
            build_dashboard_data(frames)

    def test_changed_boundary_fails_closed(self) -> None:
        frames = copy.deepcopy(self.frames)
        mask = frames["payments"]["dimension"].eq("overall")
        frames["payments"].loc[mask, "decision_boundary"] = "No limitation"
        with self.assertRaisesRegex(DashboardDataError, "payments overall boundary changed"):
            build_dashboard_data(frames)

    def test_numeric_validated_mobility_fails_closed(self) -> None:
        frames = copy.deepcopy(self.frames)
        mask = frames["liquidity_scenarios"]["metric"].eq(
            "validated_movable_cash"
        )
        frames["liquidity_scenarios"].loc[mask, "value_usd"] = 0
        with self.assertRaisesRegex(
            DashboardDataError,
            "validated movable cash must be null/not established",
        ):
            build_dashboard_data(frames)

    def test_changed_liquidity_ladder_value_fails_closed(self) -> None:
        frames = copy.deepcopy(self.frames)
        mask = frames["liquidity_scenarios"]["metric"].eq(
            "preliminarily_restricted_positive_available_balance"
        )
        frames["liquidity_scenarios"].loc[mask, "value_usd"] = 8053700.96
        with self.assertRaisesRegex(
            DashboardDataError,
            "preliminarily_restricted_positive_available_balance changed",
        ):
            build_dashboard_data(frames)

    def test_changed_threshold_evidence_fails_closed(self) -> None:
        frames = copy.deepcopy(self.frames)
        mask = (
            frames["liquidity_thresholds"]["buffer_window_days"].eq(14)
            & frames["liquidity_thresholds"]["threshold_name"].eq("upside")
        )
        frames["liquidity_thresholds"].loc[
            mask, "median_net_scenario_surplus_usd"
        ] = 1
        with self.assertRaisesRegex(
            DashboardDataError,
            "14-day upside median_net_scenario_surplus_usd changed",
        ):
            build_dashboard_data(frames)

    def test_missing_input_fails_closed(self) -> None:
        frames = dict(self.frames)
        del frames["account_day_facts"]
        with self.assertRaisesRegex(DashboardDataError, "Missing loaded dashboard input"):
            build_dashboard_data(frames)

    def test_duplicate_account_day_fact_fails_closed(self) -> None:
        frames = copy.deepcopy(self.frames)
        facts = frames["account_day_facts"]
        dimension_columns = [
            "account_id",
            "entity_id",
            "entity_name",
            "region",
            "currency",
            "bank_name",
            "visibility_method",
        ]
        facts.loc[facts.index[1], dimension_columns] = facts.loc[
            facts.index[0], dimension_columns
        ].values
        with self.assertRaisesRegex(DashboardDataError, "keys are not unique"):
            build_dashboard_data(frames)

    def test_mutated_payment_cohort_fails_closed(self) -> None:
        frames = copy.deepcopy(self.frames)
        frames["payment_facts"].loc[
            frames["payment_facts"].index[0], "priority_payment_cohort"
        ] = "Unknown cohort"
        with self.assertRaisesRegex(DashboardDataError, "cohort domain changed"):
            build_dashboard_data(frames)

    def test_mismatched_fact_dimension_fails_closed(self) -> None:
        frames = copy.deepcopy(self.frames)
        frames["account_day_facts"].loc[
            frames["account_day_facts"].index[0], "region"
        ] = "EMEA"
        with self.assertRaisesRegex(
            DashboardDataError, "region differs from the account diagnostic"
        ):
            build_dashboard_data(frames)

    def test_nonfinite_filter_fact_fails_closed(self) -> None:
        frames = copy.deepcopy(self.frames)
        frames["account_day_facts"].loc[
            frames["account_day_facts"].index[0], "positive_available_usd"
        ] = float("inf")
        with self.assertRaisesRegex(DashboardDataError, "finite values"):
            build_dashboard_data(frames)

    def test_source_list_includes_every_governed_input(self) -> None:
        sources = build_dashboard_data(self.frames)["sources"]
        self.assertEqual(
            sources,
            [
                {"file": filename, "role": role}
                for role, filename in INPUT_FILES.items()
            ],
        )
        self.assertIn(
            {"file": "W2_dashboard_account_day_facts.csv", "role": "account_day_facts"},
            sources,
        )
        self.assertIn(
            {"file": "W2_dashboard_payment_facts.csv", "role": "payment_facts"},
            sources,
        )

    def test_atomic_writer_emits_strict_json(self) -> None:
        payload = build_dashboard_data(self.frames)
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "dashboard" / "dashboard_data.json"
            result = write_dashboard_data(payload, destination)
            self.assertEqual(result, destination)
            serialized = destination.read_text(encoding="utf-8")
            self.assertEqual(json.loads(serialized), payload)
            self.assertEqual(serialized.count("\n"), 1)
            self.assertNotIn("NaN", serialized)
            self.assertNotIn("Infinity", serialized)
            self.assertLess(destination.stat().st_size, 2_500_000)
            self.assertEqual(list(destination.parent.glob("*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
