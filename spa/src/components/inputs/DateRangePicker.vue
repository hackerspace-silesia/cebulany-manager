<template>
    <b-form-group label="Zakres" label-size="sm">
        <b-select v-model="option" size="sm" @change="updateOption">
            <option value="month">Miesiąc</option>
            <option value="year">Rok</option>
            <option value="range">Zakres</option>
        </b-select>
        <date-picker
            v-if="option == 'month'"
            v-model="month"
            type="month"
            value-type="format"
            token="YYYY-MM"
            :clearable="false"
            @change="updateMonth"
        />
        <date-picker
            v-if="option == 'year'"
            v-model="year"
            type="year"
            value-type="format"
            token="YYYY"
            :clearable="false"
            @change="updateYear"
        />
        <date-picker
            v-if="option == 'range'"
            v-model="range"
            type="date"
            value-type="format"
            token="YYYY-MM-DD"
            range-separator=" → "
            :clearable="false"
            :range="true"
            @change="updateRange"
        />
        <slot></slot>
    </b-form-group>
</template>
<script>
import { toIsoMonth } from '@/helpers/isoDate';
import DateRange from '@/models/dateRange';

export default {
    props: {
      value: { required: true, type: DateRange },
    },
    data() {
        const date = new Date();
        const year = date.getFullYear();
        const month = toIsoMonth(date);
        return {
            option: "month",
            month: month,
            year: year.toString(),
            range: DateRange.getRangeFromMonth(month),
        }
    },
    created() {
        this.updateValue(this.value);
    },
    watch: {
        value(value) {
            this.updateValue(value);
        },
    },
    methods: {
        updateOption(option) {
            switch(option) {
                case "month": this.updateMonth(); break;
                case "year": this.updateYear(); break;
                case "range": this.updateRange(); break;
            }
        },
        updateValue(value) {
            if (value.month !== undefined) {
                this.option = "month";
                this.month = value.month;
                this.range = [value.start, value.end];
            } else if (value.year !== undefined) {
                this.option = "year";
                this.year = value.year;
                this.range = [value.start, value.end];
            } else {
                this.option = "range";
                this.range = [value.start, value.end];
            }
        },
        updateMonth() {
            this.$emit('input', new DateRange({ month: this.month }));
        },
        updateYear() {
            this.$emit('input', new DateRange({ year: this.year }));
        },
        updateRange() {
            const [start, end] = this.range;
            this.$emit('input', new DateRange({ start, end }));
        }
    },
}
</script>