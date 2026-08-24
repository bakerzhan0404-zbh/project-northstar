#!/usr/bin/env python3
"""Convert the repository's simple memo Markdown into an HTML fragment.

This deliberately small renderer supports the structures used by the final
recommendation memo: headings, paragraphs, ordered/unordered lists, tables,
bold text, and inline code. It has no third-party dependencies.
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path
from typing import Iterable, List


TABLE_RULE = re.compile(r"^:?-{3,}:?$")
ORDERED_ITEM = re.compile(r"^\d+\.\s+(.*)$")

STANDALONE_CSS = """
@page { size: A4; margin: 16mm; }
body { font-family: Arial, Helvetica, sans-serif; color: #172033; font-size: 10pt; line-height: 1.34; }
.memo { max-width: 100%; }
h1 { color: #17365d; font-size: 22pt; margin: 0 0 12pt; padding-bottom: 7pt; border-bottom: 2px solid #c8a45d; }
h2 { color: #17365d; font-size: 14pt; margin: 14pt 0 6pt; page-break-after: avoid; }
h3 { color: #172033; font-size: 11.5pt; margin: 10pt 0 4pt; page-break-after: avoid; }
p { margin: 4pt 0 7pt; break-inside: avoid; }
.memo-meta { margin: 0 0 2pt; }
ul, ol { margin: 4pt 0 7pt 18pt; padding: 0; }
li { margin: 1.5pt 0; }
table { width: 100%; border-collapse: collapse; margin: 7pt 0 9pt; font-size: 8.5pt; table-layout: fixed; page-break-inside: avoid; }
thead { display: table-header-group; }
tr { page-break-inside: avoid; }
th { background: #17365d; color: white; font-weight: 600; text-align: left; }
th, td { border: 1px solid #cbd3df; padding: 4pt 5pt; vertical-align: top; word-break: normal; overflow-wrap: normal; hyphens: none; }
tr:nth-child(even) td { background: #f4f7fa; }
code { font-family: Menlo, Consolas, monospace; font-size: 8.5pt; }
""".strip()


def inline_markup(value: str) -> str:
    """Escape HTML and render the limited inline syntax used by the memo."""
    rendered = html.escape(value.strip(), quote=False)
    rendered = re.sub(r"`([^`]+)`", r"<code>\1</code>", rendered)
    rendered = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", rendered)
    return rendered


def table_cells(line: str) -> List[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_table_rule(line: str) -> bool:
    cells = table_cells(line)
    return bool(cells) and all(TABLE_RULE.fullmatch(cell) for cell in cells)


def render_table(lines: List[str], start: int) -> tuple[str, int]:
    headers = table_cells(lines[start])
    rows: List[List[str]] = []
    cursor = start + 2
    while cursor < len(lines) and lines[cursor].lstrip().startswith("|"):
        rows.append(table_cells(lines[cursor]))
        cursor += 1

    width_profiles = {
        "Option": [17, 9, 20, 54],
        "Value type": [16, 24, 16, 44],
        "Risk": [27, 24, 49],
        "Decision/action": [34, 19, 9, 38],
    }
    widths = width_profiles.get(headers[0])
    table_class = f" {headers[0].lower().replace('/', '-').replace(' ', '-')}-table"
    parts = [f'<table class="memo-table{table_class}">']
    if widths and len(widths) == len(headers):
        parts.append("<colgroup>")
        parts.extend(f'<col style="width:{width}%">' for width in widths)
        parts.append("</colgroup>")
    parts.append("<thead><tr>")
    parts.extend(f"<th>{inline_markup(cell)}</th>" for cell in headers)
    parts.append("</tr></thead><tbody>")
    for row in rows:
        padded = row + [""] * max(0, len(headers) - len(row))
        parts.append("<tr>")
        parts.extend(f"<td>{inline_markup(cell)}</td>" for cell in padded[: len(headers)])
        parts.append("</tr>")
    parts.append("</tbody></table>")
    return "".join(parts), cursor


def markdown_to_html(lines: Iterable[str]) -> str:
    source = list(lines)
    output: List[str] = ['<article class="memo">']
    paragraph: List[str] = []
    list_kind: str | None = None

    def flush_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{inline_markup(' '.join(paragraph))}</p>")
            paragraph.clear()

    def close_list() -> None:
        nonlocal list_kind
        if list_kind:
            output.append(f"</{list_kind}>")
            list_kind = None

    cursor = 0
    while cursor < len(source):
        line = source[cursor].rstrip()
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            close_list()
            cursor += 1
            continue

        if (
            stripped.startswith("|")
            and cursor + 1 < len(source)
            and is_table_rule(source[cursor + 1])
        ):
            flush_paragraph()
            close_list()
            table, cursor = render_table(source, cursor)
            output.append(table)
            continue

        heading = re.match(r"^(#{1,3})\s+(.*)$", stripped)
        if heading:
            flush_paragraph()
            close_list()
            level = len(heading.group(1))
            heading_text = heading.group(2)
            output.append(f"<h{level}>{inline_markup(heading_text)}</h{level}>")
            cursor += 1
            continue

        if stripped.startswith(("**To:**", "**From:**", "**Date:**", "**Subject:**", "**Classification:**")):
            flush_paragraph()
            close_list()
            output.append(f'<div class="memo-meta">{inline_markup(stripped)}</div>')
            cursor += 1
            continue

        unordered = re.match(r"^-\s+(.*)$", stripped)
        ordered = ORDERED_ITEM.match(stripped)
        if unordered or ordered:
            flush_paragraph()
            requested_kind = "ul" if unordered else "ol"
            if list_kind != requested_kind:
                close_list()
                output.append(f"<{requested_kind}>")
                list_kind = requested_kind
            item = unordered.group(1) if unordered else ordered.group(1)
            output.append(f"<li>{inline_markup(item)}</li>")
            cursor += 1
            continue

        close_list()
        paragraph.append(stripped)
        cursor += 1

    flush_paragraph()
    close_list()
    output.append("</article>")
    return "\n".join(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_markdown", type=Path)
    parser.add_argument("output_html", type=Path)
    parser.add_argument("--standalone", action="store_true", help="Write a complete print-ready HTML document")
    args = parser.parse_args()

    fragment = markdown_to_html(args.input_markdown.read_text(encoding="utf-8").splitlines())
    if args.standalone:
        document = (
            "<!doctype html>\n<html><head><meta charset=\"utf-8\">\n"
            "<title>Project Northstar — Final Executive Recommendation</title>\n"
            f"<style>{STANDALONE_CSS}</style>\n"
            "</head><body>\n"
            f"{fragment}\n"
            "</body></html>\n"
        )
    else:
        document = fragment + "\n"
    args.output_html.write_text(document, encoding="utf-8")
    print(f"Wrote {args.output_html}")


if __name__ == "__main__":
    main()
