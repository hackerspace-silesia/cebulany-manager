<template>
  <b-form-select
    size="sm"
    :value="value"
    @input="$emit('input', $event)"
    @change="$emit('change', $event)"
  >
    <button>
      <selectedcontent></selectedcontent>
    </button>
    <option
      v-if="hasNullOption"
      :value="null"
    >
      -
    </option>
    <option
      v-for="type in types"
      :value="type.id"
    >
      <span :style="type | colorOption">
        {{ type.name }}
      </span>
    </option>
  </b-form-select>
</template>

<script>
  export default {
    filters: {
      colorOption (obj) {
        return {color: `#${obj.color}`};
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
  select, ::picker(select) {
    appearance: base-select;
  }
  option, selectedcontent {font-weight: bold;}
</style>
