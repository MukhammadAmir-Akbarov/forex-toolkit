"""Раскладка на телефонной ширине: контент не должен схлопываться."""

from __future__ import annotations

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
