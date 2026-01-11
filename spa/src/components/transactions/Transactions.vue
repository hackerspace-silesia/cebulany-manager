<template>
  <b-row>
    <b-col>
      <h1>Przelewy</h1>
      <TransactionForm
        @change="setFormParams"
        @excel="excel"
      />
      <PromisedComponent :state="promiseState">
        <TransactionTable
          :transactions="transactions"
          :budgets="budgets"
          :payment-types="paymentTypes"
          :inner-budgets="innerBudgets"
          :sum="sum"
          :sum-left="sumLeft"
        />
      </PromisedComponent>
      <TransactionUploadForm @upload="uploadTransactions" />
    </b-col>
  </b-row>
</template>

<script>
import TransactionTable from './TransactionTable'
import TransactionForm from './TransactionForm'
import TransactionUploadForm from './TransactionUploadForm'
import linkVm from '@/helpers/linkVm'

import TransactionService from '@/services/transactions'

export default {
  components: {
    TransactionTable,
    TransactionForm,
    TransactionUploadForm
  },
  data () {
    return {
      formParams: null,
      transactions: [],
      sum: 0,
      sumLeft: 0,
      promiseState: null
    }
  },
  methods: {
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
      linkVm(this, TransactionService.getAll(this.formParams))
        .then((response) => {
          this.transactions = response.data.transactions;
          this.sum = response.data.sum;
          const sumFromPayments = this.transactions.reduce(
            (st, t) => {
              if(!t.payments) return st;
              return st + t.payments.reduce((sp, p) => sp + parseFloat(p.cost), 0.0);
            }, 0.0);
          this.sumLeft = (parseFloat(this.sum) - sumFromPayments).toFixed(2);
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