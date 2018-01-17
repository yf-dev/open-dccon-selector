import Vue from 'vue';
import './common';
import Config from './components/config/Config.vue';

/* eslint-disable no-new */
new Vue({
  el: '#app',
  render: h => h(Config),
});

