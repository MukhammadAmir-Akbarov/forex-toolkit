# 💲 Pip qiymati kalkulyatori

!!! abstract "Nima uchun bu kerak"
    Pip — bu **narx harakatining eng kichik birligi**. Har bir pipda qancha pul yutish yoki yo'qotishingiz **pozitsiya hajmi** va **juftlik**ka bog'liq. Pip qiymatini tushunmasdan xavfni to'g'ri hisoblash mumkin emas.

## Formula

```
1 lot hajmi           =  100 000 ta asosiy valyuta birligi
Pip o'lchami          =  Ko'pchilik juftliklar uchun 0.0001, JPY-juftliklar uchun 0.01
Pip qiymati (USD)     =  pip_o'lchami × lot / kurs (agar USD — quote yoki base bo'lsa)
```

---

<div class="pos-calc-widget" id="pip-calc">

<form class="pos-calc-form" onsubmit="return false">
  <label>
    Valyuta jufti
    <select id="pp-pair">
      <option value="EURUSD">EUR / USD</option>
      <option value="GBPUSD">GBP / USD</option>
      <option value="AUDUSD">AUD / USD</option>
      <option value="NZDUSD">NZD / USD</option>
      <option value="USDJPY">USD / JPY</option>
      <option value="USDCHF">USD / CHF</option>
      <option value="USDCAD">USD / CAD</option>
      <option value="EURJPY">EUR / JPY</option>
      <option value="GBPJPY">GBP / JPY</option>
      <option value="EURGBP">EUR / GBP</option>
      <option value="AUDJPY">AUD / JPY</option>
      <option value="CHFJPY">CHF / JPY</option>
      <option value="EURAUD">EUR / AUD</option>
      <option value="EURCHF">EUR / CHF</option>
    </select>
  </label>
  <label>
    Pozitsiya hajmi (lot)
    <input type="number" id="pp-lots" value="0.10" min="0.01" step="0.01" autocomplete="off">
    <span class="pc-meta">0.01 = mikro-lot, 0.1 = mini, 1.0 = standart.</span>
  </label>
  <label>
    USD→UZS kursi (so'm, ixtiyoriy)
    <input type="number" id="pp-uzs" value="12600" min="0" step="any" autocomplete="off">
    <span class="pc-meta">Faqat so'mdagi qo'shimcha natija uchun ishlatiladi.</span>
  </label>
  <label class="pc-checkbox pc-row-wide">
    <input type="checkbox" id="pp-live" checked>
    <span>Joriy ECB kursidan foydalanish (tavsiya etiladi)</span>
  </label>
  <button type="button" id="pp-calc-btn" class="pc-row-wide">Hisoblash</button>
</form>

<div id="pp-result" class="pc-result" style="display: none;">
  <div class="pc-headline" id="pp-headline">— $ / pip</div>
  <div class="pc-result-grid">
    <div class="pc-result-row"><span>Juftlik</span><span id="pp-out-pair">—</span></div>
    <div class="pc-result-row"><span>Pozitsiya hajmi</span><span id="pp-out-lots">—</span></div>
    <div class="pc-result-row"><span>Pip o'lchami</span><span id="pp-out-pipsize">—</span></div>
    <div class="pc-result-row"><span>Kurs (hisoblash uchun)</span><span id="pp-out-rate">—</span></div>
    <div class="pc-result-row"><span>1 pip qiymati</span><span id="pp-out-pip">—</span></div>
    <div class="pc-result-row"><span>10 pipda</span><span id="pp-out-10">—</span></div>
    <div class="pc-result-row" id="pp-out-uzs-row"><span>1 pip so'mda</span><span id="pp-out-uzs">—</span></div>
    <div class="pc-result-row" id="pp-out-uzs-10-row"><span>10 pip so'mda</span><span id="pp-out-uzs-10">—</span></div>
  </div>
  <div class="pc-warnings" id="pp-warnings"></div>
</div>


</div>

---

## Misollar

| Juftlik | 0.1 lot uchun 1 pip | 1 lot (standart) uchun 1 pip |
|---|---|---|
| EUR/USD | $1.00 | $10.00 |
| GBP/USD | $1.00 | $10.00 |
| USD/JPY (kurs ~150) | $0.67 | $6.67 |
| USD/CHF (kurs ~0.88) | $1.14 | $11.36 |
| EUR/JPY (kurs EUR/JPY ~162) | $0.67 | $6.67 |
| EUR/GBP (kurs GBP/USD ~1.27) | $1.27 | $12.70 |

## Nima uchun buni bilish kerak

- **Broker kalkulyatorini tekshirish** — ba'zi platformalarda pip qiymati noto'g'ri ko'rsatiladi
- **Juftliklarni taqqoslash** — nima uchun USDJPY dagi xuddi shu 25-piplik stop EURUSD ga qaraganda arzonroq tushadi
- **Hisob valyutasini konvertatsiya qilish** — agar depozit USD da bo'lmasa, qo'shimcha konvertatsiya kerak bo'ladi

## Python versiyasi

[`tools/pip_calculator.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/pip_calculator.py) ga qarang.
