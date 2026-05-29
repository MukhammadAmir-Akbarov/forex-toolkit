"""forex_toolkit.fx_math — единый источник правды для финансовой математики.

Сюда вынесены формулы, которые раньше дублировались в нескольких местах
(``tools/pip_calculator.py``, ``tools/position_calculator.py``,
``tools/multi_position_sizer.py`` и в самом пакете). Любой калькулятор должен
импортировать формулы отсюда, а не переписывать их заново — так значения не
разъедутся между инструментами.

Никаких внешних зависимостей — только стандартная библиотека.
"""

from __future__ import annotations

import math

__all__ = [
    "PIP_VALUE_USD_PER_LOT",
    "LIVE_SENSITIVE_PAIRS",
    "STANDARD_LOT_UNITS",
    "MIN_LOT",
    "normalize_pair",
    "pip_size",
    "pip_value_in_quote",
    "pip_value_in_account_currency",
    "calc_lots",
]

# Один стандартный лот = 100 000 единиц базовой валюты.
STANDARD_LOT_UNITS = 100_000

# Минимальный шаг лота у большинства брокеров.
MIN_LOT = 0.01

# Приблизительная стоимость 1 пипса на 1 стандартный лот (100 000 единиц)
# при счёте в USD. Для пар, где USD стоит первым, и для кросс-пар реальная
# стоимость зависит от текущего курса — см. LIVE_SENSITIVE_PAIRS и опцию
# ``--live`` в position_calculator. Значения ниже — снимок на момент создания.
PIP_VALUE_USD_PER_LOT: dict[str, float] = {
    "EURUSD": 10.00,
    "GBPUSD": 10.00,
    "AUDUSD": 10.00,
    "NZDUSD": 10.00,
    "USDJPY": 6.70,  # зависит от курса USD/JPY (~150)
    "USDCHF": 11.30,  # зависит от курса USD/CHF (~0.88)
    "USDCAD": 7.30,  # зависит от курса USD/CAD (~1.37)
    "EURJPY": 6.70,
    "GBPJPY": 6.70,
    "EURGBP": 12.70,
}

# Пары, у которых стоимость пипса в USD напрямую зависит от текущей котировки
# (всё, где USD — base, и все кросс-пары). Для них рекомендуется ``--live``.
LIVE_SENSITIVE_PAIRS: set[str] = {
    "USDJPY",
    "USDCHF",
    "USDCAD",
    "EURJPY",
    "GBPJPY",
    "EURGBP",
}


def normalize_pair(pair: str) -> str:
    """Приводит пару к виду ``EURUSD`` из ``eur/usd``, ``EUR-USD`` и т.п."""
    return pair.upper().replace("/", "").replace("-", "")


def pip_size(pair: str) -> float:
    """Размер пипса: 0.01 для пар с JPY, иначе 0.0001."""
    return 0.01 if "JPY" in normalize_pair(pair) else 0.0001


def pip_value_in_quote(lots: float, pair: str) -> float:
    """Стоимость 1 пипса в КОТИРУЕМОЙ валюте (USD для EUR/USD)."""
    return lots * STANDARD_LOT_UNITS * pip_size(pair)


def pip_value_in_account_currency(
    lots: float,
    pair: str,
    account_ccy: str,
    current_price: float,
) -> float:
    """Стоимость пипса в валюте счёта.

    Args:
        lots: размер позиции в лотах
        pair: торгуемая пара (например, ``EURUSD``, ``USDJPY``)
        account_ccy: валюта счёта (``USD``, ``EUR``, ...)
        current_price: текущая цена торгуемой пары

    Raises:
        ValueError: если нужна кросс-конвертация, для которой не хватает курса.
    """
    pair = normalize_pair(pair)
    account_ccy = account_ccy.upper()
    base, quote = pair[:3], pair[3:]

    pip_in_quote = pip_value_in_quote(lots, pair)

    if account_ccy == quote:
        return pip_in_quote
    if account_ccy == base:
        return pip_in_quote / current_price

    raise ValueError(
        f"Кросс-конвертация {quote}→{account_ccy} требует доп. курс. "
        f"Используй точный расчёт через терминал брокера."
    )


def calc_lots(risk_usd: float, stop_pips: float, pip_value: float) -> float:
    """Размер позиции в лотах, округлённый ВНИЗ до шага 0.01.

    Округление вниз гарантирует, что реальный риск не превысит плановый.
    Возвращает 0.0 при некорректных входных данных (стоп или стоимость пипса ≤ 0).
    """
    if stop_pips <= 0 or pip_value <= 0:
        return 0.0
    raw = risk_usd / (stop_pips * pip_value)
    return math.floor(raw * 100 + 1e-9) / 100
