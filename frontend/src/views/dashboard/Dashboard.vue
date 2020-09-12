<template>
  <v-container id="dashboard" fluid tag="section">
    <v-row id="checker">
      <div id="main">
        <div class="container1">
          <h2>MailChecker</h2>

          <form>
            <div class="input-field">
              <textarea required="required" name="query" autofocus v-model="mailcontent_input"></textarea>
              <label for>Type in mail text for identify</label>
              <span></span>
            </div>

            <v-container id="model_selector_1">
              <v-overflow-btn
                class="my-2"
                :items="dropdown_selector"
                label="Choose a model"
                target="#model_selector_1"
                dense
                loading
                menu-props="top"
                v-model="selected_model"
              ></v-overflow-btn>
            </v-container>
            <!-- <div id="choose">
              <input type="radio" id="one" value="One" v-model="picked" />
              <label for="one">模型1</label>
              <br />
              <input type="radio" id="two" value="Two" v-model="picked" />
              <label for="two">模型2</label>
              <br />
              <span>selected: {{ picked }}</span>
            </div> -->
            <input type="submit" value="Show Result" class="btn" @click="getPredicted" />
          </form>
        </div>

        <div id="output">
          <h3>Predict</h3>
          <div>
            <textarea id="content" readonly v-model="serverResponse"></textarea>
          </div>
        </div>
      </div>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DashboardDashboard',

  data() {
    return {
      serverResponse: 'Click to get prediction',
      dropdown_selector: ['Model1', 'Model2'],

      mailcontent_input: null,
      selected_model: null
    };
  },
  methods: {
    getPredicted(event) {
      event.preventDefault();
      // 对应 Python 提供的接口，这里的地址填写下面服务器运行的地址，本地则为127.0.0.1，外网则为 your_ip_address
      // TODO: auto adjust url
      const path = 'http://127.0.0.1:5000/getPredict';
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
<style>
#checker {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: sans-serif;
  display: flex;
  justify-content: center;
  text-align: left;
  min-height: 100vh;
  background: rgb(rgb(0, 0, 0));
}

#title {
  color: rgb(0, 0, 0);
  margin-bottom: 20px;
}

.container1 {
  border-radius: 15px;
  position: relative;
  width: 700px;
  padding: 20px;
  background: rgb(255, 227, 171);
}

.container1 h2 {
  color: #999;
  font-weight: lighter;
  margin-bottom: 45px;
}

.input-field {
  position: relative;
  height: 220px;
  width: 100%;
}

.input-field label {
  position: absolute;
  top: 0;
  left: 0;
  color: #555;
  pointer-events: none;
  display: block;
  transition: 0.5s;
  letter-spacing: 1px;
}

.input-field textarea {
  position: absolute;
  background: transparent;
  box-shadow: none;
  border: none;
  font-size: 16px;
  color: rgb(0, 0, 0);
  width: 100%;
  height: 210px;
  outline: none;
  resize: none;
  overflow: hidden;
  line-height: 24px;
}

.input-field textarea:focus + label,
.input-field textarea:valid + label {
  transform: translateY(-35px);
  font-size: 14px;
  color: rgb(0, 0, 0);
  background: #ff006a;
  padding: 5px 2px;
}

.input-field span {
  position: absolute;
  bottom: 0;
  right: 0;
  display: block;
  background: #555;
  width: 100%;
  height: 2px;
}

.input-field span:before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgb(255, 181, 30);
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.5s ease-in-out;
}

.input-field textarea:focus ~ span:before,
.input-field textarea:valid ~ span:before {
  transform: scaleX(1);
  transform-origin: right;
  transition: transform 0.5s ease-in-out;
}

.btn {
  margin-top: 20px;
  border: none;
  border-radius: 10px;
  box-shadow: none;
  padding: 10px 25px;
  background: rgb(255, 181, 30);
  color: #fff;
  font-size: 16px;
  cursor: pointer;
}

.btn:hover {
  background: rgb(206, 191, 191);
}

#output {
  margin-top: 20px;
  color: #999;
  height: auto;
}

#output div {
  border: 0;
  border-radius: 20px;
  background-color: rgb(255, 227, 171);
  width: 100%;
}

#output textarea {
  background-color: transparent;
  border: 0;
  width: 100%;
  height: 80px;

  color: rgb(0, 0, 0);
  resize: none;
  outline: none;
  text-align: center;
  padding: 10px;
}

/* Sidebar */
#checker {
  transition: background-color 0.5s;
}

/*侧边栏选择器*/
.sidenav {
  height: 100%;
  width: 0; /*原始宽度*/
  position: fixed;
  /*z-index、top、left共同控制侧栏的悬浮（上方1，下方-1）*/
  z-index: 1;
  top: 0;
  left: 0;
  background-color: #111;
  overflow-x: hidden;
  transition: 0.5s; /*侧栏延迟0.5s显示*/
  padding-top: 60px;
}

/*侧边栏标签选择器*/
.sidenav a {
  padding: 8px 8px 8px 32px;
  text-decoration: none;
  font-size: 25px;
  color: #818181;
  display: block;
  transition: 0.3s; /*标签延迟0.3s显示*/
}

.sidenav a.sid {
  font-size: 15px;
}

.sidenav a:hover,
.offcanvas a:focus {
  color: #f1f1f1;
}

.sidenav .closebtn {
  position: absolute;
  top: 0;
  right: 25px;
  font-size: 36px;
  margin-left: 50px;
}

#main {
  transition: margin-left 0.5s;
  padding: 16px;
}

/*when page height < 450，adjust the padding as well as the font size of sidepar*/
@media screen and (max-height: 450px) {
  .sidenav {
    padding-top: 15px;
  }
  .sidenav a {
    font-size: 18px;
  }
}
</style>
