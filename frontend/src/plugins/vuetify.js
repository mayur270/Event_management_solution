import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
import Vuelidate from 'vuelidate'

import '@fortawesome/fontawesome-free/css/all.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

Vue.use(Vuetify);
Vue.use(Vuelidate);

export default new Vuetify({
	iconfont: 'md' | 'fa',
});
