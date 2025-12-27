<template>
  <div>
  <PromisedComponent :state="promiseState">
    <TransactionTable :item="item" @update="update" ref="table" v-if="item" />
    <h5>Rozliczenia</h5>
    <table class="table table-bordered table-sm">
      <thead>
        <tr>
          <th>Typ</th>
          <th>Budżet</th>
          <th>Budżet wew.</th>
          <th>Nazwa</th>
          <th>Data</th>
          <th>Kwota</th>
          <th>*</th>
        </tr>
      </thead>
      <tbody v-if="item">
        <TransactionForm
          :item="item"
          :budgets="budgets"
          :inner-budgets="innerBudgets"
          :payment-types="paymentTypes"
        />
        <PaymentRow
          v-for="payment in item.payments"
          :key="payment.id"
          :payment="payment"
          @remove="remove"
        />
      </tbody>
    </table>
  </PromisedComponent>
  </div>
</template>
<script>
  import TransactionService from '@/services/transactions';
  import BudgetService from '@/services/budget'
  import InnerBudgetService from '@/services/innerBudget'
  import PaymentTypeService from '@/services/paymentType'

  import TransactionTable from './TransactionTable';
  import TransactionForm from './TransactionForm';
  import PaymentRow from './PaymentRow';
  import linkVm from '@/helpers/linkVm'

  export default {
    components: {TransactionTable, TransactionForm, PaymentRow},
    data () {
      return {
        item: null,
        budgets: [],
        innerBudgets: [],
        paymentTypes: [],
        promiseState: null,
      };
    },
    created() {
      const itemId = this.$route.params.id;
      let promises = [TransactionService.get(itemId), BudgetService.getAll(), InnerBudgetService.getAll(), PaymentTypeService.getAll()];
      linkVm(this, Promise.all(promises))
        .then(([ItemResponse, budgetResponse, innerBudgetResponse, paymentTypeResponse]) => {
          this.item = ItemResponse.data;
          this.budgets = this.transformArrayToMap(budgetResponse.data);
          this.innerBudgets = this.transformArrayToMap(innerBudgetResponse.data);
          this.paymentTypes = this.transformArrayToMap(paymentTypeResponse.data);
      });
    },
    methods: {
      transformArrayToMap (array) {
        let obj = {};
        array.forEach((item) => {
          obj[`${item.id}`] = item;
        });
        return obj;
      },
      update (item) {
        const {id, additional_info: AddtionalInfo} = item;
        const promise = TransactionService.put(id, {
          additional_info: AddtionalInfo,
        });
        linkVm(this.$refs.table, promise);
      },
      remove (pk) {
          let item = this.item;
          let oldObj = item.payments.find(obj => obj.id === pk);
          item.left = (Number(item.left) + Number(oldObj.cost)).toFixed(2);
          item.payments = item.payments.filter(obj => obj.id !== pk);
      }
    }
  }
</script>