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
        <div v-if="isPreview">
          <span v-for="url in img_urls" :key="`preview-${url}`">
            <v-img :src="url" />
          </span>
        </div>
        <div id="btnDiv">
          <input type="submit" value="Show Result" class="iContainer__btn" @click="getResult" />
          <input type="submit" value="Toggle Preview" class="iContainer__btn" @click="togglePreview" />
        </div>
      </div>

      <h3 class="myTitle">{{ titleOutput }}</h3>
      <div class="oContainer">
        <h2 class="oContainer__innerTitle">{{ titleInnerOutput }}</h2>
        <div class="d-flex flex-column justify-space-between align-center">
          <v-slider v-model="image_width" class="align-self-stretch" min="600" max="1000" step="10"></v-slider>
          <span v-for="data in serverData" :key="`output-${data.url}`">
            <h5 style="color: #000">{{ data.name }}</h5>
            <expandable-image :src="data.url" :width="image_width" />
          </span>
        </div>
      </div>
    </div>
  </v-container>
</template>

<script>
import ExpandableImage from '../views/dashboard/component/ExpandableImage';
export default {
  //Note: serverResponses not used for right now. Keep it for intergrating img display with img_name display
  name: 'inoutputer',

  components: {
    ExpandableImage
  },

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
      default: 'Predictions'
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
      myserverResponses: [],
      myserverPictures: [],
      isPreview: false,
      image_width: 1000
    };
  },
  methods: {
    onAddFiles(images) {
      this.images = images;
      this.img_urls = [];
      this.formData = new FormData();
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
      console.log(this.formData.get('images'));
      this.$emit('get-result', this.formData);
    },
    togglePreview(event) {
      event.preventDefault();
      this.isPreview = !this.isPreview;
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
  },

  computed: {
    serverData() {
      const data = [];
      for (let i = 0; i < this.myserverResponses.length; i++) {
        data.push({
          name: this.myserverResponses[i] || 'no name',
          url: this.myserverPictures[i]
        });
      }
      return data;
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
  width: 1050px;
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
    margin-top: 15px;
    border: none;
    border-radius: 15px;
    box-shadow: none;
    padding: 10px 15px;
    width: 140px;
    background: rgb(255, 210, 120); // buttonBackground
    color: #fff; // buttonFont
    font-size: 16px;
    cursor: pointer;

    &:hover {
      background: rgb(206, 191, 191); // buttonHover
    }
  }
}
#btnDiv {
  display: flex;
  justify-content: space-between;
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
