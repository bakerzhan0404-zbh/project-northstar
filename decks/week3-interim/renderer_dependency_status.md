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

A density pass on all ten slides cut hard text overflow from 6 shapes to 1 and
visual-review clip warnings from 9 to 4. What remains does not respond to source
edits.

| Gate | Before | After | Nature |
|---|---|---|---|
| Text overflow | 6 shapes (slides 3, 8) | 1 shape (slide 3) | Remaining box is 0.22" tall; one text line needs 0.39" |
| Visual clip risk | 9 warnings, up to 583% | 4 warnings, up to 128% | Fixed column and rail heights |
| Design font floors | 49 warnings | 49 warnings | Renderer/preset mismatch — see below |

Geometry, overlap, placeholder, whitespace, preflight, planning, and
narration/asset resolution all pass with zero issues.

### The font floors are a preset contract mismatch, not deck density

The `data-heavy-boardroom` preset declares `title_min = 30 pt`,
`body_min = 15 pt`, and `caption_min = 10 pt`, and `design_rules_qa.py` gates
against those values. The `pptxgenjs` renderer does not produce text at those
sizes on content slides:

| Warning | Count | Renderer behaviour |
|---|---|---|
| `title_font_too_small` | 9 | `titleFontForLength()` returns 26 pt at most, 24 pt above 42 characters. No content-slide title reaches 30 pt at any length. |
| `caption_font_too_small` | 24 | Page-number (`N/10`, 8.4 pt) and source-line (8.0 pt) chrome the outline does not control. |
| `table_font_too_small` | 8 | Table body text sits in a fixed 8.0–8.9 pt band. Cutting cell text on slides 2, 4, 7, and 9 did not move it. |
| `body_font_too_small` | 7 | Generated readout panels are fixed at 12 pt; timeline band bodies at 8.8 pt. |
| `chart_label_font_too_small` | 1 | Chart axis labels are fixed at 8.0 pt against a 9.0 pt floor. |

Every one of these was verified as unresponsive to content edits. This is a
mismatch inside the presentation skill between a preset's declared typography
tokens and its own renderer's output. It is recorded here rather than worked
around: no skill file was modified, and no threshold was relaxed to manufacture
a pass.

### Content changed by the density pass

Slide 3's fact rail is 0.988" wide, so `label · detail` pairs could not fit; the
details were dropped and labels reduced to `Cases`, `Gates`, and `Ready`, with
the framing carried by the subtitle and caption. Slide 8's comparison bullets
were cut roughly in half. Table cells on slides 2, 4, 7, and 9 and timeline
bodies on slide 10 were shortened. Evidence-boundary language was preserved
throughout: the `$38.13m` screen wording, `$0` recognized value, `NOT
QUANTIFIED` risk, the `$1.0-$1.5m` ceiling, the score-is-judgment framing, and
the no-authorization list all remain intact.

## Acceptance boundary

The deliverable is a rendered, visually inspected 10-slide PPTX. It is not
claimed to have passed the skill's strict polish gate: `manual_review_passed.flag`
is absent and `report_delivery_readiness.py` has not returned a clean result.
Clearing the remaining gate requires a change to the presentation skill, not to
this deck.
