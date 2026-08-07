# 🎯 Квиз: готов ли ты к реальной торговле?

!!! abstract "Как это работает"
    18 вопросов по основам форекса, риск-менеджменту и психологии. После каждого
    ответа — короткое объяснение, **почему** так. В конце получишь процент и вердикт.
    Лучший результат сохраняется в браузере.

    **Это не экзамен на «гения рынка».** Это проверка, что ты усвоил то, что
    отделяет выживших новичков от тех, кто сливает депозит в первый месяц.

!!! warning "Образовательный материал — не финансовый совет"
    Правильные ответы отражают принципы управления риском, а не гарантию прибыли.
    Торговля на форекс сопряжена с высоким риском потерь.

---

<div class="quiz-widget calc-widget">
  <div id="quiz-start">
    <p class="quiz-best" id="quiz-best"></p>
    <button class="calc-button" onclick="quizStart()">▶ Начать квиз (18 вопросов)</button>
  </div>

  <div id="quiz-play" style="display:none">
    <div class="quiz-progress">
      <span id="quiz-counter"></span>
      <span id="quiz-score"></span>
    </div>
    <div class="quiz-bar-track"><div class="quiz-bar-fill" id="quiz-bar"></div></div>
    <h3 class="quiz-question" id="quiz-question"></h3>
    <div class="quiz-options" id="quiz-options"></div>
    <div class="quiz-explain" id="quiz-explain" style="display:none"></div>
    <button class="calc-button" id="quiz-next" style="display:none" onclick="quizNext()">Дальше →</button>
  </div>

  <div id="quiz-result" style="display:none"></div>
</div>

