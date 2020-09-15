<template>
  <v-container id="Dash" fluid tag="section">
    <inoutputer
      v-on:get-result="getGenerated"
      :serverResponse="serverResponse"
      :titleOutput="titleOutput"
      :dropdown_selector="dropdown_selector"
    ></inoutputer>
  </v-container>
</template>

<script>
import inoutputer from '@/components/inoutPuter';
import axios from 'axios';

export default {
  name: 'DashboardIcons',

  components: {
    inoutputer
  },
  data() {
    return {
      titleOutput: 'Generate',
      serverResponse: 'Click to get prediction',
      dropdown_selector: ['Ham', 'Spam'],

      mailcontent_input: '',
      selected_model: null
    };
  },

  methods: {
    getGenerated(postMsg) {
      let baseURL = process.env.VUE_APP_BASEURL;
      const path = baseURL + '/getContent';

      axios
        .post(path, postMsg)
        .then((response) => {
          var msg = response.data.msg;
          this.serverResponse = msg;
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  }
};
</script>

<style></style>
