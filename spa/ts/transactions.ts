///<reference path="./templates.d.ts"/>
///<reference path="./utils.ts"/>
///<reference path="./request.ts"/>

function showTransactions() {
    setHTML('main', renderTransactions());
    view = new TransactionView();
}


class TransactionView {
    form: HTMLFormElement;
    transactions: Map | null=null;
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
        var self = this;
        setHTML('transactions', renderTableLoading());
        request(
            {url: 'transactions', query_form: 'transactions'}
        ).then((json) => {
            self.transactions = json.transactions;
            setHTML('transactions', renderTableTransactions(json));
        });
    }

    addNewTypeTransaction(id: number) {
        var transaction = this.transactions[id];
        byId('modal_add_type').className = 'modal';
        setHTML('modal_add_type', renderModalAddNewTypeTransaction({
            transaction: this.transactions[id];
        ));
}
}
