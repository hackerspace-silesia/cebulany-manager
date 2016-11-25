///<reference path="./templates.d.ts"/>
///<reference path="./utils.ts"/>
///<reference path="./request.ts"/>

function showMembers() {
    setHTML('main', renderMembers());
    view = new MemberView();
}


class MemberView {
    constructor() {
        this.getTablePaidMonths();
    }

    getTablePaidMonths() {
        var members = {};
        this.members = members;
        var paidmonths = {};
        setHTML('table-members', renderTableLoading());
        request({url: 'members'}).then((json) => {
            json.forEach((obj) => {
                members[obj.id] = obj;
            });
            return request({url: 'paid_month/table'});
        }).then((json) => {
            json.forEach((member) => {
                member.months.forEach((month) => {
                    var key = `${member.member_id}:${month.month}`;
                    paidmonths[key] = month.sum;
                })
            })
            var now = new Date();
            console.log(`${now.year}-${now.month + 1}`);
            setHTML('table-members', renderTableMembers({
                members: json.map((obj) => {
                    return members[obj.member_id];
                }),
                paid_months: paidmonths,
                dt_now: `${now.getFullYear()}-${now.getMonth() + 1}`,
                years: [2015, 2016, 2017],
                months: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'] // i know bro, arr.map() but is midnight
            }));
        })
    }

    showPaidMonths(id: number, dt: string) {
        var modal_paidmonth = byId('modal_paidmonth');
        modal_paidmonth.dataset.member_id = id;
        modal_paidmonth.dataset.dt = dt;
        modal_paidmonth.className = 'modal';
        this.getPaidMonths();
    }

    getPaidMonths() {
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
        }).then((json) => {
            setHTML('modal_paidmonth', renderModalPaidMonths({
                paid_months: json,
                member_name: member_name,
                dt: dt
            }));
        })
    }

    removePaidMonth(ev, id: number) {
        var yes = confirm(`Czy chcesz skasować tą płatność?`)
        var self = this;
        if (!yes) {
            return;
        }

        request({
            url: `paid_month/${id}`,
            method: 'DELETE',
        }).then((json) => {
            self.getPaidMonths();
            self.getTablePaidMonths();
        });
    }

    closeModal() {
        setHTML('modal_paidmonth', '');
        byId('modal_paidmonth').className = 'modal disabled';
    }
}
