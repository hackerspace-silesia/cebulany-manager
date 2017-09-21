import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'

import App from './App'
import router from './router'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false;
Vue.use(BootstrapVue);

Vue.filter('truncate', (string, value) => {
  if (string.length <= value) {
    return string;
  } else {
    return string.substring(0, value) + '…';
  }
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
});
