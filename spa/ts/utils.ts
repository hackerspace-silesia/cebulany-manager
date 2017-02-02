function byId(id: string): HTMLElement {
    return document.getElementById(id);
}

function setHTML(id: string, html: string) {
   byId(id).innerHTML = html;
}

function maxChars(str: string, charsLen: number): string {
    str = str || '';
    if (str.length > charsLen) {
        return str.slice(0, charsLen - 1) + '…';
    }
    return str;
}

function getActualMonth(): string {
    var today = new Date();
    var month = today.getMonth() + 1;
    if (month < 10) {
        month = '0' + month;
    }
    return today.getFullYear() + '-' + month;
}
