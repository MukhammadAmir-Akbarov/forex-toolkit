---
widgets: [weekly-review]
---

# 📅 Bozorda hafta: uchta eng katta harakat

!!! abstract "Bu nima"
    Sakkiz juftlik bo'yicha oxirgi to'liq haftalar arxivi: kim eng ko'p yurdi,
    bu **juftlikning o'z volatilligi (ATR) birliklarida** qancha katta va
    qaysi kuni sodir bo'ldi. ← → tugmalari haftalarni varaqlaydi. Grafik va
    raqamlar haqiqiy kotirovkalardan skript bilan hisoblanadi — bu
    taassurot emas, o'lchov.

<div id="weekly-review" data-src="../../../data/weekly-review.json"></div>

---

## Sharhni qanday o'qish kerak

**ATR dagi xod pipsdagi xoddan muhimroq.** GBP/USD da −266 pips va NZD/USD da
−112 pips turlicha eshitiladi, lekin volatillik birliklarida (−2.96 va −2.10
ATR) ko'rinadi: ikkala juftlik ham o'zining «odatiy kuni»dan deyarli uchtasini
yurdi. Haftada 2 ATR dan oshgan harakat — har doim sababli hodisa, shovqin emas.

**Pik kuni sababni qayerdan izlashni ko'rsatadi.** Butun xod bitta kunda
bo'lgan bo'lsa — o'sha kunning yangiliklar kalendarini oching: stavkalar, CPI,
NFP. Haftaga yoyilgan xod ko'pincha bitta yangilik emas, trend bo'yicha
pozitsiyalarni qayta joylashtirishdir.

**Uchtalasi ham bir yo'nalishdamı?** GBP/USD, EUR/USD va NZD/USD birga yursa,
gap funt yoki kivida emas — dollarda. Buni [korrelyatsiya xaritasi](market-analytics.md)
tekshirishga yordam beradi: bog'liq juftliklar ko'pincha umumiy harakat qiladi
va ulardagi uchta «turli» bitim bitta garov bo'lardi.

## Sababni qanday izlash kerak

1. Pik kunidagi iqtisodiy kalendarni oching (havolalar —
   [ma'lumot manbalari](../extras/market-data-sources.md) sahifasida).
2. Juftlikning ikkala valyutasi bo'yicha qizil hodisalarni belgilang.
3. [Yangiliklarda savdo protokoli](../practice/news-trading-protocol.md) bilan
   solishtiring: kirish qayerda bo'lardi va xavfiga arziydimi.

Haftada shunday 15 daqiqalik tahlil «grafik ko'rish»ni bozorni tushunishdan
ajratadi.

## Yangilash

Sahifa yangi kotirovkalardan bitta buyruq bilan qayta hisoblanadi:

```bash
python tools/fetch_quotes.py && python tools/build_weekly_review.py
```

## Keyingi o'qish

- [Volatillik va korrelyatsiyalar](market-analytics.md) — juftliklar qachon yuradi va kim birga yuradi.
- [Savdo sessiyalari](../practice/trading-sessions.md) — bunday kunlar qaysi soatlarda bo'ladi.
- [Yangiliklar protokoli](../practice/news-trading-protocol.md) — pik kunida nima qilish kerak.

!!! danger "Moliyaviy maslahat emas"
    O'tgan hafta tahlili — o'quv mashg'uloti, keyingi haftaga bashorat emas.
    −3 ATR lik harakat katta bo'lgani uchun ham «qaytishi shart» emas.
