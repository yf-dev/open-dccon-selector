import Vue from 'vue';
import Config from './components/config/Config';
import Overlay from './components/overlay/Overlay';
import './common.scss';

Vue.config.productionTip = false;

const viewer = document.getElementById('viewer');
const config = document.getElementById('config');

if (viewer !== null) {
  /* eslint-disable no-new */
  new Vue({
    el: '#viewer',
    render: h => h(Overlay),
  });
}

if (config !== null) {
  /* eslint-disable no-new */
  new Vue({
    el: '#config',
    render: h => h(Config),
  });
}
