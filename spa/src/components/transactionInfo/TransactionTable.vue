<template>
  <table class="table table-bordered">
    <tr>
      <th>Nazwa</th>
      <td colspan="3">
        {{ item.name }}
        <b-btn-group class="float-right">
          <b-btn v-if="item.prev_id" variant="info" @click="prev">
            Poprzedni
          </b-btn>
          <b-btn v-if="item.next_id" variant="success" @click="next">
            Następny
          </b-btn>
        </b-btn-group>
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
      <PromisedCellComponent :state="promiseState" colspan="3">
        <b-form-input 
          size="sm"
          v-model.lazy.trim="item.additional_info"
          @change="update"
        />
      </PromisedCellComponent>
    </tr>
  </table>
</template>
<script>
  export default {
    props: ['item'],
    data() {
      return {
        promiseState: null,
      };
    },
    methods: {
      update() {
        this.$emit('update', this.item);
      },
      prev() {
        this.$emit('reload', this.item.prev_id);
      },
      next() {
        this.$emit('reload', this.item.next_id);
      },
    }
  }
</script>
