<template>
  <table class="table table-sm table-condensed table-summary">
    <thead>
      <tr>
        <th class="text-center">
          Budżet →
        </th>
        <th
          v-for="budget in budgets"
          :key="budget.id"
          class="text-center"
          :style="getBgColorStyle(budget.color)"
          colspan="2"
        >
          {{ budget.name }}
        </th>
      </tr>
      <tr>
        <th class="text-center">
          Typ ↓
        </th><template v-for="budget in budgets">
          <th class="text-center neg-cell">
            koszt
          </th><th class="text-center pos-cell">
            przychód
          </th>
        </template>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="paymentType in paymentTypes"
        :key="paymentType.id"
      >
        <th
          class="text-center"
          :style="getBgColorStyle(paymentType.color)"
        >
          {{ paymentType.name }}
        </th><template v-for="budget in budgets">
          <td class="text-right neg-cell">
            {{ getPaymentCost(budget.id, paymentType.id, false) }}
          </td><td class="text-right pos-cell">
            {{ getPaymentCost(budget.id, paymentType.id, true) }}
          </td>
        </template>
      </tr>
    </tbody>
  </table>
</template>
<script>
  export default {
    props: ['payments', 'budgets', 'paymentTypes'],
    computed: {
      paymentsMap () {
        const data = {};
        this.payments.forEach((payment) => {
          const key = this.makeKey(payment.budget_id, payment.payment_type_id, payment.is_positive);
          data[key] = payment.cost;
        });
        return data;
      }
    },
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
