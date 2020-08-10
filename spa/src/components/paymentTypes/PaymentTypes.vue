<template>
  <b-row>
    <b-col>
      <h1>Typy płatności</h1>
      <PromisedComponent :state="promiseState">
        <PaymentTypesTable
          :payment-types="paymentTypes"
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

export default {
  components: {
    PaymentTypesTable
  },
  data () {
    return {
      paymentTypes: [],
      promiseState: null
    }
  },
  created () {
    this.fetchPaymentTypes();
  },
  methods: {
    fetchPaymentTypes () {
      linkVm(this, PaymentTypeService.getAll())
        .then((response) => {
          this.paymentTypes = response.data;
        })
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

<style>
  .payment-type-badge {
    display: inline-block;
    text-align: center;
    width: 16px;
    margin: 0 1px;
    border-radius: 4px;
    color: white;
    font-size: 7pt;
    font-weight: bold;
    border: solid black;
    border-width: 3px;
  }
  .payment-type-badge-big {
    width: 18px;
    font-size: 9pt;
    border-radius: 8px;
  }
</style>
