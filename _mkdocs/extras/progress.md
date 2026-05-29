# 🏆 Мой прогресс (трекер пути новичка)

!!! abstract "Как пользоваться этим трекером"
    Отмечай вехи по мере того, как реально их выполняешь — не торопись ради красивого прогресса.
    Данные хранятся **только в твоём браузере** (localStorage), никуда не отправляются.
    Каждый новый день обучения засчитывается в стрик — заходи хотя бы раз в сутки.

!!! warning "Образовательный материал, не финансовый совет"
    Трекер помогает организовать обучение. Выполнение всех вех **не гарантирует прибыль** на реальном счёте.

---

<style>
/* ── Progress tracker styles (self-contained) ── */
.ftk-progress-wrap {
  background: var(--md-code-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1.5rem 0;
}

/* ── Header stats bar ── */
.ftk-stats-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.ftk-stat-card {
  flex: 1 1 120px;
  background: var(--md-default-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 8px;
  padding: 0.8rem 1rem;
  text-align: center;
}

.ftk-stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--md-primary-fg-color);
  line-height: 1;
}

.ftk-stat-label {
  font-size: 0.75rem;
  color: var(--md-default-fg-color--light);
  margin-top: 0.25rem;
}

/* ── Progress bar ── */
.ftk-bar-wrap {
  margin-bottom: 1.5rem;
}

.ftk-bar-label {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 0.4rem;
  color: var(--md-default-fg-color);
}

.ftk-bar-track {
  width: 100%;
  height: 14px;
  background: var(--md-default-fg-color--lightest);
  border-radius: 99px;
  overflow: hidden;
}

.ftk-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #10b981);
  border-radius: 99px;
  transition: width 0.5s ease;
}

/* ── Milestones list ── */
.ftk-milestones {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin-bottom: 1.5rem;
}

.ftk-milestone {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  background: var(--md-default-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
  user-select: none;
}

.ftk-milestone:hover {
  border-color: var(--md-primary-fg-color);
}

.ftk-milestone.done {
  border-color: #22c55e;
  background: rgba(34, 197, 94, 0.07);
}

.ftk-milestone input[type="checkbox"] {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  margin-top: 2px;
  accent-color: #22c55e;
  cursor: pointer;
}

.ftk-milestone-body {
  flex: 1;
}

.ftk-milestone-title {
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--md-default-fg-color);
}

.ftk-milestone.done .ftk-milestone-title {
  text-decoration: line-through;
  color: var(--md-default-fg-color--light);
}

.ftk-milestone-hint {
  font-size: 0.8rem;
  color: var(--md-default-fg-color--light);
  margin-top: 0.2rem;
}

.ftk-milestone-badge {
  font-size: 1.4rem;
  flex-shrink: 0;
  filter: grayscale(1) opacity(0.35);
  transition: filter 0.3s;
}

.ftk-milestone.done .ftk-milestone-badge {
  filter: none;
}

/* ── Badges showcase ── */
.ftk-badges-title {
  font-weight: 700;
  font-size: 0.9rem;
  color: var(--md-default-fg-color--light);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.75rem;
}

.ftk-badges-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  margin-bottom: 1.5rem;
}

.ftk-badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem 0.75rem;
  border-radius: 99px;
  font-size: 0.82rem;
  font-weight: 600;
  background: var(--md-default-bg-color);
  border: 1.5px solid var(--md-default-fg-color--lightest);
  color: var(--md-default-fg-color--light);
  filter: grayscale(1) opacity(0.5);
  transition: all 0.3s;
}

.ftk-badge-pill.earned {
  border-color: #f59e0b;
  color: var(--md-default-fg-color);
  background: rgba(245, 158, 11, 0.1);
  filter: none;
}

/* ── Streak section ── */
.ftk-streak-block {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: var(--md-default-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 8px;
  padding: 0.9rem 1.1rem;
  margin-bottom: 1.5rem;
}

.ftk-streak-num {
  font-size: 2.4rem;
  font-weight: 700;
  color: #f59e0b;
  line-height: 1;
}

.ftk-streak-label {
  font-size: 0.82rem;
  color: var(--md-default-fg-color--light);
  margin-top: 0.1rem;
}

/* ── Buttons ── */
.ftk-btn-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  margin-top: 0.5rem;
}

.ftk-btn {
  padding: 0.55rem 1.1rem;
  font-size: 0.9rem;
  font-weight: 600;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: filter 0.2s;
}

.ftk-btn:hover { filter: brightness(1.1); }

.ftk-btn-primary {
  background: var(--md-primary-fg-color);
  color: var(--md-primary-bg-color);
}

