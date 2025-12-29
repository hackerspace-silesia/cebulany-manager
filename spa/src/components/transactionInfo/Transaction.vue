<template>
  <div>
  <PromisedComponent :state="promiseState">
    <template v-if="transaction">
      <TransactionTable :item="transaction" @update="update" ref="table"/>
      <PaymentTable 
        :transaction="transaction"
        :budgets="budgets"
        :inner-budgets="innerBudgets"
        :payment-types="paymentTypes"
      />
      <AttachmentTable 
        :transaction="transaction"
      />
    </template>
    <template v-else>
      Something is wrong.
    </template>
  </PromisedComponent>
  </div>
</template>
<script>
  import TransactionService from '@/services/transactions';
  import BudgetService from '@/services/budget';
  import InnerBudgetService from '@/services/innerBudget';
  import PaymentTypeService from '@/services/paymentType';

  import TransactionTable from './TransactionTable';
  import PaymentTable from './PaymentTable';
  import AttachmentTable from './AttachmentTable';
  import linkVm from '@/helpers/linkVm';

  export default {
    components: {TransactionTable, AttachmentTable, PaymentTable},
    data () {
      return {
        transaction: null,
        budgets: [],
        innerBudgets: [],
        paymentTypes: [],
        documents: [],
        promiseState: null,
      };
    },
    created() {
      const transactionId = this.$route.params.id;
      let promises = [
        TransactionService.get(transactionId),
        BudgetService.getAll(),
        InnerBudgetService.getAll(),
        PaymentTypeService.getAll(),
      ];
      linkVm(this, Promise.all(promises))
        .then(([
          transactionResponse,
          budgetResponse,
          innerBudgetResponse,
          paymentTypeResponse,
        ]) => {
          this.transaction = transactionResponse.data;
          this.budgets = this.transformArrayToMap(budgetResponse.data);
          this.innerBudgets = this.transformArrayToMap(innerBudgetResponse.data);
          this.paymentTypes = this.transformArrayToMap(paymentTypeResponse.data);
      });
    },
    methods: {
      transformArrayToMap (array) {
        let obj = {};
        array.forEach((transaction) => {
          obj[`${transaction.id}`] = transaction;
        });
        return obj;
      },
      update (transaction) {
        const {id, additional_info: AddtionalInfo} = transaction;
        const promise = TransactionService.put(id, {
          additional_info: AddtionalInfo,
        });
        linkVm(this.$refs.table, promise);
      },
    }
  }
</script>