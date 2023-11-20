<template>
    <div class="location-modal">
        <div class="modal-content-1">
            <div class="cities-container">
                <template v-for="city in cities" :key="city">
                    <div class="row row-cols-2 row-cols-md-3 row-cols-lg-5">
                        <div class="col mb-4">
                            <div class="city-img" @click="clickImg(city)">
                                <img src="https://cdn.s3waas.gov.in/s3fb7b9ffa5462084c5f4e7e85a093e6d7/uploads/2018/02/2018022799.png"
                                    alt="" style="height: 60px;" v-if="city === 'Patna'" />
                                <img src="https://in.bmscdn.com/m6/images/common-modules/regions/ncr.png" alt=""
                                    style="height: 60px;" v-else-if="city === Delhi" />

                                <img src="https://in.bmscdn.com/m6/images/common-modules/regions/chen.png" alt=""
                                    style="height: 60px;" v-else />

                                <h7>{{ city }}</h7>
                            </div>
                        </div>
                    </div>
                </template>
            </div>

            <div class="location ">

                <div class="text-click" @click="getLocation">

                    Use current location<span class="material-symbols-outlined " v-if="!showLoading">
                        my_location
                    </span>
                    <span class="spinner-border spinner-border-sm text-danger" v-else>
                        </span>
                </div>

            </div>
        </div>
    </div>
</template>
  
<script>
export default {
    name: 'LocationModal',
    props: {
        cities: {
            type: Array,
            default: () => [' Patna', 'Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Kolkata', 'Chennai', 'Pune'],
        },
    },
    data() {
        return {
            showLoading: false,
        };
    },
    methods: {

        clickImg(event) {
            this.$emit('imageClicked', event);
        },
        getLocation() {
            setTimeout(() => {
                this.showLoading = true;
            }, 2000);

            // Implement the code to get the user's location here.
            // For demonstration purposes, we will assume the location is allowed.
            this.$emit('locationAllowed');
        },
    },
};
</script>
  
<style scoped>
/* Styles for the modal */
.text-click {
    cursor: pointer;
}

img:hover {
    cursor: pointer;
    border-radius: 5px;
    transform: scale(1.09);
    transition: 0.1s;

}

.material-symbols-outlined {
    font-variation-settings:
        'FILL' 0,
        'wght' 400,
        'GRAD' 0,
        'opsz' 48,
    ;

    color: red;
    cursor: pointer;
    padding: 0px;
    position: relative;
    top: 7px;
    left: 4px;

}

.material-symbols-outlined:hover {

    background-color: #f2f2f2;

}

.location {
    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    display: flex;
    justify-content: flex-end;
    align-items: baseline;
    flex-direction: column;
    padding: 20px;
    position: absolute;
    bottom: 0;
    right: 0;


}

.city-img {
    padding: 15px;
    cursor: pointer;
}

.cities-container {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    flex-wrap: wrap;
}

.location-modal {
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.7);
    z-index: 9999;
}

.modal-content-1 {
    width: 833px;
    height: 263px;
    background-color: #fff;
    border-radius: 4px;
    padding: 20px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    position: relative;
}

/* Additional styling to make the button more visually appealing */
</style>
  