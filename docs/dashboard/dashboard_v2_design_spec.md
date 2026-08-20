# Dashboard V2 Design Specification

**Prepared by:** Baker | **Date:** 18 August 2026 | **Status:** Interactive local dashboard implemented and validated

**Artifact scope:** This is the second visual-design iteration of the Version 1 dashboard. It does not replace the validated and repeatable pipeline described as Version 2 in the development plan.

## Objective

Turn the evidence-complete Version 1 reference into a menu-first analytical application: the first viewport asks which decision, operating scope, or evidence question to inspect, then reveals only the selected governed content without requiring a presenter.

## Menu-first application shell

### Persistent header

- `Project Northstar`
- `Treasury decision dashboard`
- Current governed scope and reconciliation status
- Search: `Search metrics, entities, banks…`
- Control: `Filters` with date, currency, region, entity, and bank
- Control: `Metric guide`

### Initial menu-only state

The main region initially shows only:

- Eyebrow: `Dashboard menu`
- Heading: `Choose a dashboard view`
- Support: `Start with one decision, operating scope, or evidence question.`
- The six choices below

No KPI, accordion, analytical chart, warning, or evidence table is visible until a view is selected.

| Menu view | Supporting copy | Content | Applicability |
|---|---|---|---|
| Executive Overview | `Portfolio decision and the validation needed before funding or execution.` | Portfolio decision | `Portfolio-wide · filters do not apply` |
| Cash Visibility & Liquidity | `Reporting delays and governed 7-day and 14-day screening sensitivities.` | Reporting visibility; Liquidity | `Date + dimensions` |
| Bank Account Footprint | `Regional account coverage and closure-validation candidates.` | Regional footprint; Closure evidence | `Mixed date rules` |
| Payment Operations | `Deduplicated payment cohorts, exceptions, and repair time.` | Payment friction | `Date + dimensions` |
| Process Workload | `Independent management and payment-file workload estimates.` | Capacity evidence | `Global · filters do not apply` |
| Data Quality & Evidence | `Structural checks, reconciliation controls, source artifacts, and open certification limits.` | Governed quality-evidence landing | `Governed contract · filters do not apply` |

### Selected-view state

A selected view replaces the menu in the main region and begins with `All views`, the exact menu title, its supporting copy, and its applicability label. Only mapped content is exposed. A normal menu selection leaves all mapped analytical sections collapsed; search may route to a view and open one exact section. Switching views closes the prior section without changing filters, the 7/14-day choice, or the Records/Exceptions/Repair time choice.

Within a selected analytical view, only one of its visible sections may be open at a time. `All views` preserves data scope and returns focus to the menu choice just left. `Reset dashboard` clears filters/search, restores full-period/14-day/Records defaults, closes transient panels, and returns to the initial menu.

### Governed Data Quality & Evidence landing

This view is a result landing rather than an eighth accordion. It displays:

- `Reconciled to supplied controls`
- `Source certification open`
- `52 / 52` Week 1 structural checks passed
- `13 / 13` Week 2 reconciliation controls reconciled
- `12` governed source artifacts
- Population controls: 16 entities; 55 accounts; 9,955 account-days; 7,600 payment records; 1,810 FX rows; 9 process activities
- Boundary: `Passing internal checks establishes structural consistency and reconciliation only; it does not certify source completeness, semantic accuracy, operational timing, causation, or decision authority`
- Next action: complete source-owner certification and resolve semantic or operational gaps before treating consistency as decision authority
- Action: `Open data-quality method`

The quality result is full-contract and filter-independent. The browser validates the exact governed counts, labels, population controls, provenance, source count, and boundary before rendering it. Do not derive a score, grade, completeness claim, certification, confidence label, or approval from passing controls.

### Analytical disclosures after view selection

