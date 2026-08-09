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
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

try:
    import handbook_chapters
except ModuleNotFoundError:  # запуск не из каталога tools/
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import handbook_chapters


ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_mkdocs"  # единственный источник правды для контента доков
IMG_DIR = SRC / "docs" / "images"
OUT = ROOT / "forex-handbook.pdf"

# Имена зарегистрированных шрифтов с кириллицей
FONT_REGULAR = "DejaVu"
FONT_MONO = "DejaVuMono"


def register_cyrillic_fonts() -> None:
    """
    Регистрирует DejaVu Sans (+ Mono) для reportlab.

    Без этого reportlab использует Helvetica/Courier, в которых НЕТ кириллицы,
    и весь русский текст в PDF превращается в чёрные квадраты (tofu).

    Шрифты берутся из matplotlib (он уже в зависимостях) — никаких новых
    пакетов или системных зависимостей.
    """
    import matplotlib.font_manager as fm

    ttf_dir = Path(fm.findfont("DejaVu Sans")).parent
    variants = {
        FONT_REGULAR: ttf_dir / "DejaVuSans.ttf",
        f"{FONT_REGULAR}-Bold": ttf_dir / "DejaVuSans-Bold.ttf",
        f"{FONT_REGULAR}-Italic": ttf_dir / "DejaVuSans-Oblique.ttf",
        f"{FONT_REGULAR}-BoldItalic": ttf_dir / "DejaVuSans-BoldOblique.ttf",
        FONT_MONO: ttf_dir / "DejaVuSansMono.ttf",
        f"{FONT_MONO}-Bold": ttf_dir / "DejaVuSansMono-Bold.ttf",
    }
    for name, path in variants.items():
        if not path.exists():
            print(f"  ⚠️  Шрифт не найден: {path}", file=sys.stderr)
            continue
        pdfmetrics.registerFont(TTFont(name, str(path)))

    # Связываем варианты в семейство, чтобы <b>, <i> работали в Paragraph
    registerFontFamily(
        FONT_REGULAR,
        normal=FONT_REGULAR,
        bold=f"{FONT_REGULAR}-Bold",
        italic=f"{FONT_REGULAR}-Italic",
        boldItalic=f"{FONT_REGULAR}-BoldItalic",
    )
    registerFontFamily(
        FONT_MONO,
        normal=FONT_MONO,
        bold=f"{FONT_MONO}-Bold",
        italic=FONT_MONO,
        boldItalic=f"{FONT_MONO}-Bold",
    )


# Состав глав живёт в отдельном модуле без зависимости от reportlab, чтобы его
# можно было проверять тестами в обычном прогоне (см. handbook_chapters.py).
# Отсутствующие файлы build() пропускает автоматически (path.exists()).
CHAPTERS_RU = handbook_chapters.chapters("ru")
CHAPTERS_EN = handbook_chapters.chapters("en")
CHAPTERS_UZ = handbook_chapters.chapters("uz")

LANG_CONFIGS = {
    "ru": {
        "chapters": CHAPTERS_RU,
        "out": ROOT / "forex-handbook.pdf",
        "title": "Forex Trading Handbook",
        "subtitle": "Полный учебный гайд для новичка",
        "warning": (
            "Этот документ — образовательный материал, а НЕ финансовый совет. "
            "Forex — высокорисковая деятельность. По данным ESMA, 74-89% розничных "
            "трейдеров теряют деньги. Никогда не торгуй на деньги, которые не "
            "готов потерять. Минимум 3 месяца демо-счёта."
        ),
    },
    "en": {
        "chapters": CHAPTERS_EN,
        "out": ROOT / "forex-handbook-en.pdf",
        "title": "Forex Trading Handbook",
        "subtitle": "A complete learning guide for beginners",
        "warning": (
            "This document is educational material, NOT financial advice. "
            "Forex is a high-risk activity. According to ESMA data, 74-89% of "
            "retail traders lose money. Never trade with money you cannot afford "
            "to lose. Minimum 3 months on a demo account before going live."
        ),
    },
    "uz": {
        "chapters": CHAPTERS_UZ,
        "out": ROOT / "forex-handbook-uz.pdf",
        "title": "Forex Treyding Qo'llanmasi",
        "subtitle": "Yangi boshlovchilar uchun to'liq o'quv qo'llanma",
        "warning": (
            "Bu hujjat — o'quv materiali, moliyaviy maslahat EMAS. "
            "Forex — yuqori xavfli faoliyat. ESMA ma'lumotlariga ko'ra, chakana "
            "treyderlarning 74-89% pul yo'qotadi. Hech qachon yo'qotishga tayyor "
            "bo'lmagan pulga savdo qilmang. Real hisobdan oldin kamida 3 oy demo."
        ),
    },
}

# Backwards-compatible alias for old code paths
CHAPTERS = CHAPTERS_RU


# ---------- Стили ----------


