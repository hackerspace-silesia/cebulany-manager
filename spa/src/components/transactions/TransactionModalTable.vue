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
  </table>
</template>
<script>
  export default {
    props: ['item']
  }
</script>
