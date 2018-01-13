<template>
  <div id="config" class="app">
    <div class="background">
      <div class="container">
        <div class="columns">
          <div class="form-group">
            <label class="form-label" for="input-dccon-url">Dccon URL (Required)</label>
            <input class="form-input" type="text" id="input-dccon-url" placeholder="https://..."
                   @input="inputDcconUrl" :value="channelData.dccon_url"/>
          </div>
          <div class="form-group">
            <label class="form-label" for="input-dccon-type">Dccon Type</label>
            <select class="form-select" id="input-dccon-type" v-model="selectedDcconType">
              <option v-for="dcconType in dcconTypes" :value="dcconType.key">{{dcconType.name}}</option>
            </select>
          </div>
        </div>
        <div class="columns">
          <div class="form-group button-group">
            <label class="form-switch">
              Cache Dccon data to server
              <input :disabled="selectedDcconType !== 'open_dccon'" type="checkbox" v-model="checkboxCache">
              <i class="form-icon"></i>
            </label>
          </div>
        </div>
        <div class="columns button-group">
          <button class="btn btn-primary" :class="{'disabled': isUpdating || !canSubmit}" @click.prevent="submit">
            Submit
          </button>
          <p class="result" v-if="submitResult">{{ submitResult }}</p>
        </div>
        <div class="divider"></div>
        <div class="columns button-group">
          <button class="btn" :disabled="isUpdating || !canTest" @click.prevent="testData">Test data format
          </button>
          <p class="result" v-if="testResult">{{ testResult }}</p>
        </div>
        <div class="columns button-group">
          <button class="btn" :disabled="isUpdating || !checkboxCache" @click.prevent="updateCache">
            Update cached Dccon data
          </button>
          <p class="result" v-if="updateCacheResult">{{ updateCacheResult }}</p>
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
        selectedDcconType: 'open_dccon',
        checkboxCache: true,
        dcconTypes: [
          {
            key: 'open_dccon',
            name: 'Open Dccon Format',
          },
          {
            key: 'open_dccon_rel_path',
            name: 'Open Dccon Format (Relative path)',
          },
          {
            key: 'funzinnu',
            name: 'Funzinnu Dccon Format',
          },
          {
            key: 'telk',
            name: 'Telk Dccon Format',
          },
        ],
        channelData: {},
        submitResult: '',
        testResult: '',
        updateCacheResult: '',
        isUpdating: true,
        canSubmit: false,
        canTest: true,
        canUpdateCache: true,
      };
    },
    watch: {
      selectedDcconType(newValue) {
        this.channelData.dccon_type = newValue;
        if (newValue !== 'open_dccon') {
          this.checkboxCache = true;
        }
      },
      checkboxCache(newValue) {
        this.channelData.is_using_cache = newValue;
      },
      channelData(newValue) {
        this.selectedDcconType = newValue.dccon_type;
        if (newValue.dccon_type !== 'open_dccon') {
          this.checkboxCache = true;
        } else {
          this.checkboxCache = newValue.is_using_cache;
        }
      },
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
              this.submitResult = 'Cannot connect to server';
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
        this.submitResult = '';
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
            this.submitResult = 'Server Error';
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
        this.submitResult = '';
        axios.put(
          `https://${process.env.API_HOSTNAME}/api/channel/${this.auth.channelId}`,
          {
            token: this.auth.token,
            dccon_url: this.channelData.dccon_url,
            dccon_type: this.channelData.dccon_type,
            is_using_cache: this.channelData.is_using_cache,
          },
        )
          .then((response) => {
            this.channelData = response.data;
            this.submitResult = 'Saved';
            this.isUpdating = false;
            this.canSubmit = true;
          })
          .catch(() => {
            this.submitResult = 'Server Error';
            this.isUpdating = false;
            this.canSubmit = true;
          });
      },
      requestTestDcconData() {
        if (this.isUpdating) {
          return;
        }
        this.isUpdating = true;
        this.canTest = false;
        this.testResult = '';
        axios.get(
          `https://${process.env.API_HOSTNAME}/api/convert-dccon-url?type=${this.channelData.dccon_type}&url=${encodeURIComponent(this.channelData.dccon_url)}`,
        )
          .then(() => {
            this.testResult = 'OK';
            this.isUpdating = false;
            this.canTest = true;
          })
          .catch((error) => {
            this.testResult = `Error: ${JSON.stringify(error.response.data)}`;
            this.isUpdating = false;
            this.canTest = true;
          });
      },
      requestUpdateCacheDcconData() {
        if (this.isUpdating) {
          return;
        }
        this.isUpdating = true;
        this.canUpdateCache = false;
        this.updateCacheResult = '';
        axios.post(
          `https://${process.env.API_HOSTNAME}/api/channel/${this.auth.channelId}/cached-dccon/update`,
          {
            token: this.auth.token,
          },
        )
          .then(() => {
            this.updateCacheResult = 'OK';
            this.isUpdating = false;
            this.canUpdateCache = true;
          })
          .catch((error) => {
            this.updateCacheResult = `Error: ${JSON.stringify(error.response.data)}`;
            this.isUpdating = false;
            this.canUpdateCache = true;
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
      testData() {
        if (this.canTest) {
          this.requestTestDcconData();
        }
      },
      updateCache() {
        if (this.canUpdateCache) {
          this.requestUpdateCacheDcconData();
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

  .result {
    line-height: 1.6rem;
    padding-left: 16px;
  }

  .form-group {
    width: 100%;
  }

  .button-group {
    margin-top: 16px;
  }

  .divider {
    margin-top: 8px;
  }
</style>
