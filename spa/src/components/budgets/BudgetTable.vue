<template lang="pug">
  .budgets
    b-table(
        hover, bordered, small, foot-clone
        :items="budgets",
        :fields="fields")
      template(slot="name", slot-scope="row")
        span(:title="row.value") {{ row.value }}
      template(slot="color", slot-scope="row")
        b-form-input(
          type="color"
          :value="getColor(row.value)"
          @input="row.item.color = $event.substring(1)"
          @change="update(row.item)"
        )
      template(slot="show_details_in_report", slot-scope="row")
        input(
          type="checkbox"
          v-model="row.item.show_details_in_report"
          :true-value="true"
          :false-value="false"
          @change="update(row.item)"
        )
      template(slot="show_count_in_report", slot-scope="row")
        input(
          type="checkbox"
          v-model="row.item.show_count_in_report"
          :true-value="true"
          :false-value="false"
          @change="update(row.item)"
        )

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
      getColor (color) {
        return '#' + color;
      },
      update (row) {
        this.$emit('row-update', row);
      }
    }
  }
</script>
