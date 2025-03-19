<template>
  <PromisedRowComponent :state="promiseState">
    <td
      class="white"
      :style="payment.payment_type | colorCell"
    >
      {{ payment.payment_type.name }}
    </td>
    <td
      class="white"
      :style="payment.budget | colorCell"
    >
      {{ payment.budget.name }}
    </td>
    <td
      class="white"
      :style="payment.inner_budget | colorCell"
    >
      {{ payment.inner_budget.name }}
    </td>
    <td>
      <span v-if="payment.member && payment.member.name">
        {{ payment.member.name }}&nbsp;
      </span>
      <span v-else>{{ payment.name }}</span>
    </td>
    <td>{{ payment.date }}</td>
    <td class="text-right">
      {{ payment.cost }} zł
    </td>
    <td>
      <b-btn
        size="sm"
        variant="danger"
        @click="remove(payment.id)"
      >
        usuń
      </b-btn>
    </td>
  </PromisedRowComponent>
</template>

<script>
  import TypeSelect from '@/components/inputs/TypeSelect';

  import MemberService from '@/services/members'
  import PaymentService from '@/services/payment'
  import linkVm from '@/helpers/linkVm'

  export default {
    components: {TypeSelect},
    props: ['payment'],
    data () {
      return {
        promiseState: null,
      };
    },
    filters: {
      colorCell (obj) {
        return {backgroundColor: `#${obj.color}`};
      }
    },
    methods: {
      remove() {
        const pk = this.payment.id;
        linkVm(this, PaymentService.delete(pk)).then(response => {
          this.$emit("remove", pk);
        });
      }
    }
  }
</script>

<style scoped>
  td.white {color: white;}
</style>