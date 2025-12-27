<template>
  <PaymentForm
    ref="parent"
    v-model="payment"
    :budgets="budgets"
    :inner-budgets="innerBudgets"
    :payment-types="paymentTypes"
    @change="update"
  >
    <template v-slot:actions>
      <b-btn
        size="sm"
        variant="danger"
        @click="remove(payment.id)"
      >
        usuń
      </b-btn>
    </template>
  </PaymentForm>
</template>

<script>
  import PaymentForm from './PaymentForm';
  import PaymentService from '@/services/payment'
  import linkVm from '@/helpers/linkVm'
  import Transaction from '@/models/transaction';

  export default {
    components: {PaymentForm},
    props: ['payment', 'transaction', 'budgets', 'innerBudgets', 'paymentTypes'],
    methods: {
      update () {
        let promise = PaymentService.put(this.payment.id, {transaction_id: this.transaction.id, ...this.payment});
        linkVm(this.$refs.parent, promise).then(response => {
          Transaction.computeLeftCost(this.transaction);
        })
      },
      remove() {
        const pk = this.payment.id;
        linkVm(this, PaymentService.delete(pk)).then(response => {
          this.$emit("remove", pk);
        });
      }
    }
  }
</script>
