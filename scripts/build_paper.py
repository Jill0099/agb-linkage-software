"""Render an English Markdown manuscript as a standalone, paginated PDF."""

from __future__ import annotations

import argparse
import html
import os
import re
import tempfile
from pathlib import Path
from typing import Any

import mistune
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image,
    ListFlowable,
    ListItem,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

WIDTH = A4[0] - 40 * mm
DASHES = str.maketrans({"–": "-", "—": "-", "‑": "-", "−": "-"})


def inline(nodes: list[dict[str, Any]]) -> str:
    """Convert a controlled subset of Markdown inline nodes to PDF markup."""
    result: list[str] = []
    for node in nodes:
        kind = node["type"]
        text = html.escape(node.get("raw", "").translate(DASHES))
        children = inline(node.get("children", []))
        if kind == "text":
            result.append(text)
        elif kind == "strong":
            result.append(f"<b>{children}</b>")
        elif kind == "emphasis":
            result.append(f"<i>{children}</i>")
        elif kind == "codespan":
            result.append(f'<font name="Courier" size="8">{text}</font>')
        elif kind == "link":
            url = node.get("attrs", {}).get("url", "")
            if re.match(r"^https?://", url):
                target = html.escape(url, quote=True)
                result.append(
                    f'<link href="{target}" color="#15556d">{children}</link>'
                )
            else:
                result.append(children)
        elif kind in {"softbreak", "linebreak"}:
            result.append(" " if kind == "softbreak" else "<br/>")
        elif kind == "image":
            continue
        elif kind in {"inline_html", "block_html"}:
            result.append(text)
        else:
            result.append(children or text)
    return "".join(result)


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    body = ParagraphStyle(
        "PaperBody",
        parent=base["BodyText"],
        fontName="Times-Roman",
        fontSize=10.5,
        leading=14.2,
        spaceAfter=7,
    )
    return {
        "body": body,
        "title": ParagraphStyle(
            "PaperTitle",
            parent=body,
            fontName="Times-Bold",
            fontSize=19,
            leading=23,
            alignment=TA_CENTER,
            spaceAfter=16,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "PaperSection",
            parent=body,
            fontName="Times-Bold",
            fontSize=13,
            leading=16,
            spaceBefore=13,
            spaceAfter=7,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "PaperSubsection",
            parent=body,
            fontName="Times-Bold",
            fontSize=11,
            leading=14,
            spaceBefore=9,
            spaceAfter=5,
            keepWithNext=True,
        ),
        "cell": ParagraphStyle(
            "PaperTable",
            parent=body,
            fontSize=8.5,
            leading=11,
            spaceAfter=0,
        ),
        "code": ParagraphStyle(
            "PaperCode",
            parent=body,
            fontName="Courier",
            fontSize=7.3,
            leading=10,
        ),
        "quote": ParagraphStyle(
            "PaperQuote",
            parent=body,
            leftIndent=12,
            rightIndent=12,
            fontName="Times-Italic",
        ),
    }


def table_flowable(node: dict[str, Any], style: ParagraphStyle) -> Table:
    rows: list[list[Paragraph]] = []
    for section in node["children"]:
        if section["type"] == "table_head":
            rows.append(
                [Paragraph(inline(c["children"]), style) for c in section["children"]]
            )
        elif section["type"] == "table_body":
            for row in section["children"]:
                rows.append(
                    [Paragraph(inline(c["children"]), style) for c in row["children"]]
                )
    if not rows or not rows[0]:
        raise ValueError("Empty manuscript table")
    column_count = len(rows[0])
    if any(len(row) != column_count for row in rows):
        raise ValueError("Inconsistent manuscript table columns")
    weights = [
        max(20, min(75, max(len(cell.getPlainText()) for cell in col)))
        for col in zip(*rows, strict=True)
    ]
    widths = [WIDTH * weight / sum(weights) for weight in weights]
    table = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef0")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#789099")),
                ("LINEBELOW", (0, 1), (-1, -1), 0.25, colors.HexColor("#ced7da")),
            ]
        )
    )
    return table


def flowables(
    nodes: list[dict[str, Any]],
    stylesheet: dict[str, ParagraphStyle],
    manuscript_dir: Path,
) -> list[Any]:
    result: list[Any] = []
    for node in nodes:
        kind = node["type"]
        if kind == "heading":
            level = node.get("attrs", {}).get("level", 2)
            style = "title" if level == 1 else "h2" if level == 2 else "h3"
            result.append(Paragraph(inline(node["children"]), stylesheet[style]))
        elif kind in {"paragraph", "block_text"}:
            children = node.get("children", [])
            for child in children:
                if child["type"] == "image":
                    path = (manuscript_dir / child["attrs"]["url"]).resolve()
                    picture = Image(str(path))
                    ratio = min(WIDTH / picture.imageWidth, 230 / picture.imageHeight)
                    picture.drawWidth = picture.imageWidth * ratio
                    picture.drawHeight = picture.imageHeight * ratio
                    result.extend([picture, Spacer(1, 8)])
            text = inline(children)
            if text.strip():
                result.append(Paragraph(text, stylesheet["body"]))
        elif kind == "table":
            result.extend([table_flowable(node, stylesheet["cell"]), Spacer(1, 9)])
        elif kind == "list":
            items = [
                ListItem(flowables(item["children"], stylesheet, manuscript_dir))
                for item in node["children"]
            ]
            ordered = node.get("attrs", {}).get("ordered", False)
            result.append(
                ListFlowable(
                    items,
                    bulletType="1" if ordered else "bullet",
                    leftIndent=17,
                    bulletFontName="Times-Roman",
                    bulletFontSize=9,
                    start=node.get("attrs", {}).get("start", 1) if ordered else None,
                )
            )
        elif kind == "block_code":
            result.append(
                Preformatted(
                    node.get("raw", "").translate(DASHES),
                    stylesheet["code"],
                    maxLineLength=89,
                )
            )
        elif kind == "block_quote":
            result.extend(flowables(node["children"], stylesheet, manuscript_dir))
        elif kind in {"blank_line", "thematic_break"}:
            continue
        else:
            text = inline(node.get("children", []))
            if text:
                result.append(Paragraph(text, stylesheet["body"]))
    return result


def footer(canvas: Any, document: Any) -> None:
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#53656d"))
    canvas.setFont("Times-Roman", 8)
    canvas.drawString(20 * mm, 12 * mm, "Wang | Location-AGB linkage | Working draft")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, str(document.page))
    canvas.restoreState()


def build(manuscript: Path, output: Path) -> None:
    if manuscript.resolve() == output.resolve():
        raise ValueError("PDF output must not replace its Markdown source.")
    if output.suffix.lower() != ".pdf":
        raise ValueError("PDF output must have a .pdf extension.")
    text = manuscript.read_text(encoding="utf-8")
    parser = mistune.create_markdown(renderer="ast", plugins=["table"])
    nodes = parser(text)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        prefix=".working-paper-", suffix=".pdf", dir=output.parent, delete=False
    ) as stream:
        temporary = Path(stream.name)
    try:
        document = SimpleDocTemplate(
            str(temporary),
            pagesize=A4,
            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=18 * mm,
            bottomMargin=20 * mm,
            title="Local Aboveground Biomass around Chinese Listed Companies",
            author="Yueyang Wang",
            subject="Measurement working draft; source and spatial validation pending",
        )
        document.build(
            flowables(nodes, styles(), manuscript.parent),
            onFirstPage=footer,
            onLaterPages=footer,
        )
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manuscript", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build(args.manuscript, args.output)
    print(f"Created {args.output}")


if __name__ == "__main__":
    main()
