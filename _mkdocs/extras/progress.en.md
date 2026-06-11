# 🏆 My Progress (Beginner's Journey Tracker)

!!! abstract "How to use this tracker"
    Mark milestones only as you genuinely complete them — don't rush for the sake of a pretty progress bar.
    Data is stored **in your browser only** (localStorage) and is never sent anywhere.
    Each new day of learning counts toward your streak — check in at least once a day.

!!! warning "Educational material, not financial advice"
    This tracker helps you organise your learning. Completing all milestones **does not guarantee profit** on a live account.

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
      <div class="ftk-stat-label">Completed</div>
    </div>
    <div class="ftk-stat-card">
      <div class="ftk-stat-value" id="ftk-done-count">0</div>
      <div class="ftk-stat-label">Milestones done</div>
    </div>
    <div class="ftk-stat-card">
      <div class="ftk-stat-value" id="ftk-badges-count">0</div>
      <div class="ftk-stat-label">Badges</div>
    </div>
  </div>

  <!-- Progress bar -->
  <div class="ftk-bar-wrap">
    <div class="ftk-bar-label">
      <span>Beginner's Journey</span>
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
      <div class="ftk-streak-label">day streak</div>
    </div>
    <div>
      <div style="font-weight:600;font-size:0.95rem;">Learning Streak</div>
      <div style="font-size:0.8rem;color:var(--md-default-fg-color--light);" id="ftk-streak-msg">Click "Mark Today" to start your streak.</div>
    </div>
    <div style="margin-left:auto">
      <button class="ftk-btn ftk-btn-primary" onclick="ftkMarkDay()">Mark Today</button>
    </div>
  </div>

  <!-- Milestones -->
  <div class="ftk-milestones" id="ftk-milestones"></div>

  <!-- Badges -->
  <div class="ftk-badges-title">Badges</div>
  <div class="ftk-badges-row" id="ftk-badges-row"></div>

  <!-- Reset -->
  <div class="ftk-btn-row">
    <button class="ftk-btn ftk-btn-danger" onclick="ftkConfirmReset()">Reset Progress</button>
  </div>

</div>

<div id="ftk-toast"></div>

