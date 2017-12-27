<template lang="pug">
  PromisedComponent(:state="promiseState")
    b-form(@submit="onSubmit")
      b-form-group(label="Nazwa")
        b-form-input(type="text", v-model="member.name", size="sm")
      b-form-group(label="Data przystąpienia")
        b-form-input(type="date", v-model="member.join_date", size="sm")
      b-form-checkbox(v-model="member.active") Aktywny?
      b-form-group
        b-button(type="submit") Aktulizuj


</template>

<script>
  export default {
    props: ['member'],
    data () {
      return {
        promiseState: null
      }
    },
    methods: {
      onSubmit (evt) {
        evt.preventDefault();
        console.log('!!');
      }
    }
  }
</script>
