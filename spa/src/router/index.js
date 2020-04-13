import Vue from 'vue';
import Router from 'vue-router';
import Transactions from '@/components/transactions/Transactions';
import Members from '@/components/members/Members';
import Budgets from '@/components/budgets/Budgets';
import PaymentTypes from '@/components/paymentTypes/PaymentTypes';

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
    },
    {
      path: '/budgets',
      name: 'Budgets',
      component: Budgets
    },
    {
      path: '/payment-types',
      name: 'PaymentTypes',
      component: PaymentTypes
    }
  ]
})
