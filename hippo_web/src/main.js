// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'  // 导入vue并且别名为Vue
import App from './App' //导入App组件
import router from './router'  // 导入路由控制系统
import settings from "./settings";
import axios from "axios";
import Antd from 'ant-design-vue';
Vue.use(Antd);
import 'ant-design-vue/dist/antd.css';
import 'xterm/css/xterm.css';
import 'xterm/lib/xterm';

// import echarts from 'echarts';
let echarts = require('echarts');

Vue.prototype.$settings = settings
Vue.prototype.$axios = axios
Vue.prototype.$echarts = echarts;


Vue.config.productionTip = false

/*
vue对象初始化入口，这里导入的一些组件
eslint-disable no-new
*/

new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'  // 调用App.vue
})
