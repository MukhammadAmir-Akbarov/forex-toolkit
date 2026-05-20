"""Командные точки входа для pip-пакета.

После `pip install forex-toolkit` пользователь получает команды:
  forex-position
  forex-backtest
  forex-journal
  forex-risk-profile
  forex-broker-check
  forex-news
  forex-correlations
  forex-monte-carlo
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _run(script_relative: str, *extra_args: str) -> int:
    """Запустить скрипт из проекта (если установлен в dev режиме)."""
    root = Path(__file__).resolve().parent.parent
    script = root / script_relative
    if not script.exists():
        print(f"⚠️  {script_relative} не найден.")
        print("    Установи проект в editable mode: pip install -e .")
        return 1
    return subprocess.call([sys.executable, str(script), *sys.argv[1:]])


def position_calculator() -> int:
    return _run("tools/position_calculator.py")


def backtest() -> int:
    return _run("bot/backtest.py")


def journal() -> int:
    return _run("tools/journal_cli.py")


def risk_profile() -> int:
    return _run("tools/risk_profile.py")


def broker_check() -> int:
    return _run("tools/broker_check.py")


def news() -> int:
    return _run("tools/news_scraper.py")


def correlations() -> int:
    return _run("tools/market_correlations.py")


def monte_carlo() -> int:
    return _run("tools/monte_carlo.py")


if __name__ == "__main__":
    # Если запущено напрямую — показать список команд
    print("forex-toolkit CLI команды:")
    print("  forex-position       — калькулятор позиции")
    print("  forex-backtest       — бэктест")
    print("  forex-journal        — журнал сделок")
    print("  forex-risk-profile   — тест готовности")
    print("  forex-broker-check   — проверка брокера")
    print("  forex-news           — экономический календарь")
    print("  forex-correlations   — корреляции рынков")
    print("  forex-monte-carlo    — монте-карло")
