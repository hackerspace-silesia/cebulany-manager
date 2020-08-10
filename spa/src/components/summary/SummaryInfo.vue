<template>
  <table class="table table-bordered table-condensed table-hover table-sm">
    <tr v-for="[name, value] in tableData">
      <td
        :class="value !== undefined ? '' : 'title'"
        :colspan="value !== undefined ? 1 : 2"
      >
        {{ name }}
      </td>
      <td
        v-if="value !== undefined"
        class="text-right"
      >
        <money-value :value="value" />
      </td>
    </tr>
  </table>
</template>
<script>
  export default {
    props: ['outstandingCost', 'balances'],
    computed: {
      tableData () {
        return [
          ['Nierozliczone', this.outstandingCost],
          ['Początek roku'],
          ['Aktywa obrotowe', this.balances.curr_start_year],
          ['Zysk/Strata z lat ubiegłych', this.balances.diff_prev_start_year],
          ['Zysk/Strata netto', this.balances.diff_start_year],
          ['Koniec roku'],
          ['Aktywa obrotowe', this.balances.curr_end_year],
          ['Zysk/Strata z lat ubiegłych', this.balances.diff_prev_end_year],
          ['Zysk/Strata netto', this.balances.diff_end_year]
        ]
      }
    }
  }
</script>

<style scoped>
  td.title {
    font-weight: bold;
    background-color: #fafafa;
  }
</style>
