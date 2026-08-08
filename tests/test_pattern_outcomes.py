"""Свечные паттерны и их исход в архиве.

Смысл этих тестов — не «распознавание работает», а «число, которое мы покажем
студенту, честное». Поэтому здесь проверяется в том числе то, что расчёт
**не** приписывает фигуре успех: ничейный исход не идёт ни в чей актив, доджи
ничего не обещает, а короткий ряд свечей не даёт исхода вовсе.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from forex_toolkit.pattern_outcomes import (
    MIN_MATCHES,
    PATTERNS,
    collect_stats,
    decode_episode,
    find_patterns,
    outcome_after,
)

EPISODES = (
    Path(__file__).resolve().parent.parent / "_mkdocs" / "data" / "replay-episodes.json"
)


def candle(o, h, low, c):
    return {"open": o, "high": h, "low": low, "close": c}


def flat_series(n, price=1.1000):
    """Ряд одинаковых свечей — ничего не находится и никуда не идёт."""
    return [candle(price, price + 0.0001, price - 0.0001, price) for _ in range(n)]


def test_hammer_is_found_at_its_own_index():
    series = flat_series(3)
    # Длинная нижняя тень, маленькое тело сверху.
    series[1] = candle(1.1000, 1.1006, 1.0980, 1.1005)
    matches = [m for m in find_patterns(series) if m.key == "hammer"]

    assert [m.index for m in matches] == [1]


def test_engulfing_needs_the_previous_candle():
    series = [
        candle(1.1010, 1.1012, 1.0995, 1.1000),  # медвежья
        candle(1.0998, 1.1020, 1.0997, 1.1015),  # поглощающая бычья
    ]
    keys = {m.key for m in find_patterns(series)}

    assert "bullish_engulfing" in keys


def test_first_candle_cannot_form_a_two_candle_pattern():
    """Индекс 0 не с чем сравнивать — поглощения там быть не может."""
    series = [candle(1.0998, 1.1020, 1.0997, 1.1015)]

    keys = {m.key for m in find_patterns(series)}
    assert "bullish_engulfing" not in keys and "bearish_engulfing" not in keys


def test_outcome_reads_the_close_after_the_horizon():
    series = flat_series(10)
    series[7] = candle(1.1000, 1.1100, 1.0900, 1.1050)

    assert outcome_after(series, 2, horizon=5) == "up"
    assert outcome_after(series, 3, horizon=5) in ("down", "flat")


def test_outcome_is_empty_when_the_future_is_missing():
    """Без будущих свечей исход неизвестен — и это не 'flat'."""
    assert outcome_after(flat_series(4), 2, horizon=5) == ""


def test_flat_outcome_is_not_counted_as_success():
    """Ничья не должна улучшать статистику паттерна."""
    # Ряд стоит ровно на цене закрытия молота — тогда через 5 свечей исход
    # действительно ничья, а не «вниз» из-за разницы уровней.
    series = flat_series(12, price=1.1005)
    series[3] = candle(1.1000, 1.1006, 1.0980, 1.1005)

    stats = collect_stats([series])["hammer"]

    assert stats.found >= 1
    assert stats.worked == 0
    assert stats.flat >= 1
    # Доля считается только среди тех, где движение было.
    assert stats.rate == 0.0


def test_doji_promises_nothing_so_it_never_counts_as_worked():
    series = flat_series(20)
    stats = collect_stats([series])["doji"]

    assert PATTERNS["doji"][1] == "none"
    assert stats.worked == 0


def test_rate_ignores_ties_rather_than_diluting_with_them():
    """Доля = отработавшие ÷ (найденные − ничьи), а не ÷ найденные."""
    from forex_toolkit.pattern_outcomes import PatternStats

    stats = PatternStats(key="hammer", found=10, worked=3, flat=4)

    assert stats.rate == pytest.approx(3 / 6)


def test_no_matches_gives_zero_rate_without_dividing_by_zero():
    from forex_toolkit.pattern_outcomes import PatternStats

    assert PatternStats(key="hammer", found=0, worked=0, flat=0).rate == 0.0


def test_decode_episode_restores_prices_from_pip_offsets():
    episode = {"base": 1.1000, "pip": 0.0001, "k": [[0, 10, -10, 5]]}

    got = decode_episode(episode)[0]

    assert got["open"] == pytest.approx(1.1000)
    assert got["high"] == pytest.approx(1.1010)
    assert got["low"] == pytest.approx(1.0990)
    assert got["close"] == pytest.approx(1.1005)


def test_every_pattern_declares_what_it_promises():
    for key, (length, promise) in PATTERNS.items():
        assert length in (1, 2), key
        assert promise in ("up", "down", "none"), key


def test_archive_gives_enough_matches_to_show_a_number():
    """Если находок мало, показывать долю нельзя — проверяем, что их хватает."""
    document = json.loads(EPISODES.read_text(encoding="utf-8"))
    series = [decode_episode(episode) for episode in document["episodes"]]

    stats = collect_stats(series)

    directional = [key for key, (_, promise) in PATTERNS.items() if promise != "none"]
    for key in directional:
        assert stats[key].found >= MIN_MATCHES, (
            f"{key}: найдено {stats[key].found} — мало, чтобы показывать долю"
        )


def test_the_archive_does_not_flatter_the_patterns():
    """Ключевой урок: доли болтаются около половины, а не подтверждают фигуры.

    Тест сторожит именно это. Если однажды доля улетит к 90%, скорее всего
    сломался расчёт исхода, а не рынок стал предсказуемым.
    """
    document = json.loads(EPISODES.read_text(encoding="utf-8"))
    series = [decode_episode(episode) for episode in document["episodes"]]

    stats = collect_stats(series)
    for key, (_, promise) in PATTERNS.items():
        if promise == "none" or stats[key].found < MIN_MATCHES:
            continue
        assert 0.2 <= stats[key].rate <= 0.8, (
            f"{key}: доля {stats[key].rate:.1%} — подозрительно далеко от половины, "
            "проверь расчёт исхода"
        )
