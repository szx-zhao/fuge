<template>
    <div style="text-align: center;">
      <h2 style="color: #57d4c3;">注册表单</h2>
      <form>
        <label class="form-label" for="username">用户名:</label>
        <input type="text" id="username" v-model="username">
        <br>
        <label class="form-label" for="password">密码:</label>
        <input type="password" id="password" v-model="password">
        <br>
        <button @click.prevent="register">点击即注册</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    name: 'RegistrationForm',
    data() {
      return {
        username: '',
        password: ''
      }
    },
    methods: {
      register() {
        // perform registration logic here
        axios.post('http://127.0.0.1:5000/register', {
        username: this.username,
        password: this.password
      })
      .then(response => {
        console.log(response);
      })
      .catch(error => {
        console.log(error);
      });

      }
    }
  }
  </script>



<style>
.form-label {
  display: inline-block;
  width: 80px; /* adjust as needed */
}
</style>