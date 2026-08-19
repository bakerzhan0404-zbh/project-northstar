# Week 3 Interim Steering Deck — Workspace Notes

> **Superseded 19 August 2026.** This workspace is the planning record only.
> The delivered deck is built by `src/week3_steering_deck.py` in the Week 2
> checkpoint house style. See `renderer_dependency_status.md`. The evidence
> and language rules below still govern the argument.

## Source-of-truth order

1. `deliverables/working/week_3/W3_interim_steering_deck.md` holds the complete ten-slide narrative, speaker notes, and file-level provenance.
2. `outline.json` is the renderable slide source and must remain exactly ten slides.
3. `content_plan.json`, `evidence_plan.json`, `design_brief.json`, `asset_plan.json`, and `style_contract.json` define the argument, evidence, taste, assets, and rebuild contract.

If a claim changes, update the evidence source first, then the Markdown deck source, the planning records, and `outline.json`. Do not patch a generated PPTX directly.

## Evidence and language rules

- `$38.13m` is the 30 June 14-day liquidity **screen**, not cash, surplus, movable value, or transfer authority.
- Validated movable cash is `$0`; validated redeployable capacity is `0 hours/month`.
- The payment population is the supplied `7,600`-record extract, not a certified ACG-wide population.
- The priority-union pattern is an association, not a root cause.
- Risk exposure and risk value are `NOT QUANTIFIED`; `$0` refers only to the current recognized-value ledger entry.
- Cash release, P&L, capacity, and risk are separate, non-additive ledgers.
- Actual implementation and run cost, ROI, NPV, payback, and a funding recommendation are unavailable.
- The FY2026 `$1.0–$1.5m` initial-stage envelope is a ceiling, not an estimate, budget, allocation, or spend authority.
- The option scores `72 / 87 / 60` are analyst judgments, not confidence, value, readiness, or client approval.
- The 90-day plan is an evidence-mobilization timebox, not a production-pilot duration. Time never overrides an open gate.

## Slide-design rules

- Use the `data-heavy-boardroom` preset with the `board-ledger` page system.
- Borrow only the table-first readout discipline from lab-results decks.
- Keep one dominant evidence object per slide.
- Slide 3 is the only chart; all other evidence remains editable text or tables.
- Carry a compact source line on every slide and keep full provenance in notes.
- Preserve the conclusion loop: slide 1 asks for direction and owners; slide 10 repeats the ask after the evidence and ends at a separate go/no-go.
- Slide 8 is the falsification page and must remain before the owner/close sequence.
- Use amber for open evidence, never for implied upside. Do not color `$0` as a “success.”
- Do not add a map merely because the operating scope is global; no decision-relevant geographic magnitude is currently certified for this steering argument.

## 90-day mobilization interpretation

The four timeboxes on slide 10 are an analyst proposal assembled from the existing evidence-readiness and stage-gate logic:

- decision day: direction, owners, fallback, and authorization boundary;
- days 1–30: source/population reconciliation and metric contract;
- days 31–60: specialist/control review, cost evidence, and safe-environment rollback rehearsal;
- days 61–90: lock baselines and return with a separate stop, extend, or later bounded-pilot recommendation.

If evidence is incomplete at day 90, the answer is extension, redesign, or local stabilization—not automatic launch.

## Rebuild and QA path

When the supported presentation environment is available, run the workspace sequence from the presentation skill:

```bash
python3 /Users/bakerzhan/.codex/skills/presentation-skill/scripts/report_workspace_readiness.py \
  --workspace decks/week3-interim

python3 /Users/bakerzhan/.codex/skills/presentation-skill/scripts/build_workspace.py \
  --workspace decks/week3-interim \
  --qa \
  --visual-review \
  --fail-on-visual-review-warnings \
  --fail-on-planning-warnings \
  --fail-on-whitespace-warnings \
  --overwrite

python3 /Users/bakerzhan/.codex/skills/presentation-skill/scripts/report_delivery_readiness.py \
  --workspace decks/week3-interim
```

Export `soffice` onto `PATH` first: `export PATH="$PATH:/Applications/LibreOffice.app/Contents/MacOS"`.

## Current renderer dependency status

The toolchain is installed and the deck renders: 10 slides to PPTX and 10/10 rasterized into `build/qa/visual_review/contact_sheet.jpg`. Geometry, overlap, whitespace, placeholder, preflight, planning, and narration checks pass.

The strict polish gate remains open. One text box on slide 3 overflows a 0.22"-tall rail, and 49 font-floor warnings come from a mismatch between the `data-heavy-boardroom` preset's declared typography and its own renderer's output — not from deck density. See `renderer_dependency_status.md` for the per-category evidence.
