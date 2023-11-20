<template>
  <!-- card for login aligned center use bootstrap -->
  <div class="custom-container">
    <RouterLink to="/" class="navbar-brand "><b>Ticket</b><span id="red">Show</span></RouterLink>
    <div class="row">
      <div class="col-md-12 text-center">
        <template v-if="shaky_cat">
          <img :src="require(`@/assets/${image}-chrome-192x192.png`)" alt="TicketShow"
            class="img-fluid float-left shaky-head">
        </template>
        <template v-else>
          <img :src="require(`@/assets/${image}-chrome-192x192.png`)" alt="TicketShow" class="img-fluid float-left">
        </template>

        <template v-if="shaky_cat">
          <h6><b style="color:red">Try Again!</b></h6>
        </template>
      </div>
    </div>
    <div class="row">
      <div class="col-md-6 offset-md-3">
      </div>
    </div>
    <form class="mx-auto" @submit.prevent="login">
      <div class="mb-3 mt-3 ">
        <label for="email" class="form-label">Email:</label>
        <input type="email" class="form-control" v-model="email" id="email" aria-describedby="emailHelp"
          placeholder="Enter email" required>
      </div>
      <div class="mb-3 ">
        <label for="validationTooltip05" class="form-label">Password</label>
        <input type="password" class="form-control " id="validationTooltip05" placeholder="Enter password" name="pswd"
          v-model="password" required>


      </div>
      <div class="mb-3 ">
        <button type="submit" class="btn btn-primary">Submit</button>
      </div>
    </form>
    <div class=" mb-3">
      <RouterLink :to="signup" class="text-danger">
        <strong>NEW!</strong> Create Account
      </RouterLink>
    </div>

  </div>
</template>

<script>
import axios from '../axios';
export default {
  name: 'loginComponent',
  props: ['image', 'signup'],
  data() {
    return {
      email: '',
      password: '',
      shaky_cat: false,

    }
  },
  methods: {
  
    async login() {

      try {
        const data =
        {
          email: this.email,
          password: this.password
        }
        const response = await axios.post('login', data);
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('role', response.data.role);
        this.$store.dispatch('user', response.data.user);

        if (response.data.message === "success") {
          if (response.data.role === 'admin') {
            this.$router.push('/admin');
          }
          else if (response.data.role === 'user') {
            if (localStorage.getItem('redirect')) {
              this.$router.push(localStorage.getItem('redirect'));
              localStorage.removeItem('redirect');
            }
            else {
              this.$router.push('/');
            
            }
          }
        }
        else {

          this.shaky_cat = true;
          setTimeout(() => {
            this.shaky_cat = false;
          }, 500);
        }
        console.log(response.data, response.message);
      }
      catch (error) {
        console.error(error);
      }

    },
  }
}
</script>

<style scoped>
@keyframes shake {
  0% {
    transform: rotate(0);
  }

  10% {
    transform: rotate(-10deg);
  }

  20% {
    transform: rotate(10deg);
  }

  30% {
    transform: rotate(-10deg);
  }

  40% {
    transform: rotate(10deg);
  }

  50% {
    transform: rotate(-5deg);
  }

  60% {
    transform: rotate(5deg);
  }

  70% {
    transform: rotate(-5deg);
  }

  80% {
    transform: rotate(5deg);
  }

  90% {
    transform: rotate(-2deg);
  }

  100% {
    transform: rotate(0);
  }
}

/* Apply the animation to the image */
img.shaky-head {
  animation: shake 0.5s 1;
}


#red {
  font-family: 'Lily Script One', cursive;
  color: red;
}



.custom-container {
  width: 50vw;
  height: 100%;
  background-color: #f2f2f2;
  padding: 20px;
  border-radius: 5px;
  margin: 10px auto;
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
}
</style>