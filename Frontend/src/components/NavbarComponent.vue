<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <RouterLink to="/" class="navbar-brand">Ticket<span id="red">Show</span></RouterLink>
      <ul class="navbar-nav me-auto mb-2 mb-lg-0" v-if="searchBox">
        <li class="nav-item">
          <form @submit.prevent="navigateToSearch">
            <div class="form-group">
              <div class="input-group">
                <input type="search" class="search" placeholder="search" name="search" id="search" v-model="search"
                  @input="emitSearch">
                <div class="input-group-append">
                  <button class="btn" type="submit"><i class="fa fa-search"></i></button>
                </div>
              </div>
            </div>
          </form>
        </li>
      </ul>

      <div class="dropdown-toggle text-dark dropdown dropstart" data-bs-toggle="dropdown" id="cityDropdownToggle"
        style="cursor: pointer;" v-if="isLocation">{{ city }}
        <div class="dropdown-menu" aria-labelledby="cityDropdownToggle">
          <!-- Add your city options here as list items -->
          <template v-for="location in locations" :key="location">
            <button class="dropdown-item" @click="emitCity(location)">{{ location }}</button>
          </template>
        </div>
        
      </div>

      <ul></ul>

      <div class=" dropstart" v-if="!user">

        <button class="btn btn-danger btn-sm nav-item dropdown" data-bs-toggle="dropdown">Login</button>
        <ul class="dropdown-menu ">
          <li>
            <RouterLink to="/login" class="dropdown-item">Login as user</RouterLink>
          </li>
          <li>
            <RouterLink to="/admin_login" class="dropdown-item">Host as admin</RouterLink>
          </li>

        </ul>
      </div>
      <div class=" dropstart" v-if="user">

        <img :src=" `https://api.multiavatar.com/${user.id}.png?apikey=OwWtNfcb5ZgUTy`" class="avatar" alt=""
        
        type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight"
          aria-controls="offcanvasRight"
        >



      </div>

    </div>

  </nav>
  <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel"
    v-if="user">
    <div class="offcanvas-header">
      <h5 class="offcanvas-title" id="offcanvasRightLabel">Account</h5>
      <button type="button" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body">
      <!-- <button class="btn btn-danger" @click="clickHandler">{{ user.name }}</button> -->
      <ul class="list-group">
        <RouterLink to="order" style="text-decoration: none;">
          <li class="list-group-item list-group-item-action "><span class="material-symbols-outlined">
              subscriptions
            </span><span class="profile-tab" data-bs-dismiss="offcanvas">Orders</span></li>
        </RouterLink>
        <li class="list-group-item list-group-item-action "><span class="material-symbols-outlined">
            settings
          </span><span class="profile-tab" data-bs-dismiss="offcanvas">Settings</span></li>

      </ul>
      <div class="offcanvas-footer">
        <div class=" list-group-item list-group-item-action  " @click="clickHandler"><span id="logout"
            class="material-symbols-outlined" style="font-size: 25px;">
            logout
          </span><span class="logout-tab" data-bs-dismiss="offcanvas">Logout</span></div>

      </div>
    </div>
  </div>
  <div class="toast" role="alert" aria-live="assertive" aria-atomic="true"
    :class="{ 'show': showToastFlag, 'hide': !showToastFlag }">
    <div class="toast-header">
      <strong class="mr-auto text-success" id="content">logout success!</strong>
      <span>
      <button @click="hideToast" type="button" class="ml-2 mb-1 close btn " data-dismiss="toast" aria-label="Close" id="close">
        <span aria-hidden="true">&times;</span>
      </button></span>
    </div>

  </div>
</template>

<script>

