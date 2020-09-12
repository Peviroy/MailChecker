<template>
  <div id="word-analysis">
    <ve-line :data="chartData" height="400px"></ve-line>
    <ve-histogram :data="chartData" height="400px"></ve-histogram>
  </div>
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
      }
    };
  }
};
</script>

<style scoped>
#word-analysis {
  width: 100%;
}
</style>
