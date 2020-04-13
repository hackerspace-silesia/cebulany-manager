<template lang="pug">
  .paymentTypes
    b-table(
        hover, bordered, small, foot-clone
        :items="payments",
        :fields="fields")
      template(slot="name", slot-scope="row")
        span(v-if="!row.item.member") {{ row.value }}
        span(v-else) {{ row.item.member.name }}
      template(slot="budget", slot-scope="row")
        strong(:style="getBgColorStyle(row.value.color)") {{ row.value.name }}
      template(slot="payment_type", slot-scope="row")
        strong(:style="getBgColorStyle(row.value.color)") {{ row.value.name }}
      template(slot="transaction_date", slot-scope="row")
        span {{ row.item.transaction.date }}
      template(slot="transaction_title", slot-scope="row")
        span {{ row.item.transaction.title }}
      template(slot="cost", slot-scope="row")
        span(class="float-right") {{ row.value }} PLN

</template>
<script>
  export default {
    props: ['payments'],
    data () {
      return {
        fields: {
          'name': {label: 'Nazwa / członek'},
          'budget': {label: 'Budżet'},
          'payment_type': {label: 'Typ'},
          'date': {label: 'Data płatności'},
          'transaction_date': {label: 'Data transakcji'},
          'transaction_title': {label: 'Tytuł Transakcji'},
          'cost': {label: 'Kwota'}
        }
      }
    },
    methods: {
      getColor (color) {
        return '#' + color;
      },
      getBgColorStyle (color) {
        return {
          color: this.getColor(color)
        };
      }
    }
  }
</script>
