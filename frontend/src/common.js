import WebFont from 'webfontloader';
import Vue from 'vue';
import './common.scss';

Vue.config.productionTip = false;

WebFont.load({
  custom: {
    families: ['Spoqa Han Sans'],
    urls: ['/static/spoqa-han-sans/SpoqaHanSans-kr.css'],
  },
});
