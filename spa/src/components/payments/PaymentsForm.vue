<template>
  <PromisedComponent :state="promiseState">
    <b-form>
      <b-form-row>
        <b-col>
          <b-form-group
            label="Budżet"
            label-size="sm"
          >
            <type-select
              v-model="query.budget_id"
              :types="budgets"
              has-null-option="hasNullOption"
            />
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group
            label="Typ"
            label-size="sm"
          >
            <type-select
              v-model="query.payment_type_id"
              :types="paymentTypes"
              has-null-option="hasNullOption"
            />
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group
            label="Miesiąc / Rok"
            label-size="sm"
          >
            <b-select
              v-model="withMonth"
              size="sm"
            >
              <option :value="true">
                Miesiąc
              </option>
              <option :value="false">
                Rok
              </option>
            </b-select>
            <b-form-input
              v-if="withMonth"
              v-model="month"
              type="month"
            />
            <b-form-input
              v-if="!withMonth"
              v-model="year"
              type="number"
            />
          </b-form-group>
        </b-col>
      </b-form-row>
    </b-form>
  </PromisedComponent>
</template>
<script>
  import TypeSelect from '@/components/inputs/TypeSelect';
  import linkVm from '@/helpers/linkVm'

  import PaymentTypeService from '@/services/paymentType'
  import BudgetService from '@/services/budget'

  export default {
    components: {
      TypeSelect
    },
    data () {
      const date = new Date();
      const year = date.getFullYear();
      let month = date.getMonth() + 1;
      month = month < 10 ? `0${month}` : '' + month;
      return {
        query: {
          payment_type_id: null,
          budget_id: null,
          month: `${year}-${month}`
        },
        month: `${year}-${month}`,
        year: year,
        withMonth: true,
        promiseState: null,
        paymentTypes: [],
        budgets: []
      };
    },
    watch: {
      query: {
        deep: true,
        handler () {
          this.setQuery();
        }
      },
      year (value) {
        this.query.month = value;
      },
      month (value) {
        this.query.month = value;
      },
      withMonth (withMonth) {
        this.query.month = withMonth ? this.month : this.year;
      }
    },
    created () {
      this.setQuery();
      this.fetchInit();
    },
    methods: {
      fetchInit () {
        let promises = [BudgetService.getAll(), PaymentTypeService.getAll()];
        linkVm(this, Promise.all(promises))
          .then(([budgetResponse, paymentTypeResponse]) => {
            this.budgets = this.transformArrayToMap(budgetResponse.data);
            this.paymentTypes = this.transformArrayToMap(paymentTypeResponse.data);
          })
      },
      transformArrayToMap (array) {
        let obj = {};
        array.forEach((item) => {
          obj[`${item.id}`] = item;
        });
        return obj;
      },
      setQuery () {
        const query = Object.assign({}, this.query);
        this.$emit('input', query);
      }
    }
  }
</script>
