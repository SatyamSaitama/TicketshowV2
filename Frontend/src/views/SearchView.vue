<template>
<NavbarComponent @form-submitted="handleSubmitted" @search-submitted="updateSearch" :isLocation="false" /> 
    <div class="container">
      <div class="row">
        <div class="col" id="filter">
          <div class="card">
            <div class="card-header h5">
              Filter-BY
            </div>
            <div class="card-body">
              <form @submit.prevent="filter">
                <label for="tags" class="h6">Tags:</label>
                <br>
                <input type="checkbox" id="adventure" name="tags" value="adventure" v-model="tags">
                <label for="adventure">Adventure</label>
                <br>
                <input type="checkbox" id="horror" name="tags" value="horror" v-model="tags">
                <label for="horror">Horror</label>
                <br>
                <input type="checkbox" id="romance" name="tags" value="romance" v-model="tags">
                <label for="romance">Romance</label>
                <br>
                <input type="checkbox" id="drama" name="tags" value="drama" v-model="tags">
                <label for="drama">Drama</label>
                <br>
                <input type="checkbox" id="animation" name="tags" value="animation" v-model="tags">
                <label for="animation">Animation</label>
                <br>
                <br>
                <label for="location" class="h6">Location:</label>
                <br>
                <template v-for="v in location" :key="v">
                  <input type="checkbox" :id="v" name="location" :value="v" v-model="locationList">
                  <label :for="v">{{ v }}</label>
                  <br>
                </template>
                <br>
                <label for="venue" class="h6">Venue:</label>
                <br>
                <template v-for="v in venues" :key="v.id">
                  <input type="checkbox" :id="v.id" name="venue" :value="v.id" v-model="venuelist">
                  <label :for="v.id">{{ v.name }}</label>
                  <br>
                </template>
                <br>
                <label for="rating" class="h6">Rating:</label>
                <br>
                <input type="checkbox" id="pg-13" name="rating" value="pg-13" v-model="ratingList">
                <label for="pg-13">PG-13</label>
                <br>
                <input type="checkbox" id="r" name="rating" value="r" v-model="ratingList">
                <label for="r">R</label>
                <br>
                <input type="checkbox" id="nc-17" name="rating" value="nc-17" v-model="ratingList">
                <label for="nc-17">NC-17</label>
                <br>
                <br>
                <button type="submit"  class="btn btn-primary" >Filter</button>
              </form>
            </div>
          </div>
        </div>
        <div class="col" id="results">
          <div class="card" id="result-card">
            <div class="card-header h5" id="result-header">
              Results
            </div>
            <div class="card-body" id="result-body">
             <contentComponent :objects="results" :ratings="ratings" />
            </div>
          </div>
        </div>
      </div>
    </div>
</template>
  
<script>
import contentComponent from '@/components/contentComponent.vue';
import NavbarComponent from '@/components/NavbarComponent.vue';
import axios from '../axios';

export default {
  name: 'SearchView',
  components: {
    NavbarComponent,
    contentComponent

  },
  data() {
    return {
      results: [],
      venuelist: [],
      ratingList: [],
      locationList: [],
      searchData: '',
      tags: [],
      location: [],
      ratings: {},
      venues: [],
    };
  },
  
  async created() {
    this.searchData = this.$route.query.searchData;
    this.search();
    try {
      
      const response = await axios.get('user')
      this.$store.dispatch('user', response.data)
    } catch (error) {
      console.log("error in getting user")
    }
  },
  mounted() {

  },
  methods: {
    async filter(){
      const data = {
        tags: this.tags,
        location: this.locationList,
        venues: this.venuelist,
        rating: this.ratingList
      };
     await axios
        .post('search', data)
        .then(response => {
          this.results = response.data.results;
          this.location = response.data.location;
          this.ratings = response.data.ratings;
          this.venues = response.data.venues;
          //unique venues by name 
          this.venues = this.venues.filter((v, i, a) => a.findIndex(t => (t.name === v.name)) === i)
        })
        .catch(error => {
          console.error(error);
        });

    },
    async search() {
      const response=await axios.get('search/' + this.searchData)
      this.results = response.data.results;
      this.location = response.data.location;
      this.ratings = response.data.ratings;
      this.venues = response.data.venues;
      //unique venues by name
      this.venues = this.venues.filter((v, i, a) => a.findIndex(t => (t.name === v.name)) === i)
    },


handleSubmitted() { 
  // this.searchData = this.$route.query.searchData;
    this.search();
     
},
updateSearch(value) {
            this.searchData = value;
        }  

  },
};
</script>
  
<style scoped>
#filter {
  margin-top: 60px;
  position: absolute;
  top: 0;
  left: 0;
  width: 350px; /* Adjust the width as needed */
}

#results {
  margin-top: 60px;
  position: absolute;
  top: 0;
  left: 370px;
  width: calc(100% - 370px); /* Adjust the width as needed */
}

#result-card {
  height: 100%; /* Make sure the cards take the full height of their parent container */
  --bs-card-spacer-x: 0rem;
}

#result-body {
  overflow-y: auto; /* Add vertical scrolling to the card body if content overflows */
padding: 0px;}

/* Add any additional styling to the cards and their content here */

/* To make sure the checkboxes and labels align properly, you can use flexbox like this: */
#result-body form {
  display: flex;
  flex-wrap: wrap;
}

.card-body label {
  flex: 0 0 50%; /* Adjust this percentage based on your layout preference */
}

/* Additional styling for the filter section */
#filter .card-header {
  background-color: #f2f2f2;
}
/* responsive for phone desktop */
@media (max-width: 768px) {
  #filter {
    position: relative;
    width: 100%;
    left: 0;
  }
  #results {
    position: relative;
    width: 100%;
    left: 0;
  }
}
@media(max-width: 576px){
  #filter {
    position: relative;
    width: 100%;
    left: 0;
  }
  #results {
    position: relative;
    width: 100%;
    left: 0;
  }
}

</style>
