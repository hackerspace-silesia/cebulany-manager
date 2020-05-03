<template lang="pug">
  b-form-row
    b-col(cols="3"): b-form-group(label="Rok", label-size="sm")
      b-form-input(
        v-model="query.year",
        type="number")
</template>
<script>
  export default {
    data () {
      const date = new Date();
      const year = date.getFullYear();
      return {
        query: { year }
      };
    },
    watch: {
      query: {
        deep: true,
        handler () {
          this.setQuery();
        }
      }
    },
    mounted () {
      this.setQuery();
    },
    methods: {
      setQuery () {
        const query = Object.assign({}, this.query);
        this.$emit('input', query);
      }
    }
  }
</script>
