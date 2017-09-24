<template lang="pug">
  div(v-if="state && state.key == 'loading'")
    b-progress(:value="1", :max="1", animated)
  div(v-else-if="state && state.key == 'error'")
    b-progress(:value="1", :max="1", variant="danger" striped)
    div(class='text-center')
      slot(name='error')
        strong Ugh Error ;_;
        template(v-if="state.code") &nbsp; HTTP: {{ state.code }}
        template(v-if="state.msg") &nbsp;{{ state.msg }}
  div(v-else)
    slot Insert Template Here.
</template>

<script>
  export default {
    props: ['state']
  }
</script>
