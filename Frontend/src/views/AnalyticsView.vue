<template>
    <div>
        <!-- Navbar -->
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container">
                <a class="navbar-brand" href="/admin">Home</a>
                <!-- Add any other navigation links if needed -->
            </div>
        </nav>

        <!-- Venue Dashboard -->
        <div class="container mt-4">
            <h2 class="mb-4">Theatres</h2>

            <!-- Table to display venues -->
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Place</th>
                        <th>Location</th>
                        <th>Capacity</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="venue in venues" :key="venue.id">
                        <td>{{ venue.name }}</td>
                        <td>{{ venue.place }}</td>
                        <td>{{ venue.location }}</td>
                        <td>{{ venue.capacity }}</td>
                        <td><button class="btn btn-primary btn-sm" @click="asyncRequest(venue.id)">Export</button></td>


                    </tr>
                </tbody>
            </table>

            <!-- Buttons for downloading CSV -->
           
        </div>

        <!-- Popularity Chart -->
        <div class="container mt-4">
            <h2 class="mb-4">Popularity Chart</h2>
            <popularity-chart :showPopularityData="showPopularity" :venuePopularityData="venuePopularity"
           v-if="loading" />
        </div>
        <div class="toast" role="alert" aria-live="assertive" aria-atomic="true"
        :class="{ 'show': showToastFlag, 'hide': !showToastFlag }">
        <div class="toast-header">
            <strong class="mr-auto" id="content">Venue Deleted!</strong>
            <button @click="hideToast" type="button" class="ml-2 mb-1 close btn" data-dismiss="toast" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>

    </div>
    </div>
</template>
  
<script>
import axios from '../axios';
import PopularityChart from '@/components/PopularityChart.vue'; // Adjust the import path based on your project structure

export default {
    name: 'AnalyticsView',
    components: {
        PopularityChart,
    },
    data() {
        return {
            venues: [], // Store venue data from the API
            showPopularity: [], // Store show_popularity data for the chart
            venuePopularity: [], // Store venue_popularity data for the chart
            loading: false,
            showToastFlag: false,

        };
    },
    async created() {
        const res = await axios.get('user')
        this.$store.dispatch('user', res.data)
       await this.fetchVenueData();
       await this.fetchPopularityData().then(() => {
            this.loading = true;
        });
        

    },
    methods: {
        async asyncRequest(id){
           await axios.get(`export/${id}`)
            .then((response) => {
                console.log(response.data)
            })
            .catch((error) => {
                console.error('Error fetching popularity data:', error);
            });
            document.getElementById('content').innerHTML = "Exported!"
            this.showToastFlag = true
            setTimeout(() => {
                this.showToastFlag = false
            }, 3000);

        },
        hideToast() {
            this.showToastFlag = false
        },
        
       async fetchVenueData() {
            // Make an API request to fetch venue data from the server
           await axios
                .get('/api/venues') // Replace '/api/venues' with the actual API endpoint for fetching venues
                .then((response) => {
                    this.venues = response.data;
                })
                .catch((error) => {
                    console.error('Error fetching venue data:', error);
                });
        },
       async  fetchPopularityData() {
            // Make an API request to fetch popularity data from the server
           await axios
                .get('popularity')
                .then((response) => {
                    this.showPopularity = response.data.show_popularity;
                    this.venuePopularity = response.data.venue_popularity;
                })
                .catch((error) => {
                    console.error('Error fetching popularity data:', error);
                });
        },
       
    },
};
</script>
  
<style scoped>
.custom-container {
    max-width: 800px;
    margin: 0 auto;
}
.toast {
    position: absolute;
    top: 0;
    right: 0;
    margin: 1rem;
    z-index: 1000;
}
</style>
  