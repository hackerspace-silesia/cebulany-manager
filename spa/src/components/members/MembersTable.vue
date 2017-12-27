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
      template(v-for="o in memberList")
        PaidRow(
            v-if="o.filtered", :member="o.member", :years="years",
            :months="months", :paidmonth="o.paidmonth", :dtNow="dtNow",
            @updateMember="updateMemberInTable")
</template>
<script>
  //
  import PaidRow from './PaidRow';

  export default {
    props: ['years', 'members', 'paidmonths', 'updateMember', 'memberFilter'],
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
    computed: {
      memberList () {
        let members = this.members;
        let memberFilter = this.memberFilter.toLowerCase();
        return this.paidmonths.map(paidmonth => {
          let member = members[paidmonth.member_id];
          let name = member.name.toLowerCase();
          return {
            member: member,
            paidmonth: paidmonth,
            filtered: name.indexOf(memberFilter) !== -1
          };
        })
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

