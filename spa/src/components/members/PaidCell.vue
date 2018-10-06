<template lang="pug">
  td(v-if='!sum', :class="notPayedInDate ? 'table-danger' : ''") -
  td(v-else, :class="payedInDate ? 'table-warning' : ''")
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
    changed () {
      let obj = this.paidmonth.months[this.getKey()] || {};
      let key = this.getKey();
      let dt = `${key}-01`;

      this.sum = obj.sum || '';
      this.count = obj.count || 0;
      this.popoverId = `id--${this.member.id}-${key}`;
      this.notPayedInDate = dt <= this.dtNow && this.member.join_date < dt;
      this.payedInDate = dt <= this.dtNow && this.member.join_date > dt;
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