| Menu view | Section | Always-visible result | Supporting boundary |
|---|---|---|---|
| Executive Overview | Portfolio decision | `Design and test; do not fund or execute yet.` | Portfolio-wide; separate signals, not a composite score |
| Cash Visibility & Liquidity | Reporting visibility | `23 / 55 accounts delayed` at baseline | Calendar-date proxy; not start-of-day or elapsed-24-hour visibility |
| Cash Visibility & Liquidity | Liquidity | `$0 funded case`; 14-day screen `$38.13m` at baseline | Mobility not established; screen is not surplus cash or transfer authority |
| Bank Account Footprint | Regional footprint | `3 regions represented`; `55 selected accounts` at baseline | Schematic supplied classification; not a live or precise location map |
| Bank Account Footprint | Closure evidence | `4 validation candidates`; `$7.8k` estimated annual fees | Fixed 30 Jun snapshot; not approved closures or booked savings |
| Payment Operations | Payment friction | `37.36%`; `2,839 / 7,600` records at baseline | Supplied records; overlap counted once; association is not causation |
| Process Workload | Capacity evidence | `102.6 h/month vs 55.8 h/month` | Global estimates; filters do not apply; independent, non-additive, not fundable |

## Expanded analytical-view specification

The visual language takes the useful hierarchy and density of the supplied dashboard references while preserving the limits of the Week 1–2 evidence. Visuals appear only after a menu view is selected and its analytical section is opened; the initial menu remains free of results.

| Section | Expanded visual and role | Interaction and scope | Required evidence boundary |
|---|---|---|---|
| Portfolio decision | Three portfolio evidence chips headed `Three signals remain separate` | The chips remain portfolio-wide and filter-independent | Always show `Separate signals—not a composite score.` No weighting, recommendation score, or confidence score is calculated. |
| Reporting visibility | `Account visibility composition` ring beside filtered reporting-method exposure bars | Inclusive From/To dates plus currency, region, entity, and bank update the ring, bars, interpretation, and summary | Show delayed accounts over selected accounts and `Calendar-date proxy · not start-of-day or elapsed-24-hour visibility`. The ring is composition, not target attainment. Action copy must follow the delayed methods present in the selected scope. |
| Liquidity | Selected 7-day/14-day `Account-floor waterfall`, followed by solid 7-day and dashed 14-day daily screen lines plus `View trend data table` | Dimension filters select accounts. To supplies the waterfall as-of date; the horizon control changes the waterfall and summary. The trend spans the inclusive selected range and retains both horizons. | Gross positive estimate − preliminary restrictions + negative positions − effective buffer after account-level floors = modeled screen. Use the effective deduction, not the raw buffer. Trend gaps mean incomplete trailing windows. Always show `$0` funded case, mobility `not established`, and screening-only language. No area fill, forecast, goal, or performance arrow. |
| Payment friction | Priority-union composition ring beside a 100% stack for Manual only, Manual + cross-border wire, Cross-border wire only, and Neither | Records/Exceptions/Repair time updates the ring, stack, persistent legend, numerator, denominator, and summary from the same filtered rows | The stack denominator is all matching selected-measure evidence; all four cohorts reconcile to it. The overlap is one mutually exclusive cohort and is counted once. Keep supplied-extract and association-not-causation boundaries visible. |
| Regional footprint | Schematic world map with selectable NA, EMEA, and APAC markers plus a semantic regional comparison table | Each regional row overrides the active region while date, currency, entity, and bank remain applied. A marker or table action sets the region across the dashboard; `All regions` clears only region. | Treat markers as business-region classifications, not precise bank, account, cash, legal-domicile, or transfer-path locations. Do not plot liquidity, rank regions, or introduce risk/performance colors. Matching accounts ignore the date filter; delayed/payment evidence uses the inclusive period; closures use the fixed 30 Jun 2026 snapshot. |
| Capacity evidence | Shared-scale bars comparing the management process estimate with the supplied payment-file monthly average | Filters never apply; both bars remain enterprise-global | Keep `Independent baselines`, `Shared scale · never additive`, and the global-filter boundary. Neither value is observed labor, headcount, cashable savings, or a combined P&L baseline. |
| Closure evidence | Semantic table with Account, Entity, Bank, Account currency, Estimated annual fee (USD), Candidate rule, and Status | Currency, region, entity, and bank update rows and summary; date does not apply to the fixed 30 Jun 2026 snapshot | Every row states the narrow screen and `Validation required · not approved`. Candidate fees are not booked savings. |

### Regional facet and map behavior

