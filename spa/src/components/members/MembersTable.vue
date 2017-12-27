<template lang="pug">
  table.table-sm.table.table-bordered.table-condensed.table-hover.table-members
    thead
      tr
        th(rowspan=2) Członek
        th(v-for="year in years", colspan="12") {{ year }}
      tr
        template(v-for='year in years')
          th.text-center(v-for='month in months') {{ month }}
    tbody
      template(v-for="paidmonth in paidmonths")
        PaidRow(
            :member="members[paidmonth.member_id]", :years="years",
            :months="months", :paidmonth="paidmonth", :dtNow="dtNow",
            @updateMember="updateMemberInTable")
</template>
<script>
  import PaidRow from './PaidRow';

  export default {
    props: ['years', 'members', 'paidmonths', 'updateMember'],
    data () {
      return {
        months: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
        dtNow: (new Date()).toISOString().slice(0, 10)
      }
    },
    methods: {
      updateMemberInTable (data) {
        this.$emit('updateMember', data)
      }
    },
    components: {
      PaidRow
    }
  }
</script>
<style>
 .table-members th,.table-members td {text-align: center; vertical-align: middle !important;}
</style>
<style scoped>
  table { background-color: #fafafa;}
</style>

