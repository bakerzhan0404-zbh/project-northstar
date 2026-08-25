"""Build the Week 4 final executive deck in the Week 2/3 house style.

The first build of this deck came from an external presentation toolchain
(PptxGenJS), which produced a different visual language from the Week 2
checkpoint and Week 3 interim decks and could not be rebuilt from this
repository. This module rebuilds it from the same design system as
``week3_steering_deck``: identical tokens, identical components, one
reproducible command.

Fifteen core slides plus a four-slide appendix, per the rubric cap.
"""

from pathlib import Path

from pptx import Presentation

from week3_steering_deck import (
    BLUE,
    CONTENT_W,
    INK,
    MARGIN,
    MUTED,
    NAVY,
    OCHRE,
    PH,
    PT_BODY,
    PT_LABEL,
    PT_LEAD,
    PW,
    RULE_LT,
    TEAL,
    TEAL_LT,
    WHITE,
    Y_BODY,
    _pt,
    callout,
    hrule,
    new_slide,
    numbered_list,
    page_frame,
    panel,
    rect,
    section_label,
    source,
    stat_tiles,
    table,
    textbox,
    title,
    write,
)

TOTAL = 19
EYEBROW = "Project Northstar — Final steering committee"


def body_text(slide, x, y, w, text, *, size=PT_BODY, color=INK, h=40):
    frame = textbox(slide, x, y, w, h)
    write(frame, text, size=size, color=color, line=1.3)
    return frame


def bullets(slide, x, y, w, items, *, gap=16.0, color=INK):
    for index, item in enumerate(items):
        iy = y + index * gap
        rect(slide, x, iy + 4, 3.5, 3.5, fill=TEAL)
        frame = textbox(slide, x + 11, iy - 1, w - 11, gap + 4)
        write(frame, item, size=PT_BODY, color=color, line=1.25)


def slide_01(prs):
    s = new_slide(prs)
    page_frame(s, EYEBROW, 1, TOTAL)
    title(s, "Authorize 90 days to make the next treasury decision",
          subtitle="Direction and evidence mobilization only — no production, funding, or value approval")
    stat_tiles(s, MARGIN, Y_BODY + 6, CONTENT_W, 122, [
        {"label": "Direction", "value": "87", "unit": "federated",
         "body": "Against 72 local and 60 global. A design direction, not "
                 "confidence, value, or readiness."},
        {"label": "Recognized value", "value": "$0", "unit": "today",
         "tag": "Risk not quantified",
         "body": "Cash, P&L, and capacity each recognize nothing. ROI, NPV, "
                 "and payback remain unavailable."},
        {"label": "Return point", "value": "90", "unit": "days",
         "body": "A separate stop / extend / bounded-pilot decision at G3. "
                 "Time does not override an open gate."},
    ])
    section_label(s, MARGIN, 244, "Decisions requested today")
    numbered_list(s, MARGIN, 262, CONTENT_W, [
        "Authorize federated coordination as the direction, with local "
        "stabilization as the documented fallback.",
        "Confirm accountable owners for data, mobility, payments, controls, "
        "service, cost, and benefits.",
        "Approve the 90-day evidence timebox and reserve every launch, spend, "
        "value, and scale decision.",
    ])
    callout(s, "Governing message",
            "ACG has enough evidence to choose a direction—not enough to "
            "authorize execution or book value.")
    source(s, "Source: W3 strategic options; W3 business case; W4 roadmap and governance; final decision log.")


