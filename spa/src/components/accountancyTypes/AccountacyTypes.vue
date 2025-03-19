<template>
  <b-row>
    <b-col>
      <h1>Księgowe typy</h1>
      <PromisedComponent :state="promiseState">
        <AccountancyTypesTable
          :accountancy-types="accountancyTypes"
          @row-update="update"
          @row-remove="remove"
        />
      </PromisedComponent>
    </b-col>
  </b-row>
</template>

<script>
import AccountancyTypesTable from './AccoutancyTypesTable'
import linkVm from '@/helpers/linkVm'

import AccountancyTypeService from '@/services/accountancyType'

export default {
  components: {
    AccountancyTypesTable
  },
  data () {
    return {
      accountancyTypes: [],
      promiseState: null
    }
  },
  created () {
    this.fetchAccountancyTypes();
  },
  methods: {
    fetchAccountancyTypes () {
      linkVm(this, AccountancyTypeService.getAll())
        .then((response) => {
          this.accountancyTypes = response.data;
        })
    },
    update (data) {
      if (!data.id) {
        AccountancyTypeService.post(data).then(obj => {
          this.accountancyTypes.push(obj.data);
        });
      } else {
        AccountancyTypeService.update(data.id, data);
      }
    },
    remove (data) {
      AccountancyTypeService.delete(data.id).then(() => {
        this.paymentTypes = this.paymentTypes.filter(obj => obj.id !== data.id);
      });
    }
  }
}
</script>