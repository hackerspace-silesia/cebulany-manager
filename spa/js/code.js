var __extends = (this && this.__extends) || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
};
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
    var hash = window.btoa(auth.user + ':' + auth.password);
    headers.set('Authorization', 'Basic ' + hash);
    return fetch(url, {
        method: method,
        body: data && JSON.stringify(data),
        headers: headers
    }).then(function (response) {
        switch (response.status) {
            case 200:
            case 201:
                return response.json();
                break;
            case 204:
                return null;
                break;
            default: throw 'Unknown error';
        }
    });
}
///<reference path="./templates.d.ts"/>
///<reference path="./utils.ts"/>
///<reference path="./request.ts"/>
var DefaultTableView = (function () {
    function DefaultTableView() {
    }
    DefaultTableView.prototype.showRecords = function () {
        setHTML('table', renderTableLoading());
        request({ url: this.endpoint }).then(function (json) {
            setHTML('table', renderDefaultTable({
                data: json
            }));
        });
    };
    DefaultTableView.prototype.deleteRecord = function (ev, id) {
        var yes = confirm("Czy napewno chcesz skasowa\u0107?");
        var self = this;
        if (!yes) {
            return;
        }
        request({
            url: this.endpoint + "/" + id,
            method: 'DELETE'
        }).then(function (json) {
            self.showRecords();
        });
    };
    return DefaultTableView;
}());
///<reference path="./default_table.ts"/>
function showBills() {
    setHTML('main', renderBills());
    view = new BillView();
}
var BillView = (function (_super) {
    __extends(BillView, _super);
    function BillView() {
        this.endpoint = 'bill';
        this.showRecords();
    }
    return BillView;
}(DefaultTableView));
///<reference path="./default_table.ts"/>
function showDonations() {
    setHTML('main', renderDonations());
    view = new DonationView();
}
var DonationView = (function (_super) {
    __extends(DonationView, _super);
    function DonationView() {
        this.endpoint = 'donation';
        this.showRecords();
    }
    return DonationView;
}(DefaultTableView));
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
            var total_left = 0;
            self.transactions = json.transactions;
            self.transactions.forEach(function (tran) {
                tran.left = new Number(tran.cost);
                var sub_total = function (obj) { tran.left -= new Number(obj.cost); };
                var types = [tran.donations, tran.paidmonths, tran.bills, tran.others];
                types.forEach(function (tran_type) { tran_type.forEach(sub_total); });
                total_left += tran.left;
            });
            json.total_left = total_left;
            setHTML('transactions', renderTableTransactions(json));
        });
    };
    TransactionView.prototype.addNewTypeTransaction = function (id) {
        var transaction = this.transactions[id];
        byId('modal_add_type').className = 'modal';
        setHTML('modal_add_type', renderModalAddNewTypeTransaction({
            transaction: this.transactions[id]
        }));
        this.changeModalForm(transaction.proposed_type);
    };
    TransactionView.prototype.changeModalForm = function (default_action) {
        action = default_action || document.forms['select_type']['type'].value;
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
        if (default_action) {
            document.forms['select_type']['type'].value = default_action;
        }
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
    TransactionView.prototype.removeType = function (ev, str_type, id) {
        var title = ev.title.replace('/\\n/g', ' ');
        var yes = confirm("Czy chcesz skasowa\u0107 typ \"" + str_type + "\" o tytule \"" + ev.title + "\"?");
        var self = this;
        if (!yes) {
            return;
        }
        request({
            url: str_type + "/" + id,
            method: 'DELETE'
        }).then(function (json) {
            self.getTransactions();
        });
    };
    return TransactionView;
}());
///<reference path="./templates.d.ts"/>
///<reference path="./utils.ts"/>
///<reference path="./request.ts"/>
function showMembers() {
    setHTML('main', renderMembers());
    view = new MemberView();
}
var MemberView = (function () {
    function MemberView() {
        this.getTablePaidMonths();
    }
    MemberView.prototype.getTablePaidMonths = function () {
        var members = {};
        this.members = members;
        var paidmonths = {};
        setHTML('table-members', renderTableLoading());
        request({ url: 'members' }).then(function (json) {
            json.forEach(function (obj) {
                members[obj.id] = obj;
            });
            return request({ url: 'paid_month/table' });
        }).then(function (json) {
            json.forEach(function (member) {
                member.months.forEach(function (month) {
                    var key = member.member_id + ":" + month.month;
                    paidmonths[key] = month.sum;
                });
            });
            var now = new Date();
            console.log(now.year + "-" + (now.month + 1));
            setHTML('table-members', renderTableMembers({
                members: json.map(function (obj) {
                    return members[obj.member_id];
                }),
                paid_months: paidmonths,
                dt_now: now.getFullYear() + "-" + (now.getMonth() + 1),
                years: [2015, 2016, 2017],
                months: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'] // i know bro, arr.map() but is midnight
            }));
        });
    };
    MemberView.prototype.showPaidMonths = function (id, dt) {
        var modal_paidmonth = byId('modal_paidmonth');
        modal_paidmonth.dataset.member_id = id;
        modal_paidmonth.dataset.dt = dt;
        modal_paidmonth.className = 'modal';
        this.getPaidMonths();
    };
    MemberView.prototype.getPaidMonths = function () {
        var modal_paidmonth = byId('modal_paidmonth');
        var member_id = modal_paidmonth.dataset.member_id;
        var dt = modal_paidmonth.dataset.dt;
        var member_name = this.members[member_id].name;
        request({
            url: 'paid_month',
            query_params: {
                member_id: member_id,
                month: dt
            }
        }).then(function (json) {
            setHTML('modal_paidmonth', renderModalPaidMonths({
                paid_months: json,
                member_name: member_name,
                dt: dt
            }));
        });
    };
    MemberView.prototype.removePaidMonth = function (ev, id) {
        var yes = confirm("Czy chcesz skasowa\u0107 t\u0105 p\u0142atno\u015B\u0107?");
        var self = this;
        if (!yes) {
            return;
        }
        request({
            url: "paid_month/" + id,
            method: 'DELETE'
        }).then(function (json) {
            self.getPaidMonths();
            self.getTablePaidMonths();
        });
    };
    MemberView.prototype.closeModal = function () {
        setHTML('modal_paidmonth', '');
        byId('modal_paidmonth').className = 'modal disabled';
    };
    return MemberView;
}());
///<reference path="./default_table.ts"/>
function showOthers() {
    setHTML('main', renderOthers());
    view = new OthersView();
}
var OthersView = (function (_super) {
    __extends(OthersView, _super);
    function OthersView() {
        this.endpoint = 'other';
        this.showRecords();
    }
    return OthersView;
}(DefaultTableView));
///<reference path="./transactions.ts"/>
///<reference path="./members.ts"/>
///<reference path="./bills.ts"/>
///<reference path="./donations.ts"/>
///<reference path="./others.ts"/>
function showLogin() {
    setHTML('main', renderLogin());
    view = new LoginView();
    menu = document.getElementById('menu');
    menu.style.display = 'none';
}
var LoginView = (function () {
    function LoginView() {
        this.form = document.forms['login'];
        this.form.onsubmit = doLogin;
    }
    return LoginView;
}());
function doLogin() {
    form = document.forms['login'];
    auth.password = form.elements['password'].value;
    auth.user = form.elements['user'].value;
    console.log(auth);
    menu = document.getElementById('menu');
    menu.style.display = 'block';
    showTransactions();
    return false;
}
///<reference path="./login.ts"/>
var view = null;
var auth = {};
showLogin();