def slide_02(prs):
    s = new_slide(prs)
    page_frame(s, "Why act now", 2, TOTAL)
    title(s, "Enough evidence to choose a direction—not to approve value or production")
    ix, iy, iw, _ = panel(s, MARGIN, Y_BODY + 6, CONTENT_W, 176, "Supplied-data readout")
    table(s, ix, iy, iw,
          ["Measure", "Supplied result", "What it is not"],
          [["Same-day calendar proxy", "58.18% of 9,955 account-days",
            "Not intraday completeness or an SLA result"],
           ["Payment exception rate", "6.30% of 7,600 records",
            "Not a certified enterprise population or a cause"],
           ["Weighted option score", "87 federated / 72 local / 60 global",
            "Not value, confidence, cost, or readiness"],
           ["Recognized cash, P&L, capacity", "$0 today",
            "Not a claim that no opportunity exists"]],
          [0.28, 0.32, 0.40], row_h=30)
    callout(s, "Boundary",
            "Model-control passes and supplied-data calculations are not "
            "execution evidence.")
    source(s, "Source: W1 data-quality outputs; W2 diagnostic; W3 options and business case.")


def slide_03(prs):
    s = new_slide(prs)
    page_frame(s, "Diagnostic summary", 3, TOTAL)
    title(s, "Four linked failures explain ACG's treasury problem",
          subtitle="The recommendation must fix ownership, evidence, control, and service together")
    ix, iy, iw, _ = panel(s, MARGIN, Y_BODY + 6, CONTENT_W, 186, "Failure map")
    table(s, ix, iy, iw,
          ["Failure", "Supplied evidence", "Management implication"],
          [["Visibility", "58.18% same-day; 2,534 account-days beyond one day",
            "Own the source, cutoff, reconciliation, and exception path"],
           ["Liquidity", "$21m / $35m / $46.2m screens",
            "Certify mobility, buffers, and economics before any action"],
           ["Payment operations", "31.51% manual touch; 6.30% exceptions",
            "Prove causes before standardizing or automating"],
           ["Operating model", "Local practice; three ERPs; no enterprise TMS",
            "A federated policy, data, and control spine with local rights"]],
          [0.22, 0.34, 0.44], row_h=32)
    callout(s, "Read together",
            "These are one connected ownership, evidence, control, and service "
            "gap—not four separate projects.")
    source(s, "Source: W2 diagnostic report; W3 future-state operating model.")


def slide_04(prs):
    s = new_slide(prs)
    page_frame(s, "Finding 01 · Visibility", 4, TOTAL)
    title(s, "Manual sources explain every delayed account-day in the supplied pattern")
    ix, iy, iw, _ = panel(s, MARGIN, Y_BODY + 6, CONTENT_W, 160, "Reporting method exposure")
    table(s, ix, iy, iw,
          ["Method", "Accounts", "Same-day", "Supplied pattern"],
          [["API", "12", "100%", "No delayed account-day in the extract"],
           ["Host-to-host", "20", "100%", "No delayed account-day in the extract"],
           ["Portal", "9", "0%", "All observations one day late"],
           ["Spreadsheet", "14", "0%", "All observations two or more days late"]],
          [0.20, 0.13, 0.15, 0.52], row_h=27,
          emphasis={2: {"color": OCHRE, "bold": False},
                    3: {"color": OCHRE, "bold": False}})
    callout(s, "Method limit",
            "A reporting-date proxy. It is not proof of intraday completeness, "
            "and it does not establish cause.")
    source(s, "Source: W2 visibility outputs; dashboard reporting-method facts.")


def slide_05(prs):
    s = new_slide(prs)
    page_frame(s, "Finding 02 · Liquidity", 5, TOTAL)
    title(s, "The liquidity analysis defines a certification agenda—not a cash-release claim")
    stat_tiles(s, MARGIN, Y_BODY + 6, CONTENT_W, 118, [
        {"label": "$21m screen", "value": "168", "unit": "of 168 windows",
         "body": "Every complete 14-day window clears the stress threshold."},
        {"label": "$35m screen", "value": "138", "unit": "of 168 windows",
         "body": "The base threshold thins materially at fourteen days."},
        {"label": "$46.2m screen", "value": "0", "unit": "of 168 windows",
         "tag": "Not achievable", "body": "No complete window clears the upper case."},
    ])
    body_text(s, MARGIN, 252, CONTENT_W,
              "Recognized movable cash remains $0 until VG01–VG05 close: authoritative balance and "
              "timestamp, legal and tax transferability, approved operating buffers, transfer economics, "
              "and a Finance-approved recognition rule.")
    callout(s, "Boundary",
            "A screening sensitivity on supplied balances—not surplus cash, "
            "transferable cash, or transfer authority.")
    source(s, "Source: W2 liquidity outputs; W3 business case VG01–VG05.")


