import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'

import App from './App'
import router from './router'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import MoneyValue from './components/MoneyValue'
import PromisedComponent from './components/PromisedComponent'

Vue.config.productionTip = false;
Vue.use(BootstrapVue);

Vue.filter('truncate', (string, value) => {
  if (string.length <= value) {
    return string;
  } else {
    return string.substring(0, value) + '…';
  }
});

Vue.component('money-value', MoneyValue);
Vue.component('PromisedComponent', PromisedComponent);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
});
