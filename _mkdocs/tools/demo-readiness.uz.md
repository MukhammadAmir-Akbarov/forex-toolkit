---
widgets: [readiness]
---

# 🚦 Realga tayyormanmi? — demo bo'yicha xulosa

!!! abstract "«Shekilli chiqyapti» o'rniga halol javob"
    Demo hisobingiz statistikasini kiriting — vosita uni [realga o'tish chek-listi](../journal/demo-vs-real-comparison.md) bilan solishtiradi va to'g'ridan-to'g'ri aytadi: **tayyor** yoki **hali erta, mana nimani yaxshilash kerak**. «Deyarli» yo'q: bajarilmagan har bir band realda pul turadi.

    Raqamlarni [savdo jurnali](../journal/README.md) yoki MT5 hisobotidan oling. Hech narsa serverga yuborilmaydi.

---

## 🧮 Demo statistikangiz

<div class="calc-widget">

<div class="calc-row"><label>Demoda necha oy savdo qilyapsiz</label><input type="number" id="rd-months" min="0" step="1" value="1"></div>
<div class="calc-row"><label>Yopilgan savdolar soni</label><input type="number" id="rd-trades" min="0" step="1" value="20"></div>
<div class="calc-row"><label>Winrate (foydali savdolar ulushi)</label><input type="number" id="rd-winrate" min="0" max="100" step="1" value="45"><span>%</span></div>
<div class="calc-row"><label>O'rtacha RR (o'rtacha foyda / o'rtacha zarar)</label><input type="number" id="rd-rr" min="0.1" step="0.1" value="1.5"></div>
<div class="calc-row"><label>Demo hisobining maksimal tushishi</label><input type="number" id="rd-dd" min="0" max="100" step="1" value="12"><span>%</span></div>
<div class="calc-row"><label>O'z qoidalaringiz buzilgan savdolar</label><input type="number" id="rd-viol" min="0" max="100" step="1" value="10"><span>%</span></div>
<div class="calc-row"><label><input type="checkbox" id="rd-journal"> Har bir savdo uchun jurnal yuritaman</label></div>
<div class="calc-row"><label><input type="checkbox" id="rd-canlose"> Real uchun summani to'liq yo'qotishga tayyorman</label></div>

<button class="calc-button" id="rd-calc-btn">Tekshirish</button>

<div id="rd-result" class="calc-result"></div>

</div>

---

## 📋 Mezonlar va nega aynan shunday

| Band | Chegara | Nega |
|---|---|---|
| Demodagi muddat | ≥ 3 oy | Bir omadli oyni tizimdan ajratib bo'lmaydi |
| Savdolar soni | ≥ 50 | 10–20 savdoda statistika — shovqin |
| Winrate | ≥ 40% | Undan past bo'lsa, yaxshi RR bilan ham stoplar seriyasi og'ir |
| Profit Factor | ≥ 1.5 | Realdagi spred, komissiya va slippage uchun zaxira |
| Maks. tushish | ≤ 20% | Chuqurroq bo'lsa, [tiklanish](drawdown-recovery.md) nomutanosib foyda talab qiladi |
| Qoida buzilishi | < 5% savdolar | Natijani improvizatsiya emas, tizim berishi kerak |
| Jurnal + «yo'qotishga tayyorman» | ha | Jurnalsiz tuzatadigan narsa yo'q, zaxirasiz — har savdoda bosim |

Profit Factor winrate va RR dan hisoblanadi: `PF = winrate × RR / (1 − winrate)`. Savdoga R dagi kutilma: `winrate × RR − (1 − winrate)`. Batafsil — [WinRate × RR kalkulyatorida](winrate-rr-calculator.md).

---

## 🔗 Keyin nima

- [Tayyorlik testi](risk-profile.md) — psixologiya va moliyaviy zaxira (bu xulosani to'ldiradi)
- [Demo vs Real](../journal/demo-vs-real-comparison.md) — realga asta-sekin qanday o'tish
- [Bankrotlik riski](risk-of-ruin.md) — statistikangiz yomon seriyalarga qanday bardosh beradi

---

!!! note "Ta'limiy material"
    Xulosa — **o'quv mo'ljali**, moliyaviy maslahat va natija kafolati emas. Bajarilgan chek-list zarardan himoya qilmaydi: real savdo har doim kiritilgan mablag'ni to'liq yo'qotish riskini o'z ichiga oladi.
