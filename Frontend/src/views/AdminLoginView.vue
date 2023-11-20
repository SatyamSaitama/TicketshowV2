<template>
    <loginComponent :image="'admin'" :signup="'admin_signup'"/>
  </template>
  
  <script >
  
    import loginComponent from '../components/loginComponent.vue'
    export default {
      name: 'AdminLoginView',
      components: {
        loginComponent}
    }
  </script>
  
  <style scoped>
  
  </style>