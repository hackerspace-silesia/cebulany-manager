<template>
  <div class="paymentTypes">
    <b-table
      hover="hover"
      bordered="bordered"
      small="small"
      foot-clone="foot-clone"
      :items="payments"
      :fields="fields"
    >
      <template
        slot="name"
        slot-scope="row"
      >
        <span v-if="!row.item.member">{{ row.value }}</span><span v-else>{{ row.item.member.name }}</span>
      </template><template
        slot="budget"
        slot-scope="row"
      >
        <strong :style="getBgColorStyle(row.value.color)">{{ row.value.name }}</strong>
      </template>
      <template
        slot="payment_type"
        slot-scope="row"
      >
        <strong :style="getBgColorStyle(row.value.color)">{{ row.value.name }}</strong>
      </template><template
        slot="transaction_date"
        slot-scope="row"
      >
        <span>{{ row.item.transaction.date }}</span>
      </template><template
        slot="transaction_title"
        slot-scope="row"
      >
        <span>{{ row.item.transaction.title }}</span>
      </template>
      <template
        slot="cost"
        slot-scope="row"
      >
        <span class="float-right">{{ row.value }} PLN</span>
      </template>
    </b-table>
  </div>
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
