# 🏆 Mening taraqqiyotim (yangi boshlovchi yo'li trekeri)

!!! abstract "Bu trekerdan qanday foydalanish"
    Bosqichlarni haqiqatan bajarganingizda belgilang — chiroyli ko'rinish uchun shoshilmang.
    Ma'lumotlar **faqat brauzeringizda** saqlanadi (localStorage), hech qayerga yuborilmaydi.
    Har yangi o'quv kuni strikka hisoblanadi — kuniga kamida bir marta kiring.

!!! warning "Ta'lim materiali, moliyaviy maslahat emas"
    Treker o'qishni tashkil etishga yordam beradi. Barcha bosqichlarni bajarish **real hisobda foyda kafolatlamaydi**.

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
      <div class="ftk-stat-label">Bajarildi</div>
    </div>
    <div class="ftk-stat-card">
      <div class="ftk-stat-value" id="ftk-done-count">0</div>
      <div class="ftk-stat-label">Bosqich yopildi</div>
    </div>
    <div class="ftk-stat-card">
      <div class="ftk-stat-value" id="ftk-badges-count">0</div>
      <div class="ftk-stat-label">Nishonlar</div>
    </div>
  </div>

  <!-- Progress bar -->
  <div class="ftk-bar-wrap">
    <div class="ftk-bar-label">
      <span>Yangi boshlovchi yo'li</span>
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
      <div class="ftk-streak-label">kun strik</div>
    </div>
    <div>
      <div style="font-weight:600;font-size:0.95rem;">O'quv strigi</div>
      <div style="font-size:0.8rem;color:var(--md-default-fg-color--light);" id="ftk-streak-msg">Strikni boshlash uchun «Kunni belgilash» tugmasini bosing.</div>
    </div>
    <div style="margin-left:auto">
      <button class="ftk-btn ftk-btn-primary" onclick="ftkMarkDay()">Kunni belgilash</button>
    </div>
  </div>

  <!-- Milestones -->
  <div class="ftk-milestones" id="ftk-milestones"></div>

  <!-- Badges -->
  <div class="ftk-badges-title">Nishonlar</div>
  <div class="ftk-badges-row" id="ftk-badges-row"></div>

  <!-- Reset -->
  <div class="ftk-btn-row">
    <button class="ftk-btn ftk-btn-danger" onclick="ftkConfirmReset()">Taraqqiyotni tiklash</button>
  </div>

</div>

<div id="ftk-toast"></div>

