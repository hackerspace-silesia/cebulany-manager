<template lang="pug">
  .budgets
    b-button(@click="addBudget") Dodaj nowy rekord
    b-table(
        hover, bordered, small, foot-clone
        :items="budgets",
        :fields="fields")
      template(slot="name", slot-scope="row")
        b-form-input(
          v-model.lazy.trim="row.item.name"
          @change="update(row.item)"
        )
      template(slot="color", slot-scope="row")
        input(
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
      template(slot="action", slot-scope="row")
        b-button(@click='removeBudget(row.item)') Skasuj

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
          'show_count_in_report': {label: 'Zliczaj w raporcie'},
          'action': {label: 'Akcje'}
        }
      }
    },
    methods: {
      getColor (color) {
        return '#' + color;
      },
      update (row) {
        this.$emit('row-update', row);
      },
      addBudget () {
        const len = this.budgets.length;
        const obj = {
          name: `BUDGET-${len}`,
          color: '000000',
          show_details_in_report: false,
          show_count_in_report: false
        };
        this.$emit('row-update', obj);
      },
      removeBudget (row) {
        this.$emit('row-remove', row);
      }
    }
  }
</script>
