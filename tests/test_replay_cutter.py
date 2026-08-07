from __future__ import annotations

import replay_cutter


def candles(count: int = 12) -> list[dict]:
    return [
        {
            "t": f"2026-01-{index + 1:02d} 10:00",
            "o": 150.00 + index * 0.01,
            "h": 150.03 + index * 0.01,
            "l": 149.98 + index * 0.01,
            "c": 150.01 + index * 0.01,
        }
        for index in range(count)
    ]


def test_pip_size_supports_jpy_pairs():
    assert replay_cutter.pip_size("EURUSD") == 0.0001
    assert replay_cutter.pip_size("USDJPY") == 0.01


def market(count: int) -> list[dict]:
    """Длинный архив: тренд вверх, затем боковик, затем тренд вниз."""
    rows = []
    for index in range(count):
        third = count // 3
        if index < third:
            level = 1.1000 + index * 0.0002
        elif index < 2 * third:
            level = 1.1000 + third * 0.0002
        else:
            level = 1.1000 + third * 0.0002 - (index - 2 * third) * 0.0002
        rows.append(
            {
                "t": f"2026-01-01 {index:04d}",
                "o": level,
                "h": level + 0.0005,
                "l": level - 0.0005,
                "c": level + 0.0001,
            }
        )
    return rows


def test_cut_episodes_spans_the_whole_archive():
    """Регрессия: все эпизоды приходились на начало файла.

    Шаг выборки был фиксированным (30 свечей), а сбор кандидатов обрывался
    после 2×n штук. На часовом архиве в 12 000 свечей это давало десять
    эпизодов из первого месяца — один и тот же режим рынка вместо истории.
    """
    candles = market(3000)
    episodes = replay_cutter.cut_episodes(
        candles, n_episodes=10, context=30, outcome=15
    )

    assert len(episodes) == 10
    starts = [ep["start"] for ep in episodes]
    # Последний эпизод должен приходиться на дальнюю половину архива.
    assert max(starts) > len(candles) // 2, f"выборка осталась в начале: {starts}"


def test_cut_episodes_does_not_overlap_windows():
    """Соседние эпизоды не должны показывать одни и те же свечи."""
    episodes = replay_cutter.cut_episodes(
        market(3000), n_episodes=10, context=30, outcome=15
    )
    starts = sorted(ep["start"] for ep in episodes)
    for earlier, later in zip(starts, starts[1:]):
        assert later - earlier >= 45, f"окна пересекаются: {earlier} и {later}"


def test_cut_episodes_mixes_market_character():
    """В наборе должен быть не только боковик: спокойных участков всегда больше."""
    episodes = replay_cutter.cut_episodes(
        market(3000), n_episodes=9, context=30, outcome=15
    )
    categories = {ep["category"] for ep in episodes}
    assert len(categories) >= 2, f"весь набор одной категории: {categories}"


def test_encode_episode_includes_market_metadata():
    source = {
        "id": 3,
        "category": "uptrend",
        "atr_pips": 7.5,
        "entry": 150.11,
        "context": candles(4),
        "future": candles(2),
    }

    encoded = replay_cutter.encode_episode(source, "USDJPY", "1h")

    assert encoded["id"] == "USDJPY-1h-3"
    assert encoded["pair"] == "USDJPY"
    assert encoded["tf"] == "H1"
    assert encoded["pip"] == 0.01
    assert encoded["ctx"] == 4
    assert len(encoded["k"]) == 6
