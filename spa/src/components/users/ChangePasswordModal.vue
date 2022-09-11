<template>
  <div>
    <h5>Zmień hasło dla {{ user.username }}</h5>
    <b-form>
      <label>Nowe Hasło</label> <b-form-input v-model="data.password" />
      <b-btn @click="change"> Zmień </b-btn>
    </b-form>
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
      change () {
        const data = {id: this.user.id, password: this.data.password};
        this.$emit('change', data);
      }
    }
  }
</script>
