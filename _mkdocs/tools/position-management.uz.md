---
widgets: [position-management]
---

# 🎚️ Savdo ochiq turganda nima qilish kerak

!!! abstract "Bu o'quv yo'lidagi bo'shliq edi"
    «Savdodan oldin» riskni hisoblaydi. Jurnal natijani tahlil qiladi. Qarorlar
    esa **ular orasida** qabul qilinadi — va keyin jurnal aynan shular uchun
    qoidabuzarlik qo'yadi: stopni ko'chirdi, erta yopdi, ortiqcha ushlab turdi.
    Sababini mashq qiladigan joy yo'q edi.

    Bu yerda savdo allaqachon ochiq. Stop — bitta ATR, maqsad — 2R, oldinda 15
    ta haqiqiy arxiv shami. Nima qilishingizni tanlang va ikkita raqamni
    ko'ring: shu savdoda nima chiqqani va o'sha reja arxivdagi 160 ta savdoda
    nima bergani.

<div id="position-management" data-src="../../../data/replay-episodes.json"></div>

---

## Arxiv nima ko'rsatdi

80 epizod ikki tomonga — 160 savdo. Bir xil kirish, bir xil stop, kirishdan
keyin turlicha xatti-harakat.

| Reja | Jami | «Shunchaki ushlash»ga nisbatan | Yordam berdi | Zarar qildi |
|---|---|---|---|---|
| Shunchaki ushlash | −10.9R | — | — | — |
| +1R da zararsizlik | **−16.5R** | **−5.5R** | 25 | 18 |
| +1R da yarmini yopish | **−3.5R** | **+7.5R** | 32 | **41** |
| 1R trayl | −9.2R | +1.8R | 28 | 24 |

## Uchta xulosa, ikkitasi kutilmagan

**Zararsizlik — eng mashhur maslahat — eng yomoni bo'lib chiqdi.** U maqsadga
yetadigan savdolardan chiqarib yuboradi: narx +1R ga bordi, kirishga qaytdi va
faqat keyin kerakli tomonga ketdi. U 25 marta qutqardi, buzgani kamroq — 18,
lekin buzgani qutqarganidan qimmatroq turdi.

**Qisman yopish yordam berganidan ko'ra ko'proq zarar qildi — va baribir
yutdi.** 32 taga qarshi 41 ta. Shunday bo'ladi: kichik tez-tez yo'qotishlarga
qarshi kamdan-kam yirik qutqaruv. Holatlar sonini emas, yig'indini sanash
kerak. Sahifadagi eng foydali narsa, ehtimol, shu.

**Trayl deyarli hech narsani o'zgartirmadi.** 160 savdoda +1.8R — shovqin
doirasida.

## Halol izoh

Bu to'plamda «shunchaki ushlash» **−10.9R** beradi. Ya'ni «stop bitta ATR,
maqsad 2R, ixtiyoriy tomonga kirish» sxemasining o'zi zararli — u hamma uchun
bir xil o'lchov chizg'ichi sifatida olingan, ishlaydigan tizim sifatida emas.
Jadvaldan yarmini yopish kerak degan xulosa **chiqmaydi**: undan faqat
**boshqaruv natijani kuchli o'zgartirishi** kelib chiqadi, qaysi tomonga esa
oldindan aniq emas.

[Qayta o'qitish sahifasidagi](overfitting.md) kabi: bitta arxiv, bitta davr.

## Bu qanday hisoblanadi

Raqamlarni oshirib yubormaslik uchun kerak bo'lgan qoida: **agar sham stopga
ham, maqsadga ham tekkan bo'lsa, stop hisoblanadi.** Sham ichidagi harakat
tartibi noma'lum, shuning uchun yomonrog'i olinadi. Reja ishga tushishi
stopdan keyin tekshiriladi — aks holda bir vaqtda zararsizlikka ham, stopga
ham yetgan sham yutuqday ko'rinardi.

R dastlabki riskdan hisoblanadi: qisman yopish hajmni kamaytiradi, lekin
bazani qayta hisoblamaydi.

## Keyingi qadam

- [Replay trenajyori](replay-trainer.md) — kirish va stop qo'yish.
- [Savdo jurnali](../journal/web-journal.md) — stop ko'chirilganda qoidabuzarlik
  qo'yadigan o'sha jurnal; endi sababini mashq qiladigan joy bor.
- [Mahorat yoki omad](monte-carlo.md) — nega bitta seriya bo'yicha hukm
  chiqarib bo'lmaydi.

!!! danger "Moliyaviy maslahat emas"
    Raqamlar to'rtta juftlikning 3600 shamida o'lchangan. Boshqa to'plamda ular
    boshqacha bo'ladi — bu darsning bir qismi, shunchaki rasmiyatchilik uchun
    izoh emas.
