<template lang="pug">
  .row
    .col-6
      b-form-radio(v-model="monthOption", :options="monthOptions", @change="updateForm")
      b-form(inline)
        template(v-if="monthOption == 'month'")
          b-form-input(size="sm", v-model="month", type="month", @change="updateForm")
        template(v-else-if="monthOption == 'date_range'")
          label od&nbsp;
          b-form-input(size="sm", v-model="startDate", type="date", @change="updateForm")
          label &nbsp;do&nbsp;
          b-form-input(size="sm", v-model="endDate", type="date", @change="updateForm")
    .col-6
      b-form
        b-form-input(
            size="sm", v-model.trim="text", type="text",
            placeholder="Szukaj...", @change="updateForm")
</template>

<script>
  export default {
    data () {
      let today = (new Date()).toISOString();
      return {
        month: today.slice(0, 7),
        startDate: today.slice(0, 7) + '-01',
        endDate: today.slice(0, 10),
        text: '',
        monthOption: 'month',
        monthOptions: [
          {'text': 'Miesiąc', value: 'month'},
          {'text': 'Zakres Dat', value: 'date_range'}
        ]
      }
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
          data.date_start = this.startDate;
          data.date_end = this.endDate;
        }
        this.$emit('change', data);
      }
    }
  }
</script>
