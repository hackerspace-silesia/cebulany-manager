<template lang="pug">
  b-row
    b-col
      h1 Podsumowanie
      SummaryForm(v-model="query")
      PromisedComponent(:state="promiseState")
        h2 Płatności
        SummaryTable(
          :budgets="budgets"
          :payment-types="paymentTypes"
          :payments="payments"
        )
        h2 Bilans
        SummaryInfo(
          :outstanding-cost="outstandingCost"
          :balances="balances"
        )
</template>

<script>
import SummaryTable from './SummaryTable'
import SummaryForm from './SummaryForm'
import SummaryInfo from './SummaryInfo'
import linkVm from '@/helpers/linkVm'

import PaymentService from '@/services/payment'
import PaymentTypeService from '@/services/paymentType';
import BudgetService from '@/services/budget';

export default {
  data () {
    return {
      payments: [],
      balances: {},
      outstandingCost: '0.00',
      budgets: [],
      paymentTypes: [],
      query: {},
      promiseState: null
    }
  },
  components: { SummaryTable, SummaryForm, SummaryInfo },
  watch: {
    query () {
      this.fetchPayments();
    }
  },
  mounted () {
    this.fetchAll();
  },
  methods: {
    fetchAll () {
      const promises = [
        PaymentService.getSummary(this.query),
        PaymentTypeService.getAll(),
        BudgetService.getAll()
      ];
      linkVm(this, Promise.all(promises))
        .then(([summaryResp, paymentTypeResp, budgetResp]) => {
          this.unpackSummaryResp(summaryResp);
          this.paymentTypes = paymentTypeResp.data;
          this.budgets = budgetResp.data;
        })
    },
    fetchPayments () {
      linkVm(this, PaymentService.getSummary(this.query))
        .then(this.unpackSummaryResp);
    },
    unpackSummaryResp (summaryResp) {
      this.payments = summaryResp.data.payments;
      this.balances = summaryResp.data.balances;
      this.outstandingCost = summaryResp.data.outstanding_cost;
    }
  }
}
</script>
