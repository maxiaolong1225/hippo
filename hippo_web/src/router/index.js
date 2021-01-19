import Vue from 'vue'
import Router from 'vue-router'  // export default {功能} 抛出才能引入
import ShowCenter from '@/components/ShowCenter'  // 引入HelloWorld组件
import Login from '@/components/Login'
import Base from '@/components/Base'
import Host from "@/components/Host";

Vue.use(Router)

export default new Router({
  mode:'history', // 新增的，修改模式
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/hippo',
      name:'hippo',
      component:Base,
      children:[
        {
          path:'',
          name:"ShowCenter",
          component:ShowCenter,

        },
        {
          path:'showcenter',
          name:"ShowCenter",
          component:ShowCenter,

        },
        {
          path:'hosts/',
          name:"Host",
          component:Host,

        }

      ]
    }
  ]
})
