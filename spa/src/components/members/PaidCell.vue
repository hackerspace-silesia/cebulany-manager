<template lang="pug">
  td(v-if='!sum', :class="notPaidInDate ? 'table-danger' : ''") -
  td(v-else, :class="PaidInDate ? 'table-warning' : ''")
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
      key () {
        return `${this.year}-${this.month}`;
      },
      keyDate () {
        return `${this.key}-01`;
      },
      sum () {
        let obj = this.paidmonth.months[this.key] || {};
        return obj.sum || '';
      },
      count () {
        let obj = this.paidmonth.months[this.key] || {};
        return obj.count || 0;
      },
      popoverId () {
        return `id--${this.member.id}-${this.key}`;
      },
      notPaidInDate () {
        let dt = this.keyDate;
        return dt <= this.dtNow && this.member.join_date < dt;
      },
      PaidInDate () {
        let dt = this.keyDate;
        return dt <= this.dtNow && this.member.join_date > dt;
      }

    },
    methods: {
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
