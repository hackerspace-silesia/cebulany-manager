var BASE_URL:URL = new URL('http://localhost:5000/api/');

function request(options: any): any {
    // nie chcesz frameworka w js? napisz go kurwa sam ._.
    // ten jezyk nie ma przyszlosci
    var url = new URL(options.url, BASE_URL);
    var method = options.method || 'get';
    var query_params;
    var query_form = options.query_form
    if (query_form !== undefined) {
        query_params = new FormData(document.forms[query_form]);
    }
    query_params.forEach((value, key) => {
        if (value !== '' && value !== undefined) {
            url.searchParams.append(key, value);
        }
    });
    return fetch(
        url, {
            method: method,
        }
    ).then((response) => {return response.json();});
}
