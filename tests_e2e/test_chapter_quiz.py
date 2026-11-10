"""e2e мини-квизов в конце глав гайда.

Правильные ответы виджет перемешивает, поэтому тест читает банк из JSON-блока
страницы и ищет кнопку по тексту правильного варианта — как это сделал бы
человек, знающий материал.
"""

from __future__ import annotations

import json


def _bank(page):
    raw = page.locator("#chapter-quiz-questions").text_content()
    return json.loads(raw)


def _click_correct(page, question):
    correct = question["options"][question["answer"]]
    page.locator(".chapter-quiz__option", has_text=correct).first.click()


def _answer_all(page, bank, correctly: bool):
    for question in bank:
        if correctly:
            _click_correct(page, question)
        else:
            # Кликаем любой неверный вариант — берём первый, который не answer.
            wrong = next(
                o for j, o in enumerate(question["options"]) if j != question["answer"]
            )
            page.locator(".chapter-quiz__option", has_text=wrong).first.click()
        # «Дальше» после последнего вопроса тоже обязательно: вердикт
        # показывается именно этим кликом, а не выбором ответа.
        page.click("#cq-next")


def test_quiz_pass_marks_chapter_read_and_stores_result(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/docs/technical-analysis/")
    page.wait_for_selector("#cq-start-btn")
    bank = _bank(page)
    assert len(bank) == 3

    page.click("#cq-start-btn")
    _answer_all(page, bank, correctly=True)
    page.wait_for_selector(".chapter-quiz__verdict.is-pass")

    quiz = page.evaluate("() => JSON.parse(localStorage.getItem('fx-quiz-v1') || '{}')")
    record = quiz.get("technical-analysis")
    assert record, "результат квиза не записался в fx-quiz-v1"
    assert record["passed"] is True
    assert record["score"] == 3

    progress = page.evaluate(
        "() => JSON.parse(localStorage.getItem('fx-progress-v1') || '[]')"
    )
    assert any(p.endswith("/docs/technical-analysis/") for p in progress), (
        "сданная глава должна автоматически отмечаться прочитанной"
    )

    page.reload()
    page.wait_for_selector("#chapter-quiz .chapter-quiz__best--done")


def test_quiz_fail_does_not_mark_chapter_read(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/docs/strategy-details/")
    page.wait_for_selector("#cq-start-btn")
    bank = _bank(page)

    page.click("#cq-start-btn")
    _answer_all(page, bank, correctly=False)
    page.wait_for_selector(".chapter-quiz__verdict.is-fail")

    quiz = page.evaluate("() => JSON.parse(localStorage.getItem('fx-quiz-v1') || '{}')")
    record = quiz.get("strategy-details")
    assert record, "попытка должна записаться даже при провале"
    assert record["passed"] is False

    progress = page.evaluate(
        "() => JSON.parse(localStorage.getItem('fx-progress-v1') || '[]')"
    )
    assert not any("strategy-details" in p for p in progress)


def test_quiz_explanation_shown_after_answer(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/docs/order-types-mechanics/")
    page.wait_for_selector("#cq-start-btn")
    bank = _bank(page)

    page.click("#cq-start-btn")
    _click_correct(page, bank[0])
    explain = page.locator("#cq-explain")
    assert explain.is_visible()
    assert bank[0]["explain"].split()[0] in explain.text_content()
    # После ответа все варианты блокируются — второй клик ничего не меняет.
    assert page.locator(".chapter-quiz__option[disabled]").count() == 4


def test_quiz_renders_in_all_locales(pw_page, site_url):
    page = pw_page
    for prefix, needle in (
        ("", "Проверь себя"),
        ("en/", "Check yourself"),
        ("uz/", "O'zingni sinash"),
    ):
        page.goto(f"{site_url}/{prefix}docs/real-analysis/")
        page.wait_for_selector("#cq-start-btn")
        assert needle in page.text_content("#chapter-quiz")


def test_dashboard_counts_passed_quizzes(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/docs/real-analysis/")
    page.wait_for_selector("#cq-start-btn")
    bank = _bank(page)
    page.click("#cq-start-btn")
    _answer_all(page, bank, correctly=True)
    page.wait_for_selector(".chapter-quiz__verdict.is-pass")

    page.goto(f"{site_url}/extras/dashboard/")
    page.wait_for_selector("#student-dashboard .sd-hero")
    values = page.locator(".sd-card__value").all_text_contents()
    assert any(v.strip().startswith("1 / 6") for v in values), (
        f"карточка квизов не показала 1 / 6: {values}"
    )
