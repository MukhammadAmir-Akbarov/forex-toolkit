# Video-stsenariy №4: «Birinchi savdoimni tahlil qilish»

> Kamera uchun to'liq matn — ~5–7 daqiqa. Demoda birinchi ongli savdoni yopgandan **keyin darhol** yozing — hissiyotlar hali yangi ekan.

---

## 🎬 TAYMKODLAR

- 0:00–0:30 — Kirish
- 0:30–2:30 — Kontekst: savdo oldidan nima ko'rdim
- 2:30–4:00 — Savdo parametrlari
- 4:00–5:30 — Savdo qanday rivojlandi va yopildi
- 5:30–7:00 — Asosiy dars

---

## ⚠️ YOZISHDAN OLDIN

```
☐ Kirishdan OLDINGI grafik skrinshoti saqlangan
☐ Yopilishdan KEYINGI grafik skrinshoti saqlangan
☐ Savdo jurnali to'liq to'ldirilgan
☐ Savdo kuni yozyapsiz, bir haftadan keyin emas
☐ Yopilishdan kamida 30 daqiqa o'tgan (hissiyotlar tindi)
```

---

## 🎥 STSENARIY

### [0:00 — BOSHLANISH]

Salom. Bugun men demo-hisobdagi **birinchi ongli savdoimni tahlil qilaman**. Bu jurnalidagi **[N]-savdo**. Hayotimdagi birinchi savdo emas — balki **boshidan oxirigacha rejaga amal qilgan birinchi savdo**.

Bu videoning maqsadi — **foyda yoki zararni ko'rsatish emas**, balki **jarayonni tahlil qilish**. Bir yildan so'ng ushbu videoni qaytadan ko'rib, yo'lning boshida qanday fikrlayotganimni ko'raman.

