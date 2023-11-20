import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:3000/',
});

instance.interceptors.request.use(
  (config) => {
    // Get the latest token from localStorage and set the Authorization header
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = 'Bearer ' + token;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default instance;
