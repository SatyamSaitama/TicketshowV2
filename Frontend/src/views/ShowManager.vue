<template>
    <div>
        <nav class="navbar navbar-expand-lg bg-body-tertiary">

            <ul class="navbar-nav me-auto mb-2 mb-lg-0 ">
                <li class="nav-item">
                    <RouterLink class="nav-link" aria-current="page" to="/admin">Home</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" to="/venues">My Venues</RouterLink>
                </li>
            </ul>
        </nav>
        <div class="container my-5 sm">
            <div class="col-md-2">
                <h1>My Shows!</h1>
            </div>

            <div class="container mt-4">
                <div class="row row-cols-1 row-cols-md-3 g-4">
                    <div class="col">
                        <div class="card h-100">
                            <div class="card-body d-flex flex-column justify-content-center align-items-center">
                                <div class="d-flex flex-column align-items-center">
                                    <div class="btn-group" role="group">
                                        <span class="display-4 ">

                                            <button type="button" class="btn  btn-outline-info" data-bs-toggle="modal"
                                                :data-bs-target="`#createShowModal`">+</button>
                                        </span>

                                        <!-- Modal -->
                                        <div class="modal fade" :id="`createShowModal`" tabindex="-1"
                                            aria-labelledby="exampleModalLabel" aria-hidden="true">
                                            <div class="modal-dialog">
                                                <div class="modal-content">
                                                    <form @submit.prevent="createShowHandler">
                                                        <div class="modal-body">
                                                            <h2 class="text-center mb-4">Book a Show</h2>
                                                            <p class="text-success" id="message"></p>
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
                                                            <input type="datetime-local" class="form-control" id="timing"
                                                                v-model="formData.timing" required>
                                                            </div>
                                                            <div class="form-group">
                                                                <label for="rating">GENRES</label>
                                                            <select class="form-control" id="tags" v-model="formData.tags"
                                                                required>
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
                                                                    :placeholder="pricePlaceholder" step="0.01" required>
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
                                                                <button type="button"
                                                                @click="uploadImage">Upload</button>
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
                                        <h5 class="card-title">{{ row.show_name }}</h5>

                                        <div class="d-flex flex-column align-items-center">
                                            <span class="display-4 text-primary mb-4"></span>

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
                                                            <form  @submit.prevent="editHandler(row.id)">
                                                                <div class="modal-body">

                                                                    <h2 class="text-center mb-4">Book a Show</h2>
                                                                    <p class="text-success" :id="`messageEdit${row.id}`"></p>
                                                                    <div class="form-group">
                                                                        <label for="show_name">Show Name</label>
                                                                        <input type="text" class="form-control"
                                                                    :placeholder="row.show_name"
                                                                    id="show_name"
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
                                                                        <input type="number"
                                                                        
                                                                         class="form-control" id="price"
                                                                            v-model.number="formData.price" :min="minPrice"
                                                                            :placeholder="row.price" step="0.01"
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
                                                                <button 
                                                                type="button"
                                                                            @click="uploadImage">Upload</button>
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
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </template>
                </div>
            </div>

            <!-- Modal -->
            <template v-if="rows.length > 0">
                <template v-for="row in sortedRows" :key="row.id">
                    <div class="modal fade" :id="`deleteModal${row.id}`" tabindex="-1" role="dialog"
                        aria-labelledby="deleteModalLabel" aria-hidden="true">
                        <div class="modal-dialog" role="document">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="deleteModalLabel">Delete Show</h5>
                                    <button type="button" class="close" data-bs-dismiss="modal" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                    </button>
                                </div>
                                <div class="modal-body">
                                    Are you sure you want to delete this show?
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                                    <button type="button" class="btn btn-danger" @click="deleteHandler(row.id)"
                                        data-bs-dismiss="modal">Delete</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
            </template>
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
    name: 'ShowManager',
    data() {
        return {
            rows: [],
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
        closeAction() {
            this.formData = {
                show_name: '',
                rating: '',
                timing: '',
                tags: '',
                price: 0,
                yt_link: '',
                venue_id: this.$route.query.id,
            };

        },
        handleFileChange(event) {
            this.selectedFile = event.target.files[0];
        },
        async uploadImage() {
            const data = new FormData();
            const customFileName = `${this.$route.query.id}.${this.formData.show_name}.jpg`; // Replace with your desired custom filename
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
        editHandler(id) {
            const data = this.formData;
            axios.put(`/api/shows/${id}`, data);
            document.getElementById(`messageEdit${id}`).innerHTML = "✅ Show Updated!"
            setTimeout(() => {
                document.getElementById(`messageEdit${id}`).innerHTML = ""
            }, 3000);
            this.showManager();
        },
        hideToast() {
            this.showToastFlag = false;
        },
        async deleteHandler(id) {
            const resp =await axios.get ('/api/bookings')
            for (let show of resp.data){
                if (show.show_id === id){
                    alert("please don't delete it")
                    console.log("its deleted")
                    return 
                }
            }
            await axios.delete(`/api/shows/${id}`);
            
            this.showManager();
            this.showToastFlag = true;
            document.getElementById('content').innerHTML = "Show Deleted!"
            setTimeout(() => {
                this.showToastFlag = false;
            }, 3000);
        },
        async createShowHandler() {
            const data = this.formData;
            await axios.post('api/shows', data);
            document.getElementById('message').innerHTML = "✅ Show Created!"
            setTimeout(() => {
                document.getElementById('message').innerHTML = ""
            }, 3000);
            await this.showManager();
        },
        async showManager() {
            try {
                const id = this.$route.query.id;
                const response = await axios.get('/api/venues/' + id);
                this.rows = response.data.shows;

            } catch (error) {
                this.$router.push('/admin_login');
            }
        }
    },
    computed: {
        sortedRows() {
            // Sort the 'rows' array based on the 'id' attribute in reverse order
            return this.rows.slice().sort((a, b) => b.id - a.id);
        },
    },
    async created() {
        await this.showManager()
    },
};
</script>
  
<style scoped>.toast {
    position: absolute;
    top: 0;
    right: 0;
    margin: 1rem;
    z-index: 1000;
}</style>