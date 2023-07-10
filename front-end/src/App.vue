<template>
  <div id="app" >
    <transition name="fade">
    <keep-alive>
      <router-view></router-view>
    </keep-alive>
  </transition>
  </div>
</template>

<script>
// import Login from "./components/Login.vue";
// import userInfo from "./components/userInfo.vue";


export default {
  name: "",
  data() {
    return {};
  },
  components: {

    // "app-login"  : Login,
    // "app-userInfo" : userInfo,

  },
  methods: {},
};
</script>