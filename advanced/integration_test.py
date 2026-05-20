#!/usr/bin/env python3
"""
Integration test для broker_api — проверяет всю цепочку end-to-end.

Что тестирует:
  1. Импорты всех модулей
  2. YFinance — реальное подключение, скачивание свечей, цена
  3. MT5 — корректное сообщение что нужно
  4. Binance — корректное сообщение что нужно
  5. Цепочка: данные → стратегия → бэктест → отчёт

Если хочешь реально протестировать MT5 — передай свои демо-креды:
  .venv/bin/python advanced/integration_test.py \\
      --mt5-login 12345 --mt5-password XXX --mt5-server "Exness-Demo"
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from broker_api import get_broker  # noqa: E402


PASS, FAIL, SKIP = "✅", "❌", "⏭️ "


def test_imports() -> bool:
    """Тест 1: все модули импортируются без ошибок."""
    print("\n[TEST 1] Импорты модулей...")
    try:
        from broker_api import Broker, get_broker  # noqa: F401
        from broker_api.base import Order, Position  # noqa: F401
        from broker_api.factory import get_broker as gb  # noqa: F401
        print(f"  {PASS} broker_api импортируется")
        return True
    except Exception as e:
        print(f"  {FAIL} Ошибка импорта: {e}")
        return False


def test_yfinance() -> bool:
    """Тест 2: yfinance подключается и отдаёт данные."""
    print("\n[TEST 2] YFinance broker (data only)...")
    try:
        broker = get_broker("yfinance")
        if not broker.connect():
            print(f"  {FAIL} Connect failed")
            return False
        print(f"  {PASS} connect()")

        # Свечи
        candles = broker.get_candles("EURUSD", "H1", 10)
        if candles.empty or len(candles) < 5:
            print(f"  {FAIL} get_candles вернул {len(candles)} свечей (ожидали ≥ 5)")
            return False
        print(f"  {PASS} get_candles(): {len(candles)} свечей")
        print(f"     Последняя: {candles.index[-1]}, close={candles['close'].iloc[-1]:.5f}")

        # Цена
        price = broker.get_price("EURUSD")
        if price["bid"] == 0:
            print(f"  {FAIL} get_price вернул нули")
            return False
        print(f"  {PASS} get_price(): bid={price['bid']:.5f}, ask={price['ask']:.5f}")

        # Несколько разных пар и таймфреймов
        for sym, tf in [("GBPUSD", "H1"), ("USDJPY", "D1")]:
            df = broker.get_candles(sym, tf, 5)
            if df.empty:
                print(f"  {FAIL} get_candles({sym}, {tf}) пусто")
                return False
            print(f"  {PASS} get_candles({sym}, {tf}): {len(df)} свечей")

        # Не поддерживаемые операции должны корректно падать
        try:
            broker.get_balance()
            print(f"  {FAIL} get_balance НЕ упал, должен был")
            return False
        except NotImplementedError:
            print(f"  {PASS} get_balance корректно бросает NotImplementedError")

        broker.disconnect()
        print(f"  {PASS} disconnect()")
        return True
    except Exception as e:
        print(f"  {FAIL} Неожиданная ошибка: {e}")
        return False


def test_mt5(login: int = None, password: str = None,
             server: str = None) -> bool:
    """Тест 3: MT5 broker (или сообщение что пропущено)."""
    print("\n[TEST 3] MT5 broker...")
    try:
        broker = get_broker("mt5")
    except ImportError as e:
        print(f"  {SKIP} {e}")
        print(f"     Это нормально на Mac/Linux. MT5 — Windows only.")
        return True  # это не fail, это пропуск

    if not login or not password or not server:
        print(f"  {SKIP} Не переданы креды MT5. Запусти с --mt5-login/--mt5-password/--mt5-server")
        return True

    # Реальное подключение (только если есть креды)
    try:
        if not broker.connect(login=login, password=password, server=server):
            print(f"  {FAIL} connect failed")
            return False
        print(f"  {PASS} connect()")

        bal = broker.get_balance()
        print(f"  {PASS} Баланс: {bal}")

        candles = broker.get_candles("EURUSD", "H1", 100)
        print(f"  {PASS} get_candles: {len(candles)} свечей")

        positions = broker.get_positions()
        print(f"  {PASS} get_positions: {len(positions)} открытых")

        broker.disconnect()
        return True
    except Exception as e:
        print(f"  {FAIL} {e}")
        return False


def test_binance() -> bool:
    """Тест 4: Binance broker (без креденшилов)."""
    print("\n[TEST 4] Binance broker...")
    try:
        broker = get_broker("binance", testnet=True)
        print(f"  {PASS} get_broker('binance')")
        print(f"  {SKIP} Без api_key/api_secret — пропускаем подключение")
        return True
    except ImportError as e:
        print(f"  {SKIP} {e}")
        return True


def test_strategy_chain() -> bool:
    """Тест 5: данные → стратегия → бэктест."""
    print("\n[TEST 5] End-to-end цепочка: данные → стратегия → бэктест...")

    try:
        # 5a: скачать данные
        broker = get_broker("yfinance")
        broker.connect()
        df = broker.get_candles("EURUSD", "H1", 500)
        broker.disconnect()
        print(f"  {PASS} Шаг 1: получено {len(df)} свечей через broker_api")

        # 5b: применить стратегию
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bot"))
        from strategy import detect_signals, prepare_dataframe

        df_prep = prepare_dataframe(df)
        signals = detect_signals(df_prep)
        print(f"  {PASS} Шаг 2: стратегия нашла {len(signals)} сигналов")

        # 5c: симулировать сделки
        from bot.backtest import simulate, stats

        trades = simulate(df_prep, signals)
        s = stats(trades)
        print(f"  {PASS} Шаг 3: симулировано {s['total']} сделок")

        if s["total"] > 0:
            print(f"     Win rate: {s['win_rate']*100:.1f}%")
            print(f"     Profit Factor: {s['profit_factor']:.2f}")
            print(f"     Итого: {s['total_r']:+.2f}R")

        return True
    except Exception as e:
        print(f"  {FAIL} {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tools() -> bool:
    """Тест 6: что основные tools/ запускаются без ошибок."""
    print("\n[TEST 6] Запуск ключевых tools/...")
    import subprocess

    venv_py = str(Path(__file__).resolve().parent.parent / ".venv" / "bin" / "python")
    tools_dir = Path(__file__).resolve().parent.parent / "tools"

    checks = [
        ("position_calculator", [
            "tools/position_calculator.py",
            "--balance", "1000", "--risk", "0.5",
            "--stop", "25", "--pair", "EURUSD",
        ]),
        ("compound_calculator", [
            "tools/compound_calculator.py",
            "--initial", "1000", "--months", "12",
            "--out", "/tmp/compound-test.png",
        ]),
        ("risk_profile (demo)", [
            "tools/risk_profile.py", "--simulate", "ideal",
        ]),
        ("margin_calculator", [
            "tools/margin_calculator.py",
            "--lots", "0.01", "--price", "1.08", "--leverage", "30",
        ]),
        ("multi_position_sizer", [
            "tools/multi_position_sizer.py",
            "--deposit", "1000", "--total-risk", "2",
            "--trade", "EURUSD", "25",
            "--trade", "GBPUSD", "30",
        ]),
        ("broker_check", [
            "tools/broker_check.py", "Pepperstone",
        ]),
    ]

    all_ok = True
    for name, cmd in checks:
        result = subprocess.run(
            [venv_py] + cmd,
            cwd=str(tools_dir.parent),
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode == 0:
            print(f"  {PASS} {name}")
        else:
            print(f"  {FAIL} {name} (exit {result.returncode})")
            if result.stderr:
                print(f"     stderr: {result.stderr[:200]}")
            all_ok = False
    return all_ok


def main() -> int:
    parser = argparse.ArgumentParser(description="Integration test")
    parser.add_argument("--mt5-login", type=int)
    parser.add_argument("--mt5-password")
    parser.add_argument("--mt5-server")
    parser.add_argument("--skip-tools", action="store_true",
                        help="Не запускать tools/ тесты (быстрее)")
    args = parser.parse_args()

    print("=" * 70)
    print("  INTEGRATION TEST — проверка всей цепочки")
    print("=" * 70)

    results = []
    results.append(("Imports", test_imports()))
    results.append(("YFinance", test_yfinance()))
    results.append(("MT5", test_mt5(args.mt5_login, args.mt5_password,
                                     args.mt5_server)))
    results.append(("Binance", test_binance()))
    results.append(("Strategy chain", test_strategy_chain()))
    if not args.skip_tools:
        results.append(("Tools", test_tools()))

    print("\n" + "=" * 70)
    print("  ИТОГИ")
    print("=" * 70)
    for name, ok in results:
        status = PASS if ok else FAIL
        print(f"  {status} {name}")

    failed = sum(1 for _, ok in results if not ok)
    if failed:
        print(f"\n❌ Провалено: {failed}/{len(results)}")
        return 1
    print(f"\n✅ Все тесты прошли ({len(results)}/{len(results)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
