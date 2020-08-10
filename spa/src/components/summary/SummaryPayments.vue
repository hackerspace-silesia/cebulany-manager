<template>
  <b-row>
    <b-col>
      <h1>Podsumowanie</h1>
      <SummaryForm v-model="query" />
      <PromisedComponent :state="promiseState">
        <h2>Płatności</h2>
        <SummaryTable
          :budgets="filteredBudgets"
          :payment-types="filteredPaymentTypes"
          :payments="payments"
        />
        <h2>Bilans</h2>
        <SummaryInfo
          :outstanding-cost="outstandingCost"
          :balances="balances"
        />
      </PromisedComponent>
    </b-col>
  </b-row>
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
  components: { SummaryTable, SummaryForm, SummaryInfo },
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
  computed: {
    filteredPaymentTypes () {
      return this.paymentTypes.filter(({id}) =>
        this.payments.findIndex(payment => payment.payment_type_id === id) > -1
      )
    },
    filteredBudgets () {
      return this.budgets.filter(({id}) =>
        this.payments.findIndex(payment => payment.budget_id === id) > -1
      )
    }
  },
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
