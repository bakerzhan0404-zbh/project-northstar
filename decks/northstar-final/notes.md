# Project Northstar — Final Steering Committee Notes

## Purpose

- Audience:
- Decision / outcome:
- Style preset: `data-heavy-boardroom`
- Style reference: `ref-boardroom-operating-review` / Boardroom Operating Review
- Style metrics: `style_reference_metric_profile_v1`; density `high operating report`; whitespace target `0.18`; body-word budget `42, 72`.
- Starter scaffold: `style_reference_starter_outline_v1` synthetic examples; replace before delivery.

## Sources

- Add the datasets, URLs, or reference decks used to author this presentation.
- Record the provenance for every non-user image you stage through `asset_plan.json`.
- Promote researched claims into `evidence_plan.json` before adding them to slides.

## Research log to staging plan

Closes the gap where research produces good content but never turns into
staged visuals. Every row in this table should eventually trigger an
entry in `asset_plan.json` (wikimedia_query for a CC photo, or a staged
icon/chart).

| Fact discovered | Source | Becomes | In asset_plan as |
|---|---|---|---|
| _e.g. Chicago Pile-1, first controlled chain reaction, Dec 2 1942_ | _en.wikipedia.org/Chicago_Pile-1_ | _hero image on slide 3_ | _images[0].wikimedia_query: "Chicago Pile-1"_ |
|  |  |  |  |
|  |  |  |  |

If this table is empty at build time, ask yourself whether the deck
actually has no visual anchors or whether the research hasn't been
connected to the staging plan yet.

## Style Contract

- Slide size: 16:9 unless a reference deck says otherwise
- Title font: 40-30pt range via preset
- Section font: 28-22pt range via preset
- Body font: 22-15pt range via preset
- Margin x: 0.65
- Gutter: 0.24
- Style DNA: Dense but calm operating pages: table/chart pairs, explicit variance language, and source-backed footers.
- Preferred variants: title, stats, chart, table, matrix, comparison-2col, standard, image-sidebar
- Chart treatment: Facts-right chart with target/actual callout and source footnote.
- Table treatment: Compact sortable-style table, zebra bands, and bold exception rows.
- Decision treatment: Action table: decision, metric trigger, owner, date.

## QA Notes

- Preserve alignment first.
- Keep subtitles below wrapped titles.
- Prefer local, source-backed assets in `assets/`.
- Use `asset:alias` references in `outline.json` after staging into `assets/staged/`.
- Add any deck-specific measurements here if you later match an existing deck manually.

<!-- deck-intake-answers:start -->
## Deck Intake Answers

- Answered by: best_judgment
- Unanswered: none

### Persisted Answers
- audience_context: ACG CFO-led Steering Committee making a mobilization decision
- style_direction: Figure-first report
- density: dense report/leave-behind
- palette: restrained palette chosen by best judgment
- background_visuals: clean report with source-backed or generated visuals only when useful
- evidence_assets: use local/generated figures when data exists; otherwise use source-backed visuals selectively
- source_policy: cite key claims

### Question Card Answers
- style_density: Figure-first report
- visual_source_policy: Best judgment

### Choice Resolution Seed
- Choice contract: deck_choice_resolution_v1
- Resolved choices: audience_context: ACG CFO-led Steering Committee making a mobilization decision, style_density: Figure-first report, visual_source_policy: Best judgment
<!-- deck-intake-answers:end -->

<!-- deck-design-contract:start -->
## Deck Design Contract

- Contract file: `design_contract.json`
- Version: `deck_design_contract_v1`
- Stable prompt id: `northstar-final-steerco-v1`
- Working title: Project Northstar — Final Steering Committee
- Design DNA: board risk memo
- Style preset: data-heavy-boardroom
- Style seed: `northstar-final-steerco-v1`
- Proof burden: Use reconciled ACG project outputs first, then analyst assumptions and judgments with explicit labels.

