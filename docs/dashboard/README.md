# Interactive Dashboard V2

This dashboard turns the concise Figma V2 design into a data-connected diagnostic experience. It reads one governed JSON contract generated from the committed Week 1 and Week 2 processed outputs, including validated account-day and payment facts for filtering.

## Live dashboard

**https://bakerzhan0404-zbh.github.io/project-northstar/dashboard/**

Published from this folder by GitHub Pages (repository Settings → Pages, source: `main` branch, `/docs` folder). The repository is public, so anyone with the link can open it. Every push to `main` that changes this folder republishes the site automatically.

## Open the dashboard locally

From the repository root:

```bash
python3 src/build_dashboard_data.py
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/docs/dashboard/`.

The published site is a static snapshot of this folder: pure HTML, CSS, and JavaScript reading one pre-generated JSON file, with no backend, no build step, and no live connection to any operational system.

## Traceability and export

The header carries a **Last updated** date and a **Data** version, e.g. `2.0+d410f256ec`. The version is a fingerprint of the published payload: it changes whenever any value, label, or boundary changes, so two readers can confirm they are looking at the same numbers. The date is a declared release constant in `src/build_dashboard_data.py`, not a build clock — the build must stay byte-identical for identical inputs, and a wall-clock stamp would break that.

**Export filtered results (CSV)** in the filter toolbar downloads the current scope. Every row carries the applied scope, the evidence boundary that governs it, and the dataset version and date, because an exported file outlives the page it came from. Unestablished values export as `not_established`, never as `0`, and an empty scope exports a stated no-match row rather than a zero. Cells are quoted and leading `=`, `+`, `-`, `@` are neutralised so a spreadsheet cannot execute exported text.

## What is interactive—and why

### The landing page: one recommendation, three KPIs, three actions

The homepage answers three questions in one viewport — *what should we do*, *what does the evidence say*, and *what happens next* — and nothing more. Everything technical moved to the secondary detail pages.

| Element | Shows | Boundary kept visible |
|---|---|---|
| Primary recommendation | The governed decision headline, its next step, and an evidence-strength line | `Three separate signals—not a composite score. Portfolio-wide · filters do not apply.` |
| Three KPIs | Accounts reporting late, gross positive availability, and payment exception rate | Each tile carries its own proxy, mobility, or causation limit |
| Three next actions | The governed `next_action` for visibility, liquidity, and payments, each with its supplied measure | Method next-steps, not an approved workplan, funding decision, or execution authority |
| Start Guided Review | Opens the three-step guided review | — |

Every number is read from the governed JSON contract at render time; none is hard-coded. If the contract fails validation, the recommendation and evidence are removed and only the disabled menu and failure banner remain — the page never shows a conclusion it cannot source.

Why the change: the earlier build presented six menu options, four KPI cards, and four finding cards at once, which asked users to absorb seven conclusions before choosing an investigation. The homepage now summarizes and routes; depth lives one click away.

### Take a tour

`Take a tour` on the homepage launches a **spotlight tour**: the page dims and one real element is highlighted at a time, so a first-time reader learns what they are looking at before being asked to decide anything.

| Step | Highlights | Answers |
|---|---|---|
| 1 | The recommendation band | What is this dashboard recommending? |
| 2 | The evidence-base line | How much weight can that recommendation bear? |
| 3 | The three KPIs | Which measures support it, and what are their limits? |
| 4 | The three next actions | What should happen next? |
| 5 | The view menu | Where do I go deeper? |
| 6 | The filter toolbar | How do I narrow the scope? |
| 7 | The Metric guide button | Where are definitions, formulas, and limits? |

Every step shows `Step N of 7`, progress dots, `Back` (except step 1), `Next` (except the last), and `Skip to Full Dashboard`, available throughout. The last step offers `Start Guided Review`, which hands off to the three-step review below. Escape closes the tour, arrow keys move between steps, focus is trapped in the popover, and page scroll is locked while it runs. A step whose target is missing or collapsed is skipped rather than pointing at nothing, so the tour adapts to viewport and data state.

### Guided review

`Start Guided Review` — and the tour's final step — opens a three-step modal built on the same `<dialog>` pattern as the Metric guide.