def slide_06(prs):
    s = new_slide(prs)
    page_frame(s, "Finding 03 · Payments", 6, TOTAL)
    title(s, "Payment friction is material enough to diagnose—too weakly evidenced to automate")
    ix, iy, iw, _ = panel(s, MARGIN, Y_BODY + 6, CONTENT_W, 160, "Supplied extract rates")
    table(s, ix, iy, iw,
          ["Measure", "Supplied rate", "Required before any change"],
          [["Manual touch", "31.51%", "Classify required control work before calling it avoidable"],
           ["Exceptions", "6.30%", "Reason codes and source documents for the 120-record frame"],
           ["Late release", "5.00%", "Approved cutoffs and event timestamps, not a supplied flag"],
           ["Cross-border", "10.34%", "Corridor, beneficiary, and settlement evidence"]],
          [0.24, 0.18, 0.58], row_h=27)
    callout(s, "Boundary",
            "These are associations. The 120-record source-linked sample must "
            "establish causes and controls first.")
    source(s, "Source: W2 payment outputs; W3 payment pilot charter.")


def slide_07(prs):
    s = new_slide(prs)
    page_frame(s, "How we will know", 7, TOTAL)
    title(s, "Six measures tell management whether this is working",
          subtitle="Two performance signals, one value gate, two safety gates, one readiness gate")
    ix, iy, iw, _ = panel(s, MARGIN, Y_BODY + 6, CONTENT_W, 200, "Management KPI set")
    table(s, ix, iy, iw,
          ["KPI", "Baseline today", "Decision threshold", "Owner"],
          [["Same-day cash visibility", "58.18%", "\u226590% in approved cohort at G4", "Group Treasurer"],
           ["Payment exception rate", "6.30%", "\u226520% like-for-like reduction by G5", "Shared Services"],
           ["Certified movable cash", "$0 recognized", "Target only after VG01\u2013VG05", "Treasurer / Finance"],
           ["Rollback within four hours", "Not tested", "Pass before G3 and each scale event", "CIO / Process owner"],
           ["Change-attributable incidents", "Not available", "0 \u2014 any event triggers review", "Control owner / CIO"],
           ["Evidence-gate closure", "0%", "VG/CR packages closed per decision", "Finance Benefits"]],
          [0.27, 0.16, 0.35, 0.22], row_h=25)
    callout(s, "Baseline caution",
            "\u201cNot available\u201d and \u201c$0 recognized\u201d mean the evidence has not met "
            "the rule\u2014not that the risk or the opportunity is zero.")
    source(s, "Source: W4 KPI and benefits framework; full fourteen-KPI set in Appendix D.")


def slide_08(prs):
    s = new_slide(prs)
    page_frame(s, "Design principles", 8, TOTAL)
    title(s, "Eight principles resolve enterprise control versus local responsiveness")
    ix, iy, iw, _ = panel(s, MARGIN, Y_BODY + 6, CONTENT_W, 182, "Governing principles")
    bullets(s, ix, iy + 4, iw, [
        "One enterprise standards spine for policy, data contracts, and control definitions.",
        "Certified local context: restrictions, operating minimums, and emergency rights stay local and evidenced.",
        "Control by design—authorization, SoD, access, audit, and reconciliation specified before build.",
        "Staged, reversible change with a rehearsed return to the approved prior process.",
        "Evidence before value: no benefit enters a ledger without its own gate and Finance approval.",
        "Service continuity is non-negotiable, including the approved peak change freeze.",
        "Work around the three existing ERPs; sequence platform choices after data and control ownership.",
        "Non-compensating gates: a failed critical gate blocks the affected decision value.",
    ], gap=18.0)
    callout(s, "Gate rule",
            "A failed critical gate cannot be averaged away by a strong "
            "weighted score.", fill=OCHRE, label_color=NAVY)
    source(s, "Source: W3 design principles DP-01–DP-08.")