.ftk-btn-danger {
  background: rgba(220, 38, 38, 0.12);
  color: #dc2626;
  border: 1px solid rgba(220, 38, 38, 0.35);
}

/* ── Toast ── */
#ftk-toast {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  background: #1e293b;
  color: #f1f5f9;
  padding: 0.7rem 1.2rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s;
  z-index: 9999;
  max-width: 280px;
}

#ftk-toast.show { opacity: 1; }
</style>

<div class="ftk-progress-wrap" id="ftk-wrap">

  <!-- Stats bar -->
  <div class="ftk-stats-bar">
    <div class="ftk-stat-card">
      <div class="ftk-stat-value" id="ftk-pct">0%</div>
      <div class="ftk-stat-label">Выполнено</div>
    </div>
    <div class="ftk-stat-card">
      <div class="ftk-stat-value" id="ftk-done-count">0</div>
      <div class="ftk-stat-label">Вех закрыто</div>
    </div>
    <div class="ftk-stat-card">
      <div class="ftk-stat-value" id="ftk-badges-count">0</div>
      <div class="ftk-stat-label">Бейджей</div>
    </div>
  </div>

  <!-- Progress bar -->
  <div class="ftk-bar-wrap">
    <div class="ftk-bar-label">
      <span>Путь новичка</span>
      <span id="ftk-bar-pct-txt">0 / 12</span>
    </div>
    <div class="ftk-bar-track">
      <div class="ftk-bar-fill" id="ftk-bar-fill" style="width:0%"></div>
    </div>
  </div>

  <!-- Streak -->
  <div class="ftk-streak-block">
    <div>
      <div class="ftk-streak-num" id="ftk-streak">0</div>
      <div class="ftk-streak-label">дней стрика</div>
    </div>
    <div>
      <div style="font-weight:600;font-size:0.95rem;">Стрик обучения</div>
      <div style="font-size:0.8rem;color:var(--md-default-fg-color--light);" id="ftk-streak-msg">Нажми «Отметить день», чтобы начать стрик.</div>
    </div>
    <div style="margin-left:auto">
      <button class="ftk-btn ftk-btn-primary" onclick="ftkMarkDay()">Отметить день</button>
    </div>
  </div>

  <!-- Milestones -->
  <div class="ftk-milestones" id="ftk-milestones"></div>

  <!-- Badges -->
  <div class="ftk-badges-title">Бейджи</div>
  <div class="ftk-badges-row" id="ftk-badges-row"></div>

  <!-- Reset -->
  <div class="ftk-btn-row">
    <button class="ftk-btn ftk-btn-danger" onclick="ftkConfirmReset()">Сбросить прогресс</button>
  </div>

</div>

<div id="ftk-toast"></div>

<script>
/* ── DATA ──────────────────────────────────────────────────── */
var FTK_MILESTONES = [
  {
    id: 'read-guide',
    title: 'Прочитал главный учебник (forex-guide.md)',
    hint: 'Уровень 1 — фундамент без которого всё остальное бесполезно.',
    badge: '📖',
    badgeName: 'Читатель'
  },
  {
    id: 'read-roadmap',
    title: 'Изучил дорожную карту и понял этапы пути',
    hint: 'Знаешь разницу между уровнями 0–6 и контрольными точками.',
    badge: '🗺️',
    badgeName: 'Навигатор'
  },
  {
    id: 'read-psychology',
    title: 'Прочитал раздел психологии (psychology.md)',
    hint: 'Главный враг — ты сам. Этот раздел читают дважды.',
    badge: '🧠',
    badgeName: 'Психолог'
  },
  {
    id: 'demo-account',
    title: 'Открыл демо-счёт у регулируемого брокера',
    hint: 'Реальная платформа, виртуальные деньги — единственный безопасный старт.',
    badge: '🖥️',
    badgeName: 'Практикант'
  },
  {
    id: 'week-no-real',
    title: 'Прожил неделю без реальных денег (только демо)',
    hint: 'Первые 7 дней — самый большой соблазн «попробовать по-быстрому». Если устоял — ты уже лучше 60% новичков.',
    badge: '🛡️',
    badgeName: 'Стойкость'
  },
  {
    id: 'checklist-10',
    title: 'Провёл 10 сделок строго по чек-листу (без исключений)',
    hint: 'Каждый вход — чек-лист перед глазами. Без исключений.',
    badge: '✅',
    badgeName: 'Дисциплина'
  },
  {
    id: 'calc-10',
    title: 'Посчитал лот калькулятором позиции 10 раз',
    hint: 'Открыл tools/position-calculator.md и использовал перед каждой сделкой.',
    badge: '🔢',
    badgeName: 'Математик'
  },
  {
    id: 'no-sl-zero',
    title: 'Ни одного входа без стоп-лосса за неделю',
    hint: 'SL выставляется до входа, не после. 7 дней без исключений.',
    badge: '🚧',
    badgeName: 'Риск-страж'
  },
  {
    id: 'journal-30',
    title: 'Записал 30 демо-сделок в торговый журнал',
    hint: '30 записей с причиной входа, SL, TP и итогом — это уже статистика.',
    badge: '📓',
    badgeName: 'Хроникёр'
  },
  {
    id: 'trading-plan',
    title: 'Заполнил и «подписал» Trading Plan',
    hint: 'extras/trading-plan-template.md — заполни полностью, не пропуская.',
    badge: '📋',
    badgeName: 'Планировщик'
  },
  {
    id: 'first-analysis',
    title: 'Сделал первый анализ своих сделок: нашёл 3 главные ошибки',
    hint: 'Уровень 4 — посмотрел на журнал, выписал повторяющиеся ошибки.',
    badge: '🔍',
    badgeName: 'Аналитик'
  },
  {
    id: 'three-months-demo',
    title: 'Провёл 3 месяца на демо без перехода на реал',
    hint: 'Минимум по дорожной карте перед первым реальным счётом.',
    badge: '🏅',
    badgeName: 'Терпеливый'
  }
];

