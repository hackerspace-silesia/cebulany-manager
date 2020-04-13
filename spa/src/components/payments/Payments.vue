<template lang="pug">
  b-row
    b-col
      h1 Płatności
      PaymentsNavigation(v-model="page", :count="count", :items-per-page="itemsPerPage")
      PromisedComponent(:state="promiseState")
        PaymentsTable(
          :payments="payments"
        )
      PaymentsNavigation(v-model="page", :count="count", :items-per-page="itemsPerPage")
</template>

<script>
import PaymentsTable from './PaymentsTable'
import PaymentsNavigation from './PaymentsNavigation'
import linkVm from '@/helpers/linkVm'

import PaymentService from '@/services/payment'

export default {
  data () {
    return {
      payments: [],
      page: 1,
      count: 0,
      itemsPerPage: 1,
      promiseState: null
    }
  },
  components: {
    PaymentsTable,
    PaymentsNavigation
  },
  created () {
    this.fetchPayments();
  },
  watch: {
    page () {
      this.fetchPayments();
    }
  },
  methods: {
    fetchPayments () {
      const query = {
        page: this.page
      };
      linkVm(this, PaymentService.getAll(query))
        .then((response) => {
          const {data, count, items_per_page: itemsPerPage} = response.data;
          this.payments = data;
          this.count = count;
          this.itemsPerPage = itemsPerPage;
        })
    }
  }
}
</script>

<style>
  .payment-type-badge {
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
  .payment-type-badge-big {
    width: 18px;
    font-size: 9pt;
    border-radius: 8px;
  }
</style>
