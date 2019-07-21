<template lang="pug">
  .budgets
    b-table(
        hover, bordered, small, foot-clone
        @row-clicked.captured="rowClicked",
        :items="budgets",
        :fields="fields")
      template(slot="name", slot-scope="row")
        span(:title="row.value") {{ row.value }}
      template(slot="color", slot-scope="row")
        span(:title="row.value") {{ row.value }}
      template(slot="show_details_in_report", slot-scope="row")
        span(:title="row.value") {{ row.value }}  

      template(slot="show_count_in_report", slot-scope="row")
        span(:title="row.value") {{ row.value }}

</template>
<script>
  export default {
    props: ['budgets'],
    data () {
      return {
        fields: {
          'name': {label: 'Nazwa'},
          'color': {label: 'Kolor'},
          'show_details_in_report': {label: 'Pokaż szczegóły w raporcie'},
          'show_count_in_report': {label: 'Zliczaj w raporcie'}
        }
      }
    },
    methods: {
      rowClicked (item) {
        this.showModal = true;
        this.modalItem = item;
      }
    },
    filters: {
      paymentStyle (payment) {
        return {
          backgroundColor: `#${payment.payment_type.color}`,
          borderColor: `#${payment.budget.color}`
        };
      },
      paymentTitle (payment) {
        return payment.payment_type.name;
      },
      paymentName (payment) {
        let name = payment.payment_type.name;
        return name ? name.charAt(0).toUpperCase() : '?';
      }
    }
  }
</script>
