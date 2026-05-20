//+------------------------------------------------------------------+
//|                                          EMA50Pullback.mq5       |
//|                  Учебный Expert Advisor для MetaTrader 5         |
//|                                                                  |
//| Стратегия: откат к EMA50 на H1 при тренде по EMA200              |
//|                                                                  |
//| ⚠️ ИСПОЛЬЗОВАТЬ ТОЛЬКО НА ДЕМО-СЧЁТЕ ⚠️                          |
//| Этот код — для обучения, не для реальной торговли.               |
//+------------------------------------------------------------------+
#property copyright "forex-trading project (educational)"
#property version   "1.00"
#property strict

#include <Trade\Trade.mqh>

// ===== Входные параметры =====
input double Risk_Percent      = 0.5;     // Риск на сделку, % депозита
input int    Ema_Fast_Period   = 50;      // Период быстрой EMA
input int    Ema_Slow_Period   = 200;     // Период медленной EMA
input int    Rsi_Period        = 14;      // RSI период
input double Rsi_Min_Long      = 40.0;    // RSI мин для long
input double Rsi_Max_Long      = 65.0;    // RSI макс для long
input double Risk_Reward       = 2.0;     // R:R соотношение
input int    Stop_Buffer_Pips  = 5;       // Буфер за свинг для стопа
input int    Magic_Number      = 20260520;

CTrade trade;
int ema_fast_handle, ema_slow_handle, rsi_handle;
double ema_fast_buf[], ema_slow_buf[], rsi_buf[];

//+------------------------------------------------------------------+
int OnInit()
{
    // Проверка демо-счёта
    if(AccountInfoInteger(ACCOUNT_TRADE_MODE) != ACCOUNT_TRADE_MODE_DEMO)
    {
        Print("⚠️ ВНИМАНИЕ: счёт НЕ демо. EA остановлен из соображений безопасности.");
        Print("   Если ты уверен — закомментируй эту проверку в OnInit().");
        return INIT_FAILED;
    }

    ema_fast_handle = iMA(_Symbol, PERIOD_H1, Ema_Fast_Period, 0, MODE_EMA, PRICE_CLOSE);
    ema_slow_handle = iMA(_Symbol, PERIOD_H1, Ema_Slow_Period, 0, MODE_EMA, PRICE_CLOSE);
    rsi_handle      = iRSI(_Symbol, PERIOD_H1, Rsi_Period, PRICE_CLOSE);

    if(ema_fast_handle == INVALID_HANDLE
       || ema_slow_handle == INVALID_HANDLE
       || rsi_handle == INVALID_HANDLE)
    {
        Print("Ошибка инициализации индикаторов");
        return INIT_FAILED;
    }

    ArraySetAsSeries(ema_fast_buf, true);
    ArraySetAsSeries(ema_slow_buf, true);
    ArraySetAsSeries(rsi_buf, true);

    trade.SetExpertMagicNumber(Magic_Number);
    Print("EA запущен. Демо-счёт подтверждён.");
    return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    IndicatorRelease(ema_fast_handle);
    IndicatorRelease(ema_slow_handle);
    IndicatorRelease(rsi_handle);
}

