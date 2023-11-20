<template>
  
  <router-view />
 
</template>
<script>
import axios from 'axios'
export default{
 async created(){
  try{
      console.log("in created part 2")
      const response = await axios.get('user')
      this.$store.dispatch('user',response.data)
    }catch(error){
      console.log("error in getting user")
    }
  }
}
</script>
<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  // text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;


  }
}
</style>
