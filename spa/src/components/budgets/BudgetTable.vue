<template>
  <div class="budgets">
    <b-button @click="add">
      Dodaj nowy rekord
    </b-button>
    <b-table
      hover="hover"
      bordered="bordered"
      small="small"
      foot-clone="foot-clone"
      :items="budgets"
      :fields="fields"
    >
      <template v-slot:cell(name)="row">
        <b-form-input
          v-model.lazy.trim="row.item.name"
          @change="update(row.item)"
        />
      </template>
      <template v-slot:cell(description_on_positive)="row">
        <b-form-input
          v-model.lazy.trim="row.item.description_on_positive"
          @change="update(row.item)"
        />
      </template>
      <template v-slot:cell(description_on_negative)="row">
        <b-form-input
          v-model.lazy.trim="row.item.description_on_negative"
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
      <template v-slot:cell(action)="row" >
        <b-button @click="remove(row.item)">
          Skasuj
        </b-button>
      </template>
    </b-table>
  </div>
</template>
<script>
  export default {
    props: ['budgets'],
    data () {
      return {
        fields: [
          {key: 'name', label: 'Nazwa'},
          {key: 'description_on_positive', label: 'Opis (Zysk)'},
          {key: 'description_on_negative', label: 'Opis (Koszt)'},
          {key: 'color', label: 'Kolor'},
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
      add () {
        const len = this.budgets.length;
        const obj = {
          name: `BUDGET-${len}`,
          color: '000000',
          description_on_negative: '',
          description_on_positive: '',
          show_details_in_report: false,
          show_count_in_report: false
        };
        this.$emit('row-update', obj);
      },
      remove (row) {
        this.$emit('row-remove', row);
      }
    }
  }
</script>
