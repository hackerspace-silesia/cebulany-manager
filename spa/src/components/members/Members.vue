<template lang="pug">
  b-container
    b-row: b-col
      PromisedComponent(:state="promiseMemberState")
        b-form(inline)
          b-form-group(label="Od")
            b-form-input(v-model="yearStart", type="number")
          b-form-group(label="Do")
            b-form-input(v-model="yearEnd", type="number")
          b-form-group(label="Szukaj")
            b-form-input(
              v-model.trim="memberFilter", type="text",
              placeholder="Szukaj...")
          b-form-group(label="*")
            b-button(id="new-member-form", variant="primary") Dodaj
            b-popover(
                target="new-member-form",
                triggers="focus click",
                placement="bottom",
                title="Dodaj nowego członka",
                :show.sync="showNewMemberForm")
              MemberForm(@update="createNewMember", is-new)
    br
    b-row: b-col
      PromisedComponent(:state="promiseState")
        MembersTable(
          :members="members",
          :paidmonths="paidmonths",
          :years="years",
          :memberFilter="memberFilter",
          @updateMember="updateMember")
</template>
<script>
  import MembersTable from './MembersTable';
  import MemberForm from './MemberForm';
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
        memberFilter: '',
        showNewMemberForm: false,
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
      },
      createNewMember (obj) {
        this.updateMember(obj);
        this.getPaidMonths();
        this.showNewMemberForm = false;
      }
    },
    components: {
      MembersTable,
      MemberForm
    }
  }
</script>