<script>
const QUIZ = [
  {
    q: "Какой риск на одну сделку максимально допустим для новичка?",
    options: ["0.5–1% депозита", "5–10% депозита", "Весь свободный остаток", "Зависит от уверенности в сделке"],
    correct: 0,
    explain: "Новичку — 0.5–1% на сделку. При 1% риска даже 10 убытков подряд заберут лишь ~10% депозита, и счёт переживёт серию неудач. 5–10% убивают депозит за одну плохую неделю."
  },
  {
    q: "Что обязательно выставить ПЕРЕД входом в сделку?",
    options: ["Take Profit побольше", "Стоп-лосс (Stop Loss)", "Кредитное плечо 1:500", "Уведомления в Telegram"],
    correct: 1,
    explain: "Стоп-лосс — это заранее принятое решение, где ты признаёшь, что ошибся. Без него один разворот рынка может обнулить счёт. Стоп ставится ДО входа, а не «по ситуации»."
  },
  {
    q: "Сколько минимум стоит торговать на демо перед реальными деньгами?",
    options: ["Пару дней", "Неделю", "Минимум 3 месяца", "Демо — пустая трата времени"],
    correct: 2,
    explain: "Минимум 3 месяца стабильной торговли на демо с журналом. Демо учит механике платформы и дисциплине без потери денег. Спешка с реалом — самая частая ошибка."
  },
  {
    q: "Win Rate 45%, RR (риск-награда) 1:2. Стратегия в долгосроке…",
    options: ["Убыточна — мало побед", "Прибыльна по математике", "Нейтральна", "Зависит от везения"],
    correct: 1,
    explain: "EV = 0.45×2 − 0.55×1 = +0.35R на сделку. При RR 1:2 достаточно выигрывать ~34% сделок, чтобы быть в плюсе. Win Rate сам по себе ничего не значит без RR."
  },
  {
    q: "Брокер обещает «гарантированную прибыль 30% в месяц». Это…",
    options: ["Отличная возможность", "Признак мошенничества", "Норма для форекса", "Только для VIP-клиентов"],
    correct: 1,
    explain: "Гарантированной прибыли на рынке не существует. 74–89% розничных трейдеров теряют деньги. Любая «гарантия дохода» — красный флаг мошенничества."
  },
  {
    q: "Зачем нужно большое кредитное плечо (1:500)?",
    options: ["Чтобы больше зарабатывать", "Оно опасно — усиливает и убытки", "Это обязательно для торговли", "Снижает риск"],
    correct: 1,
    explain: "Плечо усиливает И прибыль, И убытки. Риском управляет размер позиции и стоп, а не плечо. Большое плечо лишь позволяет открыть позицию больше, чем стоит депозит, — и быстрее его потерять."
  },
  {
    q: "Что делать, если цена почти дошла до стопа, но «вот-вот развернётся»?",
    options: ["Отодвинуть стоп подальше", "Ничего — стоп есть стоп", "Долить позицию (усреднить)", "Снять стоп вручную"],
    correct: 1,
    explain: "Двигать стоп против себя — путь к большому убытку. Стоп — это твоё заранее принятое правило. «Вот-вот развернётся» — это надежда, а не анализ."
  },
  {
    q: "Главный смысл торгового журнала?",
    options: ["Хвастаться прибылью", "Найти свои повторяющиеся ошибки", "Требование брокера", "Считать налоги"],
    correct: 1,
    explain: "Журнал показывает паттерны: в какое время, на каких парах, в каком настроении ты теряешь деньги. Без журнала ты повторяешь одни ошибки и не видишь этого."
  },
  {
    q: "Ты потерял 3 сделки подряд и хочешь «отыграться» большой позицией. Это…",
    options: ["Разумный план", "Тилт — стоп-сигнал", "Нормальный риск-менеджмент", "Стратегия мартингейл, она работает"],
    correct: 1,
    explain: "Желание отыграться (revenge trading) на тилте сливает депозиты. После серии убытков правильно — уменьшить размер или сделать паузу, а не увеличивать ставку."
  },
  {
    q: "Депозит просел на 50%. Сколько нужно заработать, чтобы вернуться к началу?",
    options: ["50%", "75%", "100%", "25%"],
    correct: 2,
    explain: "Математика просадки безжалостна: −50% требует +100% для восстановления. Поэтому защита капитала важнее погони за прибылью — большие просадки почти невозможно отыграть."
  },
  {
    q: "Перед важной новостью (NFP, заседание ФРС) спред расширяется и цена скачет. Новичку лучше…",
    options: ["Войти на всю котлету", "Воздержаться от входа", "Снять стоп-лоссы", "Увеличить плечо"],
    correct: 1,
    explain: "В моменты выхода новостей резкие движения и проскальзывание выбивают стопы по худшей цене. Новичку безопаснее не торговать за несколько минут до и после важных новостей."
  },
  {
    q: "Как выбрать брокера?",
    options: ["По размеру бонуса за депозит", "По наличию лицензии регулятора (FCA, CySEC, ASIC)", "По красивой рекламе", "По обещанному плечу 1:1000"],
    correct: 1,
    explain: "Главное — регулирование. Лицензия FCA/CySEC/ASIC означает сегрегацию средств клиентов и надзор. Бонусы и огромное плечо — маркетинг, часто у нерегулируемых контор."
  },
  {
    q: "Депозит $1000, риск 1%, стоп 25 пипсов, EUR/USD ($10/пипс за лот). Размер позиции?",
    options: ["0.04 лота", "0.4 лота", "1 лот", "0.004 лота"],
    correct: 0,
    explain: "Риск = $10. Лот = 10 / (25 × 10) = 0.04. Сначала считаешь допустимый риск в деньгах, потом — размер позиции от стопа. Никогда наоборот."
  },
  {
    q: "Что такое R (1R) в риск-менеджменте?",
    options: ["Размер прибыли", "Величина твоего риска на сделку (расстояние до стопа)", "Кредитное плечо", "Размер спреда"],
    correct: 1,
    explain: "1R — единица риска, твой стоп-лосс в деньгах. Прибыль удобно мерить в R: +2R значит «взял вдвое больше, чем рисковал». Это делает сделки сравнимыми независимо от размера."
  },
  {
    q: "Результат бэктеста на истории показал +200%. Это значит…",
    options: ["На реале будет так же", "Прошлое не гарантирует будущее, реал обычно хуже", "Можно сразу на реал", "Стратегия идеальна"],
    correct: 1,
    explain: "Бэктест не учитывает психологию, проскальзывание, изменение рынка и риск переподгонки (overfitting). Реальный результат почти всегда хуже. Бэктест — фильтр плохих идей, а не обещание прибыли."
  },
  {
    q: "Можно ли торговать на деньги, отложенные на аренду/еду?",
    options: ["Да, если уверен в сделке", "Категорически нет", "Только половиной", "Если плечо небольшое"],
    correct: 1,
    explain: "Торгуй только теми деньгами, потерю которых переживёшь без последствий для жизни. Деньги «на жизнь» создают эмоциональное давление, которое разрушает дисциплину."
  },
  {
    q: "Прибыльная сделка пошла в плюс. Когда сдвинуть стоп в безубыток (BE)?",
    options: ["Сразу при входе", "Когда цена прошла разумное расстояние в твою сторону", "Никогда не двигать", "Когда станет страшно"],
    correct: 1,
    explain: "Перенос в безубыток после прохождения значимого уровня защищает прибыль и снимает риск. Но слишком ранний BE (на старте) выбивает из нормальных колебаний цены."
  },
  {
    q: "Главная причина, по которой новички теряют деньги, — это…",
    options: ["Плохие индикаторы", "Отсутствие дисциплины и риск-менеджмента", "Маленький депозит", "Неправильный брокер"],
    correct: 1,
    explain: "Не индикаторы и не «секретная стратегия». Сливают из-за нарушения собственных правил: большой риск, отсутствие стопа, отыгрыш, торговля на эмоциях. Дисциплина важнее любой стратегии."
  }
];

