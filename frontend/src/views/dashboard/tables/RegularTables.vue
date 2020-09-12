<template>
  <v-container id="regular-tables" fluid tag="section">
    <!-- <base-v-component heading="Simple Tables" link="components/simple-tables" /> -->

    <base-material-card icon="mdi-clipboard-text" title="正常邮件展示" class="px-5 py-3">
      <v-simple-table>
        <thead>
          <tr>
            <th class="primary--text">ID</th>
            <th class="primary--text">类型</th>
            <th class="primary--text">正文</th>
          </tr>
        </thead>

        <tbody>
          <tr>
            <td>1</td>
            <td>ham</td>
            <td class="text-left">{{ message1 }}</td>
          </tr>
          <tr>
            <td>2</td>
            <td>ham</td>
            <td class="text-left">{{ message2 }}</td>
          </tr>
          <tr>
            <td>3</td>
            <td>ham</td>
            <td class="text-left">{{ message3 }}</td>
          </tr>
          <tr>
            <td>4</td>
            <td>ham</td>
            <td class="text-left">{{ message4 }}</td>
          </tr>
          <tr>
            <td>5</td>
            <td>ham</td>
            <td class="text-left">{{ message5 }}</td>
          </tr>
        </tbody>
      </v-simple-table>
    </base-material-card>

    <div class="py-3" />

    <base-material-card color="success" dark icon="mdi-clipboard-plus" title="垃圾邮件展示" class="px-5 py-3">
      <v-simple-table>
        <thead>
          <tr>
            <th class="primary--text">ID</th>
            <th class="primary--text">类型</th>
            <th class="primary--text">正文</th>
          </tr>
        </thead>

        <tbody>
          <tr>
            <td>1</td>
            <td>spam</td>
            <td class="text-left">{{ message6 }}</td>
          </tr>
          <tr>
            <td>2</td>
            <td>spam</td>
            <td class="text-left">{{ message7 }}</td>
          </tr>
          <tr>
            <td>3</td>
            <td>spam</td>
            <td class="text-left">{{ message8 }}</td>
          </tr>
          <tr>
            <td>4</td>
            <td>spam</td>
            <td class="text-left">{{ message9 }}</td>
          </tr>
          <tr>
            <td>5</td>
            <td>spam</td>
            <td class="text-left">{{ message10 }}</td>
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
      message1: '',
      message2: '',
      message3: '',
      message4: '',
      message5: '',
      message6: '',
      message7: '',
      message8: '',
      message9: '',
      message10: ''
    };
  },
  created() {
    //console.log('created');
    const path = 'http://127.0.0.1:5000/getCsv';
    axios
      .get(path)
      .then((response) => {
        var list = response.data;
        this.message1 = list.message1;
        this.message2 = list.message2;
        this.message3 = list.message3;
        this.message4 = list.message4;
        this.message5 = list.message5;
        this.message6 = list.message6;
        this.message7 = list.message7;
        this.message8 = list.message8;
        this.message9 = list.message9;
        this.message10 = list.message10;
        console.log('前端');
        console.log(list);
      })
      .catch(function(error) {
        console.log(error);
      });
  }
};
</script>
