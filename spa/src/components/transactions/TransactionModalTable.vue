<template>
  <table class="table table-bordered table-sm">
    <tr>
      <th>Nazwa</th>
      <td colspan="3">
        {{ item.name }}
      </td>
    </tr>
    <tr>
      <th>Tytuł</th>
      <td colspan="3">
        {{ item.title }}
      </td>
    </tr>
    <tr>
      <th>IBAN</th>
      <td>{{ item.iban }}</td>
      <th>Data</th>
      <td>{{ item.date }}</td>
    </tr>
    <tr>
      <th>Kwota</th>
      <th>
        <money-value :value="item.cost" />
      </th>
      <th>Pozostało do rozliczenia</th>
      <td>
        <money-value :value="item.left" />
      </td>
    </tr>
    <tr>
      <th>Dodatkowa informacja</th>
      <td colspan="3">
        <b-form-input size="sm" v-model.lazy.trim="item.additional_info" />
      </td>
    </tr>
  </table>
</template>
<script>
  export default {
    props: ['item']
  }
</script>
