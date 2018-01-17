import Vue from 'vue';
import './common';
import Overlay from './components/overlay/Overlay.vue';

/* eslint-disable no-new */
new Vue({
  el: '#app',
  render: h => h(Overlay),
});

