---
widgets: [journal]
---

# 📊 Veb savdo jurnali

!!! abstract "Bu vosita nima qiladi"
    CSV jurnal yoki MT5 HTML hisobotini yuklang — brauzer Win Rate, Profit Factor, P&L, jami R,
    maksimal pasayish va intizomni hisoblaydi. Savdolarni sana, juftlik,
    yo'nalish va qoidalarga rioya bo'yicha filtrlash mumkin.

    «Savdodan oldin» ekranidagi rejalar bu yerda avtomatik ko'rinadi. Ularni
    **Plan → Ochiq → Yopiq** holatlaridan o'tkazing, yopilgach tahlil qiling va
    statistikani shaxsiy Monte Carlo modeliga yuboring.

    Importdan oldin jurnal ma'lumot sifatini ko'rsatadi: to'g'ri va muammoli
    qatorlar, dublikatlar, noma'lum ustunlar hamda dastlabki 10 yozuv. Haftalik
    hisobot USD/UZS/R natijasi, intizom va keyingi vazifani beradi.

!!! tip "Maxfiylik"
    Fayl **faqat brauzeringizda** qayta ishlanadi. U serverga yuklanmaydi va
    jurnal keyingi safar tiklanishi uchun qurilmada lokal saqlanadi.

Loyihaning ikkala formati ham qo'llab-quvvatlanadi: kengaytirilgan
[`trading-journal-template.csv`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/journal/trading-journal-template.csv)
va `forex-journal` yaratadigan qisqa CSV, shuningdek MT5 HTML hisoboti.

Hisobot olish: **MT5 → View → Toolbox → History → o'ng tugma → Report →
HTML**. Yuklashdan oldin ulashishni istamaydigan ma'lumotlar yo'qligini
tekshiring; vosita faylni faqat lokal qayta ishlaydi.

Terminal orqali ham import qilish mumkin:

```bash
forex-journal import-mt5 report.html --out journal/mt5-trades.csv
```

<div class="journal-widget" id="journal-widget">
  <div class="journal-drop" id="journal-drop">
    <strong>CSV yoki MT5 HTML faylni shu yerga tashlang</strong>
    <div class="journal-actions">
      <label class="journal-button" for="journal-file">Fayl tanlash</label>
      <input id="journal-file" type="file" accept=".csv,.html,.htm,.xls,text/csv,text/html" hidden>
      <button class="journal-button secondary" id="journal-demo" type="button">Demoni ochish</button>
      <button class="journal-button secondary" id="journal-clear" type="button">Ma'lumotni tozalash</button>
    </div>
    <p class="journal-file-name" id="journal-file-name">Fayl tanlanmagan</p>
    <p class="journal-status" id="journal-status" aria-live="polite"></p>
    <p class="journal-privacy">🔒 Ma'lumot shu qurilmada qoladi.</p>
  </div>
  <div class="journal-error" id="journal-error"></div>

  <div class="journal-dashboard" id="journal-dashboard">
    <div class="journal-filters">
      <label>Boshlanish<input id="journal-from" type="date"></label>
      <label>Tugash<input id="journal-to" type="date"></label>
      <label>Juftlik<select id="journal-pair"><option value="">Barchasi</option></select></label>
      <label>Yo'nalish
        <select id="journal-direction">
          <option value="">Barchasi</option><option value="long">Long</option><option value="short">Short</option>
        </select>
      </label>
      <label>Qoidalar
        <select id="journal-rules">
          <option value="">Barchasi</option><option value="yes">Ha</option><option value="no">Yo'q</option>
        </select>
      </label>
    </div>

    <div class="journal-metrics">
      <div class="journal-card"><div class="journal-card-label">Savdolar</div><div class="journal-card-value" id="journal-m-trades">0</div></div>
      <div class="journal-card"><div class="journal-card-label">Win Rate</div><div class="journal-card-value" id="journal-m-winrate">0%</div></div>
      <div class="journal-card"><div class="journal-card-label">Profit Factor</div><div class="journal-card-value" id="journal-m-pf">0</div></div>
      <div class="journal-card"><div class="journal-card-label">Sof P&L</div><div class="journal-card-value" id="journal-m-pnl">$0</div></div>
      <div class="journal-card"><div class="journal-card-label">Jami R</div><div class="journal-card-value" id="journal-m-r">0R</div></div>
      <div class="journal-card"><div class="journal-card-label">Maks. pasayish</div><div class="journal-card-value" id="journal-m-dd">$0</div></div>
      <div class="journal-card"><div class="journal-card-label">Qoidaga rioya</div><div class="journal-card-value" id="journal-m-discipline">0%</div></div>
      <div class="journal-card"><div class="journal-card-label">Ko'rsatildi</div><div class="journal-card-value" id="journal-m-filtered">0 / 0</div></div>
    </div>

    <div class="journal-empty" id="journal-empty" style="display:none"></div>
    <div class="journal-toolbar">
      <button class="journal-button secondary" id="journal-export-csv" type="button">CSV hisobotni eksport qilish</button>
      <button class="journal-button secondary" id="journal-export-html" type="button">HTML hisobotni eksport qilish</button>
    </div>
    <section class="journal-insights">
      <h3>Avtomatik xulosalar</h3>
      <ul id="journal-insights-list"></ul>
    </section>
    <section class="journal-heatmap-wrap">
      <h3>Kun va soat bo'yicha natija</h3>
      <p>Rang jami R ni, raqam esa savdolar sonini ko'rsatadi.</p>
      <div class="journal-heatmap-scroll"><div class="journal-heatmap" id="journal-heatmap"></div></div>
    </section>
    <div class="journal-chart-wrap"><h3>Equity curve</h3><canvas id="journal-equity"></canvas></div>
    <div class="journal-rules">
      <h3>Qoidaga rioya va qoida buzilgan savdolar</h3>
      <div class="journal-rules-grid">
        <div class="journal-rule-card" id="journal-rules-yes"></div>
        <div class="journal-rule-card" id="journal-rules-no"></div>
      </div>
    </div>
    <div class="journal-breakdowns">
      <div class="journal-breakdown"><h3>Juftliklar bo'yicha</h3><div class="journal-table-scroll"><table class="journal-table compact"><thead><tr><th>Guruh</th><th>Savdo</th><th>WR</th><th>P&L</th><th>R</th></tr></thead><tbody id="journal-by-pair"></tbody></table></div></div>
      <div class="journal-breakdown"><h3>Setuplar bo'yicha</h3><div class="journal-table-scroll"><table class="journal-table compact"><thead><tr><th>Guruh</th><th>Savdo</th><th>WR</th><th>P&L</th><th>R</th></tr></thead><tbody id="journal-by-setup"></tbody></table></div></div>
      <div class="journal-breakdown"><h3>Yo'nalish bo'yicha</h3><div class="journal-table-scroll"><table class="journal-table compact"><thead><tr><th>Guruh</th><th>Savdo</th><th>WR</th><th>P&L</th><th>R</th></tr></thead><tbody id="journal-by-direction"></tbody></table></div></div>
      <div class="journal-breakdown"><h3>Hissiyotlar bo'yicha</h3><div class="journal-table-scroll"><table class="journal-table compact"><thead><tr><th>Guruh</th><th>Savdo</th><th>WR</th><th>P&L</th><th>R</th></tr></thead><tbody id="journal-by-emotion"></tbody></table></div></div>
    </div>
    <div class="journal-table-wrap">
      <h3>Oxirgi 30 savdo</h3>
      <div class="journal-table-scroll">
        <table class="journal-table">
          <thead><tr><th>Sana</th><th>Vaqt</th><th>Juftlik</th><th>Dir</th><th>Setup</th><th>Natija</th><th>P&L</th><th>R</th></tr></thead>
          <tbody id="journal-table-body"></tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<script id="journal-demo-data" type="text/plain">
