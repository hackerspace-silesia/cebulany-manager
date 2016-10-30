///<reference path="./templates.d.ts"/>
///<reference path="./utils.ts"/>

function showTransactions() {
    getTransactions();
}

function getTransactions() {
    fetch('http://localhost:5000/transactions')
    .then((response) => {return response.json();})
    .then((json) => {
        setMainHTML(renderTransactions(json));
    });
}
