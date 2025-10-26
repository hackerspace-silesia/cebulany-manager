import Vue from 'vue';
import Router from 'vue-router';
import Transactions from '@/components/transactions/Transactions';
import Members from '@/components/members/Members';
import Budgets from '@/components/budgets/Budgets';
import PaymentTypes from '@/components/paymentTypes/PaymentTypes';
import Payments from '@/components/payments/Payments';
import SummaryPayments from '@/components/summary/SummaryPayments';
import Users from '@/components/users/Users';
import AccountacyTypes from '@/components/accountancyTypes/AccountacyTypes';
import InnerBudgets from '@/components/innerBudgets/InnerBudgets';
import InnerTransfers from '../components/innerTransfers/InnerTransfers.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Transactions',
      component: Transactions
    },
    {
      path: '/transactions/:start/:end',
      name: 'Transactions-Range',
      component: Transactions
    },
    {
      path: '/members',
      name: 'Members',
      component: Members
    },
    {
      path: '/payments',
      name: 'Payments',
      component: Payments
    },
    {
      path: '/budgets',
      name: 'Budgets',
      component: Budgets
    },
    {
      path: '/inner-budgets',
      name: 'InnerBudgets',
      component: InnerBudgets,
    },
    {
      path: '/inner-transfers',
      name: 'InnerTransfers',
      component: InnerTransfers,
    },
    {
      path: '/payment-types',
      name: 'PaymentTypes',
      component: PaymentTypes
    },
    {
      path: '/accountancy-types',
      name: 'AccountancyTypes',
      component: AccountacyTypes,
    },
    {
      path: '/summary',
      name: 'Summary',
      component: SummaryPayments
    },
    {
      path: '/users',
      name: 'Users',
      component: Users
    },
  ]
})
