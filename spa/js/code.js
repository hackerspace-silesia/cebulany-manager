function byId(id) {
    return document.getElementById(id);
}
function setHTML(id, html) {
    byId(id).innerHTML = html;
}
function maxChars(str, charsLen) {
    str = str || '';
    if (str.length > charsLen) {
        return str.slice(0, charsLen - 1) + '…';
    }
    return str;
}
function getActualMonth() {
    var today = new Date();
    return today.getFullYear() + '-' + (today.getMonth() + 1);
}
var BASE_URL = new URL('http://localhost:5000/api/');
function request(options) {
    // nie chcesz frameworka w js? napisz go kurwa sam ._.
    // ten jezyk nie ma przyszlosci
    var url = new URL(options.url, BASE_URL);
    var method = options.method || 'get';
    var query_params;
    var query_form = options.query_form;
    if (query_form !== undefined) {
        query_params = new FormData(document.forms[query_form]);
    }
    query_params.forEach(function (value, key) {
        if (value !== '' && value !== undefined) {
            url.searchParams.append(key, value);
        }
    });
    return fetch(url, {
        method: method
    }).then(function (response) { return response.json(); });
}
///<reference path="./templates.d.ts"/>
///<reference path="./utils.ts"/>
///<reference path="./request.ts"/>
function showTransactions() {
    setHTML('main', renderTransactions());
    view = new TransactionView();
}
var TransactionView = (function () {
    function TransactionView() {
        this.form = document.forms['transactions'];
        this.setupSearchForm();
        this.getTransactions();
    }
    TransactionView.prototype.setupSearchForm = function () {
        this.form['month'].value = getActualMonth();
    };
    TransactionView.prototype.changeDateRange = function (ev) {
        var form = this.form;
        if (ev.value == 'y') {
            form['date_end'].disabled = true;
            form['date_start'].disabled = true;
            form['month'].disabled = false;
            byId('transaction-month').className = '';
            byId('transaction-range').className = 'disabled';
        }
        else {
            form['date_end'].disabled = false;
            form['date_start'].disabled = false;
            form['month'].disabled = true;
            byId('transaction-range').className = '';
            byId('transaction-month').className = 'disabled';
        }
        this.getTransactions();
    };
    TransactionView.prototype.getTransactions = function () {
        setHTML('transactions', renderTableLoading());
        request({ url: 'transactions', query_form: 'transactions' }).then(function (json) {
            setHTML('transactions', renderTableTransactions(json));
        });
    };
    return TransactionView;
}());
///<reference path="./transactions.ts"/>
var view = null;
showTransactions();
