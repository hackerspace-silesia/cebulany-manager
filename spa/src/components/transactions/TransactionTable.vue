<template lang="pug">
  b-table(class="transactions", hover, bordered, small, :items="transactions", :fields="fields")
    template(slot="name", scope="row")
      span(:title="row.value") {{ row.value | truncate(50) }}
    template(slot="title", scope="row")
      span(:title="row.value") {{ row.value | truncate(50) }}
    template(slot="cost", scope="row") {{ row.value }} zł
    template(slot="left", scope="row") {{ computeLeftCost(row.item) }} zł
    template(slot="types", scope="row")
      span(v-for="donation in row.item.donations")
        span.badge.badge-success(:title="donation | type_basic_title") D
      span(v-for="bill in row.item.bills")
        span.badge.badge-danger(:title="bill | type_basic_title") R
      span(v-for="paidmonth in row.item.paidmonths")
        span.badge.badge-primary(:title="paidmonth | type_paid_title") S
      span(v-for="other in row.item.others")
        span.badge.badge-secondary(:title="other | type_basic_title") O

</template>
<script>
  import Transaction from '@/models/transaction.js';
  export default {
    props: ['transactions'],
    data () {
      return {
        fields: {
          'date': {label: 'Data', class: 'no-wrap'},
          'name': {label: 'Nazwa'},
          'title': {label: 'Tytuł'},
          'cost': {label: 'Kwota', class: 'no-wrap'},
          'left': {label: 'Poz.', class: 'no-wrap'},
          'types': {label: '*'}
        }
      }
    },
    methods: {
      computeLeftCost: Transaction.computeLeftCost
    },
    filters: {
      type_basic_title (obj) {
        return `${obj.name}\n${obj.cost} zł`;
      },
      type_paid_title (obj) {
        return `${obj.member.name}\n${obj.date}\n${obj.cost} zł`;
      }
    }
  }
</script>

<style>
  .transactions td { font-size: 8pt; }
  .transactions td.no-wrap { white-space: nowrap; }
</style>
