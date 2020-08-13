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
          <b-form-input
            v-model="month"
            size="sm"
            type="month"
            @change="updateForm"
          />
        </template><template v-else-if="monthOption == 'date_range'">
          <label>od&nbsp;</label><b-form-input
            v-model="startDate"
            size="sm"
            type="date"
            @change="updateForm"
          /><label>&nbsp;do&nbsp;</label><b-form-input
            v-model="endDate"
            size="sm"
            type="date"
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
        startDate: today.slice(0, 7) + '-01',
        endDate: today.slice(0, 10),
        text: '',
        monthOption: 'month',
        monthOptions: [
          {text: 'Miesiąc', value: 'month'},
          {text: 'Zakres Dat', value: 'date_range'}
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
