function renderDataListUsers(locals) {
var buf = [];
var jade_mixins = {};
var jade_interp;
;var locals_for_with = (locals || {});(function (func, undefined, users) {
// iterate users
;(function(){
  var $$obj = users;
  if ('number' == typeof $$obj.length) {

    for (var $index = 0, $$l = $$obj.length; $index < $$l; $index++) {
      var user = $$obj[$index];

buf.push("<li" + (jade.attr("data-id", user.id, true, false)) + (jade.attr("onclick", func, true, false)) + ">" + (jade.escape(null == (jade_interp = user.name) ? "" : jade_interp)));
if ( !user.is_active)
{
buf.push("<span class=\"not-active\">(NIE AKTYWNY)</span>");
}
buf.push("</li>");
    }

  } else {
    var $$l = 0;
    for (var $index in $$obj) {
      $$l++;      var user = $$obj[$index];

buf.push("<li" + (jade.attr("data-id", user.id, true, false)) + (jade.attr("onclick", func, true, false)) + ">" + (jade.escape(null == (jade_interp = user.name) ? "" : jade_interp)));
if ( !user.is_active)
{
buf.push("<span class=\"not-active\">(NIE AKTYWNY)</span>");
}
buf.push("</li>");
    }

  }
}).call(this);
}.call(this,"func" in locals_for_with?locals_for_with.func:typeof func!=="undefined"?func:undefined,"undefined" in locals_for_with?locals_for_with.undefined:typeof undefined!=="undefined"?undefined:undefined,"users" in locals_for_with?locals_for_with.users:typeof users!=="undefined"?users:undefined));;return buf.join("");
}
function renderMembers(locals) {
var buf = [];
var jade_mixins = {};
var jade_interp;

buf.push("<h1>Członkowie</h1><h2>Płatności</h2><table id=\"table-members\"></table>");;return buf.join("");
}
function renderModalAddNewTypeTransaction(locals) {
var buf = [];
var jade_mixins = {};
var jade_interp;
;var locals_for_with = (locals || {});(function (transaction) {
jade_mixins["default_form"] = jade_interp = function(name){
var block = (this && this.block), attributes = (this && this.attributes) || {};
buf.push("<form" + (jade.attr("name", name, true, false)) + " class=\"disabled form\"><input type=\"hidden\" name=\"transaction_id\"" + (jade.attr("value", transaction.id, true, false)) + "/><fieldset><legend>Kwota</legend><input type=\"number\" name=\"cost\" min=\"0\"" + (jade.attr("value", transaction.cost, true, false)) + "/></fieldset><fieldset><legend>Nazwa</legend><input type=\"text\" name=\"name\"" + (jade.attr("value", transaction.proposed_type_name || transaction.title, true, false)) + "/></fieldset></form>");
};
buf.push("<div class=\"modal-content\"><table class=\"summary\"><tr><th>Data</th><td>" + (jade.escape(null == (jade_interp = transaction.date) ? "" : jade_interp)) + "</td></tr><tr><th>Nazwa</th><td>" + (jade.escape(null == (jade_interp = transaction.name) ? "" : jade_interp)) + "</td></tr><tr><th>Tytuł</th><td>" + (jade.escape(null == (jade_interp = transaction.title) ? "" : jade_interp)) + "</td></tr><tr><th>IBAN</th><td>" + (jade.escape(null == (jade_interp = transaction.iban) ? "" : jade_interp)) + "</td></tr></table><form name=\"select_type\"><legend>Typ przelewu:</legend><input type=\"radio\" name=\"type\" value=\"paid_month\" checked=\"checked\" onchange=\"view.changeModalForm()\"/><label>Składka</label><input type=\"radio\" name=\"type\" value=\"bill\" onchange=\"view.changeModalForm()\"/><label>Rachunek</label><input type=\"radio\" name=\"type\" value=\"donation\" onchange=\"view.changeModalForm()\"/><label>Darowizna</label><input type=\"radio\" name=\"type\" value=\"other\" onchange=\"view.changeModalForm()\"/><label>Inne</label></form><form name=\"add_type_paid_month\" class=\"form\"><input type=\"hidden\" name=\"transaction_id\"" + (jade.attr("value", transaction.id, true, false)) + "/><input type=\"hidden\" name=\"member_id\"" + (jade.attr("value", transaction.proposed_member_id || '', true, false)) + "/><fieldset><legend>Członek</legend><input type=\"search\" name=\"user_search\"" + (jade.attr("value", transaction.proposed_member ? transaction.proposed_member.name : '', true, false)) + " oninput=\"view.seekUsers(this)\"" + (jade.cls([transaction.proposed_member_id ? 'good-input' : ''], [true])) + "/><ul id=\"type_users\" class=\"data-list\"></ul></fieldset><fieldset><legend>Miesiąc</legend><input type=\"month\" name=\"date\"" + (jade.attr("value", transaction.date.slice(0, 7), true, false)) + "/></fieldset><fieldset><legend>Kwota</legend><input type=\"number\" name=\"cost\" min=\"0\"" + (jade.attr("value", transaction.cost, true, false)) + "/></fieldset></form>");
jade_mixins["default_form"]('add_type_bill');
jade_mixins["default_form"]('add_type_donation');
jade_mixins["default_form"]('add_type_other');
buf.push("<button type=\"button\" onclick=\"view.addType()\">Dodaj</button><button type=\"button\" onclick=\"view.closeModal()\">Zamknij</button></div>");}.call(this,"transaction" in locals_for_with?locals_for_with.transaction:typeof transaction!=="undefined"?transaction:undefined));;return buf.join("");
}
function renderTableLoading(locals) {
var buf = [];
var jade_mixins = {};
var jade_interp;

buf.push("<tr><td class=\"loading\"><img src=\"img/firemark.png\"/><br/><strong>Loading…</strong></td></tr>");;return buf.join("");
}
function renderTableMembers(locals) {
var buf = [];
var jade_mixins = {};
var jade_interp;
;var locals_for_with = (locals || {});(function (Number, dt_now, members, months, paid_months, undefined, years) {
jade_mixins["paid_cell"] = jade_interp = function(member, year, month){
var block = (this && this.block), attributes = (this && this.attributes) || {};
var dt = year + '-' + month
var key = member.id + ':' + dt
var value = paid_months[key]
if ( value === undefined)
{
var not_payed = member.join_date < dt && dt <= dt_now
buf.push("<td" + (jade.cls([not_payed? 'warn' : ''], [true])) + ">" + (jade.escape(null == (jade_interp = '-') ? "" : jade_interp)) + "</td>");
}
else
{
buf.push("<td>" + (jade.escape(null == (jade_interp = Number(value).toFixed()) ? "" : jade_interp)) + "</td>");
}
};
buf.push("<thead><tr><th rowspan=\"2\">Nazwa</th>");
// iterate years
;(function(){
  var $$obj = years;
  if ('number' == typeof $$obj.length) {

    for (var $index = 0, $$l = $$obj.length; $index < $$l; $index++) {
      var year = $$obj[$index];

buf.push("<th colspan=\"12\">" + (jade.escape(null == (jade_interp = year) ? "" : jade_interp)) + "</th>");
    }

  } else {
    var $$l = 0;
    for (var $index in $$obj) {
      $$l++;      var year = $$obj[$index];

buf.push("<th colspan=\"12\">" + (jade.escape(null == (jade_interp = year) ? "" : jade_interp)) + "</th>");
    }

  }
}).call(this);

buf.push("</tr><tr>");
// iterate years
;(function(){
  var $$obj = years;
  if ('number' == typeof $$obj.length) {

    for (var $index = 0, $$l = $$obj.length; $index < $$l; $index++) {
      var year = $$obj[$index];

// iterate months
;(function(){
  var $$obj = months;
  if ('number' == typeof $$obj.length) {

    for (var $index = 0, $$l = $$obj.length; $index < $$l; $index++) {
      var month = $$obj[$index];

buf.push("<th>" + (jade.escape(null == (jade_interp = month) ? "" : jade_interp)) + "</th>");
    }

  } else {
    var $$l = 0;
    for (var $index in $$obj) {
      $$l++;      var month = $$obj[$index];

buf.push("<th>" + (jade.escape(null == (jade_interp = month) ? "" : jade_interp)) + "</th>");
    }

  }
}).call(this);

    }

  } else {
    var $$l = 0;
    for (var $index in $$obj) {
      $$l++;      var year = $$obj[$index];

// iterate months
;(function(){
  var $$obj = months;
  if ('number' == typeof $$obj.length) {

    for (var $index = 0, $$l = $$obj.length; $index < $$l; $index++) {
      var month = $$obj[$index];

buf.push("<th>" + (jade.escape(null == (jade_interp = month) ? "" : jade_interp)) + "</th>");
    }

  } else {
    var $$l = 0;
    for (var $index in $$obj) {
      $$l++;      var month = $$obj[$index];

buf.push("<th>" + (jade.escape(null == (jade_interp = month) ? "" : jade_interp)) + "</th>");
    }

  }
}).call(this);

    }

  }
}).call(this);

buf.push("</tr></thead><tbody>");
// iterate members
;(function(){
  var $$obj = members;
  if ('number' == typeof $$obj.length) {

    for (var $index = 0, $$l = $$obj.length; $index < $$l; $index++) {
      var member = $$obj[$index];

buf.push("<tr><th" + (jade.cls([!member.is_active ? 'not-active' : ''], [true])) + ">" + (jade.escape(null == (jade_interp = member.name) ? "" : jade_interp)) + "</th>");
// iterate years
;(function(){
  var $$obj = years;
  if ('number' == typeof $$obj.length) {

    for (var $index = 0, $$l = $$obj.length; $index < $$l; $index++) {
      var year = $$obj[$index];

// iterate months
;(function(){
  var $$obj = months;
  if ('number' == typeof $$obj.length) {

    for (var $index = 0, $$l = $$obj.length; $index < $$l; $index++) {
      var month = $$obj[$index];

jade_mixins["paid_cell"](member, year, month);
    }

  } else {
    var $$l = 0;
    for (var $index in $$obj) {
      $$l++;      var month = $$obj[$index];

jade_mixins["paid_cell"](member, year, month);
    }

  }
}).call(this);

    }

  } else {
    var $$l = 0;
    for (var $index in $$obj) {
      $$l++;      var year = $$obj[$index];

// iterate months
;(function(){
  var $$obj = months;
  if ('number' == typeof $$obj.length) {

    for (var $index = 0, $$l = $$obj.length; $index < $$l; $index++) {
      var month = $$obj[$index];

jade_mixins["paid_cell"](member, year, month);
    }

  } else {
    var $$l = 0;
    for (var $index in $$obj) {
      $$l++;      var month = $$obj[$index];

jade_mixins["paid_cell"](member, year, month);
    }

  }
}).call(this);

    }

  }
}).call(this);

buf.push("</tr>");
    }

  } else {
    var $$l = 0;
    for (var $index in $$obj) {
      $$l++;      var member = $$obj[$index];

buf.push("<tr><th" + (jade.cls([!member.is_active ? 'not-active' : ''], [true])) + ">" + (jade.escape(null == (jade_interp = member.name) ? "" : jade_interp)) + "</th>");
// iterate years
;(function(){
  var $$obj = years;
  if ('number' == typeof $$obj.length) {

    for (var $index = 0, $$l = $$obj.length; $index < $$l; $index++) {
      var year = $$obj[$index];

// iterate months
;(function(){
  var $$obj = months;
  if ('number' == typeof $$obj.length) {

    for (var $index = 0, $$l = $$obj.length; $index < $$l; $index++) {
      var month = $$obj[$index];

jade_mixins["paid_cell"](member, year, month);
    }

  } else {
    var $$l = 0;
    for (var $index in $$obj) {
      $$l++;      var month = $$obj[$index];

jade_mixins["paid_cell"](member, year, month);
    }

  }
}).call(this);

    }

  } else {
    var $$l = 0;
    for (var $index in $$obj) {
      $$l++;      var year = $$obj[$index];

// iterate months
;(function(){
  var $$obj = months;
  if ('number' == typeof $$obj.length) {

    for (var $index = 0, $$l = $$obj.length; $index < $$l; $index++) {
      var month = $$obj[$index];

jade_mixins["paid_cell"](member, year, month);
    }

  } else {
    var $$l = 0;
    for (var $index in $$obj) {
      $$l++;      var month = $$obj[$index];

jade_mixins["paid_cell"](member, year, month);
    }

  }
}).call(this);

    }

  }
}).call(this);

buf.push("</tr>");
    }

  }
}).call(this);

buf.push("</tbody>");}.call(this,"Number" in locals_for_with?locals_for_with.Number:typeof Number!=="undefined"?Number:undefined,"dt_now" in locals_for_with?locals_for_with.dt_now:typeof dt_now!=="undefined"?dt_now:undefined,"members" in locals_for_with?locals_for_with.members:typeof members!=="undefined"?members:undefined,"months" in locals_for_with?locals_for_with.months:typeof months!=="undefined"?months:undefined,"paid_months" in locals_for_with?locals_for_with.paid_months:typeof paid_months!=="undefined"?paid_months:undefined,"undefined" in locals_for_with?locals_for_with.undefined:typeof undefined!=="undefined"?undefined:undefined,"years" in locals_for_with?locals_for_with.years:typeof years!=="undefined"?years:undefined));;return buf.join("");
}
function renderTableTransactions(locals) {
var buf = [];
var jade_mixins = {};
var jade_interp;
;var locals_for_with = (locals || {});(function (maxChars, sum, transactions, undefined) {
jade_mixins["transaction_row"] = jade_interp = function(num, row){
var block = (this && this.block), attributes = (this && this.attributes) || {};
buf.push("<tr><th>" + (jade.escape(null == (jade_interp = row.date) ? "" : jade_interp)) + "</th><td" + (jade.attr("title", row.name, true, false)) + ">" + (jade.escape(null == (jade_interp = maxChars(row.name, 60)) ? "" : jade_interp)) + "</td><td" + (jade.attr("title", row.title, true, false)) + ">" + (jade.escape(null == (jade_interp = maxChars(row.title, 60)) ? "" : jade_interp)) + "</td><td" + (jade.cls(['price',row.cost < 0 ? 'negative' : 'positive'], [null,true])) + ">" + (jade.escape(null == (jade_interp = row.cost + " zł") ? "" : jade_interp)) + "</td><!--td(title=row.iban)= maxChars(row.iban && row.iban.replace(/ /g, ''), 5)--><td>");
// iterate row.donations
;(function(){
  var $$obj = row.donations;
  if ('number' == typeof $$obj.length) {

    for (var $index = 0, $$l = $$obj.length; $index < $$l; $index++) {
      var donat = $$obj[$index];

buf.push("<span" + (jade.attr("title", '' + (donat.name) + '\n' + (donat.cost) + ' zł', true, false)) + " class=\"badge type_donation\">D</span>");
    }

  } else {
    var $$l = 0;
    for (var $index in $$obj) {
      $$l++;      var donat = $$obj[$index];

buf.push("<span" + (jade.attr("title", '' + (donat.name) + '\n' + (donat.cost) + ' zł', true, false)) + " class=\"badge type_donation\">D</span>");
    }

  }
}).call(this);

// iterate row.bills
;(function(){
  var $$obj = row.bills;
  if ('number' == typeof $$obj.length) {

    for (var $index = 0, $$l = $$obj.length; $index < $$l; $index++) {
      var bill = $$obj[$index];

buf.push("<span" + (jade.attr("title", '' + (bill.name) + '\n' + (bill.cost) + ' zł', true, false)) + " class=\"badge type_bill\">R</span>");
    }

  } else {
    var $$l = 0;
    for (var $index in $$obj) {
      $$l++;      var bill = $$obj[$index];

buf.push("<span" + (jade.attr("title", '' + (bill.name) + '\n' + (bill.cost) + ' zł', true, false)) + " class=\"badge type_bill\">R</span>");
    }

  }
}).call(this);

// iterate row.paidmonths
;(function(){
  var $$obj = row.paidmonths;
  if ('number' == typeof $$obj.length) {

    for (var $index = 0, $$l = $$obj.length; $index < $$l; $index++) {
      var paid = $$obj[$index];

buf.push("<span" + (jade.attr("title", '' + (paid.name) + '\n' + (paid.cost) + ' zł', true, false)) + " class=\"badge type_paid_month\">S</span>");
    }

  } else {
    var $$l = 0;
    for (var $index in $$obj) {
      $$l++;      var paid = $$obj[$index];

buf.push("<span" + (jade.attr("title", '' + (paid.name) + '\n' + (paid.cost) + ' zł', true, false)) + " class=\"badge type_paid_month\">S</span>");
    }

  }
}).call(this);

// iterate row.others
;(function(){
  var $$obj = row.others;
  if ('number' == typeof $$obj.length) {

    for (var $index = 0, $$l = $$obj.length; $index < $$l; $index++) {
      var other = $$obj[$index];

buf.push("<span" + (jade.attr("title", '' + (other.name) + '\n' + (other.cost) + ' zł', true, false)) + " class=\"badge type_other\">O</span>");
    }

  } else {
    var $$l = 0;
    for (var $index in $$obj) {
      $$l++;      var other = $$obj[$index];

buf.push("<span" + (jade.attr("title", '' + (other.name) + '\n' + (other.cost) + ' zł', true, false)) + " class=\"badge type_other\">O</span>");
    }

  }
}).call(this);

buf.push("<a" + (jade.attr("onclick", 'view.addNewTypeTransaction(' + (num) + ')', true, false)) + " class=\"right btn\">+</a></td></tr>");
};
jade_mixins["foot_row"] = jade_interp = function(title, value){
var block = (this && this.block), attributes = (this && this.attributes) || {};
buf.push("<tr><th>" + (jade.escape(null == (jade_interp = title) ? "" : jade_interp)) + "</th><th colspan=\"2\"></th><th class=\"price\"><strong>" + (jade.escape(null == (jade_interp = value) ? "" : jade_interp)) + "</strong></th><th></th></tr>");
};
buf.push("<thead><tr><th width=\"7%\">Data</th><th width=\"38%\">Nazwa</th><th width=\"40%\">Tytuł</th><th width=\"6%\">Kwota</th><th width=\"5%\">Typy </th></tr></thead><tbody>");
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
buf.push("<label>Dodatnie?</label></fieldset></form><div class=\"legend\"><strong>Legenda: &nbsp;</strong><span class=\"badge type_donation\">D</span><span>&nbsp; Darowizna &nbsp;</span><span class=\"badge type_bill\">R</span><span>&nbsp; Rachunek &nbsp;</span><span class=\"badge type_paid_month\">S</span><span>&nbsp; Składka &nbsp;</span><span class=\"badge type_other\">O</span><span>&nbsp; Inne &nbsp;</span></div><div id=\"modal_add_type\" class=\"modal disabled\"></div><table id=\"transactions\"></table>");;return buf.join("");
}