<template>
  <div class="transactions">
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
      <template v-slot:cell(attachments)="row">
        <ul>
          <li v-for="attachment in row.item.attachments">
            <attachment-badge :document="attachment.document" />
          </li>
        </ul>
      </template>
      <template v-slot:cell(types)="row">
        <ul v-if="row.item.payments.length > 0">
          <li v-for="payment in row.item.payments">
            <type-badge :type="payment.payment_type" />
            <type-badge :type="payment.budget" />
            <type-badge :type="payment.inner_budget" />
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
  import TypeBadge from './TypeBadge';
  import AttachmentBadge from './AttachmentBadge';

  export default {
    components: {TypeBadge, AttachmentBadge},
    props: ['transactions', 'sum', 'sumLeft', 'budgets', 'innerBudgets', 'paymentTypes'],
    data () {
      return {
        fields: [
          {key: 'date', label: 'Data', class: 'text-nowrap'},
          {key: 'name', label: 'Nazwa & Tytuł', class: 'transaction-name'},
          {key: 'cost', label: 'Kwota', class: 'text-nowrap text-right'},
          {key: 'left', label: 'Poz.', class: 'text-nowrap text-right'},
          {key: 'attachments', label: '*', class: 'badges'},
          {key: 'types', label: '*', class: 'badges'}
        ],
      }
    },
    methods: {
      rowClicked (item) {
        this.$router.push({
          name: 'TransactionInfo',
          params: {id: item.id},
        });
      }
    }
  }
</script>

<style scoped>
  .transaction-name > div {
    width: 60vw;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
  .badges > ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
  }
  .badges > ul > li {
    display: flex;
  }
  .badges > ul > li:not(:last-child) {
    padding-bottom: 4px;
    margin-bottom: 4px;
    border-bottom: 1px solid #bbb;
  }
</style>
