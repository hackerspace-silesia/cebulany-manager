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
      let monthOption = 'month';
      let month = today.slice(0, 7);
      let dateRange = [today.slice(0, 7) + '-01', today.slice(0, 10)];
      const params = this.$route.params;
      if (params.start && params.end) {
        if (params.end === "-") {
          monthOption = 'month';
          month = params.start;
        } else {
          monthOption = 'date_range';
          dateRange = [params.start, params.end];
        }
      }
      return {
        month,
        dateRange,
        monthOption,
        text: this.$route.query.text || '',
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
        let query = {};
        if (this.text) {
          data.text = this.text;
          query.text = this.text;
        }
        if (this.monthOption === 'month') {
          this.$router.replace({
            name: 'Transactions-Range',
            params: { start: this.month, end: "-" },
            query,
          });
          data.month = this.month;
        } else if (this.monthOption === 'date_range') {
          const [start, end] = this.dateRange
          this.$router.replace({
            name: 'Transactions-Range',
            params: { start, end },
            query,
          });
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
