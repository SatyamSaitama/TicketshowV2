<template>
    <div>
      <!-- Button to trigger the toast -->
      <button @click="showToast" class="btn btn-primary">Show Live Toast</button>
  
      <!-- Toast container -->
      <div
        class="toast"
        role="alert"
        aria-live="assertive"
        aria-atomic="true"
        :class="{ 'show': showToastFlag, 'hide': !showToastFlag }"
      >
        <div class="toast-header">
          <strong class="mr-auto">Live Toast</strong>
          <button @click="hideToast" type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="toast-body">
          This is a live toast notification!
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        showToastFlag: false,
      };
    },
    methods: {
      showToast() {
        this.showToastFlag = true;
        setTimeout(() => {
          this.showToastFlag = false;
        }, 3000); // Hide the toast after 3 seconds
      },
      hideToast() {
        this.showToastFlag = false;
      },
    },
  };
  </script>
  
  <style scoped>
  /* Custom styles for the toast container */
  .toast {
    position: absolute;
    top: 0;
    right: 0;
    margin: 1rem;
    z-index: 1000;
  }
  </style>
  