<template lang="pug">
  PromisedRowComponent(:state="promiseState")
    td: b-form-select(size="sm", v-model="type", :options="typeOptions")
    td
      template(v-if="type == 'paid_month'")
        b-form-input(
          size="sm", type="month",
          v-model="date", placeholder="miesiąc")
        v-select(
          size="sm", label="name", placeholder="członek",
          :value="member", :on-search="getMembers",
          :on-change="selectMember",
          :options="memberOptions", :debounce="250")
      template(v-else): b-form-input(size="sm" v-model.trim="name")
    td: b-input-group(left="zł", size="sm")
      b-form-input(size="sm", type="number", v-model.trim="cost")
    td: b-btn(size="sm" variant="primary", @click="addType()") dodaj
</template>

<script>
  import MemberService from '@/services/members'
  import TransactionTypesService from '@/services/transactionTypes';
  import linkVm from '@/helpers/linkVm'

  export default {
    props: ['item'],
    data () {
      var member = null;
      if (this.item.proposed_member && this.item.proposed_member.name) {
        member = this.item.proposed_member;
      }

      return {
        promiseState: null,
        type: this.item.proposed_type || 'paid_month',
        cost: this.item.left || 0,
        name: this.item.proposed_type_name || '',
        member: member,
        memberOptions: [],
        date: (new Date()).toISOString().slice(0, 7),
        typeOptions: {
          paid_month: 'Składka',
          bill: 'Rachunek',
          other: 'Inne',
          donation: 'Dotacja'
        },
        containers: {
          paid_month: 'paidmonths',
          bill: 'bills',
          other: 'others',
          donation: 'donations'
        }
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
        let service = TransactionTypesService.getServiceByType(this.type);
        var promise = null;
        if (this.type === 'paid_month') {
          promise = service.post({
            transaction_id: this.item.id,
            member_id: this.member.id,
            date: this.date,
            cost: this.cost
          });
        } else {
          promise = service.post({
            transaction_id: this.item.id,
            name: this.name,
            cost: this.cost
          });
        }
        linkVm(this, promise).then(response => {
          let container = this.containers[this.type];
          let cost = Number(response.data.cost) || 0;
          this.item.left -= cost;
          this.item[container].push(response.data);
          this.cost = this.item.left;
        })
      }
    }
  }
</script>
