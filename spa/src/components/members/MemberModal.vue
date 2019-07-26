<template lang="pug">
  div
    h5 Formularz
    MemberForm(:member="item", :is-new="false", @update="updateForm")
    h5 Płatności
    MemberPaymentsTable(:member="item")
</template>
<script>
  import MemberForm from './MemberForm';
  import MemberPaymentsTable from './MemberPaymentsTable';

  export default {
    props: ['item'],
    data () {
      return {
        promiseState: null
      }
    },
    components: { MemberForm, MemberPaymentsTable },
    methods: {
      updateForm (data) {
        this.$emit('update', data);
      }
    }
  }
</script>
