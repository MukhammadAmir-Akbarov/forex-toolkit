"""Командные точки входа для pip-пакета.

После `pip install forex-toolkit` пользователь получает команды:
  forex-position, forex-backtest, forex-journal, forex-risk-profile,
  forex-broker-check, forex-news, forex-correlations, forex-monte-carlo

Чтобы команды работали и из установленного wheel, и из репозитория
(editable / clone), каждый скрипт ищется в двух местах по очереди:

  1. forex_toolkit/_tools/<script>  — копии, вшитые в wheel (force-include).
  2. <repo>/{tools,bot}/<script>    — оригиналы в репозитории.

Скрипт исполняется через runpy с именем "__main__", поэтому его блок
`if __name__ == "__main__": sys.exit(main())` отрабатывает как при прямом запуске,
а аргументы командной строки прокидываются через обычный sys.argv.
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

_PKG = Path(__file__).resolve().parent
_ROOT = _PKG.parent


def _run(script: str, *repo_subdirs: str) -> int:
    """Найти скрипт и выполнить его. Возвращает код возврата скрипта."""
    candidates = [_PKG / "_tools" / script]
    candidates += [_ROOT / sub / script for sub in repo_subdirs]

    path = next((p for p in candidates if p.exists()), None)
    if path is None:
        print(f"⚠️  Скрипт {script!r} не найден.")
        print("    Если ставил из исходников — установи editable: pip install -e .")
        return 1

    # Чтобы соседние импорты внутри скрипта резолвились
    # (например, backtest.py делает `from strategy import ...`).
    script_dir = str(path.parent)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    try:
        runpy.run_path(str(path), run_name="__main__")
    except SystemExit as exc:  # скрипты завершаются через sys.exit(main())
        code = exc.code
        if code is None:
            return 0
        return code if isinstance(code, int) else 1
    return 0


def position_calculator() -> int:
    return _run("position_calculator.py", "tools")


def backtest() -> int:
    return _run("backtest.py", "bot")


def journal() -> int:
    return _run("journal_cli.py", "tools")


def risk_profile() -> int:
    return _run("risk_profile.py", "tools")


def broker_check() -> int:
    return _run("broker_check.py", "tools")


def news() -> int:
    return _run("news_scraper.py", "tools")


def correlations() -> int:
    return _run("market_correlations.py", "tools")


def monte_carlo() -> int:
    return _run("monte_carlo.py", "tools")


_COMMANDS = {
    "forex-position": "калькулятор размера позиции",
    "forex-backtest": "бэктест стратегии EMA50 pullback",
    "forex-journal": "журнал сделок",
    "forex-risk-profile": "тест готовности к реальной торговле",
    "forex-broker-check": "проверка брокера",
    "forex-news": "экономический календарь / новости",
    "forex-correlations": "корреляции рынков",
    "forex-monte-carlo": "монте-карло симуляция",
}


def main() -> int:
    """Запуск `python -m forex_toolkit.cli` — показать список команд."""
    print("forex-toolkit CLI команды:")
    for name, desc in _COMMANDS.items():
        print(f"  {name:22s} — {desc}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
