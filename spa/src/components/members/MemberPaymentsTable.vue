<template lang="pug">
  PromisedComponent(:state="promiseState")
    .content: table.table.table-bordered.table-sm
      thead: tr
        th Budżet
        th Nazwa
        th Data płatności
        th Data transakcji
        th Kwota
      tbody
        template(v-for="transaction in transactions")
          tr(v-for="payment in transaction.payments", :key="`${transaction.id}-${payment.id}`")
            td.white(:style="payment.budget | colorCell") {{payment.budget.name}}
            td {{transaction.title}}
            td {{payment.date}}
            td {{transaction.date}}
            td.text-right {{payment.cost}} zł

</template>
<script>
  import linkVm from '@/helpers/linkVm'
  import TransactionService from '@/services/transactions'

  export default {
    props: ['member'],
    data () {
      return {
        promiseState: null,
        transactions: []
      }
    },
    filters: {
      colorCell (obj) {
        return {backgroundColor: `#${obj.color}`};
      }
    },
    watch: {
      member: {
        immediate: true,
        handler (value) {
          this.fetchTransactions(value);
        }
      }
    },
    methods: {
      fetchTransactions (member) {
        if (member === null) {
          this.transactions = [];
          return;
        }

        const params = {
          member_id: this.member.id
        };
        linkVm(this, TransactionService.get(params))
          .then(resp => {
            this.transactions = resp.data.transactions;
          })
      }
    }
  }
</script>

<style scoped>
  td.white {color: white;}
  .content {
    max-height: 400px;
    overflow-y: auto;
  }
</style>
