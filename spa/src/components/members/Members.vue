<template lang="pug">
  b-container
    b-row: b-col
      PromisedComponent(:state="promiseInnerState")
        b-form(inline)
          b-form-group(label="Od")
            b-form-input(v-model="yearStart", type="number")
          b-form-group(label="Do")
            b-form-input(v-model="yearEnd", type="number")
          b-form-group(label="Typ")
            TypeSelect(:types="paymentTypes", v-model="paymentTypeId")
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
          :paymentTypeId="paymentTypeId",
          :years="years",
          :memberFilter="memberFilter",
          @updateMember="updateMember")
</template>
<script>
  import MembersTable from './MembersTable';
  import MemberForm from './MemberForm';
  import TypeSelect from '@/components/inputs/TypeSelect';

  import MembersService from '@/services/members';
  import PaymentService from '@/services/payment';
  import PaymentTypeService from '@/services/paymentType';

  import linkVm from '@/helpers/linkVm';

  export default {
    data () {
      let now = new Date();
      return {
        promiseState: null,
        promiseInnerState: null,
        members: {},
        paidmonths: [],
        paymentTypes: {},
        paymentTypeId: null,
        memberFilter: '',
        showNewMemberForm: false,
        yearEnd: now.getFullYear(),
        yearStart: now.getFullYear() - 1
      }
    },
    created () {
      this.fetchInit();
    },
    computed: {
      years () {
        if (this.paymentTypeId === null) {
          return;
        }
        let years = [];
        let yearEnd = parseInt(this.yearEnd);
        let yearStart = parseInt(this.yearStart);
        let range = yearEnd - yearStart;
        for (let i = 0; i <= range; i++) {
          years.push(i + yearStart);
        }
        this.getPaidMonths(yearStart, yearEnd);
        return years;
      }
    },
    methods: {
      fetchInit () {
        let promises = [
          PaymentTypeService.getAll({has_members: true}),
          MembersService.getAll()
        ];
        linkVm(this, Promise.all(promises), 'promiseInnerState')
          .then(responses => {
            let [paymentTypeResponse, memberResponse] = responses;
            this.paymentTypes = paymentTypeResponse.data;
            let paymentType = this.paymentTypes[0];
            this.paymentTypeId = paymentType ? paymentType.id : null;
            this.members = {};
            memberResponse.data.forEach(member => {
              this.members[member.id] = member;
            });
          })
      },
      getPaidMonths () {
        let promise = PaymentService.getTable({
          payment_type_id: this.paymentTypeId
        });
        linkVm(this, promise)
          .then(resp => { this.paidmonths = resp.data; });
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
      MemberForm,
      TypeSelect
    }
  }
</script>
