---
widgets: [news-sim]
---

# 📰 Yangiliklar simulyatori: NFP chiqqanda nima qilish kerak

!!! abstract "Bu nima"
    Har bir treyder duch keladigan oltita vaziyat: 10 daqiqadan keyin qizil
    yangilik chiqadi, pozitsiya esa ochiq; raqam chiqdi va narx uchib ketyapti;
    Telegramdagi «insayd». Siz harakatni tanlaysiz va darhol
    [yangiliklar asosida savdo protokoli](../practice/news-trading-protocol.md)
    bo'yicha tahlilni, bozorning odatiy reaksiyasini va **tarixdan haqiqiy
    holatni** ko'rasiz.

<div id="ns-widget"></div>

<script type="application/json" id="ns-scenarios">
[
  {
    "event": "🇺🇸 AQSH inflyatsiyasi (CPI) 10 daqiqadan keyin",
    "situation": "Sizda USD/JPY bo'yicha long: +40 pips foyda, stop kirishdan 30 pips pastda. Tahlilchilar yuqori inflyatsiyani kutmoqda — «dollar faqat mustahkamlanadi».",
    "options": [
      {"text": "Pozitsiyani reliz oldidan yopish", "verdict": "best", "why": "CPI — 1-darajali voqea: daqiqalar ichida istalgan tomonga 50–150+ pips. Foyda relizdan keyin emas, relizdan oldin fiksatsiya qilinadi."},
      {"text": "Stopni breakevenga o'tkazib, ushlab turish", "verdict": "ok", "why": "Hech narsadan yaxshi, lekin relizda spred kengayadi va stop slippage bilan, ya'ni breakevendan pastda bajarilishi mumkin."},
      {"text": "Pozitsiyani oshirish — tahlilchilar ishonchli-ku", "verdict": "bad", "why": "Tahlilchilarning kutishlari allaqachon narxda. Raqam prognozdan past chiqsa, ikki baravar pozitsiya zarbani ham ikki baravar qiladi."},
      {"text": "Stopni olib tashlash, uni «igna» urib tushirmasin", "verdict": "bad", "why": "Stopsiz zarar hech narsa bilan cheklanmaydi, CPI dan keyin esa juftlik kun davomida yuzlab pipsga ketishi mumkin."}
    ],
    "reaction": "Prognozga qarshi syurpriz dollarni keskin va uzoq muddatga harakatlantiradi: dastlabki daqiqalarda keng spredda sakrash, keyin harakat ko'pincha kun bo'yi davom etadi.",
    "history": "2022-yil 10-noyabrda AQSH inflyatsiyasi kutilgan ≈8% o'rniga ≈7,7% bo'ldi. Dollar keskin arzonlashdi: USD/JPY taxminan 146–147 dan ≈141–142 gacha tushdi (≈−3–4%), EUR/USD esa ≈2 sentga o'sdi."
  },
  {
    "event": "🇺🇸 NFP prognozdan ancha kuchli chiqdi",
    "situation": "Pozitsiyalaringiz yo'q. Ortda olti oylik demo, savdo rejangizda esa yangiliklarda kirish qoidasi bor. Raqam prognozdan ancha yaxshi, EUR/USD 10 soniyada 60 pips tushdi — hoziroq sotgingiz keladi.",
    "options": [
      {"text": "Narx uchib turganda darhol bozor narxida sotish", "verdict": "bad", "why": "Bu soniyalarda spred eng katta, market-order esa 5–30 pips slippage bilan bajariladi. Siz vahimaning aynan tubida sotasiz."},
      {"text": "5–15 daqiqa kutib, qaytish o'tib ketishi va spred torayishini kutish, so'ng o'z tizimingiz bo'yicha limit-order bilan kirish", "verdict": "best", "why": "Protokoldagi «Chang cho'kishini kut» strategiyasi: yo'nalish allaqachon ko'rinadi, narx va spred esa to'g'ri bo'ladi."},
      {"text": "Bu relizni o'tkazib yuborib, shunchaki kuzatish", "verdict": "ok", "why": "Xavfsiz va foydali. Lekin sizda yangiliklarda kirish qoidasi bor, protokol bo'yicha qaytishdan keyin kirish ham joiz."},
      {"text": "Ikki baravar lot ochish: harakat-ku kafolatlangan", "verdict": "bad", "why": "Kafolat yo'q: 1–5 daqiqadan keyin narx ko'pincha birinchi harakatning 30–50% iga qaytadi. Shunday qaytishda ikki baravar lot — ikki baravar zarar."}
    ],
    "reaction": "Dastlabki soniyalarda narx sakraydi, spred bir necha baravar kengayadi. 1–5 daqiqadan keyin ko'pincha birinchi harakatning 30–50% iga qaytish (shakeout) bo'ladi, kun yo'nalishi esa 15–30 daqiqada shakllanadi.",
    "history": "2023-yil 3-fevralda AQSHda prognoz qilingan ≈190 ming o'rniga ≈517 ming yangi ish o'rni paydo bo'ldi; ishsizlik 3,4% gacha tushdi — 1969-yildan beri eng past daraja. EUR/USD kun davomida ≈1% pasayib, ≈1,08 ga tushdi."
  },
  {
    "event": "🇨🇭 EUR/CHF 1,20 «pol»i uch yildan beri ushlab turibdi",
    "situation": "Shveytsariya Milliy banki uch yildan beri EUR/CHF ni 1,20 dan pastga tushirmaslikka va'da bermoqda. Juftlik 1,2010 atrofida. G'oya: deyarli risksiz long — 1,20 dan pastga «qo'yishmaydi», stop 30 pipsda.",
    "options": [
      {"text": "Yelkani kattaroq olish: risk atigi 30 pips", "verdict": "bad", "why": "30 pipsli stop faqat oddiy bozorda himoya qiladi. Pol bekor qilinsa, narx stopdan sakrab o'tadi va zarar hisoblanganidan o'nlab baravar ko'p bo'ladi."},
      {"text": "30 pipsli stop bilan odatiy 1% risk", "verdict": "ok", "why": "Intizomli, lekin hisob faqat narx bo'shlig'isiz to'g'ri: pol buzilsa, stop ancha pastda bajariladi va 1% ko'p marta katta zararga aylanadi."},
      {"text": "Narx bo'shlig'iga zaxirali kichik hajm va manfiy balansdan himoyasi bor broker", "verdict": "best", "why": "Markaziy bank va'dasi — kafolat emas. Hajm faqat stop ishga tushishiga emas, narx bo'shlig'iga ham bardosh beradigan qilib hisoblanadi."},
      {"text": "Stopsiz — 1,20 dan pastga baribir qo'yishmaydi", "verdict": "bad", "why": "Bu butun depozitni Markaziy bank so'ziga tikish. So'z esa ogohlantirishsiz o'zgaradi."}
    ],
    "reaction": "Markaziy bank to'satdan siyosatni o'zgartirganda likvidlik bo'lmaydi: narx yurmaydi, balki darajalardan sakrab o'tadi. Stop-orderlar birinchi mavjud narxda bajariladi — ba'zan belgilangan narxdan yuzlab pips narida.",
    "history": "2015-yil 15-yanvarda Shveytsariya Milliy banki ogohlantirishsiz EUR/CHF = 1,20 quyi chegarasidan voz kechdi. Bir necha daqiqada juftlik taxminan 0,85–0,90 gacha tushdi: yevro frankka nisbatan ≈25–30% arzonlashdi. Stoplar belgilanganidan ancha yomon bajarildi; FXCM brokeri ≈$300 mln qutqaruv qarzi oldi, Alpari UK esa bankrot bo'ldi."
  },
  {
    "event": "🇬🇧 Tunda — referendum natijalari",
    "situation": "Kechqurun siz GBP/USD da longdasiz: so'rovnomalar Britaniya YeI da qolishini va'da qilmoqda. Natijalar tunda, siz uxlab yotganingizda e'lon qilinadi.",
    "options": [
      {"text": "Pozitsiyani tungacha yopish: oqibat binar, siz esa terminal oldida emassiz", "verdict": "best", "why": "Protokol bo'yicha 1-darajali voqealarda pozitsiyalar yopiladi. So'rovnomalar natija emas, tunda esa javob beradigan hech kim yo'q."},
      {"text": "Minimal hajmgacha qisqartirib, stop qo'yish", "verdict": "ok", "why": "Risk kamroq, lekin tunda stop narx bo'shlig'i bilan bajarilishi mumkin — stopgacha bo'lganidan ko'proq yo'qotishingizni hisobga oling."},
      {"text": "Hozirgidek ushlab turish — so'rovnomalar-ku «qolish» tarafida", "verdict": "bad", "why": "So'rovnomalar adashadi. To'liq hajmni binar voqea orqali ushlab turish — butun riskni tanga tashlashga tikish."},
      {"text": "Pozitsiyani oshirish: bozor hali «qolish»ga to'liq ishonmayapti", "verdict": "bad", "why": "Bu tahlil emas, balki ovoz berish natijasiga maksimal hajm bilan va tungi narx bo'shlig'idan himoyasiz tikish."}
    ],
    "reaction": "Binar voqealar (referendumlar, saylovlar) narx bo'shliqlarini beradi: bozor valyutani daqiqalar ichida qayta baholaydi, tunda likvidlik yupqa, stoplar belgilanganidan yomonroq bajariladi.",
    "history": "2016-yil 24-iyunga o'tar kechasi, referendum natijalari ma'lum bo'lganda, GBP/USD taxminan 1,50 dan ≈1,33 gacha tushdi (≈−10%). Bu 1985-yildan beri eng past daraja."
  },
  {
    "event": "🇯🇵 Yaponiya Moliya vazirligi: «qat'iy harakat qilishga tayyormiz»",
    "situation": "USD/JPY 152 atrofida — o'nlab yillardagi maksimum. Siz yaxshi foydali longdasiz. Yaponiya hokimiyati haftalardan beri mumkin bo'lgan intervensiya haqida ogohlantirmoqda.",
    "options": [
      {"text": "Foydaning bir qismini fiksatsiya qilib, qolganini slippage bilan ham yo'qotishdan qo'rqmaydigan stop bilan ushlab turish", "verdict": "best", "why": "Hokimiyat ogohlantirishlari — qizil bayroq. Trend davom etishi mumkin, lekin keskin burilish riski endi boshqacha."},
      {"text": "Butun pozitsiyani yopish", "verdict": "ok", "why": "Xavfsiz. Kamchiligi faqat trenddan butunlay chiqib ketasiz; tizimingiz qoidalari shuni talab qilsa — bu normal."},
      {"text": "Qo'shib olish: trend kuchli, baribir intervensiya bo'lmaydi", "verdict": "bad", "why": "Hokimiyatning to'g'ridan-to'g'ri ogohlantirishlariga qaramay pozitsiyani oshirish — ular blef qilyapti degan tikish."},
      {"text": "Stopni olib tashlash, o'zgaruvchanlik uni urib tushirmasin", "verdict": "bad", "why": "Intervensiya narxni soatlar ichida yuzlab pipsga siljitadi. Stopsiz bu endi o'zgaruvchanlik emas, cheksiz zarar."}
    ],
    "reaction": "Intervensiya oldindan e'lon qilinmaydi: harakat to'satdan, ko'pincha yupqa bozorda boshlanadi va soatlar ichida yuzlab pipsni bosib o'tadi.",
    "history": "2022-yil 21-oktabrda USD/JPY ≈152 ga yetdi — 32 yillik maksimum. Keyin Yaponiya Moliya vazirligi intervensiya o'tkazdi va bir necha soatda juftlik taxminan 146 gacha tushdi. Oktabr oyida Yaponiya rekord ≈6,3 trln iyena (≈$43 mlrd) sarfladi."
  },
  {
    "event": "📱 Telegram-kanaldagi «insayd»",
    "situation": "Mashhur kanal yozadi: «Shoshilinch! Fed bir soatdan keyin favqulodda stavkani tushiradi». Iqtisodiy kalendarda hech narsa yo'q, Fed sayti jim.",
    "options": [
      {"text": "Hamma bilib olmasidan oldin darhol dollarni sotish", "verdict": "bad", "why": "Siz manbasiz mish-mishni savdo qilyapsiz. Soxta bo'lsa, harakat daqiqalar ichida sizga qarshi aylanadi."},
      {"text": "Rasmiy manbalarni tekshirib, tasdiq bo'lmaguncha hech narsa qilmaslik", "verdict": "best", "why": "Tasdiqlangan ma'lumotlar savdo qilinadi: kalendar, markaziy bank sayti, yirik agentliklar. Manbasiz mish-mish — signal emas."},
      {"text": "Kirmaslik, lekin har ehtimolga qarshi o'z pozitsiyalarini yopish", "verdict": "ok", "why": "Ehtiyotkor, lekin asossiz: siz mish-mishga reaksiya uchun spred to'laysiz. Avval manbani tekshiring."},
      {"text": "Kech bo'lmasidan katta yelka bilan pozitsiya ochish", "verdict": "bad", "why": "Tekshirilmagan mish-mishda maksimal hajm — soxta yangiliklar hisoblarni aynan shunday bo'shatadi."}
    ],
    "reaction": "Yolg'on yangilik narxni soniyalar yoki daqiqalarga siljitadi — u rad etilguncha. Keyin harakat orqaga qaytadi va oxirgi bo'lib sakragan treyderlar eng yomon narxlarda chiqadi.",
    "history": "2013-yil 23-aprelda xakerlar AP agentligining Twitter-akkauntini buzib, «Oq uydagi portlashlar» haqida yozdi. Dow Jones indeksi daqiqalar ichida taxminan 140–150 punktga (≈1%) tushdi, S&P 500 bir lahza ≈$135 mlrd kapitalizatsiyani yo'qotdi — bozor esa pasayishni bir necha daqiqada qaytarib oldi."
  }
]
</script>

