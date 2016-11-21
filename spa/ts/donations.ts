///<reference path="./default_table.ts"/>

function showDonations() {
    setHTML('main', renderDonations());
    view = new DonationView();
}


class DonationView extends DefaultTableView {

    constructor() {
        this.endpoint = 'donation';
        this.showRecords();
    }

}
