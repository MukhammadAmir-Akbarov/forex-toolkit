# Streamlit o'rnatish qo'llanmasi — brauzerda interaktiv bektest

## Bu nima beradi

Ishga tushirgandan so'ng **slayderlar bilan veb-sahifa** ochiladi, u yerda quyidagilarni amalga oshirish mumkin:

- Strategiyani ochiladigan ro'yxatdan tanlash
- R:R, win rate, shamlar soni slayderlarini harakatlatish
- **Yangilangan** equity curve, metrikalar, savdolar jadvalini darhol ko'rish
- Signal markerli narx grafigi

Bu turli parametrlar bilan Python-skriptni qayta ishga tushirishdan ancha qulay.

## 1-qadam: Streamlit o'rnatish

```bash
cd /Users/mukhammadamir/Sites/WORK/trading
.venv/bin/pip install streamlit plotly
```

Bu Streamlit (~30 MB) ni o'rnatadi.

## 2-qadam: Ishga tushirish

```bash
.venv/bin/streamlit run advanced/streamlit_app.py
```

Nima bo'ladi:

1. Terminalda quyidagi xabar paydo bo'ladi:
   ```
   You can now view your Streamlit app in your browser.
   Local URL: http://localhost:8501
   ```
2. **Brauzer o'zi ochiladi** http://localhost:8501 manziliga
3. Ochilmagan bo'lsa — havolani qo'lda oching

## 3-qadam: Foydalanish

### Chap panel (sidebar) — parametrlar

- **Strategiya** — 4 ta strategiyadan birini tanlash
- **Namunadagi shamlar soni** — qancha H1-sham generatsiya qilish (ko'proq = ko'proq savdo)
- **R:R** — Risk/Reward nisbati (1.0–5.0)
- **Random seed** — takrorlanish uchun (bir xil son = bir xil ma'lumotlar)
- **Savdodagi xavf** — yakuniy % hisoblash uchun

### Sahifaning asosiy qismi

1. **Metrikalar** yuqorida (4 ta karta):
   - Savdolar soni
   - Win rate
   - Profit Factor
   - Jami natija

2. **Equity curve** — interaktiv grafik
   - Sichqonchani olib boring — aniq qiymatlarni ko'rasiz
   - Kattalashtirish mumkin

3. **Savdolar jadvali** — oxirgi 50 ta savdo

4. **Shamli narx grafiki** — signal markerlari ko'rinadi (▲ long, ▼ short)

## 4-qadam: Tajribalar

Sinab ko'ring:

### 1-tajriba: R:R ta'siri

- R:R ni 1.0 dan 5.0 ga suring
- Yakuniy foyda qanday o'zgarishini kuzating
- **Xulosa:** katta R:R da kamroq savdo muvaffaqiyatli bo'ladi, lekin har biri ko'proq foyda keltiradi

### 2-tajriba: Strategiyalarni solishtirish

- Strategiyani almashtiring (EMA50 → Mean Reversion → Breakout → Three Soldiers)
- Bir xil seed = bir xil ma'lumotlar
- **Xulosa:** qaysi biri ushbu ma'lumotlarda yaxshiroq ishlaydi?

### 3-tajriba: Ma'lumotlarga bog'liqlik

- Random seed ni o'zgartiring (1, 42, 100, 9999)
- Bir xil strategiya **juda har xil** natijalar beradi
- **Xulosa:** natija omad + ma'lumotlar miqdoriga bog'liq

## 5-qadam: Ilovani to'xtatish

Terminalda **Ctrl+C** tugmasini bosing — Streamlit to'xtaydi.

Qayta ishga tushirish uchun — 2-qadamni takrorlang.

## Fonda ishlatish (ixtiyoriy)

Agar Streamlit doimo ishlashini istasangiz:

```bash
.venv/bin/streamlit run advanced/streamlit_app.py &
```

Kerak bo'lmaganda o'chirish uchun:
```bash
pkill -f streamlit
```

## Boshqa qurilmadan kirish (ixtiyoriy)

Odatda Streamlit faqat o'z kompyuteringizda ko'rinadi. Bir xil Wi-Fi tarmog'idagi telefondan ochish uchun:

```bash
.venv/bin/streamlit run advanced/streamlit_app.py --server.address 0.0.0.0
```

Keyin telefonda quyidagini oching:
```
http://<Mac-ning-IP-manzili>:8501
```

IP manzilini bilish: `ifconfig | grep "inet 192"`

## Bulutda joylashtirish (ilg'or foydalanuvchilar uchun)

Streamlit Cloud (bepul) yoki Render / Railway:

1. Loyihani GitHub ga yuklang
2. streamlit.io/cloud saytida ro'yxatdan o'ting
3. Repozitoriyni ulang → `advanced/streamlit_app.py` ni tanlang
4. Ommaviy URL olasiz

**⚠️** Haqiqiy ma'lumotlar bilan savdolar jurnalini ommaviy repozitoriyga joylamang.

## Muammolarni bartaraf etish

### `streamlit: command not found`

Faqat `streamlit` emas, `.venv/bin/streamlit` orqali ishga tushiring.

### Brauzer ochilmadi

Qo'lda oching: http://localhost:8501

### 8501-port band

```bash
.venv/bin/streamlit run advanced/streamlit_app.py --server.port 8502
```

### Streamlit import xatosi bilan ishlamayapti

Barcha bog'liqliklar o'rnatilganligini tekshiring:
```bash
.venv/bin/pip install streamlit plotly pandas numpy matplotlib
```

### Grafiklar yangilanmayapti

- Keshni tozalang: sahifaning o'ng yuqori burchagida → menyu → **Clear cache**
- Sahifani qayta yuklang (Cmd+R)

## Ichida nima bor (qiziquvchilar uchun)

[streamlit_app.py](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/advanced/streamlit_app.py) fayli — ~150 qator Pythonda yozilgan veb-ilova:

- `st.sidebar` — chap panel
- `st.slider`, `st.selectbox` — boshqaruv elementlari
- `st.cache_data` — keshlash: har o'zgarishda hammasini qayta hisoblashning oldi olinadi
- `plotly.graph_objects` — interaktiv grafiklar
- Bektest logikasi `bot/backtest.py` dagi bilan bir xil

Faylni tahrirlashingiz va o'zgarishlarni darhol ko'rishingiz mumkin (Streamlit sahifani avtomatik qayta yuklaydi).

---

[← Asosiy qo'llanmaga qaytish](../forex-guide.md)