var FTK_TOTAL = FTK_MILESTONES.length;

/* ── STORAGE HELPERS ────────────────────────────────────────── */
function ftkGet(key) {
  try { return localStorage.getItem('ftk-' + key); } catch(e) { return null; }
}
function ftkSet(key, val) {
  try { localStorage.setItem('ftk-' + key, val); } catch(e) {}
}
function ftkRemove(key) {
  try { localStorage.removeItem('ftk-' + key); } catch(e) {}
}

function ftkGetDone(id) {
  return ftkGet('progress-' + id) === '1';
}
function ftkSetDone(id, val) {
  if (val) ftkSet('progress-' + id, '1');
  else ftkRemove('progress-' + id);
}

/* ── STREAK ─────────────────────────────────────────────────── */
function ftkGetStreak() {
  return parseInt(ftkGet('progress-streak') || '0', 10);
}
function ftkGetLastDay() {
  return ftkGet('progress-lastday') || '';
}

function ftkMarkDay() {
  var today = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
  var last  = ftkGetLastDay();
  var streak = ftkGetStreak();

  if (last === today) {
    ftkShowToast('Сегодня уже отмечено. Возвращайся завтра!');
    return;
  }

  var yesterday = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
  if (last === yesterday) {
    streak = streak + 1;
  } else {
    streak = 1; // streak broken or first time
  }

  ftkSet('progress-streak', String(streak));
  ftkSet('progress-lastday', today);
  ftkRender();
  ftkShowToast('День отмечен! Стрик: ' + streak + ' ' + ftkDayWord(streak));
}

function ftkDayWord(n) {
  var mod10 = n % 10, mod100 = n % 100;
  if (mod10 === 1 && mod100 !== 11) return 'день';
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 10 || mod100 >= 20)) return 'дня';
  return 'дней';
}

