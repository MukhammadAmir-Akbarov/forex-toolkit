#!/usr/bin/env python3
"""
Калькулятор размера позиции для forex.

Считает размер позиции (в лотах) на основе:
  - размера депозита,
  - процента риска на сделку,
  - расстояния до стоп-лосса в пипсах,
  - валютной пары.

Использование:
  Интерактивный режим:
    python position_calculator.py

  Однострочно:
    python position_calculator.py --balance 1000 --risk 0.5 --stop 25 --pair EURUSD

Никаких внешних зависимостей — только стандартная библиотека Python 3.

Disclaimer: учебный калькулятор. Точные котировки и стоимость пипса
лучше брать из терминала твоего брокера.
"""

from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass


# Стоимость пипса и список «чувствительных к курсу» пар живут в одном месте —
# forex_toolkit.fx_math (фолбэк на sys.path — чтобы скрипт работал и без установки).
try:
    from forex_toolkit.fx_math import (
        LIVE_SENSITIVE_PAIRS as _LIVE_SENSITIVE_PAIRS,
        PIP_VALUE_USD_PER_LOT,
    )
except ModuleNotFoundError:  # запуск скрипта без установки пакета
    from pathlib import Path as _Path

    sys.path.insert(0, str(_Path(__file__).resolve().parent.parent))
    from forex_toolkit.fx_math import (
        LIVE_SENSITIVE_PAIRS as _LIVE_SENSITIVE_PAIRS,
        PIP_VALUE_USD_PER_LOT,
    )


def _live_pip_value(pair: str) -> float | None:
    """
    Получить актуальную стоимость 1 пипса (в USD) для 1 стандартного лота
    через yfinance. Возвращает None, если yfinance недоступен или не удалось
    скачать котировку.

    Формула:
      pip_size = 0.01 для JPY-пар, 0.0001 для остальных
      lot     = 100_000 единиц base-валюты

      Если quote = USD                → pip_value = pip_size * lot
      Если base  = USD (USDJPY/CHF/…) → pip_value = pip_size * lot / quote_rate
      Если кросс (EURJPY, EURGBP, …)  → берём котировку base/USD
                                         pip_value = pip_size * lot * base_to_usd / pair_rate
    """
    try:
        import yfinance as yf  # noqa: WPS433 — ленивый импорт, опц. зависимость
    except ImportError:
        return None

    pair = pair.upper()
    pip_size = 0.01 if "JPY" in pair else 0.0001
    lot = 100_000
    base, quote = pair[:3], pair[3:]

    def _last(ticker: str) -> float | None:
        try:
            data = yf.Ticker(f"{ticker}=X").history(period="1d", interval="1h")
            if data is None or data.empty:
                return None
            return float(data["Close"].iloc[-1])
        except Exception:
            return None

    if quote == "USD":
        return pip_size * lot  # ровно $10 на 4-знач, $1 на JPY — не наш случай

    if base == "USD":
        rate = _last(pair)
        if rate is None or rate == 0:
            return None
        return pip_size * lot / rate

    # Кросс-пара: нужны base/USD и сам курс пары
    pair_rate = _last(pair)
    base_to_usd = _last(f"{base}USD") or (
        1.0 / _last(f"USD{base}") if _last(f"USD{base}") else None
    )
    if not pair_rate or not base_to_usd:
        return None
    return pip_size * lot * base_to_usd / pair_rate


@dataclass
class PositionResult:
    balance: float
    risk_percent: float
    risk_amount: float
    stop_pips: float
    pair: str
    pip_value: float
    lots: float
    lots_rounded: float
    actual_risk: float
    actual_risk_percent: float


def calculate_position(
    balance: float,
    risk_percent: float,
    stop_pips: float,
    pair: str,
    live: bool = False,
) -> PositionResult:
    """Считает размер позиции в лотах.

    Если ``live=True``, для чувствительных к курсу пар (USDJPY, USDCHF, USDCAD,
    кросс-пары) подтягиваем актуальную стоимость пипса через yfinance. Если
    скачать не удалось — мягкий фолбэк на табличное значение с предупреждением
    в stdout.
    """
    if balance <= 0:
        raise ValueError("Депозит должен быть > 0")
    if risk_percent <= 0 or risk_percent > 10:
        raise ValueError("Риск % должен быть в диапазоне 0 < risk ≤ 10")
    if stop_pips <= 0:
        raise ValueError("Стоп в пипсах должен быть > 0")

    pair = pair.upper().replace("/", "").replace("-", "")
    if pair not in PIP_VALUE_USD_PER_LOT:
        raise ValueError(
            f"Пара {pair!r} не в таблице. Доступные: "
            + ", ".join(sorted(PIP_VALUE_USD_PER_LOT))
        )

    pip_value = PIP_VALUE_USD_PER_LOT[pair]
    if live and pair in _LIVE_SENSITIVE_PAIRS:
        live_value = _live_pip_value(pair)
        if live_value is None:
            print(
                f"  ⚠️  --live: не удалось получить курс для {pair}, "
                f"использую табличное ${pip_value:.2f}/пипс",
                file=sys.stderr,
            )
        else:
            drift = abs(live_value - pip_value) / pip_value * 100
            print(
                f"  📡 --live: актуальная стоимость пипса для {pair} = "
                f"${live_value:.2f} (отклонение от таблицы: {drift:.1f}%)"
            )
            pip_value = live_value

    risk_amount = balance * risk_percent / 100

    # Размер в стандартных лотах
    lots = risk_amount / (stop_pips * pip_value)

    # Округляем ВНИЗ до 0.01 — минимальный шаг у большинства брокеров.
    # math.floor чтобы реальный риск не превышал плановый.
    lots_rounded = math.floor(lots * 100 + 1e-9) / 100
    if lots_rounded < 0.01:
        lots_rounded = 0.01

    actual_risk = lots_rounded * stop_pips * pip_value
    actual_risk_percent = actual_risk / balance * 100

    return PositionResult(
        balance=balance,
        risk_percent=risk_percent,
        risk_amount=risk_amount,
        stop_pips=stop_pips,
        pair=pair,
        pip_value=pip_value,
        lots=lots,
        lots_rounded=lots_rounded,
        actual_risk=actual_risk,
        actual_risk_percent=actual_risk_percent,
    )


