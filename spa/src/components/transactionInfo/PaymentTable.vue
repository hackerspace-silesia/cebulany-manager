<template>
  <b-row>
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
      <tbody>
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
  </b-row>
</template>
<script>
  import PaymentFormAdd from './PaymentFormAdd';
  import PaymentFormUpdate from './PaymentFormUpdate.vue';

  export default {
    components: {PaymentFormAdd, PaymentFormUpdate},
    props: ['transaction', 'budgets', 'innerBudgets', 'paymentTypes'],
    methods: {
      remove (pk) {
          let transaction = this.transaction;
          let oldObj = transaction.payments.find(obj => obj.id === pk);
          transaction.left = (Number(transaction.left) + Number(oldObj.cost)).toFixed(2);
          transaction.payments = transaction.payments.filter(obj => obj.id !== pk);
      },
    }
  }
</script>
