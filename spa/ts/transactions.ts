///<reference path="./templates.d.ts"/>
///<reference path="./utils.ts"/>
///<reference path="./request.ts"/>

function showTransactions() {
    setHTML('main', renderTransactions());
    view = new TransactionView();
}

class TransactionView {
    form: HTMLFormElement;
    constructor() {
        this.form = document.forms['transactions'];
        this.setupSearchForm();
        this.getTransactions();
    }

    setupSearchForm() {
        this.form['month'].value = getActualMonth();
    }

    changeDateRange(ev) {
        var form = this.form;
        if (ev.value == 'y') {
            form['date_end'].disabled = true;
            form['date_start'].disabled = true;
            form['month'].disabled = false;
            byId('transaction-month').className = '';
            byId('transaction-range').className = 'disabled';
        } else {
            form['date_end'].disabled = false;
            form['date_start'].disabled = false;
            form['month'].disabled = true;
            byId('transaction-range').className = '';
            byId('transaction-month').className = 'disabled';
        }
        this.getTransactions();
    }

    getTransactions() {
        setHTML('transactions', renderTableLoading());
        request(
            {url: 'transactions', query_form: 'transactions'}
        ).then((json) => {
            setHTML('transactions', renderTableTransactions(json));
        });
    }
}
