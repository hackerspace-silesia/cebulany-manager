import { toIsoDate, toIsoMonth } from '@/helpers/isoDate';

export default class DateRange {
  constructor(value) {
    if (value.month !== undefined) {
      this.month = value.month;
      const [start, end] = DateRange.getRangeFromMonth(value.month);
      this.start = start;
      this.end = end;
    } else if (value.year !== undefined) {
      this.year = value.year;
      const [start, end] = DateRange.getRangeFromYear(value.year);
      this.start = start;
      this.end = end;
    } else if (value.start !== undefined && value.end !== undefined) {
      this.start = value.start;
      this.end = value.end;
    } else {
      const date = new Date();
      this.month = toIsoMonth(date);
      const [start, end] = DateRange.getRangeFromMonth(this.month);
      this.start = start;
      this.end = end;
    }
  }

  toQuery() {
    if (this.year !== undefined) {
      return { year: this.year };
    }
    if (this.month !== undefined) {
      return { month: this.month };
    }
    return { start: this.start, end: this.end };
  }

  static fromQuery(query) {
    if (query.year !== undefined) {
      return new DateRange({ year: query.year });
    }
    if (query.month !== undefined) {
      return new DateRange({ month: query.month });
    }
    return new DateRange({ start: query.start, end: query.end });
  }

  static getRangeFromMonth(month) {
    let [_year, _month] = month.split("-");
    _year = parseInt(_year);
    _month = parseInt(_month) - 1;

    const start = new Date(_year, _month, 1);
    const end = new Date(_year, _month + 1, 0);
    return [toIsoDate(start), toIsoDate(end)];
  }

  static getRangeFromYear(year) {
    const _year = parseInt(year);

    const start = new Date(_year, 0, 1);
    const end = new Date(_year + 1, 0, 0);
    return [toIsoDate(start), toIsoDate(end)];
  }
};

export function queryToDateRange(query) {
  if (query.year !== undefined) {
    return new DateRange({ year: query.year });
  }
  if (query.month !== undefined) {
    return new DateRange({ month: query.month });
  }
  return new DateRange({ start: query.start, end: query.end });
}