"""Ведение открытой позиции — в настоящем браузере.

Тренажёр обязан оставаться тренажёром, а не рекламой управления позицией.
Поэтому проверяется не только «что-то показалось», но и три вещи по существу:

* итог по этой сделке идёт рядом с итогом «просто держать» — иначе сравнивать
  не с чем и любой план выглядит полезным;
* сводка считается по всем сделкам архива, а не по одной попавшейся;
* правило подсчёта (стоп внутри свечи важнее цели) написано на экране.
"""

from __future__ import annotations

import pytest

LOCALES = ["", "en/", "uz/"]
PLANS = ["hold", "be", "partial", "trail"]


def _open(page, site_url, prefix):
    page.goto(f"{site_url}/{prefix}tools/position-management/")
    page.wait_for_selector(".pm-plans, .calc-error", timeout=30_000)


@pytest.mark.parametrize("prefix", LOCALES, ids=["ru", "en", "uz"])
def test_widget_gets_its_data(pw_page, site_url, prefix):
    page = pw_page
    _open(page, site_url, prefix)

    assert page.locator(".calc-error").count() == 0, (
        f"[{prefix or 'ru'}] эпизоды не загрузились: {page.text_content('.calc-error')}"
    )
    assert page.locator(".pm-plan").count() == len(PLANS)


@pytest.mark.parametrize("plan", PLANS)
def test_every_plan_reports_both_numbers(pw_page, site_url, plan):
    """Свой результат и «просто держать» — всегда рядом."""
    page = pw_page
    _open(page, site_url, "")

    page.locator(f'.pm-plan[data-key="{plan}"]').click()
    page.wait_for_selector("#pm-verdict h4")

    verdict = page.text_content("#pm-verdict")
    assert "R" in verdict
    assert page.locator(".pm-overall").count() == 1, "нет свода по всем сделкам"
    assert page.locator(".pm-lesson").count() == 1
    # Правило подсчёта обязано быть на экране: без него числа выглядят точнее,
    # чем они есть.
    assert page.locator(".pm-note").count() == 1, "нет правила подсчёта"


def test_the_verdict_counts_the_whole_archive(pw_page, site_url):
    page = pw_page
    _open(page, site_url, "")

    page.locator('.pm-plan[data-key="be"]').click()
    page.wait_for_selector(".pm-overall")

    overall = page.text_content(".pm-overall")
    # 80 эпизодов в обе стороны — сводка обязана быть по 160 сделкам, а не по
    # одной показанной.
    assert "160" in overall, overall


def test_browser_matches_python_on_the_whole_archive(pw_page, site_url):
    """Числа страницы обязаны совпасть с пакетом на тех же эпизодах."""
    import json
    from pathlib import Path

    from forex_toolkit.position_management import Plan, compare, summarize

    page = pw_page
    _open(page, site_url, "")

    root = Path(__file__).resolve().parent.parent
    document = json.loads(
        (root / "_mkdocs" / "data" / "replay-episodes.json").read_text(encoding="utf-8")
    )

    rows = []
    for episode in document["episodes"]:
        base, pip = episode["base"], episode["pip"]
        candles = [
            {
                "open": base + c[0] * pip,
                "high": base + c[1] * pip,
                "low": base + c[2] * pip,
                "close": base + c[3] * pip,
            }
            for c in episode["k"]
        ]
        risk = episode["atr"] * pip
        entry = candles[29]["close"]
        for side in ("long", "short"):
            stop = entry - risk if side == "long" else entry + risk
            take = entry + 2 * risk if side == "long" else entry - 2 * risk
            got = compare(
                candles,
                entry_index=29,
                entry=entry,
                stop=stop,
                take=take,
                direction=side,
                plan=Plan(breakeven_at=1.0),
            )
            if got:
                rows.append(got)
    expected = summarize(rows)

    page.locator('.pm-plan[data-key="be"]').click()
    page.wait_for_selector(".pm-overall")
    shown = page.text_content(".pm-overall")

    assert str(expected.trades) in shown
    assert f"{expected.managed_total:+.2f}R" in shown, (
        f"на экране {shown!r}, пакет даёт {expected.managed_total:+.2f}R"
    )
    assert f"{expected.plain_total:+.2f}R" in shown


def test_you_can_take_another_trade(pw_page, site_url):
    page = pw_page
    _open(page, site_url, "")

    page.locator(".pm-plan").first.click()
    page.wait_for_selector("#pm-next")
    page.click("#pm-next")
    page.wait_for_selector(".pm-plans")
    assert page.locator(".pm-plan").count() == len(PLANS)