1. **Choose the decision** — Cash Visibility, Liquidity, Payments, or Data Quality, as an accessible radiogroup with arrow-key support. Step 1 cannot be advanced until a decision is chosen.
2. **Select the scope** — the same governed date, region, entity, bank, and currency filters the dashboard uses. Selections persist across Back and Next.
3. **Review the answer** — deliberately narrow: one core finding, what the evidence cannot show, one recommended action, and the role whose approval is required. Formulas, methodology, and datasets are *linked*, not inlined.

Each step shows `Step N of 3`, a Back button (except step 1), a Next button (except step 3), and `Skip to Full Dashboard`. The final step offers `View Full Dashboard`, which applies the chosen scope through the same governed filter pipeline the toolbar uses — the review cannot bypass validation or the empty-scope guard.

The approver named in step 3 is an analyst-proposed accountable role, not a recorded client approval.

### Secondary detail pages

Four reference pages hold the technical depth that used to crowd the homepage:

| Page | Contains |
|---|---|
| Calculation formulas | The calculation narrative and formula for all seven governed topics |
| Constraints & limitations | Each topic's method limit — what it may not be used to claim |
| Methodology | What each measure means and the next action its method prescribes |
| Detailed data | Population controls, structural checks, reconciliation controls, source artifacts, and per-topic sources |

They are reachable from the Metric guide drawer, from the homepage constraints link, and from the "Go deeper" links in the guided review answer. Opening one takes over the main area and hides the menu; `Back to dashboard` restores it and returns focus to the trigger.

### Menu navigation

Search, filters, the applied-scope summary, and the Metric guide remain available on the landing page. No analytical view, KPI panel, or evidence table opens until a user chooses one of six views.

| Menu view | Purpose | Content shown | Filter applicability |
|---|---|---|---|
| Executive Overview | Portfolio decision and validation before funding or execution | Portfolio decision | `Portfolio-wide · filters do not apply` |
| Cash Visibility & Liquidity | Reporting delays and governed 7-day and 14-day screening sensitivities | Reporting visibility; Liquidity | `Date + dimensions` |
| Bank Account Footprint | Regional account coverage and closure-validation candidates | Regional footprint; Closure evidence | `Mixed date rules` |
| Payment Operations | Deduplicated cohorts, exceptions, and repair time | Payment friction | `Date + dimensions` |
| Process Workload | Independent management and payment-file workload estimates | Capacity evidence | `Global · filters do not apply` |
| Data Quality & Evidence | Structural checks, controls, governed sources, and certification limits | Governed quality-evidence landing | `Governed contract · filters do not apply` |

A normal menu selection reveals only the mapped content and leaves every analytical section collapsed. Metric search may route directly to a view and open one matching section. Switching views collapses the previous section, while filters and the liquidity/payment control choices remain applied.

Why: selecting a view keeps one investigation on screen at a time, instead of presenting seven conclusions like a slide. The landing brief is deliberately separate from this — it reports the fixed portfolio baseline and cannot be filtered, so it never competes with the filtered evidence inside a view.

### Expanded analytical views

Reference-inspired visuals appear only after a view is selected and an analytical section is opened. They translate governed Week 1–2 evidence into inspectable comparisons; they are not targets, scores, forecasts, or approved value. Data Quality & Evidence is a direct evidence landing with progressive-disclosure details rather than another top-level analytical accordion.

