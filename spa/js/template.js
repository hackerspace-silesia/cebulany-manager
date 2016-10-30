function renderTransactions(locals) {
var buf = [];
var jade_mixins = {};
var jade_interp;
;var locals_for_with = (locals || {});(function (maxChars, sum, transactions, undefined) {
jade_mixins["transaction_row"] = jade_interp = function(row){
var block = (this && this.block), attributes = (this && this.attributes) || {};
buf.push("<tr><td>" + (jade.escape(null == (jade_interp = row.date) ? "" : jade_interp)) + "</td><td" + (jade.attr("title", row.name, true, false)) + ">" + (jade.escape(null == (jade_interp = maxChars(row.name, 60)) ? "" : jade_interp)) + "</td><td" + (jade.attr("title", row.title, true, false)) + ">" + (jade.escape(null == (jade_interp = maxChars(row.title, 60)) ? "" : jade_interp)) + "</td><td" + (jade.cls(['price',row.cost < 0 ? 'negative' : 'positive'], [null,true])) + ">" + (jade.escape(null == (jade_interp = row.cost + " zł") ? "" : jade_interp)) + "</td><td" + (jade.attr("title", row.iban, true, false)) + ">" + (jade.escape(null == (jade_interp = maxChars(row.iban.replace(/ /g, ''), 5)) ? "" : jade_interp)) + "</td></tr>");
};
buf.push("<h1>Przelewy</h1><table><thead><tr><th>Data</th><th>Nazwa</th><th>Tytuł</th><th>Kwota</th><th>IBAN</th></tr></thead><tbody>");
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

buf.push("</tbody><tfoot><tr><th>SUMA</th><th colspan=\"2\"></th><th class=\"price\"><strong>" + (jade.escape(null == (jade_interp = sum + " zł") ? "" : jade_interp)) + "</strong></th><th></th></tr></tfoot></table>");}.call(this,"maxChars" in locals_for_with?locals_for_with.maxChars:typeof maxChars!=="undefined"?maxChars:undefined,"sum" in locals_for_with?locals_for_with.sum:typeof sum!=="undefined"?sum:undefined,"transactions" in locals_for_with?locals_for_with.transactions:typeof transactions!=="undefined"?transactions:undefined,"undefined" in locals_for_with?locals_for_with.undefined:typeof undefined!=="undefined"?undefined:undefined));;return buf.join("");
}