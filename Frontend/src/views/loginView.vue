<template>
  <loginComponent :image="'android'" :signup="'signup'"/>
</template>

<script>
  import loginComponent from '../components/loginComponent.vue'
  export default {
    name: 'loginView',
    components: {
      loginComponent}
  }
</script>

<style scoped>

</style>