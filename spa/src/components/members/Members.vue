<template lang="pug">
  b-row: b-col
    PromisedComponent(:state="promiseMemberState")
      b-form(inline)
        b-form-input(v-model="yearStart", type="number")
        b-form-input(v-model="yearEnd", type="number")
    PromisedComponent(:state="promiseState")
      MembersTable(
        :members="members",
        :paidmonths="paidmonths",
        :years="years",
        @updateMember="updateMember")
</template>
<script>
  import MembersTable from './MembersTable';
  import MembersService from '@/services/members';
  import PaidMonthService from '@/services/paidmonth';
  import linkVm from '@/helpers/linkVm';

  export default {
    data () {
      let now = new Date();
      return {
        promiseState: null,
        members: {},
        paidmonths: [],
        yearEnd: now.getFullYear(),
        yearStart: now.getFullYear() - 1
      }
    },
    created () {
      this.getMembers();
    },
    computed: {
      years: (obj) => {
        let years = [];
        let yearEnd = parseInt(obj.yearEnd);
        let yearStart = parseInt(obj.yearStart);
        let range = yearEnd - yearStart;
        for (let i = 0; i <= range; i++) {
          years.push(i + yearStart);
        }
        obj.getPaidMonths(yearStart, yearEnd);
        return years;
      }
    },
    methods: {
      getPaidMonths () {
        linkVm(this, PaidMonthService.getTable())
          .then(resp => { this.paidmonths = resp.data; });
      },
      getMembers () {
        linkVm(this, MembersService.getAll(), 'promiseMemberState')
          .then(resp => {
            this.members = {};
            resp.data.forEach(obj => {
              this.members[obj.id] = obj;
            });
          });
      },
      updateMember (obj) {
        let newMembers = {};
        newMembers[obj.id] = obj;
        this.members = Object.assign({}, this.members, newMembers);
      }
    },
    components: {
      MembersTable
    }
  }
</script>
