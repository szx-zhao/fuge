<template>
    <div>
    <app-header></app-header>
    <app-content></app-content>
    </div>
</template>



<script>
import Header from "./Header.vue";
import Content from "./Content.vue";

export default {
  name: "验证码识别系统",
  data() {
    return {};
  },
  components: {
    "app-header": Header,
    "app-content": Content,
  },
  methods: {},
};
</script>

<style scope="this api replaced by slot-scope in 2.5.0+">
</style>
