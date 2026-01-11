<template>
  <PaymentForm
    ref="parent"
    v-model="payment"
    :budgets="budgets"
    :inner-budgets="innerBudgets"
    :payment-types="paymentTypes"
    class="table-primary"
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
  import PaymentService from '@/services/payment'
  import linkVm from '@/helpers/linkVm'
  import Transaction from '@/models/transaction';

  export default {
    components: {PaymentForm},
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
      payment.date = this.transaction.date || (new Date()).toISOString().slice(0, 10);
      payment.cost = (this.transaction.left ? Number(this.transaction.left) : 0).toFixed(2);

      return { payment };
    },
    watch: {
      transaction: {
        handler(value) {
          this.payment.cost = (value.left ? Number(value.left) : 0).toFixed(2);
        },
        deep: true,
      },
    },
    methods: {
      addType () {
        const payload = {transaction_id: this.transaction.id, ...this.payment};
        if (!payload.member_id) {
          // During update member_id = 0 creates Integrity error in Sqlalchemy
          // I don't have time to fix this in backend.
          delete payload.member_id;
        }
        let promise = PaymentService.post(payload);

        linkVm(this.$refs.parent, promise).then(response => {
          this.transaction.payments.push(response.data);
          Transaction.computeLeftCost(this.transaction);
        })
      }
    }
  }
</script>
