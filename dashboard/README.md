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

The main body uses seven click-to-open sections: `Portfolio decision`, `Reporting visibility`, `Liquidity`, `Payment friction`, `Regional footprint`, `Capacity evidence`, and `Closure evidence`. `Regional footprint` is a scope lens—not a performance signal. All details are collapsed by default, and only one section can be open at a time. Opening another section closes the previous one; clicking the open header collapses it.

Each collapsed row keeps the decision-ready summary and its essential evidence boundary visible. Expanded panels contain the current-scope evidence, interpretation, decision boundary, and next action. Liquidity always keeps `$0` funded-case mobility and `not established` visible; capacity always remains labelled as an enterprise-global management estimate to which filters do not apply.

Why: the default view behaves like an analytical worklist rather than a presentation slide. A user can scan every conclusion first, then open only the evidence needed for the current decision.

### Expanded analytical views

Reference-inspired visuals appear only after a section is opened. They translate governed Week 1–2 evidence into inspectable comparisons; they are not targets, scores, forecasts, or approved value.

| Section | Expanded evidence | Why this form fits the evidence |
|---|---|---|
| Portfolio decision | Three evidence chips for reporting visibility, liquidity, and payment friction | The chips make separate portfolio signals scannable without combining them into a recommendation or confidence score. The portfolio-wide decision does not change with filters. |
| Reporting visibility | A selected-account composition ring and reporting-method exposure bars | The ring shows delayed and same-day parts of the selected account population; the bars show where source exposure sits. Both describe composition, not target attainment. |
| Liquidity | A selected-horizon account-floor waterfall, unfilled 7-day/14-day screen lines, and an exact-value table | The waterfall makes the governed construction auditable. The lines show modeled sensitivity across supplied dates—not a forecast, surplus-cash series, or transfer authorization. |
| Payment friction | A priority-union composition ring and a 100% stack of four mutually exclusive cohorts | The ring shows how much of the selected measure is in the deduplicated union; the stack shows each cohort's contribution while counting the overlap once. |
| Regional footprint | A schematic CC0 world map with selectable NA, EMEA, and APAC markers plus a reconciled regional table | The map provides spatial orientation and a direct region-filter shortcut. The table supplies the exact account, delayed-reporting, priority-union, and closure-candidate evidence without implying live cash locations or regional performance. |
| Capacity evidence | Two shared-scale comparison bars | The bars compare the management process estimate with the supplied payment-file monthly average without adding them or presenting either as removable labor or cashable savings. |
| Closure evidence | A row-level candidate table | Account, entity, bank, account currency, USD fee estimate, candidate rule, and validation status stay together so every row reads as a validation candidate—not an approved closure. |

### Dashboard search

Search metrics, entities, banks, regions, currencies, or account identifiers. Selecting a metric expands and focuses the matching inline section. Selecting a dimension applies that filter; selecting an account applies its currency, region, entity, and bank context. Exact `NA`, `EMEA`, and `APAC` matches present the region filter first; `Regional footprint`, `region overview`, or `map` opens the scope lens. Searches for definitions, formulas, sources, or methodology open the Metric guide.

Why: search is a navigation and scope shortcut, not an opaque recalculation or a card-hiding mechanism.

### Governed filters

Open `Filters` to select an inclusive date range, currency, region, entity, and bank. Dimension filters combine with `AND` logic and use the same selected account population across visibility, liquidity, payments, and closure candidates.

Why: this tests whether a portfolio-level signal persists in a specific operating scope. Visibility and payments use the selected date range; liquidity uses the selected end date and its complete trailing 7/14-day window; closure candidates use account dimensions; the capacity baseline remains global.

Applied filters update the closed summaries and every open visual atomically: visibility composition/source bars and payment composition use the inclusive period, the liquidity waterfall uses the range end and selected horizon while its trend spans the inclusive range, closure rows use account dimensions only, and capacity remains global.

### Regional footprint

Open `Regional footprint` to compare the governed NA, EMEA, and APAC classifications. Selecting a map marker or the matching table action applies that region across the dashboard while preserving the current date, currency, entity, bank, liquidity-horizon, and payment-measure choices. `All regions` clears only the region filter.

The comparison behaves as a region facet: each row temporarily overrides the active region while holding the other filters constant, so alternatives remain visible even after one region is selected. This is labelled comparison behavior, not a fallback to portfolio totals. If an applied region has no matches under the other filters, the closed row says so while the facet can still show comparable alternatives. Matching-account counts use currency, entity, and bank only; delayed-account and payment evidence also uses the inclusive date range; closure candidates remain a fixed 30 June 2026 snapshot. The map never plots liquidity.

