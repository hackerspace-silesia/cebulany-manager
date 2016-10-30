function setMainHTML(html) {
    document.getElementById('main').innerHTML = html;
}
function maxChars(str, charsLen) {
    if (str.length > charsLen + 1) {
        return str.slice(0, charsLen) + '…';
    }
    return str;
}
///<reference path="./templates.d.ts"/>
///<reference path="./utils.ts"/>
function showTransactions() {
    getTransactions();
}
function getTransactions() {
    fetch('http://localhost:5000/transactions')
        .then(function (response) { return response.json(); })
        .then(function (json) {
        setMainHTML(renderTransactions(json));
    });
}
///<reference path="./transactions.ts"/>
showTransactions();
