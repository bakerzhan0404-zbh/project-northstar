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

### Inline decision sections

The main body uses six click-to-open sections: `Portfolio decision`, `Reporting visibility`, `Liquidity`, `Payment friction`, `Capacity evidence`, and `Closure evidence`. All details are collapsed by default, and only one section can be open at a time. Opening another section closes the previous one; clicking the open header collapses it.

Each collapsed row keeps the decision-ready summary and its essential evidence boundary visible. Expanded panels contain the current-scope evidence, interpretation, decision boundary, and next action. Liquidity always keeps `$0` funded-case mobility and `not established` visible; capacity always remains labelled as an enterprise-global management estimate to which filters do not apply.

Why: the default view behaves like an analytical worklist rather than a presentation slide. A user can scan every conclusion first, then open only the evidence needed for the current decision.

### Dashboard search

Search metrics, entities, banks, regions, currencies, or account identifiers. Selecting a metric expands and focuses the matching inline section. Selecting a dimension applies that filter; selecting an account applies its currency, region, entity, and bank context. Searches for definitions, formulas, sources, or methodology open the Metric guide.

Why: search is a navigation and scope shortcut, not an opaque recalculation or a card-hiding mechanism.

### Governed filters

Open `Filters` to select an inclusive date range, currency, region, entity, and bank. Dimension filters combine with `AND` logic and use the same selected account population across visibility, liquidity, payments, and closure candidates.

Why: this tests whether a portfolio-level signal persists in a specific operating scope. Visibility and payments use the selected date range; liquidity uses the selected end date and its complete trailing 7/14-day window; closure candidates use account dimensions; the capacity baseline remains global.

### Liquidity horizon and payment measure

Open `Liquidity` to switch between the governed 7-day and 14-day screens. Open `Payment friction` to switch the same four mutually exclusive cohorts between `Records`, `Exceptions`, and `Repair time`. Each control updates its collapsed summary and open detail panel together.

Why: controls stay next to the evidence they change. The liquidity screen never implies transferability, and the payment numerator, denominator, unit, chart, and explanation move together while the overlap is counted once.

### Metric guide

Open the right-side guide from the top menu or from any expanded section. The guide is methodology-only: `Definition`, `Formula / calculation`, `Data source`, and `Method limit`.

Current filtered values, interpretation, decision boundaries, and next actions remain in the inline sections and are not repeated in the guide.

Why: the page answers “what is happening and what should I do?” while the guide answers “what does this mean and how is it calculated?”

### Reset and keyboard behavior

Reset clears search and filters, restores the full-period, 14-day liquidity and payment-record defaults, and collapses all detail sections.

Native disclosure headers support `Enter` and `Space`. `Up`/`Down` or `Left`/`Right` moves between section headers, `Home`/`End` moves to the first or last header, and `Escape` collapses the open section and returns focus. Interactive targets remain at least 44 px.

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
- `dashboard/app.js` — accordion, search, filter, Metric guide, accessibility, and fail-closed interactions
- `tests/test_dashboard_data.py` — analytical contract tests
- `tests/test_dashboard_filter_model.js` — filter, search, date, and empty-scope tests
- `tests/test_dashboard_ui.py` — structure, accordion exclusivity, keyboard, claim, safety, and local-asset tests
