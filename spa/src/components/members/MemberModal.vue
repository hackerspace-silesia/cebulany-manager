<template>
  <div>
    <h5>Formularz</h5>
    <MemberForm
      :member="item"
      :is-new="false"
      @update="updateForm"
    />
    <h5>Płatności</h5>
    <MemberPaymentsTable :member="item" />
  </div>
</template>
<script>
  import MemberForm from './MemberForm';
  import MemberPaymentsTable from './MemberPaymentsTable';

  export default {
    components: { MemberForm, MemberPaymentsTable },
    props: ['item'],
    data () {
      return {
        promiseState: null
      }
    },
    methods: {
      updateForm (data) {
        this.$emit('update', data);
      }
    }
  }
</script>
