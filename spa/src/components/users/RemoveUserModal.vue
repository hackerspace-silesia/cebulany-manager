<template>
  <div>
    <h5>Czy chcesz skasować usera {{ user.username }}?</h5>
    <b-btn @click="remove" >
      Tak
    </b-btn>
  </div>
</template>
<script>
  export default {
    props: ['user'],
    data () {
      return {
        data: {
          password: '',
        },
      }
    },
    methods: {
      remove () {
        this.$emit('remove', this.user.id);
      }
    }
  }
</script>
