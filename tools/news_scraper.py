#!/usr/bin/env python3
"""
News scraper для экономического календаря Forex Factory.

Скачивает события на сегодня/завтра, показывает только важные (red folder).
Если scraping упадёт (FF может изменить разметку) — даёт ссылку на сайт.
"""
from __future__ import annotations

import argparse
import sys

import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
}


def fetch_calendar(date: str = "today") -> list[dict]:
    """
    Скачивает Forex Factory календарь.
    date: "today" | "tomorrow" | "this-week" | "next-week"
    """
    url = f"https://www.forexfactory.com/calendar?day={date}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка загрузки: {e}", file=sys.stderr)
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    events = []

    # Forex Factory часто меняет разметку. Пробуем несколько селекторов.
    rows = soup.find_all("tr", class_=lambda c: c and "calendar__row" in str(c))

    for row in rows:
        try:
            event = {}
            time_cell = row.find("td", class_=lambda c: c and "time" in str(c))
            if time_cell:
                event["time"] = time_cell.text.strip()

            currency = row.find("td",
                                class_=lambda c: c and "currency" in str(c))
            if currency:
                event["currency"] = currency.text.strip()

            impact = row.find("td", class_=lambda c: c and "impact" in str(c))
            if impact:
                spans = impact.find_all("span")
                impact_class = " ".join(
                    str(s.get("class", "")) for s in spans
                )
                if "red" in impact_class or "high" in impact_class.lower():
                    event["impact"] = "🔴 ВАЖНО"
                elif "orange" in impact_class or "medium" in impact_class.lower():
                    event["impact"] = "🟡 средне"
                elif "yellow" in impact_class or "low" in impact_class.lower():
                    event["impact"] = "🟢 низко"
                else:
                    event["impact"] = "—"

            event_cell = row.find("td",
                                  class_=lambda c: c and "event" in str(c))
            if event_cell:
                event["name"] = event_cell.text.strip()

            if event.get("name") and event.get("currency"):
                events.append(event)
        except Exception:
            continue

    return events


def print_events(events: list[dict], filter_high: bool = False) -> None:
    if not events:
        print("\nНе удалось загрузить календарь.")
        print("Открой вручную: https://www.forexfactory.com/calendar")
        return

    if filter_high:
        events = [e for e in events if "🔴" in e.get("impact", "")]

    if not events:
        print("\n✓ Красных новостей сегодня нет — спокойный день.")
        return

    print(f"\n{'Время':<10} {'Валюта':<8} {'Важность':<14} Событие")
    print("─" * 70)
    for e in events:
        print(
            f"{e.get('time', '?'):<10} "
            f"{e.get('currency', '?'):<8} "
            f"{e.get('impact', '?'):<14} "
            f"{e.get('name', '?')[:50]}"
        )
    print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Экономический календарь Forex Factory",
    )
    parser.add_argument("--day", choices=["today", "tomorrow",
                                           "this-week", "next-week"],
                        default="today")
    parser.add_argument("--high-only", action="store_true",
                        help="Только красные новости")
    args = parser.parse_args()

    print(f"\n📰 Forex Factory · {args.day}")
    print("=" * 70)

    events = fetch_calendar(args.day)
    print_events(events, args.high_only)

    if events:
        print(f"Всего событий: {len(events)}")
        high = sum(1 for e in events if "🔴" in e.get("impact", ""))
        if high > 0:
            print(f"⚠️  Красных: {high} — не торгуй за 2 часа до них")

    print("\n💡 Полный календарь: https://www.forexfactory.com/calendar")
    return 0


if __name__ == "__main__":
    sys.exit(main())
