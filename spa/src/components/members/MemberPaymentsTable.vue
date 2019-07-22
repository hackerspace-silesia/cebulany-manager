<template lang="pug">
  PromisedComponent(:state="promiseState")
    div.block
      table.table.table-bordered.table-sm
        thead: tr
          th Budżet
          th Nazwa
          th Data płatności
          th Data transakcji
          th Kwota
        tbody(v-for="transaction in transactions", :key="transaction.id")
          tr(v-for="payment in transaction.payments", :key="payment.id")
            td.white(:style="payment.budget | colorCell") {{payment.budget.name}}
            td {{transaction.title}}
            td {{payment.date | onlyDate }}
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
      },
      onlyDate (value) {
        return value.substr(0, 7);
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
            console.log(this.transactions);
          })
      }
    }
  }
</script>

<style scoped>
  td.white {color: white;}
  .block { max-height: 400px; overflow-y: auto;}
</style>
