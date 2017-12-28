<template lang="pug">
  b-row
    b-col
      h1 Przelewy
      TransactionForm(@change="fetchTransactions")
      TransactionLegend
      PromisedComponent(:state="promiseState")
        TransactionTable(:transactions="transactions", :sum="sum")
      TransactionLegend
      TransactionUploadForm(@upload="uploadTransactions")

</template>

<script>
import TransactionLegend from './TransactionLegend'
import TransactionTable from './TransactionTable'
import TransactionForm from './TransactionForm'
import TransactionUploadForm from './TransactionUploadForm'
import TransactionService from '@/services/transactions'
import linkVm from '@/helpers/linkVm'

export default {
  data () {
    return {
      transactions: [],
      sum: 0,
      sumLeft: 0,
      promiseState: null
    }
  },
  components: {
    TransactionLegend,
    TransactionTable,
    TransactionForm,
    TransactionUploadForm
  },
  created () {
    this.fetchTransactions();
  },
  methods: {
    fetchTransactions (params) {
      linkVm(this, TransactionService.get(params))
        .then((response) => {
          this.transactions = response.data.transactions;
          this.sum = response.data.sum;
          this.sumLeft = response.data.sumLeft;
        })
    },
    uploadTransactions () {
      this.fetchTransactions();
    }
  }
}
</script>

