<template>
  <tr
    :class="!member.is_active ? 'table-active' : ''"
    @click="updateMemberInRow"
  >
    <th :id="popoverId">
      {{ member.name }}
    </th><template v-for="year in years">
      <template v-for="month in months">
        <PaidCell
          :member="member"
          :year="year"
          :dt-now="dtNow"
          :payment-type-id="paymentTypeId"
          :paidmonth="paidmonth"
          :month="month"
        />
      </template>
    </template>
  </tr>
</template>
<script>
  import PaidCell from './PaidCell';
  import MemberForm from './MemberForm';

  export default {
    components: {
      PaidCell,
      MemberForm
    },
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
    }
  }
</script>
