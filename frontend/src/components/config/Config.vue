<template>
  <div id="config" class="app">
    <div class="background">
      <div class="container">
        <div class="columns">
          <div class="form-group">
            <label class="form-label" for="inputDcconUrl">Dccon URL (Required)</label>
            <input class="form-input" type="text" id="inputDcconUrl" placeholder="https://..."
                   @input="inputDcconUrl" :value="channelData.dccon_url"/>
          </div>
        </div>
        <div class="columns submit-button-group">
          <button class="btn" :class="{'btn-primary': !isUpdating && canSubmit}" @click.prevent="submit">Submit</button>
          <p id="updateResult" v-if="result">{{ result }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import getParameterByName from '../../common';

  // noinspection JSUnusedGlobalSymbols
  export default {
    name: 'config',
    components: {},
    data() {
      return {
        auth: {},
        channelData: {},
        result: '',
        isUpdating: true,
        canSubmit: false,
      };
    },
    created() {
      if (window.Twitch.ext) {
        this.auth.channelId = getParameterByName('id');
        this.auth.token = getParameterByName('token');
        if (this.auth.channelId !== null && this.auth.token !== null) {
          this.getDcconUrl();
        }
        window.Twitch.ext.onAuthorized((auth) => {
          this.auth = auth;
          this.getDcconUrl();
        });
      }
    },
    methods: {
      getDcconUrl() {
        this.isUpdating = true;
        this.canSubmit = false;
        axios.get(
          `https://${process.env.API_HOSTNAME}/api/channel/${this.auth.channelId}?token=${this.auth.token}`,
        )
          .then((response) => {
            if (response.status === 200) {
              this.channelData = response.data;
              this.isUpdating = false;
              this.canSubmit = true;
            }
          })
          .catch((error) => {
            if (error.response.status === 404) {
              this.channelData = {};
              this.isUpdating = false;
              this.canSubmit = false;
              this.createChannel();
            } else {
              this.result = 'Cannot connect to server';
              this.isUpdating = false;
              this.canSubmit = false;
            }
          });
      },
      createChannel() {
        if (this.isUpdating) {
          return;
        }
        this.isUpdating = true;
        this.canSubmit = false;
        this.result = '';
        axios.post(
          `https://${process.env.API_HOSTNAME}/api/channels`,
          {
            token: this.auth.token,
          },
        )
          .then((response) => {
            this.channelData = response.data;
            this.isUpdating = false;
            this.canSubmit = true;
          })
          .catch(() => {
            this.result = 'Server Error';
            this.isUpdating = false;
            this.canSubmit = false;
          });
      },
      updateDcconUrl() {
        if (this.isUpdating) {
          return;
        }
        this.isUpdating = true;
        this.canSubmit = false;
        this.result = '';
        axios.put(
          `https://${process.env.API_HOSTNAME}/api/channel/${this.auth.channelId}`,
          {
            token: this.auth.token,
            dccon_url: this.channelData.dccon_url,
          },
        )
          .then((response) => {
            this.channelData = response.data;
            this.result = 'Saved';
            this.isUpdating = false;
            this.canSubmit = true;
          })
          .catch(() => {
            this.result = 'Server Error';
            this.isUpdating = false;
            this.canSubmit = true;
          });
      },
      inputDcconUrl(e) {
        this.channelData.dccon_url = e.target.value;
      },
      submit() {
        if (this.canSubmit) {
          this.updateDcconUrl();
        }
      },
    },
  };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
  @import "~spectre.css/dist/spectre.css";
  @import "~spectre.css/dist/spectre-exp.css";
  @import "~spectre.css/dist/spectre-icons.css";

  #updateResult {
    height: 1.6rem;
    line-height: 1.6rem;
    padding-left: 16px;
  }

  .form-group {
    width: 100%;
  }

  .submit-button-group {
    margin-top: 16px;
  }
</style>
