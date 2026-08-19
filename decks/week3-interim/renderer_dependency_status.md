# Renderer Dependency Status

**Checked:** 19 August 2026 (supersedes the 18 August blocked status)

**Scope:** Week 3 interim steering deck workspace

**Result:** The workspace builds and renders. Visual QA now runs against real
rasterized slides. Polish gates remain open.

## Resolved

The 18 August block was `ModuleNotFoundError: No module named 'pptx'`, raised by
the workspace initializer before it could write `workspace.json`. The workspace
was therefore a set of orphaned plan files that `build_workspace.py` could not
resolve.

The declared dependency set is now installed locally:

| Dependency | Purpose | Status |
|---|---|---|
| `python-pptx` 1.0.2 | Workspace init, inventory, and design-rule QA | Installed |
| `pptxgenjs` 4.x (node) | Default `.pptx` renderer | Installed under the skill's `node_modules` |
| LibreOffice 26.2 (`soffice`) | PPTX to PDF for rasterization | Installed |
| `poppler` (`pdftoppm`) | PDF to PNG for the contact sheet | Installed |

`soffice` is not on the default `PATH`. Export it before building:

```bash
export PATH="$PATH:/Applications/LibreOffice.app/Contents/MacOS"
```

## Current build result

`build_workspace.py --qa --visual-review` produces a 10-slide
`build/project-northstar-week3-interim-steering.pptx`, renders 10/10 slides, and
writes `build/qa/visual_review/contact_sheet.jpg`.

Passing gates: preflight, planning validation, whitespace, geometry, overlap,
placeholder scan, and narration/asset resolution.

## Open gates

| Gate | Result | Nature |
|---|---|---|
| Text overflow | 6 shapes on slides 3 and 8 | Content density; fixable at source |
| Body/table/chart font floors | 17 warnings | Content density; fixable at source |
| Title font floor | 9 warnings | Not reachable from source — see below |
| Caption font floor | 23 warnings | Mostly chrome — see below |

### Title and caption floors are a preset contract mismatch

The `data-heavy-boardroom` preset declares `title_min = 30 pt` and
`caption_min = 10 pt`, and `design_rules_qa.py` gates against those values. The
`pptxgenjs` renderer sizes every content-slide title through
`titleFontForLength()`, which returns **26 pt at most and 24 pt above 42
characters**. No content-slide title can reach 30 pt at any length, so these nine
warnings cannot be cleared by editing the deck. The caption warnings are
dominated by renderer chrome — the `N/10` page number at 8.4 pt and the source
line at 8.0 pt — which the outline does not control either.

This is a mismatch inside the presentation skill between a preset's declared
typography tokens and its own renderer's output. It is recorded here rather than
worked around, and no skill file was modified.

## Acceptance boundary

The deliverable is a rendered, visually inspected 10-slide PPTX. It is not
claimed to have passed the skill's strict polish gate: `manual_review_passed.flag`
is absent and `report_delivery_readiness.py` has not returned a clean result.
