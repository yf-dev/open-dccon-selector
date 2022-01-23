<template>
  <div class="dccon">
    <img
      class="image"
      loading="lazy"
      width="32px"
      height="32px"
      :src="dccon.path"
      :alt="dccon.keywords[0]"
      @click.prevent="clicked"
      @mouseover="hovered">
  </div>
</template>

<script>
  // noinspection JSUnusedGlobalSymbols
  export default {
    name: 'dccon',
    props: {
      dccon: {
        type: Object,
        default: Object,
      },
    },
    data() {
      return {};
    },
    created() {

    },
    methods: {
      clicked() {
        this.$emit('click', this.dccon);
      },
      hovered() {
        this.$emit('hover', this.dccon);
      },
    },
  };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
  .dccon {
    display: inline-block;
    padding: 0;
    margin: 0;
    cursor: pointer;
  }
  .image {
    width: 32px;
    height: 32px;
  }

  .dccon:hover .image {
  -moz-transform: scale(1.2);
  -webkit-transform: scale(1.2);
  transform: scale(1.2);
}
</style>
