<template>
  <div class="transactions">
    <b-modal
      v-model="showModal"
      title="Transakcja"
      size="lg"
      ok-only="ok-only"
    >
      <TransactionModal
        v-if="showModal"
        :item="modalItem"
        :budgets="budgets"
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
        <span :title="row.value">{{ row.value | truncate(50) }}</span>
      </template>
      <template v-slot:cell(title)="row">
        <span :title="row.value">{{ row.value | truncate(50) }}</span>
      </template>
      <template v-slot:cell(cost)="row">
        <money-value :value="row.value" />
      </template>
      <template v-slot:cell(left)="row">
        <money-value :value="row.value" />
      </template>
      <template v-slot:cell(types)="row">
        <span v-for="payment in row.item.payments"><span
          class="transaction-badge"
          :title="payment | paymentTitle"
          :style="payment | paymentStyle"
        >{{ payment | paymentName }}</span></span>
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

  export default {
    components: {TransactionModal},
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
    },
    props: ['transactions', 'sum', 'sumLeft', 'budgets', 'paymentTypes'],
    data () {
      return {
        fields: [
          {key: 'date', label: 'Data', class: 'text-no-wrap'},
          {key: 'name', label: 'Nazwa'},
          {key: 'title', label: 'Tytuł'},
          {key: 'cost', label: 'Kwota', class: 'text-no-wrap text-right'},
          {key: 'left', label: 'Poz.', class: 'text-no-wrap text-right'},
          {key: 'types', label: '*'}
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