---

## Natija qanday hisoblanadi

| Yurish | Ball | Nimani anglatadi |
|---|---|---|
| ✅ Protokol bo'yicha eng yaxshi | 2 | Professionallar hisobni shunday himoya qiladi |
| 🟡 Joiz, lekin riskli | 1 | Falokat emas, lekin risk sizda qoladi |
| ❌ Xavfli | 0 | Yangiliklar hisoblarni aynan shunday bo'shatadi |

80% va undan yuqori — protokol sizning boshingizda. 50% dan past — haqiqiy
yangiliklarda hali erta: avval demo va kuzatuv. Xavfli yurishlar avtomatik
ravishda «🔁 Mening xatolarim» filtri bilan [flesh-kartochkalarga](flashcards.md)
tushadi — ularni takrorlang.

## Barcha stsenariylar tayanadigan uchta qoida

1. **Qizil yangilik oldidan pozitsiya yopiladi** yoki hech bo'lmasa
   breakevenga o'tkaziladi — va relizda stop slippage bilan bajarilishi
   mumkinligini unutmang.
2. **Reliz lahzasida hech narsa qilinmaydi.** Kirish — 5–15 daqiqadan keyin,
   qaytishda, limit-order bilan, o'z tizimingiz qoidalari bo'yicha.
3. **Markaziy bank va'dalari, so'rovnomalar va mish-mishlar — kafolat emas.**
   Hajm faqat stop ishga tushishiga emas, narx bo'shlig'iga ham bardosh
   beradigan qilib hisoblanadi.

