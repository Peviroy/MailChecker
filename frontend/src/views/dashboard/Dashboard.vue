<template>
  <v-container id="dashboard" fluid tag="section">
    <v-container id="inoutputer">
      <div id="main">
        <h2 class="myTitle">{{ titleInput }}</h2>

        <div class="iContainer">
          <h2 class="iContainer__innerTitle">{{ titleInnerInput }}</h2>

          <form>
            <div class="iContainer__inputField">
              <textarea required="required" name="query" autofocus v-model="mailcontent_input"></textarea>
              <label>Type in mail text for identify</label>
              <span></span>
            </div>

            <v-container id="iContainer__modelSelector">
              <v-overflow-btn
                class="my-2"
                :items="dropdown_selector"
                label="Choose a model"
                target="#iContainer__modelSelector"
                dense
                loading
                menu-props="top"
                v-model="selected_model"
              ></v-overflow-btn>
            </v-container>
            <input type="submit" value="Show Result" class="iContainer__btn" @click="getPredicted" />
          </form>
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
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DashboardDashboard',

  data() {
    return {
      titleInput: 'MailChecker',
      titleInnerInput: 'MailChecker',
      titleInnerOutput: '',
      titleOutput: 'Predict',

      serverResponse: 'Click to get prediction',
      dropdown_selector: ['Model1', 'Model2'],

      mailcontent_input: null,
      selected_model: null
    };
  },
  methods: {
    getPredicted(event) {
      event.preventDefault();
      let baseURL = process.env.VUE_APP_BASEURL;
      const path = baseURL + '/getPredict';
      console.log(baseURL);

      axios
        .post(path, {
          content: this.mailcontent_input,
          model: this.selected_model
        })
        .then((response) => {
          var prediction = response.data.msg;
          var prob = response.data.prob;

          var display;
          if (this.selected_model === 'Model1') {
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
<style lang="scss">
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
  background: rgb(255, 227, 171); // containerColor
  margin-bottom: 20px;

  /* container inner title */
  &__innerTitle {
    color: #999; //innerTitleColor
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
    background: rgb(255, 181, 30); // buttonBackground
    color: #fff; // buttonFont
    font-size: 16px;
    cursor: pointer;

    &:hover {
      background: rgb(206, 191, 191); // buttonHover
    }
  }
}

/* sub of input-container */
.iContainer__inputField {
  position: relative;
  height: 220px;
  width: 100%;

  /* label for input area */
  label {
    position: absolute;
    top: 0;
    left: 0;
    color: #555; // labelColor_before
    pointer-events: none;
    display: block;
    transition: 0.5s;
    letter-spacing: 1px;
  }

  /* input area */
  textarea {
    position: absolute;
    background: transparent;
    box-shadow: none;
    border: none;
    font-size: 16px;
    color: rgb(0, 0, 0); // fontColor
    width: 100%;
    height: 210px;
    outline: none;
    resize: none;
    overflow: hidden;
    line-height: 24px;

    &:focus + label,
    &:valid + label {
      transform: translateY(-35px);
      font-size: 14px;
      color: rgb(0, 0, 0); // labelColorAfter
      background: #ff006a; // labelBackground
      padding: 5px 2px;
    }

    &:focus ~ span:before,
    &:valid ~ span:before {
      transform: scaleX(1);
      transform-origin: right;
      transition: transform 0.5s ease-in-out;
    }
  }

  /* marker bar of inputFiled */
  span {
    position: absolute;
    bottom: 0;
    right: 0;
    display: block;
    background: #555; // lineColor_before
    width: 100%;
    height: 2px;

    &:before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgb(255, 181, 30); // lineColor_after
      transform: scaleX(0);
      transform-origin: right;
      transition: transform 0.5s ease-in-out;
    }
  }
}

/* output-container */
.oContainer {
  color: #999; // font containerColor
  height: auto;

  border: 0;
  border-radius: 20px;
  background-color: rgb(255, 227, 171); //  containerColor
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
