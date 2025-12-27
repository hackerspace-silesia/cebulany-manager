<template>
  <td v-if="state && state.key === 'loading'">
    <b-progress
      :value="1"
      :max="1"
      animated="animated"
    />
  </td>
  <td v-else-if="state && state.key === 'error'">
    <b-progress
      :value="1"
      :max="1"
      variant="danger"
      striped="striped"
    />
    <div class="text-center">
      <slot name="error">
        <strong>Ugh Error ;_;</strong>
        <template v-if="state.code">
          &nbsp; HTTP: {{ state.code }}
        </template>
        <template v-if="state.msg">
          &nbsp;{{ state.msg }}
        </template>
      </slot>
    </div>
  </td>
  <td v-else>
    <slot>Insert Template Here.</slot>
  </td>
</template>

<script>
  export default {
    props: ['state']
  }
</script>
