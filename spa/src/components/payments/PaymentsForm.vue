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
          <date-range-picker v-model="query.dateRange" />
        </b-col>
      </b-form-row>
    </b-form>
  </PromisedComponent>
</template>
<script>
  import DateRange from '@/models/dateRange';
  import TypeSelect from '@/components/inputs/TypeSelect';
  import DateRangePicker from '@/components/inputs/DateRangePicker';
  import linkVm from '@/helpers/linkVm'

  import PaymentTypeService from '@/services/paymentType'
  import BudgetService from '@/services/budget'
  import InnerBudgetService from '@/services/innerBudget'

  export default {
    components: {
      TypeSelect,
      DateRangePicker,
    },
    data () {
      return {
        query: this.makeNewQuery(),
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
      $route() {
        this.query = this.makeNewQuery();
      },
    },
    created () {
      this.setQuery();
      this.fetchInit();
    },
    methods: {
      makeNewQuery() {
        const dateRange = DateRange.fromQuery(this.$route.query);
        return {
          payment_type_id: this.$route.query.payment_type_id || null,
          budget_id: this.$route.query.budget_id || null,
          inner_budget_id: this.$route.query.inner_budget_id || null,
          dateRange,
        };
      },
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
