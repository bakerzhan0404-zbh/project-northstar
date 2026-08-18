# Interactive Dashboard V2

This local dashboard turns the concise Figma V2 design into a data-connected diagnostic experience. It reads one governed JSON contract generated from the committed Week 1 and Week 2 processed outputs, including validated account-day and payment facts for filtering.

## Open the dashboard

From the repository root:

```bash
python3 src/build_dashboard_data.py
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/dashboard/`.

The dashboard is intentionally local and has not been deployed or pushed.

## What is interactive—and why

### Dashboard search

Search metrics, entities, banks, regions, currencies, or account identifiers. Selecting a metric opens the relevant Metric guide topic; selecting a filter value applies that scope.

Why: search is a navigation shortcut, not an opaque recalculation or a card-hiding mechanism.

### Governed filters

Open `Filters` to select an inclusive date range, currency, region, entity, and bank. Dimension filters combine with `AND` logic and use the same selected account population across visibility, liquidity, payments, and closure candidates.

Why: this lets a user test whether a portfolio-level signal persists in a specific operating scope. Visibility and payments use the selected date range; liquidity uses the selected end date and its complete trailing 7/14-day window; closure candidates use account dimensions; the capacity baseline remains global and is labelled accordingly.

### Liquidity horizon

Switch between the 7-day and 14-day modeled screens. The selected screen, illustrative buffer, as-of evidence, and interpretation boundary update together.

Why: this shows sensitivity to the payment-intent horizon without implying transferability. Validated mobility remains `not established`, and the funded case remains `$0`, in both states.

### Payment measure

Switch the same four mutually exclusive cohorts between `Records`, `Exceptions`, and `Repair time`.

Why: the deduplicated priority union represents 37.36% of supplied records but 74.32% of exceptions and 74.40% of repair minutes. The control changes the numerator, denominator, unit, chart, and explanation together. The 342-record overlap is always counted once.

### Metric guide

Open the right-side guide from the top menu, any signal, or either evidence gate. Each topic exposes the definition, calculation and formula, data source, interpretation limit, and next action for the current filtered view.

Why: progressive disclosure keeps the executive view concise while allowing self-service interpretation and auditability.

### Reset

Reset clears search and filters and returns to the full-period, 14-day liquidity, and payment-record defaults.

## Evidence safeguards

- The browser aggregates only governed filter facts; it never reads or recalculates from raw source files.
- The adapter validates exact schemas, keys, dimensions, control totals, cohort reconciliation, evidence labels, and decision boundaries before writing JSON.
- Validated movable cash is serialized as `null` with status `not_established`, never as an observed numeric zero.
- A failed validation leaves no new plausible dashboard result.
- An empty or incomplete filtered scope is shown as unavailable, never as a false zero or a retained portfolio value.
- No free-form threshold sliders, recommendation scores, funding controls, or execution actions are included.
- The snapshot remains limited to supplied data for 1 January–30 June 2026 and is not live operations.

## Refresh and verify

```bash
python3 tests/test_data_quality.py
python3 tests/test_week2_diagnostic.py
python3 tests/test_dashboard_data.py
python3 src/build_dashboard_data.py
node --check dashboard/filter_model.js
node --check dashboard/app.js
node --test tests/test_dashboard_filter_model.js
python3 tests/test_dashboard_ui.py
```

The final UI test opens a temporary loopback server when the environment permits it. In a restricted sandbox, that one HTTP check is skipped; the same assets can be checked against the local preview server.

## Files

- `src/build_dashboard_data.py` — validation and dashboard-data adapter
- `data/processed/W2_dashboard_account_day_facts.csv` — governed visibility and liquidity filter facts
- `data/processed/W2_dashboard_payment_facts.csv` — governed payment filter facts
- `dashboard/dashboard_data.json` — generated governed contract
- `dashboard/index.html` — semantic dashboard structure
- `dashboard/styles.css` — Figma-aligned responsive design
- `dashboard/filter_model.js` — deterministic filtering, summaries, and search
- `dashboard/app.js` — menu interactions, Metric guide, accessibility, and fail-closed loading
- `tests/test_dashboard_data.py` — analytical contract tests
- `tests/test_dashboard_filter_model.js` — filter, search, date, and empty-scope tests
- `tests/test_dashboard_ui.py` — structural, interaction, claim, safety, and local-asset tests
