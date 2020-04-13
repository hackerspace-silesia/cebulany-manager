<template lang="pug">
  b-pagination(
    :value="value",
    :total-rows="count",
    :per-page="itemsPerPage",
    align="center",
    @input="input",
  )
</template>
<script>
  export default {
    props: ['value', 'count', 'itemsPerPage'],
    methods: {
      input (value) {
        this.$emit('input', value);
      }
    }
  }
</script>
