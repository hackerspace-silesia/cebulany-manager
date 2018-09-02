<template lang="pug">
  td(v-if='!sum', :class="notPayedInDate ? 'table-danger' : ''") -
  td(v-else, :class="PayedInDate ? 'table-warning' : ''")
    span(:id="popoverId") {{ Number(sum).toFixed() }}
      small.text-warning(v-if="count > 1") &nbsp;({{ count }})
    b-popover(
        :target="popoverId", triggers="focus click",
        placement="bottom", @show="getPayments()", @hide="clearPayments()")
      PromisedComponent(:state="promiseState")
        small: ol: li(v-for="payment in payments")
          strong {{ payment.transaction.date }}
          | &nbsp; {{ payment.transaction.title }}
          | &nbsp; {{ payment.cost }} zł

</template>
<script>
  import PaymentService from '@/services/payment';
  import linkVm from '@/helpers/linkVm';
  export default {
    props: ['year', 'month', 'member', 'paidmonth', 'dtNow', 'paymentTypeId'],
    data () {
      return {
        promiseState: null,
        payments: []
      }
    },
    computed: {
      sum () {
        let obj = this.paidmonth.months[this.getKey()] || {};
        return obj.sum || '';
      },
      count () {
        let obj = this.paidmonth.months[this.getKey()] || {};
        return obj.count || 0;
      },
      popoverId () {
        let key = this.getKey();
        return `id--${this.member.id}-${key}`;
      },
      notPayedInDate () {
        let dt = `${this.getKey()}-01`;
        return dt <= this.dtNow && this.member.join_date < dt;
      },
      PayedInDate () {
        let dt = `${this.getKey()}-01`;
        return dt <= this.dtNow && this.member.join_date > dt;
      }

    },
    methods: {
      getKey () {
        return `${this.year}-${this.month}`;
      },
      getPayments () {
        let promise = PaymentService.get({
          member_id: this.member.id,
          payment_type_id: this.paymentTypeId,
          month: this.key
        });
        linkVm(this, promise)
          .then(resp => { this.payments = resp.data; });
      },
      clearPayments () {
        this.payments = [];
      }
    }
  }
</script>
<style>
  .popover {max-width: none;}
</style>