| Section | Expanded evidence | Why this form fits the evidence |
|---|---|---|
| Portfolio decision | Three evidence chips for reporting visibility, liquidity, and payment friction | The chips make separate portfolio signals scannable without combining them into a recommendation or confidence score. The portfolio-wide decision does not change with filters. |
| Reporting visibility | A selected-account composition ring and reporting-method exposure bars | The ring shows delayed and same-day parts of the selected account population; the bars show where source exposure sits. Both describe composition, not target attainment. |
| Liquidity | A selected-horizon account-floor waterfall, unfilled 7-day/14-day screen lines, and an exact-value table | The waterfall makes the governed construction auditable. The lines show modeled sensitivity across supplied dates—not a forecast, surplus-cash series, or transfer authorization. |
| Payment friction | A priority-union composition ring and a 100% stack of four mutually exclusive cohorts | The ring shows how much of the selected measure is in the deduplicated union; the stack shows each cohort's contribution while counting the overlap once. |
| Regional footprint | A schematic CC0 world map with selectable NA, EMEA, and APAC markers plus a reconciled regional table | The map provides spatial orientation and a direct region-filter shortcut. The table supplies the exact account, delayed-reporting, priority-union, and closure-candidate evidence without implying live cash locations or regional performance. |
| Capacity evidence | Two shared-scale comparison bars | The bars compare the management process estimate with the supplied payment-file monthly average without adding them or presenting either as removable labor or cashable savings. |
| Closure evidence | A row-level candidate table | Account, entity, bank, account currency, USD fee estimate, candidate rule, and validation status stay together so every row reads as a validation candidate—not an approved closure. |
| Data Quality & Evidence | Contract status, seven evidence dimensions, a baseline-only monitoring state, population provenance, and a 15-item validation queue | Closed dimension rows keep the landing concise; opening one reveals its definition, grain, rule coverage, evidence limit, proposed owner, source, and next action without inventing a pass-rate score. |

### Data Quality & Evidence

The quality landing reads the governed contract rather than hard-coded fallback values. It shows:

- `Reconciled to supplied controls`
- `Source certification open`
- `52 / 52` Week 1 structural checks passed
- `13 / 13` Week 2 reconciliation controls reconciled
- `12` governed source artifacts
- Population controls for 16 entities, 55 accounts, 9,955 account-days, 7,600 payment records, 1,810 FX rows, and 9 process activities

Its persistent limit is: `Passing internal checks establishes structural consistency and reconciliation only; it does not certify source completeness, semantic accuracy, operational timing, causation, or decision authority.` The displayed next action is to complete source-owner certification and resolve semantic or operational gaps before treating consistency as decision authority.

The 52 Week 1 rules are mapped exactly once across seven evidence dimensions:

| Dimension | Evidence status | Mapped Week 1 rules | Current interpretation |
|---|---|---:|---|
| Uniqueness | `Measured` | 5 | Reproducible internal duplicate/key checks passed for the supplied snapshot. |
| Accuracy | `Not certified` | 0 | No certified source comparison exists; the interface never renders a misleading `0 / 0` pass rate. |
| Consistency | `Partial · proxy` | 15 | Internal relationships reconcile, while source certification and the $3.9bn-versus-$3.8bn boundary remain open. |
| Completeness | `Partial · proxy` | 4 | Supplied-file fields can be tested, but completeness against the authoritative source population is not established. |
| Timeliness | `Partial · proxy` | 1 | The reporting-date proxy is measurable; it is not start-of-day, elapsed-24-hour, or SLA evidence. |
| Currency / freshness | `Not certified` | 2 | The supplied period is known, but no owner-approved freshness policy or continuing refresh history exists. |
| Conformance / validity | `Measured` | 25 | Internal type, domain, schema, and logical checks passed for the supplied snapshot. |

`Measured` means a reproducible internal rule exists for this supplied snapshot—not that an external source has been certified. `Partial · proxy` means some evidence is available but the decision-relevant definition remains incomplete. `Not certified` means no authoritative or owner-approved control supports the claim yet. The 13 Week 2 reconciliation controls remain a separate denominator and are never blended into the 52-rule coverage.

Every dimension is closed by default. Opening one reveals its definition, current evidence, grain and denominator, threshold status, evidence limit, proposed validation owner, next action, sources, and mapped technical rules. `Population & provenance`, `Evidence issues & actions`, and the methodology library are separate closed disclosures. The issue queue preserves DQ-01 through DQ-15 from the Week 1 report—11 High and 4 Medium—as validation and decision-evidence gaps, not as failed structural rules.

