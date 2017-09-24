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
    td: b-form-input(size="sm", type="number", v-model.trim="cost")
    td: b-btn(size="sm" variant="primary", @on-click="addType()") dodaj
</template>

<script>
  import MemberService from '@/services/members'
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
      }
    }
  }
</script>
