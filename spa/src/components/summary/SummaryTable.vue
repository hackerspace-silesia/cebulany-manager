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
        <th colspan="2" class="text-center">SUMA</th>
      </tr>
      <tr>
        <th class="text-center">
          Typ ↓
        </th>
        <template v-for="budget in budgets">
          <th class="text-center neg-cell">
            koszt
          </th>
          <th class="text-center pos-cell">
            przychód
          </th>
        </template>
        <th class="text-center neg-cell">
          koszt
        </th>
        <th class="text-center pos-cell">
          przychód
        </th>
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
        </th>
        <template v-for="budget in budgets">
          <td class="text-right neg-cell">
            {{ getPaymentCost(budget.id, paymentType.id, false) }}
          </td>
          <td class="text-right pos-cell">
            {{ getPaymentCost(budget.id, paymentType.id, true) }}
          </td>
        </template>
        <td class="text-right neg-cell">
          {{ getPaymentRowCost(paymentType.id, false).toFixed(2) }}
        </td>
        <td class="text-right pos-cell">
          {{ getPaymentRowCost(paymentType.id, true).toFixed(2) }}
        </td>
      </tr>
    </tbody>
    <tfoot>
      <tr>
        <th class="text-center">SUMA</th>
        <template v-for="budget in budgets">
          <td class="text-right neg-cell">
            {{ getPaymentColCost(budget.id, false).toFixed(2) }}
          </td>
          <td class="text-right pos-cell">
            {{ getPaymentColCost(budget.id, true).toFixed(2) }}
          </td>
        </template>
        <td class="text-right neg-cell">{{ totalNeg.toFixed(2) }}</td>
        <td class="text-right pos-cell">{{ totalPos.toFixed(2) }}</td>
      </tr>
      <tr>
        <th class="text-center">SUMA</th>
        <td v-for="budget in budgets" colspan="2" class="text-right total-cell">
          {{ (getPaymentColCost(budget.id, false) + getPaymentColCost(budget.id, true)).toFixed(2) }}
        </td>
        <td class="text-right total-cell" colspan="2">{{ (totalPos + totalNeg).toFixed(2) }}</td>
      </tr>
    </tfoot>
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
      },
      totalNeg () {
        const total = this.payments
          .filter(p => !p.is_positive)
          .reduce((c, payment) => c + parseFloat(payment.cost || "0"), 0);
        return total;
      },
      totalPos () {
        const total = this.payments
          .filter(p => p.is_positive)
          .reduce((c, payment) => c + parseFloat(payment.cost || "0"), 0);
        return total;
      },
    },
    methods: {
      getColor (color) {
        return '#' + color;
      },
      getBgColorStyle (color) {
        return {
          backgroundColor: this.getColor(color),
          color: 'white',
        };
      },
      makeKey (budgetId, paymentTypeId, isPositive) {
        return `${budgetId}-${paymentTypeId}-${isPositive ? 'p' : 'n'}`;
      },
      getPaymentCost (budgetId, paymentTypeId, isPositive) {
        const key = this.makeKey(budgetId, paymentTypeId, isPositive);
        return this.paymentsMap[key];
      },
      getPaymentColCost (budgetId, isPositive) {
        return this.paymentTypes.reduce((c, payment) => {
          const key = this.makeKey(budgetId, payment.id, isPositive);
          const value = this.paymentsMap[key] || "0";
          return c + parseFloat(value);
        }, 0);
      },
      getPaymentRowCost (paymentTypeId, isPositive) {
        return this.budgets.reduce((c, budget) => {
          const key = this.makeKey(budget.id, paymentTypeId, isPositive);
          const value = this.paymentsMap[key] || "0";
          return c + parseFloat(value);
        }, 0);
      },
    }
  }
</script>

<style scoped>
  .table-summary td, .table-summary th {
    border: 1px solid black;
  }

  .pos-cell, .neg-cell, .total-cell {
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
