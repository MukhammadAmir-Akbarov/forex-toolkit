---
widgets: [risk-profile]
---

# Savdoga tayyorlik testi

!!! abstract "Bu test nima qiladi"
    Pul, vaqt, psixologiya va salomatlik haqida 30 ta savol. Oxirida 0 dan 100%
    gacha baho va zaif tomonlar ro'yxatini olasiz. Bu loyihadagi yagona vosita
    bo'lib, u halol ayta oladi: **hozircha savdo qilmang**.

!!! danger "Rostini javob bering"
    Natijani faqat siz ko'rasiz. U brauzeringizda qoladi va hech qayerga
    yuborilmaydi. Testni aldash oson — lekin buning evaziga ball emas, pulingiz
    to'lanadi.

[Yo'l xaritasi](../roadmap.md) bu testni birinchi haftaga qo'yadi. 50% dan past
natija — taqiq emas, avval zaif tomonlarni yopish uchun sabab: olti oylik
yostiq, barqaror daromad va zararga munosabat.

<div id="risk-profile-widget"></div>

<script type="application/json" id="risk-profile-questions">
[
  {
    "q": "1. Savdoga qancha pul kiritmoqchisiz?",
    "category": "finance",
    "options": [
      {
        "label": "Ortiqcha pulning 2% gacha (yashash uchun emas)",
        "points": 10
      },
      {
        "label": "Ortiqcha pulning 5-10% i",
        "points": 5
      },
      {
        "label": "Barcha jamg'armamni",
        "points": -10
      },
      {
        "label": "Kredit / qarz olingan mablag'",
        "points": -20
      }
    ]
  },
  {
    "q": "2. 6 oylik yashash uchun \"xavfsizlik yostig'i\" bormi?",
    "category": "finance",
    "options": [
      {
        "label": "Ha, kamida 6 oylik xarajat alohida turadi",
        "points": 10
      },
      {
        "label": "3-5 oy",
        "points": 5
      },
      {
        "label": "1-2 oy",
        "points": 0
      },
      {
        "label": "Yo'q",
        "points": -10
      }
    ]
  },
  {
    "q": "3. Barqaror asosiy daromadingiz bormi?",
    "category": "finance",
    "options": [
      {
        "label": "Ha, doimiy ish / biznes",
        "points": 10
      },
      {
        "label": "Frilans / beqaror, lekin yetarli",
        "points": 5
      },
      {
        "label": "Tasodifiy qo'shimcha ishlar",
        "points": -5
      },
      {
        "label": "Hozir daromad yo'q",
        "points": -15
      }
    ]
  },
  {
    "q": "4. Kiritgan pulingizni butunlay yo'qotsangiz, bu hayotingizga qanday ta'sir qiladi?",
    "category": "finance",
    "options": [
      {
        "label": "Hech qanday, yo'qotishga tayyorman",
        "points": 10
      },
      {
        "label": "Yoqimsiz, lekin chidayman",
        "points": 0
      },
      {
        "label": "Qattiq, o'zimni cheklashga to'g'ri keladi",
        "points": -10
      },
      {
        "label": "Halokatli — kreditlar, jiddiy muammolar",
        "points": -25
      }
    ]
  },
  {
    "q": "5. Haftasiga necha soat savdoga ajrata olasiz?",
    "category": "time",
    "options": [
      {
        "label": "10-20 soat (o'rganish uchun to'g'ri)",
        "points": 10
      },
      {
        "label": "5-10 soat",
        "points": 5
      },
      {
        "label": "1-5 soat",
        "points": 0
      },
      {
        "label": "1 soatdan kam",
        "points": -5
      }
    ]
  },
  {
    "q": "6. Barqaror foydagacha 1-3 yil o'rganishga tayyormisiz?",
    "category": "time",
    "options": [
      {
        "label": "Ha, bu uzoq muddatli ekanini tushunaman",
        "points": 10
      },
      {
        "label": "6-12 oy urinib ko'raman",
        "points": 0
      },
      {
        "label": "3-6 oyda foyda istayman",
        "points": -10
      },
      {
        "label": "Foydani darhol istayman",
        "points": -25
      }
    ]
  },
  {
    "q": "7. Har bir savdoni kundalikka yozishga tayyormisiz?",
    "category": "time",
    "options": [
      {
        "label": "Ha, muhimligini tushunaman",
        "points": 10
      },
      {
        "label": "Harakat qilaman, lekin ishonchim yo'q",
        "points": 0
      },
      {
        "label": "Buning ma'nosini ko'rmayapman",
        "points": -10
      }
    ]
  },
  {
    "q": "8. Moliyaviy yo'qotishga odatda qanday munosabatdasiz?",
    "category": "psychology",
    "options": [
      {
        "label": "Tahlil qilaman, xulosa chiqaraman",
        "points": 10
      },
      {
        "label": "Xafa bo'laman, lekin o'zimga kelaman",
        "points": 5
      },
      {
        "label": "Uzoq o'ylayman, yomon uxlayman",
        "points": -10
      },
      {
        "label": "Jahlim chiqadi, darhol \"qaytarib olishni\" istayman",
        "points": -20
      }
    ]
  },
  {
    "q": "9. Reja ishlamayotganda nima qilasiz?",
    "category": "psychology",
    "options": [
      {
        "label": "Rejaga amal qilaman, oxirida tahlil qilaman",
        "points": 10
      },
      {
        "label": "Ba'zan chetga chiqaman, keyin qaytaman",
        "points": 0
      },
      {
        "label": "Yurib turib improvizatsiya qilaman",
        "points": -10
      },
      {
        "label": "Rejani darhol o'zgartiraman",
        "points": -15
      }
    ]
  },
  {
    "q": "10. Vasvasalarga (ovqat, qimor, xarid) yo'q deya olasizmi?",
    "category": "psychology",
    "options": [
      {
        "label": "Ha, o'zimni tuta olaman",
        "points": 10
      },
      {
        "label": "Ko'p hollarda",
        "points": 5
      },
      {
        "label": "Ba'zan chidayolmayman",
        "points": 0
      },
      {
        "label": "Tez-tez chidayolmayman",
        "points": -15
      }
    ]
  },
  {
    "q": "11. Qimor o'ynaganmisiz (kazino, garov, pulga poker)?",
    "category": "psychology",
    "options": [
      {
        "label": "Yo'q / faqat kamdan-kam ko'ngilxushlik uchun",
        "points": 10
      },
      {
        "label": "Ba'zan, muammosiz",
        "points": 0
      },
      {
        "label": "Muntazam o'ynayman",
        "points": -10
      },
      {
        "label": "Qaramlik bilan muammolar bo'lgan",
        "points": -25
      }
    ]
  },
  {
    "q": "12. Stressni qanday yengasiz?",
    "category": "psychology",
    "options": [
      {
        "label": "Sport, meditatsiya, yaqinlar bilan suhbat",
        "points": 10
      },
      {
        "label": "Sevimli mashg'ulot, chalg'iyman",
        "points": 5
      },
      {
        "label": "Ko'p ovqatlanaman, televizor ko'raman",
        "points": 0
      },
      {
        "label": "Alkogol / chekish / boshqa qaramliklar",
        "points": -15
      }
    ]
  },
  {
    "q": "13. Harakatsiz \"zerikarli\" davrlarga chiday olasizmi?",
    "category": "psychology",
    "options": [
      {
        "label": "Ha, har kun savdo kuni emasligini tushunaman",
        "points": 10
      },
      {
        "label": "Umuman chidayman",
        "points": 5
      },
      {
        "label": "Qiyin, nimadir qilgim keladi",
        "points": -10
      },
      {
        "label": "Harakatsiz o'tira olmayman",
        "points": -15
      }
    ]
  },
  {
    "q": "14. Siz tizimli odammisiz yoki intuitivmi?",
    "category": "character",
    "options": [
      {
        "label": "Tizimli, qoida va jarayonlarni yoqtiraman",
        "points": 10
      },
      {
        "label": "Ko'proq tizimli",
        "points": 5
      },
      {
        "label": "Ko'proq intuitiv",
        "points": -5
      },
      {
        "label": "To'liq intuitsiya bilan",
        "points": -15
      }
    ]
  },
  {
    "q": "15. Xatolaringiz uchun javobgarlikni o'z zimmangizga olasizmi?",
    "category": "character",
    "options": [
      {
        "label": "Ha, sababni doim o'zimdan qidiraman",
        "points": 10
      },
      {
        "label": "Ko'p hollarda",
        "points": 5
      },
      {
        "label": "Ko'pincha vaziyatni ayblayman",
        "points": -10
      },
      {
        "label": "Boshqalarni / bozorni / hukumatni ayblayman",
        "points": -15
      }
    ]
  },
  {
    "q": "16. Har savdodan oldin 10+ banddan iborat ro'yxatga amal qilishga tayyormisiz?",
    "category": "character",
    "options": [
      {
        "label": "Ha, intizom kerak",
        "points": 10
      },
      {
        "label": "Harakat qilaman, lekin zerikarli",
        "points": 0
      },
      {
        "label": "Juda mashaqqatli",
        "points": -10
      },
      {
        "label": "Bunday ro'yxatlar kuchsizlar uchun",
        "points": -25
      }
    ]
  },
  {
    "q": "17. O'zingizni boshqalar bilan solishtirasizmi?",
    "category": "character",
    "options": [
      {
        "label": "Kamdan-kam, o'z taraqqiyotimga qarayman",
        "points": 10
      },
      {
        "label": "Ba'zan",
        "points": 0
      },
      {
        "label": "Tez-tez, ayniqsa ijtimoiy tarmoqlarda",
        "points": -10
      },
      {
        "label": "Doim, \"hammadan yaxshi\" bo'lishim kerak",
        "points": -15
      }
    ]
  },
  {
    "q": "18. Moliya sohasida tajribangiz qanday?",
    "category": "experience",
    "options": [
      {
        "label": "Byudjet yuritaman, ETF / aksiyalarga investitsiya qilaman",
        "points": 10
      },
      {
        "label": "Asoslarni bilaman, ba'zan investitsiya qilaman",
        "points": 5
      },
      {
        "label": "Bazaviy bilim (banklar, kreditlar)",
        "points": 0
      },
      {
        "label": "Juda kam",
        "points": -5
      }
    ]
  },
  {
    "q": "19. Forex / savdo bo'yicha biror narsa o'rganganmisiz?",
    "category": "experience",
    "options": [
      {
        "label": "Bir necha kitob o'qidim, kurslarda qatnashdim",
        "points": 10
      },
      {
        "label": "YouTube va maqolalarni ko'rdim",
        "points": 5
      },
      {
        "label": "Hech nima o'qimadim, endi boshlayapman",
        "points": 0
      },
      {
        "label": "\"Oson pul\" reklamasiga ishondim",
        "points": -20
      }
    ]
  },
  {
    "q": "20. Dasturlash / matematika bilan tanishmisiz?",
    "category": "experience",
    "options": [
      {
        "label": "Ha, skript yoza olaman",
        "points": 10
      },
      {
        "label": "Asosiy mantiqni tushunaman",
        "points": 5
      },
      {
        "label": "Unchalik emas",
        "points": 0
      },
      {
        "label": "Umuman yo'q",
        "points": -5
      }
    ]
  },
  {
    "q": "21. O'rtacha necha soat uxlaysiz?",
    "category": "health",
    "options": [
      {
        "label": "Barqaror 7-9 soat",
        "points": 10
      },
      {
        "label": "6-7 soat",
        "points": 0
      },
      {
        "label": "5-6 soat",
        "points": -10
      },
      {
        "label": "5 soatdan kam",
        "points": -20
      }
    ]
  },
  {
    "q": "22. Sport bilan shug'ullanasizmi?",
    "category": "health",
    "options": [
      {
        "label": "Haftasiga 3+ marta",
        "points": 10
      },
      {
        "label": "Haftasiga 1-2 marta",
        "points": 5
      },
      {
        "label": "Kamdan-kam",
        "points": 0
      },
      {
        "label": "Hech qachon",
        "points": -5
      }
    ]
  },
  {
    "q": "23. Muntazam alkogol ichasizmi?",
    "category": "health",
    "options": [
      {
        "label": "Yo'q / juda kamdan-kam",
        "points": 10
      },
      {
        "label": "Dam olish kunlari",
        "points": 0
      },
      {
        "label": "Haftasiga 2-3 marta",
        "points": -10
      },
      {
        "label": "Har kuni",
        "points": -20
      }
    ]
  },
  {
    "q": "24. Yaqinlaringiz savdo qilmoqchi ekaningizni biladimi?",
    "category": "relationships",
    "options": [
      {
        "label": "Ha, qo'llab-quvvatlaydilar / betaraf",
        "points": 10
      },
      {
        "label": "Biladilar, lekin qarshi",
        "points": 0
      },
      {
        "label": "Yashiraman",
        "points": -10
      },
      {
        "label": "Yashiraman va ularning pulini olaman",
        "points": -25
      }
    ]
  },
  {
    "q": "25. Munosabatlaringiz / oilangiz barqarormi?",
    "category": "relationships",
    "options": [
      {
        "label": "Ha, hammasi yaxshi",
        "points": 10
      },
      {
        "label": "Umuman barqaror",
        "points": 5
      },
      {
        "label": "Muammolar bor",
        "points": -5
      },
      {
        "label": "Inqirozda / ajrashish arafasida",
        "points": -10
      }
    ]
  },
  {
    "q": "26. Nima uchun forexda savdo qilmoqchisiz?",
    "category": "motivation",
    "options": [
      {
        "label": "Kasb sifatida qiziq, o'rganishga tayyorman",
        "points": 10
      },
      {
        "label": "Qo'shimcha daromad va qiziqish",
        "points": 5
      },
      {
        "label": "Pul kerak, tez ishlab olishga umid qilaman",
        "points": -10
      },
      {
        "label": "Atrofdagilar ishlayapti, men ham istayman",
        "points": -20
      }
    ]
  },
  {
    "q": "27. Bir yildan keyin savdodagi \"muvaffaqiyat\" siz uchun nima?",
    "category": "motivation",
    "options": [
      {
        "label": "Depozitni yo'qotmaslik va bozorni tushunish",
        "points": 10
      },
      {
        "label": "Oyiga barqaror 1-3%",
        "points": 5
      },
      {
        "label": "Oyiga 10-20%",
        "points": -10
      },
      {
        "label": "Ishdan ketish / mashina sotib olish",
        "points": -20
      }
    ]
  },
  {
    "q": "28. Butun depozitni yo'qotsangiz, nima qilasiz?",
    "category": "warnings",
    "options": [
      {
        "label": "Tanaffus qilaman, tahlil qilaman, balki umuman qaytmayman",
        "points": 10
      },
      {
        "label": "1-3 oy tanaffus qilaman, keyin o'ylayman",
        "points": 5
      },
      {
        "label": "Darhol yana pul qo'shaman",
        "points": -15
      },
      {
        "label": "Kredit olaman va yana urinib ko'raman",
        "points": -30
      }
    ]
  },
  {
    "q": "29. Telegramda / \"guru\"dan signal sotib olganmisiz?",
    "category": "warnings",
    "options": [
      {
        "label": "Yo'q / sotib olmayman",
        "points": 10
      },
      {
        "label": "O'yladim, lekin sotib olmadim",
        "points": 5
      },
      {
        "label": "Sotib olgandim, lekin boshqa olmayman",
        "points": -5
      },
      {
        "label": "Muntazam sotib olaman",
        "points": -15
      }
    ]
  },
  {
    "q": "30. Dastlabki 3-6 oy faqat demoda savdo qilishga tayyormisiz?",
    "category": "warnings",
    "options": [
      {
        "label": "Ha, muhimligini tushunaman",
        "points": 10
      },
      {
        "label": "Bir-ikki oy",
        "points": 0
      },
      {
        "label": "Darhol real hisobga o'tmoqchiman",
        "points": -15
      },
      {
        "label": "Real hisob ochib, savdoni boshlab yubordim",
        "points": -25
      }
    ]
  }
]
</script>

## Natijani qanday o'qish kerak

| Natija | Ma'nosi |
|---|---|
| 80% va yuqori | A'lo profil: yostiq bor, kutganlar real |
| 60-80% | Yaxshi profil, lekin zaif joylarni real puldan oldin yoping |
| 40-60% | Chegarada: kamida olti oylik tayyorgarlik |
| 20-40% | Yuqori risk: hozircha boshlamang |
| 20% dan past | Kritik risk: uzoq muddatli investitsiya xavfsizroq |

Foizlar 300 balllik maksimumdan hisoblanadi. Yomon javoblar ball ayiradi,
shuning uchun natija manfiy ham bo'lishi mumkin — bu normal va aynan xulosada
yozilgan narsani anglatadi.

## Zaif tomonlar bilan nima qilish kerak

- **Moliya** — avval olti oylik yostiq va barqaror daromad. Qarz pulga savdo
  qilishning yaxshi yakuni yo'q.
- **Psixologiya** — zarardan keyin darhol qaytarib olish istagi savdodagi eng
  qimmat odat. [Kundalikdagi hissiyot tahlili](../journal/web-journal.md).
- **Vaqt** — haftasiga bir soatdan kam vaqt o'z savdolaringizni ko'rib chiqishga
  ham yetmaydi.
- **Ogohlantirishlar** — qimor yoki qaramlikka moyillik bo'lsa, hisob ochishdan
  oldin mutaxassis bilan gaplashing.

Xuddi shu test terminalda ham bor: `forex-risk-profile` yoki
`python tools/risk_profile.py`. Veb-versiya va CLI bir xil hisoblaydi — buni
testlar tekshiradi.

!!! warning "Moliyaviy maslahat emas"
    Bu ta'limiy o'z-o'zini tekshirish vositasi, moliyaviy maslahatchining bahosi
    emas va hech qanday natija kafolati emas.
