import Vue from 'vue'
import Router from 'vue-router'
import Transactions from '@/components/transactions/Transactions'

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Transactions',
      component: Transactions
    }
  ]
})
