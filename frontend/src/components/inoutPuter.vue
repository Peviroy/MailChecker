<template>
  <v-container id="inoutputer">
    <div id="main">
      <h2 class="myTitle">{{ titleInput }}</h2>

      <div class="iContainer">
        <h2 class="iContainer__innerTitle">{{ titleInnerInput }}</h2>

      </div>

      <h3 class="myTitle">{{ titleOutput }}</h3>
      <div class="oContainer">
        <h2 class="oContainer__innerTitle">{{ titleInnerOutput }}</h2>
        <div>
          <textarea class="oContainer__content" readonly v-model="serverResponse"></textarea>
        </div>
      </div>
    </div>
  </v-container>
</template>

<script>
export default {
  name: 'inoutputer',

  props: {
    titleInput: {
      type: String,
      default: 'TextSpotter'
    },
    titleInnerInput: {
      type: String,
      default: 'Scene text sample'
    },
    titleInnerOutput: {
      type: String,
      default: ''
    },
    titleOutput: {
      type: String,
      default: 'Predict'
    },

    serverResponse: {
      type: String,
      default: 'Click to get prediction'
    },
    theme: {
      type: String,
      required: false
    }
  },

  data() {
    return {
      mailcontent_input: null,
      selected_model: null
    };
  },
  methods: {
    getResult(event) {
      event.preventDefault();

      let postMsg = {
        content: this.mailcontent_input,
        model: this.selected_model
      };

      this.$emit('get-result', postMsg);
    }
  }
};
</script>

<style lang="scss" scoped>
/* root */
#inoutputer {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: sans-serif;
  display: flex;
  justify-content: center;
  text-align: left;
  min-height: 100vh;
}

.myTitle {
  color: rgb(0, 0, 0); //titleColor
  margin-bottom: 20px;
}

/* input-container */
.iContainer {
  border-radius: 15px;
  position: relative;
  width: 700px;
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
