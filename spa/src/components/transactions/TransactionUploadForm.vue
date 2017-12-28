<template lang="pug">
  b-card: PromisedComponent(:state="promiseState", show-on-promise)
    Alert(ref="successAlert")
    b-form(@submit="uploadFile")
      b-form-group(label="Wrzuć plik z transakcjami")
        b-form-file(size="sm", v-model="file", accept=".csv")
        | &nbsp;
        b-button(type="submit") Wrzuć

</template>
<script>
  import Alert from '@/components/Alert';
  import transactionService from '@/services/transactions';
  import linkVm from '@/helpers/linkVm';

  export default {
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
    },
    components: {
      Alert
    }
  }
</script>
