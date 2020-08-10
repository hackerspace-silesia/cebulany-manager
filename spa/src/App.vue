<template>
  <div id="app">
    <MenuPanel v-if="logged" /><br>
    <b-container v-if="logged">
      <router-view />
    </b-container>
    <b-container v-else>
      <LoginView @onSuccess="logged = true" />
    </b-container>
  </div>
</template>

<script>
import MenuPanel from '@/components/MenuPanel'
import LoginView from '@/components/Login'
export default {
  name: 'App',
  components: {
    MenuPanel,
    LoginView
  },
  data () {
    return {
      logged: false
    }
  }
}
</script>

<style>
  .table-sm td { font-size: 8pt; }
  .table-sm th { font-size: 8pt; }
  .monospace { font-family: 'monospace'; }
</style>
