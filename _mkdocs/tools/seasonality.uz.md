---
widgets: [seasonality]
---

# 🗓️ Valyuta juftliklari mavsumiyligi

!!! abstract "Bu nima"
    8 juftlik × 12 oy xaritasi: qaysi oylarda juftlik **tarixan** tez-tez va
    kuchliroq o'sgan yoki pasaygan. Kunlik shamchalardan skript hisoblaydi —
    har bir katakta o'rtacha xod, mediana va ijobiy yillar ulushi.

<div id="seasonality" data-src="../../../data/seasonality.json"></div>

---

## Xaritani qanday o'qish kerak

**Rang — oyning o'rtacha xodi foizda.** Firuza — oy o'rtacha ijobiy, qizil —
salbiy. Katakka bossangiz mediana, ijobiy yillar ulushi va kuzatilgan yillar
soni ko'rinadi.

**Ochiq rangli kataklarni o'tkazib yuboring.** Har oyga to'g'ri keladigan yillar
sanab bo'lg'uday, kichik tanlovli katak — qonuniyat emas, shovqin. Foreksda
mavsumiylik aksiyalar yoki gazga qaraganda zaifroq: bu yerda hosil yoki isitish
mavsumi yo'q.

**Bitta katakka emas, tuzilishga qarang.** AUDUSD da kuchli yanvar bo'lsa —
NZDUSD da ham shunday yanvar bormi, tekshiring. Bir ishorali ikkita qo'shni
katak fon bo'la oladi; yolg'iz yorug' katak deyarli har doim bitta tasodifiy yil.

## Qanday ishlatish (va qanday ishlatmaslik) kerak

- ✅ **Reja uchun fon.** «Tarixan ehtiyotkor oy» — riskni kamaytirishga sabab,
  «albatta short»ga emas.
- ✅ **Ma'lumotga savol.** Kuchli katak — o'sha oylarda qanday hodisalar
  bo'lganini tekshirishga sabab (CPI, stavkalar), o'ziyoq signal emas.
- ❌ **Kalendar bo'yicha kirish yo'q.** 5–20 yillik o'rtacha bu oyga va'da
  bermaydi. «Mavsumiy pattern»larning yarmi keyingi o'n yillikda yashamaydi.

## Yangilash

Xarita yangi kotirovkalardan bitta buyruq bilan qayta hisoblanadi:

```bash
python tools/fetch_quotes.py && python tools/build_seasonality.py
```

## Keyingi o'qish

- [Volatillik va korrelyatsiyalar](market-analytics.md) — juftliklar kun ichida qachon yuradi.
- [Bozorda hafta](weekly-review.md) — o'tgan hafta aslida nima bo'ldi.
- [Iqtisodiy kalendar](../extras/market-data-sources.md) — kuchli oylarning sabablarini qayerdan izlash.

!!! danger "Moliyaviy maslahat emas"
    Mavsumiylik — o'tganning statistikasi, kelajakning jadvali emas. 5 yildan
    4 tasida o'sgan oy beshinchisida tushgan — va bu yil beshinchi yil bo'lishi mumkin.
