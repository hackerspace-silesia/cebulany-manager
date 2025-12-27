<template>
  <div class="paymentTypes">
    <b-table
      hover="hover"
      bordered="bordered"
      small="small"
      foot-clone="foot-clone"
      :items="payments"
      :fields="fields"
      @row-clicked="showTransaction"
    >
      <template v-slot:cell(name)="row">
        <span v-if="!row.item.member">{{ row.value }}</span><span v-else>{{ row.item.member.name }}</span>
      </template>
      <template v-slot:cell(budget)="row">
        <strong :style="getBgColorStyle(row.value.color)">{{ row.value.name }}</strong>
      </template>
      <template v-slot:cell(inner_budget)="row">
        <strong :style="getBgColorStyle(row.value.color)">{{ row.value.name }}</strong>
      </template>
      <template v-slot:cell(payment_type)="row">
        <strong :style="getBgColorStyle(row.value.color)">{{ row.value.name }}</strong>
      </template>
      <template v-slot:cell(transaction_date)="row">
        <span>{{ row.item.transaction.date }}</span>
      </template>
      <template v-slot:cell(transaction_title)="row">
        <span>{{ row.item.transaction.title }}</span>
      </template>
      <template v-slot:cell(cost)="row">
        <money-value class="float-right" :value="row.value" />
      </template>
    </b-table>
  </div>
</template>
<script>
  export default {
    props: ['payments'],
    data () {
      return {
        fields: [
          {key: 'name', label: 'Nazwa / członek'},
          {key: 'budget', label: 'Budżet'},
          {key: 'inner_budget', label: 'Budżet wew.'},
          {key: 'payment_type', label: 'Typ'},
          {key: 'date', label: 'Data płatności'},
          {key: 'transaction_date', label: 'Data transakcji'},
          {key: 'transaction_title', label: 'Tytuł Transakcji'},
          {key: 'cost', label: 'Kwota'},
        ]
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
      },
      showTransaction(item) {
        this.$router.push({
          name: 'TransactionInfo',
          params: {id: item.transaction_id},
        });
      }
    }
  }
</script>
