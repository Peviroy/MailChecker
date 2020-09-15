<template>
  <v-container id="dashboard" fluid tag="section">
    <inoutputer v-on:get-result="getPredicted" :serverResponse="serverResponse"></inoutputer>
  </v-container>
</template>

<script>
import inoutputer from '@/components/inoutPuter';
import axios from 'axios';

export default {
  name: 'DashboardDashboard',

  components: {
    inoutputer
  },

  data() {
    return {
      serverResponse: 'Click to get prediction'
    };
  },

  methods: {
    getPredicted(postMsg) {
      let baseURL = process.env.VUE_APP_BASEURL;
      const path = baseURL + '/getPredict';

      axios
        .post(path, postMsg)
        .then((response) => {
          var prediction = response.data.msg;
          var prob = response.data.prob;

          var display;
          if (postMsg.model === 'Model1') {
            display = `${prediction.toUpperCase()}     Score  ${prob.toFixed(4) * 100}`;
          } else {
            display = `${prediction.toUpperCase()}`;
          }
          this.serverResponse = display;
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  }
};
</script>
<style lang="scss"></style>
