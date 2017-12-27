<template lang="pug">
  tr(:class="!member.is_active ? 'table-active' : ''")
    th(:id="popoverId") {{ member.name }}
    b-popover(
        :target="popoverId", triggers="blur click",
        placement="bottom")
      MemberForm(:member="member")


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
    props: ['years', 'months', 'member', 'paidmonth', 'dtNow'],
    data () {
      return {
        popoverId: `id--${this.member.id}--form`
      }
    },
    components: {
      PaidCell,
      MemberForm
    }
  }
</script>
