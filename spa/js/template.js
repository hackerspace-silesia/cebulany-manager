function renderTableLoading(locals) {
var buf = [];
var jade_mixins = {};
var jade_interp;

buf.push("<tr><td class=\"loading\"><img src=\"img/firemark.png\"/><br/><strong>Loading…</strong></td></tr>");;return buf.join("");
}
function renderTableTransactions(locals) {
var buf = [];
var jade_mixins = {};
var jade_interp;
;var locals_for_with = (locals || {});(function (maxChars, sum, transactions, undefined) {
jade_mixins["transaction_row"] = jade_interp = function(row){
var block = (this && this.block), attributes = (this && this.attributes) || {};
buf.push("<tr><td>" + (jade.escape(null == (jade_interp = row.date) ? "" : jade_interp)) + "</td><td" + (jade.attr("title", row.name, true, false)) + ">" + (jade.escape(null == (jade_interp = maxChars(row.name, 60)) ? "" : jade_interp)) + "</td><td" + (jade.attr("title", row.title, true, false)) + ">" + (jade.escape(null == (jade_interp = maxChars(row.title, 60)) ? "" : jade_interp)) + "</td><td" + (jade.cls(['price',row.cost < 0 ? 'negative' : 'positive'], [null,true])) + ">" + (jade.escape(null == (jade_interp = row.cost + " zł") ? "" : jade_interp)) + "</td><td" + (jade.attr("title", row.iban, true, false)) + ">" + (jade.escape(null == (jade_interp = maxChars(row.iban && row.iban.replace(/ /g, ''), 5)) ? "" : jade_interp)) + "</td><td><a onclick=\"addNewTypeTransaction\" class=\"btn\">+</a></td></tr>");
};
jade_mixins["foot_row"] = jade_interp = function(title, value){
var block = (this && this.block), attributes = (this && this.attributes) || {};
buf.push("<tr><th>" + (jade.escape(null == (jade_interp = title) ? "" : jade_interp)) + "</th><th colspan=\"2\"></th><th class=\"price\"><strong>" + (jade.escape(null == (jade_interp = value) ? "" : jade_interp)) + "</strong></th><th colspan=\"2\"></th></tr>");
};
buf.push("<thead><tr><th>Data</th><th>Nazwa</th><th>Tytuł</th><th>Kwota</th><th>IBAN</th><th>Typy </th></tr></thead><tbody>");
// iterate transactions
;(function(){
  var $$obj = transactions;
  if ('number' == typeof $$obj.length) {

    for (var $index = 0, $$l = $$obj.length; $index < $$l; $index++) {
      var row = $$obj[$index];

jade_mixins["transaction_row"](row);
    }

  } else {
    var $$l = 0;
    for (var $index in $$obj) {
      $$l++;      var row = $$obj[$index];

jade_mixins["transaction_row"](row);
    }

  }
}).call(this);

buf.push("</tbody><tfoot>");
jade_mixins["foot_row"]('SUMA', sum + ' zł');
jade_mixins["foot_row"]('TOTAL', transactions.length);
buf.push("</tfoot>");}.call(this,"maxChars" in locals_for_with?locals_for_with.maxChars:typeof maxChars!=="undefined"?maxChars:undefined,"sum" in locals_for_with?locals_for_with.sum:typeof sum!=="undefined"?sum:undefined,"transactions" in locals_for_with?locals_for_with.transactions:typeof transactions!=="undefined"?transactions:undefined,"undefined" in locals_for_with?locals_for_with.undefined:typeof undefined!=="undefined"?undefined:undefined));;return buf.join("");
}
function renderTransactions(locals) {
var buf = [];
var jade_mixins = {};
var jade_interp;

buf.push("<h1>Przelewy</h1><form name=\"transactions\"><fieldset><legend>Data</legend><label>Miesiac</label><input type=\"radio\" name=\"has_month\" value=\"y\" checked=\"checked\"/><label>Zakres</label><input type=\"radio\" name=\"has_month\" value=\"n\"/><div id=\"transaction-month\"><input type=\"month\" name=\"month\"/></div><div id=\"transaction-range\" class=\"disabled\"><label>Od dnia</label><input type=\"date\" name=\"date_start\" disabled=\"disabled\"/><br/><label>Do dnia</label><input type=\"date\" name=\"date_end\" disabled=\"disabled\"/></div></fieldset><fieldset><legend>mniejszy od</legend><input type=\"number\" min=\"0\" step=\"0.01\" name=\"cost_le\"/></fieldset><fieldset><legend>większy od</legend><input type=\"number\" min=\"0\" step=\"0.01\" name=\"cost_ge\"/></fieldset><fieldset><legend>Szukaj</legend><input type=\"search\" name=\"text\"/></fieldset><fieldset><legend>Opcje</legend><input type=\"checkbox\" name=\"negative\" value=\"t\"/><span>Ujemne?</span><input type=\"checkbox\" name=\"positive\" value=\"t\"/><span>Dodatnie?</span></fieldset></form><table id=\"transactions\"></table>");;return buf.join("");
}