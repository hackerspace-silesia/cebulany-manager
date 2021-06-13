<template>
  <div class="paymentTypes">
    <b-button @click="addPaymentType">
      Dodaj nowy rekord
    </b-button>
    <b-table
      hover="hover"
      bordered="bordered"
      small="small"
      foot-clone="foot-clone"
      :items="paymentTypes"
      :fields="fields"
    >
      <template v-slot:cell(name)="row">
        <b-form-input
          v-model.lazy.trim="row.item.name"
          @change="update(row.item)"
        />
      </template>
      <template v-slot:cell(color)="row">
        <input
          type="color"
          :value="getColor(row.value)"
          @input="row.item.color = $event.target.value.substring(1)"
          @change="update(row.item)"
        >
      </template>
      <template v-slot:cell(has_members)="row">
        <input
          v-model="row.item.has_members"
          type="checkbox"
          :true-value="true"
          :false-value="false"
          @change="update(row.item)"
        >
      </template>
      <template v-slot:cell(show_details_in_report)="row">
        <input
          v-model="row.item.show_details_in_report"
          type="checkbox"
          :true-value="true"
          :false-value="false"
          @change="update(row.item)"
        >
      </template>
      <template v-slot:cell(show_count_in_report)="row">
        <input
          v-model="row.item.show_count_in_report"
          type="checkbox"
          :true-value="true"
          :false-value="false"
          @change="update(row.item)"
        >
      </template>
      <template v-slot:cell(has_members)="row">
        <input
          v-model="row.item.has_members"
          type="checkbox"
          :true-value="true"
          :false-value="false"
          @change="update(row.item)"
        >
      </template>
      <template v-slot:cell(action)="row"
      >
        <b-button @click="removePaymentType(row.item)">
          Skasuj
        </b-button>
      </template>
    </b-table>
  </div>
</template>
<script>
  export default {
    props: ['paymentTypes'],
    data () {
      return {
        fields: [
          {key: 'name', label: 'Nazwa'},
          {key: 'color', label: 'Kolor'},
          {key: 'has_members', label: 'Obsługa użytkowników'},
          {key: 'show_details_in_report', label: 'Pokaż szczegóły w raporcie'},
          {key: 'show_count_in_report', label: 'Zliczaj w raporcie'},
          {key: 'action', label: 'Akcje'},
        ]
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
