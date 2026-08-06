#!/usr/bin/env python3
"""
Проверка статуса лицензии форекс-брокера.

Использует публичные данные регуляторов:
  - FCA (UK): Financial Services Register (требует API key для полного доступа,
              но базовая проверка через публичный поиск)
  - CySEC (Cyprus): открытый список инвестиционных фирм
  - ASIC (Australia): открытая база данных

Скрипт строит URL для поиска и опционально парсит HTML.
Для уверенности всегда проверяй вручную на официальном сайте регулятора.
"""

from __future__ import annotations

import argparse
import sys
import webbrowser
from urllib.parse import quote

import requests


REGULATORS = {
    "FCA": {
        "name": "Financial Conduct Authority (UK)",
        "search_url": "https://register.fca.org.uk/s/search?q={name}&type=Companies",
        "verify_url": "https://register.fca.org.uk/",
        "country": "🇬🇧 Великобритания",
    },
    "CySEC": {
        "name": "Cyprus Securities and Exchange Commission",
        "search_url": "https://www.cysec.gov.cy/en-GB/entities/investment-firms/cypriot/?searchTerm={name}",
        "verify_url": "https://www.cysec.gov.cy/en-GB/entities/investment-firms/cypriot/",
        "country": "🇨🇾 Кипр",
    },
    "ASIC": {
        "name": "Australian Securities and Investments Commission",
        "search_url": "https://connectonline.asic.gov.au/RegistrySearch/faces/landing/SearchRegisters.jspx?searchText={name}",
        "verify_url": "https://asic.gov.au/online-services/search-asic-s-registers/",
        "country": "🇦🇺 Австралия",
    },
    "NFA": {
        "name": "National Futures Association (US)",
        "search_url": "https://www.nfa.futures.org/BasicNet/basic-profile.aspx?nfaid={name}",
        "verify_url": "https://www.nfa.futures.org/BasicNet/",
        "country": "🇺🇸 США",
    },
    "FINMA": {
        "name": "Swiss Financial Market Supervisory Authority",
        "search_url": "https://www.finma.ch/en/finma-public/authorised-institutions-individuals-and-products/",
        "verify_url": "https://www.finma.ch/en/finma-public/",
        "country": "🇨🇭 Швейцария",
    },
}


KNOWN_BROKERS = {
    "exness": {
        "FCA": "Exness (UK) Ltd — №730729 (был активен на 2025)",
        "CySEC": "Exness (Cy) Ltd — №178/12",
        "FSA Seychelles": "для клиентов из СНГ — менее жёсткий регулятор",
    },
    "ic markets": {
        "ASIC": "IC Markets Ltd — №335692",
        "CySEC": "IC Markets EU — №362/18",
    },
    "pepperstone": {
        "FCA": "Pepperstone Ltd — №684312",
        "ASIC": "Pepperstone Group Ltd — №414530",
        "CySEC": "Pepperstone EU — №388/20",
    },
    "fxpro": {
        "FCA": "FxPro UK Ltd — №509956",
        "CySEC": "FxPro Financial Services — №078/07",
    },
    "tickmill": {
        "FCA": "Tickmill UK Ltd — №717270",
        "CySEC": "Tickmill Europe — №278/15",
        "FSCA": "Tickmill SA — FSP 49464",
    },
    "fp markets": {
        "ASIC": "First Prudential Markets — №286354",
        "CySEC": "FP Markets EU — №371/18",
    },
}


def check_fca_register(broker_name: str) -> dict:
    """Простая проверка через публичный поиск FCA."""
    url = REGULATORS["FCA"]["search_url"].format(name=quote(broker_name))
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10,
            allow_redirects=True,
        )
        return {
            "url": url,
            "status_code": resp.status_code,
            "ok": resp.ok,
            "found_keywords": broker_name.lower() in resp.text.lower(),
        }
    except requests.RequestException as e:
        return {"url": url, "error": str(e)}


def check_known(broker_name: str) -> dict | None:
    """Проверка в нашей встроенной базе."""
    key = broker_name.lower().strip()
    for known_key, data in KNOWN_BROKERS.items():
        if known_key in key or key in known_key:
            return {known_key: data}
    return None


def print_report(broker: str, results: dict, open_urls: bool = False) -> None:
    print()
    print("=" * 70)
    print(f"  ПРОВЕРКА БРОКЕРА: {broker}")
    print("=" * 70)
    print()

    # Из встроенной базы
    known = check_known(broker)
    if known:
        print("📚 ИЗ БАЗЫ (исторические данные, проверяй актуальность!):")
        for name, regs in known.items():
            print(f"\n  {name.title()}:")
            for reg, info in regs.items():
                print(f"    • {reg}: {info}")
        print()
    else:
        print("⚠️  Брокер не в нашей базе. Проверь вручную ниже.\n")

    print("🔍 ССЫЛКИ ДЛЯ РУЧНОЙ ПРОВЕРКИ:\n")
    for reg_id, reg in REGULATORS.items():
        url = reg["search_url"].format(name=quote(broker))
        print(f"  {reg['country']} {reg_id} ({reg['name']}):")
        print(f"    {url}")
        print()

    if open_urls:
        print("Открываю в браузере...")
        for reg_id, reg in REGULATORS.items():
            url = reg["search_url"].format(name=quote(broker))
            webbrowser.open(url)

    print("=" * 70)
    print("⚠️  ВАЖНО:")
    print("  • Лицензии меняются. Информация может устареть.")
    print("  • Всегда проверяй на ОФИЦИАЛЬНОМ сайте регулятора.")
    print("  • Многие брокеры имеют несколько юрлиц:")
    print("    - Регулируемое (для ЕС/UK) — строгое")
    print("    - Офшорное (для клиентов из СНГ) — слабее")
    print("  • Спроси у брокера: «к какому юрлицу подключается мой счёт?»")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Проверка статуса брокера у регуляторов",
    )
    parser.add_argument("broker", help="Название брокера (например 'IC Markets')")
    parser.add_argument("--open", action="store_true", help="Открыть ссылки в браузере")
    parser.add_argument(
        "--check-fca",
        action="store_true",
        help="Попытаться найти на FCA через HTTP (экспериментально)",
    )
    args = parser.parse_args()

    results = {}
    if args.check_fca:
        print("🌐 Проверяю FCA...")
        results["FCA"] = check_fca_register(args.broker)
        if results["FCA"].get("found_keywords"):
            print(f"  ✓ FCA: возможно найден '{args.broker}'")
        else:
            print("  ❌ FCA: не найдено явных упоминаний")

    print_report(args.broker, results, args.open)
    return 0


if __name__ == "__main__":
    sys.exit(main())
