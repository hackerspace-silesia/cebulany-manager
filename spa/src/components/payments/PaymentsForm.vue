<template lang="pug">
  PromisedComponent(:state="promiseState"): b-form
    b-form-row
      b-col: b-form-group(label="Budżet", label-size="sm")
        type-select(
          :types="budgets",
          hasNullOption,
          v-model="query.budget_id")
      b-col: b-form-group(label="Typ", label-size="sm")
        type-select(
          :types="paymentTypes",
          hasNullOption,
          v-model="query.payment_type_id")
      b-col
        b-select(v-model="withMonth" size="sm")
          option(:value="true") Miesiąc
          option(:value="false") Rok

        b-form-input(
          v-if="withMonth",
          v-model="query.month",
          type="month")
        b-form-input(
          v-if="!withMonth",
          v-model="query.month",
          type="number")


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
      let month = date.getMonth() + 1;
      month = month < 10 ? `0${month}` : '' + month;
      return {
        query: {
          payment_type_id: null,
          budget_id: null,
          month: `${date.getFullYear()}-${month}`
        },
        withMonth: true,
        promiseState: null,
        paymentTypes: [],
        budgets: []
      };
    },
    created () {
      this.setQuery();
      this.fetchInit();
    },
    watch: {
      query: {
        deep: true,
        handler () {
          this.setQuery();
        }
      }
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
