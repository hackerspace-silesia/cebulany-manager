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
            label="Budżet wewnętrzny"
            label-size="sm"
          >
            <type-select
              v-model="query.inner_budget_id"
              :types="innerBudgets"
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
              <option :value="true"> Miesiąc </option>
              <option :value="false"> Rok </option>
            </b-select>
            <date-picker
              v-if="withMonth"
              v-model="month"
              type="month"
              value-type="format"
              token="YYYY-MM"
              :clearable="false"
            />
            <date-picker
              v-if="!withMonth"
              v-model="year"
              type="year"
              value-type="format"
              token="YYYY"
              :clearable="false"
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
  import InnerBudgetService from '@/services/innerBudget'

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
          inner_budget_id: null,
          month: `${year}-${month}`
        },
        month: `${year}-${month}`,
        year: year.toString(),
        withMonth: true,
        promiseState: null,
        paymentTypes: [],
        budgets: [],
        innerBudgets: [],
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
        let promises = [BudgetService.getAll(), PaymentTypeService.getAll(), InnerBudgetService.getAll()];
        linkVm(this, Promise.all(promises))
          .then(([budgetResponse, paymentTypeResponse, innerBudgetResponse]) => {
            this.budgets = this.transformArrayToMap(budgetResponse.data);
            this.innerBudgets = this.transformArrayToMap(innerBudgetResponse.data);
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
