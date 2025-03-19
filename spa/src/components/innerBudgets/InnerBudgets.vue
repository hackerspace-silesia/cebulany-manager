<template>
  <b-row>
    <b-col>
      <h1>Budżety wewnętrzne</h1>
      <PromisedComponent :state="promiseState">
        <InnerBudgetTable
          :budgets="budgets"
          @row-update="update"
          @row-remove="remove"
        />
      </PromisedComponent>
    </b-col>
  </b-row>
</template>

<script>
import InnerBudgetTable from './InnerBudgetTable'
import linkVm from '@/helpers/linkVm'

import InnerBudgetService from '@/services/innerBudget'

export default {
  components: {
    InnerBudgetTable
  },
  data () {
    return {
      budgets: [],
      promiseState: null
    }
  },
  created () {
    this.fetchInnerBudgets();
  },
  methods: {
    fetchInnerBudgets () {
      linkVm(this, InnerBudgetService.getAll())
        .then((response) => {
          this.budgets = response.data;
        })
    },
    update (data) {
      if (!data.id) {
        InnerBudgetService.post(data).then(obj => {
          this.budgets.push(obj.data);
        });
      } else {
        InnerBudgetService.update(data.id, data);
      }
    },
    remove (data) {
      InnerBudgetService.delete(data.id).then(() => {
        this.budgets = this.budgets.filter(obj => obj.id !== data.id);
      });
    }
  }
}
</script>
