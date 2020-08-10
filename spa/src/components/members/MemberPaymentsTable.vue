<template>
  <PromisedComponent :state="promiseState">
    <div class="content">
      <table class="table table-bordered table-sm">
        <thead>
          <tr>
            <th>Budżet</th>
            <th>Nazwa</th>
            <th>Data płatności</th>
            <th>Data transakcji</th>
            <th>Kwota</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="transaction in transactions">
            <tr
              v-for="payment in transaction.payments"
              :key="`${transaction.id}-${payment.id}`"
            >
              <td
                class="white"
                :style="payment.budget | colorCell"
              >
                {{ payment.budget.name }}
              </td><td>{{ transaction.title }}</td><td>{{ payment.date }}</td><td>{{ transaction.date }}</td><td class="text-right">
                {{ payment.cost }} zł
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </PromisedComponent>
</template>
<script>
  import linkVm from '@/helpers/linkVm'
  import TransactionService from '@/services/transactions'

  export default {
    filters: {
      colorCell (obj) {
        return {backgroundColor: `#${obj.color}`};
      }
    },
    props: ['member'],
    data () {
      return {
        promiseState: null,
        transactions: []
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
