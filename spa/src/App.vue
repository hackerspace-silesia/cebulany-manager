<template>
  <div id="app">
    <MenuPanel v-if="logged" @logout="logout" /><br>
    <b-container fluid v-if="logged">
      <router-view />
    </b-container>
    <b-container v-else>
      <LoginView @onSuccess="login" />
    </b-container>
  </div>
</template>

<script>
import stateData from '@/state'
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
      logged: false,
    }
  },
  methods: {
    login() {
      this.logged = true;
      stateData.updateDeadline();
    },
    logout() {
      this.logged = false;
      this.tokenTime = 0;
    }
  }
}
</script>

<style>
  .table-sm td { font-size: 8pt; }
  .table-sm th { font-size: 8pt; }
  .monospace { font-family: 'monospace'; }
</style>