def slide_09(prs):
    s = new_slide(prs)
    page_frame(s, "Options and decision logic", 9, TOTAL)
    title(s, "Federated coordination offers the best balance with a local fallback")
    ix, iy, iw, _ = panel(s, MARGIN, Y_BODY + 6, CONTENT_W, 150, "Gate-then-score comparison")
    table(s, ix, iy, iw,
          ["Option", "Score", "Assessment"],
          [["Federated coordination", "87",
            "Leads all five plausible weight sensitivities; preserves local rights"],
           ["Local stabilization", "72",
            "The documented fallback; bounded improvement without the enterprise spine"],
           ["Globally coordinated", "60",
            "Held: integration readiness and affordability are unevidenced"]],
          [0.28, 0.12, 0.60], row_h=32,
          emphasis={0: {"color": TEAL, "bold": True}})
    body_text(s, MARGIN, 262, CONTENT_W,
              "Switch to local stabilization if global data/control ownership, minimum integration "
              "readiness, or affordability fails—or if any critical control, service, local-right, or "
              "resilience condition fails.")
    callout(s, "Boundary",
            "Scores compare design direction only. Every execution-evidence "
            "gate remains open.")
    source(s, "Source: W3 strategic options; W3 sensitivity outputs.")


def slide_10(prs):
    s = new_slide(prs)
    page_frame(s, "Recommended operating model", 10, TOTAL)
    title(s, "Centralize standards and evidence—not every operational decision")
    ix, iy, iw, _ = panel(s, MARGIN, Y_BODY + 6, CONTENT_W, 174, "Accountability spine")
    table(s, ix, iy, iw,
          ["Owner", "Owns", "Does not own"],
          [["Global Treasury", "Policy, data contracts, daily-position and mobility standards",
            "Local execution or emergency payment authority"],
           ["CIO", "Staged integration, access, auditability, cyber, resilience",
            "Business definitions or benefit recognition"],
           ["Finance", "Cost and benefit governance; recognition rules",
            "Operational payment execution"],
           ["Regions and BUs", "Certified local context, critical payments, emergency rights",
            "Enterprise standards or data contracts"]],
          [0.22, 0.44, 0.34], row_h=30)
    callout(s, "Design intent",
            "One control and data spine; local responsiveness preserved where "
            "service and law require it.")
    source(s, "Source: W3 future-state operating model; W4 governance and RACI.")


def slide_11(prs):
    s = new_slide(prs)
    page_frame(s, "Initiative portfolio", 11, TOTAL)
    title(s, "Seven initiatives start with data, governance, and value control")
    ix, iy, iw, _ = panel(s, MARGIN, Y_BODY + 6, CONTENT_W, 198, "Priority order")
    table(s, ix, iy, iw,
          ["#", "Initiative", "Score", "Why it leads"],
          [["1", "Cash data and visibility", "94", "Every later claim depends on certified source data"],
           ["2", "Benefits, cost, and KPI assurance", "92", "Prevents unvalidated value entering a ledger"],
           ["3", "Governance, service, and adoption", "86", "Decision rights before delivery"],
           ["4", "Payment controls and exceptions", "85", "Diagnose causes before standardizing"],
           ["5", "Liquidity certification", "83", "Mobility evidence before any cash claim"],
           ["6", "Integration, access, resilience", "80", "Staged; sequenced after ownership"],
           ["7", "Account rationalization", "63", "Lowest value; candidate closures only"]],
          [0.05, 0.34, 0.10, 0.51], row_h=21)
    callout(s, "Sequencing rule",
            "No platform procurement is proposed. Data, governance, and value "
            "control come first.")
    source(s, "Source: W4 initiative charters and prioritization model.")


