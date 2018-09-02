<template lang="pug">
  b-form-select(size="sm", v-bind:value="value", v-on:input="$emit('input', $event)")
    option(
        v-for="type in types",
        :style="type | colorOption",
        :value="type.id") {{type.name}}
</template>

<script>
  export default {
    props: ['types', 'value'],
    filters: {
      colorOption (obj) {
        return {backgroundColor: `#${obj.color}`};
      }
    }
  }
</script>

<style>
  option {color: white;}
</style>
