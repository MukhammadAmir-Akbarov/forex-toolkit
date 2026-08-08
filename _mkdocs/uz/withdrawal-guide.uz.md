---
verified: 2026-06-10
---

# Brokerdan O'zbekistonga pul yechib olish qo'llanmasi

> ⚠️ Ma'lumot umumiy, tuzilgan sanada (tekshirildi 2026-06-10). Aniq komissiyalar, muddatlar va **huquqiy holat** o'zgarib turadi — operatsiyadan oldin tekshirib oling.

!!! danger "Muhim: O'zbekistonda P2P-kripto almashuvi noqonuniy"
    **2025-yil 26-may**dan Binance O'zbekiston rezidentlari uchun P2P ni o'chirib qo'ydi, va Milliy
    ilg'or loyihalar agentligi (**NAPP**) tushuntirib berdi: P2P-maydonchalar orqali operatsiyalar
    va litsenziyalangan provayderlardan **tashqaridagi har qanday kriptoaktivlar bilan faoliyat — noqonuniy**
    va javobgarlikka tortiladi (kriptoaktivlarni noqonuniy muomalaga solganlik uchun jinoyat jazoyi ham kiritilgan).

    **USDT ni so'mga qonuniy almashtirish faqat** NAPP tomonidan litsenziyalangan provayderlar orqali mumkin:
    Binance — hamkor **CoinPay** ([coinpay.uz](https://coinpay.uz)) orqali,
    **Telegram Wallet**, shuningdek **Kobea, Coinpay, Asterium** birjalari va litsenziyalangan
    kripto-do'konlar. Dolzarb reyestr — [napp.uz](https://napp.uz) saytida.
    NAPP tushuntirishlariga ko'ra, litsenziyalangan provayderlar orqali olingan daromad soliqdan ozod.

    Kripto bilan shug'ullanishni xohlamasangiz — quyidagi bank kanallaridan foydalaning
    (SWIFT / Visa-Mastercard / Wise): ular qonuniy va hisobot berish uchun qulayroq.

    Manbalar: [spot.uz](https://www.spot.uz/ru/2025/05/28/blocked-p2p/),
    [gazeta.uz](https://www.gazeta.uz/en/2025/01/17/binance/),
    [podrobno.uz](https://podrobno.uz/cat/obchestvo/binance-mozhno-p2p-nelzya-napp-razyasnilo-poryadok-operatsiy-s-kripto-aktivami-dlya-grazhdan-uzbekis/),
    [napp.uz](https://napp.uz).

---

## Yechib olish komissiyasi kalkulyatori

!!! info "O'quv materiali, moliyaviy maslahat emas"
    Hisob taxminiy: komissiyalar istalgan vaqtda o'zgarishi mumkin. Real o'tkazmadan oldin broker va to'lov tizimining saytida joriy shartlarni tekshiring.

<style>
.wd-calc-select {
  flex: 1 1 200px;
  padding: 0.45rem 0.7rem;
  font-size: 1rem;
  border: 1px solid var(--md-default-fg-color--lighter);
  border-radius: 6px;
  background: var(--md-default-bg-color);
  color: var(--md-default-fg-color);
  font-family: inherit;
}
.wd-calc-select:focus {
  outline: 2px solid var(--md-primary-fg-color);
  outline-offset: -1px;
}
.wd-best-row {
  margin-top: 0.9rem;
  padding: 0.65rem 0.9rem;
  border-radius: 6px;
  background: rgba(34, 197, 94, 0.1);
  border-left: 3px solid #22c55e;
  font-size: 0.92rem;
}
.wd-rate-hint {
  font-size: 0.78rem;
  color: var(--md-default-fg-color--light);
  margin-top: 0.25rem;
}
</style>

<div class="calc-widget">

<div class="calc-row">
  <label>Yechib olish miqdori (USD)</label>
  <input type="number" id="wd-amount" min="1" max="100000" step="1" value="500">
  <span>USD</span>
</div>

<div class="calc-row">
  <label>Yechib olish usuli</label>
  <select id="wd-method" class="wd-calc-select">
    <option value="usdt">💰 USDT TRC-20</option>
    <option value="visa">💳 Visa / Mastercard (USD)</option>
    <option value="swift">🏦 SWIFT O'zbekiston bankiga</option>
    <option value="wise">📲 Wise</option>
    <option value="skrill">💵 Skrill / Neteller</option>
  </select>
</div>

<div class="calc-row">
  <label>Kurs USD → UZS</label>
  <input type="number" id="wd-rate" min="1000" max="99000" step="100" value="12600">
  <span>so'm</span>
</div>
<div class="wd-rate-hint" style="margin-left:0; padding: 0 0 0.5rem 0;">
  Kurs taxminiy — <a href="https://cbu.uz" target="_blank" rel="noopener">cbu.uz</a> yoki o'z bankingizda tekshiring
</div>

<button class="calc-button" onclick="calcWithdrawal()">Hisoblash</button>

<div id="wd-result" class="calc-result"></div>

</div>

<script>
(function() {
  var METHODS = {
    usdt: {
      label: 'USDT → litsenziyalangan birja (CoinPay)',
      feeFixed: 4,
      feePct: 0,
      exchangeSpread: 0.02,
      speed: '15–60 daqiqa',
      note: 'Broker komissiyasi ~$3 + TRC-20 tarmog\'i ~$1. USDT ni so\'mga sotish — faqat NAPP litsenziyalangan provayder orqali (CoinPay/Kobea/Asterium, reyestr napp.uz), spred ~2%. P2P O\'z rezidentlari uchun yopiq va noqonuniy.'
    },
    visa: {
      label: 'Visa / Mastercard',
      feeFixed: 0,
      feePct: 0.02,
      exchangeSpread: 0,
      speed: '1–5 kun',
      note: 'Komissiya 1–3% miqdordan. O\'rta qiymat 2% olindi.'
    },
    swift: {
      label: 'SWIFT O\'zbekiston bankiga',
      feeFixed: 52,
      feePct: 0,
      exchangeSpread: 0,
      speed: '3–7 ish kuni',
      note: 'Belgilangan miqdor: broker $0–30 + vositachi bank $15–25 + o\'z bankingiz $0–20. O\'rta qiymat $52 olindi.'
    },
    wise: {
      label: 'Wise',
      feeFixed: 3,
      feePct: 0.0075,
      exchangeSpread: 0,
      speed: '1–3 kun',
      note: 'Belgilangan ~$3 + konvertatsiya uchun 0.5–1%. O\'rta qiymat 0.75% olindi.'
    },
    skrill: {
      label: 'Skrill / Neteller',
      feeFixed: 0,
      feePct: 0.025,
      exchangeSpread: 0,
      speed: '1–2 kun',
      note: 'Komissiya 2–3% miqdordan. O\'rta qiymat 2.5% olindi.'
    }
  };

  function calcFee(amount, methodKey) {
    var m = METHODS[methodKey];
    var fee = m.feeFixed + amount * m.feePct + amount * m.exchangeSpread;
    return fee;
  }

  function findCheapest(amount) {
    var best = null;
    var bestFee = Infinity;
    Object.keys(METHODS).forEach(function(key) {
      var fee = calcFee(amount, key);
      if (fee < bestFee) {
        bestFee = fee;
        best = key;
      }
    });
    return { key: best, fee: bestFee };
  }

  function fmt(n) {
    return n.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
  }

  function fmtUZS(n) {
    return Math.round(n).toLocaleString('uz-UZ');
  }

  window.calcWithdrawal = function() {
    var amount = parseFloat(document.getElementById('wd-amount').value);
    var methodKey = document.getElementById('wd-method').value;
    var rate = parseFloat(document.getElementById('wd-rate').value);
    var resultEl = document.getElementById('wd-result');

    if (!amount || amount <= 0) {
      resultEl.innerHTML = '<div class="calc-warn"><h4>Yechib olish miqdorini kiriting</h4></div>';
      return;
    }
    if (!rate || rate < 1000) {
      resultEl.innerHTML = '<div class="calc-warn"><h4>USD → UZS kursini kiriting</h4></div>';
      return;
    }

    var m = METHODS[methodKey];
    var fee = calcFee(amount, methodKey);
    var net = Math.max(0, amount - fee);
    var netUZS = net * rate;
    var feePct = (fee / amount) * 100;

    var statusClass = feePct <= 2 ? 'calc-ok' : feePct <= 4 ? 'calc-warn' : 'calc-error';
    var statusLabel = feePct <= 2 ? 'Past komissiyalar' : feePct <= 4 ? 'O\'rta komissiyalar' : 'Yuqori komissiyalar';

    var cheapest = findCheapest(amount);
    var cheapestLabel = METHODS[cheapest.key].label;
    var isCheapestSelected = cheapest.key === methodKey;

    var cheapestHtml;
    if (isCheapestSelected) {
      cheapestHtml = '<div class="wd-best-row"><strong>$' + fmt(amount) + '</strong> uchun eng arzon usul — <strong>' + cheapestLabel + '</strong> (tanlangan). Komissiya ~$' + fmt(cheapest.fee) + '.</div>';
    } else {
      cheapestHtml = '<div class="wd-best-row"><strong>$' + fmt(amount) + '</strong> uchun eng arzon usul — <strong>' + cheapestLabel + '</strong> (~$' + fmt(cheapest.fee) + ' komissiya). Siz boshqa variant tanladingiz — u $' + fmt(fee - cheapest.fee) + ' qimmatroq tushadi.</div>';
    }

    var html = '<div class="' + statusClass + '">'
      + '<h4>' + statusLabel + ' — ' + m.label + '</h4>'
      + '<table class="calc-table">'
      + '<tr><td><strong>Yechib olish miqdori</strong></td><td>$' + fmt(amount) + '</td></tr>'
      + '<tr><td><strong>Taxminiy komissiya</strong></td><td>−$' + fmt(fee) + ' (' + feePct.toFixed(1) + '%)</td></tr>'
      + '<tr><td><strong>Qo\'lingizga tegadi (USD)</strong></td><td><strong>$' + fmt(net) + '</strong></td></tr>'
      + '<tr><td><strong>Taxminan so\'mda</strong></td><td><strong>' + fmtUZS(netUZS) + ' so\'m</strong></td></tr>'
      + '<tr><td><strong>Tezlik</strong></td><td>' + m.speed + '</td></tr>'
      + '</table>'
      + '<p style="margin:0.7rem 0 0; font-size:0.85rem; color:var(--md-default-fg-color--light);">Izoh: ' + m.note + '</p>'
      + '</div>'
      + cheapestHtml;

    resultEl.innerHTML = html;
  };

  document.addEventListener('DOMContentLoaded', function() {
    // Журнал знает прибыль за год и присылает её сюда: показанная там сумма
    // не равна тому, что придёт на карту, а раньше это была только сноска.
    var fromJournal = new URLSearchParams(window.location.search).get('amount');
    var asNumber = parseFloat(fromJournal);
    if (isFinite(asNumber) && asNumber > 0) {
      document.getElementById('wd-amount').value = Math.min(asNumber, 100000).toFixed(0);
    }
    window.calcWithdrawal();
    document.getElementById('wd-amount').addEventListener('input', window.calcWithdrawal);
    document.getElementById('wd-method').addEventListener('change', window.calcWithdrawal);
    document.getElementById('wd-rate').addEventListener('input', window.calcWithdrawal);
  });
})();
</script>

---

## Asosiy qoida

**Hech qachon hammasini bir o'tkazmada yechib olmang.** 2-3 qismga bo'ling, avval kichik miqdorda sinab ko'ring.

---

## Yechib olish usullari — umumiy ko'rinish

| Usul | Tezlik | Komissiya | Miqdor | Murakkablik | O'zbekistonda qonuniylik |
|---|---|---|---|---|---|
| 💳 Visa/Mastercard USD | 1-5 kun | 1-3% | $5k gacha | 🟢 oddiy | ✅ bank kanali |
| 🏦 SWIFT O'zbekiston bankiga | 3-7 kun | $25-50 | $1k+ | 🟡 o'rta | ✅ bank kanali |
| 📲 Wise | 1-3 kun | 1-2% | $10k gacha | 🟡 o'rta | ✅ bank kanali |
| 💵 Skrill / Neteller | 1-2 kun | 2-3% | $5k gacha | 🟢 oddiy | ⚠️ bankdan so'mda kiritishni aniqlang |
| 💰 USDT → litsenziyalangan birja | 15-60 daqiqa | ~2% + $4 | limitsiz | 🟡 o'rta | ✅ faqat CoinPay/Kobea/Asterium orqali |
| ❌ USDT → P2P (Binance va boshq.) | — | — | — | — | 🚫 26.05.2025 yopildi, **noqonuniy** |

---

## 1-usul: Litsenziyalangan birja orqali USDT (CoinPay/Kobea/Asterium)

Tez kripto yo'li, lekin USDT ni so'mga almashtirish **faqat** NAPP tomonidan
litsenziyalangan provayder orqali mumkin. Binance va boshqa xorijiy maydonchalar orqali P2P
O'zbekiston rezidentlari uchun yopiq va **noqonuniy** — bu qadam quyida qonuniy usul bilan almashtirildi.

!!! warning "P2P dan foydalanmang"
    Ilgari bu yo'l «USDT ni P2P da sot» bilan tugardi. **Bu endi mumkin emas.**
    USDT ni so'mga faqat litsenziyalangan maydonchada soting (reyestr — [napp.uz](https://napp.uz)).
    Kripto kerak bo'lmasa — bank kanallari (2–3-usul) qonuniy va soliq hisobot uchun qulayroq.

### Qadamlar

#### 1. Brokorda: USDT ga yechib olish
- Shaxsiy kabinet → Mablag'ni yechib olish → USDT TRC-20
- O'z USDT manzilingizni kiriting (2-qadamdan olasiz)
- Broker odatda 1-5 USD komissiya oladi + TRC-20 tarmoq komissiyasi ≈ $1
- Muddat: odatda **15–60 daqiqa**, ba'zan 24 soatgacha

#### 2. Litsenziyalangan provayder (CoinPay / Kobea / Asterium / Telegram Wallet)
- NAPP litsenziyalangan maydonchada ro'yxatdan o'ting va verifikatsiyadan (KYC) o'ting.
  Binance faqat hamkor **CoinPay** ([coinpay.uz](https://coinpay.uz)) orqali qonuniy ishlaydi
- Maydoncha hamyonida → Deposit → USDT TRC-20 → manzilni nusxalang
- Bu manzilni brokerga bering

#### 3. USDT ni so'mga sotish — provayder maydonchasida (P2P emas)
- Litsenziyalangan maydonchada: USDT ni UZS ga soting → HUMO/UZCARD kartaga yechib oling
- Kurs/spred odatda bozordan ~1–3%
- Kartaga o'sha kuni tushadi
- ✅ Bu qonuniy kanal; ❌ Binance'dagi «P2P» bo'limi O'z uchun yopiq va noqonuniy

### USDT → so'm yo'lining narxi

$1 000 yechib olish misoli:
- Broker → USDT: −$3 komissiya
- TRC-20 tarmog'i: −$1
- Litsenziyalangan birja spredi ~2%: −$20
- **Jami «yeyiladi»: ~$24 (2.4%)**

### Afzalliklari
- Tez
- Litsenziyalangan provayder orqali olingan daromad NAPP tushuntirishlariga ko'ra soliqdan ozod
- Past komissiyalar

### Kamchiliklari
- Birjada verifikatsiya talab etiladi (pasport + selfie)
- Faqat litsenziyalangan provayderlar orqali mumkin — oddiy P2P-sotuvchilardan foydalanib bo'lmaydi

---

## 2-usul: SWIFT O'zbekiston bankiga

### Qadamlar

1. Bankda **dollar hisobi** oching: Kapitalbank, Hamkorbank, Asaka, Anorbank, O'zpromstroybonk
2. Brokorda: Yechib olish → Bank Wire → SWIFT rekvizitlarini kiriting
3. Muddat: **3-7 ish kuni**, ba'zan undan ham ko'proq

### Narxi

- Broker komissiyasi: $0-30 (brokerga qarab)
- Vositachi bank komissiyasi: $15-25
- O'z bank komissiyangiz: $0-20
- **Jami: $30-75** miqdordan qat'i nazar (belgilangan)

**$2 000+ miqdorda foydali.**

### Kamchiliklari
- Uzoq
- Bank hujjat so'rashi mumkin (mablag' kelib chiqishi)
- Yakka jismoniy shaxs orqali — ba'zan kechikishlar

---

## 3-usul: Wise (sobiq TransferWise)

### Qadamlar

1. Wise hisobi (USD) ochasiz
2. Brokorda: Yechib olish → Wise (agar qo'llab-quvvatlansa) yoki Wise ga SWIFT
3. Wise da USD ni UZS ga almashtirasiz
4. Wise HUMO/UZCARD kartangizga o'tkazadi

### Narxi
- Wise: USD → UZS o'tkazma uchun 0.5-1%
- + $2-5 belgilangan komissiya

### Kamchiliklari
- Barcha brokerlar Wise ga to'g'ridan-to'g'ri yechib olmaydi
- Wise limitleri verifikatsiyaga bog'liq

---

## ⚠️ Nima qilmaslik kerak

### USDT ni P2P orqali sotmang
- Binance P2P bo'limi O'z rezidentlari uchun 26.05.2025 dan yopildi
- NAPP tushuntirishlariga ko'ra fuqarolarning P2P operatsiyalari **noqonuniy** va javobgarlikka tortiladi
- Kriptoni so'mga faqat litsenziyalangan provayderlar orqali almashtiring (reyestr [napp.uz](https://napp.uz) da)

### Telegramdagi «KYC siz» ayirboshlashdan foydalanmang
- Ko'pincha firibgarlar
- Kurs ajoyib bo'lishi mumkin, lekin 100% yo'qotish xavfi yuqori

### «Begona» USDT hamyoniga yechib olmang
- Do'st, qarindosh, «menejer» — yo'q
- Faqat birjadagi o'z hamyoningizga

### Katta o'tkazmalarni bir to'lovda amalga oshirmang
- Bir marta >$3000-5000 bank e'tiborini tortishi mumkin
- 2-3 tranzaksiyaga bo'ling, oraliq bilan

### Hammasini bir sanada yechib olmang
- Muntazam o'tkazmalar tabiiy ko'rinadi
- Yil oxirida keskin yechib olish — kamroq tabiiy

---

## Saqlash uchun hujjatlar

Har bir yechib olishdan keyin saqlang:

- 📄 **Brokerdan tasdiqlash** (yechib olish bayonnomasi)
- 📄 **USDT tranzaksiyasining TXID si** (kripto orqali bo'lsa)
- 📄 **P2P bitimining skrinshoti** (sotuvchi, vaqt, miqdor)
- 📄 **So'm tushgan karta ko'chirmasi**
- 📄 **ATM cheki** naqd pul olishda

**Kamida 3 yil** saqlang — soliq idorasi savollari uchun.

---

## Soliqlar — qisqacha

Hisoblash uchun [tax-calculator.py](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/uz/tax-calculator.py) ga qarang.

Asosiy:
- **Yillik sof daromad** (foyda − zarar) deklaratsiya qilinadi
- Jismoniy shaxslardan daromad solig'i 12% (2026 holatida)
- Deklaratsiya keyingi yilning 1 aprelgacha topshiriladi
- Har bir bitimdan emas, balki **yil yakunida** to'lanadi

---

## Buxgalter jalb qilish kerak bo'lganda

- Treyding daromadi **yiliga > $5 000**
- Asosiy ish joyi «oq» maoshi bilan bor → to'g'ri umumiy deklaratsiya kerak
- To'ldirish to'g'riligiga ishonchingiz yo'q
- **Soliq idorasidan so'rov** keldi — mutaxassisga majburan murojaat qiling

---

## Tekshirish uchun kontaktlar (tavsiya emas, ma'lumotnoma)

| Qaerda | Nima |
|---|---|
| soliq.uz | Soliq qo'mitasining rasmiy sayti |
| Soliq to'lovchining shaxsiy kabineti | my.soliq.uz |
| Soliq kontakt-markazi | 1198 |

---

[← Asosiy qo'llanmaga](../forex-guide.md)
