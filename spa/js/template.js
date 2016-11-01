function renderModalAddNewTypeTransaction(locals) {
var buf = [];
var jade_mixins = {};
var jade_interp;
;var locals_for_with = (locals || {});(function (transaction) {
buf.push("<div class=\"modal-content\"><table class=\"summary\"><tr><th>Data</th><td>" + (jade.escape(null == (jade_interp = transaction.date) ? "" : jade_interp)) + "</td></tr><tr><th>Nazwa</th><td>" + (jade.escape(null == (jade_interp = transaction.name) ? "" : jade_interp)) + "</td></tr><tr><th>Tytuł</th><td>" + (jade.escape(null == (jade_interp = transaction.title) ? "" : jade_interp)) + "</td></tr><tr><th>IBAN</th><td>" + (jade.escape(null == (jade_interp = transaction.iban) ? "" : jade_interp)) + "</td></tr></table><form name=\"select_type\"><legend>Typ przelewu:</legend><input type=\"radio\" name=\"type\" value=\"paid_month\" checked=\"checked\" onchange=\"view.changeModalForm()\"/><label>Składka</label><input type=\"radio\" name=\"type\" value=\"bill\" onchange=\"view.changeModalForm()\"/><label>Rachunek</label><input type=\"radio\" name=\"type\" value=\"donation\" onchange=\"view.changeModalForm()\"/><label>Darowizna</label></form><form name=\"add_type_paid_month\" class=\"form\"><input type=\"hidden\" name=\"transaction_id\"" + (jade.attr("value", transaction.id, true, false)) + "/><fieldset><legend>Członek</legend><input type=\"search\" name=\"user\" list=\"type_users\" onchange=\"view.seekUsers()\"/><datalist id=\"type_users\"></datalist></fieldset><fieldset><legend>Miesiąc</legend><input type=\"month\" name=\"date\"" + (jade.attr("value", transaction.date.slice(0, 7), true, false)) + "/></fieldset><fieldset><legend>Kwota</legend><input type=\"number\" name=\"cost\" min=\"0\"" + (jade.attr("value", transaction.cost, true, false)) + "/></fieldset></form><form name=\"add_type_bill\" class=\"disabled form\"><input type=\"hidden\" name=\"transaction_id\"" + (jade.attr("value", transaction.id, true, false)) + "/><fieldset><legend>Kwota</legend><input type=\"number\" name=\"cost\" min=\"0\"" + (jade.attr("value", transaction.cost, true, false)) + "/></fieldset><fieldset><legend>Nazwa</legend><input type=\"text\" name=\"name\" min=\"0\"" + (jade.attr("value", transaction.title, true, false)) + "/></fieldset></form><form name=\"add_type_donation\" class=\"disabled form\"><input type=\"hidden\" name=\"transaction_id\"" + (jade.attr("value", transaction.id, true, false)) + "/><fieldset><legend>Kwota</legend><input type=\"number\" name=\"cost\" min=\"0\"" + (jade.attr("value", transaction.cost, true, false)) + "/></fieldset><fieldset><legend>Nazwa</legend><input type=\"text\" name=\"name\" min=\"0\"" + (jade.attr("value", transaction.title, true, false)) + "/></fieldset></form><button type=\"button\" onclick=\"view.addType()\">Dodaj</button><button type=\"button\" onclick=\"view.closeModal()\">Zamknij</button></div>");}.call(this,"transaction" in locals_for_with?locals_for_with.transaction:typeof transaction!=="undefined"?transaction:undefined));;return buf.join("");
}
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
jade_mixins["transaction_row"] = jade_interp = function(num, row){
var block = (this && this.block), attributes = (this && this.attributes) || {};
buf.push("<tr><td>" + (jade.escape(null == (jade_interp = row.date) ? "" : jade_interp)) + "</td><td" + (jade.attr("title", row.name, true, false)) + ">" + (jade.escape(null == (jade_interp = maxChars(row.name, 60)) ? "" : jade_interp)) + "</td><td" + (jade.attr("title", row.title, true, false)) + ">" + (jade.escape(null == (jade_interp = maxChars(row.title, 60)) ? "" : jade_interp)) + "</td><td" + (jade.cls(['price',row.cost < 0 ? 'negative' : 'positive'], [null,true])) + ">" + (jade.escape(null == (jade_interp = row.cost + " zł") ? "" : jade_interp)) + "</td><td" + (jade.attr("title", row.iban, true, false)) + ">" + (jade.escape(null == (jade_interp = maxChars(row.iban && row.iban.replace(/ /g, ''), 5)) ? "" : jade_interp)) + "</td><td><a" + (jade.attr("onclick", 'view.addNewTypeTransaction(' + (num) + ')', true, false)) + " class=\"btn\">+</a></td></tr>");
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

    for (var num = 0, $$l = $$obj.length; num < $$l; num++) {
      var row = $$obj[num];

jade_mixins["transaction_row"](num, row);
    }

  } else {
    var $$l = 0;
    for (var num in $$obj) {
      $$l++;      var row = $$obj[num];

jade_mixins["transaction_row"](num, row);
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

jade_mixins["query_input"] = jade_interp = function(){
var block = (this && this.block), attributes = (this && this.attributes) || {};
buf.push("<input" + (jade.attrs(jade.merge([{"onchange": "view.getTransactions()"},attributes]), false)) + "/>");
};
jade_mixins["text_query_input"] = jade_interp = function(){
var block = (this && this.block), attributes = (this && this.attributes) || {};
buf.push("<input" + (jade.attrs(jade.merge([{"oninput": "view.getTransactions()"},attributes]), false)) + "/>");
};
buf.push("<h1>Przelewy</h1><form name=\"transactions\"><fieldset><legend>Data</legend><label>Miesiac</label><input type=\"radio\" name=\"has_month\" value=\"y\" checked=\"checked\" onchange=\"view.changeDateRange(this)\"/><label>Zakres</label><input type=\"radio\" name=\"has_month\" value=\"n\" onchange=\"view.changeDateRange(this)\"/><div id=\"transaction-month\">");
jade_mixins["text_query_input"].call({
attributes: {"type": "month","name": "month"}
});
buf.push("<br/></div><div id=\"transaction-range\" class=\"disabled\"><label>Od dnia</label>");
jade_mixins["text_query_input"].call({
block: function(){
buf.push(" ");
},
attributes: {"type": "date","name": "date_start","disabled": true}
});
buf.push("<br/><label>Do dnia</label>");
jade_mixins["text_query_input"].call({
attributes: {"type": "date","name": "date_end","disabled": true}
});
buf.push("</div></fieldset><fieldset><legend>Mniejszy od</legend>");
jade_mixins["text_query_input"].call({
attributes: {"type": "number","min": "0","step": "0.01","name": "cost_le"}
});
buf.push("</fieldset><fieldset><legend>Większy od</legend>");
jade_mixins["text_query_input"].call({
attributes: {"type": "number","min": "0","step": "0.01","name": "cost_ge"}
});
buf.push("</fieldset><fieldset><legend>Szukaj</legend>");
jade_mixins["text_query_input"].call({
attributes: {"type": "search","name": "text"}
});
buf.push("</fieldset><fieldset><legend>Opcje</legend>");
jade_mixins["query_input"].call({
attributes: {"type": "checkbox","name": "negative","value": "t"}
});
buf.push("<label>Ujemne?</label>");
jade_mixins["query_input"].call({
attributes: {"type": "checkbox","name": "positive","value": "t"}
});
buf.push("<label>Dodatnie?</label></fieldset></form><div id=\"modal_add_type\" class=\"modal disabled\"></div><table id=\"transactions\"></table>");;return buf.join("");
}