"""e2e для теста готовности и проверки брокера — двух портированных CLI-инструментов."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from broker_check import REGULATORS

from forex_toolkit.risk_profile import score_profile

ROOT = Path(__file__).resolve().parent.parent
BLOCK = re.compile(
    r'<script type="application/json" id="risk-profile-questions">\s*(.*?)\s*</script>',
    re.DOTALL,
)


def questions(locale: str = "") -> list[dict]:
    name = "risk-profile.md" if not locale else f"risk-profile.{locale}.md"
    text = (ROOT / "_mkdocs" / "tools" / name).read_text(encoding="utf-8")
    return json.loads(BLOCK.search(text).group(1))


def answer_all(page, picker) -> dict:
    """Проходит тест целиком, выбирая вариант через picker(points) -> index."""
    page.click("#rp-start")
    data = questions()
    for question in data:
        points = [option["points"] for option in question["options"]]
        page.locator('input[name="rp-answer"]').nth(picker(points)).click()
    return page.evaluate("() => window.__fxRiskProfile")


# Стратегии ответов. Лямбды держим здесь, а не в parametrize: hooks/project_stats.py
# разворачивает только литеральные списки, иначе счётчик тестов на главной врёт.
PICKERS = {
    "best": lambda points: points.index(max(points)),
    "worst": lambda points: points.index(min(points)),
    "second": lambda points: min(1, len(points) - 1),
}


@pytest.mark.parametrize("strategy", ["best", "worst", "second"])
def test_readiness_score_matches_python(pw_page, site_url, strategy):
    """Вердикт «стоит ли торговать» обязан совпадать в браузере и в пакете."""
    picker = PICKERS[strategy]
    page = pw_page
    page.goto(f"{site_url}/tools/risk-profile/")
    actual = answer_all(page, picker)

    data = questions()
    answers = [picker([o["points"] for o in q["options"]]) for q in data]
    expected = score_profile(data, answers)

    assert actual["total"] == expected["total"]
    assert actual["max_score"] == expected["max_score"]
    assert actual["percent"] == pytest.approx(expected["percent"])
    assert actual["band"] == expected["band"]
    assert actual["weak_categories"] == expected["weak_categories"]


def test_readiness_result_survives_reload_as_previous_attempt(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/tools/risk-profile/")
    answer_all(page, lambda points: points.index(max(points)))
    page.reload()
    assert "100.0%" in page.locator(".risk-profile__previous").inner_text()


@pytest.mark.parametrize("prefix", ["", "en/", "uz/"])
def test_readiness_test_is_reachable_in_every_locale(pw_page, site_url, prefix):
    page = pw_page
    page.goto(f"{site_url}/{prefix}tools/risk-profile/")
    assert page.locator("#rp-start").is_visible()


def test_broker_check_builds_official_registry_links(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/tools/broker-check/")
    page.fill("#bc-name", "IC Markets")
    page.click("#bc-check")
    result = page.locator("#bc-result")
    result.wait_for(state="visible")

    links = result.locator(".broker-check__registries a")
    assert links.count() == len(REGULATORS)
    hrefs = [links.nth(i).get_attribute("href") for i in range(links.count())]
    assert any("register.fca.org.uk" in href for href in hrefs)
    assert all("IC%20Markets" in href or "finma.ch" in href for href in hrefs)
    # Известный брокер: показываем исторические номера лицензий.
    assert "335692" in result.inner_text()


def test_broker_check_escalates_with_red_flags(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/tools/broker-check/")
    page.fill("#bc-name", "Unknown Broker LLC")
    page.click("#bc-check")
    result = page.locator("#bc-result")
    result.wait_for(state="visible")
    assert "справочнике" in result.inner_text()

    verdict = page.locator("#bc-verdict")
    assert "Явных красных флагов нет" in verdict.inner_text()
    flags = page.locator(".bc-flag")
    for index in range(3):
        flags.nth(index).check()
    assert "схему по отъёму денег" in verdict.inner_text()
    assert "is-warning" in (result.get_attribute("class") or "")


# ── Исламский счёт в проверке брокера ──────────────────────────────────────
# Для значительной части аудитории «есть ли своп-фри» — первый вопрос, а не
# последний. Списка брокеров со своп-фри мы сознательно не храним: условия
# меняются молча, и устаревшее «да, есть» опаснее отсутствия ответа.


@pytest.mark.parametrize("prefix", ["", "en/", "uz/"])
def test_swap_free_checklist_is_opt_in_and_translated(pw_page, site_url, prefix):
    page = pw_page
    page.goto(f"{site_url}/{prefix}tools/broker-check/")
    page.fill("#bc-name", "IC Markets")
    page.click("#bc-check")
    page.wait_for_selector("#bc-swap-need")

    # По умолчанию свёрнут: тем, кому своп-фри не нужен, он только мешает.
    assert page.evaluate("() => document.getElementById('bc-swap-body').hidden")

    page.check("#bc-swap-need")
    assert not page.evaluate("() => document.getElementById('bc-swap-body').hidden")

    items = page.locator(".bc-swap-item")
    assert items.count() == 5, f"[{prefix}] ожидали 5 пунктов чек-листа"

    items.first.check()
    partial = page.text_content("#bc-swap-verdict")
    assert partial.strip() and "undefined" not in partial, f"[{prefix}] {partial!r}"

    for index in range(1, items.count()):
        items.nth(index).check()
    done = page.text_content("#bc-swap-verdict")
    assert done != partial, f"[{prefix}] вердикт не изменился после всех пунктов"
    assert "undefined" not in done


def test_swap_free_block_never_claims_a_broker_offers_it(pw_page, site_url):
    """Виджет не должен утверждать, что у брокера есть исламский счёт.

    Такие условия меняются без объявления; устаревшее «да, есть» хуже, чем
    честное «проверь сам».
    """
    page = pw_page
    page.goto(f"{site_url}/tools/broker-check/")
    page.fill("#bc-name", "IC Markets")
    page.click("#bc-check")
    page.wait_for_selector("#bc-swap-need")
    page.check("#bc-swap-need")

    text = page.text_content("#bc-swap-body").lower()
    for claim in ("предлагает своп-фри", "есть своп-фри", "доступен своп-фри"):
        assert claim not in text, f"виджет утверждает про брокера: {claim!r}"
    # Зато обязан сказать, что своп-фри — это перераспределение издержек.
    assert "спред" in text and "не значит" in text
