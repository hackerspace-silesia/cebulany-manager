<template lang="pug">
  b-row
    b-col
      h1 Budżety
      PromisedComponent(:state="promiseState")
        BudgetTable(
          :budgets="budgets"
          @row-update="update",
        )
</template>

<script>
import BudgetTable from './BudgetTable'
import linkVm from '@/helpers/linkVm'

import BudgetService from '@/services/budget'

export default {
  data () {
    return {
      budgets: [],
      sum: 0,
      sumLeft: 0,
      promiseState: null
    }
  },
  components: {
    BudgetTable
  },
  created () {
    this.fetchBudgets();
  },
  methods: {
    transformArrayToMap (array) {
      let obj = {};
      array.forEach((item) => {
        obj[`${item.id}`] = item;
      });
      return obj;
    },
    fetchBudgets () {
      linkVm(this, BudgetService.getAll())
        .then((response) => {
          this.budgets = response.data;
        })
    },
    update (data) {
      console.log(data);
      BudgetService.update(data.id, data)
        .then((response) => {
          console.info('Budget updated');
        })
    }
  }
}
</script>

<style>
  .budget-badge {
    display: inline-block;
    text-align: center;
    width: 16px;
    margin: 0 1px;
    border-radius: 4px;
    color: white;
    font-size: 7pt;
    font-weight: bold;
    border: solid black;
    border-width: 3px;
  }
  .budget-badge-big {
    width: 18px;
    font-size: 9pt;
    border-radius: 8px;
  }
</style>