<script>
/* ── DATA ──────────────────────────────────────────────────── */
var FTK_MILESTONES = [
  {
    id: 'read-guide',
    title: 'Asosiy qo\'llanmani o\'qidim (forex-guide.md)',
    hint: '1-daraja — boshqa hamma narsa befoyda bo\'lgan poydevor.',
    badge: '📖',
    badgeName: 'O\'quvchi'
  },
  {
    id: 'read-roadmap',
    title: 'Yo\'l xaritasini o\'rganib, bosqichlarni tushundim',
    hint: '0–6-darajalar va nazorat nuqtalari o\'rtasidagi farqni bilaman.',
    badge: '🗺️',
    badgeName: 'Navigator'
  },
  {
    id: 'read-psychology',
    title: 'Psixologiya bo\'limini o\'qidim (psychology.md)',
    hint: 'Asosiy dushman — o\'zingiz. Bu bo\'limni ikki marta o\'qiydilar.',
    badge: '🧠',
    badgeName: 'Psixolog'
  },
  {
    id: 'demo-account',
    title: 'Litsenziyalangan brokerda demo-hisob ochdim',
    hint: 'Haqiqiy platforma, virtual pul — yagona xavfsiz boshlang\'ich.',
    badge: '🖥️',
    badgeName: 'Amaliyotchi'
  },
  {
    id: 'week-no-real',
    title: 'Bir haftani real pulsiz o\'tkazdim (faqat demo)',
    hint: 'Birinchi 7 kun — «tezda sinab ko\'rish» vasvasasi eng kuchli. Agar chidagan bo\'lsangiz — yangi boshlovchilarning 60% dan ko\'ragansiz.',
    badge: '🛡️',
    badgeName: 'Chidam'
  },
  {
    id: 'checklist-10',
    title: 'Cek-list bo\'yicha qat\'iy 10 ta savdo o\'tkazdim (istisnosiz)',
    hint: 'Har bir kirish — ko\'z oldida cek-list. Istisnosiz.',
    badge: '✅',
    badgeName: 'Intizom'
  },
  {
    id: 'calc-10',
    title: 'Pozitsiya kalkulyatori bilan 10 marta lot hisobladim',
    hint: 'tools/position-calculator.md ni ochdim va har savdo oldidan foydalandim.',
    badge: '🔢',
    badgeName: 'Matematik'
  },
  {
    id: 'no-sl-zero',
    title: 'Bir hafta ichida biror kirish stop-losssiz bo\'lmadi',
    hint: 'SL kirishdan oldin o\'rnatiladi, keyin emas. 7 kun istisnosiz.',
    badge: '🚧',
    badgeName: 'Risk-qo\'riqchi'
  },
  {
    id: 'journal-30',
    title: 'Savdo jurnalida 30 ta demo-savdo yozdim',
    hint: 'Kirish sababi, SL, TP va natija bilan 30 ta yozuv — bu allaqachon statistika.',
    badge: '📓',
    badgeName: 'Xronist'
  },
  {
    id: 'trading-plan',
    title: 'Trading Planni to\'ldirdim va «imzoladim»',
    hint: 'extras/trading-plan-template.md — to\'liq to\'ldiring, o\'tkazib yubormang.',
    badge: '📋',
    badgeName: 'Rejalashtiruvchi'
  },
  {
    id: 'first-analysis',
    title: 'Savdolarimni tahlil qildim: 3 ta asosiy xatoni topdim',
    hint: '4-daraja — jurnalga qaradim, takrorlanuvchi xatolarni yozdim.',
    badge: '🔍',
    badgeName: 'Tahlilchi'
  },
  {
    id: 'three-months-demo',
    title: 'Realga o\'tmasdan 3 oy demo savdo qildim',
    hint: 'Yo\'l xaritasidagi birinchi real hisobdan oldingi minimal muddat.',
    badge: '🏅',
    badgeName: 'Sabr-toqat'
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
    ftkShowToast('Bugun allaqachon belgilangan. Ertaga qayting!');
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
  ftkShowToast('Kun belgilandi! Strik: ' + streak + ' ' + ftkDayWord(streak));
}

function ftkDayWord(n) {
  return 'kun';
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
    streakMsg = 'Bugun allaqachon belgilangan. Ajoyib ish!';
  } else if (streak === 0) {
    streakMsg = 'Strikni boshlash uchun «Kunni belgilash» tugmasini bosing.';
  } else {
    var yesterday = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
    if (last === yesterday) {
      streakMsg = 'Bugunni belgilashni unutmang, aks holda strik yo\'q bo\'ladi!';
    } else {
      streakMsg = 'Strik uzildi. Qaytadan boshlang — «Kunni belgilash» tugmasini bosing.';
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
    if (m) ftkShowToast('Nishon olindi: ' + m.badge + ' ' + m.badgeName + '!');
  }
}

/* ── RESET ──────────────────────────────────────────────────── */
function ftkConfirmReset() {
  if (!confirm('Barcha taraqqiyot va strikni tiklash? Bu amalni bekor qilib bo\'lmaydi.')) return;
  FTK_MILESTONES.forEach(function(m) { ftkRemove('progress-' + m.id); });
  ftkRemove('progress-streak');
  ftkRemove('progress-lastday');
  ftkRender();
  ftkShowToast('Taraqqiyot tiklandi. Qaytadan boshlaymiz!');
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

## Bosqichlar nimani anglatadi

| Daraja | Treker bosqichlari | Yo'l xaritasi bo'yicha |
|---|---|---|
| 0–1-daraja | Qo'llanmani o'qidim, yo'l xaritasini o'rgandim | Tayyorgarlik + Asoslar |
| 2-daraja | Psixologiya, Trading Plan | Psixologiya va risk |
| 2–3-daraja | Demo-hisob, kalkulyator, cek-list | Birinchi strategiya |
| 3-daraja | Jurnalda 30 ta savdo, SL-siz hafta yo'q | Demo-amaliyot |
| 4-daraja | Xatolarning birinchi tahlili | Tahlil va takomillashtirish |
| 5-daraja | 3 oy demo savdo | Realga tayyorlik |

---

## Trekerni qanday ishlatish bo'yicha maslahatlar

!!! tip "Bosqichlar bilan shoshilmang"
    Bosqichni faqat haqiqatan bajarganingizga ishonchingiz komil bo'lganda belgilang. Trekerni faqat siz ko'rasiz — o'zingizni aldashning ma'nosi yo'q.

!!! tip "Strik tezlikdan muhimroq"
    Haftada bir marta marafondan ko'ra kuniga bir kun o'qish yaxshiroq. Strik — muntazamlik haqida, hajm haqida emas.

!!! info "Ma'lumotlar brauzerda saqlanadi"
    Brauzer keshini tozalasangiz yoki boshqa brauzerga o'tsangiz — taraqqiyot ko'chib o'tmaydi. Qo'lda saqlash shart emas: har o'zgarishda avtomatik sodir bo'ladi.

---

## Bog'liq sahifalar

- [O'quv yo'l xaritasi](../roadmap.md) — nazorat nuqtalari bilan to'liq marshrut
- [Birinchi 100 kun](first-100-days.md) — kun sayin reja
- [Trading Plan](trading-plan-template.md) — demo savdoni boshlashdan oldin to'ldiring
- [Treyding psixologiyasi](psychology.md) — o'qish majburiy
- [Pozitsiya kalkulyatori](../tools/position-calculator.md) — usiz savdoga kirish mumkin emas