[*«oldin» grafik skrinshotini ko'rsating*]

### [0:30 — KONTEKST]

Savdo sanasi: **[sana]**. Vaqti: **[vaqt]**.

Juft: **EUR/USD**, kirish taymfreymi **H1**, kontekstni **H4** va **D1** da ko'rdim.

Grafikda nima ko'rdim:

**D1 da** — o'suvchi trend, narx EMA200 dan yuqorida, so'nggi **[N] kun** davomida higher highs va higher lows hosil qilyapti.

**H4 da** — narx **[daraja]** atrofidagi qo'llab-quvvatlash zonasiga orqaga qaytdi. Bu zonadan bozor so'nggi **[davr]** ichida allaqachon **2 marta** sakragan.

**H1 da** — **EMA50 ga pastdan tegib**, **buqali yutib olish** (bullish engulfing) bilan yopilgan sham keldi. Yashil shamning tanasi oldingi qizil shamning tanasini **to'liq qopladi**.

[*skrinshottagi doiralangan elementlarni ko'rsating*]

Kirish paytida RSI(14) **[qiymat]** edi — na haddan tashqari sotib olingan, na haddan tashqari sotilgan holat. Bu mening **filtrimga mos: RSI 40 dan 65 gacha**.

**Forex Factory kalendarini** tekshirdim — keyingi 2 soatda **qizil yangiliklar yo'q edi**. Hafta kuni — **[juma kechqurun emas]**.

Tekshiruv ro'yxatidan o'tdim — **barcha 10 ta band bajarildi**.

### [2:30 — SAVDO PARAMETRLARI]

Parametrlar:

- **Kirish narxi:** [son] — H1 da signal shamining yopilishi
- **Stop Loss:** [son] — signal shamining minimumidan 5 pip pastda
- **Take Profit:** [son] — kirishdan stopgacha masofadan 2 marta uzoqroq

**Stopdagi piplar:** [N]
**Maqsaddagi piplar:** [2×N]
**R:R:** 1 ga 2 — bu men o'zimga ruxsat beradigan **minimum**.

Pozitsiya hajmini **position_calculator.py** orqali hisobladim:
- Depozit: **[N dollar]**
- Risk: **0.5%** — bu pulda **[N dollar]**
- **[N pip]** stopda EUR/USD uchun — pozitsiya **[N] lot**

[*kalkulator skrinshotini ko'rsating*]

MT5 da savdoni ochdim: bir marta F9 tugmasi, lotni kiritdim, **SL va TP ni buyurtma oynasida darhol** — bu eng muhimi.

### [4:00 — RIVOJLANISH VA YOPILISH]

Ochilgandan keyin **MT5 ni yopdim** va o'z ishim bilan ketdim. Bu **muhim**. Har bir shamni tomosha qilib o'tirsam — asabim bo'ziladi, qo'lda yopishni xohlayman.

**[N soat]** dan so'ng tekshirdim — savdo [foyda / zarar da].

[*A variant: savdo foydali*]
Narx mening tomonga **[N pip]** o'tdi va **teyk-profit ishladi**. Savdo avtomatik yopildi. Foyda: **[N dollar]** yoki **+2R**.

[*B variant: savdo zararli*]
Narx stopga qaytib **uni urib o'tdi**. Zarar: **[N dollar]** yoki **−1R**. Men bu imkoniyatni savdodan **oldin bilardim** — shuning uchun **tinchman**.

Asosiy narsa — **men aralashmadim**. Stopni surmadim. Qo'lda yopmadim. «Qaytarib olish» savdosini ochmadim.

[*belgilangan «keyin» grafik skrinshotini ko'rsating*]

### [5:30 — ASOSIY DARS]

Bu savdodan nima angladim?

**Birinchi.** Tekshiruv ro'yxati **ishlaydi**. Barcha 10 ta bandni jismonan belgilaganimda — kirishga **to'liq ishonchim** bor edi. «Biror narsani o'tkazib yubordimmi» degan shubha yo'q edi.

**Ikkinchi.** Pozitsiya kalkulyatori — **majburiy**. Men «ko'zga baholab» **3–4 marta kattaroq** hajm qo'ygan bo'lardim. U holda zarar **0.5% o'rniga depozitning 2–3%** bo'lar edi.

**Uchinchi.** Eng qiyini — tugmani bosish emas, balki **kutish**. Savdo **[N soat]** davom etdi. Shu vaqt ichida men **3 marta** «kichik foyda/zarar bilan yopaman» deb o'yladim. Lekin **bardosh berdim**.

**To'rtinchi.** Rejaga muvofiq **muvaffaqiyatli savdodan** keladigan «to'g'rilik» hissi — «omadga» asoslangan tasodifiy g'alaba hissidan **ancha kuchliroq**. Men endi o'zimga biroz ko'proq **ishonaman**.

[*pauza*]

Keyingi savdoda nima **o'zgartiraman**?
- **[aniq band]** — masalan, kirishdan oldin DXY korrelyatsiyasini tekshirish
- **[aniq band]** — masalan, jurnalda kunning vaqtini qayd etish

[*kadrga qarab*]

30 ta savdodan so'ng ushbu videoni qaytadan ko'rib, fikrlashimda nima o'zgarganini ko'raman. Tomosha qilganingiz uchun rahmat.

[*final*]

---

## 📝 JOY EGALARINI ALMASHTIRISH SHABLONI

Yozishdan oldin **[kvadrat qavslardagi]** narsalarni o'z haqiqiy ma'lumotlaringiz bilan almashtiring:

```
[ism]                 → sizning ismingiz
[N] hafta/oy          → o'qishning haqiqiy muddati
[sana]                → savdo sanasi
[vaqt]                → UTC+5 da kirish vaqti
[daraja]              → qo'llab-quvvatlash/qarshilik qiymati
[qiymat]              → o'sha paytdagi RSI(14)
[son] (kirish)        → aniq kirish narxi
[son] (SL)            → aniq stop narxi
[son] (TP)            → aniq teyk narxi
[N pip]               → stopgacha masofa
[N dollar]            → depozit / risk / natija
[N lot]               → pozitsiya hajmi
[N soat]              → savdo qancha soat ochiq bo'lgani
```

## 🎯 YAKUNLASH VARIANTLARI

**Agar savdo foydali bo'lsa:**
> Bu **o'rgandim degani emas**. Bitta foydali savdo — bu **bitta tanga tashlashning statistikasi**. 30+ seriyasi menda haqiqatan ham **ustunlik** bormi yo'qligini ko'rsatadi.

**Agar savdo zararli bo'lsa:**
> Rejaga ko'ra zarar — bu **muvaffaqiyat**. Men qoidalarga amal qildim, narx shunchaki mening tomonga bormadi. Bu **mening xatoyim emas** — bu **statistikaning bir qismi**. Uzoq masofada R:R 1:2 da men foydadaman.

**Agar SL/TP gacha qo'lda yopsam:**
> Bu **xato edi**. Reja bor edi — stop yoki teykni kutish. Kutmadim. Jurnalga «qoidalar buzilishi» bo'limiga yozdim. Keyingi gal — **bunday qilmaslik**.

---

## 🔁 BIR OYDAN SO'NG NIMA QILISH KERAK

Ushbu videoni **30 ta savdo** yoki **1 oy** dan so'ng qayta ko'ring:

```
☐ Tahlilimda NIMA soddalashtirib yuborilgan edi?
☐ Nima YAXSHI qildim?
☐ Hozir nima BOSHQACHA qilyapman?
☐ O'sha paytda qaysi atamalarni yomon tushunardim?
☐ Savdolarda tinchlashganmidim?
```

Bu aynan **o'tmishdagi o'zingizdan hozirgi o'zingizga qaytgan aloqa**. Bebaho.

---

[← Stsenariylar ro'yxatiga](video-scripts.md)
