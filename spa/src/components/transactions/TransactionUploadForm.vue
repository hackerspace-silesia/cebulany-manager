<template>
  <b-card>
    <PromisedComponent
      :state="promiseState"
      show-on-promise="show-on-promise"
    >
      <Alert ref="successAlert" />
      <b-form @submit="uploadFile">
        <b-form-group label="Wrzuć plik z transakcjami">
          <b-form-file
            v-model="file"
            size="sm"
            accept=".pdf"
          />&nbsp;
          <b-button type="submit">
            Wrzuć
          </b-button>
        </b-form-group>
      </b-form>
    </PromisedComponent>
  </b-card>
</template>
<script>
  import Alert from '@/components/Alert';
  import transactionService from '@/services/transactions';
  import linkVm from '@/helpers/linkVm';

  export default {
    components: {
      Alert
    },
    props: ['upload'],
    data () {
      return {
        promiseState: null,
        file: null
      }
    },
    methods: {
      uploadFile (event) {
        event.preventDefault();
        linkVm(this, transactionService.upload(this.file))
          .then(resp => {
            this.file = null;
            this.$refs.successAlert.$emit('turnOn');
            this.$emit('upload');
          })
      }
    }
  }
</script>
