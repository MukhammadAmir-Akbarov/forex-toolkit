# 🚦 Savdo oldidan tekshiruv ro'yxati (yashil chiroq)

!!! abstract "Bu tekshiruv ro'yxati nima uchun kerak?"
    Yangi boshlovchilarning ko'pchilik zararlari setu «yomon» bo'lgani uchun emas — balki savdo **asosiy shartlar tekshirilmasdan** ochilgani uchun sodir bo'ladi: stop-losssiz, oshirib yuborilgan xavf bilan, his-tuyg'ular ta'sirida yoki «qaytarib olish» maqsadida.

    Bu tekshiruv ro'yxati **uchuvchining parvozdan oldingi tekshiruvi** kabi ishlaydi: zerikarli, lekin majburiy. Hatto bitta belgi qo'yilmagan bo'lsa ham — **savdo ochilmaydi**.

!!! warning "Ta'lim materiali — moliyaviy maslahat emas"
    Bu sahifa o'quv loyihasining bir qismi. Barcha tavsiflar ta'lim mazmuniga ega va moliyaviy tavsiya hisoblanmaydi. Savdo real xavflar bilan bog'liq.

---

## 🚦 Savdoga kirishdan oldingi tekshiruv ro'yxati

<style>
.pretrade-widget {
  background: var(--md-code-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1.5rem 0;
}

.pretrade-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.75rem 0.9rem;
  margin-bottom: 0.5rem;
  border-radius: 8px;
  background: var(--md-default-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  cursor: pointer;
  transition: border-color 0.18s, background 0.18s;
  user-select: none;
}

.pretrade-item:hover {
  border-color: var(--md-primary-fg-color);
}

.pretrade-item.checked {
  border-color: #22c55e;
  background: rgba(34, 197, 94, 0.06);
}

.pretrade-item input[type="checkbox"] {
  margin-top: 3px;
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  accent-color: #22c55e;
  cursor: pointer;
}

.pretrade-item-text {
  flex: 1;
  font-size: 0.96rem;
}

.pretrade-item-title {
  font-weight: 600;
  margin-bottom: 0.15rem;
}

.pretrade-item-hint {
  font-size: 0.82rem;
  color: var(--md-default-fg-color--light);
  margin-top: 0.1rem;
}

.pretrade-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 1.2rem;
  flex-wrap: wrap;
}

.pretrade-reset {
  background: none;
  border: 1px solid var(--md-default-fg-color--lighter);
  color: var(--md-default-fg-color--light);
  border-radius: 6px;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  cursor: pointer;
}

.pretrade-reset:hover {
  border-color: var(--md-primary-fg-color);
  color: var(--md-primary-fg-color);
}

.pretrade-result {
  margin-top: 1.2rem;
  padding: 1.1rem 1.3rem;
  border-radius: 8px;
  border-left: 4px solid var(--md-primary-fg-color);
  background: var(--md-default-bg-color);
}

.pretrade-green {
  border-left-color: #22c55e;
  background: rgba(34, 197, 94, 0.07);
}

.pretrade-green .pt-verdict {
  color: #16a34a;
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0 0 0.4rem;
}

.pretrade-red {
  border-left-color: #dc2626;
  background: rgba(220, 38, 38, 0.07);
}

.pretrade-red .pt-verdict {
  color: #dc2626;
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0 0 0.4rem;
}

.pt-failed-list {
  margin: 0.6rem 0 0;
  padding-left: 1.2rem;
  font-size: 0.92rem;
}

.pt-failed-list li {
  margin-bottom: 0.3rem;
}

.pretrade-stats {
  margin-top: 1.2rem;
  padding: 0.9rem 1.2rem;
  background: var(--md-code-bg-color);
  border-radius: 8px;
  border: 1px solid var(--md-default-fg-color--lightest);
  font-size: 0.88rem;
}

