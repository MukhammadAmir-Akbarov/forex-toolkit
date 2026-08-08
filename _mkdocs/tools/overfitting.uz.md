---
widgets: [overfitting]
---

# 🎣 Nega chiroyli bektest hech narsa va'da qilmaydi

!!! abstract "Bu shior emas, o'lchov"
    Quyida bitta strategiyaning 54 ta parametr birikmasi **haqiqiy** EUR/USD H1
    shamlarida hisoblangan: ikki yil ichidagi 12 346 ta soatlik sham. Tarix
    vaqt bo'yicha ikkiga bo'lingan: parametrlar birinchi qismda tanlanadi,
    ikkinchisida tekshiriladi. «Robot» sotuvchisi ham xuddi shunday qiladi —
    faqat u birinchi yarmini ko'rsatadi va ikkinchisi haqida jim turadi.

    Avval qatorni o'zingiz tanlang. Keyin nima bo'lganini ko'ring.

<div id="overfitting" data-src="../../../data/overfitting.json"></div>

---

## Bu tanlanmada nima chiqdi

| Savol | Javob |
|---|---|
| O'tmishdagi eng yaxshi birikma | **+29.6R**, 92 savdo |
| O'sha birikma kelajakda | **−12.5R**, 66 savdo |
| Uning kelajakdagi o'rni | **54 tadan 40-chi** |
| Barcha birikmalarning kelajakdagi medianasi | −7.7R |
| O'tmish va kelajak bog'liqligi | **−0.09** |

Oxirgi qator eng muhimi. Nolga yaqin bog'liqlik shuni bildiradi: tarixdagi
natija kelajakdagi natija haqida **hech narsa** aytmaydi. «Kam» emas — bu
tanlanma doirasida umuman hech narsa.

Eng yaxshi ko'ringan birikma qirqtadan yomonroq chiqdi. «Bektest bo'yicha»
tanlash bu yerda tasodifiy tanlashdan ham **yomonroq** ishladi.

## Halol izoh

Kelajakdagi mediana ham manfiy: −7.7R. Ya'ni bu davrda strategiya faqat «eng
yaxshi» emas, har qanday parametrda ham zarar keltirgan. Bundan strategiya
yomon degan xulosa **chiqmaydi**, yaxshi degan ham chiqmaydi — davr qisqa,
juftlik bitta.

Sahifaning xulosasi boshqa va u davrga bog'liq emas: **parametrlarni saralash
natijani yaxshilamadi.** O'tmishdagi eng yaxshisi kelajakdagi eng yaxshisi
bo'lmadi.

## Nega shunday bo'ladi

54 ta birikmani sinash — bu tangani 54 marta tashlab, eng yaxshi tashlashni
saqlab qolish. U a'lo ko'rinadi — lekin a'lo ko'rinish va yaxshi bo'lish har xil
narsa.

Esda qoladigan qoida:

> Qancha ko'p birikma sinasangiz, g'olib shuncha chiroyli ko'rinadi va shuncha
> kam ma'no anglatadi.

Shuning uchun «tarixda 300% bergan robot» — yutuq emas, saralash tartibining
tavsifi. Buni bitta savol tekshiradi: **buni topguncha nechta variantni
sinadingiz?**

## Bu bilan nima qilish kerak

1. **Tarixni bo'lish.** Parametrlarni bir qismda tanlash, ko'rmagan boshqasida
   tekshirish. Yuqorida aynan shu qilingan.
2. **Cho'qqiga emas, barqarorlikka qarash.** Agar to'rdagi qo'shni parametrlar
   butunlay boshqa natija bersa — siz qonuniyatni emas, tasodifni topgansiz.
3. **Urinishlarni sanash.** 54 urinishdan bitta yaxshi natija — oddiy omad.
4. **«Mahorat yoki omad» tekshiruvi.** Loyihada buning uchun
   [Monte-Karlo tekshiruvi](monte-carlo.md) bor.

## O'zingiz qayta hisoblash

Kotirovkalar repozitoriyda yo'q (ular katta va bizniki emas), shuning uchun
to'plam bir marta hisoblanib qotirilgan. Agar o'z CSV faylingiz bo'lsa:

```bash
python tools/overfit_scan.py --csv data/EURUSD_1h.csv --out _mkdocs/data/overfitting.json
```

Sahifadagi raqamlarni test ushlab turadi: qayta hisoblash xulosani o'zgartirsa,
u yiqiladi va saytda eskirgan da'vo qolmaydi.

## Keyingi qadam

- [Mahorat yoki omad](monte-carlo.md) — tasodif haqidagi o'sha fikr, lekin
  sizning shaxsiy savdolar seriyangizga nisbatan.
- [Bektest nega yolg'on gapiradi](../docs/strategy-details.md) — tarix bilan
  o'zini aldashning boshqa usullari.
- [Figuralar trenajyori](pattern-trainer.md) — figuralar aslida nima bergani.

!!! danger "Moliyaviy maslahat emas"
    Bu yerdagi har bir raqam bitta juftlikda, bitta davrda o'lchangan. Boshqa
    tanlanmada ular boshqacha bo'ladi — sahifa aynan shu haqda.
