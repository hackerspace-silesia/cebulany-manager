function setHTML(id, html) {
    document.getElementById(id).innerHTML = html;
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
    var form = document.forms['transactions'];
    form.month.value = getActualMonth();
    for (var _i = 0, _a = ['month', 'date_start', 'date_end', 'text', 'cost_le', 'cost_ge']; _i < _a.length; _i++) {
        var el = _a[_i];
        form[el].oninput = getTransactions;
    }
    for (var _b = 0, _c = ['negative', 'positive']; _b < _c.length; _b++) {
        var el = _c[_b];
        form[el].onchange = getTransactions;
    }
    for (var _d = 0, _e = form.has_month; _d < _e.length; _d++) {
        var el = _e[_d];
        el.onchange = changeDateRange;
    }
    getTransactions();
}
function changeDateRange() {
    var form = document.forms['transactions'];
    console.log(this.value);
    if (this.value == 'y') {
        form.date_end.disabled = true;
        form.date_start.disabled = true;
        form.month.disabled = false;
        document.getElementById('transaction-month').className = '';
        document.getElementById('transaction-range').className = 'disabled';
    }
    else {
        form.date_end.disabled = false;
        form.date_start.disabled = false;
        form.month.disabled = true;
        document.getElementById('transaction-month').className = 'disabled';
        document.getElementById('transaction-range').className = '';
    }
    getTransactions();
}
function getTransactions() {
    setHTML('transactions', renderTableLoading());
    request({ url: 'transactions', query_form: 'transactions' }).then(function (json) {
        setHTML('transactions', renderTableTransactions(json));
    });
}
///<reference path="./transactions.ts"/>
showTransactions();
