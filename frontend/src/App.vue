<template>
  <div id="app">
    <router-view />
  </div>
</template>

<style lang="scss">
/* global setting */
body {
  margin: 0;
  padding: 0;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

/* 选择历史记录的文字颜色和背景颜色 */
input:-webkit-autofill {
  -webkit-animation: autofill-fix 1s infinite !important;
  /* 选择历史记录的文字颜色*/
  -webkit-text-fill-color: #666;
  -webkit-transition: background-color 50000s ease-in-out 0s !important;
  transition: background-color 50000s ease-in-out 0s !important;
  background-color: transparent !important;
  background-image: none !important;
  /* 选择历史记录的背景颜色 */
  -webkit-box-shadow: 0 0 0 1000px transparent inset !important;
}
[role='button'],
a,
area,
button,
input:not([type='range']),
label,
select,
summary,
textarea {
  -ms-touch-action: manipulation;
  touch-action: manipulation;
}
input[type='number'],
input[type='password'],
input[type='text'],
textarea {
  -webkit-appearance: none;
}
</style>
