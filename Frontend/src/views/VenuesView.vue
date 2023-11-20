<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">

<ul class="navbar-nav me-auto mb-2 mb-lg-0 ">
            <li class="nav-item">
                <RouterLink class="nav-link" to="/admin">Home</RouterLink>
            </li>
        </ul></nav>
        <div class="main">
        <div class="container my-5 sm bg-container">
            <div class="col-md-2 ">
                <h1>My Venues !</h1>
            </div>

            <div class="container mt-4">
                <div class="row row-cols-1 row-cols-md-3 g-4">
                    <div class="col">
                        <div class="card h-100">
                            <div class="card-body d-flex flex-column justify-content-center align-items-center">
                                <div class="d-flex flex-column align-items-center">
                                    <div class="btn-group" role="group">
                                        <input type="submit" class="btn btn-outline-primary" data-bs-toggle="modal"
                                            data-bs-target="#exampleModal" value="+" name="+">
                                        <!-- Button trigger modal -->


                                        <!-- Modal -->
                                        <div class="modal fade" id="exampleModal" tabindex="-1"
                                            aria-labelledby="exampleModalLabel" aria-hidden="true">
                                            <div class="modal-dialog">
                                                <div class="modal-content">
                                                    <div class="modal-header">
                                                        <h1 class="modal-title fs-5" id="exampleModalLabel">Create a new
                                                            venue</h1>
                                                        <button type="button" class="btn-close" data-bs-dismiss="modal"
                                                            aria-label="Close" @click="closeAction"></button>
                                                    </div>
                                                    <form @submit.prevent="handleCreated">
                                                    <div class="modal-body">
                                                        <div class="row justify-content-center">
                                                            <div class="col-lg-6">
                                                                <p class="text-success" id="message"> </p>        
                                                                <div class="form-group">
                                                                    <label for="venue">Venue:</label>
                                                                    <input class="form-control form-control-lg" type="text"
                                                                        name="venue" placeholder="Enter venue name" required
                                                                        v-model="name">
                                                                </div>
                                                                <div class="form-group">
                                                                    <label for="place">Place:</label>
                                                                    <input class="form-control form-control-lg" type="text"
                                                                        name="place" placeholder="Enter place" required
                                                                        v-model="place">
                                                                </div>
                                                                <div class="form-group">
                                                                    <label for="location">Location:</label>
                                                                    <input class="form-control form-control-lg" type="text"
                                                                        name="location" placeholder="Enter location"
                                                                        required v-model="location">
                                                                </div>
                                                                <div class="form-group">
                                                                    <label for="capacity">Capacity:</label>
                                                                    <input class="form-control form-control-lg"
                                                                        type="number" name="capacity"
                                                                        placeholder="Enter capacity" required
                                                                        v-model.number="capacity">
                                                                </div>

                                                            </div>
                                                        </div>

                                                    </div>
                                                    <div class="modal-footer">
                                                        <button type="button" class="btn btn-secondary"
                                                            data-bs-dismiss="modal" @click="closeAction">close
                                                        </button>
                                                        <button type="submit" class="btn btn-primary"
                                                             >Create
                                                        </button>
                                                    </div></form>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>


                    <template v-if="rows.length > 0">
                        <template v-for="row in sortedRows" :key="row.id">
                            <div class="col">
                                <div class="card h-100">
                                    <div class="card-body d-flex flex-column justify-content-center align-items-center">
                                        <h5 class="card-title">{{ row.name }}</h5>
                                        <RouterLink :to="`/shows/?id=${row.id}`">
                                            <button class="btn-info">Manage Your
                                                Shows
                                            </button>
                                        </RouterLink>

                                        <div class="d-flex flex-column align-items-center">
                                            <span class="display-4 ">

                                                <button type="button" class="btn  btn-outline-info" data-bs-toggle="modal"
                                                    :data-bs-target="`#createShowModal${row.id}`">+</button>
                                            </span>

                                            <!-- Modal -->
                                            <div class="modal fade" :id="`createShowModal${row.id}`" tabindex="-1"
                                                aria-labelledby="exampleModalLabel" aria-hidden="true">
                                                <div class="modal-dialog">
                                                    <div class="modal-content">
                                                        <form @submit.prevent="createShowHandler(row.id)">
                                                        <div class="modal-body">
                                                            
                                                            <h2 class="text-center mb-4">Book a Show</h2>
                                                            <p class="text-success" :id="`message${row.id}`" style="text-align: left;"> </p>
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
                                                                        v-model.number="formData.price" min="100"
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
                                                                <button type="button" id="upload-btn" @click.prevent="uploadImage(row.id)">Upload</button>
                                                            </div>

                                                        </div>
                                                        
                                                        <div class="modal-footer">
                                                            
                                                            <button type="submit" class="btn btn-primary"
                                                               
                                                                >save</button>



                                                            <button type="button" class="btn btn-secondary"
                                                                data-bs-dismiss="modal" @click="closeAction">Close</button>
                                                        </div></form>
                                                    </div>
                                                </div>
                                            </div>


                                            <div class="btn-group" role="group">

                                                <button type="button" class="btn btn-sm btn-outline-primary"
                                                    data-bs-toggle="modal" :data-bs-target="`#editModal${row.id}`">

                                                    edit
                                                </button>

                                                <!-- Modal -->
                                                <div class="modal fade" :id="`editModal${row.id}`" tabindex="-1"
                                                    aria-labelledby="exampleModalLabel" aria-hidden="true">
                                                    <div class="modal-dialog">
                                                        <div class="modal-content">
                                                            <div class="modal-header">
                                                                <h3 class="modal-title fs-5 text-center"
                                                                    id="exampleModalLabel"> Edit venue
                                                                </h3>
                                                                <button type="button" class="btn-close"
                                                                    data-bs-dismiss="modal" aria-label="Close" @click="closeAction"></button>
                                                            </div>
                                                            <form @submit.prevent="editHandler(row.id)">
                                                            <div class="modal-body">
                                                                <p class="text success" :id="`messageEdit${row.id}`"></p>
                                                                <div class="mb-3">
                                                                    <label for="venue" class="form-label">Venue Name</label>
                                                                    <input class="form-control form-control-lg" type="text"
                                                                        id="venue" name="venue" :placeholder="row.name"
                                                                        v-model="name"
                                                                        required 
                                                                        >
                                                                </div>
                                                                <div class="mb-3">
                                                                    <label for="place" class="form-label">Place</label>
                                                                    <input class="form-control form-control-lg" type="text"
                                                                        id="place" name="place" :placeholder="row.place"
                                                                        v-model="place"
                                                                        required>
                                                                </div>
                                                                <div class="mb-3">
                                                                    <label for="location"
                                                                        class="form-label">Location</label>
                                                                    <input class="form-control form-control-lg" type="text"
                                                                        id="location" name="location"
                                                                        :placeholder="row.location" v-model="location" required>
                                                                </div>
                                                                <div class="mb-3">
                                                                    <label for="capacity"
                                                                        class="form-label">Capacity</label>
                                                                    <input class="form-control form-control-lg"
                                                                        type="number" id="capacity" name="capacity"
                                                                        :placeholder="row.capacity"
                                                                        v-model.number="capacity">
                                                                </div>
                                                            </div>
                                                            <div class="modal-footer">
                                                                <button type="submit" class="btn btn-primary"
                                                                    >save</button>



                                                                <button type="button" class="btn btn-secondary"
                                                                    data-bs-dismiss="modal" @click="closeAction">Close</button>
                                                            </div></form>
                                                        </div>
                                                    </div>
                                                </div>
                                                <button type="button" class="btn btn-sm btn-outline-danger"
                                                    data-bs-toggle="modal" :data-bs-target="`#deleteModal${row.id}`">

                                                    Delete
                                                </button>

                                                <!-- Modal -->
                                                <div class="modal fade" :id="`deleteModal${row.id}`" tabindex="-1"
                                                    aria-labelledby="exampleModalLabel" aria-hidden="true">
                                                    <div class="modal-dialog">
                                                        <div class="modal-content">
                                                            <div class="modal-header">
                                                                <h1 class="modal-title fs-5" id="exampleModalLabel"> Are you
                                                                    sure want to delete the Venue ?
                                                                </h1>
                                                                <button type="button" class="btn-close"
                                                                    data-bs-dismiss="modal" aria-label="Close"></button>
                                                            </div>
                                                            <!-- <div class="modal-body">
      </div> -->
                                                            <div class="modal-footer">
                                                                <button type="button" class="btn btn-danger"
                                                                    data-bs-dismiss="modal"
                                                                    @click="deleteHandler(row.id)">Delete</button>



                                                                <button type="button" class="btn btn-secondary"
                                                                    data-bs-dismiss="modal">Close</button>
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
                    </template>
                </div>
            </div>
            <!-- Toast container -->
            <div class="toast" role="alert" aria-live="assertive" aria-atomic="true"
                :class="{ 'show': showToastFlag, 'hide': !showToastFlag }">
                <div class="toast-header">
                    <strong class="mr-auto" id="content">Venue Deleted!</strong>
                    <button @click="hideToast" type="button" class="ml-2 mb-1 close btn" data-dismiss="toast"
                        aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>

            </div>

        </div>
    </div>
