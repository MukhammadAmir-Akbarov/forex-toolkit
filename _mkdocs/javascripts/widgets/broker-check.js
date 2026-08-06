/*
 * Проверка брокера — веб-версия tools/broker_check.py.
 *
 * Зачем: аудитория теряет деньги не на плохих сделках, а на конторах, из
 * которых нельзя вывести средства. CLI-версия умела строить ссылки на реестры
 * регуляторов, но жила за установкой Python.
 *
 * Ссылки на реестры и историческая база лицензий обязаны совпадать с
 * tools/broker_check.py — это проверяет tests/test_broker_check_widget.py.
 * Сам HTTP-запрос к регулятору из браузера невозможен (CORS) и не нужен:
 * решение принимает человек, открыв официальный реестр.
 */
(function () {
  "use strict";

  var root = document.getElementById("broker-check-widget");
  if (!root || !window.FXW) return;

  var F = window.FXW;

  // Ключи и URL — копия REGULATORS из tools/broker_check.py.
  var REGULATORS = [
    { id: "FCA", flag: "🇬🇧", search: "https://register.fca.org.uk/s/search?q={name}&type=Companies" },
    { id: "CySEC", flag: "🇨🇾", search: "https://www.cysec.gov.cy/en-GB/entities/investment-firms/cypriot/?searchTerm={name}" },
    { id: "ASIC", flag: "🇦🇺", search: "https://connectonline.asic.gov.au/RegistrySearch/faces/landing/SearchRegisters.jspx?searchText={name}" },
    { id: "NFA", flag: "🇺🇸", search: "https://www.nfa.futures.org/BasicNet/basic-profile.aspx?nfaid={name}" },
    { id: "FINMA", flag: "🇨🇭", search: "https://www.finma.ch/en/finma-public/authorised-institutions-individuals-and-products/" }
  ];

  // Копия KNOWN_BROKERS: исторические ориентиры, а не текущий статус.
  var KNOWN = {
    "exness": ["FCA: Exness (UK) Ltd — №730729", "CySEC: Exness (Cy) Ltd — №178/12", "FSA Seychelles — менее жёсткий регулятор"],
    "ic markets": ["ASIC: IC Markets Ltd — №335692", "CySEC: IC Markets EU — №362/18"],
    "pepperstone": ["FCA: Pepperstone Ltd — №684312", "ASIC: Pepperstone Group Ltd — №414530", "CySEC: Pepperstone EU — №388/20"],
    "fxpro": ["FCA: FxPro UK Ltd — №509956", "CySEC: FxPro Financial Services — №078/07"],
    "tickmill": ["FCA: Tickmill UK Ltd — №717270", "CySEC: Tickmill Europe — №278/15", "FSCA: Tickmill SA — FSP 49464"],
    "fp markets": ["ASIC: First Prudential Markets — №286354", "CySEC: FP Markets EU — №371/18"]
  };

  var T = F.pick({
    ru: {
      label: "Название брокера", placeholder: "например, IC Markets",
      check: "Проверить", need: "Введи название брокера.",
      registries: "Открой реестры и найди брокера сам",
      knownTitle: "Есть в справочнике проекта",
      knownNote: "Это исторические ориентиры, а не текущий статус. Лицензию могли отозвать — проверь по ссылкам выше.",
      unknownTitle: "Брокера нет в справочнике",
      unknownNote: "Это ничего не говорит о его честности — справочник маленький. Проверь по реестрам сами.",
      flagsTitle: "Красные флаги — отметь всё, что узнаёшь",
      flags: [
        "Обещают гарантированную прибыль или «доход без риска»",
        "Торопят внести деньги сегодня, дают бонус за срочность",
        "Не отвечают прямо, к какому юрлицу подключается мой счёт",
        "Вывод средств откладывают или просят внести ещё для вывода",
        "Нашёл их через рекламу с дорогими машинами или «сигналами»",
        "Менеджер сам предлагает сделки или доступ к моему счёту",
        "Лицензия только офшорная, а сайт говорит о европейском регуляторе"
      ],
      verdictNone: "Явных красных флагов нет. Всё равно проверь лицензию в реестре и начни с минимальной суммы.",
      verdictSome: "Есть тревожные признаки. Не вноси деньги, пока не проверишь лицензию в официальном реестре.",
      verdictMany: "Очень похоже на схему по отъёму денег. Настоятельно не вноси средства.",
      askTitle: "Спроси у брокера один вопрос",
      ask: "«К какому юрлицу подключается мой счёт и какой у него регулятор?» Уклончивый ответ — сам по себе красный флаг: у крупных брокеров обычно несколько компаний, и клиентов из СНГ часто подключают к офшорной, где защиты почти нет."
    },
    en: {
      label: "Broker name", placeholder: "for example, IC Markets",
      check: "Check", need: "Enter the broker name.",
      registries: "Open the registries and look the broker up yourself",
      knownTitle: "Listed in the project reference",
      knownNote: "These are historical reference points, not current status. A licence can be withdrawn — check the links above.",
      unknownTitle: "Not in the reference list",
      unknownNote: "That says nothing about honesty — the list is small. Check the registries yourself.",
      flagsTitle: "Red flags — tick everything you recognise",
      flags: [
        "They promise guaranteed profit or income without risk",
        "They rush you to deposit today, with a bonus for hurrying",
        "They will not say plainly which legal entity holds my account",
        "Withdrawals get delayed, or they ask for another deposit to release one",
        "I found them through adverts with expensive cars or paid signals",
        "A manager offers to trade for me or wants access to my account",
        "The licence is offshore only, while the site talks about an EU regulator"
      ],
      verdictNone: "No obvious red flags. Still verify the licence in a registry and start with a minimal amount.",
      verdictSome: "There are warning signs. Do not deposit until you have verified the licence in an official registry.",
      verdictMany: "This looks a lot like a scheme to take your money. Strongly do not deposit.",
      askTitle: "Ask the broker one question",
      ask: "\"Which legal entity holds my account and who regulates it?\" An evasive answer is itself a red flag: large brokers usually have several companies, and clients from our region are often attached to an offshore one with almost no protection."
    },
    uz: {
      label: "Broker nomi", placeholder: "masalan, IC Markets",
      check: "Tekshirish", need: "Broker nomini kiriting.",
      registries: "Reyestrlarni oching va brokerni o'zingiz qidiring",
      knownTitle: "Loyiha ma'lumotnomasida bor",
      knownNote: "Bu tarixiy ma'lumot, hozirgi holat emas. Litsenziya bekor qilingan bo'lishi mumkin — yuqoridagi havolalar orqali tekshiring.",
      unknownTitle: "Ma'lumotnomada yo'q",
      unknownNote: "Bu uning halolligi haqida hech nima demaydi — ro'yxat kichik. Reyestrlardan o'zingiz tekshiring.",
      flagsTitle: "Qizil bayroqlar — tanish bo'lganini belgilang",
      flags: [
        "Kafolatlangan foyda yoki \"risksiz daromad\" va'da qilishadi",
        "Bugun pul kiritishga shoshirishadi, tezkorlik uchun bonus berishadi",
        "Hisobim qaysi yuridik shaxsga ulanishini aniq aytishmaydi",
        "Pul yechishni kechiktirishadi yoki yechish uchun yana pul so'rashadi",
        "Ularni qimmat mashinali yoki \"signal\" sotadigan reklama orqali topdim",
        "Menejer o'zi savdo taklif qiladi yoki hisobimga kirish so'raydi",
        "Litsenziya faqat ofshor, sayt esa Yevropa regulyatori haqida gapiradi"
      ],
      verdictNone: "Aniq qizil bayroqlar yo'q. Baribir litsenziyani reyestrda tekshiring va eng kichik summadan boshlang.",
      verdictSome: "Xavotirli belgilar bor. Litsenziyani rasmiy reyestrda tekshirmaguningizcha pul kiritmang.",
      verdictMany: "Bu pulni olib qo'yish sxemasiga juda o'xshaydi. Pul kiritmang.",
      askTitle: "Brokerdan bitta savol so'rang",
      ask: "\"Hisobim qaysi yuridik shaxsga ulanadi va uni kim tartibga soladi?\" Aylanma javobning o'zi qizil bayroq: yirik brokerlarda odatda bir necha kompaniya bo'ladi va bizning mintaqa mijozlari ko'pincha himoyasi deyarli yo'q ofshor kompaniyaga ulanadi."
    }
  });

  root.innerHTML = '<div class="fx-tool">' +
    '<label for="bc-name">' + F.escape(T.label) + '</label>' +
    '<input id="bc-name" type="text" autocomplete="off" placeholder="' + F.escape(T.placeholder) + '">' +
    '<div class="fx-tool-actions"><button type="button" id="bc-check">' + F.escape(T.check) + '</button></div>' +
    '<div id="bc-result" role="status" aria-live="polite" hidden></div></div>';

  function knownFor(name) {
    var key = name.toLowerCase().trim();
    var hit = Object.keys(KNOWN).filter(function (candidate) {
      return candidate.indexOf(key) >= 0 || key.indexOf(candidate) >= 0;
    })[0];
    return hit ? { name: hit, entries: KNOWN[hit] } : null;
  }

  function render() {
    var name = document.getElementById("bc-name").value.trim();
    var box = document.getElementById("bc-result");
    if (!name) {
      box.hidden = false;
      box.className = "broker-check__result is-warning";
      box.innerHTML = "<p>" + F.escape(T.need) + "</p>";
      return;
    }
    var encoded = encodeURIComponent(name);
    var links = REGULATORS.map(function (regulator) {
      var url = regulator.search.replace("{name}", encoded);
      return '<li>' + regulator.flag + ' <a href="' + F.escape(url) +
        '" target="_blank" rel="noopener noreferrer">' + F.escape(regulator.id) + '</a></li>';
    }).join("");

    var known = knownFor(name);
    var knownBlock = known
      ? '<h4>' + F.escape(T.knownTitle) + '</h4><ul>' + known.entries.map(function (entry) {
        return "<li>" + F.escape(entry) + "</li>";
      }).join("") + '</ul><p>' + F.escape(T.knownNote) + '</p>'
      : '<h4>' + F.escape(T.unknownTitle) + '</h4><p>' + F.escape(T.unknownNote) + '</p>';

    var flags = T.flags.map(function (flag, index) {
      return '<label class="risk-profile__option"><input type="checkbox" class="bc-flag" value="' +
        index + '"> <span>' + F.escape(flag) + '</span></label>';
    }).join("");

    box.hidden = false;
    box.className = "broker-check__result";
    box.innerHTML = '<h4>' + F.escape(T.registries) + '</h4>' +
      '<ul class="broker-check__registries">' + links + '</ul>' +
      knownBlock +
      '<h4>' + F.escape(T.flagsTitle) + '</h4>' +
      '<div class="broker-check__flags">' + flags + '</div>' +
      '<p id="bc-verdict" aria-live="polite"></p>' +
      '<h4>' + F.escape(T.askTitle) + '</h4><p>' + F.escape(T.ask) + '</p>';

    box.querySelectorAll(".bc-flag").forEach(function (input) {
      input.addEventListener("change", verdict);
    });
    verdict();
    if (window.fxTrack) window.fxTrack("broker_check_completed");
  }

  function verdict() {
    var checked = document.querySelectorAll(".bc-flag:checked").length;
    var box = document.getElementById("bc-result");
    var text = checked === 0 ? T.verdictNone : checked <= 2 ? T.verdictSome : T.verdictMany;
    box.className = "broker-check__result" + (checked ? " is-warning" : "");
    document.getElementById("bc-verdict").innerHTML = "<strong>" + F.escape(text) + "</strong>";
  }

  document.getElementById("bc-check").addEventListener("click", render);
  document.getElementById("bc-name").addEventListener("keydown", function (event) {
    if (event.key === "Enter") render();
  });
})();
