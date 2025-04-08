<template>
  <div v-if="value < 0" class="text-danger">
    {{ value }} zł
  </div>
  <div v-else>
    {{ value }} zł
  </div>
</template>

<script>
  export default {
    props: ['value']
  }
</script>
