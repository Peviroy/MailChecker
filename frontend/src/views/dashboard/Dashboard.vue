<template>
  <v-container id="dashboard" fluid tag="section">
    <v-row id="checker">
      <div id="main">
        <div id="title">
          <h1>MailChecker</h1>
        </div>

        <div class="container1">
          <h2>MailChecker</h2>

          <form>
            <div class="input-field">
              <textarea required="required" name="query" autofocus v-model="mailcontent"></textarea>
              <label for>Type in mail text for identify</label>
              <span></span>
            </div>

            <div id="choose">
              <input type="radio" id="one" value="One" v-model="picked" />
              <label for="one">模型1</label>
              <br />
              <input type="radio" id="two" value="Two" v-model="picked" />
              <label for="two">模型2</label>
              <br />
              <span>selected: {{ picked }}</span>
            </div>
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

    <v-row>
      <v-col cols="12" lg="4">
        <base-material-chart-card
          :data="emailsSubscriptionChart.data"
          :options="emailsSubscriptionChart.options"
          :responsive-options="emailsSubscriptionChart.responsiveOptions"
          color="#E91E63"
          hover-reveal
          type="Bar"
        >
          <template v-slot:reveal-actions>
            <v-tooltip bottom>
              <template v-slot:activator="{ attrs, on }">
                <v-btn v-bind="attrs" color="info" icon v-on="on">
                  <v-icon color="info">
                    mdi-refresh
                  </v-icon>
                </v-btn>
              </template>

              <span>Refresh</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ attrs, on }">
                <v-btn v-bind="attrs" light icon v-on="on">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
              </template>

              <span>Change Date</span>
            </v-tooltip>
          </template>

          <h4 class="card-title font-weight-light mt-2 ml-2">
            Website Views
          </h4>

          <p class="d-inline-flex font-weight-light ml-2 mt-1">
            Last Campaign Performance
          </p>

          <template v-slot:actions>
            <v-icon class="mr-1" small>
              mdi-clock-outline
            </v-icon>
            <span class="caption grey--text font-weight-light">updated 10 minutes ago</span>
          </template>
        </base-material-chart-card>
      </v-col>

      <v-col cols="12" lg="4">
        <base-material-chart-card
          :data="dailySalesChart.data"
          :options="dailySalesChart.options"
          color="success"
          hover-reveal
          type="Line"
        >
          <template v-slot:reveal-actions>
            <v-tooltip bottom>
              <template v-slot:activator="{ attrs, on }">
                <v-btn v-bind="attrs" color="info" icon v-on="on">
                  <v-icon color="info">
                    mdi-refresh
                  </v-icon>
                </v-btn>
              </template>

              <span>Refresh</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ attrs, on }">
                <v-btn v-bind="attrs" light icon v-on="on">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
              </template>

              <span>Change Date</span>
            </v-tooltip>
          </template>

          <h4 class="card-title font-weight-light mt-2 ml-2">
            Daily Sales
          </h4>

          <p class="d-inline-flex font-weight-light ml-2 mt-1">
            <v-icon color="green" small>
              mdi-arrow-up
            </v-icon>
            <span class="green--text">55%</span>
            &nbsp; increase in today's sales
          </p>

          <template v-slot:actions>
            <v-icon class="mr-1" small>
              mdi-clock-outline
            </v-icon>
            <span class="caption grey--text font-weight-light">updated 4 minutes ago</span>
          </template>
        </base-material-chart-card>
      </v-col>

      <v-col cols="12" lg="4">
        <base-material-chart-card
          :data="dataCompletedTasksChart.data"
          :options="dataCompletedTasksChart.options"
          hover-reveal
          color="info"
          type="Line"
        >
          <template v-slot:reveal-actions>
            <v-tooltip bottom>
              <template v-slot:activator="{ attrs, on }">
                <v-btn v-bind="attrs" color="info" icon v-on="on">
                  <v-icon color="info">
                    mdi-refresh
                  </v-icon>
                </v-btn>
              </template>

              <span>Refresh</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ attrs, on }">
                <v-btn v-bind="attrs" light icon v-on="on">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
              </template>

              <span>Change Date</span>
            </v-tooltip>
          </template>

          <h3 class="card-title font-weight-light mt-2 ml-2">
            Completed Tasks
          </h3>

          <p class="d-inline-flex font-weight-light ml-2 mt-1">
            Last Last Campaign Performance
          </p>

          <template v-slot:actions>
            <v-icon class="mr-1" small>
              mdi-clock-outline
            </v-icon>
            <span class="caption grey--text font-weight-light">campaign sent 26 minutes ago</span>
          </template>
        </base-material-chart-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DashboardDashboard',

  data() {
    return {
      serverResponse: 'Click to get prediction2',
      picked: '',
      mailcontent: '',

      dailySalesChart: {
        data: {
          labels: ['M', 'T', 'W', 'T', 'F', 'S', 'S'],
          series: [[12, 17, 7, 17, 23, 18, 38]]
        },
        options: {
          lineSmooth: this.$chartist.Interpolation.cardinal({
            tension: 0
          }),
          low: 0,
          high: 50, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
          chartPadding: {
            top: 0,
            right: 0,
            bottom: 0,
            left: 0
          }
        }
      },
      dataCompletedTasksChart: {
        data: {
          labels: ['12am', '3pm', '6pm', '9pm', '12pm', '3am', '6am', '9am'],
          series: [[230, 750, 450, 300, 280, 240, 200, 190]]
        },
        options: {
          lineSmooth: this.$chartist.Interpolation.cardinal({
            tension: 0
          }),
          low: 0,
          high: 1000, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
          chartPadding: {
            top: 0,
            right: 0,
            bottom: 0,
            left: 0
          }
        }
      },
      emailsSubscriptionChart: {
        data: {
          labels: ['Ja', 'Fe', 'Ma', 'Ap', 'Mai', 'Ju', 'Jul', 'Au', 'Se', 'Oc', 'No', 'De'],
          series: [[542, 443, 320, 780, 553, 453, 326, 434, 568, 610, 756, 895]]
        },
        options: {
          axisX: {
            showGrid: false
          },
          low: 0,
          high: 1000,
          chartPadding: {
            top: 0,
            right: 5,
            bottom: 0,
            left: 0
          }
        },
        responsiveOptions: [
          [
            'screen and (max-width: 640px)',
            {
              seriesBarDistance: 5,
              axisX: {
                labelInterpolationFnc: function(value) {
                  return value[0];
                }
              }
            }
          ]
        ]
      }
    };
  },

  methods: {
    getRadioVal() {
      console.log(this.radioVal);
    },
    TextAreagoEnd() {
      var textArea = document.getElementById('content');
      textArea.scrollTop = textArea.scrollHeight;
    },
    getPredicted(event) {
      event.preventDefault();
      // 对应 Python 提供的接口，这里的地址填写下面服务器运行的地址，本地则为127.0.0.1，外网则为 your_ip_address
      const path = 'http://127.0.0.1:5000/getPredict';
      axios
        .post(path, {
          content: this.mailcontent,
          model: this.picked
        })
        .then((response) => {
          // 这里服务器返回的 response 为一个 json object，可通过如下方法需要转成 json 字符串
          // 可以直接通过 response.data 取key-value
          var prediction = response.data.msg;
          var prob = response.data.prob;

          var display;
          if (this.picked === 'Two') {
            display = `${prediction.toUpperCase()}`;
          } else {
            display = `${prediction.toUpperCase()}     Score  ${prob.toFixed(4) * 100}`;
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
  color: #fff;
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
  color: #fff;
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
  background: #333;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
}

.btn:hover {
  background: rgb(255, 181, 30);
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

  color: rgb(206, 191, 191);
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
