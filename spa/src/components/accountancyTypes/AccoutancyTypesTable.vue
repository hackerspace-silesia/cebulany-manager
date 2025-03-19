<template>
  <div class="paymentTypes">
    <b-button @click="add">
      Dodaj nowy rekord
    </b-button>
    <b-table
      hover="hover"
      bordered="bordered"
      small="small"
      foot-clone="foot-clone"
      :items="accountancyTypes"
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
      <template v-slot:cell(action)="row">
        <b-button @click="remove(row.item)">
          Skasuj
        </b-button>
      </template>
    </b-table>
  </div>
</template>
<script>
  export default {
    props: ['accountancyTypes'],
    data () {
      return {
        fields: [
          {key: 'name', label: 'Nazwa'},
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
      add () {
        const len = this.accountancyTypes.length;
        const obj = {
          name: `TYPE-${len}`,
          color: '000000',
        };
        this.$emit('row-update', obj);
      },
      remove (row) {
        this.$emit('row-remove', row);
      }
    }
  }
</script>
