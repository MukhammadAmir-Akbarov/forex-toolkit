"""forex-toolkit — образовательный набор для forex-трейдинга.

Не финансовый совет. Только для обучения.
"""

from __future__ import annotations

__version__ = "0.1.0"

# Re-export ключевых функций
from forex_toolkit.position_calculator import calculate_position, PositionResult
from forex_toolkit.indicators import ema, sma, rsi, atr, bollinger, macd
from forex_toolkit.candles import (
    is_hammer,
    is_shooting_star,
    is_bullish_engulfing,
    is_bearish_engulfing,
    is_doji,
)

__all__ = [
    "__version__",
    "calculate_position",
    "PositionResult",
    "ema",
    "sma",
    "rsi",
    "atr",
    "bollinger",
    "macd",
    "is_hammer",
    "is_shooting_star",
    "is_bullish_engulfing",
    "is_bearish_engulfing",
    "is_doji",
]
