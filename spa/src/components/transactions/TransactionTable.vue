<template>
  <div class="transactions">
    <b-modal
      v-model="showModal"
      title="Transakcja"
      size="xl"
      ok-only="ok-only"
    >
      <TransactionModal
        v-if="showModal"
        :item="modalItem"
        :budgets="budgets"
        :inner-budgets="innerBudgets"
        :payment-types="paymentTypes"
        :sum-left="sumLeft"
      />
    </b-modal>
    <b-table
      hover="hover"
      bordered="bordered"
      small="small"
      foot-clone="foot-clone"
      :items="transactions"
      :fields="fields"
      @row-clicked="rowClicked"
    >
      <template v-slot:cell(name)="row">
        <div v-if="row.item && row.item.name">{{ row.item.name }}</div>
        <div v-if="row.item && row.item.title">{{ row.item.title }}</div>
      </template>
      <template v-slot:cell(cost)="row">
        <money-value :value="row.value" />
      </template>
      <template v-slot:cell(left)="row">
        <money-value :value="row.value" />
      </template>
      <template v-slot:cell(types)="row">
        <ul v-if="row.item.payments.length > 0">
          <li v-for="payment in row.item.payments">
            <type-badge :type="payment.payment_type" />
            <type-badge :type="payment.budget" />
            <type-badge :type="payment.inner_budget" v-if="payment.inner_budget.id" />
          </li>
        </ul>
        <type-badge v-if="row.item.payments.length === 0" :type="{name: '-- BRAK --'}" />
      </template>
      <template v-slot:foot(cost)="row">
        <money-value :value="sum" />
      </template>
      <template v-slot:foot(left)="row">
        <money-value :value="sumLeft" />
      </template>
    </b-table>
  </div>
</template>
<script>
  import TransactionModal from './TransactionModal';
  import TypeBadge from './TypeBadge';

  export default {
    components: {TransactionModal, TypeBadge},
    props: ['transactions', 'sum', 'sumLeft', 'budgets', 'innerBudgets', 'paymentTypes'],
    data () {
      return {
        fields: [
          {key: 'date', label: 'Data', class: 'text-nowrap'},
          {key: 'name', label: 'Nazwa & Tytuł', class: 'transaction-name'},
          {key: 'cost', label: 'Kwota', class: 'text-nowrap text-right'},
          {key: 'left', label: 'Poz.', class: 'text-nowrap text-right'},
          {key: 'types', label: '*', class: 'transaction-payment-types'}
        ],
        showModal: false,
        modalItem: null
      }
    },
    methods: {
      rowClicked (item) {
        this.showModal = true;
        this.modalItem = item;
      }
    }
  }
</script>

<style scoped>
  .transaction-name > div {
    width: 30vw;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
  .transaction-payment-types > ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
  }
  .transaction-payment-types > ul > li {
    display: flex;
  }
  .transaction-payment-types > ul > li:not(:last-child) {
    padding-bottom: 4px;
    margin-bottom: 4px;
    border-bottom: 1px solid #bbb;
  }
</style>
