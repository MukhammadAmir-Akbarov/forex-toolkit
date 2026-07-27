"""Import closed trades from MetaTrader 5 HTML account statements.

MT5 statements contain execution deals rather than one row per completed trade.
This module matches entry and exit deals FIFO by symbol and volume, including
partial closes, and returns rows compatible with the project's web journal.
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup

JOURNAL_HEADERS = [
    "id",
    "date",
    "time",
    "pair",
    "timeframe",
    "direction",
    "setup",
    "entry_price",
    "stop_loss",
    "take_profit",
    "stop_pips",
    "target_pips",
    "rr_planned",
    "lot_size",
    "risk_usd",
    "close_price",
    "close_time",
    "result_pips",
    "result_usd",
    "result_r",
    "outcome",
    "followed_rules",
    "emotions",
    "what_went_well",
    "mistakes",
    "lesson",
]

_ALIASES = {
    "time": {"time", "время"},
    "deal": {"deal", "сделка", "ticket", "тикет"},
    "symbol": {"symbol", "символ", "инструмент"},
    "type": {"type", "тип"},
    "entry": {"direction", "entry", "направление", "вход"},
    "volume": {"volume", "объем", "объём"},
    "price": {"price", "цена"},
    "commission": {"commission", "комиссия"},
    "fee": {"fee", "сбор"},
    "swap": {"swap", "своп"},
    "profit": {"profit", "прибыль"},
    "comment": {"comment", "комментарий"},
}


class MT5StatementError(ValueError):
    """The input does not contain a recognizable MT5 deals table."""


@dataclass
class ImportResult:
    trades: list[dict[str, str]]
    warnings: list[str] = field(default_factory=list)


@dataclass
class _Deal:
    ticket: str
    timestamp: datetime
    symbol: str
    side: str
    entry: str
    volume: float
    price: float
    commission: float
    fee: float
    swap: float
    profit: float
    comment: str = ""

    @property
    def costs(self) -> float:
        return self.commission + self.fee + self.swap


@dataclass
class _OpenLot:
    deal: _Deal
    remaining: float
    remaining_costs: float


def _clean(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip()


def _key(value: str) -> str:
    return _clean(value).lower().rstrip(":")


def _number(value: str) -> float:
    text = _clean(value).replace(" ", "").replace("'", "")
    if not text:
        return 0.0
    negative = text.startswith("(") and text.endswith(")")
    text = text.strip("()")
    if "," in text and "." not in text:
        text = text.replace(",", ".")
    elif "," in text and "." in text:
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    text = re.sub(r"[^0-9eE.+-]", "", text)
    try:
        number = float(text)
    except ValueError:
        return 0.0
    return -number if negative else number


def _timestamp(value: str) -> datetime:
    text = _clean(value)
    for fmt in (
        "%Y.%m.%d %H:%M:%S",
        "%Y.%m.%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%d.%m.%Y %H:%M:%S",
        "%d.%m.%Y %H:%M",
    ):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    raise MT5StatementError(f"Unsupported MT5 deal time: {value!r}")


def _canonical_header(value: str) -> str | None:
    normalized = _key(value)
    for canonical, aliases in _ALIASES.items():
        if normalized in aliases:
            return canonical
    return None


def _side(value: str) -> str:
    normalized = _key(value)
    if normalized in {"buy", "покупка"}:
        return "buy"
    if normalized in {"sell", "продажа"}:
        return "sell"
    return ""


def _entry(value: str) -> str:
    normalized = _key(value).replace(" ", "")
    if normalized in {"in", "вход"}:
        return "in"
    if normalized in {"out", "выход"}:
        return "out"
    if normalized in {"outby", "closeby", "выходвстречным"}:
        return "out"
    if normalized in {"in/out", "inout", "разворот"}:
        return "inout"
    return ""


def _extract_deals(html: str) -> list[_Deal]:
    soup = BeautifulSoup(html, "html.parser")
    deals: list[_Deal] = []
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        header_index = -1
        columns: dict[str, int] = {}
        for index, row in enumerate(rows):
            labels = [
                _clean(cell.get_text(" ", strip=True))
                for cell in row.find_all(["th", "td"])
            ]
            mapped = {
                canonical: position
                for position, label in enumerate(labels)
                if (canonical := _canonical_header(label))
            }
            required = {"time", "deal", "symbol", "type", "entry", "volume", "price"}
            if required <= mapped.keys():
                header_index = index
                columns = mapped
                break
        if header_index < 0:
            continue
        for row in rows[header_index + 1 :]:
            cells = [
                _clean(cell.get_text(" ", strip=True))
                for cell in row.find_all(["th", "td"])
            ]
            if not cells or max(columns.values()) >= len(cells):
                continue

            def get(name: str) -> str:
                position = columns.get(name)
                if position is not None and position < len(cells):
                    return cells[position]
                return ""

            side = _side(get("type"))
            entry = _entry(get("entry"))
            symbol = re.sub(r"[^A-Za-z0-9._-]", "", get("symbol")).upper()
            if not side or not entry or not symbol:
                continue
            try:
                timestamp = _timestamp(get("time"))
            except MT5StatementError:
                continue
            deals.append(
                _Deal(
                    ticket=get("deal"),
                    timestamp=timestamp,
                    symbol=symbol,
                    side=side,
                    entry=entry,
                    volume=abs(_number(get("volume"))),
                    price=_number(get("price")),
                    commission=_number(get("commission")),
                    fee=_number(get("fee")),
                    swap=_number(get("swap")),
                    profit=_number(get("profit")),
                    comment=get("comment"),
                )
            )
    if not deals:
        raise MT5StatementError(
            "No MT5 deals table found. Export Account History as an HTML report."
        )
    return sorted(deals, key=lambda deal: deal.timestamp)


def _fmt(value: float, places: int = 8) -> str:
    return f"{value:.{places}f}".rstrip("0").rstrip(".")


def _journal_row(
    opening: _Deal,
    closing: _Deal,
    volume: float,
    result_usd: float,
) -> dict[str, str]:
    direction = "long" if opening.side == "buy" else "short"
    price_diff = (
        closing.price - opening.price
        if direction == "long"
        else opening.price - closing.price
    )
    pip_size = 0.01 if "JPY" in opening.symbol.upper() else 0.0001
    result_pips = price_diff / pip_size
    outcome = "win" if result_usd > 0 else "loss" if result_usd < 0 else "be"
    row = {header: "" for header in JOURNAL_HEADERS}
    row.update(
        {
            "id": closing.ticket or opening.ticket,
            "date": opening.timestamp.strftime("%Y-%m-%d"),
            "time": opening.timestamp.strftime("%H:%M"),
            "pair": opening.symbol,
            "direction": direction,
            "entry_price": _fmt(opening.price),
            "lot_size": _fmt(volume, 4),
            "close_price": _fmt(closing.price),
            "close_time": closing.timestamp.strftime("%Y-%m-%d %H:%M"),
            "result_pips": _fmt(result_pips, 1),
            "result_usd": _fmt(result_usd, 2),
            "outcome": outcome,
            "lesson": closing.comment or opening.comment,
        }
    )
    return row


def _match_deals(deals: Iterable[_Deal]) -> ImportResult:
    open_lots: dict[str, list[_OpenLot]] = {}
    trades: list[dict[str, str]] = []
    warnings: list[str] = []
    epsilon = 1e-9

    for deal in deals:
        queue = open_lots.setdefault(deal.symbol, [])
        if deal.entry == "in":
            queue.append(_OpenLot(deal, deal.volume, deal.costs))
            continue

        remaining_close = deal.volume
        eligible = [lot for lot in queue if lot.deal.side != deal.side]
        for lot in eligible:
            if remaining_close <= epsilon:
                break
            matched = min(remaining_close, lot.remaining)
            open_ratio = matched / lot.remaining if lot.remaining else 0
            close_ratio = matched / deal.volume if deal.volume else 0
            open_costs = lot.remaining_costs * open_ratio
            close_result = (deal.profit + deal.costs) * close_ratio
            trades.append(
                _journal_row(lot.deal, deal, matched, open_costs + close_result)
            )
            lot.remaining -= matched
            lot.remaining_costs -= open_costs
            remaining_close -= matched
        queue[:] = [lot for lot in queue if lot.remaining > epsilon]
        if remaining_close > epsilon:
            warnings.append(
                f"Deal {deal.ticket}: {remaining_close:g} lots could not be matched"
            )
        if deal.entry == "inout" and remaining_close > epsilon:
            queue.append(
                _OpenLot(
                    deal=deal,
                    remaining=remaining_close,
                    remaining_costs=deal.costs * remaining_close / deal.volume,
                )
            )

    unmatched = sum(
        1
        for queue in open_lots.values()
        for lot in queue
        if lot.remaining > epsilon
    )
    if unmatched:
        warnings.append(
            f"{unmatched} open position(s) were not imported as closed trades"
        )
    if not trades:
        raise MT5StatementError(
            "No completed trades could be matched in the MT5 report."
        )
    return ImportResult(trades=trades, warnings=warnings)


def parse_mt5_html(source: str | Path) -> ImportResult:
    """Parse an MT5 HTML report from a path or an HTML string."""
    if isinstance(source, Path):
        html = source.read_text(encoding="utf-8-sig", errors="replace")
    else:
        candidate = Path(source)
        if "<" not in source and candidate.is_file():
            html = candidate.read_text(encoding="utf-8-sig", errors="replace")
        else:
            html = source
    return _match_deals(_extract_deals(html))


def write_journal_csv(rows: Iterable[dict[str, str]], output: str | Path) -> Path:
    """Write journal-compatible rows to UTF-8 CSV."""
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=JOURNAL_HEADERS)
        writer.writeheader()
        for row in rows:
            writer.writerow({header: row.get(header, "") for header in JOURNAL_HEADERS})
    return path
