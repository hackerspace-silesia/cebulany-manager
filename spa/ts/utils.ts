function setHTML(id: string, html: string) {
    document.getElementById(id).innerHTML = html;
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
    return today.getFullYear() + '-' + (today.getMonth() + 1);
}
