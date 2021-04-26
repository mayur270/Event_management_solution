import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import axios from 'axios';

const getAPI = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    timeout: 1000,
})

export { getAPI }


Vue.config.productionTip = false

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
