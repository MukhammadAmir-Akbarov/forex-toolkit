"""Качество банков мини-квизов в конце глав гайда.

Инварианты, на которые опирается виджет chapter-quiz.js:
* каждая глава несёт блок #chapter-quiz + JSON #chapter-quiz-questions;
* ровно 3 вопроса на главу, 4 варианта, тексты вариантов не повторяются
  (правильный ищется по тексту после перемешивания — дубли сделали бы
  ответ неоднозначным);
* во всех локалях один и тот же правильный индекс у вопроса под номером —
  иначе перевод переставил варианты, но не поправил answer;
* нет перекоса позиций правильных ответов (как была дыра в экзамене);
* число глав в dashboard.js (QUIZ_CHAPTERS) совпадает с реальностью.
"""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "_mkdocs"
DASHBOARD = DOCS / "javascripts" / "widgets" / "dashboard.js"
WIDGET = DOCS / "javascripts" / "widgets" / "chapter-quiz.js"

LOCALES = ("ru", "en", "uz")
SUFFIX = {"ru": "", "en": ".en", "uz": ".uz"}


def discover_chapters() -> list[str]:
    """RU-страницы с мини-квизом, относительно _mkdocs/ и без суффикса.

    Глав не хардкодим: добавил квиз на страницу (включая growth/, practice/
    и любой будущий раздел) — тесты подхватывают её сами. Пропажа квиза
    со страницы тоже не пройдёт незаметно: упадёт проверка счётчика
    кабинета (QUIZ_CHAPTERS) ниже.
    """
    found = []
    for path in sorted(DOCS.rglob("*.md")):
        if path.name.endswith((".en.md", ".uz.md")):
            continue
        if 'id="chapter-quiz"' in path.read_text(encoding="utf-8"):
            found.append(str(path.relative_to(DOCS))[:-3])
    return found


CHAPTERS = discover_chapters()


def quiz_key(chapter: str) -> str:
    """Ключ хранилища fx-quiz-v1 — basename страницы, без раздела."""
    return chapter.rsplit("/", 1)[-1]


def load_bank(chapter: str, locale: str) -> list[dict]:
    path = DOCS / f"{chapter}{SUFFIX[locale]}.md"
    text = path.read_text(encoding="utf-8")
    assert f'data-quiz-key="{quiz_key(chapter)}"' in text, (
        f"{chapter}/{locale}: нет #chapter-quiz"
    )
    match = re.search(
        r'<script type="application/json" id="chapter-quiz-questions">(.*?)</script>',
        text,
        re.S,
    )
    assert match, f"{chapter}/{locale}: блок #chapter-quiz-questions не найден"
    return json.loads(match.group(1))


@pytest.mark.parametrize("chapter", CHAPTERS)
@pytest.mark.parametrize("locale", LOCALES)
def test_every_chapter_quiz_is_well_formed(chapter: str, locale: str) -> None:
    bank = load_bank(chapter, locale)
    assert len(bank) == 3, f"{chapter}/{locale}: {len(bank)} вопросов вместо 3"
    for item in bank:
        label = f"{chapter}/{locale}: {item['q'][:50]}"
        assert len(item["options"]) == 4, f"{label} — не 4 варианта"
        assert 0 <= item["answer"] < 4, f"{label} — answer вне диапазона"
        assert item.get("explain"), f"{label} — нет объяснения"
        assert len(set(item["options"])) == 4, f"{label} — дубли вариантов"


@pytest.mark.parametrize("chapter", CHAPTERS)
def test_locales_stay_in_sync(chapter: str) -> None:
    """Один и тот же вопрос под одним номером с одним answer во всех локалях."""
    banks = {locale: load_bank(chapter, locale) for locale in LOCALES}
    for i in range(3):
        answers = {locale: banks[locale][i]["answer"] for locale in LOCALES}
        assert len(set(answers.values())) == 1, (
            f"{chapter} вопрос #{i + 1}: разные правильные ответы по локалям — "
            f"{answers}. Перевод переставил варианты, но не поправил answer."
        )


def test_answer_positions_are_not_skewed() -> None:
    """Клик по одной позиции не должен давать заметную долю верных ответов."""
    answers = [
        load_bank(chapter, "ru")[i]["answer"] for chapter in CHAPTERS for i in range(3)
    ]
    counts = collections.Counter(answers)
    best = max(counts.values()) / len(answers)
    assert best < 0.5, f"перекос позиций ответов: {dict(sorted(counts.items()))}"


def test_quiz_keys_are_unique() -> None:
    """Ключ — basename страницы: дубликаты дали бы общий прогресс в fx-quiz-v1."""
    keys = [quiz_key(c) for c in CHAPTERS]
    dupes = [k for k, n in collections.Counter(keys).items() if n > 1]
    assert not dupes, f"ключи квизов не уникальны: {dupes}"


def test_dashboard_chapter_count_matches_reality() -> None:
    """Карточка квизов в кабинете считает главы по той же цифре, что и страницы."""
    source = DASHBOARD.read_text(encoding="utf-8")
    match = re.search(r"QUIZ_CHAPTERS\s*=\s*(\d+)", source)
    assert match, "в dashboard.js не найден QUIZ_CHAPTERS"
    assert int(match.group(1)) == len(CHAPTERS), (
        f"dashboard считает {match.group(1)} глав, квизы стоят на {len(CHAPTERS)}"
    )


EXAM = DOCS / "javascripts" / "widgets" / "exam.js"


def test_exam_chapter_map_matches_quiz_pages() -> None:
    """Вердикт экзамена ссылается на главы с несданными квизами: карта в
    exam.js должна совпадать с реальным набором квизов, иначе ссылка ведёт
    в никуда или глава выпадает из маршрута повторения."""
    source = EXAM.read_text(encoding="utf-8")
    entries = re.findall(r'\{ key: "([^"]+)", path: "([^"]+)"', source)
    assert {key for key, _ in entries} == {quiz_key(c) for c in CHAPTERS}
    for key, path in entries:
        assert (DOCS / f"{path.rstrip('/')}.md").is_file(), (
            f"exam.js: глава {key} ссылается на несуществующую {path}"
        )


def test_widget_shuffles_options_without_mutating_the_bank() -> None:
    """Перемешивание идёт по копии — иначе пересдача съезжает по answer."""
    source = WIDGET.read_text(encoding="utf-8")
    assert "function shuffled(list)" in source, "функция перемешивания пропала"
    assert "list.slice()" in source, "перемешивание мутирует исходный массив"
    assert "shuffled(item.options)" in source, "варианты ответа не перемешиваются"


def test_dashboard_chapter_paths_match_quiz_pages() -> None:
    """Блок «пора повторить квизы» в кабинете использует свою карту
    CHAPTER_PATHS — она обязана покрывать все страницы с квизами."""
    source = DASHBOARD.read_text(encoding="utf-8")
    for chapter in CHAPTERS:
        key = quiz_key(chapter)
        assert f'"{key}":' in source, f"dashboard.js: нет пути для квиза {key}"
        assert f'"{chapter}/"' in source, f"dashboard.js: неверный путь у {key}"
