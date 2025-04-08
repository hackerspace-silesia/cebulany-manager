<template>
  <div>
    <b-table
      hover="hover"
      bordered="bordered"
      small="small"
      :items="group.data"
      :fields="fields"
    >
      <template v-slot:cell(id)="row">
        <strong v-if="group.ids[row.value]" :style="getBgColorStyle(group.ids[row.value].color)">
          {{ group.ids[row.value].name }}
        </strong>
        <strong v-else>
          -
        </strong>
      </template>
      <template v-slot:cell(cost)="row">
        <money-value  class="float-right" :value="row.value" />
      </template>
    </b-table>
  </div>
</template>
<script>
  export default {
    props: ['title', 'group'],
    data () {
      return {
        fields: [
          {key: 'id', label: this.title},
          {key: 'cost', label: 'Kwota'},
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
      }
    }
  }
</script>
