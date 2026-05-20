#!/usr/bin/env python3
"""
Сборка всех .md в один PDF-учебник через reportlab.

Запуск:
  .venv/bin/python tools/build_pdf.py

Создаёт: forex-handbook.pdf — компактный учебник для печати.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)


ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "docs" / "images"
OUT = ROOT / "forex-handbook.pdf"


# Главы в нужном порядке
CHAPTERS = [
    ("Введение", ROOT / "КАК-ПОЛЬЗОВАТЬСЯ.md"),
    ("Основной гайд", ROOT / "forex-guide.md"),
    ("Технический анализ", ROOT / "docs" / "technical-analysis.md"),
    ("Учебная стратегия", ROOT / "docs" / "strategy-details.md"),
    ("Психология трейдинга", ROOT / "extras" / "psychology.md"),
    ("Глоссарий", ROOT / "extras" / "glossary.md"),
    ("FAQ", ROOT / "extras" / "faq.md"),
    ("Сравнение брокеров", ROOT / "extras" / "brokers-comparison.md"),
    ("Личный торговый план", ROOT / "extras" / "trading-plan-template.md"),
    ("Первые 100 дней", ROOT / "extras" / "first-100-days.md"),
    ("Anti-Tilt протокол", ROOT / "extras" / "anti-tilt-protocol.md"),
    ("Daily Routine", ROOT / "extras" / "daily-routine.md"),
    ("Чек-лист", ROOT / "extras" / "checklist-printable.md"),
    ("Emergency Card", ROOT / "extras" / "emergency-card.md"),
]


# ---------- Стили ----------

def make_styles():
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle(
            "title", parent=base["Title"],
            fontSize=36, textColor=colors.HexColor("#1e40af"),
            spaceAfter=20, alignment=TA_CENTER,
        ),
        "subtitle": ParagraphStyle(
            "subtitle", parent=base["Normal"],
            fontSize=18, textColor=colors.HexColor("#374151"),
            spaceAfter=12, alignment=TA_CENTER,
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"],
            fontSize=22, textColor=colors.HexColor("#1e40af"),
            spaceBefore=20, spaceAfter=12, keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "h2", parent=base["Heading2"],
            fontSize=16, textColor=colors.HexColor("#1f2937"),
            spaceBefore=16, spaceAfter=8, keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "h3", parent=base["Heading3"],
            fontSize=13, textColor=colors.HexColor("#374151"),
            spaceBefore=10, spaceAfter=6, keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "body", parent=base["BodyText"],
            fontSize=10, leading=14,
            alignment=TA_JUSTIFY, spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "bullet", parent=base["BodyText"],
            fontSize=10, leading=14, leftIndent=15,
            bulletIndent=5, spaceAfter=3,
        ),
        "code": ParagraphStyle(
            "code", parent=base["Code"],
            fontSize=8, leading=10,
            leftIndent=10, rightIndent=10,
            backColor=colors.HexColor("#f3f4f6"),
            borderColor=colors.HexColor("#d1d5db"),
            borderWidth=1, borderPadding=6,
            spaceAfter=10,
        ),
        "warning": ParagraphStyle(
            "warning", parent=base["BodyText"],
            fontSize=10, leading=14,
            backColor=colors.HexColor("#fee2e2"),
            borderColor=colors.HexColor("#dc2626"),
            borderWidth=1, borderPadding=8,
            spaceAfter=10, leftIndent=5, rightIndent=5,
        ),
    }
    return styles


def parse_markdown(text: str, styles: dict) -> list:
    """Примитивный markdown → reportlab flowables."""
    flowables = []
    lines = text.split("\n")
    i = 0
    in_code = False
    code_buffer = []

    while i < len(lines):
        line = lines[i]

        # Code block
        if line.strip().startswith("```"):
            if in_code:
                if code_buffer:
                    code_text = "<br/>".join(
                        ln.replace("&", "&amp;")
                          .replace("<", "&lt;")
                          .replace(">", "&gt;")
                        for ln in code_buffer
                    )
                    flowables.append(Paragraph(code_text, styles["code"]))
                code_buffer = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue

        if in_code:
            code_buffer.append(line)
            i += 1
            continue

        stripped = line.strip()

        # Headings
        if stripped.startswith("# "):
            flowables.append(Spacer(1, 12))
            flowables.append(Paragraph(escape_html(stripped[2:]), styles["h1"]))
        elif stripped.startswith("## "):
            flowables.append(Paragraph(escape_html(stripped[3:]), styles["h2"]))
        elif stripped.startswith("### "):
            flowables.append(Paragraph(escape_html(stripped[4:]), styles["h3"]))

        # Blockquote (предупреждения)
        elif stripped.startswith("> "):
            text = escape_html(stripped[2:])
            text = parse_inline(text)
            flowables.append(Paragraph(text, styles["warning"]))

        # Bullets
        elif stripped.startswith(("- ", "* ", "+ ")):
            text = parse_inline(escape_html(stripped[2:]))
            flowables.append(Paragraph(f"• {text}", styles["bullet"]))

        # Numbered list
        elif re.match(r"^\d+\.\s", stripped):
            text = parse_inline(escape_html(re.sub(r"^\d+\.\s", "", stripped)))
            flowables.append(Paragraph(f"• {text}", styles["bullet"]))

        # Horizontal rule
        elif stripped == "---":
            flowables.append(Spacer(1, 6))

        # Empty line
        elif not stripped:
            flowables.append(Spacer(1, 4))

        # Image (markdown)
        elif stripped.startswith("!["):
            m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", stripped)
            if m:
                img_path = m.group(2)
                # Резолвим относительный путь
                if img_path.startswith("images/"):
                    full = IMG_DIR / Path(img_path).name
                elif img_path.startswith("../"):
                    full = (ROOT / Path(img_path).name)
                else:
                    full = ROOT / img_path
                if full.exists():
                    try:
                        img = Image(str(full), width=15 * cm, height=10 * cm,
                                    kind="proportional")
                        flowables.append(img)
                        flowables.append(Spacer(1, 4))
                    except Exception:
                        pass

        # Regular paragraph
        else:
            text = parse_inline(escape_html(stripped))
            flowables.append(Paragraph(text, styles["body"]))

        i += 1

    return flowables


def escape_html(text: str) -> str:
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))


def parse_inline(text: str) -> str:
    """Простая обработка inline markdown."""
    # Bold
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    # Italic
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    # Inline code
    text = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", text)
    # Strip markdown links — оставляем только текст
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text


def main() -> int:
    print("Сборка PDF учебника...")

    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title="Forex Trading Handbook",
        author="forex-trading project",
    )

    styles = make_styles()
    story = []

    # Титульный лист
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph("📈 FOREX", styles["title"]))
    story.append(Paragraph("Полный учебный гайд для новичка", styles["subtitle"]))
    story.append(Spacer(1, 2 * cm))
    story.append(Paragraph(
        "Теория · Технический анализ · Стратегии<br/>"
        "Психология · Шаблоны · Инструменты",
        styles["body"],
    ))
    story.append(Spacer(1, 4 * cm))
    story.append(Paragraph(
        "<b>⚠️ ВНИМАНИЕ:</b><br/><br/>"
        "Этот документ — образовательный материал, а НЕ финансовый совет. "
        "Forex — высокорисковая деятельность. По данным ESMA, "
        "74-89% розничных трейдеров теряют деньги. Никогда не торгуй "
        "на деньги, которые не готов потерять. "
        "Прежде чем рисковать — минимум 3 месяца на демо-счёте.",
        styles["warning"],
    ))
    story.append(PageBreak())

    # Главы
    for title, path in CHAPTERS:
        if not path.exists():
            print(f"  ⚠️  пропускаю (не найдено): {path}")
            continue

        print(f"  ✓ {title} ← {path.name}")
        text = path.read_text(encoding="utf-8")
        flowables = parse_markdown(text, styles)
        story.extend(flowables)
        story.append(PageBreak())

    print(f"\nГенерирую PDF...")
    doc.build(story)
    size_kb = OUT.stat().st_size // 1024
    print(f"\n✓ Готово: {OUT}")
    print(f"  Размер: {size_kb} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
