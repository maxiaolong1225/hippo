<template>
  <div id="app">
<!--    <img src="./assets/logo.png"> 来自App.vue组件-->
<!--    router-view 标签是出口 ，由router配置决定-->
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
/*
无用的css属性，需要移除
*/
/*#app {*/
/*  font-family: 'Avenir', Helvetica, Arial, sans-serif;*/
/*  -webkit-font-smoothing: antialiased;*/
/*  -moz-osx-font-smoothing: grayscale;*/
/*  text-align: center;*/
/*  color: #2c3e50;*/
/*  margin-top: 60px;*/
/*}*/
body{
    padding: 0;
    margin: 0;
  }
</style>
