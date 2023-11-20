<template>
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h2>{{ title }}</h2>
        <p>{{ content }}</p>
        <button @click="closeModal">Close</button>
      </div>
    </div>
    
  </template>
  
  <script scoped>
  export default {
    name: 'popupComponent',
    props: {
      showModal: {
        type: Boolean,
        required: true,
      },
      title: {
        type: String,
        required: true,
      },
      content: {
        type: String,
        required: true,
      },
    },
    methods: {
      closeModal() {
        this.$emit("close");
      },
    },
  };
  </script>
  
  <style>
  /* Style the modal here */
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }
  
  button {
    margin-top: 10px;
  }
  </style>
  