<template>
  <NavbarComponent @search-updated="updateSearch" :city="city" @city-clicked="chooseLocation" :locations="location" />
  <div class="placeholder-slide" aria-hidden="true" v-if="!shows" >
               
               
                  
                   <p class="card-text placeholder-glow">
                       <span class="placeholder col-7"></span>
                       <span class="placeholder col-4"></span>
                       <span class="placeholder col-4"></span>
                       <span class="placeholder col-6"></span>
                       <span class="placeholder col-8"></span>
                   </p>

            
           </div>
  <div class="custom-container"  v-else>
    <div id="carouselExampleAutoplaying" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-inner">
        <div class="carousel-item active">
          <img src="https://www.redwolf.in/image/cache/catalog/banners/official-merch/Across-The-Spider-Verse-Category-Banner-1920-1920x350.jpg?m=1687857106"
            class="d-block w-100" alt="">
        </div>
        <div class="carousel-item">
          <img src="https://assets-in.bmscdn.com/promotions/cms/creatives/1717494054241_badboys1240x300.jpg"
            class="d-block w-100" alt="">
        </div>
        <div class="carousel-item">
          <img src="https://assets-in.bmscdn.com/promotions/cms/creatives/1689325117598_oppenheimerdesktop.jpg"
            class="d-block w-100" alt="">
        </div>
      </div>
      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleAutoplaying"
        data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleAutoplaying"
        data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>

      </button>
    </div>
  </div>

  <locationModal v-if="dataLoaded && !isLocation" @locationAllowed="getGeoLocation" :cities="this.location"
    @imageClicked="chooseLocation" />
    <div class="card" aria-hidden="true" v-if="!shows" >
               
                <div class="card-body">
                    <p class=" placeholder-glow">
                        <span class="placeholder col-7"></span>
                        <span class="placeholder col-4"></span>
                        <span class="placeholder col-4"></span>
                        <span class="placeholder col-6"></span>
                        <span class="placeholder col-8"></span>
                    </p>

                </div>
            </div>
  <contentComponent :objects="shows" :ratings="ratings" v-else  />
  
</template>

<script>
// import { mapGetters } from 'vuex';
import axios from '../axios';
import NavbarComponent from '@/components/NavbarComponent.vue';
import contentComponent from '@/components/contentComponent.vue';
import locationModal from '@/components/modalComponent.vue';

export default {

  components: {
    NavbarComponent,
    contentComponent,
    locationModal,
  },
  data() {
    return {
      shows: null,
      ratings: {},
      search: '',
      city: 'Choose Location',
      isLocation: false,
      isLoading: false,
      dataLoaded : false,
      location: [],
    };
  },
  methods: {
    
  
    async getShows() {
      try {
        const response = await axios.get('/');
       
        for (const show in response.data.shows) {
          this.location.push(response.data.shows[show].venues.location);
        }
        this.location = [...new Set(this.location)];
      } catch (error) {
        console.error(error);
      }
    },
    
    async chooseLocation(location) {
      try {
        this.city = location;
        this.isLoading = false;
        const response = await axios.post('/', { city: location });
        this.shows = response.data.shows.sort((a, b) => {
          return new Date(a.timing) - new Date(b.timing);
        });
        
        this.ratings = response.data.ratings;
        this.isLocation = true;
        localStorage.setItem('chosenLocation', this.isLocation);
        localStorage.setItem('savedLocation', location);
      } catch (error) {
        console.error(error);
      }
    },
    updateSearch(value) {
      this.search = value;
      // Perform any necessary actions with the search data in the parent component
    },
    successCallback(position) {
      const latitude = position.coords.latitude;
      const longitude = position.coords.longitude;
      this.city = 'Patna';
      this.chooseLocation(this.city);
      // Call the reverse geocoding function to get the city name
      console.log(latitude, longitude);
    },
    errorCallback(error) {
      console.log(error);
    },
    getGeoLocation() {
      if (!navigator.geolocation) {
        alert('Geolocation is not supported by your browser');
      } else {
        navigator.geolocation.getCurrentPosition(this.successCallback, this.errorCallback);
      }
    },
  },
  // computed: {
  //   ...mapGetters(['user'])
  // },
  async created() {
    try{
      const response = await axios.get('user')
      this.$store.dispatch('user',response.data)
    }catch(error){
      console.log("error in getting user")
    }
  
    // await this.getShows();
    const savedLocation = localStorage.getItem('chosenLocation');
    if (savedLocation) {
      this.isLocation = savedLocation;
      const savedCity = localStorage.getItem('savedLocation');
      if (savedCity) {
        this.city = savedCity;
        await this.chooseLocation(this.city);
      }
    }
    this.dataLoaded = true
    await this.getShows()
  },
};
</script>



<style scoped>
/* your-custom-styles.css */
/* Custom CSS to make the hover effect faster */
#carouselExampleAutoplaying {
  margin-top: 52px;
  margin-bottom: -5px;
  /* Adjust this value to make the hover effect faster */
}

.carousel-inner {
  transition-duration: 0.2s;
  /* Adjust this value to make the hover effect faster */
}

.custom-container {
  width: 100%;
  height: 100%;
  background-color: #f2f2f2;
  padding: 12px;
  border-radius: 5px;
  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.2);
  margin: 0 auto;
  /* on hover on carasouel */

}
.card-text:last-child {
  margin-bottom: 23px;
}
p {
  margin-top: 156px;
  margin-bottom: 1rem;
}
</style>
