
<template>
    <section style="background-color: #eee;" v-if="show">
        <div class="container py-5">
            <div class="card">
                <div class="card-body">
                    <div class="row d-flex justify-content-center pb-5">
                        <div class="col-md-7 col-xl-5 mb-4 mb-md-0">
                            <div class="py-4 d-flex flex-row">
                                <h5><b>Ticket</b><span id="red">Show</span> |</h5>
                                <span class="ps-2">Pay</span>
                            </div>
                            <h4 class="text-success">₹{{ total }}</h4>
                            <h4>{{ show.show_name }}</h4>
                            <div class="d-flex pt-2">
                                <div>
                                    <span><b>
                                            <p class="text-danger">
                                                {{ show.venues.name }}
                                            </p>
                                            <p>Date: {{ show.timing.slice(8, 10) + "-" + show.timing.slice(5, 7) + "-" +
                                                show.timing.slice(0, 4) }}</p>
                                            <p>Time: {{ show.timing.slice(11, 16) }}</p>
                                        </b></span>

                                </div>
                                <div class="ms-auto">
                                    
                                </div>
                            </div>

                            <div class="accordion " id="accordionPanelsStayOpenExample">
                                <div class="accordion-item">
                                    <h2 class="accordion-header">
                                        <button class="accordion-button" type="button" data-bs-toggle="collapse"
                                            data-bs-target="#panelsStayOpen-collapseOne" aria-expanded="true"
                                            aria-controls="panelsStayOpen-collapseOne">
                                            Show Details
                                        </button>
                                    </h2>
                                    <div id="panelsStayOpen-collapseOne" class="accordion-collapse collapse show">
                                        <div class="accordion-body" v-if="show">


                                            <p><strong>Place: </strong>{{ show.venues.place }}</p>
                                            <p><strong>Location: </strong>{{ show.venues.location }}</p>
                                            <p><strong>Capacity: </strong>{{ show.venues.capacity }}</p>

                                            <p><strong>Genre: </strong>{{ show.tags }}</p>
                                            <p><strong>Rating: </strong>{{ show.rating }}</p>
                                            <p><strong>Price: </strong>{{ show.price }}</p>
                                        </div>
                                    </div>


                                </div>
                            </div>
                            <hr />
                            <div class="pt-2">
                                <div class="d-flex pb-2">
                                    <div>
                                        <p>
                                            <b>Choose Payment Options </b>
                                        </p>
                                    </div>

                                </div>

                                <form class="pb-3">
                                    <div class="d-flex flex-row pb-3">
                                        <div class="d-flex align-items-center pe-2">
                                            <input class="form-check-input" type="radio" name="radioNoLabel"
                                                id="radioNoLabel1" value="" aria-label="..." checked />
                                        </div>
                                        <div class="rounded border d-flex w-100 p-3 align-items-center">
                                            <p class="mb-0">
                                                <i class="fab fa-cc-visa fa-lg text-primary pe-2"></i>Visa Debit
                                                Card
                                            </p>
                                            <div class="ms-auto">************3456</div>
                                        </div>
                                    </div>

                                    <div class="d-flex flex-row">
                                        <div class="d-flex align-items-center pe-2">
                                            <input class="form-check-input" type="radio" name="radioNoLabel"
                                                id="radioNoLabel2" value="" aria-label="..." />
                                        </div>
                                        <div class="rounded border d-flex w-100 p-3 align-items-center">
                                            <p class="mb-0">
                                                <i class="fab fa-cc-mastercard fa-lg text-dark pe-2"></i>Mastercard
                                                Office
                                            </p>
                                            <div class="ms-auto">************1038</div>
                                        </div>
                                    </div>
                                </form>

                                <!-- Button trigger modal -->
                                <button type="button" class="btn btn-primary" data-bs-toggle="modal"
                                    data-bs-target="#exampleModal" v-if="user">
                                    Proceed to payment
                                </button>
                                <button type="button" class="btn btn-warning" v-if="!user" @click="redirect">
                                    Login to proceed </button>

                                <!-- Modal -->
                                <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel"
                                    aria-hidden="true">
                                    <div class="modal-dialog">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h1 class="modal-title fs-5" id="exampleModalLabel">Enter your cvv</h1>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal"
                                                    aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <div class="col-md-6">
                                                    <div class="d-flex flex-column pe-md-5 px-md-0 px-4 mb-4">
                                                        <span>CVV</span>
                                                        <div class="inputWithIcon">
                                                            <input type="password" class="form-control" placeholder="cvv"
                                                                value="123">

                                                        </div>
                                                    </div>
                                                </div>


                                            </div>
                                            <div class="modal-footer">
                                                <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
                                                    @click="order">Continue</button>


                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="col-md-5 col-xl-4 offset-xl-1">
                            <div class="py-4 d-flex justify-content-end">
                                <RouterLink :to="`/book?id=${$route.query.id}`" class="cancel-link">Click here to go back
                                </RouterLink>

                            </div>
                            <div class="rounded d-flex flex-column p-2" style="background-color: #f8f9fa;">
                                <div class="p-2 me-3">
                                    <h4>Order Recap</h4>
                                </div>
                                <div class="p-2 d-flex">
                                    <div class="col-8">Sub Total</div>
                                    <div class="ms-auto">₹{{ show.price }}</div>
                                </div>
                                <div class="p-2 d-flex">
                                    <div class="col-8">Discount</div>
                                    <div class="ms-auto">-₹{{ discount }}</div>
                                </div>
                                <div class="p-2 d-flex">
                                    <div class="col-8">Taxes and Charges <span class="gst">(includes G.S.T)</span> </div>
                                    <div class="ms-auto">+ ₹{{ taxes }}</div>
                                </div>

                                <div class="border-top px-2 mx-2"></div>
                                <div class="p-2 d-flex pt-3">
                                    <div class="col-8">Food & Bevarages</div>
                                    <div class="ms-auto">
                                        <div class="checkbox-wrapper-35">
                                            <input class="switch" type="checkbox" id="switch" name="switch" value="food"
                                                v-model="food" @change="calculateTotal">
                                            <label for="switch">
                                                <span class="switch-x-text">🍕</span>
                                                <span class="switch-x-toggletext">
                                                    <span class="switch-x-unchecked"><span
                                                            class="switch-x-hiddenlabel">Unchecked: </span>0</span>
                                                    <span class="switch-x-checked"><span
                                                            class="switch-x-hiddenlabel">Checked:
                                                        </span>₹{{ foodPrice }}</span>
                                                </span>
                                            </label>
                                        </div>


                                    </div>
                                </div>
                                <div class="p-2 d-flex pt-3">
                                    <div class="col-8">Total number of Tickets</div>
                                    <div class="ms-auto">{{ this.$route.query.seatsBoooked }}</div>
                                </div>

                                <div class="border-top px-2 mx-2"></div>


                                <div class="border-top px-2 mx-2"></div>
                                <div class="p-2 d-flex pt-3">
                                    <div class="col-8"><b>Total</b></div>
                                    <div class="ms-auto"><b class="text-success">₹{{ total }}</b></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from '../axios';