let qDeck = [], qIdx = 0, qScore = 0, qAnswered = false;

function shuffle(list) {
  const a = [...list];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function showBest() {
  const best = localStorage.getItem("forex_quiz_best");
  const el = document.getElementById("quiz-best");
  el.textContent = best ? `🏆 Твой лучший результат: ${best}%` : "Ещё не проходил — попробуй!";
}

function quizStart() {
  // Перемешиваем и вопросы, и варианты: раньше правильный ответ почти всегда
  // стоял вторым, и квиз проходился вслепую на 78%.
  qDeck = shuffle(QUIZ).map((item) => {
    const right = item.options[item.correct];
    const options = shuffle(item.options);
    return { ...item, options, correct: options.indexOf(right) };
  });
  qIdx = 0; qScore = 0;
  document.getElementById("quiz-start").style.display = "none";
  document.getElementById("quiz-result").style.display = "none";
  document.getElementById("quiz-play").style.display = "block";
  renderQuestion();
}

function renderQuestion() {
  qAnswered = false;
  const item = qDeck[qIdx];
  document.getElementById("quiz-counter").textContent = `Вопрос ${qIdx + 1} из ${QUIZ.length}`;
  document.getElementById("quiz-score").textContent = `Очки: ${qScore}`;
  document.getElementById("quiz-bar").style.width = `${(qIdx / QUIZ.length) * 100}%`;
  document.getElementById("quiz-question").textContent = item.q;
  document.getElementById("quiz-explain").style.display = "none";
  document.getElementById("quiz-next").style.display = "none";

  const box = document.getElementById("quiz-options");
  box.innerHTML = "";
  item.options.forEach((opt, i) => {
    const btn = document.createElement("button");
    btn.className = "quiz-opt";
    btn.textContent = opt;
    btn.onclick = () => quizAnswer(i, btn);
    box.appendChild(btn);
  });
}

function quizAnswer(choice, btn) {
  if (qAnswered) return;
  qAnswered = true;
  const item = qDeck[qIdx];
  const buttons = document.querySelectorAll("#quiz-options .quiz-opt");
  buttons.forEach((b, i) => {
    b.disabled = true;
    if (i === item.correct) b.classList.add("quiz-correct");
    else if (i === choice) b.classList.add("quiz-wrong");
  });
  if (choice === item.correct) qScore++;
  document.getElementById("quiz-score").textContent = `Очки: ${qScore}`;

  const ex = document.getElementById("quiz-explain");
  const ok = choice === item.correct;
  ex.className = "quiz-explain " + (ok ? "quiz-ex-ok" : "quiz-ex-bad");
  ex.innerHTML = `<strong>${ok ? "✅ Верно" : "❌ Неверно"}.</strong> ${item.explain}`;
  ex.style.display = "block";
  document.getElementById("quiz-next").style.display = "inline-block";
  document.getElementById("quiz-next").textContent =
    qIdx + 1 < QUIZ.length ? "Дальше →" : "Показать результат";
}

function quizNext() {
  qIdx++;
  if (qIdx < QUIZ.length) renderQuestion();
  else quizFinish();
}

function quizFinish() {
  const pct = Math.round((qScore / QUIZ.length) * 100);
  const prevBest = parseInt(localStorage.getItem("forex_quiz_best") || "0", 10);
  const isRecord = pct > prevBest;
  if (isRecord) localStorage.setItem("forex_quiz_best", String(pct));

  let verdict, cls;
  if (pct >= 85) { verdict = "🟢 Отличная база. Ты понимаешь главное — управление риском и дисциплину."; cls = "calc-ok"; }
  else if (pct >= 65) { verdict = "🟡 Неплохо, но есть пробелы. Перечитай разделы, где ошибся, — особенно про риск."; cls = "calc-warn"; }
  else { verdict = "🔴 Рано думать о реальных деньгах. Вернись к учебнику: риск-менеджмент и психология."; cls = "calc-error"; }

  document.getElementById("quiz-play").style.display = "none";
  const res = document.getElementById("quiz-result");
  res.style.display = "block";
  res.innerHTML = `
    <div class="calc-result ${cls}">
      <h4>Результат: ${qScore} из ${QUIZ.length} (${pct}%)</h4>
      <p>${verdict}</p>
      ${isRecord ? "<p>🏆 <strong>Новый личный рекорд!</strong></p>" : `<p>Твой лучший результат: ${Math.max(pct, prevBest)}%</p>`}
      <ul>
        <li>Перечитай <a href="../forex-guide.md">главный учебник</a> по слабым темам.</li>
        <li>Раздел <a href="../extras/psychology.md">психологии</a> — если ошибся в вопросах про тилт и отыгрыш.</li>
        <li><a href="flashcards.md">Карточки</a> и <a href="winrate-rr-calculator.md">калькулятор WinRate × RR</a> — закрепить.</li>
      </ul>
      <button class="calc-button" onclick="quizStart()">↻ Пройти заново</button>
    </div>
  `;
}

window.addEventListener("DOMContentLoaded", showBest);
</script>

<style>
.quiz-progress {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--md-default-fg-color--light);
  margin-bottom: 0.4rem;
}
.quiz-bar-track {
  width: 100%;
  height: 8px;
  background: var(--md-default-fg-color--lightest);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 1.2rem;
}
.quiz-bar-fill {
  height: 100%;
  width: 0;
  background: var(--md-primary-fg-color);
  transition: width 0.3s ease;
}
.quiz-question {
  font-size: 1.15rem;
  margin: 0.3rem 0 1rem;
}
.quiz-options { display: flex; flex-direction: column; gap: 0.6rem; }
.quiz-opt {
  text-align: left;
  padding: 0.7rem 1rem;
  font-size: 0.95rem;
  border: 1px solid var(--md-default-fg-color--lighter);
  border-radius: 8px;
  background: var(--md-default-bg-color);
  color: var(--md-default-fg-color);
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s;
}
.quiz-opt:hover:not(:disabled) { border-color: var(--md-primary-fg-color); }
.quiz-opt:disabled { cursor: default; opacity: 0.95; }
.quiz-opt.quiz-correct {
  background: rgba(34, 197, 94, 0.15);
  border-color: #22c55e;
  font-weight: 600;
}
.quiz-opt.quiz-wrong {
  background: rgba(220, 38, 38, 0.12);
  border-color: #dc2626;
}
.quiz-explain {
  margin-top: 1rem;
  padding: 0.9rem 1.1rem;
  border-radius: 8px;
  font-size: 0.92rem;
  line-height: 1.5;
}
.quiz-ex-ok { background: rgba(34, 197, 94, 0.1); border-left: 4px solid #22c55e; }
.quiz-ex-bad { background: rgba(245, 158, 11, 0.1); border-left: 4px solid #f59e0b; }
.quiz-best { font-weight: 600; margin-bottom: 1rem; }
#quiz-result .calc-result ul { margin: 0.6rem 0; }
</style>

---

## 📚 Слабые места? Сюда

- [Главный учебник](../forex-guide.md) — вся теория с нуля
- [Психология трейдинга](../extras/psychology.md) — тилт, FOMO, отыгрыш
- [Калькулятор позиции](position-calculator.md) — как считать лот от риска
- [WinRate × RR](winrate-rr-calculator.md) — почему важна связка, а не один Win Rate
- [Тренажёр карточек](flashcards.md) — 105 терминов для запоминания
- [Риск разорения](risk-of-ruin.md) — Монте-Карло: шанс слить депозит
