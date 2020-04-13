<template lang="pug">
  .paymentTypes
    b-button(@click="addPaymentType") Dodaj nowy rekord
    b-table(
        hover, bordered, small, foot-clone
        :items="paymentTypes",
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
      template(slot="has_members", slot-scope="row")
        input(
          type="checkbox"
          v-model="row.item.has_members"
          :true-value="true"
          :false-value="false"
          @change="update(row.item)"
        )
      template(slot="action", slot-scope="row")
        b-button(@click='removePaymentType(row.item)') Skasuj

</template>
<script>
  export default {
    props: ['paymentTypes'],
    data () {
      return {
        fields: {
          'name': {label: 'Nazwa'},
          'color': {label: 'Kolor'},
          'show_details_in_report': {label: 'Pokaż szczegóły w raporcie'},
          'show_count_in_report': {label: 'Zliczaj w raporcie'},
          'has_members': {label: 'Posiada członków'},
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
      addPaymentType () {
        const len = this.paymentTypes.length;
        const obj = {
          name: `TYPE-${len}`,
          color: '000000',
          show_details_in_report: false,
          show_count_in_report: false,
          has_members: false
        };
        this.$emit('row-update', obj);
      },
      removePaymentType (row) {
        this.$emit('row-remove', row);
      }
    }
  }
</script>
