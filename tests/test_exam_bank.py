"""Качество банка вопросов итогового экзамена.

Зачем: экзамен сдавался не читая вопросов. В банке правильный ответ стоял
вторым 16 раз из 18, поэтому 18 кликов по второй кнопке давали 89% при
проходном балле 80% — сертификат выдавался за узнавание позиции, а не за знание.

Дыру закрывают две вещи, и обе проверяются здесь:

* виджет перемешивает варианты на каждой попытке (тест ниже читает exam.js);
* сам банк не должен иметь перекоса позиций — если перемешивание когда-нибудь
  уберут, содержимое не должно снова выдавать ответ бесплатно.

Плюс инварианты, на которые опирается виджет: правильный вариант ищется по
тексту после перемешивания, значит тексты внутри вопроса не должны повторяться.
"""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PAGES = {
    "ru": ROOT / "_mkdocs" / "tools" / "exam.md",
    "en": ROOT / "_mkdocs" / "tools" / "exam.en.md",
    "uz": ROOT / "_mkdocs" / "tools" / "exam.uz.md",
}
WIDGET = ROOT / "_mkdocs" / "javascripts" / "widgets" / "exam.js"

# Сколько вопросов виджет достаёт за попытку и какой балл считается сдачей.
DRAW = 20
PASS_PERCENT = 80
LOCALES = tuple(PAGES)


def load_bank(locale: str) -> list[dict]:
    text = PAGES[locale].read_text(encoding="utf-8")
    match = re.search(
        r'<script type="application/json" id="exam-questions">(.*?)</script>',
        text,
        re.S,
    )
    assert match, f"{locale}: блок #exam-questions не найден"
    return json.loads(match.group(1))


@pytest.mark.parametrize("locale", LOCALES)
def test_bank_is_larger_than_one_attempt(locale: str) -> None:
    """Банк больше выборки — иначе пересдача идёт по тем же вопросам."""
    bank = load_bank(locale)
    assert len(bank) > DRAW, f"{locale}: в банке {len(bank)}, выборка {DRAW}"


@pytest.mark.parametrize("locale", LOCALES)
def test_blind_clicking_one_position_cannot_pass(locale: str) -> None:
    """Регрессия: постоянный клик по одной позиции не должен давать сдачу.

    Раньше вторая кнопка была верной в 89% вопросов при проходном балле 80%.
    """
    bank = load_bank(locale)
    counts = collections.Counter(item["answer"] for item in bank)
    best = 100 * max(counts.values()) / len(bank)
    assert best < PASS_PERCENT, (
        f"{locale}: клик по одной позиции даёт {best:.0f}% при проходном "
        f"{PASS_PERCENT}% — распределение ответов {dict(sorted(counts.items()))}"
    )


@pytest.mark.parametrize("locale", LOCALES)
def test_every_question_is_well_formed(locale: str) -> None:
    bank = load_bank(locale)
    for item in bank:
        label = item["q"][:50]
        assert len(item["options"]) == 4, f"{locale}: {label} — не 4 варианта"
        assert 0 <= item["answer"] < 4, f"{locale}: {label} — answer вне диапазона"
        assert item.get("explain"), f"{locale}: {label} — нет объяснения"
        # Виджет находит правильный вариант по тексту после перемешивания:
        # одинаковые тексты сделали бы ответ неоднозначным.
        assert len(set(item["options"])) == 4, f"{locale}: {label} — дубли вариантов"


@pytest.mark.parametrize("locale", LOCALES)
def test_questions_are_unique(locale: str) -> None:
    bank = load_bank(locale)
    repeated = [
        q for q, n in collections.Counter(i["q"] for i in bank).items() if n > 1
    ]
    assert not repeated, f"{locale}: повторяются вопросы: {repeated}"


def test_locales_stay_in_sync() -> None:
    """Один и тот же вопрос под одним номером во всех локалях."""
    banks = {locale: load_bank(locale) for locale in LOCALES}
    sizes = {locale: len(bank) for locale, bank in banks.items()}
    assert len(set(sizes.values())) == 1, f"разный размер банка: {sizes}"
    for i in range(len(banks["ru"])):
        answers = {locale: banks[locale][i]["answer"] for locale in LOCALES}
        assert len(set(answers.values())) == 1, (
            f"вопрос #{i + 1}: разные правильные ответы по локалям — {answers}. "
            "Значит перевод переставил варианты, но не поправил answer."
        )


def test_widget_shuffles_options_without_mutating_the_bank() -> None:
    """Перемешивание идёт по копии.

    Если перемешивать массив вариантов на месте, вторая попытка получит уже
    переставленный options при старом answer — и виджет засчитает как верный
    другой вариант.
    """
    source = WIDGET.read_text(encoding="utf-8")
    assert "function shuffled(list)" in source, "функция перемешивания пропала"
    assert "list.slice()" in source, "перемешивание мутирует исходный массив"
    assert "shuffled(item.options)" in source, "варианты ответа не перемешиваются"
    assert "shuffled(BANK)" in source, "вопросы не перемешиваются"


@pytest.mark.parametrize("locale", LOCALES)
def test_most_questions_are_applied_not_definitions(locale: str) -> None:
    """Экзамен проверяет применение, а не узнавание определений.

    Прикидка грубая, но удерживает состав: «расчётным» считаем вопрос, где
    числа стоят в вариантах ответа (объём, маржа, EV, налог), «прикладным» —
    где число есть в самой постановке, то есть дана конкретная ситуация.
    Пороги стоят ниже текущих значений (13 и 21 из 30): тест ловит сползание
    банка обратно в «что такое стоп-лосс», а не запрещает менять вопросы.
    """
    bank = load_bank(locale)
    numeric = [
        i for i in bank if sum(bool(re.search(r"\d", o)) for o in i["options"]) >= 3
    ]
    applied = [i for i in bank if i in numeric or re.search(r"\d", i["q"])]
    assert len(numeric) >= 10, (
        f"{locale}: только {len(numeric)} вопросов требуют вычисления"
    )
    assert len(applied) * 2 > len(bank), (
        f"{locale}: только {len(applied)} из {len(bank)} вопросов прикладные"
    )
