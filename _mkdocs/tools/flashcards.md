# 🎴 Тренажёр карточек (форекс-термины)

!!! abstract "Как работает тренажёр"
    Перед тобой 105 карточек по форексу: термины, паттерны, психология.
    Нажимай **«Показать ответ»**, потом честно оцени — «Знал» или «Не знал».
    Программа запоминает твой прогресс в браузере и показывает сложные карточки чаще.

    **Цель:** дойти до 105/105 выученных карточек (≥3 правильных подряд).

!!! warning "Образовательный материал — не финансовый совет"
    Все термины предоставлены в учебных целях. Торговля на форекс сопряжена с высоким риском.

---

<style>
/* Flashcard widget — самодостаточные стили */
.ftk-widget {
  background: var(--md-code-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1.5rem 0;
}

/* Progress bar */
.ftk-progress-wrap {
  margin-bottom: 1.2rem;
}
.ftk-progress-label {
  display: flex;
  justify-content: space-between;
  font-size: 0.88rem;
  font-weight: 600;
  margin-bottom: 0.35rem;
  color: var(--md-default-fg-color--light);
}
.ftk-progress-track {
  width: 100%;
  height: 10px;
  background: var(--md-default-fg-color--lightest);
  border-radius: 99px;
  overflow: hidden;
}
.ftk-progress-bar {
  height: 100%;
  background: #22c55e;
  border-radius: 99px;
  transition: width 0.4s ease;
}

/* Stats row */
.ftk-stats {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1.2rem;
}
.ftk-stat {
  flex: 1 1 120px;
  background: var(--md-default-bg-color);
  border-radius: 8px;
  padding: 0.6rem 0.9rem;
  text-align: center;
  border: 1px solid var(--md-default-fg-color--lightest);
}
.ftk-stat-num {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--md-primary-fg-color);
  font-family: var(--md-code-font-family);
}
.ftk-stat-lbl {
  font-size: 0.75rem;
  color: var(--md-default-fg-color--light);
  margin-top: 0.15rem;
}

/* Filter row */
.ftk-filter-row {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  margin-bottom: 1.2rem;
  flex-wrap: wrap;
}
.ftk-filter-row label {
  font-size: 0.88rem;
  font-weight: 600;
}
.ftk-filter-row select {
  padding: 0.4rem 0.7rem;
  font-size: 0.9rem;
  border: 1px solid var(--md-default-fg-color--lighter);
  border-radius: 6px;
  background: var(--md-default-bg-color);
  color: var(--md-default-fg-color);
  font-family: inherit;
  cursor: pointer;
}
.ftk-filter-row select:focus {
  outline: 2px solid var(--md-primary-fg-color);
}

/* Card */
.ftk-card-area {
  perspective: 800px;
  margin-bottom: 1.2rem;
  min-height: 180px;
}
.ftk-card {
  position: relative;
  width: 100%;
  min-height: 180px;
  transform-style: preserve-3d;
  transition: transform 0.45s cubic-bezier(.4,0,.2,1);
  cursor: default;
}
.ftk-card.flipped {
  transform: rotateY(180deg);
}
.ftk-card-face {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: var(--md-default-bg-color);
  border-radius: 10px;
  border: 2px solid var(--md-primary-fg-color);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
}
.ftk-card-face.ftk-back {
  transform: rotateY(180deg);
  border-color: #22c55e;
}
.ftk-card-tag {
  font-size: 0.72rem;
  color: var(--md-default-fg-color--light);
  background: var(--md-code-bg-color);
  padding: 0.15rem 0.5rem;
  border-radius: 99px;
  margin-bottom: 0.7rem;
  font-family: var(--md-code-font-family);
}
.ftk-card-term {
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--md-default-fg-color);
  line-height: 1.2;
}
.ftk-card-hint {
  margin-top: 0.6rem;
  font-size: 0.8rem;
  color: var(--md-default-fg-color--light);
}
.ftk-card-def {
  font-size: 1.05rem;
  line-height: 1.55;
  color: var(--md-default-fg-color);
}
.ftk-card-repeats {
  margin-top: 0.6rem;
  font-size: 0.78rem;
  color: var(--md-default-fg-color--light);
}

