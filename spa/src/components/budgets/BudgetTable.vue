<template lang="pug">
  .budgets
    b-table(
        hover, bordered, small, foot-clone
        :items="budgets",
        :fields="fields")
      template(slot="name", slot-scope="row")
        span(:title="row.value") {{ row.value }}
      template(slot="color", slot-scope="row")
        b-form-input( type="color" :value="getColor(row.value)")
      template(slot="show_details_in_report", slot-scope="row")
        input(type="checkbox" :value="row.value")
      template(slot="show_count_in_report", slot-scope="row")
        input(type="checkbox" :value="row.value" true-value="true" false-value="false" @change="update(row)" )

</template>
<script>
  export default {
    props: ['budgets', 'update'],
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
      getColor (color) {
        return '#' + color;
      }
    }
  }
</script>
