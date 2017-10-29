import Vue from 'vue'
import Router from 'vue-router'
import Transactions from '@/components/transactions/Transactions'
import GenericTypes from '@/components/genericTypes/GenericTypes'
import Members from '@/components/members/Members'

import BillService from '@/services/bill'
import DonationService from '@/services/donation'
import OtherService from '@/services/other'

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
      path: '/bills',
      name: 'bills',
      component: GenericTypes,
      props: {'service': BillService, 'title': 'Rachunki'}
    },
    {
      path: '/donations',
      name: 'donations',
      component: GenericTypes,
      props: {'service': DonationService, 'title': 'Darowizny'}
    },
    {
      path: '/others',
      name: 'others',
      component: GenericTypes,
      props: {'service': OtherService, 'title': 'Inne płatności'}
    }
  ]
})
