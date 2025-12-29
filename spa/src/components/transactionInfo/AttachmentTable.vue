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

    <PromisedComponent :state="promiseState">
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>Dokument</th>
            <th>Numer</th>
            <th>Firma</th>
            <th>Data</th>
            <th>Opis</th>
            <th>Kwota</th>
            <th>*</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="att in transaction.attachments" :key="att.id">
            <th>{{ att.document.filename }}</th>
            <td>{{ att.document.accounting_record }}</td>
            <td>{{ att.document.company_name }}</td>
            <td>{{ att.document.accounting_date }}</td>
            <td>{{ att.document.description || '-' }}</td>
            <td><money-value :value="att.document.price" /></td>
            <td>
              <b-button variant="danger" @click="remove(att.id)">Usuń</b-button>
            </td>
          </tr>
        </tbody>
      </table>
    </PromisedComponent>
  </div>
</template>
<script>
  import DocumentModal from './DocumentModal.vue';
  import AttachmentService from '@/services/attachment';

  import linkVm from '@/helpers/linkVm';

  export default {
    components: {DocumentModal},
    props: ['transaction'],
    data() {
      return {
        promiseState: null,
      };
    },
    methods: {
      showModal() {
        this.$refs.documentModal.show();
      },
      add (document) {
        let transaction = this.transaction;
        this.$refs.documentModal.hide();
        linkVm(this, AttachmentService.post({
          transaction_id: transaction.id,
          document_id: document.id,
        })).then((response) => {
          transaction.attachments.push(response.data);
        });
      },
      remove (pk) {
        let transaction = this.transaction;
        linkVm(this, AttachmentService.delete(pk)).then((response) => {
          transaction.attachments = transaction.attachments.filter(obj => obj.id !== pk);
        })
      },
    }
  }
</script>
