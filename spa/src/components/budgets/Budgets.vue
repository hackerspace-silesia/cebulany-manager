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
