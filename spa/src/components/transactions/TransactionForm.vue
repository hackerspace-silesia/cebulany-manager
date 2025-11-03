<template>
  <b-form-row inline="inline" @submit.stop.prevent>
    <b-col sm="4">
      <date-range-picker v-model="dateRange">
        <b-button size="sm" v-if="dateRange.month !== undefined" @click="excel">Excel</b-button>
      </date-range-picker>
    </b-col>
    <b-col sm="8">
      <b-form-group label="Szukaj" label-size="sm">
        <b-form-input
          v-model.trim="text"
          size="sm"
          type="text"
          placeholder="Szukaj..."
        />
      </b-form-group>
    </b-col>
  </b-form-row>
</template>

<script>
  import DateRange from '@/models/dateRange';
  import DateRangePicker from '@/components/inputs/DateRangePicker';

  export default {
    components: {
      DateRangePicker,
    },
    data () {
      const dateRange = DateRange.fromQuery(this.$route.query);
      return {
        dateRange,
        text: this.$route.query.text || '',
      }
    },
    watch: {
      text() { this.updateForm(); },
      dateRange() { this.updateForm(); },
      $route() { 
        this.dateRange = DateRange.fromQuery(this.$route.query);
        this.text = this.$route.query.text || '';
      },
    },
    created () {
      this.updateForm();
    },
    methods: {
      updateForm () {
        let data = {
          date_start: this.dateRange.start,
          date_end: this.dateRange.end,
        }
        let query = this.dateRange.toQuery();
        if (this.text) {
          data.text = this.text;
          query.text = this.text;
        }
        this.$router.replace({
          name: 'Transactions',
          query,
        }).catch(()=>{});
        this.$emit('change', data);
      },
      excel () {
        if (this.dateRange.month !== undefined) {
          this.$emit('excel', this.dateRange.month );
        }
      }
    }
  }
</script>
