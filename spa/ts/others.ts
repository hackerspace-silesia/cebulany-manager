///<reference path="./default_table.ts"/>

function showOthers() {
    setHTML('main', renderOthers());
    view = new OthersView();
}


class OthersView extends DefaultTableView {

    constructor() {
        this.endpoint = 'other';
        this.showRecords();
    }

}
