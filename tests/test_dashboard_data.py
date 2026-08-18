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
    build_dashboard_data,
    load_dashboard_inputs,
    write_dashboard_data,
)


class DashboardDataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.frames = load_dashboard_inputs(ROOT / "data" / "processed")

    def test_build_exposes_interactive_evidence_without_inventing_mobility(self) -> None:
        payload = build_dashboard_data(self.frames)

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
        del frames["visibility"]
        with self.assertRaisesRegex(DashboardDataError, "Missing loaded dashboard input"):
            build_dashboard_data(frames)

    def test_atomic_writer_emits_strict_json(self) -> None:
        payload = build_dashboard_data(self.frames)
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "dashboard" / "dashboard_data.json"
            result = write_dashboard_data(payload, destination)
            self.assertEqual(result, destination)
            self.assertEqual(json.loads(destination.read_text()), payload)
            self.assertEqual(list(destination.parent.glob("*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
