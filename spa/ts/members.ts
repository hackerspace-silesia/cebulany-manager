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
        var paidmonths = {};
        setHTML('table-members', renderTableLoading());
        request({url: 'members'}).then((json) => {
            json.forEach((obj) => {
                members[obj.id] = obj;
            });
            return request({url: 'paid_month'});
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

}
