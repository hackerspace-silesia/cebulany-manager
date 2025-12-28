<template>
  <div>
  <PromisedComponent :state="promiseState">
    <TransactionTable :item="transaction" @update="update" ref="table" v-if="transaction" />
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
      <tbody v-if="transaction">
        <PaymentFormAdd
          :transaction="transaction"
          :budgets="budgets"
          :inner-budgets="innerBudgets"
          :payment-types="paymentTypes"
        />
        <PaymentFormUpdate
          v-for="payment in transaction.payments"
          :key="payment.id"
          :payment="payment"
          :transaction="transaction"
          :budgets="budgets"
          :inner-budgets="innerBudgets"
          :payment-types="paymentTypes"
          @remove="remove"
        />
      </tbody>
    </table>
    <h5>
      Załączniki 
      <b-button variant="primary" @click="showModal">Dodaj</b-button>
    </h5> 
    <DocumentModal
      v-if="transaction"
      ref="documentModal"
      :transaction="transaction"
      @add="addAttachment"
    />
  </PromisedComponent>
  </div>
</template>
<script>
  import TransactionService from '@/services/transactions';
  import BudgetService from '@/services/budget';
  import InnerBudgetService from '@/services/innerBudget';
  import PaymentTypeService from '@/services/paymentType';

  import TransactionTable from './TransactionTable';
  import PaymentFormAdd from './PaymentFormAdd';
  import PaymentFormUpdate from './PaymentFormUpdate.vue';
  import DocumentModal from './DocumentModal.vue';
  import linkVm from '@/helpers/linkVm';

  export default {
    components: {TransactionTable, PaymentFormAdd, PaymentFormUpdate, DocumentModal},
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
      remove (pk) {
          let transaction = this.transaction;
          let oldObj = transaction.payments.find(obj => obj.id === pk);
          transaction.left = (Number(transaction.left) + Number(oldObj.cost)).toFixed(2);
          transaction.payments = transaction.payments.filter(obj => obj.id !== pk);
      },
      showModal() {
        this.$refs.documentModal.show();
      },
      addAttachment(obj) {
        this.$refs.documentModal.hide();
        console.log(obj);
      },
    }
  }
</script>