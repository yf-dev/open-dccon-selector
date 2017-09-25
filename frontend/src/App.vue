<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
  // noinspection JSUnusedGlobalSymbols
  export default {
    name: 'app',
  };

  let p = location.pathname.split('/');
  p.pop();
  p = `${p.join('/')}/static/typeface-nanum-barun-gothic/nanumbarungothic.css`;
  const link = document.createElement('link');
  link.href = p;
  link.type = 'text/css';
  link.rel = 'stylesheet';
  document.getElementsByTagName('head')[0].appendChild(link);
</script>

<style lang="scss">

  #app {
    min-height: 100%;
    font-family: 'Nanum Barun Gothic', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  body {
    background: transparent !important;
  }
</style>