- The local 1,280 × 650 map is a decorative rasterization of a CC0 Robinson-projection map; its source, author, geography, license, retrieval date, dimensions, and SHA-256 are recorded in `dashboard/assets/README.md`.
- Each facet row removes only the active region constraint, retains From/To, currency, entity, and bank, and recomputes the governed NA, EMEA, or APAC summary. The interface labels this as `Comparison basis: each row overrides region`.
- Desktop marker size represents matching account count and always shows the raw count. Unavailable anchors use a fixed size plus `Unavailable` or `Applied · no matches`, so size never invents a value.
- Marker or table selection applies the region atomically, preserves all other filters and analytical controls, keeps Bank Account Footprint selected and Regional footprint open, synchronizes the region chip and filter form, and restores focus. Selecting an unavailable or already-applied region produces an explanatory announcement; `All regions` clears only region.
- Liquidity remains outside the map and table. A region selection scopes the separate Liquidity section, where the as-of date, trailing horizon, `$0` funded case, and mobility `not established` remain visible.

### Visual and interaction behavior

- First load exposes only the six-option menu; a normal view selection reveals its mapped content without automatically opening an analytical section.
- `All views` returns to the menu without changing filters or analytical toggles. `Reset dashboard` restores all data/control defaults and the initial menu state.
- Keep the one-open-at-a-time rule among the analytical sections visible in the selected view. Metric search routes to the owning view and opens its section; an exact menu-title search selects that view; methodology search opens the Metric guide without changing views.
- Apply a valid filter atomically to the collapsed summary, expanded visual, legend or table, interpretation, and scope. An invalid range leaves the last valid view unchanged.
- Empty scopes show `No matching data` and `—`. Incomplete liquidity windows show gaps and unavailable values; neither state may retain a portfolio value or substitute `0%`.
- Use a restrained light application shell and dark navy analytical cards with purple, teal, blue, orange, and neutral accents. These colors separate categories and horizons; they do not grade performance.
- On desktop, place primary visuals beside the interpretation rail. On tablet and mobile, stack visual regions in reading order. Long evidence tables and waterfall steps may scroll horizontally without clipping the page.
- On desktop, keep the regional map spatial and the comparison table full width. At mobile widths, hide the decorative silhouette and convert the same region controls to a two-column, then one-column, selector-card layout without dropping counts or selected/unavailable states.
- Treat Regional footprint as a scope-selection surface, not a ranked signal: no choropleth, performance heat, pulsing live marker, route arc, cash-sized bubble, or transfer-flow animation is permitted.
- Exact region-code search (`NA`, `EMEA`, `APAC`) presents the dimension action first. `Regional footprint`, `region overview`, and `map` open the scope lens; methodology terms open its Metric guide topic.
- At 1,120 px and above, the menu is a compact dark navigation surface. At 760 px and below, menu choices remain a single readable column; descriptions and applicability text may wrap without hiding meaning. Hidden views use the native `hidden` state.

### Accessible evidence rendering

- Implement the view chooser as `<nav aria-label="Dashboard views">` with ordinary buttons, not `role="menu"`, menuitems, or a listbox. The selected destination uses `aria-current="page"`.
- View selection focuses its heading; `All views` restores focus to the menu choice just left. The skip link follows the currently visible menu/view target, and view/filter changes are announced through the polite live region.
- Keep every section summary and control keyboard-operable with a minimum 44 px target and visible focus.
- Give each composition ring and chart an accessible name containing the current numerator, denominator, unit, and scope. Repeat essential values visibly.
- Keep legends persistent with labels, values, and shares; color alone does not encode cohort, horizon, or status.
- Distinguish the liquidity horizons by line style as well as color: 7-day solid, 14-day dashed. Do not require hover; the trend table is the exact-value alternative.
- Render liquidity and closure tables with captions, column headers, and row-header semantics. Announce filter and toggle updates through the existing live region.
- Render region markers as real buttons in a labelled group, expose selected and unavailable states in text and ARIA, support arrow/Home/End movement, and repeat every regional value and action in a captioned semantic table.

## Metric guide

The top-menu control and the button inside each expanded section open an accessible right-side dialog on the relevant topic.

The Metric guide is stable methodology, not a second results view. It contains:

