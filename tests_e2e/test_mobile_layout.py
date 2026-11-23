"""Раскладка на телефонной ширине: контент не должен схлопываться."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

PHONE = {"width": 390, "height": 844}
PAGES = ["/tools/exam/", "/tools/risk-profile/", "/journal/web-journal/", "/"]


def measure(page):
    return page.evaluate(
        """
        () => {
          const w = el => Math.round(el.getBoundingClientRect().width);
          const row = document.querySelector('.md-main__inner');
          const own = /md-sidebar|md-content/;
          const escaped = [...row.children].filter(
            c => !own.test(String(c.className)) && c.tagName !== 'SCRIPT');
          return {
            viewport: window.innerWidth,
            content: w(document.querySelector('.md-content')),
            escaped: escaped.length,
            overflows: document.documentElement.scrollWidth > window.innerWidth + 1
          };
        }
        """
    )


@pytest.mark.parametrize("path", PAGES)
def test_content_column_survives_on_a_phone(pw_page, site_url, path):
    """Лишний </div> уводил контент из .md-content и сжимал колонку до 24px."""
    page = pw_page
    page.set_viewport_size(PHONE)
    page.goto(f"{site_url}{path}")
    result = measure(page)
    assert result["escaped"] == 0, f"{path}: контент вышел за .md-content"
    assert result["content"] > 300, (
        f"{path}: колонка схлопнулась до {result['content']}px"
    )
    assert not result["overflows"], f"{path}: появилась горизонтальная прокрутка"


def test_exam_question_is_readable_on_a_phone(pw_page, site_url):
    page = pw_page
    page.set_viewport_size(PHONE)
    page.goto(f"{site_url}/tools/exam/")
    page.click("#exam-start-btn")
    width = page.evaluate(
        "() => Math.round(document.getElementById('exam-question')"
        "  .getBoundingClientRect().width)"
    )
    # Узкая колонка переносила вопрос по одной букве в строку.
    assert width > 250, f"вопрос шириной {width}px — текст будет рваться по буквам"
    assert "Вопрос 1 из 20" in page.text_content("#exam-counter")
    assert "Очки" in page.text_content("#exam-score")
    assert page.locator(".exam-option").count() == 4


# ── Аудит 375px: каждый виджет во всех локалях ──────────────────────────────
# Половина аудитории заходит с телефона. Переполнение по ширине — не только
# «некрасиво»: страница ездит вбок, а часть результата уезжает за экран.
# Ловим его на каждой странице с виджетом в RU/EN/UZ (узбекские строки длиннее
# всех) до и после нажатия основных кнопок — многие виджеты рисуют таблицы
# результатов только после «Рассчитать»/«Начать».

NARROW = {"width": 375, "height": 812}
DOCS = Path(__file__).resolve().parent.parent / "_mkdocs"
GLOSSARY_PAGES = ["/practice/trading-sessions/", "/en/practice/news-trading-protocol/"]

# Кнопки, которые меняют данные или скачивают файлы, не жмём.
SKIP = (
    "reset|сброс|export|экспорт|import|импорт|download|скачать|share|подел|"
    "delete|удал|clear|очист|persist|anki|tozalash|o'chir|yukla|ulash"
)
CLICK_PRIMARY = """
(skip) => {
  const re = new RegExp(skip, 'i');
  const ok = b => !b.disabled && b.offsetParent && !re.test(b.id + ' ' + b.textContent);
  const buttons = [...document.querySelectorAll('.md-content button')].filter(ok);
  buttons.slice(0, 4).forEach(b => b.click());
}
"""
OVERFLOW = """
() => document.documentElement.scrollWidth - document.documentElement.clientWidth
"""


def widget_pages() -> list[str]:
    """URL страниц с виджетом: `widgets:` во front matter или inline-скрипт."""
    urls = []
    for page in sorted(DOCS.rglob("*.md")):
        if page.name.endswith((".en.md", ".uz.md")):
            continue
        text = page.read_text(encoding="utf-8")
        head = re.match(r"---\n(.*?)\n---\n", text, re.S)
        found = re.search(r"widgets:\s*\[([^\]]*)\]", head.group(1)) if head else None
        only_quiz = found and found.group(1).strip() == "chapter-quiz"
        if (found and not only_quiz) or "<script>" in text:
            rel = page.relative_to(DOCS).with_suffix("").as_posix()
            urls.append("/" if rel == "index" else f"/{rel}/")
    return urls


WIDGET_PAGES = widget_pages()


def test_audit_covers_all_tools():
    assert len(WIDGET_PAGES) >= 35, "разбор front matter сломался — аудит пустой"


@pytest.mark.parametrize("locale", ["", "/en", "/uz"], ids=["ru", "en", "uz"])
@pytest.mark.parametrize("path", WIDGET_PAGES)
def test_widget_page_fits_375px(pw_page, site_url, path, locale):
    page = pw_page
    page.on("dialog", lambda d: d.dismiss())
    page.set_viewport_size(NARROW)
    page.goto(f"{site_url}{locale}{path}")
    extra = page.evaluate(OVERFLOW)
    assert extra <= 1, f"{locale}{path}: шире экрана на {extra}px после загрузки"
    for _ in range(2):
        page.evaluate(CLICK_PRIMARY, SKIP)
        page.wait_for_timeout(150)
    extra = page.evaluate(OVERFLOW)
    assert extra <= 1, f"{locale}{path}: шире экрана на {extra}px после кнопок"


@pytest.mark.parametrize("path", GLOSSARY_PAGES)
def test_glossary_tooltip_stays_on_screen(pw_page, site_url, path):
    """Скрытые подсказки глоссария раздвигали главы до 450–485px на телефоне."""
    page = pw_page
    page.set_viewport_size(NARROW)
    page.goto(f"{site_url}{path}")
    assert page.evaluate(OVERFLOW) <= 1, f"{path}: горизонтальная прокрутка"
    page.locator(".fx-term").first.focus()
    tip = page.evaluate(
        """() => {
          const term = document.activeElement;
          const s = getComputedStyle(term, '::after');
          // Предок с transform/filter/backdrop-filter стал бы опорой для fixed,
          // и подсказка «прилипла» бы к нему, а не к низу экрана.
          const traps = [];
          for (let q = term.parentElement; q; q = q.parentElement) {
            const c = getComputedStyle(q);
            if (c.transform !== 'none' || c.filter !== 'none' ||
                (c.backdropFilter || 'none') !== 'none') traps.push(q.className);
          }
          return { display: s.display, position: s.position, traps };
        }"""
    )
    assert tip == {"display": "block", "position": "fixed", "traps": []}, tip
