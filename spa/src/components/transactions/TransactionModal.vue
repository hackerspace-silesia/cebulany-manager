<template lang="pug">
  div
    TransactionModalTable(:item="item")
    h5 Rozliczenia
    table.table.table-bordered.table-sm
      thead: tr
        th Typ
        th Budżet
        th Nazwa
        th Data
        th Kwota
        th *
      tbody
        TransactionModalForm(:item="item", :budgets="budgets", :paymentTypes="paymentTypes")
        tr(v-for="payment in item.payments")
          td.white(:style="payment.payment_type | colorCell") {{payment.payment_type.name}}
          td.white(:style="payment.budget | colorCell") {{payment.budget.name}}
          td
            span(v-if="payment.member.name") {{payment.member.name}}&nbsp;
            span(v-else) {{payment.name}}
          td {{payment.date}}
          td.text-right {{payment.cost}} zł
          td: PromisedComponent(:state="promiseState")
            b-btn(size="sm" variant="danger", @click="remove(payment.id)") usuń


</template>
<script>
  import TransactionModalTable from './TransactionModalTable';
  import TransactionModalForm from './TransactionModalForm';
  import linkVm from '@/helpers/linkVm';

  import PaymentService from '@/services/payment';

  export default {
    props: ['item', 'budgets', 'paymentTypes'],
    data () {
      return {
        promiseState: null
      }
    },
    components: {TransactionModalTable, TransactionModalForm},
    filters: {
      colorCell (obj) {
        return {backgroundColor: `#${obj.color}`};
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
