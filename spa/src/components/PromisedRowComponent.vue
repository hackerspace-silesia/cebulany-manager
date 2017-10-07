<template lang="pug">
  tr
    template(v-if="state && state.key == 'loading'")
      td(colspan="1000")
        b-progress(:value="1", :max="1", animated)
    template(v-else-if="state && state.key == 'error'")
      td(colspan="1000")
        b-progress(:value="1", :max="1", variant="danger" striped)
        div(class='text-center')
          slot(name='error')
            strong Ugh Error ;_;
            template(v-if="state.code") &nbsp; HTTP: {{ state.code }}
            template(v-if="state.msg") &nbsp;{{ state.msg }}
    template(v-else)
      slot Insert Template Here.
</template>

<script>
  export default {
    props: ['state']
  }
</script>
