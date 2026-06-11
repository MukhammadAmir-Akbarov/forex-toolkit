# Daily Routine — treyderning kun tartibi

> Professional treyder — bu **rutina va odatlar**, «daholarcha shu'la» emas. Ushbu hujjat — sizning kunlik shabloningiz.

---

## 🌅 ERTALAB (savdo sessiyasidan 30 daqiqa oldin)

### O'z-o'zini tekshirish
- [ ] ≥ 7 soat uyqladim
- [ ] Ovqatlandim / suv ichdim
- [ ] G'azabli, tashvishli yoki eyforik emas man
- [ ] Shoshilmayapman («ishlar orasida» emas)

**Agar hech bo'lmaganda bitta band «yo'q» bo'lsa → bugun savdo qilmayman.**

### Muhitni tayyorlash
- [ ] Tinch ish joyi
- [ ] Telefon «bezovta qilmang» rejimida (yoki boshqa xonada)
- [ ] Ijtimoiy tarmoqlar o'chirilgan (Telegram, o'z botim signallaridan tashqari, Instagram, TikTok)
- [ ] Faqat kerakli tablar ochiq

### Asboblarni tayyorlash
- [ ] MT5 ishga tushirilgan, serverga ulangan
- [ ] EUR/USD H1 + EMA50/EMA200/RSI grafigi ochiq
- [ ] H4 grafigi parallel ochiq (trend konteksti uchun)
- [ ] Pozitsiya kalkulyatori terminalda ishga tushirilgan
- [ ] Jurnal tayyor (Google Sheets yoki Markdown)
- [ ] Chop etilgan chek-list stol ustida

### Ertalabki tahlil (15 daqiqa)

1. **Yangiliklar taqvimi** (5 daqiqa)
   ```bash
   .venv/bin/python tools/news_scraper.py --day today --high-only
   ```
   Yozib olish: bugun qizil yangiliklar qachon → ulardan 2 soat oldin va keyin savdo qilmaslik

2. **Global manzara** (5 daqiqa)
   - D1 EUR/USD — qaysi trendda?
   - H4 EUR/USD — HH/HL yoki LH/LL tuzilmasi?
   - Eng yaqin D1 darajalari qayerda?
   - Kechasi nima bo'ldi? (Osiyo sessiyasi harakat berdimi?)

3. **Kun rejasi** (5 daqiqa)
   - Bugun qaysi yo'nalishda savdo qilaman?
   - Qiziqish zonalari (setup kutish joyi)?
   - Maksimal nechta savdo? (1-3)
   - Qaysi yangiliklar / voqealardan qochasiz?

---

## 🎯 KUN — ish sessiyasi (London + Nyu-York)

### London sessiyasi (10:00–19:00 UTC = 15:00–24:00 UTC+5)

**Grafik oldida doim o'tirib turmaslik kerak.** Professional yondashuv:

