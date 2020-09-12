// =========================================================
// * Vuetify Material Dashboard - v2.1.0
// =========================================================
//
// * Product Page: https://www.creative-tim.com/product/vuetify-material-dashboard
// * Copyright 2019 Creative Tim (https://www.creative-tim.com)
//
// * Coded by Creative Tim
//
// =========================================================
//
// * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import './plugins/base';
import './plugins/chartist';
import './plugins/vee-validate';
import vuetify from './plugins/vuetify';
import i18n from './i18n';

import axios from 'axios';

import { VTable, VPagination } from 'vue-easytable';
import VCharts from 'v-charts';
Vue.use(VCharts);

// 引入样式
import 'vue-easytable/libs/themes-base/index.css';
// 导入 table 和 分页组件

// 注册到全局
Vue.component(VTable.name, VTable);
Vue.component(VPagination.name, VPagination);

Vue.prototype.$axios = axios;

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  vuetify,
  i18n,
  render: (h) => h(App)
}).$mount('#app');
