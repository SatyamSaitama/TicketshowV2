<template>
    <div class="my-0">
        <NavbarComponent :isLocation="false" />
        <div class="custom-container">

            <div class="card" v-if="show">
                <img :src="`https://image-service-53fa.onrender.com/images/${show.venue_id}.${show.show_name}`" class="card-img-top"
                    :alt="show.show_name">

            </div>


            <div class="card" aria-hidden="true" v-else>
                <img src="https://placehold.co/600x400?text=..." class="card-img-top" alt="Loading">
                <div class="card-body">
                    <h5 class="card-title placeholder-glow">
                        <span class="placeholder col-6"></span>
                    </h5>
                    <p class="card-text placeholder-glow">
                        <span class="placeholder col-7"></span>
                        <span class="placeholder col-4"></span>
                        <span class="placeholder col-4"></span>
                        <span class="placeholder col-6"></span>
                        <span class="placeholder col-8"></span>
                    </p>

                </div>
            </div>
            <!-- Button trigger modal -->
            <div class="videoDiv">
                <button type="button" class="button-85" data-bs-toggle="modal" data-bs-target="#videoModal"
                    @click="extractVideoId">
                    watch trailer
                </button>

                <!-- Modal -->
                <div class="modal fade" id="videoModal" tabindex="-1" role="dialog" aria-labelledby="videoModalLabel"
                    aria-hidden="true" v-if="show">
                    <div class="modal-dialog modal-dialog-centered" role="document">
                        <div class="modal-content" id="videoContent">
                            <div class="modal-header">
                                <h5 class="modal-title" id="videoModalLabel">{{ show.show_name }} Video</h5>

                            </div>
                            <div class="modal-body text-center">
                                <div class="embed-responsive embed-responsive-16by9 ">
                                    <iframe width="548" height="320" top="-45" left="10"
                                        :src="`https://www.youtube.com/embed/${videoId}`" title="YouTube video player"
                                        frameborder="0"
                                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                                        allowfullscreen></iframe>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>


            <div class="container-content" v-if="!show">
                <p class="card-text placeholder-glow" id="contentPlaceholder">

                    <span class="placeholder col-7"></span>
                    <span class="placeholder col-4"></span>
                    <span class="placeholder col-4"></span>
                    <span class="placeholder col-6"></span>
                    <span class="placeholder col-8"></span>
                    <span class="placeholder col-7"></span>
                    <span class="placeholder col-4"></span>
                    <span class="placeholder col-4"></span>
                    <span class="placeholder col-6"></span>
                    <span class="placeholder col-8"></span>
                </p>
            </div>

            <div class="container-content" v-else>
                <h3>{{ show.show_name }}</h3>
                <hr>

                <div class="row">
                    <div class="col-md-6">
                        <p class="mb-2"><strong>Venue:</strong> {{ show.venues.name }}</p>
                        <p class="mb-2"><strong>Location:</strong> {{ show.venues.location }}</p>
                        <p class="mb-2"><strong>Capacity:</strong> {{ show.venues.capacity }}</p>
                        <p class="mb-2 text-danger"><strong>Timing:</strong>
                            {{ show.timing.slice(8, 10) + "-" + show.timing.slice(5, 7) + "-" + show.timing.slice(0, 4) }},
                            {{ show.timing.slice(11, 16) }}
                        </p>
                        <p class="mb-2"><strong>Genre:</strong> {{ show.tags }}</p>
                        <p class="mb-2"><strong>Rating:</strong> {{ show.rating }}</p>
                        <p class="mb-2"><strong>Price:</strong> {{ show.price }}</p>
                    </div>
                    <!-- if showtime has passed there should not be any button -->
                    <div class="col-md-6 text-center" 
                    v-if="new Date(show.timing) > new Date()"
                    >
                        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal"
                            v-if="show.venues.capacity > 0">
                            Book Now
                        </button>
                        <RouterLink to="/">
                            <button class="btn btn-danger mt-3 mt-md-0" v-if="show.venues.capacity <= 0">Houseful</button>
                        </RouterLink>
                        
                    </div>
                </div>
                <hr>

                <!-- Modal -->
                <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel"
                    aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h1 class="modal-title fs-5" id="exampleModalLabel">Choose Number of Seats</h1>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <label for="quantity">Quantity:</label>
                                <div class="input-group">
                                    <div class="input-group-prepend">
                                        <button class="btn btn-secondary" @click="decrement">-</button>
                                    </div>
                                    <input type="text" class="form-control text-center" v-model="count">
                                    <div class="input-group-append">
                                        <button class="btn btn-secondary" @click="increment">+</button>
                                    </div>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-danger" @click="toPayment"
                                    data-bs-dismiss="modal">Confirm</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="description-content" style="line-height: 6px;">
                <h3>Description</h3>
                <hr>
                <p> <b>IMDB Rating: </b>{{ IMDBRating }}</p>
                <p style="line-height:20px"> <b>Plot: </b>{{ plot }}</p>
                <p><b>Actors: </b>{{ Actors }}</p>
                <p><b>Director: </b>{{ Director }}</p>
            </div>
           <section 
 id="section">
                <div class="container bootstrap snippets bootdey">
                    <h3 style="    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
