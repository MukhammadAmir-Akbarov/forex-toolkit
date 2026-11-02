"""Режим Replay «на время» — свечи идут сами, решение — в темпе.

Смысл режима: на реальном рынке решение даётся за секунды, а тренажёр без
таймера ждёт кликов бесконечно. Тесты гоняют таймер через playwright clock,
поэтому прогон мгновенный, а проверяемые утверждения — поведенческие:

* будущие свечи двигаются без участия пользователя;
* первое валидное решение фиксируется само (передумать нельзя);
* не решился до конца эпизода — это пропуск, а не «подожди ещё».
"""

from __future__ import annotations

import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "_mkdocs" / "data"


def _future_candles() -> int:
    """Сколько свечей идёт после контекста — столько тиков до таймаута."""
    document = json.loads((DATA / "replay-episodes.json").read_text(encoding="utf-8"))
    episode = document["episodes"][0]
    return len(episode["k"]) - episode["ctx"]


def _open_timed(page, site_url):
    page.clock.install()
    page.goto(f"{site_url}/tools/replay-trainer/")
    page.wait_for_selector("#rp-timed")
    page.check("#rp-timed")


def test_timed_mode_advances_candles_by_itself(site_url, pw_page):
    page = pw_page
    _open_timed(page, site_url)

    assert page.locator("#rp-timerline").inner_text() == ""
    page.clock.run_for(2100)
    assert "⏱" in page.locator("#rp-timerline").inner_text(), (
        "таймер включён, но строка темпа не появилась — свечи не идут сами"
    )


def test_timed_mode_locks_the_first_valid_decision(site_url, pw_page):
    page = pw_page
    _open_timed(page, site_url)

    page.select_option("#rp-pair", "USDJPY")
    page.select_option("#rp-tf", "D1")
    page.click("#rp-buy")
    canvas = page.locator("#replay-canvas")
    box = canvas.bounding_box()
    assert box is not None
    x = box["width"] * 0.55
    canvas.click(position={"x": x, "y": box["height"] * 0.50})
    canvas.click(position={"x": x, "y": box["height"] * 0.72})
    canvas.click(position={"x": x, "y": box["height"] * 0.25})

    # Кнопку «Запустить» никто не нажимал: тик таймера обязан зафиксировать
    # валидное решение сам и запустить доигровку (80 мс/свеча).
    page.clock.run_for(2100)
    page.clock.run_for(60_000)
    assert page.locator("#rp-result").is_visible(), (
        "валидные уровни в режиме «на время» не привели к сделке"
    )


def test_timed_mode_counts_timeout_as_a_skip(site_url, pw_page):
    page = pw_page
    _open_timed(page, site_url)

    # Ничего не делаем: эпизод обязан кончиться пропуском, а не ждать вечно.
    page.clock.run_for((_future_candles() + 1) * 2100)

    result = page.locator("#rp-result")
    assert result.is_visible()
    assert "пропуск" in result.inner_text().lower()
    # Таймер остановлен: строка темпа пуста, кнопка «Следующий эпизод» ждёт.
    assert page.locator("#rp-timerline").inner_text() == ""
    assert page.locator("#rp-next").is_visible()
