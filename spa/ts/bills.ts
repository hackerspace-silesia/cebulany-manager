///<reference path="./default_table.ts"/>

function showBills() {
    setHTML('main', renderBills());
    view = new BillView();
}


class BillView extends DefaultTableView {

    constructor() {
        this.endpoint = 'bill';
        this.showRecords();
    }

}
