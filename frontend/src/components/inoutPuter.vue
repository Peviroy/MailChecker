<template>
  <v-container id="inoutputer">
    <div id="main">
      <h2 class="myTitle">{{ titleInput }}</h2>

      <div class="iContainer">
        <h2 class="iContainer__innerTitle">{{ titleInnerInput }}</h2>

        <v-file-input
          label="Picture here"
          show-size
          small-chips
          multiple
          truncate-length="15"
          prepend-icon="mdi-camera"
          accept="image/png, image/jpeg"
          @change="onAddFiles"
        ></v-file-input>
        <span v-for="url in img_urls" :key="`preview-${url}`">
          <v-img :src="url" />
        </span>

        <input type="submit" value="Show Result" class="iContainer__btn" @click="getResult" />
      </div>

      <h3 class="myTitle">{{ titleOutput }}</h3>
      <div class="oContainer">
        <h2 class="oContainer__innerTitle">{{ titleInnerOutput }}</h2>
        <div>
          <!--TODO: Merge into a tableview <textarea class="oContainer__content" readonly v-model="myserverResponses[0]"></textarea> -->
          <span v-for="url in myserverPictures" :key="`output-${url}`">
            <v-img :src="url" />
          </span>
        </div>
      </div>
    </div>
  </v-container>
</template>

<script>
export default {
  //Note: serverResponses not used for right now. Keep it for intergrating img display with img_name display
  name: 'inoutputer',

  props: {
    titleInput: {
      type: String,
      default: 'TextSpotter'
    },
    titleInnerInput: {
      type: String,
      default: 'Upload scene text samples'
    },
    titleInnerOutput: {
      type: String,
      default: ''
    },
    titleOutput: {
      type: String,
      default: 'Predict'
    },
    serverResponses: {
      type: Array
    },
    serverPictures: {
      type: Array
    },
    theme: {
      type: String,
      required: false
    }
  },

  data() {
    return {
      img_urls: [],
      images: [],
      formData: new FormData(),
      myserverResponses: ['Click to get prediction'],
      myserverPictures: []
    };
  },
  methods: {
    onAddFiles(images) {
      this.images = images;
      this.img_urls = [];
      images.forEach((image, index) => {
        this.img_urls[index] = URL.createObjectURL(image);
        this.formData.append('images', image, image.name);
      });
      console.log('11');
      console.log(this.img_urls);
    },
    onUpload() {
      console.log(this.images);
    },
    getResult(event) {
      event.preventDefault();

      // var formData = new FormData();
      // if (this.images) {
      //   // images
      //   for (let image of this.images) {
      //     formData.append('images', image);
      //     console.log(image);
      //     console.log(image.name);
      //   }
      //   console.log(formData);
      // } else {
      //   console.log('no images specified.');
      // }

      // additional data
      console.log(this.formData.get('images'));
      this.$emit('get-result', this.formData);
    }
  },
  mounted() {
    this.myserverResponses = this.serverResponses;
    this.myserverPictures = this.serverPictures;
  },
  watch: {
    serverResponses() {
      this.myserverResponses = this.serverResponses;
    },
    serverPictures() {
      this.myserverPictures = this.serverPictures;
    }
  }
};
</script>

<style lang="scss" scoped>
/* root */
#inoutputer {
  padding: 0;
  box-sizing: border-box;
  font-family: sans-serif;
  display: flex;
  justify-content: center;
  text-align: left;
  min-height: 100vh;
}

#main {
  width: 1000px;
}

.myTitle {
  color: rgb(0, 0, 0); //titleColor
  margin-bottom: 20px;
}

/* input-container */
.iContainer {
  border-radius: 15px;
  position: relative;
  width: 100%;
  padding: 20px;
  background: rgb(247, 228, 190); // containerColor
  margin-bottom: 20px;

  /* container inner title */
  &__innerTitle {
    color: #333333; //innerTitleColor
    font-weight: lighter;
    margin-bottom: 40px;
    font-size: 1.2rem;
  }

  &__btn {
    margin-top: 20px;
    border: none;
    border-radius: 10px;
    box-shadow: none;
    padding: 10px 25px;
    background: rgb(255, 210, 120); // buttonBackground
    color: #fff; // buttonFont
    font-size: 16px;
    cursor: pointer;

    &:hover {
      background: rgb(206, 191, 191); // buttonHover
    }
  }
}

/* output-container */
.oContainer {
  color: #999; // font containerColor
  height: auto;
  padding: 20px;
  border: 0;
  border-radius: 20px;
  background-color: rgb(247, 228, 190); //  containerColor
  width: 100%;

  &__content {
    background-color: transparent;
    border: 0;
    width: 100%;
    height: 80px;

    color: rgb(0, 0, 0); // fontColor
    resize: none;
    outline: none;
    text-align: center;
    padding: 10px;
  }
}
</style>
