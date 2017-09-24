<template lang="pug">
  table.table.table-bordered.table-sm
    tr
      th Nazwa
      td(colspan="3") {{ item.name }}
    tr
      th Tytuł
      td(colspan="3") {{ item.title }}
    tr
      th IBAN
      td {{ item.iban }}
      th Data
      td {{ item.date }}
    tr
      th Kwota
      th
        span.text-danger(v-if="item.cost < 0") {{ item.cost }} zł
        span(v-else) {{ item.cost }} zł
      th Pozostało do rozliczenia
      td {{ computeLeftCost(item) }} zł

</template>
<script>
  import Transaction from '@/models/transaction';
  export default {
    props: ['item'],
    methods: {
      computeLeftCost: Transaction.computeLeftCost
    }
  }
</script>
