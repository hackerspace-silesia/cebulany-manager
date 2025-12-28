<template>
  <div>
    <b-button @click="add">
      Dodaj nowy Transfer
    </b-button>
    <b-table
      hover="hover"
      bordered="bordered"
      small="small"
      :items="innerTransfers"
      :fields="fields"
    >
      <template v-slot:cell(date)="row">
        <date-picker
            v-model="row.item.date"
            type="date"
            value-type="format"
            token="YYYY-MM-DD"
            :clearable="false"
            @change="update(row.item)"
        />
      </template>
      <template v-slot:cell(budget_id)="row">
        <type-select
          v-model="row.item.budget_id" 
          :types="budgets"
          @change="update(row.item)"
        />
      </template>
      <template v-slot:cell(from_id)="row">
        <type-select 
          v-model="row.item.from_id" 
          :types="innerBudgets"
          @change="update(row.item)"
        />
      </template>
      <template v-slot:cell(to_id)="row">
        <type-select
          v-model="row.item.to_id" 
          :types="innerBudgets"
          @change="update(row.item)"
        />
      </template>
      <template v-slot:cell(cost)="row">
        <b-input-group
          append="zł"
          size="sm"
        >
          <b-form-input
            v-model.trim="row.item.cost"
            size="sm"
            type="number"
            @change="update(row.item)"
          />
        </b-input-group>
      </template>
      <template v-slot:cell(action)="row">
        <b-button @click="remove(row.item)">
          Skasuj
        </b-button>
      </template>
    </b-table>
  </div>
</template>
<script>
  import { toIsoDate } from '@/helpers/isoDate';
  import TypeSelect from '@/components/inputs/TypeSelect';
  export default {
    components: {
      TypeSelect,
    },
    props: ['innerTransfers', 'innerBudgets', 'budgets'],
    data () {
      return {
        fields: [
          {key: 'date', label: 'Data'},
          {key: 'budget_id', label: 'Budżet'},
          {key: 'from_id', label: 'Od'},
          {key: 'to_id', label: 'Do'},
          {key: 'cost', label: 'Kwota'},
          {key: 'action', label: '*'},
        ]
      }
    },
    methods: {
      getColor (color) {
        return '#' + color;
      },
      getBgColorStyle (color) {
        return {
          color: this.getColor(color),
        };
      },
      update (row) {
        this.$emit('row-update', row);
      },
      add () {
        const obj = {
          date: toIsoDate(new Date()),
          budget_id: 1,
          from_id: 1,
          to_id: 1,
          cost: 0,
        };
        this.$emit('row-update', obj);
      },
      remove (row) {
        this.$emit('row-remove', row);
      }
    },
  }
</script>
