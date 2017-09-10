import Vue from 'vue';
import Router from 'vue-router';
import Overlay from '@/components/overlay/Overlay';
import Config from '@/components/config/Config';

Vue.use(Router);

export default new Router({
  routes: [
    { path: '/', name: 'index', redirect: { name: 'overlay' } },
    { path: '/overlay', name: 'overlay', component: Overlay },
    { path: '/config', name: 'config', component: Config },
  ],
});
