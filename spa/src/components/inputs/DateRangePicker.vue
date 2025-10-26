<template>
    <b-form-group label="Zakres" label-size="sm">
        <b-select v-model="range" size="sm" >
            <option value="month">Miesiąc</option>
            <option value="year">Rok</option>
            <!-- <option value="range">Zakres</option> -->
        </b-select>
        <date-picker
            v-if="range == 'month'"
            v-model="month"
            type="month"
            value-type="format"
            token="YYYY-MM"
            :clearable="false"
            @change="updateMonth"
        />
        <date-picker
            v-if="range == 'year'"
            v-model="year"
            type="year"
            value-type="format"
            token="YYYY"
            :clearable="false"
            @change="updateYear"
        />
    </b-form-group>
</template>
<script>
import { toIsoDate } from '@/helpers/isoDate';

export default {
    props: {
      value: { required: true },
    },
    data() {
        const date = new Date();
        const year = date.getFullYear();
        let month = date.getMonth();
        month = month < 10 ? `0${month}` : '' + month;
        return {
            range: "month",
            month: `${year}-${month}`,
            year: year.toString(),
        }
    },
    mounted() {
        if (this.value.month !== undefined) {
            this.range = "month";
            this.month = this.value.month;
        }
        if (this.value.year !== undefined) {
            this.range = "year";
            this.year = this.value.year;
        }
        this.update();
    },
    watch: {
        range() { this.update(); }
    },
    methods: {
        update() {
            switch(this.range) {
                case "month": this.updateMonth(); break;
                case "year": this.updateYear(); break;
            }
        },
        getRangeFromMonth(month) {
            let [_year, _month] = month.split("-");
            _year = parseInt(_year);
            _month = parseInt(_month) - 1;

            const start = new Date(_year, _month, 1);
            const end = new Date(_year, _month + 1, 0);
            return [start, end];
        },
        getRangeFromYear(year) {
            const _year = parseInt(year);

            const start = new Date(_year, 0, 1);
            const end = new Date(_year + 1, 0, 0);
            return [start, end];
        },
        updateMonth() {
            const [start, end] = this.getRangeFromMonth(this.month);
            this.$emit('input', {
                month: this.month,
                start: toIsoDate(start),
                end: toIsoDate(end),
            });
        },
        updateYear() {
            const [start, end] = this.getRangeFromYear(this.year);
            this.$emit('input', {
                year: this.year,
                start: toIsoDate(start),
                end: toIsoDate(end),
            });
        }
    },
}
</script>