export default {
    name: "PaymentView",
    data() {
        return {
            show: null,
            food: 0,

            count: 1,
            discount: 10,
            total: 10,
            taxes: 0,
            confirm: true,

        }
    },
    computed: {
        foodPrice() {
            return this.food === true ? 40 : 0;
        },
        ...mapGetters(['user']),


    },


    methods: {
        redirect() {
            localStorage.setItem('redirect', '/payment?id=' + this.$route.query.id + '&seatsBoooked=' + this.$route.query.seatsBoooked);
            this.$router.push('/login');

        },
        getImageURL() {
            return require(`@/assets/${this.show.venue_id}.${this.show.show_name}.jpg`);
        }, calculateTotal() {
            let foodCost = this.food === true ? 40 : 0;
            this.total =
                this.show.price * this.$route.query.seatsBoooked +
                foodCost - this.discount + this.taxes;
        },
        async order() {
            const id = this.show.venue_id;
            const capacity = this.show.venues.capacity - this.$route.query.seatsBoooked;
            const data = {

                capacity
            };
           await axios.put('api/venues/' + id, data);
           await axios.post('api/bookings',
                {
                    rating: 0.0,
                    user_id: this.user.id,
                    show_id: this.show.id,
                    seat_booked: this.$route.query.seatsBoooked,
                    timing : new Date().toLocaleString("en-US", {timeZone: "Asia/Kolkata"})
                }
            )
            this.$router.push('/order');
        }

    },
    async created() {
        try {
      
      const response = await axios.get('user')
      this.$store.dispatch('user', response.data)
    } catch (error) {
      console.log("error in getting user")
    }
        const id = this.$route.query.id;
        const response = await axios.get("api/shows/" + id);
        this.show = response.data;
        this.discount = this.show.price * this.$route.query.seatsBoooked * 0.1;
        this.taxes = this.show.price * this.$route.query.seatsBoooked * 0.18;
        this.total =
            this.show.price * this.$route.query.seatsBoooked +
            this.food - this.discount + this.taxes;
    },
}
</script>

