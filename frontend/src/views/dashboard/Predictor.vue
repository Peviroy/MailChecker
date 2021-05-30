<template>
  <v-container id="dashboard" fluid tag="section">
    <inoutputer
      v-on:get-result="getPredicted"
      :serverResponse="serverResponse"
      :serverPicture="serverPicture"
    ></inoutputer>
  </v-container>
</template>

<script>
import inoutputer from '@/components/inoutPuter';
import axios from 'axios';

export default {
  name: 'DashboardPredictor',

  components: {
    inoutputer
  },

  data() {
    return {
      serverResponse: 'Click to get prediction',
      serverPicture: ''
    };
  },

  methods: {
    getPredicted(formData) {
      let baseURL = process.env.VUE_APP_BASEURL;
      const path = baseURL + '/photos/upload';

      axios
        .post(path, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then((response) => {
          console.log(response);
          var image = response.data.image;
          console.log(image);
          //var decoded_image = base64.b64decode(image);
          //console.log(decoded_image);
          var decoded_img_string = 'data:image/jpeg;base64,' + image;
          this.serverResponse = '111';
          this.serverPicture = decoded_img_string;
        })
        .catch(function (error) {
          console.log(error);
        });
    }
  }
};
</script>
<style lang="scss"></style>
