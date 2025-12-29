<template>
  <b-modal ref="modal" title="Dodaj załącznik" size="xl" hide-footer>
    <b-form>
      <b-form-group label-cols="3" label="Dane przelewu" size="sm">
        <span v-if="transaction.name">{{ transaction.name }}<br /></span>
        {{ transaction.title }}
      </b-form-group>
      <b-form-group label-cols="3" label="Numer / Firma / Nazwa Pliku" size="sm">
        <b-form-input v-model.trim="name" size="sm" />
      </b-form-group>
      <b-form-group label-cols="3" label="Kwota" size="sm">
        <b-input-group append="zł" size="sm">
          <b-form-input v-model.trim="price" size="sm" type="number" />
        </b-input-group>
      </b-form-group>
    </b-form>
    <hr />
    <PromisedComponent :state="promiseState">
      <table class="table table-bordered table-sm">
        <thead>
          <tr>
            <th>Dokument</th>
            <th>Numer</th>
            <th>Podmiot</th>
            <th>Data</th>
            <th>Opis</th>
            <th>Kwota</th>
            <th>Prawdopobieństwo</th>
            <th>*</th>
          </tr>
        </thead>
        <tbody v-if="transaction">
          <tr v-for="doc in documents">
            <th>{{ doc.filename }}</th>
            <td>{{ doc.accounting_record }}</td>
            <td>{{ doc.company_name }}</td>
            <td>{{ doc.accounting_date }}</td>
            <td>{{ doc.description || '-' }}</td>
            <td><money-value :value="doc.price" /></td>
            <td v-if="isNaN(doc.score) || doc.score === scoreTotal"> - </td>
            <td v-else> {{ (100 - 100 * (doc.score / scoreTotal)).toFixed(2) }}% </td>
            <td>
              <b-button 
                size="sm"
                variant="primary"
                @click="add(doc)">
                Dodaj
              </b-button>
            </td>
          </tr>
        </tbody>
      </table>
    </PromisedComponent>
  </b-modal>
</template>
<script>
  import DocumentService from '@/services/document';
  import linkVm from '@/helpers/linkVm';

  export default {
    props: ['transaction'],
    data () {
      return {
        name: '',
        documents: [],
        promiseState: null,
        scoreTotal: 0,
        price: this.transaction.cost,
      };
    },
    watch: {
      name() {
        this.getAll();
      },
      price() {
        this.getAll();
      },
    },
    methods: {
      getAll() {
        const promise = DocumentService.getScore({
          parent: this.transaction.date.substr(0, 4 + 1 + 2),
          date: this.transaction.date,
          price: this.price,
          name: this.name,
        });

        linkVm(this, promise)
          .then((documentResponse) => {
            const documentIds = this.transaction.attachments.map(a => a.document.id);
            this.documents = documentResponse.data.filter(doc => !documentIds.includes(doc.id));
            this.scoreTotal = this.documents.reduce((total, doc) => total + (isNaN(doc.score) ? 0 : doc.score), 0);
          });
      },
      add(doc) {
        this.$emit("add", doc);
      },
      show() {
        this.$refs.modal.show();
        this.getAll();
      },
      hide() {
        this.$refs.modal.hide();
      },
    },
  }
</script>