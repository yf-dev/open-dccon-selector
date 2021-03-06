<template>
  <div id="viewer" class="app">
    <div class="container" @mouseleave="containerMouseLeave" @mousemove="containerMouseMove">
      <div :class="{'invisible': !isHovered || dccons.length === 0, 'visible': isHovered && dccons.length !== 0}">
        <button class="btn" @click.prevent="toggle">
          <i class="icon" :class="{'icon-cross': isOpened, 'icon-menu': !isOpened}"></i>
        </button>
        <p class="notice" :class="{'invisible': !isNotified, 'visible': isNotified}">{{notice}}</p>
        <div class="float-view" :class="{'hide': !isOpened}">
          <div class="dccon-scroll" @mouseout="dcconContainerMouseOut">
            <div class="dccon-container">
              <dccon v-for="dccon in dccons" :key="dccon.keywords[0]" :dccon="dccon"
                     @click="clickDccon" @hover="hoverDccon"/>
            </div>
          </div>
          <div class="preview" v-if="hoveredDccon !== null">
            <img :src="hoveredDccon.path" :alt="hoveredDccon.keywords[0]">
          </div>
        </div>
      </div>
      <button ref="clipboard" class="clipboard" :data-clipboard-text="textForCopy"></button>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import Clipboard from 'clipboard';
  import _ from 'lodash';
  import Dccon from './Dccon.vue';
  import getParameterByName from '../../util';

  // noinspection JSUnusedGlobalSymbols
  export default {
    name: 'overlay',
    components: {
      Dccon,
    },
    data() {
      return {
        auth: {},
        isHovered: false,
        isNotified: false,
        isOpened: false,
        notice: '',
        dccons: [],
        hoveredDccon: null,
        isDcconLoading: false,
        textForCopy: '',
      };
    },
    created() {
      if (window.Twitch.ext) {
        this.auth.channelId = getParameterByName('id');
        if (this.auth.channelId !== null) {
          this.getDcconsFromUrl();
        }
        window.Twitch.ext.onAuthorized((auth) => {
          this.auth = auth;
          if (!this.isDcconLoading && this.dccons.length === 0) {
            this.getDcconsFromUrl();
          }
        });
      }

      // eslint-disable-next-line no-unused-vars
      const clipboard = new Clipboard('.clipboard');
    },
    methods: {
      getDcconsFromUrl() {
        this.isDcconLoading = true;
        axios.get(`https://${process.env.API_HOSTNAME}/api/channel/${this.auth.channelId}/proxy-dccon`)
          .then((response) => {
            this.dccons = response.data.dccons;
            this.isDcconLoading = false;
          })
          .catch(() => {
            this.dccons = []
            this.isDcconLoading = false;
          });
      },
      toggle() {
        if (this.isOpened) {
          this.isOpened = false;
        } else {
          this.isOpened = true;
        }
      },
      hoverDccon(dccon) {
        this.hoveredDccon = dccon;
      },
      clickDccon(dccon) {
        this.copy(dccon.keywords[0]);
      },
      copy(keyword) {
        this.textForCopy = `~${keyword}`;
        this.notice = `${this.textForCopy} Copied`;
        this.isNotified = true;
        this.hideNotice();
        this.$nextTick(function f() {
          this.$refs.clipboard.click();
        });
      },
      hideNotice: _.debounce(function hideNoticeInner() {
        if (this.isNotified) {
          this.isNotified = false;
        }
      }, 3000),
      dcconContainerMouseOut() {
        this.hoveredDccon = null;
      },
      containerMouseLeave() {
        this.isHovered = false;
      },
      // eslint-disable-next-line prefer-arrow-callback
      debouncedContainerMouseLeave: _.debounce(function containerMouseLeaveInner() {
        this.isHovered = false;
      }, 5000),
      containerMouseMove() {
        this.isHovered = true;
        this.debouncedContainerMouseLeave();
      },
    },
  };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
  @import "~spectre.css/dist/spectre.css";
  @import "~spectre.css/dist/spectre-exp.css";
  @import "~spectre.css/dist/spectre-icons.css";

  $height-factor: 3.5;
  $width-factor: 12;

  .container {
    padding: 100px 16px 80px 8px;
    min-height: 100vh;
  }

  .clipboard {
    display: none;
  }

  .float-view {
    margin-top: 8px;
  }

  .dccon-scroll {
    display: inline-block;
    max-width: 32px * $width-factor + 4px * 2 + 20px;
    max-height: 32px * $height-factor + 4px * 2;
    overflow-x: hidden;
    overflow-y: scroll;
    background: rgba(255, 255, 255, 0.5);
    padding: 4px;
    border-radius: 2px;
  }

  .dccon-container {
    line-height: 0;
    min-height: 32px * $height-factor + 4px * 2;
  }

  .preview {
    display: inline-block;
  }

  .preview > img {
    height: 32px * $height-factor + 4px * 2;
  }

  .hide {
    display: none;
  }

  .invisible {
    visibility: hidden;
    opacity: 0;
    transition: visibility 0s 0.2s, opacity 0.2s linear;
  }

  .visible {
    visibility: visible;
    opacity: 1;
    transition: opacity 0.2s linear;
  }

  .notice {
    display: inline-block;
    margin-bottom: 0;
    background: rgba(255, 255, 255, 0.5);
    padding: 4px 8px;
    color: #000000;
    border-radius: 4px;
    margin-left: 8px;
  }
</style>
