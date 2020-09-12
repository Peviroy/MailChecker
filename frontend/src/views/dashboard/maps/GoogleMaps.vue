<template>
  <el-container>
    <el-main>
      <div
        style="display: inline; float: left; width: 50%; height: 800px; border: #3b4151 solid 1px"
      >
        <ve-line :data="chartData" height="400px"></ve-line>
        <ve-histogram :data="chartData_1" height="400px"></ve-histogram>
      </div>
      <div style="display: inline;float: right; width: 50%; border: #3b4151 solid 1px">
        <ve-pie :data="chartData" height="400px"></ve-pie>
      </div>
    </el-main>
  </el-container>
</template>

<script>
export default {
  name: 'simple',
  data: function() {
    return {
      chartData: {
        columns: ['单词名称', 'spam单词', 'ham单词'],
        rows: [
          { 单词名称: 'CALL', spam单词: 347, ham单词: 638 },
          { 单词名称: 'win/won', spam单词: 223, ham单词: 334 },
          { 单词名称: 'FREE', spam单词: 199, ham单词: 265 },
          { 单词名称: 'MOBILE', spam单词: 147, ham单词: 162 },
          { 单词名称: 'Text', spam单词: 137, ham单词: 224 },
          { 单词名称: 'www', spam单词: 98, ham单词: 101 }
        ]
      },
      chartData_1: {
        columns: ['单词名称', 'spam单词', 'ham单词'],
        rows: [
          { 单词名称: 'CALL', spam单词: 347, ham单词: 638 },
          { 单词名称: 'win/won', spam单词: 223, ham单词: 334 },
          { 单词名称: 'FREE', spam单词: 199, ham单词: 265 },
          { 单词名称: 'MOBILE', spam单词: 147, ham单词: 162 },
          { 单词名称: 'Text', spam单词: 137, ham单词: 224 },
          { 单词名称: 'www', spam单词: 98, ham单词: 101 }
        ]
      },
      chartData_2: {
        columns: ['日期', '访问用户', '下单用户', '下单率'],
        rows: [
          { 日期: '1/1', 访问用户: 1393, 下单用户: 1093, 下单率: 0.32 },
          { 日期: '1/2', 访问用户: 3530, 下单用户: 3230, 下单率: 0.26 },
          { 日期: '1/3', 访问用户: 2923, 下单用户: 2623, 下单率: 0.76 },
          { 日期: '1/4', 访问用户: 1723, 下单用户: 1423, 下单率: 0.49 },
          { 日期: '1/5', 访问用户: 3792, 下单用户: 3492, 下单率: 0.323 },
          { 日期: '1/6', 访问用户: 4593, 下单用户: 4293, 下单率: 0.78 }
        ]
      }
    };
  }
};
</script>

<style scoped>
.el-header {
  background-color: #1f5dea;
  color: white;
  text-align: center;
  line-height: 60px;
  font-size: 24px;
}
</style>