/* Buttons */
.ftk-btn-row {
  display: flex;
  gap: 0.7rem;
  flex-wrap: wrap;
  margin-bottom: 0.8rem;
}
.ftk-btn {
  flex: 1 1 130px;
  padding: 0.7rem 1.2rem;
  font-size: 0.95rem;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: filter 0.15s;
  font-family: inherit;
}
.ftk-btn:hover { filter: brightness(1.1); }
.ftk-btn:disabled { opacity: 0.4; cursor: default; filter: none; }
.ftk-btn-show {
  background: var(--md-primary-fg-color);
  color: var(--md-primary-bg-color);
}
.ftk-btn-knew {
  background: #22c55e;
  color: #fff;
}
.ftk-btn-didnt {
  background: #ef4444;
  color: #fff;
}
.ftk-btn-reset {
  flex: none;
  padding: 0.5rem 1rem;
  font-size: 0.8rem;
  font-weight: 600;
  background: transparent;
  color: var(--md-default-fg-color--light);
  border: 1px solid var(--md-default-fg-color--lighter);
  border-radius: 6px;
  cursor: pointer;
  font-family: inherit;
}
.ftk-btn-reset:hover { color: #ef4444; border-color: #ef4444; }

/* No cards message */
.ftk-empty {
  text-align: center;
  padding: 2rem;
  color: var(--md-default-fg-color--light);
  font-size: 1rem;
}
</style>

<div class="ftk-widget" id="ftk-widget">

  <!-- Progress -->
  <div class="ftk-progress-wrap">
    <div class="ftk-progress-label">
      <span>Прогресс: <span id="ftk-learned-count">0</span> / <span id="ftk-total-count">105</span> выучено</span>
      <span id="ftk-pct">0%</span>
    </div>
    <div class="ftk-progress-track">
      <div class="ftk-progress-bar" id="ftk-progress-bar" style="width:0%"></div>
    </div>
  </div>

  <!-- Stats -->
  <div class="ftk-stats">
    <div class="ftk-stat">
      <div class="ftk-stat-num" id="ftk-streak">0</div>
      <div class="ftk-stat-lbl">дней подряд</div>
    </div>
    <div class="ftk-stat">
      <div class="ftk-stat-num" id="ftk-session-ok">0</div>
      <div class="ftk-stat-lbl">«Знал» за сессию</div>
    </div>
    <div class="ftk-stat">
      <div class="ftk-stat-num" id="ftk-session-fail">0</div>
      <div class="ftk-stat-lbl">«Не знал» за сессию</div>
    </div>
    <div class="ftk-stat">
      <div class="ftk-stat-num" id="ftk-remaining">105</div>
      <div class="ftk-stat-lbl">ещё не выучено</div>
    </div>
  </div>

  <!-- Filter -->
  <div class="ftk-filter-row">
    <label for="ftk-tag-select">Фильтр по теме:</label>
    <select id="ftk-tag-select">
      <option value="all">Все карточки (105)</option>
    </select>
    <button class="ftk-btn-reset" id="ftk-reset-btn" title="Сбросить прогресс по всем карточкам">Сбросить прогресс</button>
  </div>

  <!-- Card area -->
  <div class="ftk-card-area" id="ftk-card-area">
    <div class="ftk-card" id="ftk-card">
      <div class="ftk-card-face ftk-front" id="ftk-front">
        <div class="ftk-card-tag" id="ftk-card-tag">...</div>
        <div class="ftk-card-term" id="ftk-card-term">Загрузка...</div>
        <div class="ftk-card-hint">Нажми «Показать ответ»</div>
      </div>
      <div class="ftk-card-face ftk-back" id="ftk-back">
        <div class="ftk-card-tag" id="ftk-card-tag-back">...</div>
        <div class="ftk-card-def" id="ftk-card-def">...</div>
        <div class="ftk-card-repeats" id="ftk-card-repeats"></div>
      </div>
    </div>
  </div>

  <!-- Buttons -->
  <div class="ftk-btn-row" id="ftk-btn-row">
    <button class="ftk-btn ftk-btn-show" id="ftk-show-btn">Показать ответ</button>
    <button class="ftk-btn ftk-btn-knew" id="ftk-knew-btn" disabled>Знал ✓</button>
    <button class="ftk-btn ftk-btn-didnt" id="ftk-didnt-btn" disabled>Не знал ✗</button>
  </div>

  <div class="ftk-empty" id="ftk-empty" style="display:none">
    Все карточки по этой теме выучены! Выбери другую тему или сбрось прогресс.
  </div>

</div>

<script>
(function () {
  /* ─────────── данные карточек ─────────── */
  var CARDS = [
    {front:"Pip",back:"Стандартная единица изменения цены. Обычно 4-й знак после запятой. Для пар с JPY — 2-й знак.",tags:["forex","basic"]},
    {front:"Lot",back:"Единица объёма позиции. 1 стандартный лот = 100 000 базовой валюты. Микро-лот = 0.01.",tags:["forex","basic"]},
    {front:"Spread",back:"Разница между Ask и Bid. Плата брокеру за каждую сделку.",tags:["forex","basic"]},
    {front:"Bid",back:"Цена, по которой брокер ПОКУПАЕТ у тебя валюту (по которой ты продаёшь). Ниже Ask.",tags:["forex","basic"]},
    {front:"Ask",back:"Цена, по которой брокер ПРОДАЁТ тебе валюту (по которой ты покупаешь). Выше Bid.",tags:["forex","basic"]},
    {front:"Leverage",back:"Кредитное плечо. 1:30 → депозит $100 даёт открыть позицию $3 000. Увеличивает И прибыль И убыток.",tags:["forex","basic"]},
    {front:"Margin",back:"Сумма, замороженная под открытую позицию (как залог).",tags:["forex","basic"]},
    {front:"Long",back:"Покупка. Ставка на рост цены.",tags:["forex","basic"]},
    {front:"Short",back:"Продажа. Ставка на падение цены.",tags:["forex","basic"]},
    {front:"Stop Loss (SL)",back:"Ордер, автоматически закрывающий позицию при заданном убытке. ОБЯЗАТЕЛЬНО в каждой сделке.",tags:["forex","risk"]},
    {front:"Take Profit (TP)",back:"Ордер, автоматически закрывающий позицию при достижении прибыли.",tags:["forex","risk"]},
    {front:"Margin Call",back:"Предупреждение брокера, что свободной маржи мало. Скоро принудительное закрытие.",tags:["forex","risk"]},
    {front:"Stop Out",back:"Принудительное закрытие позиций брокером при критическом уровне маржи (обычно 20-50%).",tags:["forex","risk"]},
    {front:"Major",back:"Самые ликвидные валютные пары с USD: EUR/USD, GBP/USD, USD/JPY, USD/CHF, AUD/USD, USD/CAD, NZD/USD.",tags:["forex","basic"]},
    {front:"Cross",back:"Валютная пара без USD: EUR/GBP, EUR/JPY, GBP/JPY.",tags:["forex","basic"]},
    {front:"Exotic",back:"Пары с валютой развивающейся страны: USD/TRY, USD/ZAR. ОПАСНО для новичков.",tags:["forex","basic"]},
    {front:"Swap",back:"Комиссия за перенос позиции через ночь. Может быть положительной и отрицательной.",tags:["forex","basic"]},
    {front:"Base currency",back:"Первая валюта в паре. В EUR/USD базовая = EUR.",tags:["forex","basic"]},
    {front:"Quote currency",back:"Вторая (котируемая) валюта в паре. В EUR/USD котируемая = USD.",tags:["forex","basic"]},
    {front:"OHLC",back:"Open, High, Low, Close — четыре цены, образующие свечу.",tags:["technical","candles"]},
    {front:"Bullish candle",back:"Бычья свеча: Close > Open. Зелёная или белая.",tags:["technical","candles"]},
    {front:"Bearish candle",back:"Медвежья свеча: Close < Open. Красная или чёрная.",tags:["technical","candles"]},
    {front:"Body",back:"Тело свечи — прямоугольник между Open и Close.",tags:["technical","candles"]},
    {front:"Wick / Shadow",back:"Тень свечи — линии сверху и снизу тела, до High и Low.",tags:["technical","candles"]},
    {front:"Hammer",back:"Молот. Маленькое тело сверху, длинная нижняя тень. Бычий разворотный паттерн в конце нисхождения.",tags:["technical","patterns"]},
    {front:"Shooting Star",back:"Падающая звезда. Маленькое тело снизу, длинная верхняя тень. Медвежий разворотный паттерн.",tags:["technical","patterns"]},
    {front:"Bullish Engulfing",back:"Бычье поглощение. Большая зелёная свеча, накрывшая тело предыдущей красной. Сигнал разворота вверх.",tags:["technical","patterns"]},
    {front:"Bearish Engulfing",back:"Медвежье поглощение. Большая красная свеча, накрывшая тело предыдущей зелёной. Сигнал разворота вниз.",tags:["technical","patterns"]},
    {front:"Doji",back:"Свеча с Open ≈ Close (маленькое тело). Неопределённость, бычий/медвежий контроль уравновесились.",tags:["technical","patterns"]},
    {front:"Pin Bar",back:"Свеча с длинной тенью и маленьким телом. Разворотный сигнал в направлении противоположном тени.",tags:["technical","patterns"]},
    {front:"Uptrend",back:"Восходящий тренд. Серия higher highs (HH) и higher lows (HL).",tags:["technical","trends"]},
    {front:"Downtrend",back:"Нисходящий тренд. Серия lower highs (LH) и lower lows (LL).",tags:["technical","trends"]},
    {front:"Range / Flat",back:"Боковик / флэт. Цена движется в горизонтальном коридоре.",tags:["technical","trends"]},
    {front:"Support",back:"Поддержка. Уровень, от которого цена отскакивала вверх.",tags:["technical","levels"]},
    {front:"Resistance",back:"Сопротивление. Уровень, от которого цена отскакивала вниз.",tags:["technical","levels"]},
    {front:"Breakout",back:"Пробой уровня поддержки или сопротивления.",tags:["technical","levels"]},
    {front:"Retest",back:"Возврат цены к пробитому уровню для подтверждения.",tags:["technical","levels"]},
    {front:"Pullback / Retracement",back:"Откат. Временное движение против основного тренда.",tags:["technical","trends"]},
    {front:"EMA",back:"Exponential Moving Average. Экспоненциальное скользящее среднее. Последние свечи весят больше старых.",tags:["technical","indicators"]},
    {front:"SMA",back:"Simple Moving Average. Простое среднее цен закрытия за N периодов.",tags:["technical","indicators"]},
    {front:"EMA 200",back:"Главный фильтр направления: цена выше EMA200 = только long, ниже = только short.",tags:["technical","indicators"]},
    {front:"RSI",back:"Relative Strength Index. Осциллятор 0-100. >70 = перекупленность, <30 = перепроданность.",tags:["technical","indicators"]},
    {front:"MACD",back:"Индикатор тренда + моментума. MACD = EMA(12) − EMA(26). Сигналы: пересечения, дивергенция.",tags:["technical","indicators"]},
    {front:"Bollinger Bands",back:"Полосы Боллинджера. Средняя + 2 стандартных отклонения. Цена 95% времени между полосами.",tags:["technical","indicators"]},
    {front:"ATR",back:"Average True Range. Средний размер свечи. Помогает выставлять стопы.",tags:["technical","indicators"]},
    {front:"Divergence",back:"Расхождение цены и индикатора: цена делает новый экстремум, индикатор — нет. Сигнал ослабления.",tags:["technical","patterns"]},
    {front:"Head and Shoulders",back:"Голова и плечи. Разворотный паттерн вершины: левое плечо → голова (выше) → правое плечо.",tags:["technical","patterns"]},
    {front:"Double Top",back:"Двойная вершина. Цена дважды не пробивает уровень, потом разворачивается вниз.",tags:["technical","patterns"]},
    {front:"Triangle",back:"Треугольник. Восходящий = чаще пробой вверх. Нисходящий = чаще вниз. Симметричный = непредсказуемо.",tags:["technical","patterns"]},
    {front:"Flag",back:"Флаг. Паттерн продолжения тренда: сильный импульс + короткая консолидация.",tags:["technical","patterns"]},
    {front:"Fibonacci",back:"Уровни отката: 23.6%, 38.2%, 50%, 61.8%, 78.6%. Используются как зоны входа на откате.",tags:["technical","levels"]},
    {front:"Risk Reward (R:R)",back:"Соотношение риска к прибыли. R:R 1:2 = на $1 риска целишься $2 прибыли. Минимум для новичка: 1:2.",tags:["risk","basic"]},
    {front:"Win Rate",back:"Процент прибыльных сделок. При R:R 1:2 хорошо ≥ 40%.",tags:["risk","metrics"]},
    {front:"Profit Factor",back:"Сумма прибылей / Сумма убытков. Хорошо ≥ 1.5.",tags:["risk","metrics"]},
    {front:"Expectancy",back:"Ожидаемый результат одной сделки: (WR × Avg Win) − (LR × Avg Loss). Должен быть > 0.",tags:["risk","metrics"]},
    {front:"Drawdown",back:"Просадка. Отклонение баланса от максимума.",tags:["risk","metrics"]},
    {front:"Max Drawdown",back:"Максимальная просадка за период. < 15% депозита = хорошо.",tags:["risk","metrics"]},
    {front:"R (Risk Unit)",back:"Единица твоего риска в одной сделке. Если рискнул $5 — это 1R. +2R = +$10.",tags:["risk","metrics"]},
    {front:"Equity",back:"Текущий баланс счёта + плавающий результат открытых сделок.",tags:["risk","metrics"]},
    {front:"Equity Curve",back:"График изменения эквити по времени. Главный визуальный показатель стратегии.",tags:["risk","metrics"]},
    {front:"1% Rule",back:"Правило: риск на одну сделку ≤ 1% депозита. Для новичка лучше 0.5%.",tags:["risk","management"]},
    {front:"Tilt",back:"Тильт. Психологическое состояние после убытка: гнев, желание отыграться. Главный убийца депозитов.",tags:["psychology","basic"]},
    {front:"FOMO",back:"Fear of Missing Out. Страх упустить движение. Заставляет входить без сигнала.",tags:["psychology","basic"]},
    {front:"Averaging Down",back:"Усреднение убыточной позиции в надежде на разворот. ОПАСНЫЙ приём, новичкам запрещено.",tags:["psychology","management"]},
    {front:"Demo Account",back:"Счёт с виртуальными деньгами на реальных котировках. Обязательный этап обучения 2-3 месяца.",tags:["basic","broker"]},
    {front:"Live Account",back:"Реальный счёт с настоящими деньгами. Переход только после стабильного плюса на демо.",tags:["basic","broker"]},
    {front:"Cent Account",back:"Счёт с балансом в центах. $10 = 1000 центов. Подходит для микро-тренировки.",tags:["basic","broker"]},
    {front:"ECN Account",back:"Прямой вывод ордеров на рынок. Узкий спред + комиссия. Для опытных.",tags:["basic","broker"]},
    {front:"Market Order",back:"Ордер на исполнение по текущей рыночной цене.",tags:["basic","orders"]},
    {front:"Limit Order",back:"Отложенный ордер на покупку ниже / продажу выше текущей цены.",tags:["basic","orders"]},
    {front:"Stop Order",back:"Отложенный ордер на покупку выше / продажу ниже текущей цены (для пробоя).",tags:["basic","orders"]},
    {front:"Slippage",back:"Проскальзывание. Реальная цена исполнения отличается от ожидаемой. Особенно на новостях.",tags:["basic","orders"]},
    {front:"Liquidity",back:"Ликвидность. Насколько легко купить/продать без существенного изменения цены.",tags:["basic","market"]},
    {front:"Volatility",back:"Волатильность. Амплитуда колебаний цены за период.",tags:["basic","market"]},
    {front:"NFP",back:"Non-Farm Payrolls. Занятость в США. Первая пятница месяца. Самая важная новость месяца.",tags:["fundamental","news"]},
    {front:"FOMC",back:"Federal Open Market Committee. Заседание ФРС по ставкам. 8 раз в год.",tags:["fundamental","news"]},
    {front:"CPI",back:"Consumer Price Index. Индекс потребительских цен (инфляция).",tags:["fundamental","news"]},
    {front:"GDP",back:"Gross Domestic Product. Валовый внутренний продукт страны.",tags:["fundamental","news"]},
    {front:"Interest Rate",back:"Процентная ставка ЦБ. Чем выше ставка — тем сильнее валюта (упрощённо).",tags:["fundamental","news"]},
    {front:"Carry Trade",back:"Стратегия: покупка валюты с высокой ставкой против валюты с низкой. Заработок на свопах.",tags:["fundamental","strategy"]},
    {front:"Hedging",back:"Хеджирование. Открытие противоположной позиции для защиты от риска.",tags:["risk","management"]},
    {front:"Diversification",back:"Диверсификация. Распределение риска по разным активам.",tags:["risk","management"]},
    {front:"Money Management (MM)",back:"Управление капиталом: размер позиции, риск, диверсификация.",tags:["risk","management"]},
    {front:"Trailing Stop",back:"Стоп, который двигается за ценой в прибыльную сторону, но не назад.",tags:["risk","orders"]},
    {front:"Break-even",back:"Безубыток. Закрытие сделки в ноль или перенос стопа на цену входа.",tags:["risk","orders"]},
    {front:"Scalping",back:"Скальпинг. Торговля на M1-M5 с маленькими прибылями. Стрессово, не для новичков.",tags:["style","trading"]},
    {front:"Day Trading",back:"Дневная торговля. Сделки закрываются в течение торгового дня.",tags:["style","trading"]},
    {front:"Swing Trading",back:"Свинг-трейдинг. Сделки от нескольких часов до нескольких дней.",tags:["style","trading"]},
    {front:"Position Trading",back:"Позиционная торговля. Сделки удерживаются недели-месяцы.",tags:["style","trading"]},
    {front:"Backtest",back:"Бэктест. Проверка стратегии на исторических данных.",tags:["strategy","testing"]},
    {front:"Forward Test",back:"Форвард-тест. Проверка стратегии на демо в реальном времени.",tags:["strategy","testing"]},
    {front:"Walk-Forward",back:"Walk-forward optimization. Подбор параметров на одной части истории, проверка на следующей.",tags:["strategy","testing"]},
    {front:"Overfitting",back:"Переподгонка. Стратегия слишком сильно подогнана под историю и не работает на новых данных.",tags:["strategy","testing"]},
    {front:"Expert Advisor (EA)",back:"Торговый советник для MT4/MT5. Автоматический бот.",tags:["technology","bots"]},
    {front:"MQL5",back:"Язык программирования для написания EA в MetaTrader 5.",tags:["technology","bots"]},
    {front:"API",back:"Программный интерфейс для подключения к брокеру (например, MetaTrader 5 Python API).",tags:["technology","bots"]},
    {front:"Spread Cost",back:"Стоимость спреда. На EUR/USD спред 1 пипс = $1 на каждый стандартный лот.",tags:["risk","costs"]},
    {front:"Pip Value",back:"Стоимость 1 пипса. На EUR/USD за 1 стандартный лот ≈ $10. За 0.01 лота ≈ $0.10.",tags:["basic","costs"]},
    {front:"Lot Size",back:"Размер позиции. Считается по формуле: (Депозит × Риск%) / (Стоп × Pip Value).",tags:["risk","management"]},
    {front:"Trading Session",back:"Торговая сессия. Лондонская (10:00-19:00 UTC+3), Американская (14:00-23:00 UTC+3).",tags:["basic","time"]},
    {front:"Asian Session",back:"Азиатская сессия (02:00-11:00 UTC+3). Низкая ликвидность. Лучше пропускать новичкам.",tags:["basic","time"]},
    {front:"Sniper Entry",back:"Снайперский вход. Терпеливое ожидание идеальной точки входа по правилам.",tags:["psychology","patience"]},
    {front:"Trading Plan",back:"Торговый план. Записанные правила: что, когда, как торговать.",tags:["psychology","discipline"]},
    {front:"Trading Journal",back:"Журнал сделок. Запись каждой сделки. Главный инструмент роста.",tags:["psychology","discipline"]}
  ];

  /* ─────────── константы ─────────── */
  var LEARNED_THRESHOLD = 3; // сколько раз подряд нужно ответить «Знал»

  /* ─────────── localStorage helpers ─────────── */
  function getState(idx) {
    /* returns {streak: number} — количество успешных повторов подряд */
    try {
      var raw = localStorage.getItem('ftk-flash-' + idx);
      if (raw) return JSON.parse(raw);
    } catch(e) {}
    return {streak: 0};
  }

  function setState(idx, obj) {
    try { localStorage.setItem('ftk-flash-' + idx, JSON.stringify(obj)); } catch(e) {}
  }

  function getSessionStats() {
    try {
      var raw = localStorage.getItem('ftk-flash-session');
      if (raw) return JSON.parse(raw);
    } catch(e) {}
    return {ok: 0, fail: 0};
  }

  function setSessionStats(obj) {
    try { localStorage.setItem('ftk-flash-session', JSON.stringify(obj)); } catch(e) {}
  }

  function getStreak() {
    var streak = 0;
    var lastDay = '';
    try {
      streak = parseInt(localStorage.getItem('ftk-flash-streak') || '0', 10);
      lastDay = localStorage.getItem('ftk-flash-lastday') || '';
    } catch(e) {}
    return {streak: streak, lastDay: lastDay};
  }

  function touchStreak() {
    var today = new Date().toISOString().slice(0, 10);
    var s = getStreak();
    if (s.lastDay === today) return; // уже отметились сегодня
    var yesterday = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
    var newStreak = (s.lastDay === yesterday) ? s.streak + 1 : 1;
    try {
      localStorage.setItem('ftk-flash-streak', String(newStreak));
      localStorage.setItem('ftk-flash-lastday', today);
    } catch(e) {}
  }

  /* ─────────── SM-2-подобный приоритет ─────────── */
  /*
    Алгоритм: каждой карточке сопоставляем «приоритет»:
      - streak=0 → самый высокий приоритет (не начато)
      - 1 ≤ streak < LEARNED_THRESHOLD → средний (в процессе)
      - streak ≥ LEARNED_THRESHOLD → низкий (выучено), но изредка повторяем
    Среди карточек одного уровня — случайный порядок.
    Отбираем карточки, соответствующие выбранному тегу/фильтру.
  */
  function pickNext(activeIndices, lastIdx) {
    if (activeIndices.length === 0) return -1;

    var buckets = [[], [], []]; // [не начато/сброшено, в процессе, выучено]
    activeIndices.forEach(function(i) {
      if (i === lastIdx) return; // не повторяем ту же карточку подряд
      var s = getState(i).streak;
      if (s <= 0) buckets[0].push(i);
      else if (s < LEARNED_THRESHOLD) buckets[1].push(i);
      else buckets[2].push(i);
    });

    // если есть хоть одна карточка в первых двух бакетах — берём оттуда
    var pool = buckets[0].length > 0 ? buckets[0]
             : buckets[1].length > 0 ? buckets[1]
             : buckets[2];

    // если все исключены из-за lastIdx — включаем lastIdx обратно
    if (pool.length === 0) pool = activeIndices;

    return pool[Math.floor(Math.random() * pool.length)];
  }

  /* ─────────── фильтр по тегам ─────────── */
  // Собираем уникальные теги
  var tagSet = {};
  var tagLabelMap = {
    'forex':        'Форекс: основы',
    'technical':    'Технический анализ',
    'risk':         'Риск-менеджмент',
    'psychology':   'Психология',
    'fundamental':  'Фундаментальный анализ',
    'basic':        'Базовые понятия',
    'strategy':     'Стратегия и тестирование',
    'style':        'Стиль торговли',
    'technology':   'Технологии (EA, API)',
    'candles':      'Свечной анализ',
    'patterns':     'Паттерны',
    'trends':       'Тренды',
    'levels':       'Уровни',
    'indicators':   'Индикаторы',
    'management':   'Управление капиталом',
    'metrics':      'Метрики',
    'orders':       'Ордера',
    'news':         'Новости (Fundamental)',
    'broker':       'Типы счетов',
    'bots':         'Боты и автоматизация',
    'costs':        'Расходы',
    'time':         'Торговые сессии',
    'testing':      'Тестирование стратегий',
    'discipline':   'Дисциплина',
    'patience':     'Терпение и вход'
  };

  CARDS.forEach(function(c) {
    c.tags.forEach(function(t) { tagSet[t] = true; });
  });

  var tagSelect = document.getElementById('ftk-tag-select');
  Object.keys(tagSet).sort().forEach(function(t) {
    var count = CARDS.filter(function(c){ return c.tags.indexOf(t) !== -1; }).length;
    var opt = document.createElement('option');
    opt.value = t;
    opt.textContent = (tagLabelMap[t] || t) + ' (' + count + ')';
    tagSelect.appendChild(opt);
  });

  /* ─────────── состояние виджета ─────────── */
  var currentFilter = 'all';
  var activeIndices = [];
  var currentIdx = -1;
  var isFlipped = false;
  var sessionOk = 0;
  var sessionFail = 0;

  /* ─────────── DOM-ссылки ─────────── */
  var elCard        = document.getElementById('ftk-card');
  var elFront       = document.getElementById('ftk-front');
  var elBack        = document.getElementById('ftk-back');
  var elCardTag     = document.getElementById('ftk-card-tag');
  var elCardTagBack = document.getElementById('ftk-card-tag-back');
  var elCardTerm    = document.getElementById('ftk-card-term');
  var elCardDef     = document.getElementById('ftk-card-def');
  var elCardRep     = document.getElementById('ftk-card-repeats');
  var elShowBtn     = document.getElementById('ftk-show-btn');
  var elKnewBtn     = document.getElementById('ftk-knew-btn');
  var elDidntBtn    = document.getElementById('ftk-didnt-btn');
  var elEmpty       = document.getElementById('ftk-empty');
  var elCardArea    = document.getElementById('ftk-card-area');
  var elLearnedCount= document.getElementById('ftk-learned-count');
  var elTotalCount  = document.getElementById('ftk-total-count');
  var elPct         = document.getElementById('ftk-pct');
  var elProgressBar = document.getElementById('ftk-progress-bar');
  var elStreakNum    = document.getElementById('ftk-streak');
  var elSessionOk   = document.getElementById('ftk-session-ok');
  var elSessionFail = document.getElementById('ftk-session-fail');
  var elRemaining   = document.getElementById('ftk-remaining');

  /* ─────────── вычислить активные индексы по фильтру ─────────── */
  function rebuildActive() {
    if (currentFilter === 'all') {
      activeIndices = CARDS.map(function(_, i){ return i; });
    } else {
      activeIndices = CARDS.reduce(function(acc, c, i){
        if (c.tags.indexOf(currentFilter) !== -1) acc.push(i);
        return acc;
      }, []);
    }
  }

  /* ─────────── обновить счётчики и прогресс ─────────── */
  function updateStats() {
    var learned = CARDS.filter(function(_, i){
      return getState(i).streak >= LEARNED_THRESHOLD;
    }).length;
    var total = CARDS.length;
    var pct = Math.round(learned / total * 100);

    elLearnedCount.textContent = learned;
    elTotalCount.textContent   = total;
    elPct.textContent          = pct + '%';
    elProgressBar.style.width  = pct + '%';

    var activeLearnedCount = activeIndices.filter(function(i){
      return getState(i).streak >= LEARNED_THRESHOLD;
    }).length;
    elRemaining.textContent = activeIndices.length - activeLearnedCount;

    var s = getStreak();
    elStreakNum.textContent = s.streak;
    elSessionOk.textContent   = sessionOk;
    elSessionFail.textContent = sessionFail;
  }

  /* ─────────── показать карточку ─────────── */
  function showCard(idx) {
    if (idx < 0) {
      // пустой результат (все выучены в этой теме)
      elCardArea.style.display = 'none';
      document.getElementById('ftk-btn-row').style.display = 'none';
      elEmpty.style.display = 'block';
      return;
    }
    elCardArea.style.display = '';
    document.getElementById('ftk-btn-row').style.display = '';
    elEmpty.style.display = 'none';

    var card = CARDS[idx];
    var tagLabel = card.tags.map(function(t){ return tagLabelMap[t] || t; }).join(' · ');
    var s = getState(idx);

    elCardTag.textContent     = tagLabel;
    elCardTagBack.textContent = tagLabel;
    elCardTerm.textContent    = card.front;
    elCardDef.textContent     = card.back;

    var streakTxt = s.streak >= LEARNED_THRESHOLD
      ? '✅ Выучено (' + s.streak + ' раз подряд)'
      : s.streak > 0
        ? '🔄 Повторений подряд: ' + s.streak + ' / ' + LEARNED_THRESHOLD
        : '🆕 Новая карточка';
    elCardRep.textContent = streakTxt;

    // убираем флип без анимации
    elCard.style.transition = 'none';
    elCard.classList.remove('flipped');
    void elCard.offsetWidth; // reflow
    elCard.style.transition = '';

    isFlipped = false;
    elShowBtn.disabled  = false;
    elKnewBtn.disabled  = true;
    elDidntBtn.disabled = true;
  }

  /* ─────────── события кнопок ─────────── */
  elShowBtn.addEventListener('click', function() {
    if (isFlipped) return;
    elCard.classList.add('flipped');
    isFlipped = true;
    elShowBtn.disabled  = true;
    elKnewBtn.disabled  = false;
    elDidntBtn.disabled = false;
    touchStreak(); // отметим день как активный
    updateStats();
  });

  elKnewBtn.addEventListener('click', function() {
    if (!isFlipped || currentIdx < 0) return;
    var s = getState(currentIdx);
    s.streak = (s.streak || 0) + 1;
    setState(currentIdx, s);
    sessionOk++;
    advance();
  });

  elDidntBtn.addEventListener('click', function() {
    if (!isFlipped || currentIdx < 0) return;
    setState(currentIdx, {streak: 0});
    sessionFail++;
    advance();
  });

  function advance() {
    updateStats();
    var next = pickNext(activeIndices, currentIdx);
    currentIdx = next;
    showCard(next);
  }

  /* ─────────── фильтр ─────────── */
  tagSelect.addEventListener('change', function() {
    currentFilter = tagSelect.value;
    rebuildActive();
    currentIdx = -1;
    advance();
  });

  /* ─────────── сброс прогресса ─────────── */
  document.getElementById('ftk-reset-btn').addEventListener('click', function() {
    if (!confirm('Сбросить весь прогресс карточек? Это удалит все результаты из браузера.')) return;
    for (var i = 0; i < CARDS.length; i++) {
      try { localStorage.removeItem('ftk-flash-' + i); } catch(e) {}
    }
    try {
      localStorage.removeItem('ftk-flash-streak');
      localStorage.removeItem('ftk-flash-lastday');
      localStorage.removeItem('ftk-flash-session');
    } catch(e) {}
    sessionOk   = 0;
    sessionFail = 0;
    currentIdx  = -1;
    rebuildActive();
    advance();
  });

  /* ─────────── инициализация ─────────── */
  rebuildActive();
  currentIdx = pickNext(activeIndices, -1);
  showCard(currentIdx);
  updateStats();

}());
</script>

---

## Как правильно заниматься

1. **Каждый день по 10-15 минут** — лучше, чем раз в неделю час.
2. **Будь честен**: нажимай «Знал» только если действительно вспомнил определение ДО переворота.
3. **Алгоритм сам расставит приоритеты**: карточки с нулевым стриком показываются чаще всего.
4. **Цель**: 105/105 карточек с 3+ правильными ответами подряд.

!!! tip "Следующий шаг после карточек"
    Когда знаешь все термины — переходи к [калькулятору WinRate × RR](winrate-rr-calculator.md), чтобы понять математику стратегии.

---

## Алгоритм интервального повторения (кратко)

Тренажёр использует упрощённую версию SM-2:

| Состояние карточки | Показывается |
|---|---|
| Никогда не отвечал / сброс | В первую очередь |
| 1-2 правильных подряд | Во вторую очередь |
| 3+ правильных подряд (выучена) | Редко, для закрепления |

Прогресс хранится в `localStorage` твоего браузера — он сохраняется между сессиями, но не синхронизируется между устройствами.

---

!!! info "Образовательный материал"
    Страница является частью учебника по форекс-трейдингу. Не является финансовым советом.
