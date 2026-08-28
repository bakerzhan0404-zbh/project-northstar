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
    DECISION_INPUT_KEYS,
    DIAGNOSTIC_INPUT_KEYS,
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
        # Diagnostic artifacts only: Week 3/4 design files are governed, but
        # they are not measured data and must not inflate this count.
        self.assertEqual(quality["source_artifacts"], len(DIAGNOSTIC_INPUT_KEYS))
        self.assertEqual(quality["source_artifacts"], 12)
        self.assertLess(quality["source_artifacts"], len(INPUT_FILES))
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
                "roadmap",
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
        output = ROOT / "docs" / "dashboard" / "dashboard_data.json"
        existed_before = output.exists()
        first = build_dashboard_data(self.frames)
        second = build_dashboard_data(self.frames)
        self.assertEqual(first, second)
        self.assertEqual(output.exists(), existed_before)

    def test_decision_pack_publishes_the_week_four_execution_plan(self) -> None:
        pack = build_dashboard_data(self.frames)["decision_pack"]

        self.assertEqual(pack["status"], "direction_proposed_no_execution_authority")
        self.assertEqual(pack["recommended_direction"], "Federated coordination")
        self.assertEqual(pack["fallback_direction"], "Local stabilization")
        self.assertEqual(pack["source_artifacts"], 6)

        # Exactly one preferred option, and it led every weighting.
        options = {row["option_id"]: row for row in pack["options"]["rows"]}
        self.assertEqual(len(options), 3)
        self.assertEqual(
            [row["option_id"] for row in pack["options"]["rows"] if row["preferred"]],
            ["federated_coordination"],
        )
        self.assertEqual(options["federated_coordination"]["score"], 87.0)
        self.assertEqual(options["local_stabilization"]["score"], 72.0)
        self.assertEqual(options["globally_coordinated"]["score"], 60.0)
        self.assertEqual(options["federated_coordination"]["sensitivity_wins"], 5)
        self.assertEqual(options["federated_coordination"]["sensitivity_scenarios"], 5)

        # Seven initiatives, ranked without ties, in descending score order.
        initiatives = pack["initiatives"]["rows"]
        self.assertEqual(pack["initiatives"]["count"], 7)
        self.assertEqual([row["priority_rank"] for row in initiatives], list(range(1, 8)))
        self.assertEqual(
            [row["initiative_id"] for row in initiatives],
            ["I01", "I07", "I06", "I03", "I02", "I05", "I04"],
        )
        self.assertEqual(initiatives[0]["priority_score"], 94.0)
        self.assertEqual(initiatives[-1]["priority_score"], 63.0)

        # Every gate is open and none is recorded as passed.
        gates = pack["gates"]
        self.assertEqual([row["gate_id"] for row in gates["rows"]],
                         ["G0", "G1", "G2", "G3", "G4", "G5", "G6"])
        self.assertEqual(gates["open_count"], 7)
        self.assertEqual(gates["passed_count"], 0)
        self.assertTrue(all(row["status"] == "OPEN" for row in gates["rows"]))

        self.assertEqual(pack["roadmap"]["count"], 6)
        self.assertEqual(
            [row["exit_gate"] for row in pack["roadmap"]["rows"]],
            ["G1", "G2", "G3", "G4", "G5", "G6"],
        )

    def test_decision_pack_keeps_value_unrecognized_and_non_additive(self) -> None:
        pack = build_dashboard_data(self.frames)["decision_pack"]
        benefits = pack["benefits"]

        self.assertEqual(benefits["count"], 4)
        self.assertEqual(benefits["recognized_value_usd"], 0)
        self.assertTrue(benefits["aggregation_rule"].startswith("NON-ADDITIVE"))
        self.assertEqual(
            [row["value_category"] for row in benefits["rows"]],
            ["Cash release", "Annual P&L", "Capacity", "Risk reduction"],
        )
        # The central claim of the pack: a diagnostic quantity is not value.
        for row in benefits["rows"]:
            self.assertEqual(row["validated_value_usd"], 0)
            self.assertEqual(row["funded_value_usd"], 0)
            self.assertEqual(row["recognized_value_usd"], 0)
            self.assertTrue(row["recognition_boundary"])

    def test_kpi_baselines_separate_not_established_from_zero(self) -> None:
        pack = build_dashboard_data(self.frames)["decision_pack"]
        kpis = {row["kpi_id"]: row for row in pack["kpis"]["rows"]}

        self.assertEqual(pack["kpis"]["count"], 14)
        # Measured baselines stay tied to the published diagnostic numbers.
        self.assertEqual(kpis["K01"]["baseline"], "58.18")
        self.assertEqual(kpis["K05"]["baseline"], "31.51")
        self.assertEqual(kpis["K06"]["baseline"], "6.30")
        # An unmet evidence rule is null and labelled, never a numeric zero.
        for kpi_id in ("K03", "K08", "K10", "K13"):
            self.assertIsNone(kpis[kpi_id]["baseline"])
            self.assertEqual(kpis[kpi_id]["baseline_display"], "not_established")
        self.assertEqual(pack["kpis"]["established_baselines"], 10)
        self.assertNotIn(0, [row["baseline"] for row in pack["kpis"]["rows"]])

    def test_recognized_benefit_value_fails_closed(self) -> None:
        frames = copy.deepcopy(self.frames)
        mask = frames["w4_benefits"]["benefit_id"].eq("B01")
        frames["w4_benefits"].loc[mask, "recognized_value_usd"] = 35_000_000
        with self.assertRaisesRegex(DashboardDataError, "B01 recognized_value_usd"):
            build_dashboard_data(frames)

    def test_passed_stage_gate_fails_closed(self) -> None:
        frames = copy.deepcopy(self.frames)
        mask = frames["w4_gates"]["gate_id"].eq("G1")
        frames["w4_gates"].loc[mask, "current_status"] = "PASSED"
        with self.assertRaisesRegex(DashboardDataError, "G1 status"):
            build_dashboard_data(frames)

    def test_changed_initiative_priority_fails_closed(self) -> None:
        frames = copy.deepcopy(self.frames)
        mask = frames["w4_initiatives"]["initiative_id"].eq("I04")
        frames["w4_initiatives"].loc[mask, "weighted_priority_score_0_to_100"] = 99
        with self.assertRaisesRegex(DashboardDataError, "I04 priority score"):
            build_dashboard_data(frames)

    def test_second_preferred_option_fails_closed(self) -> None:
        frames = copy.deepcopy(self.frames)
        mask = frames["w3_options"]["option_id"].eq("globally_coordinated")
        frames["w3_options"].loc[mask, "provisional_preferred_option"] = True
        with self.assertRaisesRegex(DashboardDataError, "Exactly one option must be preferred"):
            build_dashboard_data(frames)

    def test_kpi_baseline_drift_from_the_diagnostic_fails_closed(self) -> None:
        frames = copy.deepcopy(self.frames)
        mask = frames["w4_kpis"]["kpi_id"].eq("K01")
        frames["w4_kpis"].loc[mask, "current_baseline"] = "90.00"
        with self.assertRaisesRegex(DashboardDataError, "K01 baseline must stay tied"):
            build_dashboard_data(frames)

    def test_milestone_referencing_unknown_initiative_fails_closed(self) -> None:
        frames = copy.deepcopy(self.frames)
        mask = frames["w4_roadmap"]["milestone_id"].eq("M01")
        frames["w4_roadmap"].loc[mask, "linked_initiatives"] = "I01; I99"
        with self.assertRaisesRegex(DashboardDataError, "unknown initiative"):
            build_dashboard_data(frames)

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
                {
                    "file": filename,
                    "role": role,
                    "stage": (
                        "diagnostic" if role in DIAGNOSTIC_INPUT_KEYS else "decision"
                    ),
                }
                for role, filename in INPUT_FILES.items()
            ],
        )
        self.assertIn(
            {
                "file": "W2_dashboard_account_day_facts.csv",
                "role": "account_day_facts",
                "stage": "diagnostic",
            },
            sources,
        )
        self.assertIn(
            {
                "file": "W4_stage_gates.csv",
                "role": "w4_gates",
                "stage": "decision",
            },
            sources,
        )
        # The two stages must partition the inputs: an unclassified file would
        # otherwise be silently counted as measured diagnostic evidence.
        self.assertEqual(
            set(DIAGNOSTIC_INPUT_KEYS) | set(DECISION_INPUT_KEYS),
            set(INPUT_FILES),
        )
        self.assertEqual(
            set(DIAGNOSTIC_INPUT_KEYS) & set(DECISION_INPUT_KEYS), set()
        )
        self.assertEqual(len(DIAGNOSTIC_INPUT_KEYS), 12)
        self.assertEqual(len(DECISION_INPUT_KEYS), 6)

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