</template>

<script>
import axios from '../axios';
export default {
    name: 'VenuesView',
    data() {
        return {
            rows: [],
            message:'',
            place: '',
            name: '',
            capacity: 0,
            location: '',
            showToastFlag: false,
            selectedFile: null,
            formData: {
                show_name: '',
                rating: '',
                timing: '',
                tags: '',
                price: 0,
                yt_link: '',
                venue_id: null,
            },

        };
    },
    methods: {
        closeAction(){
            this.name = ''
            this.place = ''
            this.location = ''
            this.capacity = 0
            this.formData = {
                show_name: '',
                rating: '',
                timing: '',
                tags: '',
                price: 0,
                capacity: 0,
                yt_link: '',
                venue_id: null,
              };
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
        async createShowHandler(id) {
            this.formData.venue_id = id;
            const data = this.formData;
            await axios.post('/api/shows', data);
            const res = await axios.get('/set_venue');
            this.rows = res.data.rows;
            document.getElementById(`message${id}`).innerHTML = " ✅ Show Created!"
            setTimeout(() => {
                document.getElementById(`message${id}`).innerHTML = ""
            }, 3000);
           
        },
        async editHandler(id) {
            const data = {
                name: this.name,
                place: this.place,
                capacity: this.capacity,
                location: this.location
            }
            axios.put(`api/venues/${id}`, data)
            const res = await axios.get('/set_venue');
            this.rows = res.data.rows;
            document.getElementById(`messageEdit${id}`).innerHTML = " ✅ Venue Edited!"
            setTimeout(() => {
                document.getElementById(`messageEdit${id}`).innerHTML = ""
            }, 3000);
        },

        hideToast() {
            this.showToastFlag = false;
        },
        async deleteHandler(id) {
            await axios.delete(`api/venues/${id}`);
            const res = await axios.get('/set_venue');
            this.rows = res.data.rows;
            document.getElementById('content').innerHTML = "Venue Deleted!"

            this.showToastFlag = true;
            setTimeout(() => {
                this.showToastFlag = false;
            }, 3000);
        },
        async handleCreated() {
            const data = {
                name: this.name,
                place: this.place,
                capacity: this.capacity,
                location: this.location
            }
            await axios.post('api/venues', data)
            const res = await axios.get('/set_venue');
            this.rows = res.data.rows;
            document.getElementById('message').innerHTML = " ✅ Venue Created!"
            setTimeout(() => {
                document.getElementById('message').innerHTML = ""
            }, 3000);

           
           
        }
    },
    computed: {
        sortedRows() {
            // Sort the 'rows' array based on the 'id' attribute in reverse order
            return this.rows.slice().sort((a, b) => b.id - a.id);
        },
    },
    async created() {
        try {
            const response = await axios.get('/set_venue');
            this.rows = response.data.rows;

        } catch (error) {
            localStorage.removeItem('token');
            localStorage.removeItem('role');
        }
    },
};

</script>

<style scoped>.toast {
    position: absolute;
    top: 0;
    right: 0;
    margin: 1rem;
    z-index: 1000;


}
.upload-btn {
            padding: 10px 20px;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

     
        .upload-button:active,
        .upload-button:focus {
            background-color: #0056b3;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        }

        /* Optional: Add more styles to indicate focus */
        .upload-button:focus {
            outline: none;
        }



</style>
  