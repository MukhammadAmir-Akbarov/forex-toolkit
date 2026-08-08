/*
 * «Сколько нужно, чтобы жить с трейдинга» — холодный душ в местных цифрах.
 *
 * Зачем: «брось работу и живи с трейдинга» — обещание, на котором продают
 * курсы и сигналы. Проект честно говорит, что реалистичная доходность скучная,
 * но нигде не показывал, что из этого следует в деньгах. А следует простое:
 * капитал должен быть примерно в семьдесят раз больше месячных расходов.
 *
 * Математика — зеркало forex_toolkit/living_capital.py, сверка в tests_e2e.
 */
(function () {
  var root = document.getElementById("living-capital-widget");
  if (!root || !window.FXW) return;

  var F = window.FXW;
  var TAX_RATE = 0.12;
  var MAX_MONTHS = 12 * 60;

  var T = F.pick({
    ru: {
      needLabel: "Сколько нужно в месяц на жизнь, $",
      returnLabel: "Месячная доходность, %",
      bufferLabel: "Подушка, месяцев расходов",
      startLabel: "Есть сейчас, $",
      addLabel: "Могу откладывать в месяц, $",
      rateLabel: "Курс USD → UZS",
      calc: "Посчитать",
      capital: "Торговый капитал",
      buffer: "Подушка отдельно",
      total: "Всего нужно",
      gross: "Заработать до налога",
      time: "Копить при твоих вводных",
      never: "при таких вводных цель не достигается",
      months: function (n) {
        var years = Math.floor(n / 12), rest = n % 12;
        return years ? years + " г. " + rest + " мес." : n + " мес.";
      },
      ratio: function (times) {
        return "Капитал больше месячных расходов в " + times + " раз.";
      },
      note: "Расчёт учитывает НДФЛ 12%: чтобы получить на руки, заработать надо больше. Подушку держат отдельно от торгового счёта — иначе убыточный месяц съедает сам капитал.",
      warn: "Это оценка порядка величины при заданной доходности, а не план. Стабильной доходности не бывает: убыточные месяцы есть у всех, и именно поэтому снимать всё до копейки нельзя.",
      errNeed: "Укажи месячные расходы больше нуля.",
      errReturn: "Месячная доходность — от 0.1% до 99%.",
      errRate: "Курс должен быть больше нуля."
    },
    en: {
      needLabel: "Monthly living costs, $",
      returnLabel: "Monthly return, %",
      bufferLabel: "Buffer, months of expenses",
      startLabel: "Have right now, $",
      addLabel: "Can save per month, $",
      rateLabel: "USD → UZS rate",
      calc: "Calculate",
      capital: "Trading capital",
      buffer: "Buffer, held separately",
      total: "Needed in total",
      gross: "Must earn before tax",
      time: "Time to save it up",
      never: "not reachable with these inputs",
      months: function (n) {
        var years = Math.floor(n / 12), rest = n % 12;
        return years ? years + "y " + rest + "m" : n + " months";
      },
      ratio: function (times) {
        return "The capital is " + times + " times your monthly costs.";
      },
      note: "The figure includes 12% income tax: to take money home you must earn more. The buffer is held away from the trading account — otherwise a losing month eats the capital itself.",
      warn: "This is an order-of-magnitude estimate at the return you entered, not a plan. Returns are never steady: everyone has losing months, which is exactly why you cannot withdraw every last dollar.",
      errNeed: "Enter monthly costs above zero.",
      errReturn: "Monthly return must be between 0.1% and 99%.",
      errRate: "The rate must be above zero."
    },
    uz: {
      needLabel: "Oyiga yashash uchun kerak, $",
      returnLabel: "Oylik daromad, %",
      bufferLabel: "Zaxira, necha oylik xarajat",
      startLabel: "Hozir bor, $",
      addLabel: "Oyiga jamg'ara olaman, $",
      rateLabel: "USD → UZS kursi",
      calc: "Hisoblash",
      capital: "Savdo kapitali",
      buffer: "Zaxira, alohida saqlanadi",
      total: "Jami kerak",
      gross: "Soliqqacha ishlash kerak",
      time: "Shu vvodnilar bilan jamg'arish",
      never: "bunday shartlarda maqsadga erishilmaydi",
      months: function (n) {
        var years = Math.floor(n / 12), rest = n % 12;
        return years ? years + " yil " + rest + " oy" : n + " oy";
      },
      ratio: function (times) {
        return "Kapital oylik xarajatdan " + times + " barobar katta.";
      },
      note: "Hisobda JShDS 12% inobatga olingan: qo'lga olish uchun ko'proq ishlash kerak. Zaxira savdo hisobidan alohida saqlanadi — aks holda zararli oy kapitalning o'zini yeydi.",
      warn: "Bu siz kiritgan daromad bo'yicha kattalik tartibi bahosi, reja emas. Barqaror daromad bo'lmaydi: zararli oylar hammada bor, shuning uchun hammasini oxirgi tiyinigacha yechib bo'lmaydi.",
      errNeed: "Oylik xarajatni noldan katta kiriting.",
      errReturn: "Oylik daromad 0.1% dan 99% gacha bo'lishi kerak.",
      errRate: "Kurs noldan katta bo'lishi kerak."
    }
  });

  function monthsToReach(target, start, monthlyAdd, monthlyReturn) {
    if (target <= 0) return 0;
    if (start >= target) return 0;
    if (monthlyReturn <= 0 && monthlyAdd <= 0) return null;
    var balance = start;
    for (var month = 1; month <= MAX_MONTHS; month++) {
      balance = balance * (1 + monthlyReturn) + monthlyAdd;
      if (balance >= target) return month;
    }
    return null;
  }

  function planFor(need, monthlyReturn, bufferMonths, start, monthlyAdd) {
    var gross = need / (1 - TAX_RATE);
    var capital = gross / monthlyReturn;
    var buffer = need * bufferMonths;
    var total = capital + buffer;
    return {
      monthly_need: need,
      gross_needed: gross,
      required_capital: capital,
      buffer: buffer,
      total_needed: total,
      months_to_reach: monthsToReach(total, start, monthlyAdd, monthlyReturn)
    };
  }

  window.__fxLivingCapital = planFor;

  root.innerHTML = '<div class="pos-calc-widget">' +
    field("lc-need", T.needLabel, 500, 1, "any") +
    field("lc-return", T.returnLabel, 1.5, 0.1, "0.1") +
    field("lc-buffer", T.bufferLabel, 6, 0, "1") +
    field("lc-start", T.startLabel, 1000, 0, "any") +
    field("lc-add", T.addLabel, 200, 0, "any") +
    field("lc-rate", T.rateLabel, 12500, 1, "any") +
    '<button type="button" id="lc-calc-btn" class="pc-row-wide">' + F.escape(T.calc) + "</button>" +
    '<div id="lc-result" role="status" aria-live="polite" hidden></div></div>';

  function field(id, label, value, min, step) {
    return '<label for="' + id + '">' + F.escape(label) + "</label>" +
      '<input type="number" id="' + id + '" value="' + value + '" min="' + min +
      '" step="' + step + '" autocomplete="off">';
  }

  function uzs(value, rate) {
    return F.int(Math.round(value * rate)) + " UZS";
  }

  // F.money жёстко ставит minimumFractionDigits: 2, поэтому просить у неё
  // ноль знаков нельзя — Intl бросает RangeError, когда минимум больше
  // максимума. Для крупных сумм округляем сами.
  function whole(value) {
    return "$" + F.int(Math.round(value));
  }

  function row(label, value, extra) {
    return '<div class="tax-result-row"><span>' + F.escape(label) + "</span><span>" +
      value + (extra ? ' <small>' + extra + "</small>" : "") + "</span></div>";
  }

  function calculate() {
    var need = parseFloat(document.getElementById("lc-need").value);
    var percent = parseFloat(document.getElementById("lc-return").value);
    var bufferMonths = parseInt(document.getElementById("lc-buffer").value, 10);
    var start = parseFloat(document.getElementById("lc-start").value);
    var add = parseFloat(document.getElementById("lc-add").value);
    var rate = parseFloat(document.getElementById("lc-rate").value);
    var box = document.getElementById("lc-result");

    var errors = [];
    if (!(need > 0)) errors.push(T.errNeed);
    if (!(percent >= 0.1 && percent <= 99)) errors.push(T.errReturn);
    if (!(rate > 0)) errors.push(T.errRate);
    if (!(bufferMonths >= 0)) bufferMonths = 0;
    if (!(start >= 0)) start = 0;
    if (!(add >= 0)) add = 0;

    box.hidden = false;
    if (errors.length) {
      box.className = "calc-result calc-error";
      box.innerHTML = errors.map(function (message) {
        return "<p>⛔ " + F.escape(message) + "</p>";
      }).join("");
      return;
    }

    var plan = planFor(need, percent / 100, bufferMonths, start, add);
    var times = Math.round(plan.total_needed / need);

    box.className = "calc-result calc-warn";
    box.innerHTML =
      '<div class="tax-headline">' + whole(plan.total_needed) + "</div>" +
      '<div class="tax-subhead">' + F.escape(T.total) + "</div>" +
      row(T.capital, whole(plan.required_capital), uzs(plan.required_capital, rate)) +
      row(T.buffer, whole(plan.buffer), uzs(plan.buffer, rate)) +
      row(T.gross, F.money(plan.gross_needed, 2)) +
      row(T.time, plan.months_to_reach === null
        ? F.escape(T.never)
        : F.escape(T.months(plan.months_to_reach))) +
      "<p><strong>" + F.escape(T.ratio(times)) + "</strong></p>" +
      '<p class="journal-tax-note">' + F.escape(T.note) + "</p>" +
      '<p class="journal-tax-note">' + F.escape(T.warn) + "</p>";

    if (window.fxTrack) window.fxTrack("calculator_completed");
  }

  document.getElementById("lc-calc-btn").addEventListener("click", calculate);
  ["lc-need", "lc-return", "lc-buffer", "lc-start", "lc-add", "lc-rate"].forEach(function (id) {
    document.getElementById(id).addEventListener("change", calculate);
  });
  calculate();
})();
