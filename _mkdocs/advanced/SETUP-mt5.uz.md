# MT5 Setup Guide — MetaTrader 5 ni bosqichma-bosqich o'rnatish

## 1-qadam: Brokerda ro'yxatdan o'tish

1. Tartibga solinadigan broker tanlang (qarang [extras/brokers-comparison.md](../extras/brokers-comparison.md))
2. Broker saytida → **«Demo hisob ochish»** (haqiqiy emas!)
3. Formani to'ldiring: ism, email, telefon
4. Emailga **3 ta ma'lumot** keladi:
   - **Login** (masalan 50123456)
   - **Password** (investor password — ko'rish uchun, master password — savdo uchun)
   - **Server** (masalan `Exness-Demo` yoki `ICMarkets-Demo01`)

> ⚠️ Bu ma'lumotlarni saqlang. Ular MT5 ga kirish uchun kerak.

## 2-qadam: MT5 ni yuklab olish

### macOS

MetaTrader 5 Mac uchun ikki variantda mavjud:

**A variant: mahalliy (tavsiya etiladi)**

1. Broker saytini oching → **«MT5 yuklab olish»** → **Mac**
2. `.dmg` fayl yuklanadi (~60 MB)
3. Oching → MT5 ni Applications ga sudrab tashlang
4. Ishga tushiring → macOS bloklasa Tizim sozlamalarida ruxsat bering

**B variant: WINE orqali (mahalliy ishlamasa)**

1. metaquotes.net saytidan **MetaTrader 5** ni yuklab oling
2. Wine o'rnating: `brew install --cask wine-stable`
3. .exe faylni Wine orqali oching

### Windows

1. Broker saytiga kiring → Download → Windows
2. .exe ni ishga tushiring → o'rnating

### Linux

1. WINE: `sudo apt install wine`
2. Windows .exe ni yuklab oling → Wine orqali ishga tushiring

## 3-qadam: Birinchi kirish

1. MT5 ni ishga tushiring
2. Menyu: **File → Login to Trade Account**
3. To'ldiring:
   ```
   Login:    [brokerdan olingan login]
   Password: [parol]
   Server:   [xatdagi server]
   ```
4. **«Save account info»** katagini belgilang
5. **Login** tugmasini bosing

✅ Pastki o'ng burchakda yashil raqamlar ko'rinadi — balans, equity, margin.

## 4-qadam: Grafikni sozlash

### Shamli grafikni yoqish

- Grafik ustida o'ng tugma → **Candlesticks**
- Yoki yuqori paneldagi «shamlar» tugmasini bosing

### Taymfreymni H1 ga o'tkazish

- Yuqori panel: M1, M5, M15, M30, **H1**, H4, D1, W1
- **H1** ni bosing

### EMA 50 qo'shish

1. **Insert → Indicators → Trend → Moving Average**
2. Parametrlar:
   - Period: **50**
   - MA method: **Exponential**
   - Apply to: **Close**
   - Style: rang — **ko'k**, qalinlik **2**
3. OK

### EMA 200 qo'shish

Xuddi shunday, lekin Period = **200**, rang — **qizil**.

### RSI qo'shish

1. **Insert → Indicators → Oscillators → Relative Strength Index**
2. Period: **14**
3. Apply to: **Close**
4. OK

### Shablonni saqlash

Har safar sozlamaslik uchun:

- Grafik ustida o'ng tugma → **Templates → Save Template** → nom «MyTemplate»
- Keyingi safar: o'ng tugma → Templates → MyTemplate

## 5-qadam: Savdo ochish

### To'g'ri ochish usuli (SL/TP bilan birga)

1. **F9** ni bosing (yoki yuqori paneldagi «New Order» tugmasi)
2. Order oynasi:
   ```
   Symbol:        EURUSD
   Volume:        0.01     <- position_calculator.py orqali hisoblang!
   Stop Loss:     1.0827   <- majburiy!
   Take Profit:   1.0902   <- majburiy!
   Type:          Market Execution
   ```
3. **Buy by Market** (long) yoki **Sell by Market** (short) ni bosing

### Ko'p uchraydigan xatolar

❌ **SL siz ochish** → Hech qachon. Avval SL kiriting.
❌ **Hajmni ko'z bilan chamalash** → kalkulyatordan foydalaning.
❌ **«Type: Pending»** → bu kutilma order, narx yetib kelguncha kutiladi. Hozircha kerak emas.

## 6-qadam: Savdoni tekshirish

Ochgandan so'ng pastki paneldagi **Trade** bo'limida:

```
Symbol  Type  Volume  Open Price  S/L      T/P      Profit
EURUSD  buy   0.01    1.08520    1.08270  1.09020  +$1.50
```

✓ S/L va T/P **bo'sh emas** — himoya o'rnatilgan.

## 7-qadam: Savdoni yopish

**Eng yaxshi variant:** qo'lda yopmang. SL yoki TP ishlashini kuting.

**Erta yopish kerak bo'lsa** (faqat istisno holatlarda):

- Pastki qismdagi savdo ustida o'ng tugma → **Close Order**

## 8-qadam: MT5 dagi savdolar jurnali

MT5 o'zi log yuritadi:

- Pastki panel → **History**
- Barcha yopilgan savdalar natijalari bilan ko'rinadi
- Eksport qilish mumkin: o'ng tugma → **Report → Save as Report (HTML)**

Bu tarixni **parallel** ravishda o'z Markdown/CSV jurnalingizga ko'chirish tavsiya etiladi, chunki MT5 da «his-tuyg'ular», «qoidalarga amal qildimmi» kabi maydonlar yo'q.

## 9-qadam: Ko'p ishlatiladigan tezkor tugmalar

| Tugma | Vazifasi |
|---|---|
| **F9** | New Order ochish |
| **F8** | Grafik xossalari |
| **F11** | To'liq ekran rejimi |
| **Ctrl+T** | Pastki terminal |
| **Ctrl+N** | Navigator oynasi |
| **+** / **-** | Zoom in / out |
| **PageDown** | So'nggi shamlar ga o'tish |

## 10-qadam: Expert Advisor o'rnatish

Demo da bizning [EMA50Pullback.mq5](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/advanced/EMA50Pullback.mq5) ni ishga tushirmoqchi bo'lsangiz:

1. MT5 da: **File → Open Data Folder**
2. `MQL5/Experts/` papkasini oching
3. `EMA50Pullback.mq5` faylini u yerga ko'chiring
4. MT5 da: **View → Navigator** (Ctrl+N)
5. **Expert Advisors** bo'limi → o'ng tugma → **Refresh**
6. `EMA50Pullback` ko'rinadi → EUR/USD H1 grafikka sudrab tashlang
7. Sozlamalar oynasida:
   - ✅ **Allow live trading** (maslahatchi savdo qilishini istasangiz)
   - Parametrlarni kiriting (Risk_Percent, Risk_Reward va boshqalar)
   - **OK**
8. Grafikning yuqori o'ng burchagida 😀 (ishlayapti) yoki ❌ (ishlamayapti) belgisi ko'rinadi

**⚠️ MUHIM:** EA «faqat demo» tekshiruvi bilan himoyalangan. Haqiqiy hisobda ishlashdan bosh tortadi.

## 11-qadam: Demo hisob va haqiqiy hisob — asosiy farqlar

| Xususiyat | Demo | Haqiqiy |
|---|---|---|
| Ijro | Ideal | Slippage bilan |
| Spred | Ko'pincha kichikroq | Haqiqiy, kengayishi mumkin |
| His-tuyg'ular | Yo'q (virtual) | Bor (sizning muammoingiz) |
| Svoplar | Ba'zan soddalashtirilgan | Haqiqiy |
| Rekvotalar (requote) | Yo'q | Kuchli volatillikda mumkin |

## 12-qadam: MT5 dagi birinchi oy strategiyasi

1-hafta:

- O'rnatish, interfeys bilan tanishish
- Minimal 0.01 lot hajmda 5-10 ta sinov savdosi
- SL/TP ni sinab ko'rish — ishlashiga ishonch hosil qilish

2-4 hafta:

- Strategiya qoidalari bo'yicha savdo (kuniga 1-3 ta savdo)
- Parallel ravishda jurnal yuritish
- Har bir savdo oldidan kalkulyatordan foydalanish

## Qo'shimcha maslahatlar

### Terminal muzlab qolsa

- Ortiqcha grafik varaqlarini yoping
- Pastki o'ng burchak: o'ng tugma → **Connect Status** → «Connected» bo'lishi kerak
- Bo'lmasa — File → Login orqali qayta ulaning

### Kotirovkalar yangilanmasa

- Broker dam olish kunlarida kvotalarni cheklashi mumkin
- Shanba/yakshanba emasligi tekshiring (bozor yopiq)

### Sozlamalar zaxira nusxasi

- File → Open Data Folder → `config/` papkasini ko'chiring
- Keyinchalik «Restore» ni bosib tiklaysiz

---

## MT5 da savdoga tayyorlik tekshiruvi

- [ ] MT5 o'rnatilgan va demoga ulangan
- [ ] Pastki o'ng burchakda balans ko'rinyapti
- [ ] EUR/USD H1 grafigi EMA 50, EMA 200, RSI bilan sozlangan
- [ ] Shablon saqlangan
- [ ] SL va TP bilan savdo ochishni bilaman
- [ ] Tarixni qanday ko'rishni bilaman
- [ ] Pozitsiya kalkulyatori ochiq
- [ ] Savdolar jurnali ochiq (Google Sheets yoki Markdown)
- [ ] Stol ustida chop etilgan [tekshiruv ro'yxati](../extras/checklist-printable.md)

**Barchasi ☑ → birinchi demo savdoga tayyorsiz.**

---

[← Asosiy qo'llanmaga](../forex-guide.md)
