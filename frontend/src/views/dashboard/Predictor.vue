<template>
  <v-container id="dashboard" fluid tag="section">
    <inoutputer
      v-on:get-result="getPredicted"
      :serverResponses="serverResponses"
      :serverPictures="serverPictures"
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
      serverResponses: ['Click to get prediction'],
      serverPictures: [],
      predictions: {}
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
          var images = response.data.images;
          var images_name = response.data.images_name;
          console.log(images_name);

          var decoded_images = [];
          console.log('Decoding imageing');
          images.forEach((image, index) => {
            let decoded_img_string = 'data:image/jpeg;base64,' + image;
            decoded_images[index] = decoded_img_string;
          });

          this.serverResponses = images_name;
          this.serverPictures = decoded_images;
        })
        .catch(function (error) {
          console.log(error);
        });
    }
  }
};
</script>
<style lang="scss"></style>
