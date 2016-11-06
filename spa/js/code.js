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
var BASE_URL = '/api/';
function request(options) {
    // nie chcesz frameworka w js? napisz go kurwa sam ._.
    // ten jezyk nie ma przyszlosci
    var url = BASE_URL + options.url;
    var method = options.method || 'get';
    var query_params = options.query_params;
    var query_form = options.query_form;
    var data_form = options.data_form;
    var data = options.data;
    if (query_form !== undefined) {
        query_data = new FormData(document.forms[query_form]);
        query_params = {};
        query_data.forEach(function (value, key) {
            query_params[key] = value;
        });
    }
    if (data_form !== undefined) {
        var form_data = new FormData(document.forms[data_form]);
        data = {};
        form_data.forEach(function (value, key) {
            data[key] = value;
        });
    }
    if (query_params !== undefined) {
        Object.keys(query_params).forEach(function (key, index) {
            var value = query_params[key];
            if (value === '' || value === undefined)
                return;
            var delimiter = index == 0 ? '?' : '&';
            url += "" + delimiter + escape(key) + "=" + escape(value);
        });
    }
    var headers = new Headers();
    if (method == 'POST' || method == 'PUT') {
        headers.set('Content-Type', 'application/json');
    }
    return fetch(url, {
        method: method,
        body: data && JSON.stringify(data),
        headers: headers
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
        this.transactions = null;
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
        var self = this;
        setHTML('transactions', renderTableLoading());
        request({ url: 'transactions', query_form: 'transactions' }).then(function (json) {
            self.transactions = json.transactions;
            setHTML('transactions', renderTableTransactions(json));
        });
    };
    TransactionView.prototype.addNewTypeTransaction = function (id) {
        var transaction = this.transactions[id];
        byId('modal_add_type').className = 'modal';
        setHTML('modal_add_type', renderModalAddNewTypeTransaction({
            transaction: this.transactions[id]
        }));
        this.changeModalForm();
    };
    TransactionView.prototype.changeModalForm = function () {
        var action = document.forms['select_type']['type'].value;
        action = 'add_type_' + action;
        var forms = document.querySelectorAll('#modal_add_type .form');
        forms.forEach(function (form) {
            if (form.attributes.name.value !== action) {
                form.className = 'disabled form';
            }
            else {
                form.className = 'form';
            }
        });
    };
    TransactionView.prototype.addType = function () {
        var self = this;
        var action = document.forms['select_type']['type'].value;
        request({
            url: action,
            method: 'POST',
            data_form: 'add_type_' + action
        }).then(function (json) {
            self.closeModal();
            self.getTransactions();
        });
    };
    TransactionView.prototype.closeModal = function () {
        setHTML('modal_add_type', '');
        byId('modal_add_type').className = 'modal disabled';
    };
    TransactionView.prototype.seekUsers = function (ev) {
        ev.className = '';
        document.forms['add_type_paid_month']['member_id'].value = '';
        request({
            url: 'members',
            query_params: { q: ev.value, limit: 5 }
        }).then(function (json) {
            setHTML('type_users', renderDataListUsers({
                users: json,
                func: 'view.setUserInModal(this)'
            }));
        });
    };
    TransactionView.prototype.setUserInModal = function (ev) {
        var form = document.forms['add_type_paid_month'];
        form['member_id'].value = ev.dataset.id;
        form['user_search'].value = ev.textContent;
        form['user_search'].className = 'good-input';
        setHTML('type_users', '');
    };
    return TransactionView;
}());
///<reference path="./transactions.ts"/>
var view = null;
showTransactions();
