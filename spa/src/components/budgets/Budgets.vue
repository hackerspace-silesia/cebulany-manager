<template>
  <b-row>
    <b-col>
      <h1>Budżety</h1>
      <PromisedComponent :state="promiseState">
        <BudgetTable
          :budgets="budgets"
          @row-update="update"
          @row-remove="remove"
        />
      </PromisedComponent>
    </b-col>
  </b-row>
</template>

<script>
import BudgetTable from './BudgetTable'
import linkVm from '@/helpers/linkVm'

import BudgetService from '@/services/budget'

export default {
  components: {
    BudgetTable
  },
  data () {
    return {
      budgets: [],
      promiseState: null
    }
  },
  created () {
    this.fetchBudgets();
  },
  methods: {
    fetchBudgets () {
      linkVm(this, BudgetService.getAll())
        .then((response) => {
          this.budgets = response.data;
        })
    },
    update (data) {
      if (!data.id) {
        BudgetService.post(data).then(obj => {
          this.budgets.push(obj.data);
        });
      } else {
        BudgetService.update(data.id, data);
      }
    },
    remove (data) {
      BudgetService.delete(data.id).then(() => {
        this.budgets = this.budgets.filter(obj => obj.id !== data.id);
      });
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
