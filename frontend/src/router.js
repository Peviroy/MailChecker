import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      component: () => import('@/views/dashboard/Index'),
      children: [
        // Dashboard
        {
          name: 'Dashboard',
          path: '',
          component: () => import('@/views/dashboard/Dashboard')
        },
        {
          name: 'Generator lab',
          path: 'components/icons',
          component: () => import('@/views/dashboard/component/Icons')
        },
        // Tables
        {
          name: 'Data table',
          path: 'dataset/RegularTables',
          component: () => import('@/views/dashboard/dataset/RegularTables')
        },
        // Maps
        {
          name: 'Word analysis',
          path: 'dataset/WordAnalysis',
          component: () => import('@/views/dashboard/dataset/WordAnalysis')
        }
      ]
    },
    {
      name: 'NotFound',
      path: '*',
      component: () => import('@/views/NotFound')
    }
  ]
});
