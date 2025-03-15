<template>
  <div>
    <TransactionModalTable :item="item" />
    <h5>Rozliczenia</h5>
    <table class="table table-bordered table-sm">
      <thead>
        <tr>
          <th>Typ</th>
          <th>Budżet</th>
          <th>Nazwa</th>
          <th>Data</th>
          <th>Kwota</th>
          <th>*</th>
        </tr>
      </thead>
      <tbody>
        <TransactionModalForm
          :item="item"
          :budgets="budgets"
          :payment-types="paymentTypes"
        />
        <TransactionModalRow
          v-for="payment in item.payments"
          :key="payment.id"
          :payment="payment"
          @remove="remove"
        />
      </tbody>
    </table>
  </div>
</template>
<script>
  import TransactionModalTable from './TransactionModalTable';
  import TransactionModalForm from './TransactionModalForm';
  import TransactionModalRow from './TransactionModalRow';

  export default {
    components: {TransactionModalTable, TransactionModalForm, TransactionModalRow},
    props: ['item', 'budgets', 'paymentTypes'],
    data () {
      return {
        promiseState: null
      };
    },
    methods: {
      remove (pk) {
          let item = this.item;
          let oldObj = item.payments.find(obj => obj.id === pk);
          item.left = item.left + Number(oldObj.cost);
          item.payments = item.payments.filter(obj => obj.id !== pk);
      }
    }
  }
</script>