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
      tr
        td: b-dropdown(size="sm", text="Wybierz...")
          b-dropdown-item Składka
          b-dropdown-item Rachunek
          b-dropdown-item Dotacja
          b-dropdown-item Inne
        td: b-form-input(size="sm")
        td: b-form-input(size="sm", type="number")
        td: b-btn(size="sm" variant="primary") dodaj

      tr(v-for="bill in item.bills")
        td: span.badge.badge-danger Rachunek
        td {{bill.name}}
        td.text-right {{bill.cost}} zł
        td: b-btn(size="sm" variant="danger") usuń
      tr(v-for="paidmonth in item.paidmonths")
        td: span.badge.badge-primary Składka
        td
          strong {{paidmonth.date}}
          span &nbsp; (Członek {{paidmonth.member.name}})
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
  import Transaction from '@/models/transaction';
  import TransactionModalTable from './TransactionModalTable';
  export default {
    props: ['item'],
    components: {TransactionModalTable},
    methods: {
      computeLeftCost: Transaction.computeLeftCost
    }
  }
</script>
