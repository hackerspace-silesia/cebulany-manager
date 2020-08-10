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
        <tr
          v-for="payment in item.payments"
          :key="payment.id"
        >
          <td
            class="white"
            :style="payment.payment_type | colorCell"
          >
            {{ payment.payment_type.name }}
          </td>
          <td
            class="white"
            :style="payment.budget | colorCell"
          >
            {{ payment.budget.name }}
          </td>
          <td><span v-if="payment.member && payment.member.name">{{ payment.member.name }}&nbsp;</span><span v-else>{{ payment.name }}</span></td>
          <td>{{ payment.date }}</td>
          <td class="text-right">
            {{ payment.cost }} zł
          </td>
          <td>
            <PromisedComponent :state="promiseState">
              <b-btn
                size="sm"
                variant="danger"
                @click="remove(payment.id)"
              >
                usuń
              </b-btn>
            </PromisedComponent>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script>
  import TransactionModalTable from './TransactionModalTable';
  import TransactionModalForm from './TransactionModalForm';
  import linkVm from '@/helpers/linkVm';

  import PaymentService from '@/services/payment';

  export default {
    components: {TransactionModalTable, TransactionModalForm},
    filters: {
      colorCell (obj) {
        return {backgroundColor: `#${obj.color}`};
      }
    },
    props: ['item', 'budgets', 'paymentTypes'],
    data () {
      return {
        promiseState: null
      }
    },
    methods: {
      remove (pk) {
        linkVm(this, PaymentService.delete(pk)).then(response => {
          let item = this.item;
          let oldObj = item.payments.find(obj => obj.id === pk);
          item.left += Number(oldObj.cost);
          item.payments = item.payments.filter(obj => obj.id !== pk);
        });
      }
    }
  }
</script>

<style scoped>
  td.white {color: white;}
</style>