/* ── RENDER ─────────────────────────────────────────────────── */
function ftkRender() {
  var done = 0;
  FTK_MILESTONES.forEach(function(m) {
    if (ftkGetDone(m.id)) done++;
  });

  var pct = Math.round((done / FTK_TOTAL) * 100);

  // Stats
  document.getElementById('ftk-pct').textContent = pct + '%';
  document.getElementById('ftk-done-count').textContent = done;

  // Bar
  document.getElementById('ftk-bar-fill').style.width = pct + '%';
  document.getElementById('ftk-bar-pct-txt').textContent = done + ' / ' + FTK_TOTAL;

  // Streak
  var streak = ftkGetStreak();
  var last   = ftkGetLastDay();
  document.getElementById('ftk-streak').textContent = streak;

  var today = new Date().toISOString().slice(0, 10);
  var streakMsg;
  if (last === today) {
    streakMsg = 'Сегодня уже отмечено. Отличная работа!';
  } else if (streak === 0) {
    streakMsg = 'Нажми «Отметить день», чтобы начать стрик.';
  } else {
    var yesterday = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
    if (last === yesterday) {
      streakMsg = 'Не забудь отметить сегодня, иначе стрик сгорит!';
    } else {
      streakMsg = 'Стрик прервался. Начни заново — нажми «Отметить день».';
    }
  }
  document.getElementById('ftk-streak-msg').textContent = streakMsg;

  // Milestones
  var container = document.getElementById('ftk-milestones');
  container.innerHTML = '';
  FTK_MILESTONES.forEach(function(m) {
    var checked = ftkGetDone(m.id);
    var row = document.createElement('div');
    row.className = 'ftk-milestone' + (checked ? ' done' : '');
    row.innerHTML =
      '<input type="checkbox"' + (checked ? ' checked' : '') + ' id="cb-' + m.id + '">' +
      '<div class="ftk-milestone-body">' +
        '<div class="ftk-milestone-title">' + m.title + '</div>' +
        '<div class="ftk-milestone-hint">' + m.hint + '</div>' +
      '</div>' +
      '<div class="ftk-milestone-badge">' + m.badge + '</div>';

    row.addEventListener('click', function(e) {
      // allow checkbox to handle its own click naturally
      if (e.target.tagName === 'INPUT') {
        ftkToggle(m.id, e.target.checked);
      } else {
        var cb = document.getElementById('cb-' + m.id);
        var newVal = !cb.checked;
        cb.checked = newVal;
        ftkToggle(m.id, newVal);
      }
    });
    container.appendChild(row);
  });

  // Badges
  var badgesEarned = 0;
  var badgesRow = document.getElementById('ftk-badges-row');
  badgesRow.innerHTML = '';
  FTK_MILESTONES.forEach(function(m) {
    var earned = ftkGetDone(m.id);
    if (earned) badgesEarned++;
    var pill = document.createElement('span');
    pill.className = 'ftk-badge-pill' + (earned ? ' earned' : '');
    pill.innerHTML = m.badge + ' ' + m.badgeName;
    badgesRow.appendChild(pill);
  });

  document.getElementById('ftk-badges-count').textContent = badgesEarned;
}

function ftkToggle(id, checked) {
  var wasDone = ftkGetDone(id);
  ftkSetDone(id, checked);
  ftkRender();
  if (checked && !wasDone) {
    var m = FTK_MILESTONES.find(function(x) { return x.id === id; });
    if (m) ftkShowToast('Получен бейдж: ' + m.badge + ' ' + m.badgeName + '!');
  }
}

/* ── RESET ──────────────────────────────────────────────────── */
function ftkConfirmReset() {
  if (!confirm('Сбросить весь прогресс и стрик? Это действие нельзя отменить.')) return;
  FTK_MILESTONES.forEach(function(m) { ftkRemove('progress-' + m.id); });
  ftkRemove('progress-streak');
  ftkRemove('progress-lastday');
  ftkRender();
  ftkShowToast('Прогресс сброшен. Начинаем заново!');
}

/* ── TOAST ──────────────────────────────────────────────────── */
var ftkToastTimer = null;
function ftkShowToast(msg) {
  var t = document.getElementById('ftk-toast');
  t.textContent = msg;
  t.classList.add('show');
  if (ftkToastTimer) clearTimeout(ftkToastTimer);
  ftkToastTimer = setTimeout(function() { t.classList.remove('show'); }, 3000);
}

/* ── BOOT ───────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', ftkRender);
</script>

---

## Что означают вехи

| Этап | Вехи трекера | По дорожной карте |
|---|---|---|
| Уровень 0–1 | Прочитал учебник, изучил дорожную карту | Подготовка + Основы |
| Уровень 2 | Психология, Trading Plan | Психология и риск |
| Уровень 2–3 | Демо-счёт, калькулятор, чек-лист | Первая стратегия |
| Уровень 3 | 30 сделок в журнале, неделя без SL-нарушений | Демо-практика |
| Уровень 4 | Первый анализ ошибок | Анализ и доработка |
| Уровень 5 | 3 месяца на демо | Готовность к реалу |

---

## Советы по использованию трекера

!!! tip "Не торопись с вехами"
    Отмечай веху только тогда, когда честно убеждён, что выполнил её. Трекер видишь только ты — обманывать себя бессмысленно.

!!! tip "Стрик важнее скорости"
    Один день занятий в день лучше, чем марафон раз в неделю. Стрик — это про регулярность, а не про объём.

!!! info "Данные хранятся в браузере"
    Если очистишь кэш браузера или перейдёшь в другой браузер — прогресс не перенесётся. Сохранять вручную не нужно: всё происходит автоматически при каждом изменении.

---

## Связанные страницы

- [Дорожная карта обучения](../roadmap.md) — полный маршрут с контрольными точками
- [Первые 100 дней](first-100-days.md) — план день за днём
- [Trading Plan](trading-plan-template.md) — заполни до начала демо-торговли
- [Психология трейдинга](psychology.md) — обязательно к прочтению
- [Калькулятор позиции](../tools/position-calculator.md) — без него нельзя входить в сделку