The dashboard also states `Baseline only · monitoring history not yet available`. One supplied snapshot cannot establish deterioration, improvement, drift, or a control range; future refreshes can add history only after the same governed checks are rerun. This applies the useful design principles in [Informatica's dimensions-of-data-quality article](https://www.informatica.com/blogs/the-importance-of-high-quality-data-requires-constant-vigilance-dimensions-of-data-quality.html)—dimension-based rules, drill-down, traceability, ownership, and monitoring—without treating the article as project evidence or importing its example scores.

Filters never change this full-contract result. No composite quality score, grade, completeness claim, arbitrary business threshold, or approval is calculated. An incomplete, duplicated, reordered, or contradictory quality contract fails closed and publishes no plausible result.

### Dashboard search

Search is available on the menu page and in every selected view. An exact menu title opens that view. A metric result routes to its owning view and opens its section; `Data Quality & Evidence` routes to the quality landing. Searching a quality dimension, mapped rule key or label, or issue ID such as `Accuracy`, `Timeliness`, or `DQ-11` opens and focuses the matching disclosure. A methodology result opens the Metric guide without changing views.

Selecting a dimension applies that filter without forcing a view change; selecting an account applies its currency, region, entity, and bank context. Exact `NA`, `EMEA`, and `APAC` matches present the region filter first. Search uses literal token matching, not regular-expression evaluation.

Why: search is a navigation and scope shortcut, not an opaque recalculation or a card-hiding mechanism.

### Governed filters

Open `Filters` from the menu or any view to select an inclusive date range, currency, region, entity, and bank. Dimension filters combine with `AND` logic and use the same selected account population across the filter-aware evidence.

Why: this tests whether a portfolio-level signal persists in a specific operating scope. Visibility and payments use the selected date range; liquidity uses the selected end date and its complete trailing 7/14-day window; closure candidates use account dimensions; the capacity baseline remains global.

Applied filters persist as the user moves between views. Visibility and payments use the inclusive period; the liquidity waterfall uses the range end and selected horizon while its trend spans the inclusive range; regional account counts ignore date; closure rows use account dimensions against the fixed 30 June 2026 snapshot. Executive Overview, Process Workload, and Data Quality & Evidence state explicitly that filters do not apply.

### Regional footprint

Choose `Bank Account Footprint`, then open `Regional footprint` to compare the governed NA, EMEA, and APAC classifications. Selecting a map marker or the matching table action applies that region across the dashboard while preserving the current date, currency, entity, bank, liquidity-horizon, and payment-measure choices. The Bank Account Footprint view remains selected and `All regions` clears only the region filter.

The comparison behaves as a region facet: each row temporarily overrides the active region while holding the other filters constant, so alternatives remain visible even after one region is selected. This is labelled comparison behavior, not a fallback to portfolio totals. If an applied region has no matches under the other filters, the closed row says so while the facet can still show comparable alternatives. Matching-account counts use currency, entity, and bank only; delayed-account and payment evidence also uses the inclusive date range; closure candidates remain a fixed 30 June 2026 snapshot. The map never plots liquidity.

Why: the map makes geographic scope easy to navigate, while the reconciled table keeps the evidence exact. Region anchors are schematic business classifications—not bank, account, cash, legal-domicile, or transfer-path locations. On small screens, the decorative map disappears and the same controls become readable region cards.

### Liquidity horizon and payment measure

Choose `Cash Visibility & Liquidity`, then open `Liquidity` to switch the selected waterfall and collapsed summary between the governed 7-day and 14-day screens. The trend continues to compare both horizons across the selected date range, and `View trend data table` exposes the exact daily values. Dates without a complete trailing window remain unavailable and appear as gaps rather than zero.

Choose `Payment Operations`, then open `Payment friction` to switch the ring, 100% cohort stack, legend, numerator, denominator, and collapsed summary together between `Records`, `Exceptions`, and `Repair time`. All four cohorts remain mutually exclusive, so the manual-touch/cross-border overlap is counted once.

Why: controls stay next to the evidence they change. The liquidity views explain modeled construction and date sensitivity without implying transferability; the payment views preserve one selected-scope denominator from summary through detail.

### Metric guide

Open the right-side guide from the top header, an expanded section, or the quality landing. The guide is methodology-only: `Definition`, `Formula / calculation`, `Data source`, and `Method limit`.

Current filtered values, interpretation, decision boundaries, and next actions remain in the inline sections and are not repeated in the guide.

Why: the page answers “what is happening and what should I do?” while the guide answers “what does this mean and how is it calculated?”

### All views, reset, and keyboard behavior

`All views` returns to the six-option menu without clearing filters or analytical toggles and restores focus to the menu choice just left. `Reset dashboard` clears search and filters, restores the full-period, 14-day liquidity and payment-record defaults, closes transient panels, and returns to the menu.

The six view choices are ordinary buttons inside a labelled navigation list. Selected views use `aria-current="page"`; focus moves to the view heading after selection. Native disclosure headers support `Enter` and `Space`; arrow keys and Home/End move between visible headers; Escape collapses the open section. Data-quality dimension and issue disclosures use the same keyboard pattern and collapse when the user switches views, returns to All views, or resets. Regional controls preserve their marker/table keyboard behavior. Interactive targets remain at least 44 px, and hidden views are removed from the accessibility tree.

## Evidence safeguards

- Menu selection changes presentation only; it never recalculates or mutates the governed filter state.
- The quality landing requires the exact 52/52 Week 1 checks, 13/13 Week 2 controls, 12 sources, six population controls, declared provenance, and open-certification boundary. Contradictory values fail closed.
- Passing quality controls are never converted into a score, grade, source-certification claim, or decision authority.
- Every one of the 52 Week 1 rules appears exactly once in the declared seven-dimension mapping; missing, duplicated, reordered, or reassigned rules fail closed.
- Dimension coverage labels describe available evidence, not performance. Accuracy remains `Not certified` and never displays a fabricated zero-denominator rate.
- Week 1 rule coverage and Week 2 reconciliation controls retain separate denominators; they are not combined into a composite quality percentage.
- Monitoring remains explicitly baseline-only until more governed snapshots exist. No trend, improvement, deterioration, target, or control range is inferred from one snapshot.
- The DQ-01–DQ-15 queue reports validation and decision-evidence gaps from the Week 1 issue log; it does not relabel the 52 passing technical checks as failures.
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
- The local map image is decorative, hidden from assistive technology, and hash-pinned; its CC0 provenance is recorded in `docs/dashboard/assets/README.md`.
- Visual meaning is available without color or hover through direct labels, persistent legends, accessible chart descriptions, and semantic tables.

## Refresh and verify

```bash
python3 tests/test_data_quality.py
python3 tests/test_week2_diagnostic.py
python3 tests/test_dashboard_data.py
python3 src/build_dashboard_data.py
node --check docs/dashboard/filter_model.js
node --check docs/dashboard/app.js
node --test tests/test_dashboard_filter_model.js
python3 tests/test_dashboard_ui.py
```

The final UI test opens a temporary loopback server when the environment permits it. In a restricted sandbox, that one HTTP check is skipped; the same assets can be checked against the local preview server.

## Files

- `src/build_dashboard_data.py` — validation and dashboard-data adapter
- `data/processed/W2_dashboard_account_day_facts.csv` — governed visibility and liquidity filter facts
- `data/processed/W2_dashboard_payment_facts.csv` — governed payment filter facts
- `docs/dashboard/dashboard_data.json` — generated governed data, filter, definition, quality-dimension, monitoring, and action-queue contract
- `docs/dashboard/index.html` — simplified landing page, six-view menu, secondary detail pages, guided-review wizard, and semantic dashboard structure
- `docs/dashboard/styles.css` — Figma-aligned responsive design
- `docs/dashboard/assets/world-map.png` — locally vendored decorative CC0 Robinson-projection map raster
- `docs/dashboard/assets/README.md` — map source, author, CC0 license, retrieval date, dimensions, and checksum
- `docs/dashboard/filter_model.js` — deterministic filtering, governed visualization summaries, and search
- `docs/dashboard/app.js` — recommendation and next actions, guided-review wizard, secondary detail pages, six-view navigation, quality drill-down/action queue, accordions, charts, search, filters, Metric guide, accessibility, and fail-closed interactions
- `tests/test_dashboard_data.py` — analytical contract tests
- `tests/test_dashboard_filter_model.js` — filter, visualization reconciliation, search, date, mutation, and empty-scope tests
- `tests/test_dashboard_ui.py` — menu routing, exact quality mappings, adversarial quality mutations, disclosure/search behavior, visualization, keyboard, claim, safety, and local-asset tests