Why: the map makes geographic scope easy to navigate, while the reconciled table keeps the evidence exact. Region anchors are schematic business classifications—not bank, account, cash, legal-domicile, or transfer-path locations. On small screens, the decorative map disappears and the same controls become readable region cards.

### Liquidity horizon and payment measure

Open `Liquidity` to switch the selected waterfall and collapsed summary between the governed 7-day and 14-day screens. The trend continues to compare both horizons across the selected date range, and `View trend data table` exposes the exact daily values. Dates without a complete trailing window remain unavailable and appear as gaps rather than zero.

Open `Payment friction` to switch the ring, 100% cohort stack, legend, numerator, denominator, and collapsed summary together between `Records`, `Exceptions`, and `Repair time`. All four cohorts remain mutually exclusive, so the manual-touch/cross-border overlap is counted once.

Why: controls stay next to the evidence they change. The liquidity views explain modeled construction and date sensitivity without implying transferability; the payment views preserve one selected-scope denominator from summary through detail.

### Metric guide

Open the right-side guide from the top menu or from any expanded section. The guide is methodology-only: `Definition`, `Formula / calculation`, `Data source`, and `Method limit`.

Current filtered values, interpretation, decision boundaries, and next actions remain in the inline sections and are not repeated in the guide.

Why: the page answers “what is happening and what should I do?” while the guide answers “what does this mean and how is it calculated?”

### Reset and keyboard behavior

Reset clears search and filters, restores the full-period, 14-day liquidity and payment-record defaults, and collapses all detail sections.

Native disclosure headers support `Enter` and `Space`. `Up`/`Down` or `Left`/`Right` moves between section headers, `Home`/`End` moves to the first or last header, and `Escape` collapses the open section and returns focus. Within Regional footprint, `Tab` reaches `All regions`, marker controls, and table actions; marker arrow keys move focus, Home/End moves to the first or last marker, and Enter/Space applies the focused region. Exact values and actions are repeated in a semantic table. Interactive targets remain at least 44 px.

## Evidence safeguards

- The browser aggregates only governed filter facts; it never reads or recalculates from raw source files.
- The adapter validates exact schemas, keys, dimensions, control totals, cohort reconciliation, evidence labels, and decision boundaries before writing JSON.
- Validated movable cash is serialized as `null` with status `not_established`, never as an observed numeric zero.
- A failed validation leaves no new plausible dashboard result.
- An empty or incomplete filtered scope is shown as unavailable, never as a false zero or a retained portfolio value.
- No free-form threshold sliders, recommendation scores, funding controls, or execution actions are included.
- The snapshot remains limited to supplied data for 1 January–30 June 2026 and is not live operations.
- Every result is derived from a governed filter-model summary. Standard result views use the applied scope; Regional footprint rows explicitly override only region while retaining the other applied filters, and label that comparison basis in the interface.
- Composition rings show a numerator and denominator and are labelled as composition, never as a score, grade, or target.
- The liquidity waterfall uses the effective buffer deduction after account-level floors and reconciles to the selected modeled screen; the raw buffer is not substituted for that deduction.
- Liquidity lines are unfilled and retain gaps for incomplete 7-day or 14-day windows. A semantic table provides exact values; missing values are never plotted as zero.
- Payment cohort segments reconcile to the selected measure. Persistent labels show cohort, value, and share, and the overlap remains its own mutually exclusive cohort.
- Capacity bars remain independent, share a scale, and are never additive. Filters do not apply to this enterprise-global comparison.
- Closure rows remain `Candidate only · not approved`; local purpose, dependencies, continuity, closure cost, and fee removal remain unvalidated.
- Regional rows reconcile to the same governed facet scope. The map uses neutral category colors, never a regional score, rank, risk heatmap, live-cash marker, or transfer path.
- The local map image is decorative, hidden from assistive technology, and hash-pinned; its CC0 provenance is recorded in `dashboard/assets/README.md`.
- Visual meaning is available without color or hover through direct labels, persistent legends, accessible chart descriptions, and semantic tables.

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
- `dashboard/assets/world-map.png` — locally vendored decorative CC0 Robinson-projection map raster
- `dashboard/assets/README.md` — map source, author, CC0 license, retrieval date, dimensions, and checksum
- `dashboard/filter_model.js` — deterministic filtering, governed visualization summaries, and search
- `dashboard/app.js` — accordion, charts, search, filters, Metric guide, accessibility, and fail-closed interactions
- `tests/test_dashboard_data.py` — analytical contract tests
- `tests/test_dashboard_filter_model.js` — filter, visualization reconciliation, search, date, mutation, and empty-scope tests
- `tests/test_dashboard_ui.py` — structure, visualization, accordion, keyboard, claim, safety, and local-asset tests
