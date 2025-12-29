<template>
  <div>
    <h5>
      Załączniki 
      <b-button variant="primary" @click="showModal">Dodaj</b-button>
    </h5> 
    <DocumentModal
      ref="documentModal"
      :transaction="transaction"
      @add="add"
    />
    <table class="table table-bordered table-sm">
      <thead>
        <tr>
          <th>Typ</th>
          <th>Budżet</th>
          <th>Budżet wew.</th>
          <th>Nazwa</th>
          <th>Data</th>
          <th>Kwota</th>
          <th>*</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="att in transaction.attachments" :key="att.id">
          <th>{{ att.doc.filename }}</th>
          <td>
            <b-button variant="danger" @click="remove(att.id)">Usuń</b-button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script>
  import DocumentModal from './DocumentModal.vue';

  export default {
    components: {DocumentModal},
    props: ['transaction'],
    methods: {
      showModal() {
        this.$refs.documentModal.show();
      },
      add (obj) {
        this.$refs.documentModal.hide();
        console.log(obj);
      },
      remove (pk) {
          let transaction = this.transaction;
          transaction.attachments = transaction.attachments.filter(obj => obj.id !== pk);
      },
    }
  }
</script>
