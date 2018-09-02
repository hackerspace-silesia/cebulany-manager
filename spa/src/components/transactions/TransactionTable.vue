<template lang="pug">
  .transactions
    b-modal(v-model="showModal", title="Transakcja", size="lg", ok-only)
      TransactionModal(
        v-if='showModal',
        :item="modalItem",
        :budgets="budgets",
        :paymentTypes="paymentTypes",
        :sumLeft="sumLeft")
    b-table(
        hover, bordered, small, foot-clone
        @row-clicked.captured="rowClicked",
        :items="transactions",
        :fields="fields")
      template(slot="name", slot-scope="row")
        span(:title="row.value") {{ row.value | truncate(50) }}
      template(slot="title", slot-scope="row")
        span(:title="row.value") {{ row.value | truncate(50) }}
      template(slot="cost", slot-scope="row"): money-value(:value="row.value")
      template(slot="left", slot-scope="row"): money-value(:value="row.value")
      template(slot="types", slot-scope="row")
        span(v-for="payment in row.item.payments")
          span.transaction-badge(
            :title="payment | paymentTitle",
            :style="payment | paymentStyle") {{payment | paymentName}}
      template(slot="FOOT_cost" slot-scope="row"): money-value(:value="sum")
      template(slot="FOOT_left" slot-scope="row"): money-value(:value="sumLeft")

</template>
<script>
  import TransactionModal from './TransactionModal';

  export default {
    props: ['transactions', 'sum', 'sumLeft', 'budgets', 'paymentTypes'],
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
      rowClicked (item) {
        this.showModal = true;
        this.modalItem = item;
      }
    },
    filters: {
      paymentStyle (payment) {
        return {
          backgroundColor: `#${payment.payment_type.color}`,
          borderColor: `#${payment.budget.color}`
        };
      },
      paymentTitle (payment) {
        return payment.payment_type.name;
      },
      paymentName (payment) {
        let name = payment.payment_type.name;
        return name ? name.charAt(0).toUpperCase() : '?';
      }
    }
  }
</script>
