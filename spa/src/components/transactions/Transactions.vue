<template lang="pug">
  b-row
    b-col
      h1 Przelewy
      TransactionForm
      TransactionLegend
      template(v-if='is_loading')
        b-progress(:value="1", :max="1", animated)
      template(v-else-if='is_error')
        b-progress(:value="1", :max="1", variant="danger" striped)
        br
        h3(class='text-center') Ugh Error ;_;
      template(v-else)
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

