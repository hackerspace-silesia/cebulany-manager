<template lang="pug">
  td(v-if='!sum', :class="notPayedInDate ? 'table-danger' : ''") -
  td(v-else, :class="PayedInDate ? 'table-warning' : ''")
    span(:id="popoverId") {{ Number(sum).toFixed() }}
      small.text-warning(v-if="count > 1") &nbsp;({{ count }})
    b-popover(
        :target="popoverId", triggers="click",
        placement="bottom", @show="getTransactions()", @hide="clearTransactions()")
      PromisedComponent(:state="promiseState")
        small: ol: li(v-for="transaction in transactions")
          strong {{ transaction.transaction.date }}
          | &nbsp; {{ transaction.transaction.title }}
          | &nbsp; {{ transaction.cost }} zł

</template>
<script>
  import PaidMonthService from '@/services/paidmonth';
  import linkVm from '@/helpers/linkVm';
  export default {
    props: ['year', 'month', 'member', 'paidmonth', 'dtNow'],
    data () {
      let key = `${this.year}-${this.month}`;
      let dt = `${key}-01`;
      let obj = this.paidmonth.months[key] || {};
      return {
        promiseState: null,
        sum: obj.sum || null,
        count: obj.count || 0,
        notPayedInDate: dt <= this.dtNow && this.member.join_date < dt,
        PayedInDate: dt <= this.dtNow && this.member.join_date > dt,
        popoverId: `id--${this.member.id}-${key}`,
        key: key,
        transactions: []
      }
    },
    methods: {
      getTransactions () {
        let params = {member_id: this.member.id, month: this.key};
        linkVm(this, PaidMonthService.get(params))
          .then(resp => { this.transactions = resp.data; });
      },
      clearTransactions () {
        this.transactions = [];
      }
    }
  }
</script>
<style>
  .popover {max-width: none;}
</style>
