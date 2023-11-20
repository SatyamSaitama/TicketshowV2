<template>
    
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Admin</a>
           
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">


<li class="nav-item"  >
    <RouterLink to="/venues" class="nav-link" v-if="user && user.role==='admin'" >Mange Venues</RouterLink>
</li>
<li class="nav-item">
    <RouterLink to="/analytics" class="nav-link" v-if="user && user.role==='admin'">Analytics</RouterLink>
</li>







</ul>
            
            <div class=" dropstart" v-if="user && user.role==='admin'">
                
                <div class="material-symbols-outlined" type="button" data-bs-toggle="offcanvas"
                    data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">
                    admin_panel_settings
                </div>



            </div>
            <div class="dropstart" v-else>
                <button class="btn btn-danger btn-sm nav-item dropdown" data-bs-toggle="dropdown">Login</button>
                <ul class="dropdown-menu ">
                    <li>
                        <RouterLink to="/login" class="dropdown-item">Login as user</RouterLink>
                    </li>
                    <li>
                        <RouterLink to="/admin_login" class="dropdown-item">Host as admin</RouterLink>
                    </li>

                </ul>
            </div></div>
            <div class="dropstart">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            </div>

        </div>
    </nav>
    <div class="image-placeholder" v-if="!(user && user.role==='admin')">
        <!-- Login to continue -->
        <img src="../assets/laptop.svg"
        alt="" id="pixabay" > 
    </div>
    <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel"
        v-if="user && user.role==='admin'">
        <div class="offcanvas-header">
            <h5 class="offcanvas-title" id="offcanvasRightLabel">Account</h5>
            <button type="button" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">

            <ul class="list-group">
                <RouterLink to="venues" style="text-decoration: none;">
                    <li class="list-group-item list-group-item-action " aria-current="true"><span
                            class="material-symbols-outlined">
                            subscriptions
                        </span><span class="profile-tab" data-bs-dismiss="offcanvas">Manage Venues</span></li>
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
    <template v-for="venue in venues" :key="venue.id">
        <div>
            
               
            <div class="custom-container">
                <div class=" custom-header text-left h1">
                    {{ venue.name }}
                </div>

                <div class="row row-cols-2 row-cols-md-3 row-cols-lg-5">
                    <template v-for="  object in  venue.shows " :key="object.id">
                        <div class="col mb-4">
                            <div class="card">
                                <div class="card-img-top">
                                    <!-- <RouterLink :to="`/book?id=${object.id}`"> -->
                                    <img :src="`http://localhost:5000/images/${object.venue_id}.${object.show_name}`"
                                        class="card-img-top" :alt="object.show_name"
                                        style="height: 300px; object-fit:cover;">



                                    <div class="card-footer ">
                                        <div class="btn-group" role="group">
                                            <button type="button" class="btn btn-sm btn-outline-primary"
                                                data-bs-toggle="modal" :data-bs-target="`#editModal${object.id}`">

                                                edit
                                            </button>

                                            <!-- Modal -->
                                            <div class="modal fade" :id="`editModal${object.id}`" tabindex="-1"
                                                aria-labelledby="exampleModalLabel" aria-hidden="true">
                                                <div class="modal-dialog">
                                                    <div class="modal-content">

                                                        <div class="modal-body">
                                                            <h2 class="text-center mb-4">Book a Show</h2>
                                                            <div class="form-group">
                                                                <label for="show_name">Show Name</label>
                                                                <input type="text" class="form-control" id="show_name"
                                                                    v-model="formData.show_name" required>
                                                            </div>
                                                            <div class="form-group">
                                                                <label for="rating">Rating</label>
                                                                <select class="form-control" id="rating"
                                                                    v-model="formData.rating" required>
                                                                    <option value="">Select Rating</option>
                                                                    <option value="G">G</option>
                                                                    <option value="PG">PG</option>
                                                                    <option value="PG-13">PG-13</option>
                                                                    <option value="R">R</option>
                                                                    <option value="NC-17">NC-17</option>
                                                                </select>
                                                            </div>

                                                            <div class="form-group">
                                                                <label for="timing">Timing</label>
                                                                <input type="datetime-local" class="form-control"
                                                                    id="timing" v-model="formData.timing" required>
                                                            </div>
                                                            <div class="form-group">
                                                                <label for="rating">GENRES</label>
                                                                <select class="form-control" id="tags"
                                                                    v-model="formData.tags" required>
                                                                    <option value="">Select Genres</option>
                                                                    <option value="Action">Action</option>
                                                                    <option value="Adventure">Adventure</option>
                                                                    <option value="Horror">Horror</option>
                                                                    <option value="Drama">Drama</option>
                                                                    <option value="Animation">Animation</option>
                                                                </select>
                                                            </div>
                                                            <div class="form-group">
                                                                <label for="price">Price</label>
                                                                <div class="input-group">
                                                                    <div class="input-group-prepend">
                                                                        <span class="input-group-text">₹</span>
                                                                    </div>
                                                                    <input type="number" class="form-control" id="price"
                                                                        v-model.number="formData.price" :min="minPrice"
                                                                        :placeholder="pricePlaceholder" step="0.01"
                                                                        required>
                                                                </div>
                                                            </div>


                                                            <div class="form-group">
                                                                <label for="yt_link">YouTube Video Link</label>
                                                                <input type="url" class="form-control" id="yt_link"
                                                                    v-model="formData.yt_link"
                                                                    placeholder="e.g. https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                                                                    required>
                                                            </div>
                                                            <div class="form-group">
                                                                <label for="image">Image</label>
                                                                <input type="file" @change="handleFileChange"
                                                                    accept="image/*" required />
                                                                <button @click="uploadImage(object.venue_id)">Upload</button>
                                                            </div>
                                                        </div>
                                                        <div class="modal-footer">
                                                            <button type="button" class="btn btn-primary"
                                                                data-bs-dismiss="modal"
                                                                @click="editHandler(object.id)">save</button>



                                                            <button type="button" class="btn btn-secondary"
                                                                data-bs-dismiss="modal">Close</button>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                            <button type="button" class="btn btn-sm btn-outline-danger"
                                                data-bs-toggle="modal" :data-bs-target="`#deleteModal${object.id}`">
                                                Delete
                                            </button>
                                            <div class="modal fade" :id="`deleteModal${object.id}`" tabindex="-1"
                                                role="dialog" aria-labelledby="deleteModalLabel" aria-hidden="true">
                                                <div class="modal-dialog" role="document">
                                                    <div class="modal-content">
                                                        <div class="modal-header">
                                                            <h5 class="modal-title" id="deleteModalLabel">Delete Show</h5>
                                                            <button type="button" class="close" data-bs-dismiss="modal"
                                                                aria-label="Close">
                                                                <span aria-hidden="true">&times;</span>
                                                            </button>
                                                        </div>
                                                        <div class="modal-body">
                                                            Are you sure you want to delete this show?
                                                        </div>
                                                        <div class="modal-footer">
                                                            <button type="button" class="btn btn-secondary"
                                                                data-bs-dismiss="modal">Cancel</button>
                                                            <button type="button" class="btn btn-danger"
                                                                @click="deleteHandler(object.id)"
                                                                data-bs-dismiss="modal">Delete</button>
                                                        </div>
                                                    </div>
                                                </div>
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
    
    <div class="toast" role="alert" aria-live="assertive" aria-atomic="true"
        :class="{ 'show': showToastFlag, 'hide': !showToastFlag }">
        <div class="toast-header">
            <strong class="mr-auto" id="content">Venue Deleted!</strong>
            <button @click="hideToast" type="button" class="ml-2 mb-1 close btn" data-dismiss="toast" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>

    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from '../axios';
