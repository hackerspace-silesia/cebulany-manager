<template lang="pug">
  b-row: .col-6: b-form(inline)
    label Nazwa:&nbsp;
    b-form-input(size="sm", v-model.trim="name", @change="change")
</template>

<script>
  export default {
    data () {
      return {
        name: ''
      }
    },
    methods: {
      change () {
        let data = {};
        if (this.name) {
          data.name = this.name;
        }
        this.$emit('change', data)
      }
    }
  }
</script>