id,date,time,pair,direction,setup,risk_usd,result_usd,result_r,outcome,followed_rules,emotions
1,2026-05-11,09:15,EURUSD,long,EMA50 pullback,10,20,2,win,yes,calm
2,2026-05-12,14:30,GBPUSD,short,Resistance rejection,10,-10,-1,loss,yes,calm
3,2026-05-13,16:10,EURUSD,long,Breakout,10,-10,-1,loss,no,frustrated
4,2026-05-14,10:40,USDJPY,short,London range,10,15,1.5,win,yes,calm
5,2026-05-15,18:20,GBPUSD,long,FOMO entry,10,-12,-1.2,loss,no,anxious
6,2026-05-18,11:05,EURUSD,long,EMA50 pullback,10,20,2,win,yes,calm
</script>

## Natijalarni qanday o'qish kerak

- **Win Rate** faqat Win/Loss bo'yicha hisoblanadi; break-even foizni buzmaydi.
- **Profit Factor** = jami foyda / jami zarar.
- **Jami R** `result_r` dan olinadi; maydon bo'lmasa, `result_usd / risk_usd`.
- **Maksimal pasayish** — equity oldingi cho'qqidan eng chuqur tushgan masofa.
- **Qoidaga rioya** — maydon to'ldirilgan savdolardagi `yes` ulushi.

Ishonchli xulosa uchun bitta strategiyada kamida **30 ta savdo** to'plang.

## Strategiya laboratoriyasi va mashqlar

Tanlangan strategiya versiyasi har bir savdo rejasi bilan saqlanadi. Qoidalar
o'zgarsa yangi versiya yaratiladi, shu sabab turli tajribalar statistikasi
aralashmaydi. Maqsadli savdolar soniga yetgach laboratoriya expectancy, intizom,
pasayish va jami R ni ko'rsatadi.

Yopilgan savdolardagi xatolar lokal mashqlar navbatini avtomatik yaratadi:
stopni ko'chirish, FOMO va qoida buzilishi Replay uchun 10 ta mashq vazifasiga
aylanadi. Navbat ma'lumotlari brauzerdan tashqariga chiqmaydi.
