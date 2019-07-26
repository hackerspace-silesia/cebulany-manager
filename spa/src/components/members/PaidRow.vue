<template lang="pug">
  tr(
      @click="updateMemberInRow",
      :class="!member.is_active ? 'table-active' : ''"
    )
    th(:id="popoverId") {{ member.name }}
    template(v-for='year in years')
      template(v-for='month in months')
        PaidCell(
            :member="member", :year="year", :dtNow="dtNow",
            :paymentTypeId="paymentTypeId",
            :paidmonth="paidmonth", :month="month")
</template>
<script>
  import PaidCell from './PaidCell';
  import MemberForm from './MemberForm';

  export default {
    props: ['years', 'months', 'member', 'paidmonth', 'dtNow', 'updateMember', 'paymentTypeId'],
    data () {
      return {
        popoverId: `id--${this.member.id}--form`
      }
    },
    methods: {
      updateMemberInRow () {
        this.$emit('updateMember', this.member)
      }
    },
    components: {
      PaidCell,
      MemberForm
    }
  }
</script>
