(function () {
  "use strict";
  var root = document.getElementById("trade-desk-widget");
  if (!root || !window.FXW) return;
  var F = window.FXW;
  var T = F.pick({
    ru: { balance:"Депозит, USD", risk:"Риск, %", pair:"Пара", direction:"Направление", stop:"Стоп, пипсы", pip:"USD/пипс на 1 лот", rate:"USD -> UZS", setup:"Сетап", notes:"Причина входа / заметка", calculate:"1. Рассчитать", checks:"2. Проверить план", save:"3. Сохранить черновик", download:"Скачать CSV для журнала", riskAmount:"Риск", lot:"Размер позиции", all:"Отметь все пункты перед сохранением.", saved:"Черновик сохранён только в этом браузере.", checklist:["Сетап соответствует торговому плану","Стоп определён до входа","Нет важной новости рядом со входом","Совокупный риск остаётся в лимите","Принимаю полный убыток без переноса стопа"] },
    en: { balance:"Balance, USD", risk:"Risk, %", pair:"Pair", direction:"Direction", stop:"Stop, pips", pip:"USD/pip per lot", rate:"USD -> UZS", setup:"Setup", notes:"Entry reason / note", calculate:"1. Calculate", checks:"2. Verify the plan", save:"3. Save draft", download:"Download journal CSV", riskAmount:"Risk", lot:"Position size", all:"Check every item before saving.", saved:"Draft saved only in this browser.", checklist:["Setup matches the trading plan","Stop is defined before entry","No major news near the entry","Aggregate risk remains within the limit","I accept the full loss without moving the stop"] },
    uz: { balance:"Depozit, USD", risk:"Risk, %", pair:"Juftlik", direction:"Yo'nalish", stop:"Stop, pip", pip:"1 lot uchun USD/pip", rate:"USD -> UZS", setup:"Setap", notes:"Kirish sababi / izoh", calculate:"1. Hisoblash", checks:"2. Rejani tekshirish", save:"3. Qoralamani saqlash", download:"Jurnal uchun CSV yuklash", riskAmount:"Risk", lot:"Pozitsiya hajmi", all:"Saqlashdan oldin barcha bandlarni belgilang.", saved:"Qoralama faqat shu brauzerda saqlandi.", checklist:["Setap savdo rejasiga mos","Stop kirishdan oldin belgilangan","Kirish yaqinida muhim yangilik yo'q","Umumiy risk limit ichida","Stopni ko'chirmasdan to'liq zararni qabul qilaman"] }
  });
  var labels = { long: F.lang === "uz" ? "Long" : "Long", short: "Short" };
  root.innerHTML = '<div class="fx-tool-grid">' + field(T.balance,'<input id="td-balance" type="number" min="1" value="1000">') + field(T.risk,'<input id="td-risk" type="number" min="0.1" max="10" step="0.1" value="1">') + field(T.pair,'<input id="td-pair" value="EURUSD" maxlength="7">') + field(T.direction,'<select id="td-direction"><option value="long">'+labels.long+'</option><option value="short">'+labels.short+'</option></select>') + field(T.stop,'<input id="td-stop" type="number" min="0.1" value="20">') + field(T.pip,'<input id="td-pip" type="number" min="0.01" step="0.01" value="10">') + field(T.rate,'<input id="td-rate" type="number" min="1" value="12500">') + field(T.setup,'<input id="td-setup" value="pullback">') + '</div>' + field(T.notes,'<textarea id="td-notes" rows="3"></textarea>') + '<div class="fx-tool-actions"><button type="button" id="td-calc">'+T.calculate+'</button></div><div id="td-result" class="fx-result" hidden></div><h3>'+T.checks+'</h3><div id="td-checks" class="fx-checks">' + T.checklist.map(function(item,index){return '<label><input type="checkbox" data-check="'+index+'"> <span>'+item+'</span></label>';}).join('') + '</div><div class="fx-tool-actions"><button type="button" id="td-save">'+T.save+'</button><button type="button" id="td-download" class="fx-secondary" disabled>'+T.download+'</button></div><p id="td-status" class="fx-tool-note"></p>';
  var current = null;
  function field(label, control) { return '<label><span>'+label+'</span>'+control+'</label>'; }
  function value(id) { return Number(document.getElementById(id).value); }
  function calculate() {
    var balance=value("td-balance"), riskPct=value("td-risk"), stop=value("td-stop"), pip=value("td-pip"), rate=value("td-rate");
    if (!(balance>0 && riskPct>0 && stop>0 && pip>0 && rate>0)) return;
    var risk=balance*riskPct/100;
    var raw=risk/(stop*pip);
    var lot=Math.floor(raw*100)/100;
    var pair=document.getElementById("td-pair").value.toUpperCase().replace("/","").trim();
    current={date:new Date().toISOString().slice(0,10),pair:pair,direction:document.getElementById("td-direction").value,lot_size:lot,risk_usd:risk,setup:document.getElementById("td-setup").value.trim(),notes:document.getElementById("td-notes").value.trim()};
    var result=document.getElementById("td-result");
    result.innerHTML='<div class="fx-metrics"><div><span>'+T.riskAmount+'</span><strong>'+F.money(risk)+' / '+Math.round(risk*rate).toLocaleString(F.numLocale)+' UZS</strong></div><div><span>'+T.lot+'</span><strong>'+lot.toFixed(2)+' lot</strong></div></div>';
    result.hidden=false;
  }
  function allChecked(){return Array.prototype.every.call(document.querySelectorAll("#td-checks input"),function(input){return input.checked;});}
  function save(){
    if(!current) calculate();
    if(!current || !allChecked()){document.getElementById("td-status").textContent=T.all;return;}
    try{var drafts=JSON.parse(localStorage.getItem("forex_trade_drafts_v1")||"[]");drafts.unshift(current);localStorage.setItem("forex_trade_drafts_v1",JSON.stringify(drafts.slice(0,20)));}catch(error){}
    document.getElementById("td-status").textContent=T.saved;
    document.getElementById("td-download").disabled=false;
    if(window.fxTrack)window.fxTrack("trade_plan_saved",{once:false});
  }
  function csvCell(value){var text=String(value==null?"":value);return /[",\n]/.test(text)?'"'+text.replace(/"/g,'""')+'"':text;}
  function download(){
    if(!current)return;
    var headers=["date","pair","direction","lot_size","risk_usd","outcome","followed_rules","setup","notes"];
    var row=[current.date,current.pair,current.direction,current.lot_size,current.risk_usd,"open","yes",current.setup,current.notes];
    var blob=new Blob([headers.join(",")+"\n"+row.map(csvCell).join(",")+"\n"],{type:"text/csv;charset=utf-8"});
    var url=URL.createObjectURL(blob),a=document.createElement("a");a.href=url;a.download="trade-plan-"+current.date+".csv";a.click();URL.revokeObjectURL(url);
  }
  document.getElementById("td-calc").addEventListener("click",calculate);
  document.getElementById("td-save").addEventListener("click",save);
  document.getElementById("td-download").addEventListener("click",download);
})();
