"""Executable controls for the Week 4 implementation model."""

import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from week4_implementation import (  # noqa: E402
    MODEL_VERSION,
    PROCESSED,
    WEIGHTS,
    build_outputs,
    validate_outputs,
    validate_source_baselines,
    write_outputs,
)


def assertion_raises(callable_object) -> bool:
    try:
        callable_object()
    except AssertionError:
        return True
    return False


def main() -> None:
    validate_source_baselines()
    outputs = build_outputs()
    validate_outputs(outputs)

    assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9
    assert outputs["initiatives"].sort_values("priority_rank").iloc[0]["initiative_id"] in {"I01", "I07"}
    assert outputs["initiatives"]["prerequisites"].str.strip().ne("").all()
    assert outputs["stage_gates"].iloc[3]["gate_id"] == "G3"
    assert outputs["roadmap"].iloc[-1]["timing"] == "Months 13–18"
    assert set(outputs["benefits"]["aggregation_rule"]) == {"NON-ADDITIVE — do not sum categories"}
    assert outputs["kpis"].loc[outputs["kpis"]["kpi_id"] == "K01", "current_baseline"].iloc[0] == "58.18"
    assert set(outputs["initiatives"]["model_version"]) == {MODEL_VERSION}

    unsafe = {key: value.copy() for key, value in outputs.items()}
    unsafe["benefits"].loc[0, "recognized_value_usd"] = "35000000"
    assert assertion_raises(lambda: validate_outputs(unsafe))

    unsafe = {key: value.copy() for key, value in outputs.items()}
    unsafe["stage_gates"].loc[0, "current_status"] = "CLOSED"
    assert assertion_raises(lambda: validate_outputs(unsafe))

    write_outputs(outputs)
    for name in [
        "W4_initiative_portfolio.csv",
        "W4_stage_gates.csv",
        "W4_roadmap_milestones.csv",
        "W4_kpi_dictionary.csv",
        "W4_benefits_tracker.csv",
    ]:
        assert (PROCESSED / name).exists()
        assert len(pd.read_csv(PROCESSED / name, keep_default_na=False)) > 0

    print("Week 4 implementation tests: PASS")


if __name__ == "__main__":
    main()
