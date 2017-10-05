<template lang="pug">
  tr
    td: b-form-select(size="sm", v-model="type", :options="typeOptions")
    td
      template(v-if="type == 'paid_month'")
        b-form-input(
          size="sm", type="month",
          v-model="date", placeholder="miesiąc")
        v-select(
          size="sm", label="name", placeholder="członek",
          :value.sync="member", :on-search="getMembers",
          :options="memberOptions", :debounce="250")
      template(v-else): b-form-input(size="sm" v-model.trim="name")
    td: b-input-group(left="zł", size="sm")
      b-form-input(size="sm", type="number", v-model.trim="cost")
    td: b-btn(size="sm" variant="primary", @click="addType()") dodaj
</template>

<script>
  import MemberService from '@/services/members'
  import PaidMonthService from '@/services/paidmonth'
  import BillService from '@/services/bill'
  import DonationService from '@/services/donation'
  import OtherService from '@/services/other'
  export default {
    props: ['item'],
    data () {
      return {
        type: this.item.proposed_type || 'paid_month',
        cost: this.item.left || 0,
        name: this.item.proposed_type_name || '',
        member: this.item.proposed_member || { id: 0, name: null },
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
      addType () {
        var promise = null;
        console.log(this.date);
        switch (this.type) {
          case 'paid_month': promise = PaidMonthService.post({
            transaction_id: this.item.id,
            member_id: this.member.id,
            date: `${this.date}-01`,
            cost: this.cost
          }); break;
          case 'bill': promise = BillService.post({
            transaction_id: this.item.id,
            name: this.name,
            cost: this.cost
          }); break;
          case 'donation': promise = DonationService.post({
            transaction_id: this.item.id,
            name: this.name,
            cost: this.cost
          }); break;
          case 'other': promise = OtherService.post({
            transaction_id: this.item.id,
            name: this.name,
            cost: this.cost
          }); break;
        }
        promise.then(response => {
          let container = this.containers[this.type];
          this.item.left -= response.data.cost || 0;
          this.item[container].push(response.data);
          this.cost = this.item.left;
        })
      }
    }
  }
</script>