def slide_12(prs):
    s = new_slide(prs)
    page_frame(s, "Business case", 12, TOTAL)
    title(s, "The case stays credible by keeping unlike value types separate")
    ix, iy, iw, _ = panel(s, MARGIN, Y_BODY + 6, CONTENT_W, 148, "Four non-additive ledgers")
    table(s, ix, iy, iw,
          ["Value type", "Diagnostic quantity", "Recognized today"],
          [["Cash release", "$21m / $35m / $46.2m screens", "$0"],
           ["Annual P&L", "$3,900 / $7,800 fee sensitivity", "$0"],
           ["Productive capacity", "50 / 150 hours per month", "$0"],
           ["Risk reduction", "Exposure not quantified", "NOT QUANTIFIED"]],
          [0.30, 0.44, 0.26], row_h=24, align_right=(2,))
    section_label(s, MARGIN, 272, "Provisional planning cost — analyst assumption")
    body_text(s, MARGIN, 288, CONTENT_W,
              "One-time $755k / $1.155m / $1.715m and recurring $175k / $281k / $442k per year. "
              "The base case fits the FY2026 $1.0–$1.5m ceiling; the high case breaches it and returns "
              "for staged approval. No vendor quote, statement of work, or rate card exists.")
    callout(s, "Boundary",
            "Never add these ledgers. ROI, NPV, and payback stay unavailable "
            "while recognized benefit is $0.", fill=OCHRE, label_color=NAVY)
    source(s, "Source: W3 business case; W3 provisional cost estimates; W4 KPI and benefits framework.")


def slide_13(prs):
    s = new_slide(prs)
    page_frame(s, "Roadmap", 13, TOTAL)
    title(s, "Use 90 days to earn a bounded test before scaling",
          subtitle="Evidence mobilization first; every wave sits behind its own gate")
    bands = [
        ("Days 1–30", "Own the facts",
         "Record direction and rights; reconcile the 55-account and 7,600-record populations; "
         "confirm exact North America freeze dates."),
        ("Days 31–60", "Prove conditions",
         "Mobility and local-right reviews; service and control design; bottom-up CR01–CR10 "
         "cost ranges."),
        ("Days 61–90", "Make ready, then return",
         "Link source evidence; lock target rules; rehearse rollback safely; return for a "
         "separate G3 decision."),
        ("Months 4–18", "Only if evidence holds",
         "Wave 1 after separate approval and outside the freeze; Wave 2 expands only while "
         "evidence holds."),
    ]
    y = Y_BODY + 10
    for i, (label, head, body) in enumerate(bands):
        rect(s, MARGIN, y, 2.5, 34, fill=TEAL if i < 3 else OCHRE)
        f = textbox(s, MARGIN + 12, y + 1, 74, 11)
        write(f, label.upper(), size=PT_LABEL, color=TEAL, bold=True, spacing=1.2)
        g = textbox(s, MARGIN + 12, y + 14, 128, 14)
        write(g, head, size=PT_LEAD, color=NAVY, bold=True)
        h = textbox(s, MARGIN + 160, y + 2, CONTENT_W - 162, 32)
        write(h, body, size=PT_BODY, color=INK, line=1.25)
        y += 44
        if i < len(bands) - 1:
            hrule(s, MARGIN, y - 5, CONTENT_W, color=RULE_LT, weight=0.5)
    callout(s, "Freeze constraint",
            "No North America payment-routing or approval-workflow production "
            "change during the eight-week peak freeze; NA BU CFO sign-off required.",
            fill=OCHRE, label_color=NAVY)
    source(s, "Source: W4 implementation roadmap; W3 payment pilot charter; risk R031.")