">Comments</h3>
                    <div class="row">
                        <div class="col-md-12">
                            <div class="blog-comment">
                              
                                <hr />
                                <ul class="comments">
                                    <li class="clearfix" v-for="(comment, index) in comments" :key="index">
                                        <img :src=" `https://api.multiavatar.com/${comment.user_id}.png?apikey=OwWtNfcb5ZgUTy`" class="avatar" alt="">

                                        <div class="post-comments">
                                            <p class="meta">{{ comment.time }} User{{ comment.user_id }} says : <i class="pull-right"><a
                                                        href="#"><small>Reply</small></a></i></p>
                                            <p>{{ comment.text }}</p>
                                        </div>
                                    </li>
                                    <li class="clearfix" v-if="!comments.length">
                                        <div class="post-comments">
                                            <p class="meta">No comments yet</p>
                                        </div></li>

                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

        </div>

    </div>
</template>

<script>
import NavbarComponent from "@/components/NavbarComponent.vue";
import axios from '../axios';
import { mapGetters } from "vuex";

export default {
    name: "BookingView",
    components: {
        NavbarComponent,
    },
    data() {
        return {
            count: 1,
            show: null,
            videoId: 'u31qwQUeGuM',
            comments: [],
            Actors: '',
            Director: '',
            IMDBRating: '',
            plot: '',



        };
    },
    methods: {
        async showDetails() {
            const OMDB_API_KEY = '34ea11c2'; // Replace with your actual OMDB API key
            const showName = this.show.show_name; // Replace with the show_name you want to search for

            fetch(`https://www.omdbapi.com/?apikey=${OMDB_API_KEY}&t=${showName}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(showData => {
                    if (showData && showData.Response === 'True') {
                        console.log('Show data:', showData);
                        this.Actors = showData.Actors;
                        this.Director = showData.Director;
                        this.IMDBRating = showData.imdbRating;
                        this.plot = showData.Plot;
                    } else {
                        console.log('Show not found');
                    }
                })
                .catch(error => {
                    console.error('Error fetching show data:', error);
                });
        },
        extractVideoId() {
            // Extract the video ID from the YouTube link
            const youtubeLink = this.show.yt_link
            this.videoId = youtubeLink.split("?v=")[1];
        },
        increment() {
            this.count = this.count + 1
            if (this.count >= this.show.venues.capacity) {
                this.count = this.show.venues.capacity
            }
        },
        decrement() {
            this.count = this.count - 1
            if (this.count < 1) {
                this.count = 1
            }
        },
        toPayment() {

            this.$router.push({
                name: "PaymentView",
                query: {
                    id: this.show.id,
                    seatsBoooked: this.count,
                },
            });
        },

    },
    computed: {
        ...mapGetters(["user"]),
    },
    async created() {
        try {
         
            const response = await axios.get('user')
            this.$store.dispatch('user', response.data)
        } catch (error) {
            console.log("error in getting user")
        }
        const id = this.$route.query.id;
        await axios.get("api/shows/" + id).then((response) => {
            this.show = response.data;
           
        }).then(() => {
            this.showDetails()
        })
        await axios.get("comment/" + id).then((response) => {
            this.comments = response.data;
        
        })





    },
};
</script>

<style scoped lang="scss">
.blog-comment::before,
.blog-comment::after,
.blog-comment-form::before,
.blog-comment-form::after {
    content: "";
    display: table;
    clear: both;
}

.blog-comment {
    padding-left: 15%;
    padding-right: 15%;
}

.blog-comment ul {
    list-style-type: none;
    padding: 0;
}

.blog-comment img {
    opacity: 1;
    filter: Alpha(opacity=100);
    -webkit-border-radius: 4px;
    -moz-border-radius: 4px;
    -o-border-radius: 4px;
    border-radius: 4px;
}

.blog-comment img.avatar {
    position: relative;
    float: left;
    margin-left: 0;
    margin-top: 0;
    width: 65px;
    height: 65px;
}

.blog-comment .post-comments {
    border: 1px solid #eee;
    margin-bottom: 20px;
    margin-left: 85px;
    margin-right: 0px;
    padding: 10px 20px;
    position: relative;
    -webkit-border-radius: 4px;
    -moz-border-radius: 4px;
    -o-border-radius: 4px;
    border-radius: 4px;
    background: #fff;
    color: #6b6e80;
    position: relative;
}

.blog-comment .meta {
    font-size: 13px;
    color: #aaaaaa;
    padding-bottom: 8px;
    margin-bottom: 10px !important;
    border-bottom: 1px solid #eee;
}

.blog-comment ul.comments ul {
    list-style-type: none;
    padding: 0;
    margin-left: 85px;
}

.blog-comment-form {
    padding-left: 15%;
    padding-right: 15%;
    padding-top: 40px;
}

.blog-comment h3,
.blog-comment-form h3 {
    margin-bottom: 40px;
    font-size: 26px;
    line-height: 30px;
    font-weight: 800;
}

.description-content {
    margin-top: 0px;
    width: 840px;
    text-overflow: ellipsis;

    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    height: 10px;
    position: relative;
    top: -169px;
    left: 375px;

}


#videoContent {
    background-color: #000000;
    color: #ffffff;
    padding: 20px;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    top: 30px;
    left: 0;
    height: 450px
}

#videoModal {
    --bs-modal-zindex: 1055;
    --bs-modal-width: 612px;
}

.button-2 {
    background-color: rgba(51, 51, 51, 0.05);
    border-radius: 8px;
    border-width: 0;
    color: #333333;
    cursor: pointer;
    display: inline-block;
    font-family: "Haas Grot Text R Web", "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 14px;
    font-weight: 500;
    line-height: 20px;
    list-style: none;
    margin: 0;
    padding: 10px 12px;
    text-align: center;
    transition: all 200ms;
    vertical-align: baseline;
    white-space: nowrap;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
}

#contentPlaceholder {
    position: relative;
    top: 80px;
    left: 99px;
}

.container-content {
    margin-top: 0px;
    width: 840px;
    height: 330px;
    position: relative;
    top: -169px;
    left: 375px;
    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;

}

.card:hover {
    box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.5);
    transform: scale(1.05);
    transition: all 0.3s ease-in-out;
    cursor: pointer;

}

.card {
    height: 278px;
    width: 193px;
    border-radius: 13px;
    box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.2);
    position: relative;
    top: 126px;
    left: 49px;
}

.card-img-top {
    position: relative;
    top: 0;
    left: 0;
    height: 279px;
    width: 191px;
    border-radius: 13px;

    object-fit: cover;
}


/* Custom CSS */
.custom-container {
    /* Remove the position: fixed; property */
    /* position: fixed; */
    top: 0;
    left: 0;
    width: 99vw;
    height: 100%;
    margin: 0;
    padding: 0;
    margin-top: 1px;
    display: flex;
    justify-content: left;
    align-items: left;
    flex-direction: column;
}

.modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    top: 100px;
    left: 0;
}



.button-85 {
    padding: 0.6em 3em;
    border: none;
    outline: none;
    color: rgb(255, 255, 255);
    background: #111;
    cursor: pointer;
    position: relative;
    z-index: 0;
    border-radius: 10px;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
}


.videoDiv {
    position: relative;
    top: 130px;
    left: 5px;
    height: 0;
    width: 191px;
    border-radius: 13px;
    margin-top: 10px;
    margin-left: 50px;
    margin-bottom: 10px;
    margin-right: 50px;
    object-fit: cover;
}

.comment-header {
    position: relative;
    top: 130px;
    left: 50px;
    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    font-size: 30px;
    font-weight: 500;
    line-height: 20px;
    list-style: none;
    margin: 0;
    padding: 10px 12px;
    text-align: center;
    transition: all 200ms;
    vertical-align: baseline;
    white-space: nowrap;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
}
/* Cool Gradient Background */
body {
    background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
    height: 100vh;
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* Example usage in a div container */
.custom-container  {
    // fit 
    background: linear-gradient(135deg, #dd65f6 0% 0%, #fda085 100%);
    border-radius: 20px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}



/* Optional: Adding a blur effect */
.blur-background {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: inherit;
    filter: blur(20px);
    z-index: -1;
}
@media only screen and (max-width: 600px) {
    .description-content, .container-content{
        all: unset;
     }

//     .blog-comment::before,
// .blog-comment::after,
// .blog-comment-form::before,
// .blog-comment-form::after {
//     content: "";
//     display: table;
//     clear: both;
// }

// .blog-comment {
//     padding-left: 15%;
//     padding-right: 15%;
// }

// .blog-comment ul {
//     list-style-type: none;
//     padding: 0;
// }

// .blog-comment img {
//     opacity: 1;
//     filter: Alpha(opacity=100);
//     -webkit-border-radius: 4px;
//     -moz-border-radius: 4px;
//     -o-border-radius: 4px;
//     border-radius: 4px;
// }

// .blog-comment img.avatar {
//     position: relative;
//     float: left;
//     margin-left: 0;
//     margin-top: 0;
//     width: 65px;
//     height: 65px;
// }

// .blog-comment .post-comments {
//     border: 1px solid #eee;
//     margin-bottom: 20px;
//     margin-left: 85px;
//     margin-right: 0px;
//     padding: 10px 20px;
//     position: relative;
//     -webkit-border-radius: 4px;
//     -moz-border-radius: 4px;
//     -o-border-radius: 4px;
//     border-radius: 4px;
//     background: #fff;
//     color: #6b6e80;
//     position: relative;
// }

// .blog-comment .meta {
//     font-size: 13px;
//     color: #aaaaaa;
//     padding-bottom: 8px;
//     margin-bottom: 10px !important;
//     border-bottom: 1px solid #eee;
// }

// .blog-comment ul.comments ul {
//     list-style-type: none;
//     padding: 0;
//     margin-left: 85px;
// }

// .blog-comment-form {
//     padding-left: 15%;
//     padding-right: 15%;
//     padding-top: 40px;
// }

// .blog-comment h3,
// .blog-comment-form h3 {
//     margin-bottom: 40px;
//     font-size: 26px;
//     line-height: 30px;
//     font-weight: 800;
// }

.description-content {
    margin-top: 0px;
    padding: 10px 20px;

    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    // height: 10px;
    // /position: relative;
    // top:0px;
    // left: 0px;

}


#videoContent {
    background-color: #000000;
    color: #ffffff;
    padding: 20px;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    top: unset;
    left: unset;
    height: unset;
}

// #videoModal {
//     --bs-modal-zindex: 1055;
//     --bs-modal-width: 612px;
// }

// .button-2 {
//     background-color: rgba(51, 51, 51, 0.05);
//     border-radius: 8px;
//     border-width: 0;
//     color: #333333;
//     cursor: pointer;
//     display: inline-block;
//     font-family: "Haas Grot Text R Web", "Helvetica Neue", Helvetica, Arial, sans-serif;
//     font-size: 14px;
//     font-weight: 500;
//     line-height: 20px;
//     list-style: none;
//     margin: 0;
//     padding: 10px 12px;
//     text-align: center;
//     transition: all 200ms;
//     vertical-align: baseline;
//     white-space: nowrap;
//     user-select: none;
//     -webkit-user-select: none;
//     touch-action: manipulation;
// }

#contentPlaceholder {
   position:unset
}

.container-content {
    margin-top: 100px;
    padding: 100px 10px;
    
   
    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;

}
iframe{
    width: 100%;
    height: 100%;
}

// .card:hover {
//     box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.5);
//     transform: scale(1.05);
//     transition: all 0.3s ease-in-out;
//     cursor: pointer;

// }

// .card {
//     height: 278px;
//     width: 193px;
//     border-radius: 13px;
//     box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.2);
//     position: relative;
//     top: 126px;
//     left: 49px;
// }

// .card-img-top {
//     position: relative;
//     top: 0;
//     left: 0;
//     height: 279px;
//     width: 191px;
//     border-radius: 13px;

//     object-fit: cover;
// }


// /* Custom CSS */
// .custom-container {
//     /* Remove the position: fixed; property */
//     /* position: fixed; */
//     top: 0;
//     left: 0;
//     width: 99vw;
//     height: 100%;
//     margin: 0;
//     padding: 0;
//     margin-top: 1px;
//     display: flex;
//     justify-content: left;
//     align-items: left;
//     flex-direction: column;
// }

// .modal-content {
//     background-color: white;
//     padding: 20px;
//     border-radius: 4px;
//     box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
//     top: 100px;
//     left: 0;
// }



// .button-85 {
//     padding: 0.6em 3em;
//     border: none;
//     outline: none;
//     color: rgb(255, 255, 255);
//     background: #111;
//     cursor: pointer;
//     position: relative;
//     z-index: 0;
//     border-radius: 10px;
//     user-select: none;
//     -webkit-user-select: none;
//     touch-action: manipulation;
// }


// .videoDiv {
//     position: relative;
//     top: 130px;
//     left: 5px;
//     height: 0;
//     width: 191px;
//     border-radius: 13px;
//     margin-top: 10px;
//     margin-left: 50px;
//     margin-bottom: 10px;
//     margin-right: 50px;
//     object-fit: cover;
// }

// .comment-header {
//     position: relative;
//     top: 130px;
//     left: 50px;
//     font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
//     font-size: 30px;
//     font-weight: 500;
//     line-height: 20px;
//     list-style: none;
//     margin: 0;
//     padding: 10px 12px;
//     text-align: center;
//     transition: all 200ms;
//     vertical-align: baseline;
//     white-space: nowrap;
//     user-select: none;
//     -webkit-user-select: none;
//     touch-action: manipulation;
// }
// /* Cool Gradient Background */
// body {
//     background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
//     height: 100vh;
//     margin: 0;
//     display: flex;
//     justify-content: center;
//     align-items: center;
// }

// /* Example usage in a div container */
// .custom-container  {
//     // fit 
//     background: linear-gradient(135deg, #dd65f6 0% 0%, #fda085 100%);
//     border-radius: 20px;
//     box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
// }



// /* Optional: Adding a blur effect */
// .blur-background {
//     position: absolute;
//     top: 0;
//     left: 0;
//     right: 0;
//     bottom: 0;
//     background: inherit;
//     filter: blur(20px);
//     z-index: -1;
// }
    
}
</style>
