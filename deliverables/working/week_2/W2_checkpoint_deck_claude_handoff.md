# Week 2 Checkpoint — Claude Presentation Handoff

**Production scope:** Revise the existing five-page checkpoint presentation from the updated [Markdown source](W2_checkpoint_deck.md). Keep exactly five slides. Do not change the evidence, add slides, or edit the diagnostic report/data.

**Source of truth:** `W2_checkpoint_deck.md`, `W2_diagnostic_report.md`, `data/processed/W2_visibility_diagnostic.csv`, `data/processed/W2_liquidity_scenarios.csv`, `data/processed/W2_liquidity_thresholds.csv`, and `data/processed/W2_payment_diagnostic.csv`.

## Global direction

- Retain the current 16:9 executive style, but reduce visible copy and give each slide one dominant visual.
- Use claim-led titles and readable management-level type. Avoid dense tables, repeated cards, and technical test counts on-slide.
- Keep detailed conditions, definitions, counterevidence, and provenance in speaker notes. Do not delete the notes.
- Preserve evidence language: `$38.13m` is a **14-day screening result**, not surplus, available, transferable, or movable cash. Validated movable cash established by current evidence is `$0`.
- Keep every payment conclusion bounded to the supplied 7,600 records. Gross amounts are all-status payment-intent values translated at payment-date project FX—not settlement, outflow, or loss.
- Use the same color semantics throughout: teal for observed/current evidence, amber for assumptions or gates, red only for unsupported/stop conditions, and neutral gray for comparators.

## Slide 1 — Cut to the three findings and three decisions

**Title:** ACG should advance to option design, but through two targeted pilot designs and three evidence gates.

**Visible findings:** Use three short horizontal bands or columns.

1. `23/55 delayed` — all delayed accounts use portal or spreadsheet reporting.
2. `$38.13m 14-day screening result` — validated movable cash remains `$0 established`.
3. `2,839-record priority union` — 356 exceptions and 14,939 repair minutes.

**Visible decision requests:** Keep each to one line.

1. Authorize the Week 3 three-option comparison.
2. Approve design—not execution—of two bounded validation pilots.
3. Confirm evidence owners and the 18 / 19 / 21 August deadlines.

Remove the visible technical-test footer. Put the option names, downside tests, pilot controls, value conditions, owners, dates, and deliverables in speaker notes exactly as set out in the Markdown.

## Slide 2 — Replace the numeric cards with two dominant visuals

### Left/top: visibility distribution

Build one 100% stacked horizontal distribution bar:

`API 12 | Host-to-host 20 | Portal 9 | Spreadsheet 14`

Add a simple bracket or secondary label below it:

`32 same-day date proxy | 23 delayed date proxy`

Do not represent the date proxy as start-of-day or elapsed-24-hour performance.

### Right/bottom: liquidity waterfall

Use these exact steps:

1. `$57.80m` gross positive estimated availability
2. `−$8.05m` preliminary restriction screen
3. `−$2.14m` negative account positions
4. `$47.61m` apparent net before screening window
5. `−$9.48m` effective 14-day reduction after account floors
6. `$38.13m` **14-day screening result — not movable cash**

The seven-day and 14-day windows are alternatives. Do not place both as sequential deductions. Keep only one visible threshold callout: `$35m passes 138/168 complete 14-day windows (82%); minimum $31.28m.` Put the full threshold table, the `$42.84m` seven-day reference, the reason for 7/14 days, and the unmodeled-cash-needs caveat in notes.

## Slide 3 — Make overlap and absolute workload unmistakable

Use a four-quadrant matrix or one compact four-row table:

| Cohort | Records | Exceptions | Rate | Repair min | Gross payment-intent amount |
|---|---:|---:|---:|---:|---:|
| Manual touch only | 2,053 | 246 | 11.98% | 10,018 | $51.98m |
| Manual touch + cross-border wire | 342 | 58 | 16.96% | 2,702 | $6.85m |
| Cross-border wire only | 444 | 52 | 11.71% | 2,219 | $7.88m |
| Neither | 4,761 | 123 | 2.58% | 5,141 | $131.43m |

Add one dominant union strip: `2,839 records | 356 exceptions | 14,939 repair min | $66.71m`. Label it `74.32% of exceptions; 74.40% of repair minutes`.

Emphasize the overlap: `342 records = 14.28% of manual touch / 43.51% of cross-border wires`. State that the original manual-touch and cross-border-wire totals cannot be added. Keep the causal limitation and gross-amount definition in notes.

## Slides 4–5 — Preserve structure; tighten language only

- Slide 4: keep the data/control spine and current maturity logic. If mentioning the payment population, use `deduplicated priority union / four mutually exclusive strata`, not “two cohorts.”
- Slide 5: keep the three dated evidence gates and common downside tests. Payment/process evidence should unlock a four-stratum root-cause review and a controlled capacity case.
- Do not add another conclusion or repeat the three long decision paragraphs from Slide 1.

## Final production QA

- Exactly five slides; no hidden sixth appendix slide.
- No clipped text, overlapping objects, tiny footnotes, or orphaned labels.
- Slide 1 decision requests are one line each.
- Slide 2 has one distribution bar and one true waterfall; 7/14-day windows are not stacked sequentially.
- Slide 3 includes records, exceptions, rates, repair minutes, gross amounts, overlap, and deduplicated union.
- `$38.13m` is labeled “14-day screening result” everywhere; no slide calls it cash available or surplus.
- No visible `57/57`, `69/69`, or other test-count language.
- Every slide retains speaker notes and source provenance.
- Export a new PDF only after visual review at full-slide and thumbnail scale; keep the editable source alongside the export.
