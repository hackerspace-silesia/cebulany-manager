<template>
  <div class="budgets">
    <b-button @click="addInnerBudget">
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
      <template v-slot:cell(action)="row" >
        <b-button @click="removeInnerBudget(row.item)">
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
      addInnerBudget () {
        const len = this.budgets.length;
        const obj = {
          name: `BUDGET-${len}`,
          color: '000000',
        };
        this.$emit('row-update', obj);
      },
      removeInnerBudget (row) {
        this.$emit('row-remove', row);
      }
    }
  }
</script>
