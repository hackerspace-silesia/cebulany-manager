<template lang="pug">
  b-row
    b-col
      h1 Przelewy
      TransactionForm
      TransactionLegend
      TransactionTable(:transactions="transactions")
      TransactionLegend

</template>

<script>
import TransactionLegend from './TransactionLegend'
import TransactionTable from './TransactionTable'
import TransactionForm from './TransactionForm'
import TransactionService from '@/services/transactions'
import linkVm from '@/helpers/linkVm'

export default {
  data () {
    return {
      transactions: [],
      is_loading: false,
      is_error: false
    }
  },
  components: {
    TransactionLegend,
    TransactionTable,
    TransactionForm
  },
  created () {
    this.fetchTransactions();
  },
  methods: {
    fetchTransactions () {
      linkVm(this, TransactionService.get())
        .then((response) => {
          this.transactions = response.data.transactions;
        })
    }
  }
}
</script>