### Style Mix Ledger
- Style reference: `ref-boardroom-operating-review` / Boardroom Operating Review
- Reference DNA: Dense but calm operating pages: table/chart pairs, explicit variance language, and source-backed footers.
- Reference treatment coverage: title, comparison, chart, table, figure, dashboard, decision, references
- Reference layout playbook: `style_reference_layout_playbook_v1`
- Preferred variants: title, stats, chart, table, matrix, comparison-2col, standard, image-sidebar
- Title archetype: `board-period-scope-opener`
- References archetype: `data-cut-version-appendix`
- Body treatment archetypes: comparison=`boardroom-operating-review-comparison-frame`, chart=`boardroom-operating-review-chart-readout`, table=`boardroom-operating-review-table-ledger`, figure=`boardroom-operating-review-figure-proof-object`, dashboard=`boardroom-operating-review-dashboard-state-board`, decision=`boardroom-operating-review-decision-record`
- Avoid variants: generated-image, cards-3, kpi-hero
- Structural motif library: `style_reference_structural_motif_library_v1`
- Background structure: dense operating report with KPI strip, chart/table pair, and bottom decision band
- Layout motifs: variance band, facts-right chart, exception ledger, owner decision table
- Mix rule: Keep the consulting answer-pyramid and board-ledger page system coherent; vary only evidence-fit slide treatments.
- Header variants: split-rule, left-accent, top-bottom-rule, plain
- Timeline modes: bands
- Matrix modes: open-quadrants
- Stats modes: policy-bands, feature-left
- Chart treatments: facts-right, minimal
- Table treatments: compact-ledger, readout-sidecar, decision-matrix
- Footers: source-line

### Reproducibility Replay
- Replay contract: `deck_reproducibility_contract_v1`
- Stable prompt id: `northstar-final-steerco-v1`
- Style seed: `northstar-final-steerco-v1`
- Renderer: `pptxgenjs`
- Renderer treatment signature: `page_system:board-ledger|structural_motif:board-index|title_layout:split-hero|footer_mode:source-line|chart_treatment:facts-right|table_treatment:compact-ledger|figure_table_treatment:table-first|stats_mode:policy-bands|matrix_mode:open-quadrants|summary_callout_mode:default|image_sidebar_mode:analysis-rail|comparison_mode:scorecard`
- Style preset: data-heavy-boardroom
- Background: white board report with dark navy cover and restrained blue/cyan accents
- Header pool: split-rule, left-accent, top-bottom-rule, plain
- Footer pool: source-line
- Chart pool: facts-right, minimal
- Table pool: compact-ledger, readout-sidecar, decision-matrix
- Replay commands: python3 scripts/apply_design_contract.py --workspace <deck> --contract <deck>/design_contract.json --report <deck>/design_contract_apply_report.json, python3 scripts/build_workspace.py --workspace <deck> --qa --fail-on-planning-warnings --fail-on-whitespace-warnings --overwrite, python3 scripts/report_delivery_readiness.py --workspace <deck>

### Slide Quality Contract
- Quality contract: `slide_quality_contract_v1`
- Readability targets: title=24, body=12, caption=7.5, chart labels=8, footer reserve=0.34
- Layout targets: fail whitespace=True, source footer: Short source line on every content slide; complete paths in notes and final evidence register.
- Artifact quality: required_when_data_active=True
- Quality fail on: planning warnings, whitespace warnings, design warnings, placeholder text, stale sources
- Quality commands: planning validation, preflight, strict geometry, +3 more

### Artifact Ledger
- Local data needed: False

### QA and Execution Ledger
- Required checks: planning validation, preflight, strict geometry, rendered visual review, placeholder check, delivery readiness
- Fail on: planning warnings, whitespace warnings, design warnings, placeholder text, stale sources

### Choice Resolution Ledger
- Choice contract: deck_choice_resolution_v1
- Answered by: best_judgment
- Resolved choices: audience_context: ACG CFO-led Steering Committee making a mobilization decision, style_density: Figure-first report, visual_source_policy: Best judgment; cite key claims
- Selected renderer treatment signature: `page_system:board-ledger|structural_motif:board-index|title_layout:split-hero|footer_mode:source-line|chart_treatment:facts-right|table_treatment:compact-ledger|figure_table_treatment:table-first|stats_mode:policy-bands|matrix_mode:open-quadrants|summary_callout_mode:default|image_sidebar_mode:analysis-rail|comparison_mode:scorecard`
- Locked fields: style preset, board-ledger page system, source-line footers, 15 core slide limit, no external imagery

### Missing Inputs
- Exact North America eight-week freeze calendar

### Assumptions
- No corporate logo or proprietary brand assets are required.
- A restrained boardroom style is appropriate for the CFO-led audience.
- All factual claims can be supported from local project evidence without web research.

### Authoring Instructions
- Keep 15 core slides plus three appendix slides.
- Write claim-led titles and make every evidence limitation visible.
- Use editable charts and tables; no decorative imagery.
- Close with the same 90-day mobilization decision stated on slide 1.
<!-- deck-design-contract:end -->
