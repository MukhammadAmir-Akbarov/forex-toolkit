---
widgets: [broker-check]
verified: 2026-08-06
---

# Brokerni tekshirish

!!! abstract "Bu vosita nima qiladi"
    Beshta regulyatorning rasmiy reyestrlariga to'g'ridan-to'g'ri havolalar
    tuzadi, loyiha ma'lumotnomasidagi litsenziya tarixini ko'rsatadi va qizil
    bayroqlarni belgilashga yordam beradi. Qarorni siz qabul qilasiz — sayt
    hech kimni "tasdiqlamaydi".

!!! danger "Yangi boshlovchining eng qimmat xatosi — yomon savdo emas"
    Yomon savdo bitta risk turadi. Pulni yechib bo'lmaydigan kontora esa butun
    depozitni oladi. Litsenziyani birinchi to'lovdan **oldin** tekshiring,
    birinchi muammodan keyin emas.

<div id="broker-check-widget"></div>

## Nega bitta litsenziya yetarli emas

Yirik brokerlarda odatda bir necha yuridik shaxs bo'ladi:

| Yuridik shaxs | Kimlar uchun | Himoya |
|---|---|---|
| Yevropa / Britaniya | YeI va Buyuk Britaniya mijozlari | qat'iy: kompensatsiya fondlari, yelka chegarasi |
| Ofshor | ko'pincha bizning mintaqa mijozlari | zaif: nizolar ofshor qonuni bo'yicha hal qilinadi |

Broker sayti FCA haqida gapirishi mumkin, hisobingiz esa ofshor kompaniyada
ochiladi. Shuning uchun asosiy savol "umuman litsenziya bormi" emas, balki
**"hisobim qaysi yuridik shaxsga ulanadi"**.

## Reyestrni qanday tekshirish kerak

1. Yuqoridagi vidjetdan regulyator havolasini oching.
2. Kompaniyani nomi bo'yicha toping — u shartnomadagi nom bilan mos kelishi
   kerak, saytdagi brend bilan emas.
3. Holatini tekshiring: litsenziya amaldami yoki bekor qilinganmi.
4. Manzil va litsenziya raqamini broker saytining pastki qismidagilar bilan
   solishtiring.

Agar kompaniya reyestrda bo'lmasa, broker esa tartibga solinishini da'vo qilsa —
bu to'liq javob.

## Yana nima o'qish kerak

- [Firibgarlikdan himoya](../uz/scam-protection.md) — sxemalar qanday ishlaydi va
  pul allaqachon chiqmayotgan bo'lsa nima qilish kerak.
- [O'zbekiston uchun brokerlar](../uz/brokers-uz.md) — tanlashda nimaga e'tibor berish.
- [Pulni yechish](../uz/withdrawal-guide.md) — yo'llar va komissiyalar.

Xuddi shu vosita terminalda ham bor: `forex-broker-check "IC Markets"` yoki
`python tools/broker_check.py "IC Markets"`.

!!! warning "Moliyaviy maslahat emas va brokerlar reytingi emas"
    Loyiha aniq brokerlarni tavsiya qilmaydi va ulardan haq olmaydi. Litsenziya
    ma'lumotlari tarixiy mo'ljal bo'lib, eskiradi; yagona haqiqat manbai —
    regulyatorning rasmiy reyestri.