<script>
/* ── DATA ──────────────────────────────────────────────────── */
var FTK_MILESTONES = [
  {
    id: 'read-guide',
    title: 'Read the main guide (forex-guide.md)',
    hint: 'Level 1 — the foundation without which everything else is useless.',
    badge: '📖',
    badgeName: 'Reader'
  },
  {
    id: 'read-roadmap',
    title: 'Studied the roadmap and understood the stages of the journey',
    hint: 'You know the difference between levels 0–6 and the checkpoints.',
    badge: '🗺️',
    badgeName: 'Navigator'
  },
  {
    id: 'read-psychology',
    title: 'Read the psychology section (psychology.md)',
    hint: 'Your biggest enemy is yourself. This section is worth reading twice.',
    badge: '🧠',
    badgeName: 'Psychologist'
  },
  {
    id: 'demo-account',
    title: 'Opened a demo account with a regulated broker',
    hint: 'Real platform, virtual money — the only safe way to start.',
    badge: '🖥️',
    badgeName: 'Practitioner'
  },
  {
    id: 'week-no-real',
    title: 'Spent one week without real money (demo only)',
    hint: 'The first 7 days bring the biggest temptation to "just try real quick". If you held back — you\'re already ahead of 60% of beginners.',
    badge: '🛡️',
    badgeName: 'Resilience'
  },
  {
    id: 'checklist-10',
    title: 'Executed 10 trades strictly following the checklist (no exceptions)',
    hint: 'Every entry — checklist in front of you. No exceptions.',
    badge: '✅',
    badgeName: 'Discipline'
  },
  {
    id: 'calc-10',
    title: 'Used the position-size calculator 10 times',
    hint: 'Opened tools/position-calculator.md and used it before every trade.',
    badge: '🔢',
    badgeName: 'Mathematician'
  },
  {
    id: 'no-sl-zero',
    title: 'Zero entries without a stop-loss for one full week',
    hint: 'SL is set before entry, not after. 7 days without exceptions.',
    badge: '🚧',
    badgeName: 'Risk Guard'
  },
  {
    id: 'journal-30',
    title: 'Logged 30 demo trades in the trading journal',
    hint: '30 records with entry reason, SL, TP, and outcome — that\'s already statistics.',
    badge: '📓',
    badgeName: 'Chronicler'
  },
  {
    id: 'trading-plan',
    title: 'Filled out and "signed" a Trading Plan',
    hint: 'extras/trading-plan-template.md — fill it out completely, skipping nothing.',
    badge: '📋',
    badgeName: 'Planner'
  },
  {
    id: 'first-analysis',
    title: 'Completed a first analysis of your trades: found 3 main mistakes',
    hint: 'Level 4 — reviewed the journal and identified recurring errors.',
    badge: '🔍',
    badgeName: 'Analyst'
  },
  {
    id: 'three-months-demo',
    title: 'Spent 3 months on demo without switching to live',
    hint: 'The minimum required by the roadmap before opening a first live account.',
    badge: '🏅',
    badgeName: 'Patient'
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
    ftkShowToast('Already marked today. Come back tomorrow!');
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
  ftkShowToast('Day marked! Streak: ' + streak + ' ' + ftkDayWord(streak));
}

function ftkDayWord(n) {
  return n === 1 ? 'day' : 'days';
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
    streakMsg = 'Already marked today. Great work!';
  } else if (streak === 0) {
    streakMsg = 'Click "Mark Today" to start your streak.';
  } else {
    var yesterday = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
    if (last === yesterday) {
      streakMsg = 'Don\'t forget to mark today or your streak will reset!';
    } else {
      streakMsg = 'Streak broken. Start fresh — click "Mark Today".';
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
    if (m) ftkShowToast('Badge earned: ' + m.badge + ' ' + m.badgeName + '!');
  }
}

/* ── RESET ──────────────────────────────────────────────────── */
function ftkConfirmReset() {
  if (!confirm('Reset all progress and streak? This action cannot be undone.')) return;
  FTK_MILESTONES.forEach(function(m) { ftkRemove('progress-' + m.id); });
  ftkRemove('progress-streak');
  ftkRemove('progress-lastday');
  ftkRender();
  ftkShowToast('Progress reset. Starting fresh!');
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

## What the milestones mean

| Stage | Tracker milestones | On the roadmap |
|---|---|---|
| Level 0–1 | Read the guide, studied the roadmap | Preparation + Basics |
| Level 2 | Psychology, Trading Plan | Psychology and risk |
| Level 2–3 | Demo account, calculator, checklist | First strategy |
| Level 3 | 30 trades in the journal, one week without SL violations | Demo practice |
| Level 4 | First error analysis | Analysis and refinement |
| Level 5 | 3 months on demo | Readiness for live |

---

## Tips for using the tracker

!!! tip "Don't rush milestones"
    Mark a milestone only when you honestly believe you have completed it. Only you see this tracker — deceiving yourself is pointless.

!!! tip "Streak beats speed"
    One study session per day is better than a marathon once a week. The streak is about consistency, not volume.

!!! info "Data is stored in the browser"
    If you clear your browser cache or switch to a different browser, your progress will not transfer. No manual saving is needed: everything happens automatically with every change.

---

## Related pages

- [Learning Roadmap](../roadmap.md) — the full route with checkpoints
- [First 100 Days](first-100-days.md) — day-by-day plan
- [Trading Plan](trading-plan-template.md) — fill this out before starting demo trading
- [Trading Psychology](psychology.md) — required reading
- [Position Calculator](../tools/position-calculator.md) — never enter a trade without it
