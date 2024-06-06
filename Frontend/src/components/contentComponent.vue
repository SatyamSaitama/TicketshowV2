<template>
  <div class="custom-container"  >
    <div class="row row-cols-2 row-cols-md-3 row-cols-lg-5">
      <template v-for="  object in  objects " :key="object.id">
        <div class="col mb-4">
          <div class="card">
            <div class="card-img-top">
              <RouterLink :to="`/book?id=${object.id}`">
                
                  <img :src="`require(`@/assets/${object.venue_id}.${object.show_name}.jpg`"
                 class="card-img-top" :alt="object.show_name"
                  style="height: 300px; object-fit:cover;">
                  <span class="rating" v-if="ratings[object.id] !== undefined">{{ ratings[object.id].toFixed(1) }}<span>
                      ★

                    </span>
                  </span>
                </div>
              </RouterLink>


              <div class="card-title venue">
               
                <RouterLink :to="`/book?id=${object.id}`" style="color: black; text-decoration: none;"
                  onmouseover="this.style.color='purple'" onmouseout="this.style.color='black'"><b
                    class="object_name">{{ object.show_name }}</b></RouterLink>

                <p class="location">
                  @ venue: {{ object.venues.name }} </p>


              </div>

            </div>

          </div>
        </div>

      </template>
    </div>
  </div>
  
  
</template>

<script>
export default {
  name: "contentComponent",
  props: {
    objects: {
      type: Array,
      required: true
    }
    ,
    ratings: {
      type: Object,
      default: () => ({})

    },
  
   
  },
  methods: {
    getImagePath(venueId, showName) {
      return require(`@/assets/${venueId}.${showName}.jpg`);
    }
  }

}
</script>

<style scoped>
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
  position: absolute;
  top: 0;
  left: 0;
  padding: 5px 10px;
  background-color: rgba(236, 33, 12, 0.9);
  color: white;
  font-weight: bold;
  font-size: 12px;
  border-radius: 0 10px 0 10px;
  border: 1px solid white;
  border-bottom: none;
  border-right: none;
  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.2);
  z-index: 1;
  cursor: pointer;
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

.card {
  height: 340px;
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.2);
}

.card:hover {
  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.6);
  transform: scale(1.05);
  transition: 0.1s;

  cursor: pointer;
}

.custom-container {
  width: 99vw;
  height: 100%;
  background-color: #f2f2f2;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.2);
  margin: 0 auto;
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

.card-img-top {
  height: 200px;
  object-fit: cover;
}
</style>
