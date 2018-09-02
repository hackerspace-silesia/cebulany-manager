<template lang="pug">
  b-form-select(size="sm", :value="value", @input="doInput()")
    option(
        v-for="type in types",
        :style="type | colorOption",
        :value="type.id") {{type.name}}
</template>

<script>
  export default {
    props: ['types', 'value'],
    methods: {
      doInput () {
        this.$emit('input', this.$event.target.value);
      }
    },
    filters: {
      colorOption (obj) {
        return {backgroundColor: `#${obj.color}`};
      }
    }
  }
</script>
