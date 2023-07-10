import Vue from 'vue'
import App from './App'
import Login from './components/Login.vue'
import usesrInfo from './components/userInfo.vue'
import VueRouter from 'vue-router'
import axios from 'axios'
import Element from 'element-ui'
import echarts from "echarts";

Vue.prototype.$echarts = echarts;
import '../node_modules/element-ui/lib/theme-chalk/index.css'
import '../src/assets/style.css'
import './theme/index.css'

Vue.use(Element)
Vue.config.productionTip = false
Vue.use(VueRouter)
Vue.prototype.$http = axios

const router = new VueRouter({
    routes: [
        {
        path: "/",
        name: "Login",
        component: Login,
        },
        {
        path: "/userInfo",
        name: "userInfo",
        component: usesrInfo,
        },
        {
        path: "*",
        redirect: "/",
        },
        ],
    mode: "history"
})

// // 全局注册组件
Vue.component("App", App);

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    render: h => h(App)
})

