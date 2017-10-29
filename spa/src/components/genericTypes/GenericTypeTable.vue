<template lang="pug">
  b-table(hover, bordered, :items="items", :fields="fields")
    template(slot="cost" scope="row"): money-value(:value="row.value")
    template(slot="date" scope="row") {{ row.item.transaction.date }}
    template(slot="transactionName" scope="row")
      span(:title="row.item.transaction.name")
        | {{ row.item.transaction.name | truncate(50) }}
</template>

<script>
  export default {
    props: ['items'],
    data () {
      return {
        fields: {
          date: {label: 'Data transakcji', class: 'text-no-wrap'},
          transactionName: {label: 'Nazwa transakcji'},
          name: {label: 'Nazwa Rachunku'},
          cost: {label: 'Kwota', class: 'text-no-wrap text-right'}
        }
      }
    }
  }
</script>
