# Interactive Dashboard V2

This local dashboard turns the concise Figma V2 design into a data-connected diagnostic experience. It reads one governed JSON contract generated from the committed Week 1 and Week 2 processed outputs.

## Open the dashboard

From the repository root:

```bash
python3 src/build_dashboard_data.py
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/dashboard/`.

The dashboard is intentionally local and has not been deployed or pushed.

## What is interactive—and why

### Liquidity horizon

Switch between the 7-day and 14-day modeled screens. The selected screen, illustrative buffer, complete-window evidence, and threshold table update together.

Why: this shows sensitivity to the payment-intent horizon without implying transferability. Validated mobility remains `not established`, and the funded case remains `$0`, in both states.

### Payment measure

Switch the same four mutually exclusive cohorts between `Records`, `Exceptions`, and `Repair time`.

Why: the deduplicated priority union represents 37.36% of supplied records but 74.32% of exceptions and 74.40% of repair minutes. The control changes the numerator, denominator, unit, chart, and explanation together. The 342-record overlap is always counted once.

### Evidence drawer and reporting-source inspection

Open the drawer from any signal or guardrail. Tabs expose `What this means`, `Evidence`, `Decision boundary`, `Next action`, and `Definition & source`. The visibility tab can inspect API, host-to-host, portal, and spreadsheet evidence without changing the global 55-account denominator.

Why: progressive disclosure keeps the executive view concise while allowing self-service interpretation and auditability.

### Reset

Reset returns to the 14-day liquidity screen, payment records, all reporting sources, and the governed default state.

## Evidence safeguards

- The browser selects and formats governed values; it does not recalculate treasury metrics from raw data.
- The adapter validates exact controls, cohort reconciliation, evidence labels, and decision boundaries before writing JSON.
- Validated movable cash is serialized as `null` with status `not_established`, never as an observed numeric zero.
- A failed validation leaves no new plausible dashboard result.
- No arbitrary date filters, threshold sliders, recommendation scores, funding controls, or execution actions are included.
- The snapshot remains limited to supplied data for 1 January–30 June 2026 and is not live operations.

## Refresh and verify

```bash
python3 tests/test_data_quality.py
python3 tests/test_week2_diagnostic.py
python3 tests/test_dashboard_data.py
python3 src/build_dashboard_data.py
node --check dashboard/app.js
python3 tests/test_dashboard_ui.py
```

The final UI test opens a temporary loopback server when the environment permits it. In a restricted sandbox, that one HTTP check is skipped; the same assets can be checked against the local preview server.

## Files

- `src/build_dashboard_data.py` — validation and dashboard-data adapter
- `dashboard/dashboard_data.json` — generated governed contract
- `dashboard/index.html` — semantic dashboard structure
- `dashboard/styles.css` — Figma-aligned responsive design
- `dashboard/app.js` — interactions, evidence drawer, accessibility, and fail-closed loading
- `tests/test_dashboard_data.py` — analytical contract tests
- `tests/test_dashboard_ui.py` — structural, interaction, claim, safety, and local-asset tests
