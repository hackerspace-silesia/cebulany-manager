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
      @row-clicked.captured="rowClicked"
    >
      <template
        slot="name"
        slot-scope="row"
      >
        <span :title="row.value">{{ row.value | truncate(50) }}</span>
      </template><template
        slot="title"
        slot-scope="row"
      >
        <span :title="row.value">{{ row.value | truncate(50) }}</span>
      </template><template
        slot="cost"
        slot-scope="row"
      >
        <money-value :value="row.value" />
      </template><template
        slot="left"
        slot-scope="row"
      >
        <money-value :value="row.value" />
      </template><template
        slot="types"
        slot-scope="row"
      >
        <span v-for="payment in row.item.payments"><span
          class="transaction-badge"
          :title="payment | paymentTitle"
          :style="payment | paymentStyle"
        >{{ payment | paymentName }}</span></span>
      </template>
      <template
        slot="FOOT_cost"
        slot-scope="row"
      >
        <money-value :value="sum" />
      </template><template
        slot="FOOT_left"
        slot-scope="row"
      >
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
    }
  }
</script>
