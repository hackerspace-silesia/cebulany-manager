<template lang="pug">
  tr
    td: b-form-select(size="sm", v-model="type", :options="typeOptions")
    td
      template(v-if="type == 'paid_month'")
        b-form-input(size="sm", type="month", v-model="date")
        b-form-input(size="sm", v-model="member.name")
      template(v-else): b-form-input(size="sm" v-model.trim="name")
    td: b-form-input(size="sm", type="number", v-model.trim="cost")
    td: b-btn(size="sm" variant="primary") dodaj
</template>

<script>
  export default {
    props: ['item'],
    data () {
      let date = new Date();
      let month = `${date.getFullYear()}-${date.getUTCMonth()}`;
      return {
        type: this.item.proposed_type || 'paid_month',
        cost: this.item.left || 0,
        name: this.item.proposed_type_name || '',
        member: this.item.proposed_member || { id: 0, name: null },
        date: month,
        typeOptions: {
          paid_month: 'Składka',
          bill: 'Rachunek',
          other: 'Inne',
          donation: 'Dotacja'
        }
      }
    }
  }
</script>
