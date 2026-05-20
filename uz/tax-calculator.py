#!/usr/bin/env python3
"""
Налоговый калькулятор для трейдинг-прибыли в Узбекистане.

⚠️ ДИСКЛЕЙМЕР:
  Это упрощённый калькулятор для оценки. Конкретные ставки и порядок
  декларирования уточни на сайте Налогового комитета РУз (soliq.uz)
  или у квалифицированного бухгалтера. Законодательство меняется.

На момент составления (2026):
  - НДФЛ для физлиц-резидентов: 12% от чистого дохода
  - Зарубежные брокерские счета: декларируется доход за календарный год
  - Учитывается ЧИСТЫЙ результат (прибыли − убытки за год)
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime


# Текущие ставки (проверять актуальность!)
NDFL_RATE = 0.12  # 12% НДФЛ для физлиц-резидентов
SOCIAL_RATE = 0.0  # Социальный налог обычно не применяется к инвест-доходу


def calculate_tax(
    gross_profit_usd: float, gross_loss_usd: float,
    deposits_usd: float = 0, withdrawals_usd: float = 0,
    usd_to_uzs: float = 12_500,
) -> dict:
    """Расчёт налога."""
    net_profit_usd = gross_profit_usd - gross_loss_usd
    net_profit_uzs = net_profit_usd * usd_to_uzs

    if net_profit_usd <= 0:
        return {
            "net_profit_usd": net_profit_usd,
            "net_profit_uzs": net_profit_uzs,
            "tax_usd": 0.0,
            "tax_uzs": 0.0,
            "after_tax_usd": net_profit_usd,
            "after_tax_uzs": net_profit_uzs,
            "note": "Убыток — налогов нет. Сохрани отчёт брокера на случай вопросов.",
        }

    tax_usd = net_profit_usd * NDFL_RATE
    tax_uzs = tax_usd * usd_to_uzs

    return {
        "net_profit_usd": net_profit_usd,
        "net_profit_uzs": net_profit_uzs,
        "tax_usd": tax_usd,
        "tax_uzs": tax_uzs,
        "after_tax_usd": net_profit_usd - tax_usd,
        "after_tax_uzs": (net_profit_usd - tax_usd) * usd_to_uzs,
        "note": f"Декларировать до 1 апреля {datetime.now().year + 1} года.",
    }


def print_report(r: dict, gross_profit: float, gross_loss: float) -> None:
    print("\n" + "=" * 60)
    print("  НАЛОГОВЫЙ КАЛЬКУЛЯТОР — РУз")
    print("=" * 60)
    print(f"\n  Валовая прибыль за год:  ${gross_profit:,.2f}")
    print(f"  Валовый убыток за год:   ${gross_loss:,.2f}")
    print(f"  Чистая прибыль:          ${r['net_profit_usd']:,.2f}")
    print(f"                          {r['net_profit_uzs']:>17,.0f} сум")
    print()
    print(f"  Ставка НДФЛ:             {NDFL_RATE * 100:.0f}%")
    print(f"  Налог к уплате:          ${r['tax_usd']:,.2f}")
    print(f"                          {r['tax_uzs']:>17,.0f} сум")
    print(f"\n  После налога:            ${r['after_tax_usd']:,.2f}")
    print(f"                          {r['after_tax_uzs']:>17,.0f} сум")
    print()
    print(f"  📌 {r['note']}")
    print()
    print("─" * 60)
    print("ВАЖНО:")
    print("  • Это УПРОЩЁННЫЙ расчёт. Точные правила — на soliq.uz")
    print("  • Сохраняй ВСЕ отчёты брокера (statement) и P2P-переводы")
    print("  • Налоговые вопросы — к квалифицированному бухгалтеру")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Налоговый калькулятор для трейдинга в РУз",
    )
    parser.add_argument("--profit", type=float, required=True,
                        help="Валовая прибыль за год в USD")
    parser.add_argument("--loss", type=float, default=0,
                        help="Валовый убыток за год в USD")
    parser.add_argument("--usd-rate", type=float, default=12_500,
                        help="Курс USD/UZS (по умолч. 12500)")
    args = parser.parse_args()

    r = calculate_tax(args.profit, args.loss, usd_to_uzs=args.usd_rate)
    print_report(r, args.profit, args.loss)
    return 0


if __name__ == "__main__":
    sys.exit(main())