def format_result(r: PositionResult) -> str:
    """Красивый вывод в терминал."""
    warning = ""
    if r.actual_risk > r.risk_amount * 1.05:
        warning = (
            "\n⚠️  Округление дало риск БОЛЬШЕ запланированного — "
            "уменьши размер вручную до 0.01."
        )
    if r.actual_risk_percent > 2.0:
        warning += "\n⚠️  Реальный риск > 2% депозита. Это много для новичка."

    return f"""
╭─────────────────────────────────────────╮
│  КАЛЬКУЛЯТОР РАЗМЕРА ПОЗИЦИИ            │
╰─────────────────────────────────────────╯

Входные данные:
  Депозит:           ${r.balance:,.2f}
  Риск:              {r.risk_percent:.2f}% = ${r.risk_amount:,.2f}
  Стоп-лосс:         {r.stop_pips:.0f} пипсов
  Пара:              {r.pair}
  Стоимость пипса:   ${r.pip_value:.2f} за 1 лот

Расчёт:
  Размер (точный):   {r.lots:.4f} лота
  Размер (округл.):  {r.lots_rounded:.2f} лота
  Реальный риск:     ${r.actual_risk:.2f} ({r.actual_risk_percent:.2f}%)

→ Выстави в терминале: {r.lots_rounded:.2f} лота{warning}
"""


def interactive() -> int:
    """Интерактивный режим — задаёт вопросы пользователю."""
    print("\n=== Калькулятор размера позиции ===\n")
    try:
        balance = float(input("Депозит ($): ").strip())
        risk = float(input("Риск на сделку (%, например 0.5): ").strip())
        stop = float(input("Стоп-лосс (в пипсах): ").strip())
        pair = input("Пара (EURUSD / GBPUSD / USDJPY / ...): ").strip() or "EURUSD"
    except (ValueError, KeyboardInterrupt, EOFError):
        print("\nОтмена.")
        return 1

    try:
        result = calculate_position(balance, risk, stop, pair)
    except ValueError as e:
        print(f"\nОшибка: {e}")
        return 1

    print(format_result(result))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Калькулятор размера позиции для forex",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Примеры:\n"
        "  position_calculator.py\n"
        "  position_calculator.py --balance 1000 --risk 0.5 "
        "--stop 25 --pair EURUSD",
    )
    parser.add_argument("--balance", "-b", type=float, help="Депозит в USD")
    parser.add_argument(
        "--risk", "-r", type=float, help="Риск на сделку в процентах (0.5 = 0.5%%)"
    )
    parser.add_argument("--stop", "-s", type=float, help="Стоп-лосс в пипсах")
    parser.add_argument(
        "--pair",
        "-p",
        type=str,
        default="EURUSD",
        help="Валютная пара (по умолчанию EURUSD)",
    )
    parser.add_argument(
        "--list-pairs", action="store_true", help="Показать список поддерживаемых пар"
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Подтянуть актуальную стоимость пипса через "
        "yfinance (для USDJPY, USDCHF, USDCAD, кросс-пар). "
        "Без yfinance — мягкий фолбэк на таблицу.",
    )
    args = parser.parse_args()

    if args.list_pairs:
        print("Поддерживаемые пары:")
        for p, v in sorted(PIP_VALUE_USD_PER_LOT.items()):
            print(f"  {p:8s} ≈ ${v:.2f} / пипс / стд. лот")
        return 0

    # Если не переданы все 3 параметра — интерактивный режим
    if args.balance is None or args.risk is None or args.stop is None:
        return interactive()

    try:
        result = calculate_position(
            args.balance, args.risk, args.stop, args.pair, live=args.live
        )
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1

    print(format_result(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
