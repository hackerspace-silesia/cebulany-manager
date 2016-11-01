var BASE_URL:URL = new URL('http://localhost:5000/api/');

function request(options: any): any {
    // nie chcesz frameworka w js? napisz go kurwa sam ._.
    // ten jezyk nie ma przyszlosci
    var url = new URL(options.url, BASE_URL);
    var method = options.method || 'get';
    var query_params = options.query_params;
    var query_form = options.query_form;
    var data_form = options.data_form;
    var data = options.data;
    if (query_form !== undefined) {
        query_params = new FormData(document.forms[query_form]);
    }
    if (data_form !== undefined) {
        var form_data = new FormData(document.forms[data_form]);
        data = {};
        form_data.forEach((value, key) => {
            data[key] = value;
        })
    }
    if (query_params !== undefined) {
        query_params.forEach((value, key) => {
            if (value !== '' && value !== undefined) {
                url.searchParams.append(key, value);
            }
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
