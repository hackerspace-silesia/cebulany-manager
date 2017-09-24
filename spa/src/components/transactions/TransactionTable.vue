<template lang="pug">
  .transactions
    b-modal(v-model="showModal", ok-only, title="Transakcja" size="lg")
      TransactionModal(v-if='showModal', :item="modalItem")
    b-table(
        hover, bordered, small,
        @row-clicked.captured="rowClicked",
        :items="transactions",
        :fields="fields")
      template(slot="name", scope="row")
        span(:title="row.value") {{ row.value | truncate(50) }}
      template(slot="title", scope="row")
        span(:title="row.value") {{ row.value | truncate(50) }}
      template(slot="cost", scope="row")
        span.text-danger(v-if="row.value < 0") {{ row.value }} zł
        span(v-else) {{ row.value }} zł
      template(slot="left", scope="row") {{ computeLeftCost(row.item) }} zł
      template(slot="types", scope="row")
        span(v-for="donation in row.item.donations")
          span.badge.badge-success(:title="donation | type_basic_title") D
        span(v-for="bill in row.item.bills")
          span.badge.badge-danger(:title="bill | type_basic_title") R
        span(v-for="paidmonth in row.item.paidmonths")
          span.badge.badge-primary(:title="paidmonth | type_paid_title") S
        span(v-for="other in row.item.others")
          span.badge.badge-secondary(:title="other | type_basic_title") O

</template>
<script>
  import Transaction from '@/models/transaction';
  import TransactionModal from './TransactionModal';

  export default {
    props: ['transactions'],
    components: {TransactionModal},
    data () {
      return {
        fields: {
          'date': {label: 'Data', class: 'text-no-wrap'},
          'name': {label: 'Nazwa'},
          'title': {label: 'Tytuł'},
          'cost': {label: 'Kwota', class: 'text-no-wrap text-right'},
          'left': {label: 'Poz.', class: 'text-no-wrap text-right'},
          'types': {label: '*'}
        },
        showModal: false,
        modalItem: null
      }
    },
    methods: {
      computeLeftCost: Transaction.computeLeftCost,
      rowClicked (item) {
        this.showModal = true;
        this.modalItem = item;
      }
    },
    filters: {
      type_basic_title (obj) {
        return `${obj.name}\n${obj.cost} zł`;
      },
      type_paid_title (obj) {
        return `${obj.member.name}\n${obj.date}\n${obj.cost} zł`;
      }
    }
  }
</script>

<style>
  .table-sm td { font-size: 8pt; }
  .table-sm th { font-size: 8pt; }
</style>
