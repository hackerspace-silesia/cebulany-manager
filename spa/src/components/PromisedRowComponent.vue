<template>
  <tr>
    <template v-if="state && state.key === 'loading'">
      <td colspan="1000">
        <b-progress
          :value="1"
          :max="1"
          animated="animated"
        />
      </td>
    </template>
    <template v-else-if="state && state.key === 'error'">
      <td colspan="1000">
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
    </template>
    <template v-else>
      <slot>Insert Template Here.</slot>
    </template>
  </tr>
</template>

<script>
  export default {
    props: ['state']
  }
</script>
