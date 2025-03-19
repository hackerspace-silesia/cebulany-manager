<template>
  <b-form-select
    size="sm"
    :value="value"
    @input="$emit('input', $event)"
    @change="$emit('change', $event)"
  >
    <option
      v-if="hasNullOption"
      :value="null"
    >
      -
    </option>
    <option
      v-for="type in types"
      :style="type | colorOption"
      :value="type.id"
    >
      {{ type.name }}
    </option>
  </b-form-select>
</template>

<script>
  export default {
    filters: {
      colorOption (obj) {
        return {backgroundColor: `#${obj.color}`};
      }
    },
    props: {
      types: { required: true },
      value: { required: true },
      hasNullOption: { default: false }
    }
  }
</script>

<style scoped>
  option {color: white;}
</style>
