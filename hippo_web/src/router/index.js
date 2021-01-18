import Vue from 'vue'
import Router from 'vue-router'  // export default {功能} 抛出才能引入
import ShowCenter from '@/components/ShowCenter'  // 引入HelloWorld组件

Vue.use(Router)

export default new Router({
  mode:'history', // 新增的，修改模式
  routes: [
    {
      path: '/',
      name: 'ShowCenter',
      component: ShowCenter
    }
  ]
})