//+------------------------------------------------------------------+
void OnTick()
{
    // Только новая свеча H1
    static datetime last_bar = 0;
    datetime curr_bar = iTime(_Symbol, PERIOD_H1, 0);
    if(curr_bar == last_bar) return;
    last_bar = curr_bar;

    // Не торгуем при открытой позиции
    if(PositionsTotal() > 0) return;

    // Получаем последние значения индикаторов
    if(CopyBuffer(ema_fast_handle, 0, 0, 3, ema_fast_buf) < 3) return;
    if(CopyBuffer(ema_slow_handle, 0, 0, 3, ema_slow_buf) < 3) return;
    if(CopyBuffer(rsi_handle, 0, 0, 3, rsi_buf) < 3) return;

    double close_1 = iClose(_Symbol, PERIOD_H1, 1);
    double open_1  = iOpen(_Symbol, PERIOD_H1, 1);
    double low_1   = iLow(_Symbol, PERIOD_H1, 1);
    double high_1  = iHigh(_Symbol, PERIOD_H1, 1);
    double close_2 = iClose(_Symbol, PERIOD_H1, 2);
    double open_2  = iOpen(_Symbol, PERIOD_H1, 2);

    // ===== LONG =====
    bool trend_up = close_1 > ema_slow_buf[1];
    bool near_ema = MathAbs(close_1 - ema_fast_buf[1]) < (10 * _Point * 10);
    bool rsi_ok   = rsi_buf[1] >= Rsi_Min_Long && rsi_buf[1] <= Rsi_Max_Long;
    bool bullish_engulfing = (close_2 < open_2)
                           && (close_1 > open_1)
                           && (close_1 > open_2)
                           && (open_1 < close_2);
    bool hammer = (low_1 < open_1) && ((open_1 - low_1) > 2 * (close_1 - open_1))
                  && (close_1 > open_1);

    if(trend_up && near_ema && rsi_ok && (bullish_engulfing || hammer))
    {
        OpenTrade(POSITION_TYPE_BUY, low_1);
        return;
    }

    // ===== SHORT =====
    bool trend_dn = close_1 < ema_slow_buf[1];
    bool rsi_ok_s = rsi_buf[1] >= 35.0 && rsi_buf[1] <= 60.0;
    bool bearish_engulfing = (close_2 > open_2)
                           && (close_1 < open_1)
                           && (close_1 < open_2)
                           && (open_1 > close_2);
    bool shooting_star = (high_1 > open_1)
                       && ((high_1 - open_1) > 2 * (open_1 - close_1))
                       && (close_1 < open_1);

    if(trend_dn && near_ema && rsi_ok_s && (bearish_engulfing || shooting_star))
    {
        OpenTrade(POSITION_TYPE_SELL, high_1);
    }
}

//+------------------------------------------------------------------+
void OpenTrade(ENUM_POSITION_TYPE type, double swing_price)
{
    double price, sl, tp, point;
    point = _Point;
    int digits = (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS);

    if(type == POSITION_TYPE_BUY)
    {
        price = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
        sl = NormalizeDouble(swing_price - Stop_Buffer_Pips * point * 10, digits);
        double risk = price - sl;
        if(risk <= 0) return;
        tp = NormalizeDouble(price + Risk_Reward * risk, digits);
    }
    else
    {
        price = SymbolInfoDouble(_Symbol, SYMBOL_BID);
        sl = NormalizeDouble(swing_price + Stop_Buffer_Pips * point * 10, digits);
        double risk = sl - price;
        if(risk <= 0) return;
        tp = NormalizeDouble(price - Risk_Reward * risk, digits);
    }

    double lot = CalculateLot(MathAbs(price - sl));
    if(lot < SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN)) return;

    if(type == POSITION_TYPE_BUY)
        trade.Buy(lot, _Symbol, price, sl, tp, "EMA50Pullback");
    else
        trade.Sell(lot, _Symbol, price, sl, tp, "EMA50Pullback");
}

//+------------------------------------------------------------------+
double CalculateLot(double stop_distance)
{
    double balance = AccountInfoDouble(ACCOUNT_BALANCE);
    double risk_money = balance * Risk_Percent / 100.0;
    double tick_value = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
    double tick_size  = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);

    double pip_value_per_lot = tick_value * (stop_distance / tick_size);
    if(pip_value_per_lot <= 0) return 0;

    double lot = risk_money / pip_value_per_lot;

    // Округление до минимального шага
    double step = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
    double min_lot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
    double max_lot = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);

    lot = MathFloor(lot / step) * step;
    if(lot < min_lot) lot = min_lot;
    if(lot > max_lot) lot = max_lot;
    return NormalizeDouble(lot, 2);
}
//+------------------------------------------------------------------+
