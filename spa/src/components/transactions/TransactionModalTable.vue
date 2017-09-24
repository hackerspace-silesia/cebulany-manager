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
      th: money-value(:value="item.cost")
      th Pozostało do rozliczenia
      td: money-value(:value="item.left")

</template>
<script>
  export default {
    props: ['item']
  }
</script>
