<template lang="pug">
  table.table.table-sm.table-condensed.table-summary
    thead
      tr
        th.text-center Budżet →
        th.text-center(
          v-for="budget in budgets"
          :key="budget.id"
          :style="getBgColorStyle(budget.color)",
          colspan="2") {{budget.name}}
      tr
        th.text-center Typ ↓
        template(v-for="budget in budgets")
          th.text-center.neg-cell koszt
          th.text-center.pos-cell przychód
    tbody
      tr(v-for="paymentType in paymentTypes", :key="paymentType.id")
        th.text-center(:style="getBgColorStyle(paymentType.color)") {{ paymentType.name }}
        template(v-for="budget in budgets")
          td.text-right.neg-cell {{ getPaymentCost(budget.id, paymentType.id, false) }}
          td.text-right.pos-cell {{ getPaymentCost(budget.id, paymentType.id, true) }}

</template>
<script>
  export default {
    props: ['payments', 'budgets', 'paymentTypes'],
    methods: {
      getColor (color) {
        return '#' + color;
      },
      getBgColorStyle (color) {
        return {
          backgroundColor: this.getColor(color),
          color: 'white'
        };
      },
      makeKey (budgetId, paymentTypeId, isPositive) {
        return `${budgetId}-${paymentTypeId}-${isPositive ? 'p' : 'n'}`;
      },
      getPaymentCost (budgetId, paymentTypeId, isPositive) {
        const key = this.makeKey(budgetId, paymentTypeId, isPositive);
        return this.paymentsMap[key];
      }
    },
    computed: {
      paymentsMap () {
        const data = {};
        this.payments.forEach((payment) => {
          const key = this.makeKey(payment.budget_id, payment.payment_type_id, payment.is_positive);
          data[key] = payment.cost;
        });
        return data;
      }
    }
  }
</script>

<style scoped>
  .table-summary td, .table-summary th {
    border: 1px solid black;
  }

  .pos-cell, .neg-cell {
    font-family: monospace;
    font-weight: bold;
    vertical-align: middle;
  }
  .pos-cell {
    background-color: #cef3d2;
    color: #5FA777;
  }
  .neg-cell {
    background-color: #fdcccc;
    color: #FE4C40;
  }

</style>