import { mapGetters } from 'vuex';
export default {
  name: 'NavbarComponent',
  props: {
    city: {
      type: String,
      default: 'Choose location'
    },
    locations: {
      type: Array,
      default: () => [' Patna', 'Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Kolkata', 'Chennai', 'Pune'],
    },
    isLocation: {
      type: Boolean,
      default: true
    },
    searchBox: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      search: '',
      showToastFlag:false,

    }
  },

  methods: {
    hideToast() {
      this.showToastFlag = false;
    },
    clickHandler() {
      localStorage.removeItem('token');
      this.$store.dispatch('user', null);
      document.getElementById('content').innerHTML = "loggedOut!"
      this.showToastFlag = true;
      setTimeout(() => {
        this.showToastFlag = false;
      }, 3000);
      return false;
    },
    emitCity(location) {

      this.$emit('city-clicked', location);
    },
    emitSearch() {
      this.$emit('search-submitted', this.search); // emit a custom event with the search data as payload

    },
    navigateToSearch(event) {
      event.preventDefault();
      this.$emit('form-submitted');
      this.$router.push({

        name: 'SearchView',
        query: {
          searchData: this.search

        },


      });
    }
  },
  computed: {
    ...mapGetters(['user'])
  },
 

}
</script>

<style  scoped>
/* .container-fluid ,.navbar ,.navbar-expand-lg, .bg-body-tertiary {
 background-color: yellowgreen;
} */
#close{
  top :0;
  right:-10px;
  position :relative
}
.toast {
    position: absolute;
    top: 70px;
    right: 0;
    margin: 1rem;
    z-index: 1000;
}
.toast-header{
  background-color: #f8e1e1;
  padding : 5px;
  border-bottom: 1px solid rgba(0, 0, 0, .1);
  border-bottom-right-radius: calc(.3rem - 1px);
  border-bottom-left-radius: calc(.3rem - 1px);
}
.list-group-item {
  /* border: none; */
  border-bottom: 1px solid #ccc;
  cursor: pointer;
}

.logout-tab {
  position: relative;
  top: -5px;
  right: 1px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;

}

.logout-tab:hover {
  color: red;
  cursor: pointer;
}

.profile-tab {
  position: relative;
  top: -5px;
  right: 1px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
}

.offcanvas-footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  left: 0;
  right: 0;
  padding: 1rem;
  background-color: #f5f5f5;
  border-top: 1px solid rgba(0, 0, 0, .1);
  border-bottom-right-radius: calc(.3rem - 1px);
  border-bottom-left-radius: calc(.3rem - 1px);
}

.offcanvas {
  width: 300px;

}

.material-symbols-outlined {

  position: relative;
  top: 2px;
  right: 10px;
  font-size: 35px;


}


.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 9999;

  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.2);


}

.text-dark {
  font-weight: bold;


}


.search {
  width: 300px;
  height: 33px;
  border-radius: 5px;
  border: 1px solid #ccc;
  padding-left: 10px;
  font-size: 16px;
  font-family: 'Rubik', sans-serif;
  outline: none;
  transition: 0.3s;
}

#myCarousel,
#red {
  font-family: 'Lily Script One', cursive;
}

#red {
  color: red;
}

.input-group-append {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  z-index: 999;
  display: flex;
  align-items: center;
  padding: 0 10px;



  font-style: italic;
}

input:focus {
  /* placehoder should be floating like bootstrap */
  border: 1px solid #ccc;
  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.2);
  outline: none;
  transition: 0.3s;

}
/* Media Query for Phones */
@media screen and (max-width: 480px) {
  .search {
    width: 200px;
  }
  .input-group-append {
    padding: 0 5px;
  }
  .navbar-brand {
    font-size: 20px;
  }
  .dropdown-toggle {
    font-size: 14px;
  }
  .dropdown-menu {
    font-size: 14px;
  }
  .nav-item {
    font-size: 14px;
  }
  .nav-link {
    font-size: 14px;
  }
  .btn {
    font-size: 14px;
  }
  .material-symbols-outlined {
    font-size: 20px;
  }
  .profile-tab {
    font-size: 14px;
  }
  .logout-tab {
    font-size: 14px;
  } 
  .toast-header{
    font-size: 14px;
  }
  .toast{
    top: 60px;
  }
  .offcanvas{
    width: 250px;
  }
  .offcanvas-footer{
    padding: 0.5rem;
  }
  .offcanvas-title{
    font-size: 14px;
  }
  .list-group-item{
    font-size: 14px;
  }
  .list-group-item-action{
    padding: 0.5rem;
  }
  .dropdown-item{
    font-size: 14px;
  }
  .dropdown-menu{
    font-size: 14px;
  }
  .avatar{
    width: 30px;
    height: 30px;
  }
}
.avatar{
 width: 40px; 
 height: 40px;
  border-radius: 50%; 
  cursor: pointer;
}

</style>