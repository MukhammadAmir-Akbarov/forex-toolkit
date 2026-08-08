"""Данные квиза: структура и качество вариантов.

Квиз лежит инлайном в трёх локалях, и проверять его было нечем — в отличие от
экзамена, у которого банк вынесен в JSON и покрыт тестами. Отсюда две группы
проверок: инварианты, на которые опирается виджет, и заслон от возврата
вариантов-заполнителей.

Заполнитель вроде «хвастаться прибылью» сокращает выбор с четырёх до двух и
превращает квиз в проверку внимательности вместо понимания.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

DOCS = Path(__file__).resolve().parent.parent / "_mkdocs" / "tools"
LOCALES = {"ru": "quiz.md", "en": "quiz.en.md", "uz": "quiz.uz.md"}

ITEM = re.compile(
    r'q:\s*"(?P<q>.*?)",\s*\n\s*options:\s*(?P<options>\[.*?\]),'
    r"\s*\n\s*correct:\s*(?P<correct>\d+)",
    re.S,
)


def load(locale: str) -> list[dict]:
    text = (DOCS / LOCALES[locale]).read_text(encoding="utf-8")
    block = text[text.index("const QUIZ") : text.index("let qDeck")]
    return [
        {
            "q": match.group("q"),
            "options": json.loads(match.group("options")),
            "correct": int(match.group("correct")),
        }
        for match in ITEM.finditer(block)
    ]


@pytest.mark.parametrize("locale", LOCALES)
def test_every_question_is_well_formed(locale: str) -> None:
    for number, item in enumerate(load(locale), start=1):
        label = f"{locale} #{number}"
        assert len(item["options"]) == 4, f"{label}: не четыре варианта"
        # Виджет перемешивает варианты и находит верный по тексту —
        # одинаковые тексты сделали бы ответ неоднозначным.
        assert len(set(item["options"])) == 4, f"{label}: дубли вариантов"
        assert 0 <= item["correct"] < 4, f"{label}: индекс вне диапазона"
        assert item["q"].strip(), f"{label}: пустой вопрос"


def test_locales_stay_in_sync() -> None:
    """Один вопрос под одним номером и с одним правильным индексом везде."""
    banks = {locale: load(locale) for locale in LOCALES}
    sizes = {locale: len(bank) for locale, bank in banks.items()}
    assert len(set(sizes.values())) == 1, f"разный размер: {sizes}"

    for index in range(len(banks["ru"])):
        answers = {locale: banks[locale][index]["correct"] for locale in LOCALES}
        assert len(set(answers.values())) == 1, (
            f"вопрос #{index + 1}: разные правильные ответы — {answers}. "
            "Перевод переставил варианты, но не поправил correct."
        )


# Формулировки, которые никто не выберет всерьёз: они выдают правильный ответ
# и снижают квиз до угадывания. Список пополняется, если снова заведутся.
FILLER = (
    "хвастаться",
    "уведомления в telegram",
    "войти на всю котлету",
    "по красивой рекламе",
    "пустая трата времени",
    "отличная возможность",
    "разумный план",
    "brag",
    "telegram notifications",
    "waste of time",
    "beautiful advert",
)


@pytest.mark.parametrize("locale", LOCALES)
def test_no_filler_options(locale: str) -> None:
    offenders = []
    for number, item in enumerate(load(locale), start=1):
        for option in item["options"]:
            lowered = option.lower()
            for phrase in FILLER:
                if phrase in lowered:
                    offenders.append(f"#{number}: {option!r}")
    assert not offenders, (
        f"{locale}: варианты-заполнители вернулись — их никто не выберет, "
        f"и выбор сокращается с четырёх до двух: {offenders}"
    )


@pytest.mark.parametrize("locale", LOCALES)
def test_wrong_options_are_not_obviously_shorter(locale: str) -> None:
    """Самый длинный вариант не должен быть правильным чаще, чем случайно.

    Классическая утечка в тестах: верный ответ пишут развёрнуто, а неверные —
    коротко, и его видно не читая.
    """
    bank = load(locale)
    longest_is_correct = sum(
        1
        for item in bank
        if item["options"].index(max(item["options"], key=len)) == item["correct"]
    )
    assert longest_is_correct <= len(bank) * 0.5, (
        f"{locale}: самый длинный вариант верен в {longest_is_correct} из "
        f"{len(bank)} вопросов — ответ виден по длине"
    )


@pytest.mark.parametrize("locale", LOCALES)
def test_quiz_shuffles_options_at_runtime(locale: str) -> None:
    """Порядок вариантов в исходнике не должен подсказывать ответ."""
    source = (DOCS / LOCALES[locale]).read_text(encoding="utf-8")
    assert "qDeck = shuffle(QUIZ)" in source, f"{locale}: вопросы не перемешиваются"
    assert "shuffle(item.options)" in source, f"{locale}: варианты не перемешиваются"
    assert "const a = [...list]" in source, f"{locale}: перемешивание мутирует вход"
