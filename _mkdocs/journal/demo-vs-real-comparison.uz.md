# Demo vs Real — qiyosiy tahlil

> Demo hisobdan haqiqiy hisobga o'tganda natijalar ko'pincha YOMONlashadi. Bu fayl **nima uchun** aynan senda shunday bo'lishini tushunishga yordam beradi.

## Nima uchun taqqoslaymiz

Haqiqiy hisobda:
- 😰 Psixologiya butunlay boshqacha
- 💸 Hissiyotlar qarorga aralashadi
- 📊 Spread va slippage haqiqiy
- 🐢 Ijro sekinroq bo'lishi mumkin
- 🕰️ Bo'sh vaqt kamroq (vahima = xatolar)

Taqqoslashning maqsadi: **aynan senda o'tishda nima SINISHI**ni topish.

---

## Taqqoslash uchun ko'rsatkichlar

Ikkita jurnal parallel yurgiz: biri demo uchun, biri real uchun. Har 2 haftada bir taqqosla.

### Jadval shabloni

```markdown
## YYYY-MM-DD — YYYY-MM-DD davr uchun taqqoslash

| Ko'rsatkich | Demo | Real | Farq | Norma |
|---|---|---|---|---|
| Savdolar | __ | __ | | |
| Win rate | __% | __% | __% | farq < 10% |
| Profit Factor | __ | __ | | real ≥ 70% of demo |
| Avg Win (R) | __ | __ | | farq < 0.3R |
| Avg Loss (R) | __ | __ | | real ≤ 1.2R (demo dan oshmasin) |
| Max DD | __% | __% | | real juda oshmasligi kerak |
| Qoidaga mos savdolar % | __% | __% | | real ≥ 90% of demo |
| Qo'lda yopilgan savdolar % | __% | __% | | real o'smasligi kerak |
| Kunlik savdolar | __ | __ | | real ≈ demo |
```

---

## Farq sabablari tahlili

Agar real hisobdagi natija yomonroq bo'lsa — savol ber:

### 🧠 Psixologik sabablar

- [ ] Men savdolarni **kamroq ochyapman** (qo'rquv)?
- [ ] Men savdolarni TP dan **oldin yopyapman** (foyda yo'qolishidan qo'rquv)?
- [ ] Men **stoplarni** uzoqlashtiraman (umid bilan)?
- [ ] Men «har ehtimolga qarshi» pozitsiya hajmini **kamaytiraman**?
- [ ] Men «ishonchim komil» deganda hajmni **oshiraman**?
- [ ] Men bir qator zarardan keyin yaxshi setaplardan **qochaman**?

**Agar kamida 1 ta — ha:** muammo **intizomda**, strategiyada emas.

### 💰 Texnik sabablar

- [ ] Haqiqiy spread demo-servernikidan katta
- [ ] Kirish vaqtida slippage (siljish)
- [ ] Stop vaqtida slippage
- [ ] Haqiqiy kotirovkalar demo dan farq qilishi mumkin
- [ ] Svoplar (overnight) uzoq muddatli savdolarni kamaytiradi

**Agar shunday bo'lsa:** jurnalga «haqiqiy kirish narxi vs rejalashtirilgan» maydonini qo'sh — farqni ko'rasan.

### ⏰ Savdo sharoitlari

- [ ] Bo'sh vaqt kamroq → setaplarni o'tkazib yuboraman
- [ ] Noqulay vaqtda savdo qilyapman
- [ ] Charchoq to'planib bormoqda
- [ ] Savdo oldidan tahlilga vaqt kamroq

---

## Normaga qaytish taktikalari

### Agar win rate 20+% ga tushib ketsa

**Muammo:** sen qoidalarni shu zahotda buzmoqdasan.

**Yechim:**
1. Haqiqiy pozitsiya hajmini **5 marta** kamaytir
2. Har bir savdo oldidan qog'oz chek-listni jismoniy belgilab o't
3. Savdolar sonini kuniga 1-3 tagacha **qisqartir**
4. Har bir savdo oldidan **hissiyotni** yoz (0-10)
5. 2-4 hafta ichida normaga qaytasan — hajmni asta-sekin oshirasan

### Agar win rate demoga yaqin, lekin foyda kamroq bo'lsa

**Muammo:** qo'shimcha xarajatlar.

**Yechim:**
1. **Spread** qancha yeyishi ni hisoblang (ko'pincha foydaning 10-15%)
2. Hisobda **komissiya** borligini tekshiring
3. 1 kundan ortiq savdolarda **svoplarni** hisobga ol
4. Agar farq > 20% bo'lsa — ehtimol tor spreadli ECN-hisob kerak

### Agar kichikroq pozitsiyalar qo'yayotgan bo'lsam (qo'rquv)

**Muammo:** demo-psixologiya va real-psixologiya o'rtasidagi bo'shliq.

**Yechim:**
1. **Cent-hisobdan** boshlang: $10 = 1000 sent. Psixologik jihatdan og'riq kamroq.
2. Odatlanib ketgandan so'ng — oddiy hisob, lekin pozitsiya hajmi **hisob-kitobdan 5 marta kichik**
3. Asta-sekin (oyiga 20% ga) hisob-kitobga ko'taring

---

## «Realga o'tish» nazorat ro'yxati

Birinchi haqiqiy hisobdan oldin tekshiring:

- [ ] Demoda kamida **3 oy** barqaror musbat natija
- [ ] Demoda win rate barqaror ≥ 40%
- [ ] Demoda Profit Factor ≥ 1.5
- [ ] Savdolarning 5% dan kamrog'i qoidabuzarlik bilan
- [ ] Jurnal demoda **har bir savdo** bo'yicha yuritilgan
- [ ] Boshlang'ich summa — **$100–$300** (ko'pi emas)
- [ ] Bu summani **to'liq yo'qotishga tayyor**san
- [ ] Hayotingiz bu pulga bog'liq emas

Agar **hammasi** ☑ bo'lsa — realga o'tishingiz mumkin. Agar biron narsa **yo'q** bo'lsa — hali erta.

---

## Realga o'tishdan oldin psixologik trening

O'tishdan 2 hafta oldin:

1. **Har bir** demo-savdoni ovoz chiqarib ayt: «EUR/USD bo'yicha long ochyapman, stop 25 pips, teyk 50 pips, xavf $5...»
2. Bu **haqiqiy pul** ekanini tasavvur qil. Stop urilganda og'riqmi? **Hajmni kamaytir.**
3. **Demoni platformada «real» nomi bilan oc** — miyangni aldab qo'y
4. Kun davomida **qoidani buzgim keldi** deya necha marta o'ylashingni sanab tur. Qancha kam bo'lsa — realga shuncha tayyor ekansiz.

---

## Yakuniy fikr

Demo bu **kompyuterdagi parvoz simulyatori** kabidir. Real esa **haqiqiy samolyot** kabidir. Bilim jihatidan bir xil, lekin **his-tuyg'ular butunlay boshqacha**. Bosqichma-bosqich o'tish + qattiq jurnal = yagona yo'l.

---

[← Jurnalga qaytish](trading-journal-template.md)
