# Renderer Status — SUPERSEDED

**Superseded:** 19 August 2026

This workspace is **no longer the source of the Week 3 steering deck.** It is
retained as the planning record only: the content, evidence, design, and asset
plans that shaped the ten-slide argument.

## Why it was replaced

The workspace built the deck through the presentation skill's
`data-heavy-boardroom` preset. That produced a competent deck, but a visually
unrelated one — the Week 2 checkpoint was authored as HTML in Barlow on a warm
grey ground with teal and ochre accents, while the preset renders Helvetica Neue
on navy title bars. Submitting both would have read as two different firms.

The preset also could not satisfy its own contract. It declares
`title_min = 30 pt` while `titleFontForLength()` returns 26 pt at most, so nine
title warnings were unreachable from the deck source; caption, table, and chart
warnings were likewise fixed renderer bands. 49 design warnings survived a full
density pass across all ten slides.

## What builds the deck now

[`src/week3_steering_deck.py`](../../src/week3_steering_deck.py) composes the
PPTX directly with `python-pptx`, reproducing the Week 2 house style natively:
the same 720x405 pt page, Barlow and Barlow Condensed, the sampled palette, the
plus-corner panel rules, eyebrow labels, dark callout bars, and page counter.

The PDF is exported from that PPTX, so both submission formats are the same deck:

```bash
python3 src/week3_steering_deck.py
/Applications/LibreOffice.app/Contents/MacOS/soffice --headless \
  --convert-to pdf deliverables/working/week_3/W3_interim_steering_deck.pptx \
  --outdir deliverables/working/week_3
```

Do not rebuild from this workspace. Doing so would overwrite the delivered deck
with the superseded visual system.
