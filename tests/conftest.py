"""Pytest fixtures и общая настройка для всех тестов."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent

# Делаем все модули проекта импортируемыми
for sub in ("", "tools", "bot", "strategies", "advanced", "journal"):
    p = ROOT / sub if sub else ROOT
    sys.path.insert(0, str(p))


@pytest.fixture
def synthetic_ohlc():
    """Синтетический OHLC ряд для тестов стратегий и бэктестера."""
    rng = np.random.default_rng(42)
    n = 500
    times = pd.date_range("2025-01-01", periods=n, freq="h")
    closes = [1.08]
    for i in range(n - 1):
        drift = 0.0001 if i < n // 2 else -0.00005
        closes.append(closes[-1] + rng.normal(drift, 0.001))
    closes = np.array(closes)
    opens = np.concatenate([[closes[0]], closes[:-1]])
    highs = np.maximum(opens, closes) + rng.uniform(0.0001, 0.001, n)
    lows = np.minimum(opens, closes) - rng.uniform(0.0001, 0.001, n)
    return pd.DataFrame(
        {
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
        },
        index=times,
    )


@pytest.fixture
def trending_up_ohlc():
    """Чистый восходящий тренд — для тестов trend-following стратегий."""
    n = 300
    times = pd.date_range("2025-01-01", periods=n, freq="h")
    closes = np.linspace(1.08, 1.12, n)
    # Лёгкий шум
    rng = np.random.default_rng(7)
    closes = closes + rng.normal(0, 0.0005, n)
    opens = np.concatenate([[closes[0]], closes[:-1]])
    highs = np.maximum(opens, closes) + 0.0005
    lows = np.minimum(opens, closes) - 0.0005
    return pd.DataFrame(
        {
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
        },
        index=times,
    )


@pytest.fixture
def flat_ohlc():
    """Боковик / флэт — для тестов mean-reversion стратегий."""
    n = 300
    times = pd.date_range("2025-01-01", periods=n, freq="h")
    rng = np.random.default_rng(3)
    # Колебания вокруг 1.08 ± 0.003
    closes = 1.08 + np.sin(np.arange(n) / 10) * 0.003 + rng.normal(0, 0.0003, n)
    opens = np.concatenate([[closes[0]], closes[:-1]])
    highs = np.maximum(opens, closes) + 0.0005
    lows = np.minimum(opens, closes) - 0.0005
    return pd.DataFrame(
        {
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
        },
        index=times,
    )
