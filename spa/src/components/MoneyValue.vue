<template>
  <div v-if="value < 0" class="text-danger">
    {{ value && value.toFixed ? value.toFixed(2) : value }} zł
  </div>
  <div v-else>
    {{ value && value.toFixed ? value.toFixed(2) : value }} zł
  </div>
</template>

<script>
  export default {
    props: ['value']
  }
</script>
