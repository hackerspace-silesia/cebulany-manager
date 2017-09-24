<template lang="pug">
  .text-danger(v-if="value < 0") {{ value }} zł
  div(v-else) {{ value }} zł
</template>

<script>
  export default {
    props: ['value']
  }
</script>
