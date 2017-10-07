import Vue from 'vue'
import Router from 'vue-router'
import Transactions from '@/components/transactions/Transactions'
import Members from '@/components/members/Members'

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Transactions',
      component: Transactions
    },
    {
      path: '/members',
      name: 'Members',
      component: Members
    }
  ]
})
