<template>
  <div class="row">
    <div class="col-6">
      <b-form-radio-group
        v-model="monthOption"
        :options="monthOptions"
        @change="updateForm"
      />
      <b-form inline="inline">
        <template v-if="monthOption == 'month'">
          <date-picker
            v-model="month"
            type="month"
            value-type="format"
            token="YYYY-MM"
            :clearable="false"
            @change="updateForm"
          />
          &nbsp;
          <b-button size="sm" @click="excel">Excel</b-button>
        </template>
        <template v-else-if="monthOption == 'date_range'">
          <date-picker
            v-model="dateRange"
            type="date"
            value-type="format"
            token="YYYY-MM-DD"
            range-separator=" → "
            :clearable="false"
            range
            @change="updateForm"
          />
        </template>
      </b-form>
    </div>
    <div class="col-6">
      <b-form>
        <b-form-input
          v-model.trim="text"
          size="sm"
          type="text"
          placeholder="Szukaj..."
          @change="updateForm"
        />
      </b-form>
    </div>
  </div>
</template>

<script>
  export default {
    data () {
      let today = (new Date()).toISOString();
      return {
        month: today.slice(0, 7),
        dateRange: [today.slice(0, 7) + '-01', today.slice(0, 10)],
        text: '',
        monthOption: 'month',
        monthOptions: [
          {text: 'Miesiąc', value: 'month'},
          {text: 'Zakres Dat', value: 'date_range'}
        ]
      }
    },
    created () {
      this.updateForm();
    },
    methods: {
      updateForm () {
        let data = {};
        if (this.text) {
          data.text = this.text;
        }
        if (this.monthOption === 'month') {
          data.month = this.month;
        } else if (this.monthOption === 'date_range') {
          const [start, end] = this.dateRange
          data.date_start = start;
          data.date_end = end;
        }
        this.$emit('change', data);
      },
      excel () {
        if (this.monthOption === 'month') {
          this.$emit('excel', this.month);
        }
      }
    }
  }
</script>