def make_styles():
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName=f"{FONT_REGULAR}-Bold",
            fontSize=36,
            textColor=colors.HexColor("#1e40af"),
            spaceAfter=20,
            alignment=TA_CENTER,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["Normal"],
            fontName=FONT_REGULAR,
            fontSize=18,
            textColor=colors.HexColor("#374151"),
            spaceAfter=12,
            alignment=TA_CENTER,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName=f"{FONT_REGULAR}-Bold",
            fontSize=22,
            textColor=colors.HexColor("#1e40af"),
            spaceBefore=20,
            spaceAfter=12,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName=f"{FONT_REGULAR}-Bold",
            fontSize=16,
            textColor=colors.HexColor("#1f2937"),
            spaceBefore=16,
            spaceAfter=8,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "h3",
            parent=base["Heading3"],
            fontName=f"{FONT_REGULAR}-Bold",
            fontSize=13,
            textColor=colors.HexColor("#374151"),
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName=FONT_REGULAR,
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base["BodyText"],
            fontName=FONT_REGULAR,
            fontSize=10,
            leading=14,
            leftIndent=15,
            bulletIndent=5,
            spaceAfter=3,
        ),
        "code": ParagraphStyle(
            "code",
            parent=base["Code"],
            fontName=FONT_MONO,
            fontSize=8,
            leading=10,
            leftIndent=10,
            rightIndent=10,
            backColor=colors.HexColor("#f3f4f6"),
            borderColor=colors.HexColor("#d1d5db"),
            borderWidth=1,
            borderPadding=6,
            spaceAfter=10,
        ),
        "warning": ParagraphStyle(
            "warning",
            parent=base["BodyText"],
            fontName=FONT_REGULAR,
            fontSize=10,
            leading=14,
            backColor=colors.HexColor("#fee2e2"),
            borderColor=colors.HexColor("#dc2626"),
            borderWidth=1,
            borderPadding=8,
            spaceAfter=10,
            leftIndent=5,
            rightIndent=5,
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
                    full = ROOT / Path(img_path).name
                else:
                    full = ROOT / img_path
                if full.exists():
                    try:
                        img = Image(
                            str(full),
                            width=15 * cm,
                            height=10 * cm,
                            kind="proportional",
                        )
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
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def parse_inline(text: str) -> str:
    """Простая обработка inline markdown."""
    # Bold
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    # Italic
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    # Inline code (DejaVuMono поддерживает кириллицу, Courier — нет)
    text = re.sub(r"`([^`]+)`", rf"<font name='{FONT_MONO}'>\1</font>", text)
    # Strip markdown links — оставляем только текст
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text


def build(lang: str = "ru") -> int:
    if lang not in LANG_CONFIGS:
        print(
            f"Unknown lang: {lang!r}. Use one of: {list(LANG_CONFIGS)}", file=sys.stderr
        )
        return 2

    cfg = LANG_CONFIGS[lang]
    out_path = cfg["out"]
    print(f"Building {lang.upper()} PDF → {out_path.name}")
    register_cyrillic_fonts()

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title=cfg["title"],
        author="forex-trading project",
    )

    styles = make_styles()
    story = []

    # Title page
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph("📈 FOREX", styles["title"]))
    story.append(Paragraph(cfg["subtitle"], styles["subtitle"]))
    story.append(Spacer(1, 2 * cm))
    if lang == "ru":
        tagline = "Теория · Технический анализ · Стратегии<br/>Психология · Шаблоны · Инструменты"
        warning_label = "⚠️ ВНИМАНИЕ:"
    elif lang == "uz":
        tagline = "Nazariya · Texnik tahlil · Strategiyalar<br/>Psixologiya · Shablonlar · Asboblar"
        warning_label = "⚠️ DIQQAT:"
    else:
        tagline = "Theory · Technical analysis · Strategies<br/>Psychology · Templates · Tools"
        warning_label = "⚠️ WARNING:"
    story.append(Paragraph(tagline, styles["body"]))
    story.append(Spacer(1, 4 * cm))
    story.append(
        Paragraph(
            f"<b>{warning_label}</b><br/><br/>{cfg['warning']}",
            styles["warning"],
        )
    )
    story.append(PageBreak())

    # Chapters
    for title, path in cfg["chapters"]:
        if not path.exists():
            print(f"  ⚠️  skip (not found): {path}")
            continue
        print(f"  ✓ {title} ← {path.name}")
        text = path.read_text(encoding="utf-8")
        flowables = parse_markdown(text, styles)
        story.extend(flowables)
        story.append(PageBreak())

    print("\nGenerating PDF...")
    doc.build(story)
    size_kb = out_path.stat().st_size // 1024
    print(f"\n✓ Done: {out_path}")
    print(f"  Size: {size_kb} KB")
    return 0


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Build the Forex handbook PDF")
    parser.add_argument(
        "--lang",
        choices=["ru", "en", "uz", "all"],
        default="ru",
        help="Language to build (default: ru). 'all' builds ru/en/uz.",
    )
    args = parser.parse_args()

    if args.lang == "all":
        rc = 0
        for lang in ("ru", "en", "uz"):
            rc |= build(lang)
        return rc
    return build(args.lang)


if __name__ == "__main__":
    sys.exit(main())