def slide_14(prs):
    s = new_slide(prs)
    page_frame(s, "Risk and governance", 14, TOTAL)
    title(s, "Governance converts the roadmap into stop, switch, and scale decisions")
    ix, iy, iw, _ = panel(s, MARGIN, Y_BODY + 6, CONTENT_W, 184, "Trigger and response")
    table(s, ix, iy, iw,
          ["Trigger", "Response", "Decision owner"],
          [["Data or definition remains unowned", "Narrow scope; hold the affected gate", "CFO / Group Treasurer"],
           ["Cash mobility uncertified", "No cash claim; certification continues", "Group Treasurer / Finance"],
           ["Service, control, or rollback failure", "Stop, revert, and investigate", "CIO / BU Finance"],
           ["Affordability evidence absent", "No funding decision; return for staged approval", "CFO / Finance"],
           ["Value formula drifts", "Reject the calculation; rebuild by value type", "Finance"]],
          [0.34, 0.42, 0.24], row_h=26)
    callout(s, "Non-compensating rule",
            "Critical risk cannot be averaged away by strong performance "
            "elsewhere.")
    source(s, "Source: W4 governance and RACI; W4 risk register; W3 decision log.")


def slide_15(prs):
    s = new_slide(prs)
    page_frame(s, "Decision", 15, TOTAL)
    title(s, "Approve the direction and owners; return at Day 90")
    section_label(s, MARGIN, Y_BODY + 6, "Five commitments requested")
    numbered_list(s, MARGIN, Y_BODY + 26, CONTENT_W, [
        "Confirm the direction, the local-stabilization fallback, and the no-execution boundary at Day 0.",
        "Accept the named functional owners and data contracts by Day 30.",
        "Close the exact North America freeze dates and the sign-off path by Day 30.",
        "Produce bottom-up CR01–CR10 cost evidence by Day 60.",
        "Take a separate stop / extend / bounded-pilot decision at G3 on Day 90.",
    ], gap=25.0)
    callout(s, "What is not requested",
            "No production change, cash movement, account closure, labor "
            "action, benefit recognition, procurement, or scale.")
    source(s, "Source: W4 decision log; W4 weekly update; final recommendation memo.")


def slide_16(prs):
    s = new_slide(prs)
    page_frame(s, "Appendix A · Method", 16, TOTAL)
    title(s, "Definitions, data quality, and methods bound every metric")
    ix, iy, iw, _ = panel(s, MARGIN, Y_BODY + 6, CONTENT_W, 186, "Method limits carried with each claim")
    table(s, ix, iy, iw,
          ["Metric family", "Method", "Stated limit"],
          [["Visibility", "Reporting-date equality proxy", "Not start-of-day or elapsed-24-hour performance"],
           ["Liquidity", "Trailing-window screen after buffers", "Not surplus, transferable cash, or authority"],
           ["Payments", "Supplied flags, deduplicated cohorts", "Association only; overlap counted once"],
           ["Accounts", "Dormant + legacy + zero-payment screen", "Candidates only; no approved closure"],
           ["Capacity", "Management-estimated activity hours", "Not observed time or removable labour"]],
          [0.22, 0.36, 0.42], row_h=27)
    callout(s, "Certification status",
            "52/52 structural checks and 13/13 reconciliation controls pass; "
            "source certification remains open.")
    source(s, "Source: W1 data-quality report; W2 metric contract; final evidence register.")


def slide_17(prs):
    s = new_slide(prs)
    page_frame(s, "Appendix B · Alternatives", 17, TOTAL)
    title(s, "Sensitivities and rejected alternatives support the choice")
    ix, iy, iw, _ = panel(s, MARGIN, Y_BODY + 6, CONTENT_W, 192, "Considered and rejected")
    table(s, ix, iy, iw,
          ["Alternative", "Why it was rejected"],
          [["Immediate global coordination", "Integration readiness and affordability are unevidenced"],
           ["Indefinite local-only remediation", "Leaves the enterprise data and control gap unresolved"],
           ["Bulk account closure", "Only four candidates; local purpose and continuity unvalidated"],
           ["Automatic payment automation", "Causes unproven; required control work not yet classified"],
           ["Early labour or value claims", "No observed time, approved formula, or Finance recognition"]],
          [0.36, 0.64], row_h=28)
    callout(s, "Robustness",
            "Federated leads all five plausible weight sensitivities; the "
            "switch conditions remain explicit.")
    source(s, "Source: W3 option sensitivity outputs; W3 business case downside; W4 decision log.")


