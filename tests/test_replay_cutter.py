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
