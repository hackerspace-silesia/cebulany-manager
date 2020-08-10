<template>
  <div>
    <template v-if="state && state.key == 'loading'">
      <b-progress
        :value="1"
        :max="1"
        animated="animated"
      />
    </template><template v-else-if="state && state.key == 'error'">
      <b-progress
        :value="1"
        :max="1"
        variant="danger"
        striped="striped"
      /><div class="text-center">
        <slot name="error">
          <strong>Ugh Error ;_;</strong>
          <template v-if="state.code">
            &nbsp; HTTP: {{ state.code }}
          </template>
          <template
            v-if="state.msg"
          >
            &nbsp;{{ state.msg }}
          </template>
        </slot>
      </div>
    </template><template v-if="showOnPromise || !state">
      <slot>Insert Template Here.</slot>
    </template>
  </div>
</template>

<script>
  export default {
    props: ['state', 'showOnPromise']
  }
</script>
