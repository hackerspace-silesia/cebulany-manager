var BASE_URL = '/api/';

function request(options: any): any {
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
        query_data.forEach((value, key) => {
            query_params[key] = value;
        })
    }
    if (data_form !== undefined) {
        var form_data = new FormData(document.forms[data_form]);
        data = {};
        form_data.forEach((value, key) => {
            data[key] = value;
        })
    }
    if (query_params !== undefined) {
        Object.keys(query_params).forEach((key, index) => {
            var value = query_params[key];
            if (value === '' || value === undefined) return;
            var delimiter = index == 0 ? '?' : '&'
            url += `${delimiter}${escape(key)}=${escape(value)}`;
        });
    }
    var headers = new Headers();
    if (method == 'POST' || method == 'PUT') {
        headers.set('Content-Type', 'application/json');
    }
    return fetch(
        url, {
            method: method,
            body: data && JSON.stringify(data),
            headers: headers
        }
    ).then((response) => {return response.json();});
}
