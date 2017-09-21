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
import TransactionModel from '@/models/transactions'

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
      this.is_loading = true;
      this.is_error = false;
      TransactionModel
        .get()
        .then((response) => {
          this.transactions = response.data.transactions;
          this.is_loading = false;
        })
        .catch((response) => {
          this.is_loading = false;
          this.is_error = true;
        })
    }
  }
}
</script>

