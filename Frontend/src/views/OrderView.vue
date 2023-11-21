<template>
  <div>
    <NavbarComponent :isLocation="false" />
    <h3>Orders</h3>

    <div class="custom-container">
      <div class="row row-cols-2 row-cols-md-3 row-cols-lg-5">
        <template v-if="shows.length===0">
          <img src="../assets/shopping.svg" alt="" id="img-order">
          <h1 style="align-items: center;justify-content: center; display: flex; font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;">no orders</h1>
        </template>
        <template v-for="  show in  shows " :key="show.id">
          <div class="col mb-4">
            <div class="card">
              <div class="card-img-top">
                <RouterLink :to="`/book?id=${show.id}`">
                  <img :src="`https://ticketshow3.onrender.com/images/${show.venue_id}.${show.show_name}`" class="card-img-top" :alt="show.show_name"
                    style="height: 300px; show-fit:cover;">
                  
                </RouterLink>


                <div class="card-footer d-flex justify-content-end" v-if="hasShowPassedCurrentTime(show.timing)">
    <button class="btn btn-danger btn-sm me-2" role="button" data-bs-toggle="modal"
    :data-bs-target="`#exampleModal${show.id}`">Cancel</button>
    <button class="btn btn-info btn-sm" role="button" data-bs-toggle="modal"
        :data-bs-target="`#infoModal${show.id}`">Info</button>

        <div class="modal fade" :id="`infoModal${show.id}`" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
       <div class="row">
            <!-- Loop through the JSON data to create a ticket card for each show -->
            <div class="col-md-4" >
                <div class="ticket-card">
                    <div class="ticket-header">
                        <h4>{{ show.show_name }}</h4>
                        <span class="badge bg-primary">{{ show.rating }}</span>
                    </div>
                    <div class="ticket-details">
                        <p><strong>Date & Time:</strong> {{ show.timing }}</p>
                        <p><strong>Tags:</strong> {{ show.tags }}</p>
                        <p><strong>Venue:</strong> {{ show.venues.name }} ({{ show.venues.location }})</p>
                    </div>
                    <p class="ticket-price">{{ show.price }} INR</p>
                    <a :href=" show.yt_link " target="_blank" class="btn btn-info btn-sm">Watch Trailer</a>
                </div>
            </div>
        </div>
     
    </div>
  </div>
</div>

                    

                  <!-- Button trigger modal -->


                  <!-- Modal -->
                  <div class="modal fade" :id="`exampleModal${show.id}`" tabindex="-1" aria-labelledby="exampleModalLabel"
                    aria-hidden="true">
                    <div class="modal-dialog">
                      <div class="modal-content">
                        <div class="modal-header">
                          <h1 class="modal-title fs-5" id="exampleModalLabel"></h1>
                          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                          Are you sure you want to cancel the booking?
                        </div>
                        <div class="modal-footer" >
                          <button type="button" class="btn btn-danger" data-bs-dismiss="modal"
                            @click="cancelHandler(show.id)" >Confirm</button>
                          <!-- <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">close</button> -->
                        </div>
                      </div>
                    </div>
                  </div>





                </div>
                <div class="card-footer d-flex justify-content-end"  v-else >
<button type="button" class="btn btn-dark btn-sm " id="btn-rate" data-bs-toggle="modal" :data-bs-target="`#exampleModal${show.id}`">
  Review
</button>
<button class="btn btn-info btn-sm" role="button" data-bs-toggle="modal"
        :data-bs-target="`#infoModal${show.id}`">Info</button>

        <div class="modal fade" :id="`infoModal${show.id}`" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
       <div class="row">
            <div class="col-md-4" >
                <div class="ticket-card">
                    <div class="ticket-header">
                        <h4>{{ show.show_name }}</h4>
                        <span class="badge bg-primary">{{ show.rating }}</span>
                    </div>
                    <div class="ticket-details">
                        <p><strong>Date & Time:</strong> {{ show.timing }}</p>
                        <p><strong>Tags:</strong> {{ show.tags }}</p>
                        <p><strong>Venue:</strong> {{ show.venues.name }} ({{ show.venues.location }})</p>
                    </div>
                    <p class="ticket-price">{{ show.price }} INR</p>
                    <a :href=" show.yt_link " target="_blank" class="btn btn-info btn-sm">Watch Trailer</a>
                </div>
            </div>
        </div>
     
    </div>
  </div>
</div>


<!-- Modal -->
<div class="modal fade" :id="`exampleModal${show.id}`" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <form @submit.prevent="ratingHandler(show.id)">
    <div class="modal-content">
      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      <div class="modal-body">
        <div class="mb-3 mt-3" aria-label="Basic radio toggle button group">
      <input type="radio" class="btn-check" name="btn" id="rate1" value=1  v-model.number="rate">
      <label class="btn btn-outline-dark" for="rate1">1</label>

      <input type="radio" class="btn-check" name="btn" id="rate2" value=2 v-model.number="rate">
      <label class="btn btn-outline-dark" for="rate2">2</label>

      <input type="radio" class="btn-check" name="btn" id="rate3" value=3 v-model.number="rate">
      <label class="btn btn-outline-dark" for="rate3">3</label>

      <input type="radio" class="btn-check" name="btn" id="rate4" value=4 v-model.number="rate">
      <label class="btn btn-outline-dark" for="rate4">4</label>

      <input type="radio" class="btn-check" name="btn" id="rate5" value=5 v-model.number="rate">
      <label class="btn btn-outline-dark" for="rate5">5</label>
      <div class="col-md-6">
        <span class="material-symbols-outlined">
