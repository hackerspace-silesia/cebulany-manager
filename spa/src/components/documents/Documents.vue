<template>
  <b-row>
    <b-col>
      <h1>Budżety</h1>
      <b-form>
        <date-picker
          v-model="month"
          type="month"
          value-type="format"
          token="YYYY-MM"
          :clearable="false"
          @change="fetchDocuments"
        />
        <b-btn @click="sync">Sync</b-btn>
      </b-form>
      <PromisedComponent :state="promiseState">
        <DocumentTable
          :documents="documents"
          :item-to-show="itemToShow"
          @row-update="update"
          @row-show="showIframe"
        />
      </PromisedComponent>
    </b-col>
    <b-col>
      <div class="sticky-iframe" v-if="itemToShow">
        <b-row>
          <b-col><strong>{{ itemToShow.label }}</strong></b-col>
          <b-col class="text-right">
            <b-btn size="sm" @click="hideIframe">Zamknij</b-btn>
          </b-col>
        </b-row>
        <iframe :src="itemToShow.link" :allow="`clipboard-read; clipboard-write self ${itemToShow.link}`" />
      </div>
    </b-col>
  </b-row>
</template>

<script>
import DocumentTable from './DocumentTable'
import { toIsoMonth } from '@/helpers/isoDate';
import linkVm from '@/helpers/linkVm'

import DocumentService from '@/services/document'

export default {
  components: {
    DocumentTable
  },
  data () {
    const month = this.$route.query.month || toIsoMonth(new Date());
    return {
      month,
      documents: [],
      promiseState: null,
      itemToShow: null,
    }
  },
  created () {
    this.fetchDocuments();
  },
  methods: {
    fetchDocuments () {
      this.itemToShow = null;
      this.$router.replace({
        name: 'Documents',
        query: {month: this.month},
      }).catch(()=>{});
      linkVm(this, DocumentService.getAll({parent: this.month}))
        .then((response) => {
          this.documents = response.data;
        })
    },
    sync () {
      linkVm(this, DocumentService.sync(this.month))
        .then(this.fetchDocuments);
    },
    showIframe (item) {
      this.itemToShow = item;
    },
    hideIframe () {
      this.itemToShow = null;
    },
    update (data) {
      this.$set(data, '_state', 'loading');
      DocumentService.update(data.id, data).then(() => {
        this.$set(data, '_state', 'ok');
      }).catch(() => {
        this.$set(data, '_state', 'error');
      });
    },
  }
}
</script>

<style scoped>
  .sticky-iframe {
    position: sticky;
    top: 1em;
  }
  .sticky-iframe iframe {
    width: 100%;
    height: calc(100vh - 200px);
  }
</style>