export default {
    name: 'AdminDashboard',

    data() {
        return {
            venues: [],
            shows: [],
            showToastFlag: false,

            formData: {
                show_name: '',
                rating: '',
                timing: '',
                tags: '',
                price: 0,
                yt_link: '',
                venue_id: this.$route.query.id,
            }, imageFile: null,
        };
    },
    methods: {
        clickHandler() {
            localStorage.removeItem('token');
            this.$store.dispatch('user', null);
            this.$router.push('/admin_login');
            return false;
        },
        handleFileChange(event) {
            this.selectedFile = event.target.files[0];
        },
       async uploadImage(id) {
            const data = new FormData();
            const customFileName = `${id}.${this.formData.show_name}.jpg`; // Replace with your desired custom filename
            data.append("image", this.selectedFile, customFileName);
          await  axios
                .post("http://localhost:5000/upload", data)
                .then((response) => {
                    console.log(response.data);
                    alert("Image uploaded successfully!");
                })
                .catch((error) => {
                    console.error(error);
                });
        },
       async editHandler(id) {
            const data = this.formData;
           await axios.put(`/api/shows/${id}`, data);
            this.showManager();
            this.showToastFlag = true;
            document.getElementById('content').innerHTML = "Show Edited!"
            setTimeout(() => {
                this.showToastFlag = false;
            }, 3000);
        },
        hideToast() {
            this.showToastFlag = false;
        },
        async deleteHandler(id) {
            await axios.delete(`/api/shows/${id}`);
            this.showManager();
            this.showToastFlag = true;
            document.getElementById('content').innerHTML = "Show Deleted!"
            setTimeout(() => {
                this.showToastFlag = false;
            }, 3000);
        },
        async showManager() {
            try {
                const response = await axios.get('/set_venue');
                this.venues = response.data.rows;
            } catch (error) {
                console.error('Error fetching data:', error);
            }


        },
    },
    computed: {
        ...mapGetters(['user']),


    },

    async beforeMount() {
        try {

            const res = await axios.get('user')
            this.$store.dispatch('user', res.data)
            
            this.showManager()

        } catch (error) {
            console.log("error in getting user")
        }
    },

}
</script>

<style scoped>
#pixabay{
    width: 300px;
    height: 360px;
    display: flex;
    object-fit: cover;
    justify-content: center;
    align-items: center;
    margin: 0 auto;
    margin-top: 95px;
    margin-bottom: 50px;

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

.toast {
    position: absolute;
    top: 0;
    right: 0;
    margin: 1rem;
    z-index: 1000;
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



.custom-container {
    width: 99vw;
    height: 100%;
    background-color: #f2f2f2;
    padding: 20px;
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

.card {
    border: none;
    width: 100%;
    background-color: #f2f2f2;
}
.custom-header{
    font-family: 'Rubik', sans-serif;
    font-weight: bolder;
    font-size: 30px;
    margin-bottom: 20px;
    margin-top: 20px;
    color: #000000;
}

</style>