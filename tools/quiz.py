#!/usr/bin/env python3
"""
Spaced Repetition Quiz — еженедельный тест по терминам и концепциям.

Использует упрощённый SM-2 алгоритм (как в Anki):
  - Если знаешь — следующий показ через 1, 3, 7, 14, 30, 60 дней
  - Если не знаешь — снова через день

Прогресс сохраняется в quiz-progress.json.

Запуск раз в неделю:
  python tools/quiz.py
"""
from __future__ import annotations

import csv
import json
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

CARDS_FILE = Path(__file__).resolve().parent.parent / "extras" / "anki-cards.csv"
PROGRESS_FILE = Path(__file__).resolve().parent.parent / "quiz-progress.json"


def load_cards() -> list[dict]:
    if not CARDS_FILE.exists():
        print(f"❌ Не найден файл с карточками: {CARDS_FILE}")
        sys.exit(1)
    with open(CARDS_FILE, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    return {}


def save_progress(progress: dict) -> None:
    PROGRESS_FILE.write_text(
        json.dumps(progress, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def get_due_cards(cards: list[dict], progress: dict) -> list[dict]:
    today = datetime.now().date()
    due = []
    for card in cards:
        key = card["front"]
        entry = progress.get(key, {"next_review": today.isoformat(), "stage": 0})
        next_date = datetime.fromisoformat(entry["next_review"]).date()
        if next_date <= today:
            card["_stage"] = entry["stage"]
            due.append(card)
    return due


INTERVALS = {
    0: 1,    # после изучения — через 1 день
    1: 3,    # знаю — через 3 дня
    2: 7,    # знаю — через неделю
    3: 14,   # знаю — через 2 недели
    4: 30,   # знаю — через месяц
    5: 60,   # знаю — через 2 месяца
    6: 120,  # знаю — через 4 месяца
}


def update_progress(progress: dict, key: str, knew: bool) -> None:
    entry = progress.get(key, {"stage": 0})
    if knew:
        entry["stage"] = min(entry.get("stage", 0) + 1, 6)
    else:
        entry["stage"] = max(entry.get("stage", 0) - 1, 0)

    interval = INTERVALS.get(entry["stage"], 1)
    next_date = (datetime.now() + timedelta(days=interval)).date()
    entry["next_review"] = next_date.isoformat()
    entry["last_review"] = datetime.now().isoformat()
    progress[key] = entry


def quiz_card(card: dict) -> bool:
    """Возвращает True если пользователь ответил верно."""
    print("\n" + "─" * 60)
    print(f"❓ Что значит:")
    print(f"\n  {card['front']}")
    input("\n[Enter — показать ответ]")
    print(f"\n💡 Ответ:")
    print(f"\n  {card['back']}")
    while True:
        ans = input("\nЗнал? (y = да / n = нет / s = пропустить): ").strip().lower()
        if ans in ("y", "yes", "д", "да", "1"):
            return True
        elif ans in ("n", "no", "н", "нет", "0"):
            return False
        elif ans in ("s", "skip"):
            return None
        print("y / n / s")


def show_stats(progress: dict) -> None:
    if not progress:
        print("Прогресса пока нет. Это первое занятие.")
        return

    stages = [0] * 7
    for entry in progress.values():
        stages[min(entry.get("stage", 0), 6)] += 1

    total = sum(stages)
    learned = sum(stages[3:])  # стадия 3+ = «знаю надолго»
    print("\n📊 Твой прогресс:")
    print(f"  Изучено карточек: {total}")
    print(f"  «Знаю надолго» (стадия 3+): {learned} ({learned/total*100:.0f}%)")
    print()
    labels = ["Только узнал", "1-3 дня", "1 неделя", "2 недели",
              "1 месяц", "2 месяца", "4 месяца"]
    for i, (label, n) in enumerate(zip(labels, stages)):
        bar = "▓" * min(n, 30)
        print(f"  Стадия {i}: {label:<14} [{bar:<30}] {n}")


def main() -> int:
    cards = load_cards()
    progress = load_progress()

    print("=" * 60)
    print("  📚 SPACED REPETITION QUIZ — еженедельная проверка")
    print("=" * 60)

    show_stats(progress)

    due = get_due_cards(cards, progress)
    print(f"\nКарточек на сегодня: {len(due)}")

    if not due:
        print("\n✅ Сегодня нет карточек на повтор. Возвращайся завтра!")
        return 0

    # Перемешиваем для разнообразия
    random.shuffle(due)
    # Ограничим 20 карточек за сеанс (чтобы не выгорать)
    if len(due) > 20:
        print(f"Покажу 20 из {len(due)} — остальные в следующий раз")
        due = due[:20]

    correct = 0
    skipped = 0
    for i, card in enumerate(due, 1):
        print(f"\n[{i}/{len(due)}]", end="")
        result = quiz_card(card)
        if result is None:
            skipped += 1
            continue
        update_progress(progress, card["front"], result)
        if result:
            correct += 1

    save_progress(progress)

    answered = len(due) - skipped
    print("\n" + "=" * 60)
    print("  Сессия завершена")
    print("=" * 60)
    if answered > 0:
        print(f"\n  Отвечено: {answered}")
        print(f"  Правильно: {correct} ({correct/answered*100:.0f}%)")
        if correct / answered >= 0.8:
            print("  ✅ Отличный результат! Возвращайся через несколько дней.")
        elif correct / answered >= 0.5:
            print("  🟡 Неплохо. Слабые карточки придут раньше.")
        else:
            print("  ❌ Стоит вернуться к основным гайдам — много пробелов.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nПрервано.")
        sys.exit(0)
