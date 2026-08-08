---
widgets: [strategy-ranking]
---

# 🏁 Qaysi strategiya yaxshiroq — va bu javob turadimi

!!! abstract "O'sha oilaning uchinchi savoli"
    [Qayta o'qitish](overfitting.md) — sozlama vaqt bo'ylab ko'chadimi.
    [Boshqa juftliklarga ko'chirish](multipair.md) — u bozorlar orasida
    ko'chadimi. Bu yerda: **strategiyalarning o'z reytingi turadimi**.

    Repozitoriydagi oltita strategiya, haqiqiy EUR/USD H1 shamlari. Faqat
    tarixning birinchi yarmi ko'rsatilgan. Ikkinchisida kim birinchi bo'lishini
    tanlang.

<div id="strategy-ranking" data-src="../../../data/strategies.json"></div>

---

## Nima chiqdi

| Strategiya | O'tmish | Kelajak | O'rin |
|---|---|---|---|
| EMA50 Pullback | **+22.2R** | −10.5R | 1 → 5 |
| Three Soldiers | +16.6R | +13.1R | 2 → 2 |
| Breakout | +9.8R | −8.3R | 3 → 4 |
| Mean Reversion | +5.8R | −12.1R | 4 → 6 |
| Breakout v2 | −4.6R | +11.9R | 5 → 3 |
| London Open Range | **−39.3R** | **+18.8R** | 6 → 1 |

O'tmishdagi eng yaxshisi **oltitadan beshinchi** bo'ldi. O'tmishdagi eng yomoni
**birinchi** bo'ldi. Oltitadan bittasi o'z o'rnini saqladi. Tartib mosligi —
**−0.43**.

## Bu nimani anglatadi va nimani anglatmaydi

**Anglatadi:** tarix asosida tuzilgan strategiyalar reytingi tanlash uchun asos
bermaydi. Na birinchi o'rin, na oxirgisi keyingi yil haqida hech narsa aytmadi.

**Anglatmaydi:** tartib doim teskari bo'ladi va eng yomonini tanlash kerak
degani emas. Oltita strategiya — kichik tanlanma, bu yerdagi manfiy bog'liqlik
osongina tasodif bo'lishi mumkin. Da'vo aniq bitta: **bunday reytingga
tayanib bo'lmaydi.**

Bu qayta o'qitish sahifasidagi o'sha tuzoq. Oltita strategiyadan eng yaxshisini
tanlash — 54 ta parametr to'plamidan eng yaxshisini tanlash bilan bir xil
saralash. Chiroyli natija ko'proq variant sinaganga tegadi.

## Nega «sintetikada solishtirish» emas

Repozitoriyda `strategies/compare.py` bor — u o'sha strategiyalarni
**yaratilgan** shamlarda solishtiradi. Mexanikani ko'rsatish uchun bu normal,
«bu strategiya yaxshiroq» degan da'vo uchun esa yo'q: raqamlar o'ylab
topilgan bo'lardi. Shuning uchun bu yerda haqiqiy arxiv, vaqt bo'yicha bo'linish
esa oshkora ko'rsatilgan.

## Men chop etishimga oz qolgan xato

Birinchi hisob London Open Range uchun ikkala yarmida ham **nol savdo** berdi.
Bu uning xossasiga o'xshardi: «strategiya signal topmaydi».

Aslida `london_open.detect` avval ma'lumot indeksi vaqt indeksimi degan
tekshiruvni qiladi va aks holda jimgina bo'sh ro'yxat qaytaradi. Xato yo'q,
shunchaki «signal topilmadi». Tuzatishdan keyin strategiya 256 va 174 ta savdo
berdi — va o'tmishda eng yomon, kelajakda eng yaxshi bo'lib chiqdi, ya'ni aynan
shu sahifa mavjud bo'lgan holat.

Bir kunda ikkinchi marta o'sha tuzoq: **nol natija — o'lchanayotgan narsaning
xossasidan ko'ra ko'proq o'lchovning buzilishi.**
`test_every_strategy_actually_traded` testi endi biror strategiya kerakli
ma'lumotni olmay qolsa yiqiladi.

## Bu bilan nima qilish kerak

1. **Strategiyani bitta bektest bo'yicha tanlamang.** Bitta hisob — bitta
   tanlanma.
2. **Yakuniy raqamga emas, mantiqqa qarang.** Savdo nega ishlashi kerakligining
   aniq sababi davr almashishiga chiroyli egri chiziqdan yaxshiroq bardosh
   beradi.
3. **Barqarorlikni tekshiring.** Turli davrlar, turli juftliklar, turli
   parametrlar. Faqat bitta birikmada turadigan natija — natija emas.

## Keyingi qadam

- [Bektest nega yolg'on gapiradi](overfitting.md) — parametrlardagi o'sha tuzoq.
- [Boshqa juftliklarga ko'chirish](multipair.md) — bozorlardagi o'shanisi.
- [Mahorat yoki omad](monte-carlo.md) — o'z seriyangizni tekshirish.

!!! danger "Moliyaviy maslahat emas"
    Raqamlar bitta juftlikda, bitta davrda o'lchangan. Oltita strategiyaning
    hech biri savdo uchun tavsiya etilmaydi — ular o'quv namunasi sifatida bor.
