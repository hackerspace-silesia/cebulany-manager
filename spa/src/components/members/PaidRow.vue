<template lang="pug">
  tr(:class="!member.is_active ? 'table-active' : ''")
    th {{ member.name }}
    template(v-for='year in years')
      template(v-for='month in months')
        PaidCell(
            :member="member", :year="year", :dtNow="dtNow",
            :paidmonth="paidmonth", :month="month")
</template>
<script>
  import PaidCell from './PaidCell';

  export default {
    props: ['years', 'months', 'member', 'paidmonth', 'dtNow'],
    components: {
      PaidCell
    }
  }
</script>
