<template>
  <b-row>
    <b-col>
      <h1>Przelewy</h1>
      <TransactionForm
        @change="setFormParams"
        @excel="excel"
      />
      <TransactionLegend
        :budgets="budgets"
        :payment-types="paymentTypes"
      />
      <PromisedComponent :state="promiseState">
        <TransactionTable
          :transactions="transactions"
          :budgets="budgets"
          :payment-types="paymentTypes"
          :inner-budgets="innerBudgets"
          :sum="sum"
        />
      </PromisedComponent>
      <TransactionLegend
        :budgets="budgets"
        :payment-types="paymentTypes"
      />
      <TransactionUploadForm @upload="uploadTransactions" />
    </b-col>
  </b-row>
</template>

<script>
import TransactionLegend from './TransactionLegend'
import TransactionTable from './TransactionTable'
import TransactionForm from './TransactionForm'
import TransactionUploadForm from './TransactionUploadForm'
import linkVm from '@/helpers/linkVm'

import TransactionService from '@/services/transactions'
import BudgetService from '@/services/budget'
import InnerBudgetService from '@/services/innerBudget'
import PaymentTypeService from '@/services/paymentType'

export default {
  components: {
    TransactionLegend,
    TransactionTable,
    TransactionForm,
    TransactionUploadForm
  },
  data () {
    return {
      formParams: null,
      transactions: [],
      paymentTypes: {},
      budgets: {},
      innerBudgets: {},
      sum: 0,
      sumLeft: 0,
      promiseState: null
    }
  },
  created () {
    this.fetchInit();
  },
  methods: {
    fetchInit () {
      let promises = [BudgetService.getAll(), InnerBudgetService.getAll(), PaymentTypeService.getAll()];
      linkVm(this, Promise.all(promises))
        .then(([budgetResponse, innerBudgetResponse, paymentTypeResponse]) => {
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
    setFormParams(params) {
      this.formParams = params;
      this.fetchTransactions();
    },
    fetchTransactions () {
      linkVm(this, TransactionService.get(this.formParams))
        .then((response) => {
          this.transactions = response.data.transactions;
          this.sum = response.data.sum;
          this.sumLeft = response.data.sumLeft;
        })
    },
    uploadTransactions () {
      this.fetchTransactions();
    },
    excel (month) {
      linkVm(this, TransactionService.getExcelTable(month));
    }
  }
}
</script>

<style>
  .transaction-badge {
    display: inline-block;
    text-align: center;
    width: 16px;
    margin: 0 1px;
    border-radius: 4px;
    color: white;
    font-size: 7pt;
    font-weight: bold;
    border: solid black;
    border-width: 3px;
  }
  .transaction-badge-big {
    width: 18px;
    font-size: 9pt;
    border-radius: 8px;
  }
</style>
