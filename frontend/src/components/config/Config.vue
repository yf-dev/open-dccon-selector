<template>
  <div class="background">
    <div class="container">
      <div class="columns">
        <div class="form-group">
          <label class="form-label" for="inputDcconUrl">Dccon URL (Required)</label>
          <input class="form-input" type="text" id="inputDcconUrl" placeholder="https://..."
                 @input="inputDcconUrl" :value="dcconUrl"/>
        </div>
      </div>
      <div class="columns submit-button-group">
        <button class="btn" :class="{'btn-primary': !isUpdating}" @click.prevent="submit">Submit</button>
        <p id="updateResult" v-if="result">{{ result }}</p>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';

  // noinspection JSUnusedGlobalSymbols
  export default {
    name: 'config',
    components: {},
    data() {
      return {
        auth: {},
        dcconUrl: '',
        result: '',
        isUpdating: true,
      };
    },
    created() {
      if (window.Twitch.ext) {
        window.Twitch.ext.onAuthorized((auth) => {
          this.auth = auth;
          this.getDcconUrl();
        });
      }
    },
    methods: {
      getDcconUrl() {
        axios.get(
          `https://${process.env.API_HOSTNAME}/api/dccon-url?token=${this.auth.token}`,
        )
          .then((response) => {
            if (response.status === 200) {
              this.dcconUrl = response.data.dccon_url;
            } else if (response.status === 404) {
              this.dcconUrl = '';
            }
            this.isUpdating = false;
          })
          .catch(() => {
            this.result = 'Cannot connect to server';
            this.isUpdating = false;
          });
      },
      updateDcconUrl() {
        this.isUpdating = true;
        this.result = '';
        axios.post(
          'https://${process.env.API_HOSTNAME}/api/update-dccon-url',
          {
            token: this.auth.token,
            dcconUrl: this.dcconUrl,
          },
        )
          .then((response) => {
            if (response.status === 204) {
              this.result = 'Saved';
            } else {
              this.result = 'Cannot Saved';
            }
            this.isUpdating = false;
          })
          .catch(() => {
            this.result = 'Server Error';
            this.isUpdating = false;
          });
      },
      inputDcconUrl(e) {
        this.dcconUrl = e.target.value;
      },
      submit() {
        if (!this.isUpdating) {
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
