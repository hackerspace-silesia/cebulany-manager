<template>
  <div>
    <h2>Transfery</h2>
    <b-table
      hover="hover"
      bordered="bordered"
      small="small"
      :items="innerTransfers"
      :fields="fields"
    >
      <template v-slot:cell(budget)="row">
        <strong :style="getBgColorStyle(row.value.color)">{{ row.value.name }}</strong>
      </template>
      <template v-slot:cell(from_inner_budget)="row">
        <strong :style="getBgColorStyle(row.value.color)">{{ row.value.name }}</strong>
      </template>
      <template v-slot:cell(to_inner_budget)="row">
        <strong :style="getBgColorStyle(row.value.color)">{{ row.value.name }}</strong>
      </template>
      <template v-slot:cell(cost)="row">
        <money-value  class="float-right" :value="row.value" />
      </template>
    </b-table>
  </div>
</template>
<script>
  export default {
    props: ['innerTransfers', 'innerBudgets', 'budgets'],
    data () {
      return {
        fields: [
          {key: 'date', label: 'Data'},
          {key: 'budget', label: 'Budżet'},
          {key: 'from_inner_budget', label: 'Od'},
          {key: 'to_inner_budget', label: 'Do'},
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
          color: this.getColor(color),
        };
      }
    }
  }
</script>
