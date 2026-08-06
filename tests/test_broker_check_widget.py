"""Виджет проверки брокера повторяет данные tools/broker_check.py.

Ссылки на реестры и номера лицензий продублированы в JS намеренно: браузер не
может импортировать Python. Но разъехаться они не должны — ссылка на реестр,
ведущая не туда, обесценивает весь инструмент.
"""

from __future__ import annotations

import re
from pathlib import Path

from broker_check import KNOWN_BROKERS, REGULATORS

WIDGET = (
    Path(__file__).resolve().parent.parent
    / "_mkdocs"
    / "javascripts"
    / "widgets"
    / "broker-check.js"
)


def widget_source() -> str:
    return WIDGET.read_text(encoding="utf-8")


def test_widget_covers_every_regulator() -> None:
    source = widget_source()
    for regulator_id in REGULATORS:
        assert f'id: "{regulator_id}"' in source, f"нет регулятора {regulator_id}"


def test_search_urls_match_the_cli() -> None:
    source = widget_source()
    for regulator_id, data in REGULATORS.items():
        assert data["search_url"] in source, f"{regulator_id}: ссылка разошлась с CLI"


def test_widget_knows_the_same_brokers() -> None:
    source = widget_source()
    for broker in KNOWN_BROKERS:
        assert f'"{broker}"' in source, f"нет брокера {broker}"


def test_licence_numbers_are_carried_over() -> None:
    """Номер лицензии — то, что пользователь сверяет с реестром."""
    source = widget_source()
    numbers = set()
    for entries in KNOWN_BROKERS.values():
        for text in entries.values():
            numbers.update(re.findall(r"№\s*([\w/]+)", text))
    assert numbers, "в CLI не нашлось номеров лицензий — тест потерял смысл"
    for number in numbers:
        assert number in source, f"номер лицензии {number} потерян в виджете"
