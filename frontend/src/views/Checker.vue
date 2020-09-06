<template>
  <div id="checker">
    <div id="mySidenav" class="sidenav">
      <a href="javascript:void(0)" class="closebtn" @click="closeNav">&times;</a>
      <a href="#">MailChcker</a>
      <a href="#" class="sid">Possible views</a>
      <a href="#" class="sid">Possible views</a>
      <a href="#" class="sid">Possible views</a>
    </div>

    <div id="main">
      <div id="title">
        <span style="font-size: 20px; cursor: pointer" @click="openNav">&#9776; About</span>
        <h1>MailChcker</h1>
        <h4>
          <b>Line_1</b>
          ,
          <b>Line_2</b>
        </h4>
      </div>

      <div class="container">
        <h2>MailChcker</h2>
        <form>
          <div class="input-field">
            <textarea required="required" name="query" autofocus></textarea>
            <label for="">Type in mail text for identify</label>
            <span></span>
          </div>
          <input type="submit" value="Show Result" class="btn" @click="getPredicted" />
        </form>
      </div>

      <div id="output">
        <h3>Predict</h3>
        <div>
          <textarea id="content" readonly v-text="serverResponse"></textarea>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Checker',
  data: function() {
    return {
      serverResponse: 'Click to get prediction'
    };
  },
  methods: {
    openNav() {
      document.getElementById('mySidenav').style.width = '250px';
      document.getElementById('main').style.marginLeft = '250px';
      document.getElementById('checker').style.backgroundColor = 'rgba(17, 17, 17, 0.8)';
    },
    closeNav() {
      document.getElementById('mySidenav').style.width = '0';
      document.getElementById('main').style.marginLeft = '0';
      document.getElementById('checker').style.backgroundColor = 'rgba(17, 17, 17, 1)';
    },
    TextAreagoEnd() {
      var textArea = document.getElementById('content');
      textArea.scrollTop = textArea.scrollHeight;
    },
    getPredicted() {
      // 对应 Python 提供的接口，这里的地址填写下面服务器运行的地址，本地则为127.0.0.1，外网则为 your_ip_address
      const path = 'http://127.0.0.1:5000/getMsg';
      axios
        .get(path)
        .then((response) => {
          // 这里服务器返回的 response 为一个 json object，可通过如下方法需要转成 json 字符串
          // 可以直接通过 response.data 取key-value
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
  background: #111;
}

#title {
  color: rgb(202, 194, 194);
  margin-bottom: 20px;
}

.container {
  border-radius: 15px;
  position: relative;
  width: 700px;
  padding: 20px;
  background: #151515;
}

.container h2 {
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
  background: #00b0ff;
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
  background: #00bcd4;
}

#output {
  margin-top: 20px;
  color: #999;
  height: auto;
}

#output div {
  border: 0;
  border-radius: 20px;
  background-color: #151515;
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