def slide_18(prs):
    s = new_slide(prs)
    page_frame(s, "Appendix C · Traceability", 18, TOTAL)
    title(s, "Source and assumption controls keep every claim auditable")
    ix, iy, iw, _ = panel(s, MARGIN, Y_BODY + 6, CONTENT_W, 190, "Evidence-label convention")
    table(s, ix, iy, iw,
          ["Label", "Meaning"],
          [["PROGRAM-STANDARD", "Programme rule or template requirement"],
           ["ACG-DATA", "Supplied client material or project dataset"],
           ["ANALYST-CALC", "Reproducible calculation from supplied data"],
           ["ANALYST-ASSUMPTION", "Unverified input requiring validation"],
           ["ANALYST-JUDGMENT", "Interpretation, score, threshold, or proposed action"],
           ["JPM-PUBLIC", "Public context; never proof of ACG performance"]],
          [0.30, 0.70], row_h=23)
    callout(s, "Rebuild path",
            "Every published figure regenerates from documented scripts with "
            "fail-closed tests.")
    source(s, "Source: final source register; final assumptions register; final evidence register.")


def slide_19(prs):
    s = new_slide(prs)
    page_frame(s, "Appendix D \u00b7 Full KPI set", 19, TOTAL)
    title(s, "The remaining eight KPIs complete the performance contract",
          subtitle="Tracked by the owning function; escalated to the committee only on breach")
    ix, iy, iw, _ = panel(s, MARGIN, Y_BODY + 6, CONTENT_W, 204, "Functional KPIs")
    table(s, ix, iy, iw,
          ["KPI", "Baseline today", "Decision threshold", "Owner"],
          [["Two-plus-day delayed account-days", "2,534 of 9,955", "\u226575% reduction in cohort by G5", "Treasury Data Owner"],
           ["Reconciled cash positions", "Not available", "100% before a funding decision", "Group Treasurer"],
           ["Manual-touch rate", "31.51%", "Target after root-cause review", "Shared Services"],
           ["Late-release rate", "5.00%", "No deterioration at G4; \u226520% by G5", "Shared Services / BU"],
           ["Emergency-payment compliance", "Not available", "100%", "BU Finance / Control"],
           ["Trained and access-certified roles", "0%", "100% before production access", "Change Lead / CIO"],
           ["Verified fee removal", "$0 recognized", "Recognition only after VG06\u2013VG07", "Finance / Treasurer"],
           ["Productively redeployed hours", "0 recognized", "Recognition only after VG08\u2013VG10", "Shared Services / Finance"]],
          [0.30, 0.16, 0.32, 0.22], row_h=19)
    callout(s, "Performance contract",
            "Every KPI needs a controlled population, definition, formula, "
            "source, owner, and change history before it is used.")
    source(s, "Source: W4 KPI and benefits framework; W4 KPI dictionary CSV.")


BUILDERS = [slide_01, slide_02, slide_03, slide_04, slide_05, slide_06,
            slide_07, slide_08, slide_09, slide_10, slide_11, slide_12,
            slide_13, slide_14, slide_15, slide_16, slide_17, slide_18,
            slide_19]


def build(out_path: Path) -> Path:
    prs = Presentation()
    prs.slide_width = _pt(PW)
    prs.slide_height = _pt(PH)
    for builder in BUILDERS:
        builder(prs)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out_path))
    return out_path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out = root / "deliverables" / "final" / "Northstar_Final_Executive_Deck.pptx"
    build(out)
    print("Wrote %s (%d slides, Week 2/3 house style)" % (out, len(BUILDERS)))


if __name__ == "__main__":
    main()