Batafsil — [yangiliklar asosida savdo protokolida](../practice/news-trading-protocol.md)
va [fundamental tahlil qo'llanmasida](../docs/fundamental-analysis-guide.md).

## Tarixiy misollar manbalari

Raqamlar yaxlitlangan: turli manbalar minimum va maksimumlarni biroz boshqacha beradi.

- AQSH CPI, 10.11.2022 — [Bloomberg](https://www.bloomberg.com/news/articles/2022-11-10/dollar-dives-as-cpi-surprise-cuts-fed-interest-rate-hike-outlook), [CNBC](https://www.cnbc.com/2022/11/11/dollar-dives-investors-cheer-after-us-inflation-misses-forecasts.html)
- NFP, 03.02.2023 — [CNBC](https://www.cnbc.com/2023/02/03/jobs-report-january-2023-.html)
- SNB, 15.01.2015 — [CRS](https://www.everycrsreport.com/reports/IN10230.html), [FCA Alpari UK haqida](https://www.fca.org.uk/news/statements/news-customers-alpari-uk-limited)
- Brexit referendumi, 24.06.2016 — [CNN Money](https://money.cnn.com/2016/06/24/investing/pound-crash-eu-referendum/)
- Yaponiya intervensiyasi, 21.10.2022 — [Yaponiya Moliya vazirligi](https://www.mof.go.jp/english/policy/international_policy/reference/feio/quarter/2022_4Qe.html)
- AP Twitter-akkaunti buzilishi, 23.04.2013 — [Bloomberg](https://www.bloomberg.com/news/articles/2013-04-23/a-fake-ap-tweet-sinks-the-dow-for-an-instant)

!!! danger "Moliyaviy maslahat emas"
    Simulyator yangiliklar atrofida hisobni himoya qilishni o'rgatadi, ularning
    oqibatini topishni emas. Tarixiy harakatlar riskni tushunish uchun
    ko'rsatilgan, prognoz sifatida emas.
