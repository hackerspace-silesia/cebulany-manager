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
    <PromisedRowComponent :state="promiseState">
      <th>Dodatkowa informacja</th>
      <td colspan="3">
        <b-form-input 
          size="sm"
          v-model.lazy.trim="item.additional_info"
          @change="update"
        />
      </td>
    </PromisedRowComponent>
  </table>
</template>
<script>
  import TransactionService from '@/services/transactions'
  import linkVm from '@/helpers/linkVm'

  export default {
    props: ['item'],
    data() {
      return {
        promiseState: null,
      };
    },
    methods: {
      update() {
        const {id, additional_info: AddtionalInfo} = this.item;
        const promise = TransactionService.updateAdditionalInfo(id, {
          additional_info: AddtionalInfo,
        });
        linkVm(this.promiseState, promise);
      }
    }
  }
</script>
