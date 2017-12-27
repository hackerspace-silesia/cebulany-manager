<template lang="pug">
  tr(:class="!member.is_active ? 'table-active' : ''")
    th(:id="popoverId") {{ member.name }}
    b-popover(
        title="Zaaktulizuj dane",
        :target="popoverId", triggers="focus click",
        placement="bottom")
      MemberForm(:member="member", @update="updateMemberInRow")
    template(v-for='year in years')
      template(v-for='month in months')
        PaidCell(
            :member="member", :year="year", :dtNow="dtNow",
            :paidmonth="paidmonth", :month="month")
</template>
<script>
  import PaidCell from './PaidCell';
  import MemberForm from './MemberForm';

  export default {
    props: ['years', 'months', 'member', 'paidmonth', 'dtNow', 'updateMember'],
    data () {
      return {
        popoverId: `id--${this.member.id}--form`
      }
    },
    methods: {
      updateMemberInRow (data) {
        this.$emit('updateMember', data)
      }
    },
    components: {
      PaidCell,
      MemberForm
    }
  }
</script>
