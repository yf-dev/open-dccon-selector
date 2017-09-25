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
</script>

<style lang="scss">
  @import "~typeface-nanum-barun-gothic/nanumbarungothic.css";

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
