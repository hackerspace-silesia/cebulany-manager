///<reference path="./templates.d.ts"/>
///<reference path="./utils.ts"/>
///<reference path="./request.ts"/>

class DefaultTableView {
    endpoint:string;

    showRecords() {
        setHTML('table', renderTableLoading());
        request({url: this.endpoint}).then((json) => {
            setHTML('table', renderDefaultTable({
                data: json,
            }));
        })
    } 

    deleteRecord(ev, id) {
        var yes = confirm(`Czy napewno chcesz skasować?`);
        var self = this;
        if (!yes) {
            return;
        }

        request({
            url: `${this.endpoint}/${id}`,
            method: 'DELETE',
        }).then((json) => {
            self.showRecords();
        });

    }
}