#### 1-daqiqa: setup tekshirish
- H1 ni oching
- Oxirgi bir soatda nima bo'ldi?
- **Hozir** setup bormi (chek-list bo'yicha)?

#### Agar setup YO'Q bo'lsa
- MT5 ni bir soatga yoping
- Boshqa ish bilan shug'ullaning
- Bir soatdan keyin qayting

#### Agar setup BOR bo'lsa
**Chek-listni jismonan o'tkazing:**
```
☐ D1 / H4 trendi aniqlangan
☐ H1 — EMA50 ga chekinish
☐ Sham paterni
☐ RSI ekstremal holatda emas
☐ Stop texnik jihatdan asoslangan
☐ R:R ≥ 1:2
☐ 2 soat ichida qizil yangilik yo'q
☐ Tinchman
```

#### Pozitsiyani hisoblash
```bash
.venv/bin/python tools/position_calculator.py
```

#### Savdo **OLDIN** jurnalga yozish
- Sana, vaqt, juftlik, yo'nalish
- Kirish narxi (rejalashtirilgan), SL, TP, lot
- Hissiyotlar (0-10)
- Kirish sababi

#### MT5 da savdoni ochish
- Kalkulyatordan olingan hajm
- SL va TP **darhol** order oynasida
- Buy / Sell by Market

#### **Kompyuterdan ketasiz**
- Har bir shamni ko'rmaysiz
- Savdo TP da yoki SL da yopiladi — siz boshqa uni boshqarmaysiz
- Har 5 daqiqada emas, bir soatdan keyin tekshirishingiz mumkin

---

## 🚨 AGAR SAVDO MINUS BILAN YOPILSA

### Darhol:
1. Jurnalga yozing — **natija + hissiyot**
2. Darhol yangi savdo ochmaslik
3. Kamida **30 daqiqalik pauza**

### Agar ketma-ket 2 zarar bo'lsa:
- [anti-tilt-protocol.md](anti-tilt-protocol.md) ni yoqing, 1-daraja
- Keyingi savdo uchun hajmni yarmiga kamaytiring

### Agar ketma-ket 3 zarar bo'lsa:
- **KUN UCHUN TO'XTATISH.**
- MT5 ni yoping
- «Yana bir urinish» yo'q

---

## 🏁 SESSIYA OXIRI (20:00–22:00 UTC+5)

### Tugatishdan bir soat oldin
- [ ] Yangi savdolar ochmang (kech)
- [ ] Ishlamagan kutilma orderlarni yoping

### Agar pozitsiya kechasi qolsa
- [ ] Pozitsiyani kechasi ushlab turish kerakmi?
- [ ] Svop musbat yoki manfiy?
- [ ] Osiyo sessiyasida qaysi yangiliklar bor?
- [ ] Qaror: yopish yoki qoldirish (dushanba kuni gap hisobga olingan holda)

### Kun yakunlarini chiqarish (15 daqiqa)
- [ ] Barcha savdolar jurnaldami?
- [ ] Hissiyotlar yozilganmi?
- [ ] Nechta savdo bo'ldi?
- [ ] Qancha foydali / zararli?
- [ ] Barcha qoidalarga rioya qilindimi? (% muvofiqlik)

---

## 🌙 KECHQURUN (22:00 UTC+5 dan keyin)

- [ ] **Grafiklar yopilgan**
- [ ] MT5 yig'ilgan
- [ ] Treydingga oid Telegram-kanallar — **hech qachon**
- [ ] «Qanday pul ishlash mumkin» YouTube — **hech qachon**

### Agar kotsirovkalarni tekshirgisi kelsa
- MT5 ni ochmang
- TradingView ni ochmang
- Agar juda xohlasangiz → bu **tilt simptomi**, diqqatni chalg'iting

### Ertaga tayyorgarlik
- [ ] Ertangi yangiliklar taqvimi
- [ ] Bugungi kundan nima oldingiz — bir jumla
- [ ] 23:00 gacha yotishga boring

---

## 🗓️ HAFTALIK RUTINA

### Dushanba
- Ertalab: o'tgan hafta natijalarini tahlil qilish (15 daqiqa)
- Savdo haftasining boshlanishi — **ehtiyotkorlik**, bozor dam olish kunlaridan gap berishi mumkin
- Birinchi savdoga **shoshilmang** — o'tkazib yuborgan yaxshiroq

### Chorshanba (hafta o'rtasi)
- Mini-tahlil: hafta qanday ketmoqda?
- Agar minusda bo'lsangiz — hafta oxirigacha pozitsiya hajmini yarmiga kamaytiring

### Juma
- **18:00 UTC+5 dan keyin yangi savdolar ochmaslik**
- Ochiq savdolarni 22:00 gacha yoping (dushanba gapidan qoching)
- Hafta yakunlarini chiqaring

### Shanba
- **Savdo qilmayman.** Forex bozori yopiq.
- `tools/journal_dashboard.py` ni ishga tushiring — haftalik hisobot
- Hafta xatolarini tahlil qiling
- Bir soat o'qish (treydingga yoki psixologiyaga oid kitob)

### Yakshanba
- **Treydingdan to'liq dam olish.**
- Oila, dam olish, sport
- Dushanbaga ruhan tayyorlanish

---

## 🗓️ OYLIK RUTINA

### Oyning birinchi shanbasi
- `journal/monthly_report.py --month YYYY-MM` ni ishga tushiring
- Chuqur tahlil:
  - Oy uchun win rate
  - Oy uchun PF
  - Eng yomon 3 ta savdo — nimasi umumiy?
  - Eng yaxshi 3 ta savdo — nimasi umumiy?
  - Qoidalar bo'yicha savdolar %
- mistakes-log.md ni **yangilang**
- Qaror qiling: strategiyada nimadir o'zgartiramanmi?

### Oyning oxirgi kuni
- Moliyaviy hisobat: to'ldirish, yechib olish, umumiy P&L
- Agar pul yechib olgan bo'lsangiz — hujjatlarni saqlang
- Soliqlar haqida o'ylang (agar chorak oxiri bo'lsa)

---

## 🗓️ CHORAKLIK RUTINA

Har 3 oyda:
- [ ] Trading Planni qayta o'qing
- [ ] Plan versiyasini yangilang (agar o'zgarishlar bo'lsa)
- [ ] Treydingga/psixologiyaga oid yangi bir kitob o'qing
- [ ] Strategiyaning to'liq sharhi: hali ishlayaptimi?
- [ ] Agar depozit 50%+ o'ssa — hajmni oshirish haqida o'zingiz bilan muhokama qiling

---

## ⛔ HAR KUN QILMASLIK KERAK BO'LGAN NARSALAR

- Chek-listsiz savdo ochish
- Grafik oldida >2 soat uzluksiz o'tirish
- Bir nechta qadah ichgandan keyin savdo qilish
- Jiddiy stressdan keyin birinchi soatda savdo qilish (janjal, yomon xabar)
- Dam olish kunlari terminalni «shunchaki ko'rish uchun» ochish
- Telegram dagi boshqalarning savdolarini kuzatish
- O'z natijangizni boshqaning natijasi bilan taqqoslash (YouTube «guruları» bilan)

---

## 🎯 BITTA ASOSIY G'OYA

> **Ko'proq qilma — kamroq, lekin sifatli qil.**
>
> Kundagi bitta yaxshi setup > beshta «o'rtacha».
> Bir soatlik chuqur tahlil > grafik kuzatishning 5 soati.
> Rejaga ko'ra bitta savdo > o'nta «sinab ko'rish».

Treydingda bu **marafon**, sprint emas. Rutina daholarcha sezgidan ustun.

---

## 📋 «Men savdo kuniga tayyorman» chek-listi

Har kuni ertalab tekshiring:

```
☐ ≥ 7 soat uyqladim
☐ Ovqatlandim
☐ Tinchman
☐ Chek-list stol ustida
☐ Kalkulyator ochiq
☐ Jurnal tayyor
☐ Yangiliklar taqvimi tekshirilgan
☐ Telegram-signallar (agar mavjud bo'lsa) tekshirilgan
☐ Bugungi maksimal savdolar sonini bilaman
☐ 3 ta zararda to'xtatishga tayyorman
```

**Barcha ☑ → savdo qilsa bo'ladi. Hech bo'lmaganda bitta ☐ → dam olish kuni.**

---

[← Asosiy qo'llanmaga](../forex-guide.md) · [Anti-Tilt →](anti-tilt-protocol.md)
