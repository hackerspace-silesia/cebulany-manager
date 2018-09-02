<template lang="pug">
  PromisedRowComponent(:state="promiseState")
    td: TypeSelect(:types="paymentTypes", v-model="paymentTypeId")
    td: TypeSelect(:types="budgets", v-model="budgetId")
    td
      template(v-if="paymentType && paymentType.has_members")
        v-select(
          size="sm", label="name", placeholder="członek",
          :value="member", :on-search="getMembers",
          :on-change="selectMember",
          :options="memberOptions", :debounce="250")
      template(v-else): b-form-input(size="sm" v-model.trim="name")
    td: b-form-input(size="sm", type="date", v-model="date")
    td: b-input-group(right="zł", size="sm")
      b-form-input(size="sm", type="number", v-model.trim="cost")
    td: b-btn(size="sm" variant="primary", @click="addType()") dodaj
</template>

<script>
  import TypeSelect from '@/components/inputs/TypeSelect';

  import MemberService from '@/services/members'
  import PaymentService from '@/services/payment'
  import linkVm from '@/helpers/linkVm'

  export default {
    props: ['item', 'budgets', 'paymentTypes'],
    components: {TypeSelect},
    data () {
      var member = null;
      if (this.item.proposed_member && this.item.proposed_member.name) {
        member = this.item.proposed_member;
      }

      let budgetId = this.item.proposed_budget_id || '0';
      let paymentTypeId = this.item.proposed_type_id || '0';

      return {
        promiseState: null,
        budgetId: budgetId,
        budget: this.budgets[budgetId],
        paymentTypeId: paymentTypeId,
        paymentType: this.paymentTypes[paymentTypeId],
        cost: this.item.left || 0,
        name: this.item.proposed_type_name || '',
        member: member,
        memberOptions: [],
        date: this.item.date || (new Date()).toISOString().slice(0, 10)
      }
    },
    watch: {
      budgetId (value) {
        this.budget = this.budgets[value];
      },
      paymentTypeId (value) {
        this.paymentType = this.paymentTypes[value];
      }
    },
    methods: {
      getMembers (search, loading) {
        loading(true);
        MemberService
          .get({query: search})
          .then(response => {
            this.memberOptions = response.data;
            loading(false);
          })
      },
      selectMember (value) {
        this.member = value;
      },
      addType () {
        let name;
        let memberId;
        if (this.paymentType.has_members) {
          memberId = this.member.id;
          name = '-';
        } else {
          memberId = null;
          name = this.name;
        }

        let promise = PaymentService.post({
          transaction_id: this.item.id,
          member_id: memberId,
          budget_id: this.budgetId,
          payment_type_id: this.paymentTypeId,
          name: name,
          date: this.date,
          cost: this.cost
        });

        linkVm(this, promise).then(response => {
          this.item.left -= Number(response.data.cost) || 0;
          this.item.payments.push(response.data);
          this.cost = this.item.left;
        })
      }
    }
  }
</script>
