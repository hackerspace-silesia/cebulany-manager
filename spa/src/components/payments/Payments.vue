<template>
  <b-row>
    <b-col>
      <h1>Płatności</h1>
      <PaymentsForm v-model="query" />
      <b-button @click="excel">
        Excel
      </b-button>
      <PaymentsNavigation
        v-model="page"
        :count="count"
        :items-per-page="itemsPerPage"
      />
      <PromisedComponent :state="promiseState">
        <b-row v-if="total != '-'">
          Razem:&nbsp;<money-value :value="total" />
        </b-row>
        <b-row>
          <b-col v-if="groups.paymentType.data.length > 1">
            <PaymentsGroupTable title="Typ" :group="groups.paymentType" />
          </b-col>
          <b-col v-if="groups.budget.data.length > 1">
            <PaymentsGroupTable title="Budżet" :group="groups.budget" />
          </b-col>
          <b-col v-if="groups.innerBudget.data.length > 1">
            <PaymentsGroupTable title="Budżet Wew." :group="groups.innerBudget" />
          </b-col>
        </b-row>
        <InnerTransfersTable 
          v-if="innerTransfers && innerTransfers.length > 0"
          :inner-transfers="innerTransfers" 
        />
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
import PaymentsGroupTable from './PaymentsGroupTable'
import PaymentsNavigation from './PaymentsNavigation'
import InnerTransfersTable from './InnerTransfersTable'
import PaymentsForm from './PaymentsForm'
import linkVm from '@/helpers/linkVm'

import PaymentService from '@/services/payment'
import PaymentTypeService from '@/services/paymentType';
import BudgetService from '@/services/budget';
import InnerBudgetService from '@/services/innerBudget';

export default {
  components: {
    PaymentsTable,
    PaymentsGroupTable,
    PaymentsNavigation,
    InnerTransfersTable,
    PaymentsForm
  },
  data () {
    return {
      payments: [],
      innerTransfers: [],
      query: {},
      groups: {
        paymentType: {data: [], ids: {}},
        budget: {data: [], ids: {}},
        innerBudget: {data: [], ids: {}},
      },
      page: 1,
      total: "-",
      count: 0,
      itemsPerPage: 1,
      promiseState: null,
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
  mounted() {
      const promises = [
        PaymentTypeService.getAll(),
        BudgetService.getAll(),
        InnerBudgetService.getAll(),
      ];

      linkVm(this, Promise.all(promises))
        .then(([paymentTypeResp, budgetResp, innerBudgetResp]) => {
          this.groups.paymentType.ids = this.convertGroupIds(paymentTypeResp.data);
          this.groups.budget.ids = this.convertGroupIds(budgetResp.data);
          this.groups.innerBudget.ids = this.convertGroupIds(innerBudgetResp.data);
        });
  },
  methods: {
    fetchPayments() {
      linkVm(this, this.fetchPaymentsPromise());
    },
    convertGroupIds(group) {
      const objs = {};
      group.forEach(obj => {objs[obj.id] = obj;});
      return objs;
    },
    excel () {
      linkVm(this, PaymentService.getExcel(this.createQuery()));
    },
    fetchPaymentsPromise() {
      this.$router.replace({
        name: 'Payments',
        query: this.createQueryToRouting(),
      }).catch(()=>{});

      return PaymentService.getAll(this.createQuery())
        .then((response) => {
          const {data, count, total, groups, inner_transfers: innerTransfers, items_per_page: itemsPerPage} = response.data;
          this.payments = data;
          this.count = count;
          this.total = total;
          this.groups.paymentType.data = groups.payment_type;
          this.groups.budget.data = groups.budget;
          this.groups.innerBudget.data = groups.inner_budget;
          this.innerTransfers = innerTransfers;
          this.itemsPerPage = itemsPerPage;
        });
    },
    createQueryToRouting() {
      const {dateRange, ...prevQuery } = this.query;
      return {
          page: this.page,
          ...dateRange.toQuery(),
          ...prevQuery,
      };
    },
    createQuery() {
      const {dateRange, ...prevQuery } = this.query;
      return {
        page: this.page,
        start_date: dateRange.start,
        end_date: dateRange.end,
        ...prevQuery,
      };
    },
  }
}
</script>