- `Definition`
- `Formula / calculation`
- `Data source`
- `Method limit`

The guide does not repeat current values, interpretations, decision boundaries, or next actions. Those belong to the inline disclosure so the user can interpret evidence without leaving page context.

The Regional footprint topic defines the governed classifications, facet-override calculation, source files, mixed date applicability, and schematic/non-live method limit. It does not repeat current marker/table values or selected-region actions.

The Data Quality & Evidence landing owns the current 52/52, 13/13, 12-source, population-control, status, evidence-limit, and next-action result. Its `quality` guide topic explains the stable definition, formula/calculation, sources, and method limit without duplicating the current result.

Do not hide `supplied`, `estimated`, `screening sensitivity`, `deduplicated`, `$0 funded case`, or `not established` in hover-only help.

## User-facing design rules

- Fit the complete six-option initial menu in one 1440 × 900 desktop frame.
- Keep the initial view free of result values, analytical disclosures, charts, warnings, and evidence tables.
- Give each menu choice only its number, exact title, one-sentence purpose, and a navigation arrow; selected-view applicability appears in the view header.
- Expose only the selected view. Keep its analytical details collapsed by default and permit only one visible section to open at a time.
- Keep `Reconciled to supplied controls` beside `Source certification open`; never visualize quality checks as a score, gauge, grade, or performance color.
- Keep the decision answer, KPI meaning, essential evidence boundary, and chevron visible in every collapsed row.
- On desktop, use one-line summary rows and full-width detail content. On tablet and mobile, allow summaries and details to stack without clipping.
- Keep all toggle targets at least 44 px and use direct text; do not depend on color, hover, or icons alone.
- Preserve `$0` funded-case mobility, `not established`, and global-capacity labelling in the collapsed state.
- Keep current evidence and actions inline; reserve the Metric guide for definitions, formulas, sources, and method limits.
- Label Regional footprint as `Scope lens`; do not number or describe it as a performance signal.
- Preserve map/table equivalence: the map provides spatial selection while the table provides exact evidence and the same region actions. Remove only the decorative map when the viewport is too narrow.
- Preserve Version 1 unchanged on its own Figma page.
- Use the existing Inter fallback because SF Pro renders without glyphs through the current Figma automation integration.

## Acceptance criteria

- First load exposes exactly the six named view choices and no result accordion, chart, KPI, warning, or evidence table.
- Selecting each choice reveals only its mapped sections or the quality landing; a normal menu selection opens no accordion.
- Executive Overview makes `design and test—not fund or execute` clear after one navigation action.
- `All views` preserves filters and toggles; `Reset dashboard` restores all defaults and the initial menu.
- Exact menu-title search routes to the matching view; metric search routes to the owning view/section; methodology search opens the guide; dimension/account search applies scope without forcing navigation.
- Applied filters persist across view changes and every selected view states whether dates/dimensions apply.
- Opening one visible analytical section closes the previously open section.
- Applying filters updates the collapsed summary and open detail together without auto-opening another section.
- The quality landing renders 52/52, 13/13, 12 source artifacts, and all six population controls from the governed contract.
- Quality controls remain unchanged under filters and retain `Source certification open`, the full evidence limit, and the governed next action.
- Missing, contradictory, or falsely certified quality evidence fails closed; no quality score, grade, completeness claim, or decision approval is shown.
- `$38.13m` remains a screen; `$0` remains the funded case; mobility remains `not established`.
- Payment evidence remains deduplicated and limited to matching supplied records.
- Capacity remains visibly global and closure/capacity figures remain non-fundable.
- Empty or incomplete scopes show `No matching data` or `—`, never stale portfolio values or false zero percentages.
- Menu/All views focus, native Tab order, `aria-current`, Enter/Space, accordion arrow keys, Home/End, Escape, and polite announcements remain coherent.
- Decision chips remain separate evidence signals and never resolve to a composite score.
- Visibility ring values and source bars reconcile to the selected account population, and action copy follows the delayed methods actually present.
- The selected liquidity waterfall reconciles to the modeled screen, uses the effective post-floor buffer deduction, and never converts the screen into validated mobility.
- Liquidity lines have no fill or forecast treatment; incomplete trailing windows remain gaps, and exact daily values are available in the semantic table.
- The payment ring and four-cohort stack use the same filtered denominator and reconcile for Records, Exceptions, and Repair time; overlap is counted once.
- Regional account, delayed-account, payment, closure, and complete-screen totals reconcile to the non-region facet scope; the map never presents liquidity, a composite score, or live-location semantics.
- Region marker/table selection preserves every non-region filter, leaves the Regional footprint open, synchronizes the filter form and chips, and returns focus to the equivalent selected control. `All regions` clears only region.
- Exact NA, EMEA, and APAC search applies the corresponding region filter; `Regional footprint`, `region overview`, or `map` opens the scope lens.
- Capacity comparison bars remain global, independent, and non-additive.
- Closure candidate rows follow dimension filters, ignore the date filter by design, label fee estimates in USD, and remain explicitly unapproved and unvalidated.
- Charts retain visible labels, legends, and accessible text equivalents; empty and incomplete states never imply zero.
- The Metric guide contains no duplicate current-result or next-action content.

