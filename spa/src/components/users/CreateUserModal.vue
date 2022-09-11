<template>
  <div>
    <h5>Stwórz użytkownika</h5>
    <b-form>
      <label>Nazwa</label> <b-form-input v-model="data.username" />
      <label>Hasło</label> <b-form-input v-model="data.password" />
      <b-btn @click="create"> Dodaj </b-btn>
    </b-form>
  </div>
</template>
<script>
  export default {
    data () {
      return {
        data: {
          username: '',
          password: '',
        }
      }
    },
    methods: {
      create () {
        this.$emit('create', this.data);
      }
    }
  }
</script>