.pretrade-stats-title {
  font-weight: 700;
  font-size: 0.92rem;
  margin-bottom: 0.5rem;
  color: var(--md-default-fg-color--light);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.pt-stat-row {
  display: flex;
  justify-content: space-between;
  padding: 0.22rem 0;
  border-bottom: 1px dashed var(--md-default-fg-color--lightest);
}

.pt-stat-row:last-child { border-bottom: none; }

.pt-stat-value {
  font-family: var(--md-code-font-family);
  font-weight: 700;
}

.pt-stat-green { color: #16a34a; }
.pt-stat-red { color: #dc2626; }

.pt-discipline-bar-wrap {
  margin-top: 0.6rem;
}

.pt-discipline-label {
  font-size: 0.82rem;
  color: var(--md-default-fg-color--light);
  margin-bottom: 0.2rem;
}

.pt-discipline-bar-bg {
  width: 100%;
  height: 8px;
  background: var(--md-default-fg-color--lightest);
  border-radius: 99px;
  overflow: hidden;
}

.pt-discipline-bar-fill {
  height: 100%;
  border-radius: 99px;
  background: #22c55e;
  transition: width 0.4s ease;
}
</style>

<div class="pretrade-widget">

<div id="pt-item-0" class="pretrade-item" onclick="ptToggle(0)">
  <input type="checkbox" id="pt-cb-0" onclick="event.stopPropagation(); ptToggle(0)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">🛑 Stop-loss o'rnatilgan</div>
    <div class="pretrade-item-hint">SL darajasi kirishdan oldin aniqlanib, terminald o'rnatilgan — «xayolda» emas</div>
  </div>
</div>

<div id="pt-item-1" class="pretrade-item" onclick="ptToggle(1)">
  <input type="checkbox" id="pt-cb-1" onclick="event.stopPropagation(); ptToggle(1)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">💰 Xavf ≤ depozitning 1%</div>
    <div class="pretrade-item-hint">Lot hajmi shunday hisoblanganki, bu savdodagi zarar hisobning 1% ini oshirmaydi</div>
  </div>
</div>

<div id="pt-item-2" class="pretrade-item" onclick="ptToggle(2)">
  <input type="checkbox" id="pt-cb-2" onclick="event.stopPropagation(); ptToggle(2)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">🧮 Pozitsiya hajmi kalkulyator bilan hisoblangan</div>
    <div class="pretrade-item-hint">Lot kalkulyatordan olingan — «ko'z bilan» yoki «odatdagidek» emas</div>
  </div>
</div>

<div id="pt-item-3" class="pretrade-item" onclick="ptToggle(3)">
  <input type="checkbox" id="pt-cb-3" onclick="event.stopPropagation(); ptToggle(3)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">😤 Bu qaytarib olish savdosi (revenge trade) emas</div>
    <div class="pretrade-item-hint">Men hozirgina stop oldim va «pulni qaytarib olmoqchiman» degan sababdan kirmayman</div>
  </div>
</div>

<div id="pt-item-4" class="pretrade-item" onclick="ptToggle(4)">
  <input type="checkbox" id="pt-cb-4" onclick="event.stopPropagation(); ptToggle(4)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">📅 Iqtisodiy kalendar tekshirilgan</div>
    <div class="pretrade-item-hint">Yaqin 30 daqiqada muhim yangiliklar yo'q (NFP, foiz stavkasi qarori, CPI va h.k.)</div>
  </div>
</div>

<div id="pt-item-5" class="pretrade-item" onclick="ptToggle(5)">
  <input type="checkbox" id="pt-cb-5" onclick="event.stopPropagation(); ptToggle(5)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">📋 Setu savdo rejasiga mos keladi</div>
    <div class="pretrade-item-hint">Bu kirish mening treyding-rejamda tasvirlangan. Men «yangi g'oya»ni shoshilinch savdoga solmayman</div>
  </div>
</div>

<div id="pt-item-6" class="pretrade-item" onclick="ptToggle(6)">
  <input type="checkbox" id="pt-cb-6" onclick="event.stopPropagation(); ptToggle(6)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">📐 RR ≥ 1.5 (potensial foyda xavfdan 1.5× va undan ko'p)</div>
    <div class="pretrade-item-hint">TP gacha masofa SL gacha masofadan kamida 1.5 marta uzun</div>
  </div>
</div>

<div id="pt-item-7" class="pretrade-item" onclick="ptToggle(7)">
  <input type="checkbox" id="pt-cb-7" onclick="event.stopPropagation(); ptToggle(7)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">🔢 Kunlik savdolar limiti oshirilmagan</div>
    <div class="pretrade-item-hint">Bugun kunlik maksimal savdolar soniga hali yetganim yo'q (odatda kuniga 2–3 ta maksimum)</div>
  </div>
</div>

<div class="pretrade-actions">
  <button class="calc-button" onclick="ptCheck()">Tekshirish</button>
  <button class="pretrade-reset" onclick="ptReset()">Tozalash</button>
</div>

<div id="pt-result" class="pretrade-result" style="display:none;"></div>

<div id="pt-stats" class="pretrade-stats">
  <div class="pretrade-stats-title">Intizom statistikasi (ushbu brauzer)</div>
  <div class="pt-stat-row">
    <span>Yashil tekshiruvlar (hammasi OK)</span>
    <span class="pt-stat-value pt-stat-green" id="pt-green-count">—</span>
  </div>
  <div class="pt-stat-row">
    <span>Qizil urinishlar (hammasi OK emas)</span>
    <span class="pt-stat-value pt-stat-red" id="pt-red-count">—</span>
  </div>
  <div class="pt-stat-row">
    <span>Intizom koeffitsienti</span>
    <span class="pt-stat-value" id="pt-discipline-pct">—</span>
  </div>
  <div class="pt-discipline-bar-wrap">
    <div class="pt-discipline-label">To'liq tekshiruv ro'yxatida bosilishlar foizi</div>
    <div class="pt-discipline-bar-bg">
      <div class="pt-discipline-bar-fill" id="pt-disc-bar" style="width:0%"></div>
    </div>
  </div>
</div>

</div>

<script>
(function () {
  var TOTAL = 8;
  var KEY_RED = 'ftk-pretrade-redattempts';
  var KEY_GREEN = 'ftk-pretrade-greenattempts';

  function getCount(key) {
    return parseInt(localStorage.getItem(key) || '0', 10);
  }

  function incCount(key) {
    localStorage.setItem(key, getCount(key) + 1);
  }

  function ptToggle(idx) {
    var cb = document.getElementById('pt-cb-' + idx);
    var item = document.getElementById('pt-item-' + idx);
    cb.checked = !cb.checked;
    item.classList.toggle('checked', cb.checked);
  }

  window.ptToggle = ptToggle;

  window.ptCheck = function () {
    var failed = [];
    var labels = [
      'Stop-loss o\'rnatilgan',
      'Xavf ≤ depozitning 1%',
      'Pozitsiya hajmi kalkulyator bilan hisoblangan',
      'Bu qaytarib olish savdosi (revenge trade) emas',
      'Iqtisodiy kalendar tekshirilgan',
      'Setu savdo rejasiga mos keladi',
      'RR ≥ 1.5',
      'Kunlik savdolar limiti oshirilmagan'
    ];

    for (var i = 0; i < TOTAL; i++) {
      if (!document.getElementById('pt-cb-' + i).checked) {
        failed.push(labels[i]);
      }
    }

    var resultEl = document.getElementById('pt-result');
    resultEl.style.display = 'block';

    if (failed.length === 0) {
      incCount(KEY_GREEN);
      resultEl.className = 'pretrade-result pretrade-green';
      resultEl.innerHTML =
        '<div class="pt-verdict">✅ Ochish mumkin</div>' +
        '<p style="margin:0;font-size:0.93rem;">Barcha shartlar bajarilgan. Savdoni rejaga qat\'iy rioya qilib oching — kirishdan so\'ng stop va teykni o\'zgartirmang.</p>';
    } else {
      incCount(KEY_RED);
      var listItems = failed.map(function (f) { return '<li>' + f + '</li>'; }).join('');
      resultEl.className = 'pretrade-result pretrade-red';
      resultEl.innerHTML =
        '<div class="pt-verdict">🛑 OCHMANG</div>' +
        '<p style="margin:0 0 0.5rem;font-size:0.93rem;">' + TOTAL + ' ta shartdan <strong>' + failed.length + '</strong> tasi bajarilmagan:</p>' +
        '<ul class="pt-failed-list">' + listItems + '</ul>' +
        '<p style="margin:0.7rem 0 0;font-size:0.85rem;color:var(--md-default-fg-color--light);">Barcha bandlarni to\'g\'rilang, so\'ng «Tekshirish» tugmasini yana bosing.</p>';
    }

    updateStats();
    resultEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  };

  window.ptReset = function () {
    for (var i = 0; i < TOTAL; i++) {
      var cb = document.getElementById('pt-cb-' + i);
      var item = document.getElementById('pt-item-' + i);
      cb.checked = false;
      item.classList.remove('checked');
    }
    var resultEl = document.getElementById('pt-result');
    resultEl.style.display = 'none';
    resultEl.innerHTML = '';
  };

  function updateStats() {
    var green = getCount(KEY_GREEN);
    var red = getCount(KEY_RED);
    var total = green + red;

    document.getElementById('pt-green-count').textContent = green;
    document.getElementById('pt-red-count').textContent = red;

    if (total === 0) {
      document.getElementById('pt-discipline-pct').textContent = '—';
      document.getElementById('pt-disc-bar').style.width = '0%';
    } else {
      var pct = Math.round((green / total) * 100);
      document.getElementById('pt-discipline-pct').textContent = pct + '%';
      document.getElementById('pt-disc-bar').style.width = pct + '%';
      var bar = document.getElementById('pt-disc-bar');
      if (pct >= 80) {
        bar.style.background = '#22c55e';
      } else if (pct >= 50) {
        bar.style.background = '#f59e0b';
      } else {
        bar.style.background = '#dc2626';
      }
    }
  }

  window.addEventListener('DOMContentLoaded', updateStats);
}());
</script>

---

## 📖 Har bir band nima uchun kerak

### 1. Stop-loss o'rnatilgan

Terminaldagi stop — «xayoldagi» emas. Professional uni pozitsiyani ochishdan **oldin** qo'yadi. Stop-losssiz qancha yo'qotishingizni bilmaysiz: bu endi treyding emas, bu kazino.

### 2. Xavf ≤ 1%

Ketma-ket 10 ta zarar (kamdan-kam, lekin bo'ladi) bo'lsa depozitning ~10% ini yo'qotasiz — va hisob tirik. Savdo boshiga 5% xavf qo'yilsa — 10 ta zarar = -50% depozit, va ruhiyat sinadi.

### 3. Pozitsiya hajmi kalkulyator bilan

«Ko'z bilan» va «odatdagidek» — 1% xavf qoidasini buzishning asosiy sababi. [Pozitsiya kalkulyatoridan foydalaning](../tools/position-calculator.md). Pul saqlaydigan 30 soniya.

### 4. Bu qaytarib olish emas

Stop oldingiz — «pulni hoziroq qaytarib olish» istagi paydo bo'ldimi? Bu **revenge trade**. Bunday savdolar statistik jihatdan zararli: siz mantiq emas, his-tuyg'ular bilan kirasiz. [Anti-Tilt protokoli](anti-tilt-protocol.md) — sizning qurolingiz.

### 5. Iqtisodiy kalendar

NFP, FRS qarori, CPI — bu «yadroviy» yangiliklar. Chiqish paytida spred kengayadi, stoplar sirpanadi. Yangi boshlovchilarga — yirik yangiliklar chiqishidan **15–30 daqiqa oldin va keyin savdo qilmang**.

!!! tip "Qayerda ko'rish mumkin"
    [Investing.com/economic-calendar](https://www.investing.com/economic-calendar/) yoki [ForexFactory.com](https://www.forexfactory.com/calendar) — bepul, «High Impact» hodisalarini filtrlang.

### 6. Rejaga mos setu

Agar bu setu sizning [savdo rejangizda](trading-plan-template.md) bo'lmasa — demak siz uni sinab ko'rmagansiz. Hech bo'lmaganda demoda tekshirilmagan narsani savdoga solmang. «Yaxshi kirish kabi ko'rinadi» — savdo rejasi emas.

### 7. RR ≥ 1.5

Win Rate 50% va RR = 1.5 bo'lsa → matematik kutish **musbat**. RR = 0.8 bo'lsa — manfiy. [WinRate × RR kalkulyatori](../tools/winrate-rr-calculator.md) aniq raqamlarni ko'rsatadi.

| RR | Nolga chiqish uchun kerakli WR |
|---|---|
| 0.5 | 67% |
| 1.0 | 50% |
| **1.5** | **40%** |
| 2.0 | 33% |

### 8. Kunlik savdolar limiti

Ko'proq savdo — ko'proq foyda degani emas. Yangi boshlovchilarda «haddan ortiq savdo» (overtrading) — hisob yo'qotishning 3 ta asosiy sababidan biri. Oldindan hal qiling: kuniga maksimum **2–3 ta savdo**. Limitga yetildi — kompyuter yopildi.

---

## 🧠 Belgi qo'ya olmayotgan bo'lsangiz nima qilish kerak?

!!! danger "Qizil bayroq: «Qoidani buzayotganimni bilaman, lekin baribir kiraman»"
    Agar siz tekshiruv ro'yxatini ongli ravishda e'tiborsiz qoldirsangiz — bu «tajribali treyderning ishonchi» emas. Bu tiltning boshlanishi.

    Terminalni yoping. [Anti-Tilt Protokolini](anti-tilt-protocol.md) o'qing.

**SL o'rnatmaslik** — platformaga hozirda texnik imkon yo'qligini anglatadi (buni avval hal qiling), yoki «qo'lda chiqaman» deb umid qilayotganingizni. Bu ishlaydi.

**Xavf > 1%** — «setu juda yaxshi bo'lgani uchun hajmni oshirish» vasvasasi — tuzoq. Yaxshi setuler muntazam bo'ladi. Bu oxirgisi emas.

**Revenge trade** — yagona to'g'ri javob: stopdan keyin 30 daqiqa pauza. Turing, suv iching. Bozor hech qaerga qochib ketmaydi.

---

## 📋 Tezkor ma'lumotnoma kartasi

```
SAVDO OLDIDAN TEKSHIRUV RO'YXATI — qisqacha

☐  Stop-loss terminald o'rnatilgan
☐  Xavf ≤ depozitning 1%
☐  Lot kalkulyator bilan hisoblangan
☐  Bu qaytarib olish EMAS
☐  Yangiliklar tekshirilgan (hodisagacha ≥ 30 daqiqa)
☐  Setu savdo rejasida mavjud
☐  RR ≥ 1.5
☐  Kunlik savdolar limiti oshirilmagan

HAMMASI 8 — yashil chiroq ✅
Bitta YO'Q — to'xtash 🛑
```

> **Chop eting va monitor yoniga qo'ying.**
> Tekshiruv ro'yxati odatga aylanmaguncha — qog'oz versiyasidan foydalaning.

---

## 🔗 Bog'liq sahifalar

- [Anti-Tilt Protokoli](anti-tilt-protocol.md) — qoidalarni buzgingiz kelganda nima qilish kerak
- [Favqulodda karta](emergency-card.md) — inqiroz paytida tezkor yordam
- [Pozitsiya kalkulyatori](../tools/position-calculator.md) — to'g'ri lotni hisoblang
- [WinRate × RR kalkulyatori](../tools/winrate-rr-calculator.md) — setu matematikasini tekshiring
- [Savdo rejasi — shablon](trading-plan-template.md) — agar sizda hali reja bo'lmasa
- [Treyding psixologiyasi](psychology.md) — nima uchun miya qoidalarni sabotaj qiladi
