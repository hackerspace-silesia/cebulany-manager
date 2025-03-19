<template>
  <b-row>
    <b-col>
      <h1>Płatności</h1>
      <PaymentsForm v-model="query" />
      <PaymentsNavigation
        v-model="page"
        :count="count"
        :items-per-page="itemsPerPage"
      />
      <PromisedComponent :state="promiseState">
        <PaymentsTable :payments="payments" />
      </PromisedComponent>
      <PaymentsNavigation
        v-model="page"
        :count="count"
        :items-per-page="itemsPerPage"
      />
    </b-col>
  </b-row>
</template>

<script>
import PaymentsTable from './PaymentsTable'
import PaymentsNavigation from './PaymentsNavigation'
import PaymentsForm from './PaymentsForm'
import linkVm from '@/helpers/linkVm'

import PaymentService from '@/services/payment'

export default {
  components: {
    PaymentsTable,
    PaymentsNavigation,
    PaymentsForm
  },
  data () {
    return {
      payments: [],
      query: {},
      page: 1,
      count: 0,
      itemsPerPage: 1,
      promiseState: null
    }
  },
  watch: {
    page () {
      this.fetchPayments();
    },
    query () {
      this.fetchPayments();
    }
  },
  methods: {
    fetchPayments () {
      const query = {
        page: this.page,
        ...this.query
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