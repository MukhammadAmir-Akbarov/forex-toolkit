---
widgets: [dom-trainer]
---

# 🧱 Stakan va lenta trenajyori

!!! abstract "Bu nima"
    Order flow'ni o'rganishning yagona yo'li — **amaliyot**, yana bitta maqola emas.
    Oldingizda stakan (DOM) va bitimlar lentasi simulyatori: 25 tikni kuzatasiz,
    keyin lenta to'xtaydi — va keyingi 5 tik qayerga borishini taxmin qilasiz.
    Stakan disbalansi bu yerda **zaif, lekin haqiqiy** signal beradi — xuddi jonli bozordagi kabi.

<div id="dom-trainer"></div>

---

## Qanday o'ynash kerak

1. **«Raundni boshlash»** tugmasini bosing — 25 tikni shunchaki kuzating:
   stakanning qaysi tomonida hajm ko'proq, lentada qanday printlar kelyapti,
   yiriklari bormi.
2. Lenta to'xtaydi. Keyingi 5 tik uchun **⬆ Yuqori** yoki **⬇ Past** ni tanlang.
3. Tahlilni o'qing: to'g'ri topdingizmi va disbalans natija bilan qanday bog'liq edi.
4. Seriya — 10 raund. Eng yaxshi natija brauzerda saqlanadi.

## Qanday natija mahorat hisoblanadi

**10 tadan 7+** — disbalansni tangadan yaxshi o'qiysiz. **10 tadan 5–6** —
tasodifiy taxmin darajasi: xafa bo'lmang, trenajyorning asosiy sabog'i aynan shu.
Stakan **javob emas, ehtimol** beradi va signal ataylab zaif qilingan —
haqiqiy bozorda spred va shovqin undan ham ko'proqni yeydi.

Stakan bo'yicha «narx qayerga borishini ko'rish» mumkin deb va'da beruvchi
illyuziya sotyapti. Haqiqiy mahorat — ehtimol biroz yuqori paytni bilish va
faqat risk-menejment ustunligi bilan savdo qilish.

## Jonli bozorga nima o'tkaziladi

- **Disbalans oxirgi printdan muhimroq.** Bitta yirik print — shovqin; bir
  tomonda barqaror hajm ustunligi — allaqachon ma'lumot.
- **Disbalansga qarshi yirik print ko'pincha tuzoq.** Katta orderning narx
  harakatlanmay yutilishi orderning o'zidan ko'proq gapiradi.
- **Prognoz — ehtimolga garov.** To'g'ri o'qish ham 10 dan 3–4 marta yutqazadi.
  Shu sabab hech qanday mahorat stop'suz ishlamaydi.

## Keyingi o'qish

- [Order Flow / Volume Profile](../growth/order-flow-volume-profile.md) — nazariya: delta, absorbsiya, hajm profili.
- [Bozor tuzilishi](../practice/market-structure.md) — bu 5 tik katta masshtabda qayerga ketadi.
- [Replay trenajyori](replay-trainer.md) — xuddi shu mashq, lekin shamchalarda.

!!! danger "Moliyaviy maslahat emas"
    Simulyatsiya — o'quv modeli, daromad va'dasi emas. Trenajyordagi signal
    haqiqiy stakan disbalansidan kuchliroq va spred, slippaj hamda komissiyalarni
    hisobga olmaydi. Bu yerdagi 10 dan 7 jonli hisobdagi 70% emas.
