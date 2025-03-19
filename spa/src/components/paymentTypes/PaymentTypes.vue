<template>
  <b-row>
    <b-col>
      <h1>Typy płatności</h1>
      <PromisedComponent :state="promiseState">
        <PaymentTypesTable
          :payment-types="paymentTypes"
          :accountancy-types="accountancyTypes"
          @row-update="update"
          @row-remove="remove"
        />
      </PromisedComponent>
    </b-col>
  </b-row>
</template>

<script>
import PaymentTypesTable from './PaymentTypesTable'
import linkVm from '@/helpers/linkVm'

import PaymentTypeService from '@/services/paymentType'
import AccoutancyTypeService from '@/services/accountancyType'

export default {
  components: {
    PaymentTypesTable
  },
  data () {
    return {
      paymentTypes: [],
      accountancyTypes: [],
      promiseState: null
    }
  },
  created () {
    this.fetchPaymentTypes();
  },
  methods: {
    fetchPaymentTypes () {
      let promise = AccoutancyTypeService.getAll().then((response) => {
        this.accountancyTypes = response.data;
        return PaymentTypeService.getAll();
      }).then((response) => {
        this.paymentTypes = response.data;
      });

      linkVm(this, promise);
    },
    update (data) {
      if (!data.id) {
        PaymentTypeService.post(data).then(obj => {
          this.paymentTypes.push(obj.data);
        });
      } else {
        PaymentTypeService.update(data.id, data);
      }
    },
    remove (data) {
      PaymentTypeService.delete(data.id).then(() => {
        this.paymentTypes = this.paymentTypes.filter(obj => obj.id !== data.id);
      });
    }
  }
}
</script>