<style scoped>
.form-control {
    box-shadow: none;
}

.checkbox-wrapper-35 .switch {
    display: none;
}

.checkbox-wrapper-35 .switch+label {
    -webkit-box-align: center;
    -webkit-align-items: center;
    -ms-flex-align: center;
    align-items: center;
    color: #78768d;
    cursor: pointer;
    display: -webkit-box;
    display: -webkit-flex;
    display: -ms-flexbox;
    display: flex;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 12px;
    line-height: 15px;
    position: relative;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}

.checkbox-wrapper-35 .switch+label::before,
.checkbox-wrapper-35 .switch+label::after {
    content: '';
    display: block;
}

.checkbox-wrapper-35 .switch+label::before {
    background-color: #05012c;
    border-radius: 500px;
    height: 15px;
    margin-right: 8px;
    -webkit-transition: background-color 0.125s ease-out;
    transition: background-color 0.125s ease-out;
    width: 25px;
}

.checkbox-wrapper-35 .switch+label::after {
    background-color: #fff;
    border-radius: 13px;
    box-shadow: 0 3px 1px 0 rgba(37, 34, 71, 0.05), 0 2px 2px 0 rgba(37, 34, 71, 0.1), 0 3px 3px 0 rgba(37, 34, 71, 0.05);
    height: 13px;
    left: 1px;
    position: absolute;
    top: 1px;
    -webkit-transition: -webkit-transform 0.125s ease-out;
    transition: -webkit-transform 0.125s ease-out;
    transition: transform 0.125s ease-out;
    transition: transform 0.125s ease-out, -webkit-transform 0.125s ease-out;
    width: 13px;
}

.checkbox-wrapper-35 .switch+label .switch-x-text {
    display: block;
    margin-right: .3em;
}

.checkbox-wrapper-35 .switch+label .switch-x-toggletext {
    display: block;
    font-weight: bold;
    height: 15px;
    overflow: hidden;
    position: relative;
    width: 25px;
}

.checkbox-wrapper-35 .switch+label .switch-x-unchecked,
.checkbox-wrapper-35 .switch+label .switch-x-checked {
    left: 0;
    position: absolute;
    top: 0;
    -webkit-transition: opacity 0.125s ease-out, -webkit-transform 0.125s ease-out;
    transition: opacity 0.125s ease-out, -webkit-transform 0.125s ease-out;
    transition: transform 0.125s ease-out, opacity 0.125s ease-out;
    transition: transform 0.125s ease-out, opacity 0.125s ease-out, -webkit-transform 0.125s ease-out;
}

.checkbox-wrapper-35 .switch+label .switch-x-unchecked {
    opacity: 1;
    -webkit-transform: none;
    transform: none;
}

.checkbox-wrapper-35 .switch+label .switch-x-checked {
    opacity: 0;
    -webkit-transform: translate3d(0, 100%, 0);
    transform: translate3d(0, 100%, 0);
}

.checkbox-wrapper-35 .switch+label .switch-x-hiddenlabel {
    position: absolute;
    visibility: hidden;
}

.checkbox-wrapper-35 .switch:checked+label::before {
    background-color: #ffb500;
}

.checkbox-wrapper-35 .switch:checked+label::after {
    -webkit-transform: translate3d(10px, 0, 0);
    transform: translate3d(10px, 0, 0);
}

.checkbox-wrapper-35 .switch:checked+label .switch-x-unchecked {
    opacity: 0;
    -webkit-transform: translate3d(0, -100%, 0);
    transform: translate3d(0, -100%, 0);
}

.checkbox-wrapper-35 .switch:checked+label .switch-x-checked {
    opacity: 1;
    -webkit-transform: none;
    transform: none;
}

#red {
    font-family: 'Lily Script One', cursive;
    color: red;
}

.gst {
    font-size: 12px;
    font-weight: 600;
}

.accordion-button:focus {
    z-index: 3;
    /* border-color: var(--bs-accordion-btn-focus-border-color); */
    outline: 0;
    box-shadow: none;
}

.accordion-item {
    margin-top: 10px;
}

.cancel-link {
    text-decoration: none;
    color: #ef0b0b;




}


</style>
