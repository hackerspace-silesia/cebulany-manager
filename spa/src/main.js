import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';

import App from './App';
import router from './router';
import dataState from './state';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'vue-select/dist/vue-select.css';
import 'vue2-datepicker/index.css';

import DatePicker from 'vue2-datepicker';
import MoneyValue from './components/MoneyValue';
import PromisedComponent from './components/PromisedComponent';
import PromisedRowComponent from './components/PromisedRowComponent';
import vSelect from 'vue-select';

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
Vue.component('PromisedRowComponent', PromisedRowComponent);
Vue.component('v-select', vSelect);
Vue.component('date-picker', DatePicker);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
  data: dataState.state,
});
