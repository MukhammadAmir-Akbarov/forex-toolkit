"""e2e итогового экзамена: вердикт → ссылки на главы с несданными квизами.

Как и в квизах глав, правильный ответ ищется по тексту из JSON-банка
страницы — виджет перемешивает и вопросы, и варианты.
"""

from __future__ import annotations

import json

CHAPTER_KEYS = [
    "technical-analysis",
    "strategy-details",
    "real-analysis",
    "order-types-mechanics",
    "fundamental-analysis-guide",
    "broker-mechanics-101",
    "crypto-trading-guide",
    "order-flow-volume-profile",
    "stocks-basics",
    "breakeven-protocol",
    "cycle-theory",
    "gold-trading",
    "lot-discipline",
    "market-structure",
    "news-trading-protocol",
    "scaling-in",
    "trading-sessions",
]


def _bank(page):
    raw = page.locator("#exam-questions").text_content()
    return json.loads(raw)


def _answer_current(page, bank, correctly: bool):
    """Отвечает на показанный вопрос и жмёт «Дальше»."""
    text = page.locator("#exam-question").text_content()
    item = next(q for q in bank if q["q"] == text)
    correct = item["options"][item["answer"]]
    options = page.locator(".exam-option").all_text_contents()
    target = correct if correctly else next(o for o in options if o != correct)
    page.locator(".exam-option", has_text=target).first.click()
    page.click("#exam-next")


def _run_exam(page, site_url, correctly: bool):
    page.goto(f"{site_url}/tools/exam/")
    page.wait_for_selector("#exam-start-btn")
    bank = _bank(page)
    page.click("#exam-start-btn")
    drawn = min(20, len(bank))
    for _ in range(drawn):
        _answer_current(page, bank, correctly)
    page.wait_for_selector("#exam-result .calc-result")


def test_exam_fail_lists_unpassed_chapter_links(pw_page, site_url):
    page = pw_page
    _run_exam(page, site_url, correctly=False)
    links = page.locator("#exam-result .exam-chapters a")
    assert links.count() == len(CHAPTER_KEYS), (
        "при пустом fx-quiz-v1 должны показаться все главы"
    )
    hrefs = links.evaluate_all("(els) => els.map((e) => e.getAttribute('href'))")
    assert "../../docs/technical-analysis/" in hrefs
    assert "../../growth/crypto-trading-guide/" in hrefs


def test_exam_result_hides_links_when_all_quizzes_passed(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/tools/exam/")
    passed = {k: {"score": 3, "total": 3, "passed": True} for k in CHAPTER_KEYS}
    page.evaluate(
        "(data) => localStorage.setItem('fx-quiz-v1', JSON.stringify(data))",
        passed,
    )
    page.reload()
    page.wait_for_selector("#exam-start-btn")
    bank = _bank(page)
    page.click("#exam-start-btn")
    for _ in range(min(20, len(bank))):
        _answer_current(page, bank, correctly=False)
    page.wait_for_selector("#exam-result .calc-result")
    assert page.locator("#exam-result .exam-chapters").count() == 0


def test_exam_fail_shows_explanation_for_every_missed(pw_page, site_url):
    """Разбор промахов с объяснениями: экзамен учит, а не просто оценивает."""
    page = pw_page
    _run_exam(page, site_url, correctly=False)
    whys = page.locator("#exam-result .exam-missed__why")
    assert whys.count() == 20, "у каждого пропущенного вопроса должно быть объяснение"
    assert whys.first.inner_text().strip()