stylus
</span>
                <label for="reviewTextarea" class="form-label h5">Write a Review</label>
                <textarea class="form-control" id="reviewTextarea" rows="4" placeholder="Enter your review..." v-model="textarea"></textarea>
            </div>
    </div>
      </div>
      
        <button type="submit" class="btn btn-danger" data-bs-dismiss="modal" >Rate</button>
     
    </div>
  </form>
  </div>
</div>
</div>

              </div>

            </div>
          </div>

        </template>
      </div>
    </div>
    
  </div>
</template>
  
<script>
import NavbarComponent from '@/components/NavbarComponent.vue';
import axios from '../axios';
import { mapGetters } from 'vuex';
export default {
  name: "OrderView",
  components: {
    NavbarComponent
  },
  data() {
    return {
      shows: [],
      rate: 0,
      textarea: "",
    };
  },
  methods: {
    async ratingHandler(id) {
     await axios.put(`api/bookings/${id}`, { rating: parseFloat(this.rate) })
      this.getShows()
      await axios.post(`comment`, { text: this.textarea,user_id:this.user.id,time: new Date().toISOString().slice(0, 19).replace('T', ' '),show_id:id })
  
    },
    hasShowPassedCurrentTime(showTiming) {
  const showTime = new Date(showTiming);
  const currentTime = new Date();
  if (showTime > currentTime) {
    return true; 
  } else {
    return false; 
  }
},
    async cancelHandler(id) {
      await axios.delete(`api/bookings/${id}/${this.user.id}`)
      this.getShows()
    },
   
    async getShows() {
      try {
        const response = await axios.get('api/bookings/user/' + this.user.id)
        this.shows = response.data
        
      } catch (error) {
        console.error(error);
      }
    },
  },
  computed: {
    ...mapGetters(['user']),

  },
  async created() {
    try {
      
      const response = await axios.get('user')
      this.$store.dispatch('user', response.data)
    } catch (error) {
      console.log("error in getting user")
    }
    this.getShows()
  }

}
</script>
  
<style scoped>
.ticket-card {
            font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
            background-color: #f5f5f5;
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            width: 300px;
        }

        .ticket-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .ticket-header h4 {
            margin: 0;
        }

        .ticket-details {
            margin-bottom: 10px;
        }

        .ticket-price {
            font-size: 1.25rem;
            font-weight: bold;
            margin: 0;
        }

        .ticket-rating {
            font-size: 0.9rem;
            margin: 0;
        }
#btn-cancel {
 position: relative;
 top : -5px;
  left: 0px;
}
.rating-overlay {
  position: absolute;
  top: 0;
  left: 0;

  background-color: rgba(236, 33, 12, 0.9);
  color: white;
  font-weight: bold;
  font-size: 15px;
}

.rating {
  margin: 0;
  padding: 0;
}

#place {
  font-size: 15px;
  font-weight: bolder;
  text-align: center;
  cursor: pointer;
}

.place:hover {
  color: red;
}

.show_name {
  font-size: 15px;
  font-weight: bolder;
  text-align: center;
  color: black;
  font-family: 'Rubik', sans-serif;
}

.location {
  font-size: 12px;
  font-weight: bolder;
  text-align: center;
  color: black;
  font-family: 'Rubik', sans-serif;
}

.venue {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;

  font-size: 15px;
  font-weight: bolder;
  text-align: center;
  color: black;
  font-family: 'Rubik', sans-serif;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  top: 100px;
  left: 0;
}

.card {
  height: 340px;
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.2);
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 10px;
  margin: 10px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  height: 360px;
  position: relative;
  overflow: hidden;
  transition: box-shadow 0.3s, transform 0.3s;
}

/* .card-img-top:hover {
    box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.6);
    transform: scale(1.05);
    transition: 0.1s;
  
    cursor: pointer;
  } */

.custom-container {
  width: 99vw;
  height: 100%;
  padding: 20px;
  border-radius: 5px;
  margin-top: 30px;

}

@media (max-width: 576px) {
  .row-cols-2 .col {
    flex-basis: 50%;
    max-width: 50%;
  }
}

@media (min-width: 576px) and (max-width: 768px) {
  .row-cols-3 .col {
    flex-basis: 33.3333%;
    max-width: 33.3333%;
  }
}

@media (min-width: 768px) and (max-width: 992px) {
  .row-cols-3 .col {
    flex-basis: 33.3333%;
    max-width: 33.3333%;
  }

  .row-cols-5 .col {
    flex-basis: 20%;
    max-width: 20%;
  }
}

@media (min-width: 992px) {
  .row-cols-3 .col {
    flex-basis: 33.3333%;
    max-width: 33.3333%;
  }

  .row-cols-5 .col {
    flex-basis: 20%;
    max-width: 20%;
  }

  .carousel-inner .item img {
    height: 300px;
    /* Set the desired height here */
    object-fit: cover;
    /* Make the image cover the entire container */
  }
}

.text-right {
  color: olive;
  font-size: 20px;
  text-align: right;
}
.place{
  font-size: 20px;
  font-weight: bolder;
  text-align: center;
  cursor: pointer;
}
.rating{
  margin: 0;
  padding: 0;

}

.card-img-top {
  height: 200px;
  object-fit: cover;
}
#img-order{
  margin-left: 40%;
  margin-top: 10%;
}
#info{
  position: relative;
  top: -5px;
  left: 0px;
}
#btn-rate{
  position: relative;
  top: 0px;
  left: -5px;
}
</style>
  