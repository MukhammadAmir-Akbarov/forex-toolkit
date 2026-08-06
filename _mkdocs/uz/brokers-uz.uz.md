---
verified: 2026-06-11
---

# 🏦 O'zbekistonlik treyderlar uchun brokerlar

!!! tip "Pul kiritishdan oldin brokerni tekshiring"
    [Brokerni tekshirish](../tools/broker-check.md) FCA, CySEC, ASIC, NFA va FINMA
    reyestrlariga to'g'ridan-to'g'ri havolalar tuzadi va qizil bayroqlarni belgilashga yordam beradi.


!!! warning "O'quv materiali"
    Bu bo'lim — ma'lum variantlarning sharhi. **Reklama emas.** Hisob ochishdan oldin **o'zing tekshir**: joriy regulyatsiya, sharhlar va shartlar.

## Regulyatsiya

O'zbekistonda **maxsus forex-regulyator yo'q**. Mahalliy banklar to'g'ridan-to'g'ri forex-savdosini taqdim etmaydi. Ko'pgina o'zbek treyderlar nufuzli organlar tomonidan nazorat qilinadigan **xorijiy brokerlar**dan foydalanadi:

| Regulyator | Mamlakat | Ishonch darajasi |
|---|---|---|
| **FCA** | Buyuk Britaniya | 🟢 Juda yuqori |
| **CySEC** | Kipr / EU | 🟢 Yuqori (EU standarti) |
| **ASIC** | Avstraliya | 🟢 Yuqori |
| **FSCA** | JAR | 🟡 O'rta |
| **CBCS** | Kyurasao | 🔴 Past (tezkor ro'yxatdan o'tish) |
| **SVG FSA** | Sent-Vinsent | ⛔ Haqiqiy regulyatsiya hisoblanmaydi |

**Qoida**: regulyator qanchalik qattiq bo'lsa, undan «pul olish» shunchalik qiyin, lekin skamlarga tushish ehtimoli ham shuncha kam.

## Taniqli brokerlar (verifikatsiya talab etiladi)

!!! danger "Bu ro'yxatga ishonma — o'zing tekshir"
    Bu ro'yxat oxirgi commit sanasida tuzilgan. Brokerlar **yopiladi, shartlarini o'zgartiradi, sanksiyalarga tushadi**. Hisob ochishdan oldin:

    1. Regulyator saytida joriy regulyatsiya holatini tekshir
    2. ForexPeaceArmy / Trustpilot'da yangi sharhlarni qidir
    3. Avvalo faqat **demo-hisob** och — ishlashini ko'r
    4. Real depozit — chiqarib olishni sinash uchun $100 dan oshirma

### Kategoriyalar (tavsiyasiz)

- **FCA/ASIC litsenziyali global ECN-brokerlar**: IC Markets, Pepperstone, FP Markets
- **CySEC litsenziyali market-meykerlar**: XM, Exness, FxPro, HF Markets
- **Arzon offshorlar**: yuqori leverage taklif etadi, lekin mablag' himoyasi minimal

## O'zbekiston uchun xususiyatlar

### To'ldirish / yechib olish usullari

[Pul yechib olish bo'yicha qo'llanma](withdrawal-guide.md)ga qarang (batafsil).

Qisqacha:
- **Visa/Mastercard**: ikki tomonlama ishlaydi, komissiya 1-3%
- **USDT (Tether)**: eng arzon va tez — Binance / Bybit orqali
- **Wise / Payeer**: vositachi, limitlar bor
- **SWIFT-o'tkazma**: faqat katta summalar uchun ($5000+)

### Soliqqa tortish

O'zbekistonda forex daromadi rasman **12% JSHIT** bilan soliqqa tortiladi. Amalda soliq organlari kamdan-kam tekshiradi, lekin **bu sizning majburiyatingiz** — deklaratsiya qiling. Hisoblash uchun `uz/tax-calculator.py`ga qarang.

### Mamlakatga munosabat

Yaxshi broker UZ-rezidentlarni **cheklamasligi kerak**. Ro'yxatdan o'tish uchun VPN yoki proksi talab qilsa — bu yomon belgi.

## Broker tanlash chek-listi

- [ ] Regulyatsiya: FCA, ASIC yoki CySEC (kamida)
- [ ] ECN-hisobda EUR/USD spreadi: ≤ 1 pip (komissiasiz: ≤ 1.5)
- [ ] Minimal depozit: ≤ $100
- [ ] Mikro-lotlar mavjud (0.01)
- [ ] Rus yoki ingliz tilida qo'llab-quvvatlash (mashina tarjimasi emas)
- [ ] Pul yechib olish ≤ 5 ish kuni
- [ ] Mustaqil platformalarda 3.5 dan yuqori reyting (kamida 100 sharh)
- [ ] Marketingda «kafolatlangan daromad» tilga olinmaydi

---

## Broker haqida xabar berish

Broker haqida dolzarb ma'lumotingiz bo'lsa (ijobiy tajriba, salbiy tajriba, shartlar o'zgarishi), **[Discussion](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/discussions) oching** yoki bu faylni yangilash uchun PR yuboring. Tajribani bo'lishamiz — hamjamiyatga tuzoqlardan qochishga yordam beramiz.

Shuningdek umumiy [Brokerlarni solishtirish](../extras/brokers-comparison.md)ga qarang (xalqaro).
