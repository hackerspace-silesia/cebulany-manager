<template lang="pug">
  #app
    MenuPanel(v-if="logged")
    br
    b-container(v-if="logged")
      router-view
    b-container(v-else)
      LoginView(@onSuccess="logged = true")

</template>

<script>
import MenuPanel from '@/components/MenuPanel'
import LoginView from '@/components/Login'
export default {
  name: 'app',
  data () {
    return {
      logged: false
    }
  },
  components: {
    MenuPanel,
    LoginView
  }
}
</script>

<style>
  .table-sm td { font-size: 8pt; }
  .table-sm th { font-size: 8pt; }
  .monospace { font-family: 'monospace'; }
</style>
