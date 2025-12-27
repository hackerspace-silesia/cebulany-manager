<template>
  <PaymentForm
    ref="parent"
    v-model="payment"
    :transaction="transaction"
    :budgets="budgets"
    :inner-budgets="innerBudgets"
    :payment-types="paymentTypes"
  >
    <template v-slot:actions>
      <b-btn
        size="sm"
        variant="primary"
        @click="addType()"
      >
        dodaj
      </b-btn>
    </template>
  </PaymentForm>
</template>

<script>
  import PaymentForm from './PaymentForm';
  import TypeSelect from '@/components/inputs/TypeSelect';
  import PaymentService from '@/services/payment'
  import linkVm from '@/helpers/linkVm'
  import Transaction from '@/models/transaction';

  export default {
    components: {PaymentForm, TypeSelect},
    props: ['transaction', 'budgets', 'innerBudgets', 'paymentTypes'],
    data () {
      const payment = this.transaction.suggestion !== null ? structuredClone(this.transaction.suggestion) : {
        budget_id: 0,
        inner_budget_id: 0,
        payment_type_id: 0,
        member_id: 0,
        member: null,
        name: '-',
      };
      payment.transaction_id = this.transaction.id;
      payment.date = this.transaction.date || (new Date()).toISOString().slice(0, 10);
      payment.cost = (this.transaction.left ? Number(this.transaction.left) : 0).toFixed(2);

      return { payment };
    },
    methods: {
      addType () {
        let promise = PaymentService.post(this.payment);

        linkVm(this.$refs.parent, promise).then(response => {
          this.transaction.payments.push(response.data);
          this.payment.cost = Transaction.computeLeftCost(this.transaction);
        })
      }
    }
  }
</script>
