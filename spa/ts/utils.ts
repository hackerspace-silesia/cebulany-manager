function setMainHTML(html: string) {
    document.getElementById('main').innerHTML = html;
}

function maxChars(str: string, charsLen: number) {
    if (str.length > charsLen + 1) {
        return str.slice(0, charsLen) + '…';
    }
    return str;
}
