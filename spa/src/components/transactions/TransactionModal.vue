<template lang="pug">
  div
    TransactionModalTable(:item="item")
    h5 Rozliczenia
    table.table.table-bordered
      thead: tr
        th Typ
        th Nazwa
        th Kwota
        th *
      tbody
        TransactionModalForm(:item="item")
        tr(v-for="bill in item.bills")
          td: span.badge.badge-danger Rachunek
          td {{bill.name}}
          td.text-right {{bill.cost}} zł
          td: PromisedComponent(:state="promiseState"): b-btn(
            size="sm" variant="danger",
            @click="remove('bill', bill.id)") usuń
        tr(v-for="paidmonth in item.paidmonths")
          td: span.badge.badge-primary Składka
          td
            strong {{paidmonth.date.slice(0, 7)}}
            span &nbsp; {{paidmonth.member.name}}
          td.text-right {{paidmonth.cost}} zł
          td: PromisedComponent(:state="promiseState"): b-btn(
            size="sm" variant="danger",
            @click="remove('paid_month', paidmonth.id)") usuń
        tr(v-for="other in item.others")
          td: span.badge.badge-danger Inne
          td {{other.name}}
          td.text-right {{other.cost}} zł
          td: PromisedComponent(:state="promiseState"): b-btn(
            size="sm" variant="danger",
            @click="remove('other', other.id)") usuń
        tr(v-for="donation in item.donations")
          td: span.badge.badge-success Dotacja
          td {{donation.name}}
          td.text-right {{donation.cost}} zł
          td: PromisedComponent(:state="promiseState"): b-btn(
            size="sm" variant="danger",
            @click="remove('donation', donation.id)") usuń


</template>
<script>
  import TransactionModalTable from './TransactionModalTable';
  import TransactionModalForm from './TransactionModalForm';
  import TransactionTypesService from '@/services/transactionTypes';
  import linkVm from '@/helpers/linkVm';

  export default {
    props: ['item'],
    data () {
      return {
        promiseState: null
      }
    },
    components: {TransactionModalTable, TransactionModalForm},
    methods: {
      remove (type, pk) {
        let service = TransactionTypesService.getServiceByType(type);
        if (service === null) {
          return;
        }
        linkVm(this, service.delete(pk)).then(response => {
          var container = null;
          switch (type) {
            case 'paid_month': container = 'paidmonths'; break;
            case 'bill': container = 'bills'; break;
            case 'donation': container = 'donations'; break;
            case 'other': container = 'others'; break;
            default: container = null;
          }
          let item = this.item;
          let oldObj = item[container].find(obj => obj.id === pk);
          let cost = Number(oldObj.cost);
          item.left += cost;
          item[container] = item[container].filter(obj => obj.id !== pk);
        });
      }
    }
  }
</script>
