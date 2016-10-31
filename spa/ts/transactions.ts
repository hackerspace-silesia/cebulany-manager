///<reference path="./templates.d.ts"/>
///<reference path="./utils.ts"/>
///<reference path="./request.ts"/>

function showTransactions() {
    setHTML('main', renderTransactions());
    var form = document.forms['transactions'];
    form.month.value = getActualMonth();
    for(var el of ['month', 'date_start', 'date_end', 'text', 'cost_le', 'cost_ge']) {
        form[el].oninput = getTransactions;
    }
    for(var el of ['negative', 'positive']) {
        form[el].onchange = getTransactions;
    }
    for(var el of form.has_month) {
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
    } else {
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
    request(
        {url: 'transactions', query_form: 'transactions'}
    ).then((json) => {
        setHTML('transactions', renderTableTransactions(json));
    });
}
