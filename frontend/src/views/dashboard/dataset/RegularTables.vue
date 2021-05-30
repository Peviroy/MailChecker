<template>
  <v-container id="regular-tables" fluid tag="section">
    <base-material-card icon="mdi-clipboard-text" title="正常邮件展示" class="px-5 py-3">
      <v-simple-table>
        <thead>
          <tr>
            <th class="primary--text">ID</th>
            <th class="primary--text">正文</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="(message, index) in message0" :key="index">
            <td>{{ index + 1 }}</td>
            <td class="text-left">{{ message }}</td>
          </tr>
        </tbody>
      </v-simple-table>
    </base-material-card>

    <base-material-card color="success" dark icon="mdi-clipboard-plus" title="垃圾邮件展示" class="px-5 py-3">
      <v-simple-table>
        <thead>
          <tr>
            <th class="primary--text">ID</th>
            <th class="primary--text">正文</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="(message, index) in message1" :key="index">
            <td>{{ index + 1 }}</td>
            <td class="text-left">{{ message }}</td>
          </tr>
        </tbody>
      </v-simple-table>
    </base-material-card>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      message1: new Array(5).fill(''),
      message0: new Array(5).fill('')
    };
  },
  //页面创建时调用:
  created() {
    //console.log('created');
    let baseURL = process.env.VUE_APP_BASEURL;

    const path = baseURL + '/getCsv';
    axios
      .get(path)
      .then((response) => {
        var list = response.data;
        this.message1 = list.message1;
        this.message0 = list.message0;
      })
      .catch(function (error) {
        console.log(error);
      });
  }
};
</script>