## Figma build record

- File: `Project Northstar — Dashboard V1`
- Page: `Dashboard V2 — Executive View`
- Reference frame: `Project Northstar — Dashboard V2` (`11:3`)
- Canvas: 1440 × 900, with the original Version 1 frame preserved unchanged.
- Visual QA: 49 text layers use Inter; no zero-size text, overflow, placeholder layers, or missing required evidence language remain.
- Implementation: the Figma frame remains the palette and typography reference. The browser dashboard adds the six-view menu-first shell, governed quality landing, inline progressive disclosure, and reference-inspired analytical forms described here; the existing Figma frame is not claimed to contain that routing layer.

## Implemented interaction model

The browser implementation adds only interactions that support a decision or reveal its evidence:

- **Menu-first routing:** six ordinary navigation choices expose only the relevant subset of seven analytical sections or the governed quality landing. A normal selection leaves analytical sections collapsed.
- **Inline progressive disclosure:** one-open-at-a-time behavior reveals current evidence inside the selected view while keeping other views out of the accessibility tree.
- **Reference-inspired analytics:** expanded sections add separate decision chips, visibility composition/source exposure, liquidity construction and date sensitivity, payment cohort composition, a regional scope map/table, independent capacity comparison, and row-level closure evidence. Each form explains a supported relationship without implying performance, certainty, or fundable value.
- **Dashboard search:** routes exact menu titles to views, metrics to their owning view/section, explicit dimensions/accounts to filter state, and methodology queries to the Metric guide.
- **Governed filters:** applies an inclusive date range plus single-select currency, region, entity, and bank. Visibility and payments use the selected period; liquidity uses the period end date; closures use account dimensions; capacity remains global. Regional comparison rows explicitly override only region while retaining other filters and their measure-specific date rules.
- **Governed quality landing:** renders the exact internal controls, population counts, source count, open-certification status, evidence limit, and next action; adversarial or incomplete quality contracts fail closed.
- **Liquidity horizon:** switches governed 7-day and 14-day evidence inside the open Liquidity section. Validated mobility remains `not established`, and the funded case remains `$0`.
- **Payment measure:** switches records, exceptions, and repair minutes inside the open Payment friction section while preserving the deduplicated cohort union.
- **Regional scope lens:** applies a governed NA, EMEA, or APAC filter from either the schematic map or exact table while preserving all other control state. Each comparison row overrides region only, so alternate regional scopes remain inspectable.
- **Metric guide:** provides definition, formula, source, and method-limit reference without duplicating current evidence or actions.
- **All views and reset:** All views navigates without changing scope or analytical toggles; Reset clears search/filters, restores full-period/14-day/Records defaults, closes transient UI, and returns to the menu.
- **Accessible navigation:** menu buttons use native semantics and `aria-current`; selection and Back restore predictable focus. Disclosures retain Enter/Space, arrow, Home/End, and Escape behavior. Regional markers add pressed/disabled state, live announcements, equivalent table actions, and post-filter focus restoration.

These interactions make the artifact behave like an analytical application rather than a static slide. Free-form thresholds, recommendation scores, funding controls, and execution actions remain intentionally excluded.
