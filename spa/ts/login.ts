///<reference path="./transactions.ts"/>
///<reference path="./members.ts"/>
///<reference path="./bills.ts"/>
///<reference path="./donations.ts"/>
///<reference path="./others.ts"/>


function showLogin() {
    setHTML('main', renderLogin());
    view = new LoginView();
    menu = document.getElementById('menu')
    menu.style.display = 'none'
}


class LoginView {
    form: HTMLFormElement;
    constructor() {
        this.form = document.forms['login']
        this.form.onsubmit = doLogin
    }
}

function doLogin() {
    form = document.forms['login']
    auth.password = form.elements['password'].value
    auth.user = form.elements['user'].value
    console.log(auth)
    
    menu = document.getElementById('menu')
    menu.style.display = 'block'
    showTransactions()
    return false
}
