<template lang="pug">
  div
    TransactionModalTable(:item="item")
    h5 Rozliczenia
    table.table.table-bordered
      tr
        th Typ
        th Nazwa
        th Kwota
        th *
      TransactionModalForm(:item="item")
      tr(v-for="bill in item.bills")
        td: span.badge.badge-danger Rachunek
        td {{bill.name}}
        td.text-right {{bill.cost}} zł
        td: b-btn(size="sm" variant="danger") usuń
      tr(v-for="paidmonth in item.paidmonths")
        td: span.badge.badge-primary Składka
        td
          strong {{paidmonth.date.slice(0, 7)}}
          span &nbsp; {{paidmonth.member.name}}
        td.text-right {{paidmonth.cost}} zł
        td: b-btn(size="sm" variant="danger") usuń
      tr(v-for="other in item.others")
        td: span.badge.badge-danger Inne
        td {{other.name}}
        td.text-right {{other.cost}} zł
        td: b-btn(size="sm" variant="danger") usuń
      tr(v-for="donation in item.donations")
        td: span.badge.badge-success Dotacja
        td {{donation.name}}
        td.text-right {{donation.cost}} zł
        td: b-btn(size="sm" variant="danger") usuń


</template>
<script>
  import TransactionModalTable from './TransactionModalTable';
  import TransactionModalForm from './TransactionModalForm';
  export default {
    props: ['item'],
    components: {TransactionModalTable, TransactionModalForm}
  }
</script>
