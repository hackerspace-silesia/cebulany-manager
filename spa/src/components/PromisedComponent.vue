<template lang="pug">
  div
    template(v-if="state && state.key == 'loading'")
      b-progress(:value="1", :max="1", animated)
    template(v-else-if="state && state.key == 'error'")
      b-progress(:value="1", :max="1", variant="danger" striped)
      div(class='text-center')
        slot(name='error')
          strong Ugh Error ;_;
          template(v-if="state.code") &nbsp; HTTP: {{ state.code }}
          template(v-if="state.msg") &nbsp;{{ state.msg }}
    template(v-if="showOnPromise || !state")
      slot Insert Template Here.
</template>

<script>
  export default {
    props: ['state', 'showOnPromise']
  }
</script>
