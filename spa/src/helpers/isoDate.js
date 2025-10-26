export function toIsoDate(dt) {
    const year = dt.getFullYear();
    let month = dt.getMonth() + 1;
    let day = dt.getDate();
    month = month < 10 ? `0${month}` : '' + month;
    day = day < 10 ? `0${day}` : '' + day;
    return `${year}-${month}-${day}`;
}

export function toIsoMonth(dt) {
    const year = dt.getFullYear();
    let month = dt.getMonth() + 1;
    month = month < 10 ? `0${month}` : '' + month;
    return `${year}-${month}`;
}